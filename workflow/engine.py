"""
Bộ điều phối quy trình BI 7 Giai đoạn (workflow/engine.py)
Quản lý vòng đời thực thi:
SHEET -> CLEANING -> PROCESS -> VERIFY -> FEEDBACK -> EXPORT -> REPORT
Hỗ trợ vòng lặp "Điều chỉnh & Tái phân tích" (Loopback from Feedback to Process/Cleaning),
áp dụng cơ chế cổng bảo vệ Verify Gate bắt buộc.
"""

import os
import json
from typing import Dict, Any, List
from .state import BIWorkflowState, StageStatus
from .stage_1_sheet import SheetStage
from .stage_2_cleaning import CleaningStage
from .stage_3_process import ProcessStage
from .stage_4_verify import VerifyStage
from .stage_5_feedback import FeedbackStage
from .stage_6_export import ExportStage
from .stage_7_report import ReportStage

class BIWorkflowEngine:
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sheet_stage = SheetStage()
        self.cleaning_stage = CleaningStage()
        self.process_stage = ProcessStage()
        self.verify_stage = VerifyStage()
        self.feedback_stage = FeedbackStage()
        self.export_stage = ExportStage(os.path.join(self.workspace_root, "data", "export"))
        self.report_stage = ReportStage()

    def run_workflow(self, input_files: List[str] = None, user_feedback_decision: str = "APPROVE", feedback_adjustments: Dict[str, Any] = None) -> BIWorkflowState:
        """
        Thực thi toàn bộ quy trình BI qua 7 giai đoạn.
        """
        state = BIWorkflowState()

        # Danh sách file mặc định nếu không truyền
        if not input_files:
            raw_dir = os.path.join(self.workspace_root, "data", "raw")
            input_files = [
                os.path.join(raw_dir, "raw_sales_transactions.csv"),
                os.path.join(raw_dir, "raw_customers.csv"),
                os.path.join(raw_dir, "raw_products.csv"),
                os.path.join(raw_dir, "raw_marketing_campaigns.csv"),
                os.path.join(raw_dir, "raw_operations_logistics.csv")
            ]

        # 1. GIAI ĐOẠN 1: SHEET
        print("[STAGE 1: SHEET] Đang nạp và kiểm tra dữ liệu nguồn...")
        state = self.sheet_stage.execute(state, input_files)

        # 2. GIAI ĐOẠN 2: CLEANING
        print("[STAGE 2: CLEANING] Đang làm sạch, khử trùng lặp và tính Quality Scorecard...")
        state = self.cleaning_stage.execute(state)

        # 3. GIAI ĐOẠN 3: PROCESS
        print("[STAGE 3: PROCESS] Đang tính toán KPI, OLAP rollup và mô hình RFM...")
        state = self.process_stage.execute(state)

        # 4. GIAI ĐOẠN 4: VERIFY (GATE KIỂM CHỨNG)
        print("[STAGE 4: VERIFY] Đang kiểm chứng toán học các công thức và đối chiếu số liệu...")
        state = self.verify_stage.execute(state)

        if not state.verification_passed:
            print(f"[STAGE 4: VERIFY FAILED] Phát hiện {len(state.verification_errors)} lỗi kiểm tra! Khóa xuất báo cáo.")
            self._save_state(state)
            return state

        # 5. GIAI ĐOẠN 5: FEEDBACK & ĐIỀU CHỈNH
        print(f"[STAGE 5: FEEDBACK] Tiếp nhận phản hồi người dùng: {user_feedback_decision}...")
        state = self.feedback_stage.submit_feedback(state, user_feedback_decision, feedback_adjustments)

        # Xử lý vòng lặp nếu có yêu cầu điều chỉnh (Loopback)
        if state.stage_statuses.get("FEEDBACK") == StageStatus.NEEDS_REVISION:
            print("[FEEDBACK LOOPBACK] Người dùng yêu cầu điều chỉnh tham số -> Tái phân tích (PROCESS)...")
            state = self.process_stage.execute(state)
            state = self.verify_stage.execute(state)
            if not state.verification_passed:
                print("[LOOPBACK VERIFY FAILED] Không vượt qua kiểm chứng sau khi điều chỉnh.")
                self._save_state(state)
                return state
            # Cập nhật feedback thành công sau tái phân tích
            state.update_stage_status("FEEDBACK", StageStatus.SUCCESS, "Đã hoàn thành tái phân tích theo yêu cầu.")

        # 6. GIAI ĐOẠN 6: EXPORT
        print("[STAGE 6: EXPORT] Đang xuất dữ liệu sạch và các bảng kết quả đã kiểm chứng...")
        state = self.export_stage.execute(state)

        # 7. GIAI ĐOẠN 7: REPORT
        print("[STAGE 7: REPORT] Đang tổng hợp báo cáo điều hành Minto và cấu trúc Dashboard...")
        state = self.report_stage.execute(state)

        print(f"[WORKFLOW COMPLETE] Toàn bộ 7 giai đoạn hoàn thành xuất sắc! Mã: {state.workflow_id}")
        self._save_state(state)
        return state

    def _save_state(self, state: BIWorkflowState):
        out_path = os.path.join(self.workspace_root, "data", "workflow_execution_state.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    engine = BIWorkflowEngine()
    final_state = engine.run_workflow()
    print("Workflow Result:")
    print("- Verified Passed:", final_state.verification_passed)
    print("- Exported Files:", len(final_state.exported_files))
    print("- Stage Statuses:", final_state.stage_statuses)

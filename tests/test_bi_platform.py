"""
Hệ thống kiểm thử tự động toàn diện (tests/test_bi_platform.py)
Bao gồm:
- Kiểm tra tính toàn vẹn của Data Warehouse và mô hình Star Schema.
- Kiểm tra tính chính xác của các công thức tài chính.
- Kiểm tra Quy trình vận hành cốt lõi 7 Giai đoạn (BI Workflow Engine):
  SHEET -> CLEANING -> PROCESS -> VERIFY -> FEEDBACK -> EXPORT -> REPORT.
- Kiểm tra cơ chế cổng bảo vệ Verify Gate (chặn xuất dữ liệu khi chưa qua kiểm chứng).
- Kiểm tra cơ chế vòng lặp phản hồi (Feedback Revision Loopback).
"""

import unittest
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, "skills"))
sys.path.insert(0, os.path.join(parent_dir, "core"))
sys.path.insert(0, os.path.join(parent_dir, "workflow"))

from workflow.engine import BIWorkflowEngine
from workflow.state import StageStatus, BIWorkflowState

class TestBIPlatformAndWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = BIWorkflowEngine(parent_dir)

    def test_01_full_7_stage_workflow_execution(self):
        """Kiểm tra quy trình chạy xuyên suốt 7 giai đoạn thành công."""
        state = self.engine.run_workflow(user_feedback_decision="APPROVE")
        
        # Kiểm tra trạng thái từng giai đoạn
        self.assertEqual(state.stage_statuses["SHEET"], StageStatus.SUCCESS)
        self.assertEqual(state.stage_statuses["CLEANING"], StageStatus.SUCCESS)
        self.assertEqual(state.stage_statuses["PROCESS"], StageStatus.SUCCESS)
        self.assertEqual(state.stage_statuses["VERIFY"], StageStatus.VERIFIED)
        self.assertEqual(state.stage_statuses["FEEDBACK"], StageStatus.SUCCESS)
        self.assertEqual(state.stage_statuses["EXPORT"], StageStatus.SUCCESS)
        self.assertEqual(state.stage_statuses["REPORT"], StageStatus.SUCCESS)

        self.assertTrue(state.verification_passed, "Bước Verify bắt buộc phải Pass")
        self.assertGreater(len(state.exported_files), 0, "Phải xuất các file báo cáo đã kiểm chứng")
        self.assertGreater(len(state.executive_report), 500, "Báo cáo điều hành phải có nội dung đầy đủ")

    def test_02_verify_gate_enforcement(self):
        """Kiểm tra cơ chế cổng Verify: Khóa xuất dữ liệu khi chưa đạt yêu cầu."""
        fake_state = BIWorkflowState()
        fake_state.verification_passed = False
        fake_state.stage_statuses["VERIFY"] = StageStatus.FAILED

        # Cố gắng xuất dữ liệu khi Verify chưa đạt
        from workflow.stage_6_export import ExportStage
        from workflow.stage_7_report import ReportStage

        export_stage = ExportStage()
        with self.assertRaises(PermissionError, msg="Export phải ném lỗi PermissionError khi Verify Failed"):
            export_stage.execute(fake_state)

        report_stage = ReportStage()
        with self.assertRaises(PermissionError, msg="Report phải ném lỗi PermissionError khi Verify Failed"):
            report_stage.execute(fake_state)

    def test_03_feedback_revision_loopback(self):
        """Kiểm tra cơ chế vòng lặp phản hồi: Điều chỉnh tham số & Tái phân tích."""
        state = self.engine.run_workflow(
            user_feedback_decision="REVISE",
            feedback_adjustments={"quarter_filter": "Q1-2025"}
        )

        self.assertEqual(state.active_adjustments["quarter_filter"], "Q1-2025")
        self.assertTrue(state.verification_passed, "Dữ liệu sau khi tái phân tích phải được Verify lại")
        self.assertGreater(state.kpis["NetRevenue"], 0, "Doanh thu Q1 phải được tính toán chính xác")
        self.assertLess(state.kpis["TotalOrders"], 400, "Số đơn hàng Q1 phải là tập con của cả năm")

    def test_04_mathematical_consistency_reconciliation(self):
        """Kiểm tra đối chiếu số liệu đầu vào - đầu ra."""
        state = self.engine.run_workflow()
        kpis = state.kpis
        
        # Net = Gross - Disc
        self.assertAlmostEqual(
            kpis["NetRevenue"],
            kpis["TotalGrossSales"] - kpis["TotalDiscounts"],
            delta=1.0,
            msg="Net Revenue phải bằng Gross Sales - Discounts"
        )

        # Gross Profit = Net - COGS
        self.assertAlmostEqual(
            kpis["GrossProfit"],
            kpis["NetRevenue"] - kpis["TotalCOGS"],
            delta=1.0,
            msg="Gross Profit phải bằng Net Revenue - Total COGS"
        )

        # Sum of Monthly = Total Net
        sum_monthly = sum(m["Revenue"] for m in state.olap_cubes["monthly_rollup"])
        self.assertAlmostEqual(
            kpis["NetRevenue"],
            sum_monthly,
            delta=1.0,
            msg="Tổng doanh thu các tháng phải bằng Doanh thu thuần cả năm"
        )

if __name__ == "__main__":
    unittest.main()

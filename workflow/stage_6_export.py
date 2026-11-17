"""
Giai đoạn 6: EXPORT (workflow/stage_6_export.py)
Xuất dữ liệu sạch và bảng biểu phân tích ra tệp CSV / JSON.
NGUYÊN TẮC BẢO VỆ CHẶT CHẼ:
Chỉ cho phép xuất file khi state.verification_passed == True và state.stage_statuses['VERIFY'] == VERIFIED.
Nếu chưa kiểm chứng, từ chối xuất dữ liệu để ngăn ngừa sai lệch số liệu quản trị.
"""

import os
import csv
import json
from datetime import datetime
from typing import Dict, Any, List
from .state import BIWorkflowState, StageStatus

class ExportStage:
    def __init__(self, export_dir: str = "data/export"):
        self.stage_name = "EXPORT"
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    def write_csv(self, file_name: str, records: List[Dict[str, Any]]) -> str:
        fpath = os.path.join(self.export_dir, file_name)
        if not records:
            return fpath
        with open(fpath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
        return fpath

    def execute(self, state: BIWorkflowState) -> BIWorkflowState:
        state.update_stage_status("EXPORT", StageStatus.IN_PROGRESS)

        # 1. GATE KEEPER: Kiểm tra trạng thái VERIFY
        if not state.verification_passed or state.stage_statuses.get("VERIFY") != StageStatus.VERIFIED:
            state.update_stage_status("EXPORT", StageStatus.FAILED, "Bị chặn: Dữ liệu chưa qua kiểm chứng Verify.")
            raise PermissionError("[EXPORT GATE ERROR] Không được phép xuất dữ liệu khi bước VERIFY chưa đạt yêu cầu.")

        exported_files = []

        # 2. Xuất bảng dữ liệu sạch (Cleaned Data)
        sales = state.cleaned_data.get("sales", [])
        if sales:
            f1 = self.write_csv("verified_cleaned_sales.csv", sales)
            exported_files.append(f1)

        # 3. Xuất bảng tổng hợp KPI (KPI Summary)
        kpi_dict = state.kpis.get("Formatted", {})
        kpi_records = [{"Metric": k, "Value": v} for k, v in kpi_dict.items()]
        if kpi_records:
            f2 = self.write_csv("verified_kpi_summary.csv", kpi_records)
            exported_files.append(f2)

        # 4. Xuất bảng phân rã doanh thu thời gian (Monthly Rollup)
        monthly = state.olap_cubes.get("monthly_rollup", [])
        if monthly:
            f3 = self.write_csv("verified_monthly_performance.csv", monthly)
            exported_files.append(f3)

        # 5. Xuất phân cụm RFM khách hàng
        rfm_summary = state.analytics_models.get("rfm_segments", {})
        rfm_records = [{"Segment": k, "CustomerCount": v} for k, v in rfm_summary.items()]
        if rfm_records:
            f4 = self.write_csv("verified_rfm_segments.csv", rfm_records)
            exported_files.append(f4)

        state.exported_files = exported_files
        state.export_manifest = {
            "exported_at": datetime.now().isoformat(),
            "export_directory": self.export_dir,
            "total_files": len(exported_files),
            "files": [os.path.basename(f) for f in exported_files],
            "verified_by_gate": True
        }

        state.update_stage_status("EXPORT", StageStatus.SUCCESS)
        return state

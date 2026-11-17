"""
Workflow State (workflow/state.py)
Cấu trúc dữ liệu trạng thái thống nhất trao đổi xuyên suốt 4 giai đoạn BI chuẩn:
1. KẾT NỐI DỮ LIỆU (Connection: Dữ liệu + Bối cảnh + Câu hỏi kinh doanh)
2. LÀM SẠCH DỮ LIỆU (Cleaning: Dữ liệu sạch, có kiểm tra & Verify)
3. PHÂN TÍCH DỮ LIỆU (Analysis: KPI + Phân tích đa chiều + Insight)
4. BÁO CÁO (Reporting: Dashboard + Báo cáo + Xuất tệp + Feedback)
"""

import json
from datetime import datetime
from typing import Dict, Any, List

class StageStatus:
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    # Backward compatibility aliases
    IN_PROGRESS = "PROCESSING"
    SUCCESS = "COMPLETED"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    NEEDS_REVISION = "NEEDS_REVISION"

class BIWorkflowState:
    def __init__(self, workflow_id: str = None):
        self.workflow_id = workflow_id or f"WF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.current_stage = "CONNECTION"
        
        # Trạng thái 4 giai đoạn chuẩn
        self.stage_statuses = {
            "CONNECTION": StageStatus.PENDING,
            "CLEANING": StageStatus.PENDING,
            "ANALYSIS": StageStatus.PENDING,
            "REPORTING": StageStatus.PENDING,
            # Tương thích ngược
            "SHEET": StageStatus.PENDING,
            "PROCESS": StageStatus.PENDING,
            "VERIFY": StageStatus.PENDING,
            "FEEDBACK": StageStatus.PENDING,
            "EXPORT": StageStatus.PENDING,
            "REPORT": StageStatus.PENDING
        }
        
        # 1. KẾT NỐI DỮ LIỆU (Connection)
        self.source_metadata = []
        self.raw_data = {}
        self.business_context = {
            "industry": "Bán lẻ & Thương mại điện tử",
            "business_goals": "Tối ưu hóa doanh thu & biên lợi nhuận",
            "business_questions": [
                "Điều gì đã xảy ra với doanh thu và lợi nhuận qua các kỳ?",
                "Tại sao có sự chênh lệch lớn giữa các kênh và nhóm khách hàng?",
                "Doanh nghiệp nên hành động chiến lược gì để bứt phá tăng trưởng?"
            ]
        }
        
        # 2. LÀM SẠCH DỮ LIỆU & KIỂM TRA (Cleaning & Verify)
        self.cleaning_audit_log = []
        self.cleaned_data = {}
        self.quality_scorecard = {}
        self.verification_passed = False
        self.verification_checks = []
        self.verification_errors = []
        
        # 3. PHÂN TÍCH DỮ LIỆU & INSIGHT (Analysis)
        self.kpis = {}
        self.olap_cubes = {}
        self.analytics_models = {}
        self.insights = []
        
        # 4. BÁO CÁO & PHẢN HỒI (Reporting & Feedback)
        self.dashboard_specs = {}
        self.executive_report = ""
        self.export_manifest = {}
        self.exported_files = []
        self.feedback_history = []
        self.active_adjustments = {
            "quarter_filter": "ALL",
            "channel_filter": "ALL",
            "category_filter": "ALL",
            "min_gross_margin_target": 25.0
        }
        self.dashboard_specs = {}

    def update_stage_status(self, stage: str, status: str, message: str = None):
        self.stage_statuses[stage] = status
        self.current_stage = stage
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "current_stage": self.current_stage,
            "stage_statuses": self.stage_statuses,
            "business_context": self.business_context,
            "source_metadata": self.source_metadata,
            "raw_data_summary": {k: len(v) for k, v in self.raw_data.items()},
            "cleaning_audit_log": self.cleaning_audit_log,
            "quality_scorecard": self.quality_scorecard,
            "kpis": self.kpis,
            "olap_cubes": self.olap_cubes,
            "analytics_models": self.analytics_models,
            "insights": self.insights,
            "verification_passed": self.verification_passed,
            "verification_checks": self.verification_checks,
            "verification_errors": self.verification_errors,
            "feedback_history": self.feedback_history,
            "active_adjustments": self.active_adjustments,
            "export_manifest": self.export_manifest,
            "exported_files": self.exported_files,
            "executive_report": self.executive_report,
            "dashboard_specs": self.dashboard_specs
        }

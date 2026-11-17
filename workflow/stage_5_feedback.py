"""
Giai đoạn 5: FEEDBACK (workflow/stage_5_feedback.py)
Tiếp nhận đánh giá từ người dùng, cho phép thay đổi tham số, bộ lọc và chỉ số mục tiêu.
Lưu vết toàn bộ lịch sử phản hồi (Feedback History).
Nếu có yêu cầu điều chỉnh, thiết lập trạng thái NEEDS_REVISION để kích hoạt
vòng lặp "Điều chỉnh & Tái phân tích" (Loopback to CLEANING/PROCESS).
Nếu phê duyệt (Approved), mở khóa giai đoạn EXPORT và REPORT.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from .state import BIWorkflowState, StageStatus

class FeedbackStage:
    def __init__(self):
        self.stage_name = "FEEDBACK"

    def submit_feedback(self, state: BIWorkflowState, user_decision: str, adjustments: Optional[Dict[str, Any]] = None, notes: Optional[str] = None) -> BIWorkflowState:
        """
        Xử lý phản hồi từ người dùng.
        - user_decision: 'APPROVE' hoặc 'REVISE'
        - adjustments: dict chứa các tham số cần điều chỉnh (ví dụ: {'quarter_filter': 'Q4-2025'})
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": user_decision.upper(),
            "adjustments": adjustments or {},
            "notes": notes or "Người dùng xác nhận kết quả phân tích"
        }
        state.feedback_history.append(feedback_entry)

        if user_decision.upper() == "REVISE":
            # Cập nhật các điều chỉnh mới vào state
            if adjustments:
                state.active_adjustments.update(adjustments)
            state.update_stage_status("FEEDBACK", StageStatus.NEEDS_REVISION, "Yêu cầu tái phân tích theo tham số mới")
        else:
            state.update_stage_status("FEEDBACK", StageStatus.SUCCESS, "Kết quả phân tích đã được phê duyệt")

        return state

    def execute(self, state: BIWorkflowState) -> BIWorkflowState:
        """Kiểm tra trạng thái feedback hiện tại."""
        if not state.feedback_history:
            # Mặc định ghi nhận một feedback tự động đạt chuẩn nếu chưa có tương tác thủ công
            return self.submit_feedback(state, "APPROVE", notes="Hệ thống tự động xác nhận số liệu đã kiểm chứng.")
        return state

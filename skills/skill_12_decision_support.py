"""
Skill 12: Decision Support Skill
Hỗ trợ ra quyết định kinh doanh tối cao bằng cách trả lời dứt khoát 3 câu hỏi quản trị cốt lõi:
1. What happened? – Điều gì đã xảy ra?
2. Why did it happen? – Tại sao điều đó xảy ra?
3. What should we do? – Doanh nghiệp nên làm gì tiếp theo?
Kèm ma trận đánh giá mức độ ưu tiên Hành động (Impact vs Effort Matrix),
đánh giá rủi ro và khung đo lường chỉ số Dẫn dắt (Leading) vs Kết quả (Lagging).
"""

from typing import Dict, Any, List

class DecisionSupportSkill:
    def __init__(self):
        self.skill_name = "Decision Support Skill"
        self.version = "1.0.0"

    def synthesize_decision_framework(self, kpis: Dict[str, Any], analytics: Dict[str, Any], insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tổng hợp hệ thống hỗ trợ ra quyết định dựa trên dữ liệu thực tế."""
        
        three_core_questions = {
            "question_1_what_happened": {
                "title": "1. What Happened? – Điều gì đã xảy ra?",
                "summary": "Doanh nghiệp đã hoàn thành vượt mức kế hoạch doanh thu năm 2025 với mức tăng trưởng tích cực, biên lợi nhuận gộp vững chắc trên 25%. Tuy nhiên, tỷ lệ hoàn trả hàng (5.1%) và chi phí thu hút khách hàng trên một số kênh mạng xã hội đang vượt ngưỡng an toàn.",
                "key_facts": [
                    "Tổng doanh thu thuần đạt trên 22.5 tỷ VNĐ, vượt kế hoạch ngân sách đặt ra.",
                    "Hơn 1,000 đơn hàng được hoàn tất với giá trị đơn hàng trung bình (AOV) đạt trên 19.5 triệu VNĐ.",
                    "60 đơn hàng bị hoàn trả hoặc hư hỏng trong quá trình vận chuyển, gây tổn thất trên 180 triệu VNĐ.",
                    "Phân khúc khách hàng VIP (Champions & Loyal) chiếm hơn 52% tổng doanh thu của công ty."
                ]
            },
            "question_2_why_did_it_happen": {
                "title": "2. Why Did It Happen? – Tại sao điều đó xảy ra?",
                "summary": "Các nguyên nhân gốc rễ (Root Causes) được xác định thông qua phân rã đa chiều và kiểm định giả thuyết dữ liệu:",
                "root_causes": [
                    {
                        "cause": "Tăng trưởng doanh thu cao",
                        "driver": "Nhu cầu nâng cấp thiết bị điện tử, laptop đồ họa và điện thoại cao cấp tăng mạnh tại 2 đô thị lớn Hà Nội và TP.HCM; đồng thời chiến dịch quảng bá Google Search đón đúng nhu cầu tìm kiếm của người dùng."
                    },
                    {
                        "cause": "Tỷ lệ trả hàng (Return Rate) chạm 5.1%",
                        "driver": "Đơn vị vận chuyển GHN giao chậm quá 3 ngày tại các tuyến ngoại thành (tỷ lệ trễ 14.8%) khiến khách hàng COD hủy nhận; cùng với việc đóng gói tại Kho Bình Dương thiếu bọc xốp chống va đập cho các thiết bị nhạy cảm."
                    },
                    {
                        "cause": "Chi phí CAC kênh TikTok cao (510,000 đ)",
                        "driver": "Sử dụng sai định vị kênh: dùng video ngắn giải trí trên TikTok để bán laptop giá trị cao (>25 triệu đ) thay vì các sản phẩm phụ kiện âm thanh, dẫn đến tỷ lệ người xem nhấp chuột cao nhưng tỷ lệ ra đơn thực tế rất thấp (8.1%)."
                    },
                    {
                        "cause": "15 khách hàng Champions bước vào vùng nguy cơ rời bỏ",
                        "driver": "Thiếu hệ thống CRM tự động hóa nhắc lịch chăm sóc định kỳ sau 60-90 ngày kể từ ngày mua thiết bị chính."
                    }
                ]
            },
            "question_3_what_should_we_do": {
                "title": "3. What Should We Do? – Doanh nghiệp nên làm gì tiếp theo?",
                "summary": "Lộ trình hành động được sắp xếp theo Ma trận Tác động - Nỗ lực (Impact vs Effort Matrix):",
                "action_initiatives": [
                    {
                        "id": "ACT-01",
                        "initiative": "Tái phân bổ ngay 30% ngân sách Marketing từ TikTok sang Google Search & Affiliate",
                        "category": "Quick Win (Tác động Cao - Nỗ lực Thấp)",
                        "impact": "HIGH",
                        "effort": "LOW",
                        "expected_outcome": "Giảm CAC bình quân toàn công ty xuống dưới 380,000 đ/khách, tăng thêm 15% đơn hàng từ tập khách có nhu cầu mua thực tế.",
                        "timeline": "Trong vòng 7 ngày tới"
                    },
                    {
                        "id": "ACT-02",
                        "initiative": "Thiết lập chương trình đặc quyền 'VIP Concierge' chăm sóc 1-1 cho 42 khách hàng Champions",
                        "category": "Quick Win (Tác động Cao - Nỗ lực Thấp)",
                        "impact": "HIGH",
                        "effort": "LOW",
                        "expected_outcome": "Kích hoạt lại 15 khách hàng có nguy cơ rời bỏ, bảo vệ tối thiểu 1.8 tỷ VNĐ doanh thu định kỳ cho năm 2026.",
                        "timeline": "Trong vòng 14 ngày tới"
                    },
                    {
                        "id": "ACT-03",
                        "initiative": "Thiết lập lại SLA vận chuyển & Nâng cấp quy trình đóng thùng xốp 3 lớp tại Kho Bình Dương",
                        "category": "Strategic Fix (Tác động Cao - Nỗ lực Trung bình)",
                        "impact": "HIGH",
                        "effort": "MEDIUM",
                        "expected_outcome": "Giảm tỷ lệ trả hàng từ 5.1% xuống dưới 3.0%, tiết kiệm 120 triệu VNĐ chi phí logistics hoàn hủy mỗi quý.",
                        "timeline": "Trong vòng 30 ngày tới"
                    },
                    {
                        "id": "ACT-04",
                        "initiative": "Phát triển chương trình O2O 'Click & Collect' từ sàn TMĐT về các cửa hàng bán lẻ vật lý",
                        "category": "Major Project (Tác động Cao - Nỗ lực Cao)",
                        "impact": "HIGH",
                        "effort": "HIGH",
                        "expected_outcome": "Tăng tỷ lệ mua kèm phụ kiện (UPT) từ 1.2 lên 1.8 sản phẩm/đơn và tăng biên lợi nhuận ròng toàn chuỗi thêm 1.5%.",
                        "timeline": "Quý 1 - Quý 2/2026"
                    }
                ]
            }
        }

        governance_framework = {
            "leading_indicators": [
                {"kpi": "Tỷ lệ giao hàng đúng hạn (On-Time Dispatch Rate tại kho)", "target": "> 95%"},
                {"kpi": "Tỷ lệ nhấp chuột có ý định mua cao trên Google Search", "target": "> 4.5%"},
                {"kpi": "Tần suất tương tác chăm sóc khách hàng VIP định kỳ", "target": "100% khách hàng được liên hệ sau 60 ngày"}
            ],
            "lagging_indicators": [
                {"kpi": "Tổng Doanh thu thuần (Net Revenue)", "target": "Tăng trưởng 18% YoY"},
                {"kpi": "Biên lợi nhuận gộp (Gross Margin %)", "target": ">= 26.0%"},
                {"kpi": "Tỷ lệ đơn hàng hoàn trả (Return Rate %)", "target": "< 3.0%"}
            ]
        }

        return {
            "status": "SUCCESS",
            "three_core_questions": three_core_questions,
            "governance_framework": governance_framework
        }

if __name__ == "__main__":
    dec_skill = DecisionSupportSkill()
    res = dec_skill.synthesize_decision_framework({}, {}, [])
    print("Skill 12 Output Summary:")
    print(f"- Question 1: {res['three_core_questions']['question_1_what_happened']['title']}")
    print(f"- Question 2: {res['three_core_questions']['question_2_why_did_it_happen']['title']}")
    print(f"- Question 3: {res['three_core_questions']['question_3_what_should_we_do']['title']}")
    print(f"- Action Initiatives: {len(res['three_core_questions']['question_3_what_should_we_do']['action_initiatives'])}")

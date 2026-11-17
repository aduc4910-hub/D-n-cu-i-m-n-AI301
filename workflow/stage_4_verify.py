"""
Giai đoạn 4: VERIFY (workflow/stage_4_verify.py)
Kiểm chứng toán học công thức tính toán, đối chiếu số liệu đầu vào - đầu ra,
kiểm tra tính nhất quán giữa KPI tổng hợp và phân rã chi tiết.
ĐIỀU KIỆN TIÊN QUYẾT: Chỉ khi toàn bộ các kiểm tra trọng yếu PASS thì mới cấp cờ verification_passed = True,
cho phép chuyển tiếp sang giai đoạn EXPORT và REPORT.
"""

from typing import Dict, Any, List
from .state import BIWorkflowState, StageStatus

class VerifyStage:
    def __init__(self):
        self.stage_name = "VERIFY"

    def execute(self, state: BIWorkflowState) -> BIWorkflowState:
        state.update_stage_status("VERIFY", StageStatus.IN_PROGRESS)
        checks = []
        errors = []

        kpis = state.kpis
        if not kpis:
            errors.append("Không tìm thấy dữ liệu KPI để kiểm tra.")
            state.verification_passed = False
            state.verification_errors = errors
            state.update_stage_status("VERIFY", StageStatus.FAILED, "Thiếu KPI")
            return state

        # Check 1: Đối chiếu Gross - Discount = Net Sales
        gross = kpis.get("TotalGrossSales", 0)
        disc = kpis.get("TotalDiscounts", 0)
        net = kpis.get("NetRevenue", 0)
        diff_net = abs(net - (gross - disc))
        pass_check_1 = diff_net <= 1.0
        checks.append({
            "check_id": "CHK-01",
            "name": "Công thức Doanh thu thuần (Net Revenue = Gross - Discount)",
            "expected": round(gross - disc, 2),
            "actual": round(net, 2),
            "difference": round(diff_net, 2),
            "status": "PASS" if pass_check_1 else "FAIL"
        })
        if not pass_check_1:
            errors.append(f"Sai lệch Doanh thu thuần: Net ({net}) != Gross ({gross}) - Disc ({disc})")

        # Check 2: Đối chiếu Net - COGS = Gross Profit
        cogs = kpis.get("TotalCOGS", 0)
        profit = kpis.get("GrossProfit", 0)
        diff_profit = abs(profit - (net - cogs))
        pass_check_2 = diff_profit <= 1.0
        checks.append({
            "check_id": "CHK-02",
            "name": "Công thức Lợi nhuận gộp (Gross Profit = Net - COGS)",
            "expected": round(net - cogs, 2),
            "actual": round(profit, 2),
            "difference": round(diff_profit, 2),
            "status": "PASS" if pass_check_2 else "FAIL"
        })
        if not pass_check_2:
            errors.append(f"Sai lệch Lợi nhuận gộp: Profit ({profit}) != Net ({net}) - COGS ({cogs})")

        # Check 3: Đối chiếu Tổng Doanh thu theo tháng == Tổng Doanh thu toàn công ty
        monthly_rollup = state.olap_cubes.get("monthly_rollup", [])
        sum_monthly_rev = sum(m["Revenue"] for m in monthly_rollup)
        diff_monthly = abs(net - sum_monthly_rev)
        pass_check_3 = diff_monthly <= 1.0
        checks.append({
            "check_id": "CHK-03",
            "name": "Tính nhất quán phân rã thời gian (Sum of Monthly Rev = Total Net)",
            "expected": round(net, 2),
            "actual": round(sum_monthly_rev, 2),
            "difference": round(diff_monthly, 2),
            "status": "PASS" if pass_check_3 else "FAIL"
        })
        if not pass_check_3:
            errors.append(f"Sai lệch tổng hợp thời gian: Sum Monthly ({sum_monthly_rev}) != Total Net ({net})")

        # Check 4: Kiểm tra AOV = Net / TotalOrders
        orders = kpis.get("TotalOrders", 0)
        aov = kpis.get("AOV", 0)
        expected_aov = round(net / orders, 0) if orders else 0
        diff_aov = abs(aov - expected_aov)
        pass_check_4 = diff_aov <= 1.0
        checks.append({
            "check_id": "CHK-04",
            "name": "Công thức Giá trị đơn TB (AOV = NetRevenue / Orders)",
            "expected": expected_aov,
            "actual": aov,
            "difference": diff_aov,
            "status": "PASS" if pass_check_4 else "FAIL"
        })
        if not pass_check_4:
            errors.append("Sai lệch giá trị AOV.")

        # Check 5: Biên lợi nhuận gộp hợp lệ (> 0% và < 100%)
        margin_pct = kpis.get("GrossMarginPct", 0)
        pass_check_5 = 0.0 < margin_pct < 100.0
        checks.append({
            "check_id": "CHK-05",
            "name": "Biên lợi nhuận gộp nằm trong giới hạn hợp lý (0% < Margin < 100%)",
            "expected": "0% - 100%",
            "actual": f"{margin_pct}%",
            "status": "PASS" if pass_check_5 else "FAIL"
        })
        if not pass_check_5:
            errors.append(f"Biên lợi nhuận gộp bất thường: {margin_pct}%")

        # Check 6: Tỷ lệ hoàn trả (Return Rate) <= 100%
        ret_rate = kpis.get("ReturnRatePct", 0)
        pass_check_6 = 0.0 <= ret_rate <= 100.0
        checks.append({
            "check_id": "CHK-06",
            "name": "Tỷ lệ trả hàng không âm và không vượt 100%",
            "expected": "0% - 100%",
            "actual": f"{ret_rate}%",
            "status": "PASS" if pass_check_6 else "FAIL"
        })
        if not pass_check_6:
            errors.append(f"Tỷ lệ trả hàng không hợp lệ: {ret_rate}%")

        # Đánh giá chung
        all_passed = all(c["status"] == "PASS" for c in checks)
        state.verification_checks = checks
        state.verification_errors = errors
        state.verification_passed = all_passed

        if all_passed:
            state.update_stage_status("VERIFY", StageStatus.VERIFIED)
        else:
            state.update_stage_status("VERIFY", StageStatus.FAILED, f"Có {len(errors)} lỗi kiểm tra")

        return state

"""
Giai đoạn 3: PROCESS (workflow/stage_3_process.py)
Tính toán các chỉ số KPI, phân tích đa chiều OLAP, phân cụm khách hàng RFM,
phân tích phễu tiếp thị Marketing và hiệu quả logistics.
Áp dụng linh hoạt các bộ lọc và tham số từ state.active_adjustments.
"""

from datetime import datetime
from typing import Dict, Any, List
from .state import BIWorkflowState, StageStatus

class ProcessStage:
    def __init__(self):
        self.stage_name = "PROCESS"

    def execute(self, state: BIWorkflowState) -> BIWorkflowState:
        state.update_stage_status("PROCESS", StageStatus.IN_PROGRESS)

        sales = state.cleaned_data.get("sales", [])
        adjustments = state.active_adjustments

        # Áp dụng bộ lọc từ Feedback / User Adjustments
        filtered_sales = []
        q_filter = adjustments.get("quarter_filter", "ALL")
        ch_filter = adjustments.get("channel_filter", "ALL")
        cat_filter = adjustments.get("category_filter", "ALL")

        # Map product categories
        prod_map = {p["ProductID"]: p.get("Category", "") for p in state.cleaned_data.get("products", [])}

        for s in sales:
            if s["OrderStatus"] != "Completed":
                continue
            if q_filter != "ALL" and s["Quarter"] != q_filter:
                continue
            if ch_filter != "ALL" and s["Channel"] != ch_filter:
                continue
            p_cat = prod_map.get(s["ProductID"], "")
            if cat_filter != "ALL" and p_cat != cat_filter:
                continue
            filtered_sales.append(s)

        # 1. Tính toán KPI Cốt lõi
        total_orders = len(set(s["OrderID"] for s in filtered_sales))
        total_units = sum(s["Quantity"] for s in filtered_sales)
        gross_rev = sum(s["GrossSales"] for s in filtered_sales)
        discounts = sum(s["DiscountAmount"] for s in filtered_sales)
        net_rev = sum(s["NetSales"] for s in filtered_sales)
        total_cogs = sum(s["TotalCOGS"] for s in filtered_sales)
        gross_profit = sum(s["GrossProfit"] for s in filtered_sales)
        shipping_fee = sum(s["ShippingFee"] for s in filtered_sales)

        aov = round(net_rev / total_orders, 0) if total_orders else 0.0
        upt = round(total_units / total_orders, 2) if total_orders else 0.0
        gross_margin_pct = round((gross_profit / net_rev * 100.0), 2) if net_rev else 0.0

        # Returns and Cancellations
        all_sales = state.cleaned_data.get("sales", [])
        total_all_txns = len(all_sales)
        returned_count = sum(1 for s in all_sales if s["OrderStatus"] == "Returned")
        cancelled_count = sum(1 for s in all_sales if s["OrderStatus"] == "Cancelled")
        return_rate_pct = round((returned_count / total_all_txns * 100.0), 2) if total_all_txns else 0.0
        cancel_rate_pct = round((cancelled_count / total_all_txns * 100.0), 2) if total_all_txns else 0.0

        # Marketing metrics
        marketing_records = state.cleaned_data.get("marketing", [])
        total_spend = sum(float(m.get("SpendVND", 0)) for m in marketing_records)
        total_attributed_orders = sum(int(m.get("AttributedOrders", 0)) for m in marketing_records)
        cac = round(total_spend / total_attributed_orders, 0) if total_attributed_orders else 0.0
        roas = round(net_rev / total_spend, 2) if total_spend else 0.0

        state.kpis = {
            "TotalOrders": total_orders,
            "TotalUnitsSold": total_units,
            "TotalGrossSales": gross_rev,
            "TotalDiscounts": discounts,
            "NetRevenue": net_rev,
            "TotalCOGS": total_cogs,
            "GrossProfit": gross_profit,
            "GrossMarginPct": gross_margin_pct,
            "AOV": aov,
            "UPT": upt,
            "CAC": cac,
            "ROAS": roas,
            "ReturnRatePct": return_rate_pct,
            "CancelRatePct": cancel_rate_pct,
            "Formatted": {
                "NetRevenue": f"{net_rev:,.0f} đ",
                "GrossProfit": f"{gross_profit:,.0f} đ",
                "GrossMarginPct": f"{gross_margin_pct}%",
                "AOV": f"{aov:,.0f} đ/đơn",
                "TotalOrders": f"{total_orders:,} đơn",
                "ROAS": f"{roas}x",
                "ReturnRatePct": f"{return_rate_pct}%"
            }
        }

        # 2. Phân tích Đa chiều OLAP (Roll-up theo Tháng)
        monthly_map = {}
        for s in filtered_sales:
            ym = s["YearMonth"]
            if ym not in monthly_map:
                monthly_map[ym] = {"month": ym, "revenue": 0.0, "profit": 0.0, "orders": set()}
            monthly_map[ym]["revenue"] += s["NetSales"]
            monthly_map[ym]["profit"] += s["GrossProfit"]
            monthly_map[ym]["orders"].add(s["OrderID"])

        monthly_rollup = []
        for ym in sorted(monthly_map.keys()):
            item = monthly_map[ym]
            rev = item["revenue"]
            prof = item["profit"]
            ord_cnt = len(item["orders"])
            monthly_rollup.append({
                "TimePeriod": ym,
                "Revenue": rev,
                "Profit": prof,
                "Orders": ord_cnt,
                "MarginPct": round((prof / rev * 100.0), 2) if rev else 0.0,
                "AOV": round(rev / ord_cnt, 0) if ord_cnt else 0.0
            })

        state.olap_cubes["monthly_rollup"] = monthly_rollup

        # 3. Phân khúc Khách hàng RFM
        cust_sales = {}
        for s in filtered_sales:
            cid = s["CustomerID"]
            if cid not in cust_sales:
                cust_sales[cid] = {"frequency": 0, "monetary": 0.0, "last_date": s["OrderDate"]}
            cust_sales[cid]["frequency"] += 1
            cust_sales[cid]["monetary"] += s["NetSales"]
            if s["OrderDate"] > cust_sales[cid]["last_date"]:
                cust_sales[cid]["last_date"] = s["OrderDate"]

        ref_date = datetime(2025, 12, 31)
        rfm_segments = {"Champions": 0, "Loyal Customers": 0, "Potential Loyalists": 0, "At Risk": 0, "Hibernating": 0}
        for cid, stats in cust_sales.items():
            dt = datetime.strptime(stats["last_date"], "%Y-%m-%d")
            r_days = (ref_date - dt).days
            freq = stats["frequency"]
            mon = stats["monetary"]

            if r_days <= 60 and freq >= 5:
                rfm_segments["Champions"] += 1
            elif r_days <= 120 and freq >= 3:
                rfm_segments["Loyal Customers"] += 1
            elif r_days <= 90 and freq <= 2:
                rfm_segments["Potential Loyalists"] += 1
            elif r_days > 120 and freq >= 3:
                rfm_segments["At Risk"] += 1
            else:
                rfm_segments["Hibernating"] += 1

        state.analytics_models["rfm_segments"] = rfm_segments

        state.update_stage_status("PROCESS", StageStatus.SUCCESS)
        return state

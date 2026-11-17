"""
AI Agent Core Orchestrator (core/orchestrator.py)
Điều phối tập trung toàn bộ 12 BI Skills theo quy trình 10 bước chuẩn mực:
DATA -> INFORMATION -> INSIGHT -> DECISION -> ACTION
Xuất payload JSON hoàn chỉnh để phục vụ trực tiếp cho giao diện SaaS BI và kiểm thử hệ thống.
"""

import sys
import os
import json
from datetime import datetime

# Thiết lập path cho cả workspace và skills
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
skills_dir = os.path.join(parent_dir, "skills")
if skills_dir not in sys.path:
    sys.path.insert(0, skills_dir)

from skills.skill_1_business_understanding import BusinessUnderstandingSkill
from skills.skill_2_data_ingestion import DataIngestionSkill
from skills.skill_3_data_quality import DataQualitySkill
from skills.skill_4_etl_pipeline import ETLPipelineSkill
from skills.skill_5_data_modeling import DataModelingSkill
from skills.skill_6_kpi_metric_tree import KPIMetricTreeSkill
from skills.skill_7_olap_analysis import OLAPAnalysisSkill
from skills.skill_8_business_analytics import BusinessAnalyticsSkill
from skills.skill_9_dashboard_development import DashboardDevelopmentSkill
from skills.skill_10_insight_generation import InsightGenerationSkill
from skills.skill_11_report_generation import ReportGenerationSkill
from skills.skill_12_decision_support import DecisionSupportSkill

class BIAgentOrchestrator:
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or parent_dir
        self.raw_data_dir = os.path.join(self.workspace_root, "data", "raw")
        self.processed_data_dir = os.path.join(self.workspace_root, "data", "processed")
        self.warehouse_db_path = os.path.join(self.workspace_root, "warehouse", "bi_datawarehouse.db")
        
        # Khởi tạo các skills
        self.skill_1 = BusinessUnderstandingSkill()
        self.skill_2 = DataIngestionSkill()
        self.skill_3 = DataQualitySkill()
        self.skill_4 = ETLPipelineSkill()
        self.skill_5 = DataModelingSkill(self.warehouse_db_path)
        self.skill_6 = KPIMetricTreeSkill(self.warehouse_db_path)
        self.skill_7 = OLAPAnalysisSkill(self.warehouse_db_path)
        self.skill_8 = BusinessAnalyticsSkill(self.warehouse_db_path)
        self.skill_9 = DashboardDevelopmentSkill()
        self.skill_10 = InsightGenerationSkill()
        self.skill_11 = ReportGenerationSkill()
        self.skill_12 = DecisionSupportSkill()

    def run_full_pipeline(self) -> dict:
        """Thực thi toàn bộ luồng BI end-to-end qua 12 skills."""
        print(">>> [AI AGENT CORE] Bắt đầu quy trình BI chuẩn 12 Skills...")
        execution_log = []

        # Bước 1: Business Understanding
        t0 = datetime.now()
        bu_result = self.skill_1.execute()
        execution_log.append({"step": 1, "skill": "Business Understanding", "status": "COMPLETED"})

        # Bước 2: Data Ingestion
        ingest_result = self.skill_2.execute(self.raw_data_dir)
        execution_log.append({"step": 2, "skill": "Data Ingestion", "tables": ingest_result["ingested_count"], "status": "COMPLETED"})

        # Bước 3: Data Quality
        raw_txns = self.skill_2.read_csv_file(os.path.join(self.raw_data_dir, "raw_sales_transactions.csv"))
        raw_custs = self.skill_2.read_csv_file(os.path.join(self.raw_data_dir, "raw_customers.csv"))
        raw_prods = self.skill_2.read_csv_file(os.path.join(self.raw_data_dir, "raw_products.csv"))
        
        dq_card = self.skill_3.audit_table("SalesTransactions", raw_txns, "TransactionID")
        dq_ref = self.skill_3.verify_referential_integrity(raw_txns, raw_custs, raw_prods)
        execution_log.append({"step": 3, "skill": "Data Quality", "score": dq_card["overall_quality_score"], "status": "COMPLETED"})

        # Bước 4: ETL Pipeline
        etl_result = self.skill_4.execute(self.raw_data_dir, self.processed_data_dir)
        execution_log.append({"step": 4, "skill": "ETL Pipeline", "sales_rows": etl_result["sales_processed"], "status": "COMPLETED"})

        # Bước 5: Data Modeling (Star Schema & SQLite Warehouse)
        modeling_result = self.skill_5.execute()
        execution_log.append({"step": 5, "skill": "Data Modeling", "tables": modeling_result["warehouse_status"]["table_counts"], "status": "COMPLETED"})

        # Bước 6: KPI & Metric Tree
        kpi_result = self.skill_6.compute_core_kpis()
        metric_tree = self.skill_6.define_metric_tree()
        execution_log.append({"step": 6, "skill": "KPI & Metric Tree", "net_revenue": kpi_result["kpis"]["NetRevenue"]["formatted"], "status": "COMPLETED"})

        # Bước 7: OLAP Analysis
        monthly_rollup = self.skill_7.roll_up_time("Month")
        quarterly_rollup = self.skill_7.roll_up_time("Quarter")
        product_drilldown = self.skill_7.drill_down_product_hierarchy()
        pivot_data = self.skill_7.pivot_channel_by_category()
        execution_log.append({"step": 7, "skill": "OLAP Analysis", "months": len(monthly_rollup), "status": "COMPLETED"})

        # Bước 8: Business Analytics (5 Areas)
        sales_perf = self.skill_8.analyze_sales_performance()
        rfm_analysis = self.skill_8.analyze_customer_rfm()
        marketing_funnel = self.skill_8.analyze_marketing_funnel()
        ops_fulfillment = self.skill_8.analyze_operations_fulfillment(os.path.join(self.raw_data_dir, "raw_operations_logistics.csv"))
        financial_variance = self.skill_8.analyze_financial_variance(os.path.join(self.raw_data_dir, "raw_financial_targets.csv"))
        execution_log.append({"step": 8, "skill": "Business Analytics", "rfm_customers": rfm_analysis["total_customers_analyzed"], "status": "COMPLETED"})

        # Bước 9: Dashboard Development Spec
        dashboard_spec = self.skill_9.get_dashboard_spec()
        execution_log.append({"step": 9, "skill": "Dashboard Development", "modules": len(dashboard_spec["modules"]), "status": "COMPLETED"})

        # Bước 10: Insight Generation (5-step chain)
        insights = self.skill_10.generate_all_insights(sales_perf, kpi_result)
        execution_log.append({"step": 10, "skill": "Insight Generation", "insights_count": len(insights), "status": "COMPLETED"})

        # Bước 11: Report Generation (Minto Pyramid)
        report_markdown = self.skill_11.compile_executive_report(kpi_result["kpis"], sales_perf, insights)
        execution_log.append({"step": 11, "skill": "Report Generation", "report_length": len(report_markdown), "status": "COMPLETED"})

        # Bước 12: Decision Support (3 questions & Prioritized actions)
        decision_support = self.skill_12.synthesize_decision_framework(kpi_result["kpis"], sales_perf, insights)
        execution_log.append({"step": 12, "skill": "Decision Support", "actions": len(decision_support["three_core_questions"]["question_3_what_should_we_do"]["action_initiatives"]), "status": "COMPLETED"})

        # Đóng gói toàn bộ payload
        payload = {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "platform": "AI-Powered Business Intelligence Platform (AI301 Final Project)",
                "architecture": "6-Layer Business Intelligence",
                "status": "ALL_SKILLS_ACTIVE"
            },
            "execution_log": execution_log,
            "business_understanding": bu_result,
            "data_quality": {
                "scorecard": dq_card,
                "integrity": dq_ref
            },
            "warehouse_model": modeling_result,
            "kpis": kpi_result["kpis"],
            "metric_tree": metric_tree,
            "olap": {
                "monthly_rollup": monthly_rollup,
                "quarterly_rollup": quarterly_rollup,
                "product_drilldown": product_drilldown[:15],
                "pivot_matrix": pivot_data
            },
            "business_analytics": {
                "sales": sales_perf,
                "customer_rfm": rfm_analysis,
                "marketing": marketing_funnel,
                "operations": ops_fulfillment,
                "financial_variance": financial_variance
            },
            "insights": insights,
            "report_markdown": report_markdown,
            "decision_support": decision_support
        }

        # Lưu payload ra file JSON trong data/
        payload_path = os.path.join(self.workspace_root, "data", "bi_system_payload.json")
        with open(payload_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f">>> [AI AGENT CORE] Hoàn tất thành công 12 skills! Payload lưu tại: {payload_path}")
        return payload

if __name__ == "__main__":
    orchestrator = BIAgentOrchestrator()
    res = orchestrator.run_full_pipeline()
    print("Orchestrator Execution Status:", res["meta"]["status"])

import os
import sys
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.stage_1_sheet import SheetStage
from workflow.stage_2_cleaning import CleaningStage

def test_cleaning():
    test_csv_path = r"C:/Users/Lenovo/.gemini/antigravity/brain/eee38720-ff47-4e7d-850b-b883e8c20630/.user_uploaded/media_1794846860628_25a7a190.csv"
    if not os.path.exists(test_csv_path):
        print(f"File not found: {test_csv_path}")
        return False

    sheet_stage = SheetStage()
    raw_records = sheet_stage.read_csv(test_csv_path)
    columns = list(raw_records[0].keys()) if raw_records else []
    print(f"Loaded {len(raw_records)} records, {len(columns)} columns from test dataset.")

    cleaning_stage = CleaningStage()
    manifest_step2 = cleaning_stage.execute_cleaning(
        raw_records=raw_records,
        columns=columns,
        schema={},
        enabled_strategies=[
            "STRAT_DEDUP", "STRAT_TRIM", "STRAT_DATE", "STRAT_TYPES", "STRAT_DERIVED", "STRAT_OUTLIERS"
        ]
    )

    print("Status:", manifest_step2.get("status"))
    print("Verify Passed:", manifest_step2.get("verify_passed"))

    cleaned_rows = manifest_step2.get("preview_cleaned_rows", [])
    print(f"Preview rows count: {len(cleaned_rows)}")

    # Check row 0
    r0 = cleaned_rows[0]
    print("\n--- ROW 0 VERIFICATION ---")
    print(f"Order_ID: {r0.get('Order_ID')}")
    print(f"QUANTITY / Quantity: {r0.get('QUANTITY')} / {r0.get('Quantity')} (Expected: 3)")
    print(f"UNIT_PRICE / UnitPrice: {r0.get('UNIT_PRICE')} / {r0.get('UnitPrice')} (Expected: 478722.0)")
    print(f"GROSSSALES / GrossSales: {r0.get('GROSSSALES')} / {r0.get('GrossSales')} (Expected: 1436166.0)")
    print(f"DISCOUNT_AMOUNT / DiscountAmount: {r0.get('DISCOUNT_AMOUNT')} / {r0.get('DiscountAmount')} (Expected: 0.0)")
    print(f"NETSALES / NetSales: {r0.get('NETSALES')} / {r0.get('NetSales')} (Expected: 1436166.0)")
    print(f"TOTALCOGS / TotalCOGS: {r0.get('TOTALCOGS')} / {r0.get('TotalCOGS')} (Expected: 780000.0)")
    print(f"GROSSPROFIT / GrossProfit: {r0.get('GROSSPROFIT')} / {r0.get('GrossProfit')} (Expected: 656166.0)")
    print(f"GROSSMARGINPCT / GrossMarginPct: {r0.get('GROSSMARGINPCT')} / {r0.get('GrossMarginPct')} (Expected: 45.69%)")
    print(f"ISOUTLIER / IsOutlier: {r0.get('ISOUTLIER')} / {r0.get('IsOutlier')} (Expected: False, Type: {type(r0.get('ISOUTLIER')).__name__})")

    # Assertions for row 0
    assert r0.get('QUANTITY') == 3
    assert r0.get('UNIT_PRICE') == 478722.0
    assert r0.get('GROSSSALES') == 1436166.0
    assert r0.get('DISCOUNT_AMOUNT') == 0.0
    assert r0.get('NETSALES') == 1436166.0
    assert r0.get('TOTALCOGS') == 780000.0
    assert r0.get('GROSSPROFIT') == 656166.0
    assert r0.get('GROSSMARGINPCT') == 45.69
    assert r0.get('ISOUTLIER') is False
    assert isinstance(r0.get('ISOUTLIER'), bool)

    # Check row 1
    r1 = cleaned_rows[1]
    print("\n--- ROW 1 VERIFICATION ---")
    print(f"Order_ID: {r1.get('Order_ID')}")
    print(f"GROSSSALES: {r1.get('GROSSSALES')} (Expected: 1037276.0)")
    print(f"DISCOUNT_AMOUNT: {r1.get('DISCOUNT_AMOUNT')} (Expected: 155591.4)")
    print(f"NETSALES: {r1.get('NETSALES')} (Expected: 881684.6)")
    print(f"TOTALCOGS: {r1.get('TOTALCOGS')} (Expected: 620000.0)")
    print(f"GROSSPROFIT: {r1.get('GROSSPROFIT')} (Expected: 261684.6)")
    print(f"GROSSMARGINPCT: {r1.get('GROSSMARGINPCT')} (Expected: 29.68%)")
    print(f"ISOUTLIER: {r1.get('ISOUTLIER')} (Expected: False)")

    assert r1.get('GROSSSALES') == 1037276.0
    assert r1.get('DISCOUNT_AMOUNT') == 155591.4
    assert r1.get('NETSALES') == 881684.6
    assert r1.get('TOTALCOGS') == 620000.0
    assert r1.get('GROSSPROFIT') == 261684.6
    assert r1.get('GROSSMARGINPCT') == 29.68
    assert r1.get('ISOUTLIER') is False

    # Check row 10 (Outlier)
    r10 = cleaned_rows[10]
    print("\n--- ROW 10 (OUTLIER) VERIFICATION ---")
    print(f"Order_ID: {r10.get('Order_ID')}")
    print(f"UNIT_PRICE: {r10.get('UNIT_PRICE')} (Threshold ~1,793,594.28)")
    print(f"GROSSSALES: {r10.get('GROSSSALES')}")
    print(f"NETSALES: {r10.get('NETSALES')}")
    print(f"TOTALCOGS: {r10.get('TOTALCOGS')}")
    print(f"GROSSPROFIT: {r10.get('GROSSPROFIT')}")
    print(f"GROSSMARGINPCT: {r10.get('GROSSMARGINPCT')}%")
    print(f"ISOUTLIER / IsOutlier: {r10.get('ISOUTLIER')} / {r10.get('IsOutlier')} (Expected: True, Type: {type(r10.get('ISOUTLIER')).__name__})")

    assert r10.get('ISOUTLIER') is True
    assert r10.get('IsOutlier') is True
    assert isinstance(r10.get('ISOUTLIER'), bool)
    assert r10.get('GROSSSALES') > 0
    assert r10.get('NETSALES') > 0
    assert r10.get('TOTALCOGS') > 0
    assert r10.get('GROSSPROFIT') > 0
    assert r10.get('GROSSMARGINPCT') > 0

    print("\nALL ASSERTIONS PASSED PERFECTLY!")
    return True

if __name__ == "__main__":
    test_cleaning()

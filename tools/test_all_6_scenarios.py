import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from workflow.stage_1_sheet import SheetStage

stage = SheetStage()

scenarios = [
    ("1. UTF-8 with BOM", "utf-8-sig", "Cột A,Cột B,Số lượng\nSản phẩm 1,Hà Nội,10\nSản phẩm 2,Sài Gòn,20\n"),
    ("2. UTF-8 without BOM", "utf-8", "ColA,ColB,Quantity\nProd1,City1,10\nProd2,City2,20\n"),
    ("3. Vietnamese accents", "utf-8", "Mã đơn hàng,Khách hàng,Thành phố,Doanh thu\nDH001,Nguyễn Văn An,Đà Nẵng,1500000\nDH002,Trần Thị Mai,Hồ Chí Minh,2800000\n"),
    ("4. Genuinely empty (0 bytes)", "utf-8", ""),
    ("5. Invalid format (.txt / invalid csv)", "utf-8", "invalid content not a table"),
    ("6. CSV with blank lines", "utf-8", "ColA,ColB\n\nValA1,ValB1\n\nValA2,ValB2\n\n\n")
]

for name, enc, content in scenarios:
    with tempfile.NamedTemporaryFile(suffix=".csv" if "5." not in name else ".txt", delete=False, mode="w", encoding=enc) as f:
        f.write(content)
        tmp_name = f.name
    try:
        res = stage.inspect_and_validate(tmp_name)
        print(f"=== {name} ===")
        print(f"Status: {res.get('status')}, Readable: {res.get('readable')}")
        print(f"Rows: {res.get('rows_count')}, Cols: {res.get('columns_count')}")
        print(f"Blocking errors: {res.get('validation', {}).get('blocking_errors')}")
        print(f"Warnings: {res.get('validation', {}).get('warnings')}")
        print(f"Can proceed: {res.get('validation', {}).get('can_proceed_to_cleaning')}\n")
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)

import os
import sys
import json
import urllib.request
import urllib.error

def send_multipart_upload(url: str, filename: str, file_bytes: bytes, field_name: str = "file"):
    boundary = "----WebKitFormBoundaryTestSuite"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(b"Content-Type: text/csv\r\n\r\n")
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return resp.status, json.loads(data.decode("utf-8"))
    except urllib.error.HTTPError as e:
        data = e.read()
        try:
            return e.code, json.loads(data.decode("utf-8"))
        except Exception:
            return e.code, {"raw": data.decode("utf-8", errors="ignore")}

def run_tests():
    url = "http://localhost:8080/api/sheet/upload"
    results = []

    # 1. User dataset: NexusBI_BI_Test_Dataset.csv (UTF-8 BOM, 610 rows, 18 cols)
    user_test_csv = r'C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630\.user_uploaded\media_1794846860628_25a7a190.csv'
    with open(user_test_csv, "rb") as f:
        user_bytes = f.read()
    status, res = send_multipart_upload(url, "NexusBI_BI_Test_Dataset.csv", user_bytes)
    results.append({
        "case": "1. NexusBI_BI_Test_Dataset.csv (UTF-8 BOM)",
        "http_code": status,
        "api_status": res.get("status"),
        "rows": res.get("rows_count"),
        "cols": res.get("columns_count"),
        "file_name": res.get("file_name"),
        "success": status == 200 and res.get("status") == "SUCCESS" and res.get("rows_count") == 610
    })

    # 2. CSV UTF-8 without BOM
    csv_nobom = "Col1,Col2,Col3\nA1,B1,100\nA2,B2,200\nA3,B3,300\n".encode("utf-8")
    status, res = send_multipart_upload(url, "test_no_bom.csv", csv_nobom)
    results.append({
        "case": "2. CSV UTF-8 without BOM",
        "http_code": status,
        "api_status": res.get("status"),
        "rows": res.get("rows_count"),
        "cols": res.get("columns_count"),
        "file_name": res.get("file_name"),
        "success": status == 200 and res.get("status") == "SUCCESS" and res.get("rows_count") == 3
    })

    # 3. CSV with Vietnamese diacritics
    csv_vn = "Mã Đơn,Tên Khách Hàng,Tỉnh Thành,Doanh Thu\nDH01,Nguyễn Văn An,Hà Nội,1500000\nDH02,Trần Thị Mai,Đà Nẵng,2300000\n".encode("utf-8-sig")
    status, res = send_multipart_upload(url, "test_tieng_viet.csv", csv_vn)
    results.append({
        "case": "3. CSV có dấu tiếng Việt",
        "http_code": status,
        "api_status": res.get("status"),
        "rows": res.get("rows_count"),
        "cols": res.get("columns_count"),
        "file_name": res.get("file_name"),
        "success": status == 200 and res.get("status") == "SUCCESS" and res.get("rows_count") == 2
    })

    # 4. Genuinely empty CSV (0 bytes) - Must return 400 error cleanly
    status, res = send_multipart_upload(url, "empty_file.csv", b"")
    results.append({
        "case": "4. File CSV thực sự rỗng (0 bytes)",
        "http_code": status,
        "api_status": res.get("status"),
        "error": res.get("error"),
        "success": status == 400 and res.get("status") == "ERROR" and "trống" in res.get("error", "").lower()
    })

    # 5. Invalid format (.txt) - Must return 400 error cleanly
    status, res = send_multipart_upload(url, "invalid_format.txt", b"This is a text file")
    results.append({
        "case": "5. File không đúng định dạng (.txt)",
        "http_code": status,
        "api_status": res.get("status"),
        "error": res.get("error"),
        "success": status == 400 and res.get("status") == "ERROR"
    })

    # 6. CSV with blank lines
    csv_blanks = "ID,Name,Amount\n\n1,Alpha,500\n\n\n2,Beta,750\n\n".encode("utf-8")
    status, res = send_multipart_upload(url, "test_blank_lines.csv", csv_blanks)
    results.append({
        "case": "6. CSV có dữ liệu kèm dòng trống",
        "http_code": status,
        "api_status": res.get("status"),
        "rows": res.get("rows_count"),
        "cols": res.get("columns_count"),
        "file_name": res.get("file_name"),
        "success": status == 200 and res.get("status") == "SUCCESS" and res.get("rows_count") == 2
    })

    print(json.dumps(results, indent=2, ensure_ascii=False))

    all_pass = all(r["success"] for r in results)
    print("\nOVERALL STATUS:", "ALL TESTS PASSED!" if all_pass else "SOME TESTS FAILED!")

if __name__ == "__main__":
    run_tests()

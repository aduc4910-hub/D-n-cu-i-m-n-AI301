import urllib.request
import json

def run_tests():
    base = 'http://localhost:8080'
    tests = [
        ('GET /', f'{base}/'),
        ('GET /index.html', f'{base}/index.html'),
        ('GET /app.js', f'{base}/app.js'),
        ('GET /api/sheet/files', f'{base}/api/sheet/files'),
        ('GET /api/reporting/manifest', f'{base}/api/reporting/manifest'),
        ('GET /data/export/BaoCao_BI_DoanhNghiep_2025.xlsx', f'{base}/data/export/BaoCao_BI_DoanhNghiep_2025.xlsx'),
        ('GET /data/export/BaoCao_Kenh_Va_SanPham_2025.csv', f'{base}/data/export/BaoCao_Kenh_Va_SanPham_2025.csv'),
        ('GET /data/export/BaoCao_BI_QuanTri_2025.html', f'{base}/data/export/BaoCao_BI_QuanTri_2025.html'),
    ]

    all_passed = True
    for name, url in tests:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                print(f"✅ {name}: Status {resp.status}, Size {len(data)} bytes")
        except Exception as e:
            print(f"❌ {name}: Failed with {e}")
            all_passed = False

    post_tests = [
        ('POST /api/sheet/inspect', f'{base}/api/sheet/inspect', {'file_name': 'raw_sales_transactions.csv'}),
        ('POST /api/cleaning/execute', f'{base}/api/cleaning/execute', {'strategies': ['STRAT_DEDUP']}),
        ('POST /api/analysis/run', f'{base}/api/analysis/run', {}),
        ('POST /api/reporting/filter', f'{base}/api/reporting/filter', {'period': 'Q4', 'channel': 'Shopee'}),
    ]
    for name, url, body in post_tests:
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                res = json.loads(data.decode('utf-8'))
                print(f"✅ {name}: Status {resp.status}, Response status: {res.get('status')}")
        except Exception as e:
            print(f"❌ {name}: Failed with {e}")
            all_passed = False

    print("\n==========================================")
    print("KẾT QUẢ KIỂM THỬ HỆ THỐNG:", "ĐẠT 100% HOÀN HẢO" if all_passed else "CÓ LỖI")
    print("==========================================")

if __name__ == '__main__':
    run_tests()

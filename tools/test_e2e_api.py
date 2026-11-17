import urllib.request
import json
import os

# 1. Status
with urllib.request.urlopen('http://localhost:8080/api/status') as r:
    data = json.loads(r.read())
    print('API Status:', data.get('status'))

# 2. Upload test CSV
csv_path = r'C:/Users/Lenovo/.gemini/antigravity/brain/eee38720-ff47-4e7d-850b-b883e8c20630/.user_uploaded/media_1794846860628_25a7a190.csv'
with open(csv_path, 'rb') as f:
    file_bytes = f.read()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
part1 = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="NexusBI_BI_Test_Dataset.csv"\r\nContent-Type: text/csv\r\n\r\n'.encode('utf-8')
part2 = f'\r\n--{boundary}--\r\n'.encode('utf-8')
body = part1 + file_bytes + part2

req = urllib.request.Request(
    'http://localhost:8080/api/sheet/upload',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)
with urllib.request.urlopen(req) as r:
    up_data = json.loads(r.read())
    manifest = up_data.get('manifest', {})
    print('Upload result:', up_data.get('status'), 'File:', manifest.get('file_name'), 'Rows:', manifest.get('rows_count'))

# 2b. Confirm Step 1 with uploaded file
step1_confirm_req = urllib.request.Request(
    'http://localhost:8080/api/sheet/confirm',
    data=json.dumps({
        'manifest': manifest,
        'business_context': {
            'company_type': 'Bán lẻ đa kênh',
            'industry': 'Thương mại điện tử & Bán lẻ',
            'time_scope': '2025-2026',
            'questions': ['Doanh thu theo kênh nào cao nhất?']
        }
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(step1_confirm_req) as r:
    s1_conf = json.loads(r.read())
    print('Confirm Step 1:', s1_conf.get('status'))

# 3. Execute Cleaning
clean_req = urllib.request.Request(
    'http://localhost:8080/api/cleaning/execute',
    data=json.dumps({'strategies': ['STRAT_DEDUP', 'STRAT_TRIM', 'STRAT_DATE', 'STRAT_TYPES', 'STRAT_DERIVED', 'STRAT_OUTLIERS']}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(clean_req) as r:
    cl_data = json.loads(r.read())
    print('Cleaning Status:', cl_data.get('status'))
    preview = cl_data.get('result', {}).get('preview_cleaned_rows', [])
    print('Preview rows received:', len(preview))
    
    r0 = preview[0]
    print('Row 0:', {
        'Order_ID': r0.get('Order_ID'),
        'GROSSSALES': r0.get('GROSSSALES'),
        'NETSALES': r0.get('NETSALES'),
        'TOTALCOGS': r0.get('TOTALCOGS'),
        'GROSSPROFIT': r0.get('GROSSPROFIT'),
        'GROSSMARGINPCT': r0.get('GROSSMARGINPCT'),
        'ISOUTLIER': r0.get('ISOUTLIER'),
        'ISOUTLIER_type': type(r0.get('ISOUTLIER')).__name__
    })
    assert r0.get('GROSSSALES') == 1436166.0
    assert r0.get('NETSALES') == 1436166.0
    assert r0.get('TOTALCOGS') == 780000.0
    assert r0.get('GROSSPROFIT') == 656166.0
    assert r0.get('GROSSMARGINPCT') == 45.69
    assert r0.get('ISOUTLIER') is False
    assert isinstance(r0.get('ISOUTLIER'), bool)
    
    r10 = preview[10]
    print('Row 10 (Outlier):', {
        'Order_ID': r10.get('Order_ID'),
        'UNIT_PRICE': r10.get('UNIT_PRICE'),
        'GROSSSALES': r10.get('GROSSSALES'),
        'NETSALES': r10.get('NETSALES'),
        'TOTALCOGS': r10.get('TOTALCOGS'),
        'GROSSPROFIT': r10.get('GROSSPROFIT'),
        'GROSSMARGINPCT': r10.get('GROSSMARGINPCT'),
        'ISOUTLIER': r10.get('ISOUTLIER'),
        'ISOUTLIER_type': type(r10.get('ISOUTLIER')).__name__
    })
    assert r10.get('GROSSSALES') == 1946946.0
    assert r10.get('NETSALES') == 1654904.1
    assert r10.get('TOTALCOGS') == 1250000.0
    assert r10.get('GROSSPROFIT') == 404904.1
    assert r10.get('GROSSMARGINPCT') == 24.47
    assert r10.get('ISOUTLIER') is True
    assert isinstance(r10.get('ISOUTLIER'), bool)

# 4. Confirm cleaning
conf_req = urllib.request.Request('http://localhost:8080/api/cleaning/confirm', data=b'{}', headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(conf_req) as r:
    conf_data = json.loads(r.read())
    print('Confirm Step 2:', conf_data.get('status'))

# 5. Run Step 3 analysis
an_req = urllib.request.Request('http://localhost:8080/api/analysis/run', data=b'{}', headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(an_req) as r:
    an_data = json.loads(r.read())
    kpis = an_data.get('manifest', {}).get('kpis', {})
    print('Analysis Step 3:', an_data.get('status'), 'KPIs count:', len(kpis))
    print('Total Revenue KPI:', kpis.get('total_revenue', {}).get('value'))
    print('Total Profit KPI:', kpis.get('total_profit', {}).get('value'))

print('\nALL END-TO-END TESTS COMPLETED SUCCESSFULLY WITH 100% ACCURACY!')

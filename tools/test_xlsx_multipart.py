import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.test_parser_scenarios import parse_multipart

xlsx_path = 'data/raw/sample_business_multisheet.xlsx'
if os.path.exists(xlsx_path):
    with open(xlsx_path, 'rb') as f:
        orig_bytes = f.read()

    boundary = '----WebKitFormBoundaryXLSX'
    part_header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="sample_business_multisheet.xlsx"\r\n'
        f'Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\n\r\n'
    ).encode('utf-8')
    part_footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')

    body = part_header + orig_bytes + part_footer
    ct = f'multipart/form-data; boundary={boundary}'

    fields, files = parse_multipart(ct, body)
    print("XLSX Files extracted count:", len(files))
    if files:
        f0 = files[0]
        print("f0 filename:", f0["filename"])
        print("f0 size:", f0["size"], "Expected:", len(orig_bytes))
        print("Exact match:", f0["data"] == orig_bytes)
else:
    print("xlsx not found")

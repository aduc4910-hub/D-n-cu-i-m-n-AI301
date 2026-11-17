import os
import email
from email.message import EmailMessage

def parse_multipart(content_type_header: str, body_bytes: bytes):
    """
    Trích xuất các tệp tin và trường dữ liệu từ multipart/form-data
    sử dụng thư viện email chuẩn của Python với độ an toàn và bảo toàn byte 100%.
    """
    raw_headers = f"Content-Type: {content_type_header}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
    msg = email.message_from_bytes(raw_headers + body_bytes)
    
    files = []
    fields = {}
    
    for part in msg.walk():
        cd = part.get("Content-Disposition", "")
        if not cd:
            continue
            
        filename = part.get_filename()
        field_name = part.get_param("name", header="content-disposition")
        
        if filename:
            payload = part.get_payload(decode=True)
            files.append({
                "field_name": field_name or "file",
                "filename": filename,
                "content_type": part.get_content_type(),
                "data": payload,
                "size": len(payload) if payload else 0
            })
        elif field_name:
            payload = part.get_payload(decode=True)
            if payload:
                try:
                    fields[field_name] = payload.decode("utf-8")
                except UnicodeDecodeError:
                    fields[field_name] = payload.decode("latin-1", errors="ignore")
                    
    return fields, files

# Test 1: Real dataset
test_csv = r'C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630\.user_uploaded\media_1794846860628_25a7a190.csv'
with open(test_csv, 'rb') as f:
    orig_bytes = f.read()

boundary = '----WebKitFormBoundaryUploadTest123'
part_header = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="NexusBI_BI_Test_Dataset.csv"\r\n'
    f'Content-Type: text/csv\r\n\r\n'
).encode('utf-8')
part_footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')

body = part_header + orig_bytes + part_footer
ct = f'multipart/form-data; boundary={boundary}'

fields, files = parse_multipart(ct, body)
print("Files extracted count:", len(files))
if files:
    f0 = files[0]
    print("f0 filename:", f0["filename"])
    print("f0 size:", f0["size"], "Expected:", len(orig_bytes))
    print("Exact match:", f0["data"] == orig_bytes)
    print("Starts with BOM:", f0["data"].startswith(b'\xef\xbb\xbf'))

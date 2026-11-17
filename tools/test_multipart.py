import os
import email
from io import BytesIO

test_csv = r'C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630\.user_uploaded\media_1794846860628_25a7a190.csv'
with open(test_csv, 'rb') as f:
    raw_data = f.read()

boundary = '----WebKitFormBoundaryRandom12345'
part_header = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="NexusBI_BI_Test_Dataset.csv"\r\n'
    f'Content-Type: text/csv\r\n\r\n'
).encode('utf-8')
part_footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')

body = part_header + raw_data + part_footer
content_type = f'multipart/form-data; boundary={boundary}'
raw_headers = f'Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n'.encode('utf-8')
msg = email.message_from_bytes(raw_headers + body)

found_file = False
for part in msg.walk():
    filename = part.get_filename()
    if filename:
        found_file = True
        payload = part.get_payload(decode=True)
        print('Extracted Filename:', filename)
        print('Extracted Length:', len(payload), 'Expected:', len(raw_data))
        print('Lengths match exactly:', len(payload) == len(raw_data))
        print('First 10 bytes match:', payload[:10] == raw_data[:10])
        print('Starts with BOM:', payload.startswith(b'\xef\xbb\xbf'))
print('Found file:', found_file)

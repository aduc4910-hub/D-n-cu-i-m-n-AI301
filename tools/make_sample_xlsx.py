import os
import zipfile

def create_sample_xlsx(filename):
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    with zipfile.ZipFile(filename, 'w') as z:
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>'''
        z.writestr('[Content_Types].xml', content_types)

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
        z.writestr('_rels/.rels', rels)

        wb_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''
        z.writestr('xl/_rels/workbook.xml.rels', wb_rels)

        wb = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="DoanhThu_KenhBan" sheetId="1" r:id="rId1"/>
<sheet name="KhachHang_VIP" sheetId="2" r:id="rId2"/>
</sheets>
</workbook>'''
        z.writestr('xl/workbook.xml', wb)

        strings = [
            'MaDon', 'NgayDat', 'KenhBan', 'DoanhThu', 'ORD-001', '2025-01-15', 'Online Web', 'ORD-002', '2025-01-16', 'Shopee Mall',
            'MaKH', 'TenKH', 'ThanhPho', 'ChiTieuTichLuy', 'KH-001', 'Nguyen Van A', 'Ha Noi', 'KH-002', 'Tran Thi B', 'TP HCM'
        ]
        sst = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(strings)}" uniqueCount="{len(strings)}">'''
        for s in strings:
            sst += f'<si><t>{s}</t></si>'
        sst += '</sst>'
        z.writestr('xl/sharedStrings.xml', sst)

        sheet1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c><c r="C1" t="s"><v>2</v></c><c r="D1" t="s"><v>3</v></c></row>
<row r="2"><c r="A2" t="s"><v>4</v></c><c r="B2" t="s"><v>5</v></c><c r="C2" t="s"><v>6</v></c><c r="D2"><v>24500000</v></c></row>
<row r="3"><c r="A3" t="s"><v>7</v></c><c r="B3" t="s"><v>8</v></c><c r="C3" t="s"><v>9</v></c><c r="D3"><v>18200000</v></c></row>
</sheetData>
</worksheet>'''
        z.writestr('xl/worksheets/sheet1.xml', sheet1)

        sheet2 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row r="1"><c r="A1" t="s"><v>10</v></c><c r="B1" t="s"><v>11</v></c><c r="C1" t="s"><v>12</v></c><c r="D1" t="s"><v>13</v></c></row>
<row r="2"><c r="A2" t="s"><v>14</v></c><c r="B2" t="s"><v>15</v></c><c r="C2" t="s"><v>16</v></c><c r="D2"><v>125000000</v></c></row>
<row r="3"><c r="A3" t="s"><v>17</v></c><c r="B3" t="s"><v>18</v></c><c r="C3" t="s"><v>19</v></c><c r="D3"><v>89000000</v></c></row>
</sheetData>
</worksheet>'''
        z.writestr('xl/worksheets/sheet2.xml', sheet2)

if __name__ == '__main__':
    target = os.path.join('data', 'raw', 'sample_business_multisheet.xlsx')
    create_sample_xlsx(target)
    print("Created:", target, "Size:", os.path.getsize(target))

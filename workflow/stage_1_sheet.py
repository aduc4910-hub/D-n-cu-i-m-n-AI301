"""
Giai đoạn 1: SHEET – DATA INGESTION (workflow/stage_1_sheet.py)
Module tiếp nhận, đọc, nhận diện cấu trúc và kiểm tra tính hợp lệ của dữ liệu đầu vào.
Hỗ trợ cả file CSV và Excel (.xlsx, .xls) đa Sheet, lập Source Metadata Registry.
TUYỆT ĐỐI BẢO TOÀN DỮ LIỆU GỐC (Raw Data Preservation) - Không tự ý sửa đổi/xóa dòng.
"""

import os
import csv
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from collections import Counter
from .state import BIWorkflowState, StageStatus

class SheetStage:
    def __init__(self):
        self.stage_name = "SHEET"

    def list_sheets(self, file_path: str) -> List[str]:
        """Liệt kê danh sách tên Sheet nếu là file Excel (.xlsx), trả về ['Default'] nếu là CSV."""
        if not os.path.exists(file_path):
            return []
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            return ["Default"]
        elif ext in [".xlsx", ".xlsm"]:
            try:
                with zipfile.ZipFile(file_path, 'r') as z:
                    if 'xl/workbook.xml' in z.namelist():
                        tree = ET.fromstring(z.read('xl/workbook.xml'))
                        sheets = []
                        for s in tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                            name = s.attrib.get('name')
                            if name:
                                sheets.append(name)
                        return sheets if sheets else ["Sheet1"]
            except Exception:
                return ["Sheet1"]
        return ["Default"]

    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Đọc tệp CSV với encoding utf-8-sig và utf-8, bảo toàn 100% dữ liệu gốc."""
        records = []
        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(dict(row))
        except UnicodeDecodeError:
            with open(file_path, mode="r", encoding="latin-1") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(dict(row))
        return records

    def read_xlsx(self, file_path: str, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Đọc tệp XLSX bằng thư viện chuẩn zipfile + ElementTree theo tên Sheet được chỉ định."""
        records = []
        with zipfile.ZipFile(file_path, 'r') as z:
            # 1. Đọc shared strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
                for si in tree.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                    # Trích xuất toàn bộ text trong node
                    text_parts = [t.text for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t') if t.text]
                    shared_strings.append("".join(text_parts) if text_parts else "")

            # 2. Xác định file XML của Sheet được chọn
            sheet_target = "worksheets/sheet1.xml"
            if 'xl/workbook.xml' in z.namelist() and 'xl/_rels/workbook.xml.rels' in z.namelist():
                wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
                rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
                
                # Bản đồ rId -> target file
                rel_map = {}
                for rel in rels_tree.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                    r_id = rel.attrib.get('Id')
                    target = rel.attrib.get('Target')
                    if r_id and target:
                        rel_map[r_id] = target.replace('\\', '/')

                # Tìm r:id tương ứng với sheet_name
                target_found = None
                first_target = None
                for s in wb_tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                    s_name = s.attrib.get('name')
                    r_id = s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                    target = rel_map.get(r_id, '')
                    if not first_target and target:
                        first_target = target
                    if s_name and sheet_name and s_name.strip().lower() == sheet_name.strip().lower():
                        target_found = target
                        break

                sheet_target = target_found or first_target or "worksheets/sheet1.xml"
                if not sheet_target.startswith("xl/"):
                    sheet_target = "xl/" + sheet_target

            # 3. Phân tích nội dung Sheet XML
            if sheet_target in z.namelist():
                sheet_tree = ET.fromstring(z.read(sheet_target))
                rows = sheet_tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
                
                headers = []
                for idx, r in enumerate(rows):
                    cells = r.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                    row_vals = []
                    for c in cells:
                        v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        val_str = v.text if v is not None else ""
                        if c.attrib.get('t') == 's' and val_str.isdigit():
                            idx_str = int(val_str)
                            val_str = shared_strings[idx_str] if idx_str < len(shared_strings) else val_str
                        row_vals.append(val_str)
                    
                    if idx == 0:
                        headers = [h.strip() for h in row_vals]
                    else:
                        row_dict = {}
                        for h_idx, h in enumerate(headers):
                            if h:
                                row_dict[h] = row_vals[h_idx] if h_idx < len(row_vals) else ""
                        records.append(row_dict)
        return records

    def infer_type(self, values: List[Any]) -> str:
        """Suy luận kiểu dữ liệu của một cột dựa trên tập mẫu giá trị không rỗng."""
        non_empty = [str(v).strip() for v in values if v is not None and str(v).strip() != ""]
        if not non_empty:
            return "STRING"

        # Kiểm tra BOOLEAN
        bool_set = {"true", "false", "1", "0", "yes", "no", "đúng", "sai"}
        if all(v.lower() in bool_set for v in non_empty[:20]):
            return "BOOLEAN"

        # Kiểm tra INTEGER
        is_int = True
        for v in non_empty[:30]:
            cleaned = v.replace(',', '')
            if not (cleaned.isdigit() or (cleaned.startswith('-') and cleaned[1:].isdigit())):
                is_int = False
                break
        if is_int:
            return "INTEGER"

        # Kiểm tra FLOAT
        is_float = True
        for v in non_empty[:30]:
            cleaned = v.replace(',', '')
            try:
                float(cleaned)
            except ValueError:
                is_float = False
                break
        if is_float:
            return "FLOAT"

        # Kiểm tra DATE
        is_date = True
        for v in non_empty[:30]:
            if not ((len(v) == 10 and v[4] in ['-', '/'] and v[7] in ['-', '/']) or
                    (len(v) == 10 and v[2] in ['-', '/'] and v[5] in ['-', '/'])):
                is_date = False
                break
        if is_date:
            return "DATE"

        return "STRING"

    def inspect_and_validate(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Đọc, nhận diện cấu trúc, thống kê và kiểm tra tính hợp lệ của tệp dữ liệu.
        Chỉ ghi nhận vấn đề và cảnh báo, TUYỆT ĐỐI KHÔNG làm sạch hay chỉnh sửa dữ liệu gốc.
        """
        blocking_errors = []
        warnings = []

        if not os.path.exists(file_path):
            blocking_errors.append(f"Không tìm thấy tệp tin: {file_path}")
            return {
                "status": "ERROR",
                "readable": False,
                "file_name": os.path.basename(file_path),
                "file_size": 0,
                "rows_count": 0,
                "row_count": 0,
                "columns_count": 0,
                "column_count": 0,
                "columns": [],
                "validation": {
                    "blocking_errors": blocking_errors,
                    "warnings": warnings,
                    "can_proceed_to_cleaning": False
                },
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": False
            }

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            blocking_errors.append("Tệp tin hoàn toàn rỗng (0 bytes). Vui lòng chọn tệp có dữ liệu.")
            return {
                "status": "ERROR",
                "readable": False,
                "file_name": os.path.basename(file_path),
                "file_size": 0,
                "rows_count": 0,
                "row_count": 0,
                "columns_count": 0,
                "column_count": 0,
                "columns": [],
                "validation": {
                    "blocking_errors": blocking_errors,
                    "warnings": warnings,
                    "can_proceed_to_cleaning": False,
                    "rejection_title": "LỖI – DỮ LIỆU KHÔNG ĐẦY ĐỦ",
                    "rejection_message": "NexusBI không thể tiếp tục xử lý vì tệp dữ liệu tải lên không đáp ứng đầy đủ yêu cầu đầu vào. Vui lòng kiểm tra lại nội dung, cấu trúc và tính hợp lệ của dữ liệu trước khi tải lên."
                },
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": False
            }

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".csv", ".xlsx", ".xls", ".xlsm"]:
            blocking_errors.append(f"Định dạng tệp '{ext}' không được hỗ trợ. Chỉ hỗ trợ .csv, .xlsx, .xls.")
            return {
                "status": "ERROR",
                "readable": False,
                "file_name": os.path.basename(file_path),
                "file_size": file_size,
                "rows_count": 0,
                "row_count": 0,
                "columns_count": 0,
                "column_count": 0,
                "columns": [],
                "validation": {
                    "blocking_errors": blocking_errors,
                    "warnings": warnings,
                    "can_proceed_to_cleaning": False,
                    "rejection_title": "LỖI – DỮ LIỆU KHÔNG ĐẦY ĐỦ",
                    "rejection_message": "NexusBI không thể tiếp tục xử lý vì tệp dữ liệu tải lên không đáp ứng đầy đủ yêu cầu đầu vào. Vui lòng kiểm tra lại nội dung, cấu trúc và tính hợp lệ của dữ liệu trước khi tải lên."
                },
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": False
            }

        available_sheets = self.list_sheets(file_path)
        chosen_sheet = sheet_name if sheet_name in available_sheets else available_sheets[0]

        records = []
        try:
            if ext == ".csv":
                records = self.read_csv(file_path)
            else:
                records = self.read_xlsx(file_path, chosen_sheet)
        except Exception as e:
            blocking_errors.append(f"Không thể đọc hoặc phân tích cú pháp tệp dữ liệu: {str(e)}")
            return {
                "status": "ERROR",
                "readable": False,
                "file_name": os.path.basename(file_path),
                "file_size": file_size,
                "rows_count": 0,
                "row_count": 0,
                "columns_count": 0,
                "column_count": 0,
                "columns": [],
                "validation": {
                    "blocking_errors": blocking_errors,
                    "warnings": warnings,
                    "can_proceed_to_cleaning": False,
                    "rejection_title": "LỖI – DỮ LIỆU KHÔNG ĐẦY ĐỦ",
                    "rejection_message": "NexusBI không thể tiếp tục xử lý vì tệp dữ liệu tải lên không đáp ứng đầy đủ yêu cầu đầu vào. Vui lòng kiểm tra lại nội dung, cấu trúc và tính hợp lệ của dữ liệu trước khi tải lên."
                },
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": False
            }

        if not records:
            blocking_errors.append("Tệp dữ liệu không có bản ghi (0 dòng dữ liệu). Hệ thống chỉ phát hiện dòng tiêu đề cột.")
            return {
                "status": "ERROR",
                "readable": True,
                "file_name": os.path.basename(file_path),
                "file_size": file_size,
                "available_sheets": available_sheets,
                "selected_sheet": chosen_sheet,
                "rows_count": 0,
                "row_count": 0,
                "columns_count": 0,
                "column_count": 0,
                "columns": [],
                "validation": {
                    "blocking_errors": blocking_errors,
                    "warnings": warnings,
                    "can_proceed_to_cleaning": False,
                    "rejection_title": "LỖI – DỮ LIỆU KHÔNG ĐẦY ĐỦ",
                    "rejection_message": "NexusBI không thể tiếp tục xử lý vì tệp dữ liệu tải lên không đáp ứng đầy đủ yêu cầu đầu vào. Vui lòng kiểm tra lại nội dung, cấu trúc và tính hợp lệ của dữ liệu trước khi tải lên."
                },
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": False
            }

        # 1. Nhận diện tiêu đề cột và trùng lặp cột
        raw_headers = [str(col).strip() for col in records[0].keys() if col is not None and str(col).strip() != ""]
        duplicate_cols = [col for col, count in Counter(raw_headers).items() if count > 1]
        if duplicate_cols:
            warnings.append(f"Phát hiện tiêu đề cột bị trùng lặp: {', '.join(duplicate_cols)}. Cần xử lý ở bước Cleaning.")

        # Kiểm tra tiêu đề rỗng hoặc Unnamed
        unnamed_cols = [col for col in raw_headers if not col or col.startswith("Unnamed")]
        if unnamed_cols:
            warnings.append(f"Có {len(unnamed_cols)} cột không có tên tiêu đề rõ ràng ({', '.join(unnamed_cols[:3])}...).")

        # 2. Đếm ô có dữ liệu, ô trống và dòng trống hoàn toàn
        blank_rows_count = 0
        total_cells = len(records) * len(raw_headers)
        filled_cells = 0
        column_profiles = {}

        for col in raw_headers:
            column_profiles[col] = {
                "non_null_count": 0,
                "null_count": 0,
                "sample_values": []
            }

        for row in records:
            is_row_blank = True
            for col in raw_headers:
                val = row.get(col)
                val_str = str(val).strip() if val is not None else ""
                if val_str != "":
                    is_row_blank = False
                    filled_cells += 1
                    column_profiles[col]["non_null_count"] += 1
                    if len(column_profiles[col]["sample_values"]) < 3:
                        column_profiles[col]["sample_values"].append(val_str)
                else:
                    column_profiles[col]["null_count"] += 1
            if is_row_blank:
                blank_rows_count += 1

        empty_cells = total_cells - filled_cells
        if blank_rows_count > 0:
            warnings.append(f"Phát hiện {blank_rows_count} dòng hoàn toàn trống. Sẽ được lọc bỏ ở Bước 2 (Cleaning).")

        # 3. Suy luận kiểu dữ liệu từng cột (Schema Profiling)
        detected_schema = {}
        for col in raw_headers:
            col_vals = [r.get(col) for r in records[:100]]
            inferred = self.infer_type(col_vals)
            detected_schema[col] = inferred
            column_profiles[col]["inferred_type"] = inferred

            # Cảnh báo cột có tỷ lệ trống cao
            null_pct = round((column_profiles[col]["null_count"] / max(1, len(records))) * 100, 1)
            if null_pct > 20:
                warnings.append(f"Cột '{col}' có {column_profiles[col]['null_count']} giá trị trống ({null_pct}%).")

        # 4. Phân loại cấu trúc trường: Measures vs Dimensions
        classified = self.categorize_columns(raw_headers, detected_schema)

        # 5. Kiểm tra tính đầy đủ và phù hợp để phân tích
        empty_ratio = (empty_cells / total_cells) if total_cells > 0 else 0
        if empty_ratio > 0.75:
            blocking_errors.append(f"Tỷ lệ dữ liệu trống quá cao ({round(empty_ratio * 100, 1)}% ô dữ liệu bị rỗng). Không đủ cơ sở để AI Agent thực hiện phân tích.")

        if len(classified.get("measures", [])) == 0:
            blocking_errors.append("Tệp thiếu các trường dữ liệu định lượng cần thiết (không tìm thấy cột số liệu, doanh thu, đơn giá hoặc chỉ số đo lường).")

        # 6. Đánh giá khả năng sử dụng dữ liệu (Data Usability Assessment)
        can_proceed = len(blocking_errors) == 0 and len(records) > 0 and len(raw_headers) > 0
        usability_score = 100 if len(warnings) == 0 else max(70, 100 - (len(warnings) * 5))
        usability_rating = "OPTIMAL_READY" if len(warnings) == 0 and can_proceed else "READY_WITH_WARNINGS" if can_proceed else "BLOCKED"

        manifest = {
            "status": "COMPLETED" if can_proceed else "ERROR",
            "readable": True,
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "file_size": file_size,
            "format": ext.upper().replace('.', ''),
            "available_sheets": available_sheets,
            "selected_sheet": chosen_sheet,
            "rows_count": len(records),
            "row_count": len(records),
            "columns_count": len(raw_headers),
            "column_count": len(raw_headers),
            "columns": raw_headers,
            "detected_schema": detected_schema,
            "column_profiles": column_profiles,
            "classified_columns": classified,
            "usability_score": usability_score if can_proceed else 0,
            "usability_rating": usability_rating,
            "total_cells": total_cells,
            "filled_cells": filled_cells,
            "empty_cells": empty_cells,
            "blank_rows_count": blank_rows_count,
            "preview_data": records[:15],
            "preview_rows": records[:15],
            "validation": {
                "has_headers": True,
                "duplicate_columns": duplicate_cols,
                "is_empty": False,
                "blocking_errors": blocking_errors,
                "warnings": warnings,
                "can_proceed_to_cleaning": can_proceed,
                "rejection_title": None if can_proceed else "LỖI – DỮ LIỆU KHÔNG ĐẦY ĐỦ",
                "rejection_message": None if can_proceed else "NexusBI không thể tiếp tục xử lý vì tệp dữ liệu tải lên không đáp ứng đầy đủ yêu cầu đầu vào. Vui lòng kiểm tra lại nội dung, cấu trúc và tính hợp lệ của dữ liệu trước khi tải lên."
            },
            "raw_records": records if can_proceed else []  # Chỉ lưu trữ khi tệp hợp lệ
        }
        return manifest

    def categorize_columns(self, columns: List[str], schema: Dict[str, str]) -> Dict[str, List[str]]:
        """Phân loại cột thành Chỉ số đo lường (Measures/Metrics) và Chiều phân tích (Dimensions)."""
        measures = []
        dimensions = []
        for col in columns:
            t = schema.get(col, "STRING")
            lower_name = col.lower()
            # Nếu là kiểu số và không chứa từ khóa định danh ID / Code / Zip
            if t in ["INTEGER", "FLOAT"] and not any(k in lower_name for k in ["id", "code", "zip", "phone", "key", "number"]):
                measures.append(col)
            else:
                dimensions.append(col)
        return {
            "measures": measures,
            "dimensions": dimensions
        }

    def evaluate_business_questions(self, questions: List[str], columns: List[str], schema: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        AI phân tích và đánh giá tính khả thi của các câu hỏi kinh doanh đối với nguồn dữ liệu hiện có.
        Xác định trường cần thiết, đối chiếu cột thực tế và phát hiện nếu thiếu dữ liệu,
        tuyệt đối không tự suy đoán.
        """
        cols_lower = {col.lower(): col for col in columns}
        results = []

        domain_keywords = {
            "revenue": {
                "keywords": ["doanh thu", "doanh số", "bán hàng", "tiền bán", "revenue", "sales", "aov"],
                "target_cols": ["unitprice", "quantity", "netsales", "grosssales", "revenue", "totalamount"]
            },
            "profit": {
                "keywords": ["lợi nhuận", "lãi", "biên lợi nhuận", "profit", "margin"],
                "target_cols": ["unitcost", "unitprice", "profit", "cost"]
            },
            "discount": {
                "keywords": ["chiết khấu", "giảm giá", "khuyến mãi", "discount"],
                "target_cols": ["discountamount", "discount"]
            },
            "channel": {
                "keywords": ["kênh", "kênh bán", "sàn", "channel", "platform"],
                "target_cols": ["channel", "saleschannel", "platform"]
            },
            "product": {
                "keywords": ["sản phẩm", "mặt hàng", "ngành hàng", "danh mục", "product", "item", "category"],
                "target_cols": ["productid", "productname", "category", "sku"]
            },
            "customer": {
                "keywords": ["khách hàng", "người mua", "user", "customer", "client", "rfm"],
                "target_cols": ["customerid", "customername", "customertype"]
            },
            "time": {
                "keywords": ["thời gian", "tháng", "quý", "năm", "ngày", "kỳ", "date", "month", "quarter", "year"],
                "target_cols": ["orderdate", "date", "createdat", "time"]
            },
            "rep": {
                "keywords": ["nhân viên", "sales", "người bán", "salesrep"],
                "target_cols": ["salesrepid", "salesperson", "rep"]
            },
            "branch": {
                "keywords": ["chi nhánh", "cửa hàng", "kho", "branch", "store", "warehouse"],
                "target_cols": ["branch", "storeid", "storename", "branchid", "warehouseid"]
            },
            "shipping": {
                "keywords": ["vận chuyển", "giao hàng", "ship", "shipping"],
                "target_cols": ["shippingfee", "shippingcost", "carrier"]
            },
            "cost": {
                "keywords": ["chi phí", "ngân sách", "quảng cáo", "vận hành", "cost", "expense", "budget", "adspend"],
                "target_cols": ["cost", "expense", "budget", "adspend"]
            }
        }

        # Giới hạn tối đa 8 câu hỏi theo quy chuẩn
        valid_questions = [q.strip() for q in questions if q.strip()][:8]

        for q_clean in valid_questions:
            q_lower = q_clean.lower()
            matched_domains = []
            available_cols_matched = []
            missing_domains = []

            for dom, meta in domain_keywords.items():
                if any(kw in q_lower for kw in meta["keywords"]):
                    matched_domains.append(dom)
                    found_col = None
                    for target in meta["target_cols"]:
                        for actual_lower, actual_col in cols_lower.items():
                            if target in actual_lower or actual_lower in target:
                                found_col = actual_col
                                if actual_col not in available_cols_matched:
                                    available_cols_matched.append(actual_col)
                                break
                        if found_col:
                            break
                    if not found_col:
                        missing_domains.append(dom)

            # Phân loại tính khả thi
            if not matched_domains:
                status = "REQUIRES_REVIEW"
                message = "Câu hỏi phân tích bao quát. Bảng dữ liệu có thể hỗ trợ khai phá tổng quan."
            elif not missing_domains:
                status = "FEASIBLE"
                cols_str = ", ".join(available_cols_matched)
                message = f"Khả thi 100%: Có đủ trường dữ liệu ({cols_str}) để giải quyết câu hỏi này."
            elif len(available_cols_matched) > 0 and len(missing_domains) > 0:
                missing_str = ", ".join([domain_keywords[m]["keywords"][0] for m in missing_domains])
                cols_str = ", ".join(available_cols_matched)
                status = "PARTIALLY_FEASIBLE"
                message = f"Khả thi một phần: Có trường ({cols_str}), nhưng thiếu dữ liệu về '{missing_str}'."
            else:
                missing_str = ", ".join([domain_keywords[m]["keywords"][0] for m in missing_domains])
                status = "UNSUPPORTED"
                message = f"⚠️ Cảnh báo: Tệp dữ liệu hiện tại không có cột về '{missing_str}' để trả lời câu hỏi này."

            results.append({
                "question": q_clean,
                "status": status,
                "domains": matched_domains,
                "matched_columns": available_cols_matched,
                "missing_domains": missing_domains,
                "analysis_note": message
            })

        return results

    def execute(self, state: BIWorkflowState, input_files: List[str], selected_sheet: Optional[str] = None) -> BIWorkflowState:
        """
        Thực thi giai đoạn 1: SHEET – DATA INGESTION
        Nạp tệp, tạo Ingestion Manifest và bàn giao nguyên vẹn dữ liệu cho state.raw_data.
        """
        state.update_stage_status("SHEET", StageStatus.IN_PROGRESS)
        source_registry = []

        for fpath in input_files:
            manifest = self.inspect_and_validate(fpath, selected_sheet)
            if not manifest.get("readable") or not manifest["validation"]["can_proceed_to_cleaning"]:
                err_msg = "; ".join(manifest["validation"]["blocking_errors"]) or "Lỗi đọc tệp dữ liệu"
                state.update_stage_status("SHEET", StageStatus.FAILED, err_msg)
                raise IOError(f"[SHEET Stage Error] {err_msg}")

            table_key = os.path.splitext(os.path.basename(fpath))[0]
            # Bàn giao dữ liệu gốc 100% sang state
            state.raw_data[table_key] = manifest["raw_records"]

            source_registry.append({
                "table_key": table_key,
                "file_name": manifest["file_name"],
                "file_path": manifest["file_path"],
                "format": manifest["format"],
                "selected_sheet": manifest["selected_sheet"],
                "rows_count": manifest["rows_count"],
                "columns_count": manifest["columns_count"],
                "columns": manifest["columns"],
                "schema": manifest["detected_schema"],
                "filled_cells": manifest["filled_cells"],
                "empty_cells": manifest["empty_cells"],
                "warnings_count": len(manifest["validation"]["warnings"]),
                "warnings": manifest["validation"]["warnings"],
                "status": "COMPLETED"
            })

        state.source_metadata = source_registry
        state.update_stage_status("SHEET", StageStatus.SUCCESS)
        return state

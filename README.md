# AI-POWERED BUSINESS INTELLIGENCE PLATFORM (DỰ ÁN CUỐI MÔN AI301)

Nền tảng Business Intelligence thông minh định hướng theo phương châm cốt lõi:
$$\textbf{DATA} \longrightarrow \textbf{INFORMATION} \longrightarrow \textbf{INSIGHT} \longrightarrow \textbf{DECISION} \longrightarrow \textbf{ACTION}$$

---

## 1. QUY TRÌNH VẬN HÀNH BI 7 GIAI ĐOẠN (BI WORKFLOW)

Hệ thống được vận hành theo quy trình phân tích chuẩn 7 giai đoạn:
$$\textbf{SHEET} \longrightarrow \textbf{CLEANING} \longrightarrow \textbf{PROCESS} \longrightarrow \textbf{VERIFY} \longrightarrow \textbf{FEEDBACK} \genfrac{}{}{0pt}{}{\nearrow \textbf{EXPORT}}{\searrow \textbf{REPORT}}$$

1. **SHEET**: Tiếp nhận CSV/XLSX/XLS, đọc Sheet, kiểm tra định dạng và khả năng đọc, tạo Source Metadata Registry, bảo toàn 100% dữ liệu gốc.
2. **CLEANING**: Làm sạch dữ liệu, khử trùng lặp, xử lý thiếu sót, chuẩn hóa kiểu dữ liệu, tính Data Quality Scorecard (100/100) và lập Cleaning Audit Log.
3. **PROCESS**: Tính toán KPI cốt lõi, xây dựng mô hình Star Schema, phân tích đa chiều OLAP (12 tháng, 4 quý, 6 kênh bán) và phân cụm khách hàng RFM.
4. **VERIFY (GATE)**: Kiểm chứng công thức tài chính, đối chiếu đầu vào - đầu ra. Cổng bảo vệ bắt buộc: Khóa hoàn toàn xuất dữ liệu và báo cáo nếu chưa Pass 100%.
5. **FEEDBACK**: Tiếp nhận đánh giá người dùng, cho phép thay đổi tham số/bộ lọc, lưu lịch sử phản hồi và hỗ trợ vòng lặp **"Điều chỉnh & Tái phân tích" (Loopback to Stage 2/3)**.
6. **EXPORT**: Xuất dữ liệu sạch và các bảng biểu kết quả ra CSV/Excel trong thư mục `data/export/`, bảo đảm khớp 100% số liệu đã kiểm chứng.
7. **REPORT**: Báo cáo quản trị cấp cao theo cấu trúc Kim tự tháp Minto (Lead with Conclusion), phân tích biến động, trích xuất Insight và khuyến nghị hành động.

---

## 2. CẤU TRÚC DỰ ÁN

```text
├── workflow/                     # Quy trình vận hành cốt lõi 7 Giai đoạn
│   ├── state.py                  # Cấu trúc trạng thái thống nhất (BIWorkflowState)
│   ├── stage_1_sheet.py          # Giai đoạn 1: Tiếp nhận & đọc tệp
│   ├── stage_2_cleaning.py       # Giai đoạn 2: Làm sạch & Data Quality
│   ├── stage_3_process.py        # Giai đoạn 3: Tính toán KPI & OLAP
│   ├── stage_4_verify.py         # Giai đoạn 4: Cổng kiểm chứng bắt buộc (Gate)
│   ├── stage_5_feedback.py       # Giai đoạn 5: Phản hồi & Vòng lặp Loopback
│   ├── stage_6_export.py         # Giai đoạn 6: Xuất dữ liệu kiểm chứng
│   ├── stage_7_report.py         # Giai đoạn 7: Báo cáo quản trị Minto
│   └── engine.py                 # Bộ điều phối Workflow Engine
├── core/
│   └── orchestrator.py           # AI Agent Core điều phối 12 Skills
├── skills/                       # 12 BI Skills độc lập
├── data/
│   ├── raw/                      # Dữ liệu gốc được bảo toàn
│   ├── processed/                # Dữ liệu sạch sau chuẩn hóa
│   ├── export/                   # Dữ liệu xuất chính thức (Đã Verify)
│   ├── bi_system_payload.json    # Payload hệ thống đầy đủ
│   └── workflow_execution_state.json # Nhật ký trạng thái 7 giai đoạn
├── warehouse/
│   └── bi_datawarehouse.db       # SQLite Star Schema Data Warehouse
├── ui/
│   ├── index.html                # Giao diện SaaS BI & 7-Stage Workflow Studio
│   ├── app.js                    # Controller tương tác thời gian thực
│   └── payload.js                # State đồng bộ trực tiếp
└── tests/
    └── test_bi_platform.py       # Bộ kiểm thử tự động toàn diện (100% PASS)
```

---

## 3. HƯỚNG DẪN THỰC THI

### Chạy Quy Trình BI 7 Giai Đoạn:
```bash
python workflow/engine.py
```

### Chạy Bộ Kiểm Thử Tự Động (Bao gồm Cổng Verify & Vòng Lặp Loopback):
```bash
python -m unittest tests/test_bi_platform.py
```

### Trải Nghiệm Giao Diện SaaS Web Platform:
Mở trực tiếp tệp `ui/index.html` trên trình duyệt web. Nền tảng tích hợp toàn diện:
- Thanh điều khiển tương tác trực quan 7 Giai đoạn (**★ 7-Stage BI Workflow**).
- Cổng đối chiếu 6 quy tắc toán học (Gate Verify Console).
- Khung phản hồi điều chỉnh tham số & tái phân tích thời gian thực (**🔄 Điều chỉnh & Tái phân tích**).
- 10 phân hệ nghiệp vụ quản trị doanh nghiệp và Trợ lý AI BI Assistant tương tác.

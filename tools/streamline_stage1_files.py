import re

print("=== STREAMLINING STAGE 1 FILE SELECTOR (REMOVING CLUTTERED FILE CHIPS) ===")

with open('ui/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Define the new streamlined file selection UI block
new_stage1_replacement = '''function renderStage1_Connection() {
  const m = currentSheetManifest || {};
  const isLoaded = !!currentSheetManifest;
  const rows = m.preview_data || [];
  const cols = m.columns || (rows[0] ? Object.keys(rows[0]) : []);

  // Giao diện chọn tệp tinh gọn (Loại bỏ 8 nút phân tán, thay bằng dropdown và active banner)
  let fileControlHtml = "";
  if (isLoaded) {
    fileControlHtml = `
      <div class="p-3.5 rounded-2xl bg-[#E8F2EE] border border-[#10B981]/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs shadow-sm">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-[#0A261D] text-[#D4B07B] flex items-center justify-center font-bold text-xs shrink-0 shadow-sm border border-[#D4B07B]/30">
            ✓
          </div>
          <div>
            <div class="font-bold text-[#0A261D] flex items-center gap-2">
              <span class="text-xs md:text-sm">${currentSelectedFile}</span>
              <span class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-[#10B981] text-white">Đang sử dụng</span>
            </div>
            <div class="text-[11px] text-[#4A635A] mt-0.5">
              ${m.file_format || 'Tệp'} · ${(m.rows_count || rows.length).toLocaleString()} dòng · ${m.columns_count || cols.length} cột
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 self-end sm:self-auto">
          <!-- Dropdown đổi tệp mẫu -->
          <select onchange="if(this.value) inspectSheetFile(this.value)" class="px-3 py-1.5 text-xs rounded-xl glass-input text-[#0A261D] cursor-pointer font-medium">
            <option value="">Đổi tệp mẫu khác...</option>
            ${(availableSystemFiles || []).map(f => `
              <option value="${f.file_name}" ${currentSelectedFile === f.file_name ? 'selected' : ''}>📄 ${f.file_name}</option>
            `).join('')}
          </select>
          <!-- Nút tải tệp mới -->
          <label class="cursor-pointer px-3.5 py-1.5 rounded-xl bg-[#0A261D] hover:bg-[#133A2D] text-white font-bold text-xs shadow-md shadow-[#0A261D]/20 transition inline-flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-[#D4B07B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
            <span>Tải tệp mới</span>
            <input type="file" accept=".xlsx,.xls,.csv" onchange="handleCustomFileUpload(event)" class="hidden">
          </label>
        </div>
      </div>
    `;
  } else {
    fileControlHtml = `
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
        <!-- Dropdown chọn nhanh tệp mẫu -->
        <div class="relative flex-1">
          <select id="sample-file-select" onchange="if(this.value) inspectSheetFile(this.value)" class="w-full pl-9 pr-8 py-2.5 text-xs rounded-xl glass-input text-[#0A261D] cursor-pointer font-medium appearance-none">
            <option value="">-- Chọn tệp dữ liệu mẫu trong hệ thống (${(availableSystemFiles || []).length} tệp) --</option>
            ${(availableSystemFiles || []).map(f => `
              <option value="${f.file_name}" ${currentSelectedFile === f.file_name ? 'selected' : ''}>📄 ${f.file_name}</option>
            `).join('')}
          </select>
          <div class="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-[#C8A870]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
          </div>
          <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[#4A635A]">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>

        <!-- Nút tải tệp mới -->
        <label class="cursor-pointer px-4 py-2.5 rounded-xl bg-[#0A261D] hover:bg-[#133A2D] text-white font-bold text-xs shadow-md shadow-[#0A261D]/20 transition inline-flex items-center justify-center gap-1.5 shrink-0">
          <svg class="w-3.5 h-3.5 text-[#D4B07B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
          <span>Tải tệp mới (.xlsx, .csv)</span>
          <input type="file" accept=".xlsx,.xls,.csv" onchange="handleCustomFileUpload(event)" class="hidden">
        </label>
      </div>
    `;
  }

  let sheetChipsHtml = "";
  if (m.available_sheets && m.available_sheets.length > 1) {
    sheetChipsHtml = `
      <div class="flex items-center gap-2 mt-2 pt-2 border-t border-[#ECE4D8]">
        <span class="text-xs text-[#4A635A] font-medium">Chọn Sheet:</span>
        <div class="flex flex-wrap gap-1.5">
          ${m.available_sheets.map(s => {
            const isSel = (currentSelectedSheet === s);
            return `
              <button onclick="inspectSheetFile('${currentSelectedFile}', '${s}')" class="px-3 py-1 rounded-xl text-xs transition ${isSel ? 'bg-[#0A261D] text-white border border-[#D4B07B] shadow-sm font-semibold' : 'glass-pill hover:bg-[#F5EFE6] text-[#0A261D]'}">
                ${s}
              </button>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  let tableHtml = "";
  if (rows && rows.length > 0) {
    tableHtml = `
      <div class="border border-[#ECE4D8] rounded-2xl overflow-hidden mt-3 shadow-sm bg-white">
        <div class="overflow-x-auto max-h-72">
          <table class="w-full text-xs text-left text-[#0A261D]">
            <thead class="text-[10px] text-[#4A635A] uppercase bg-[#F5EFE6] border-b border-[#ECE4D8] sticky top-0 font-mono">
              <tr>
                ${cols.map(c => `<th class="px-3.5 py-2.5 font-bold whitespace-nowrap">${c}</th>`).join('')}
              </tr>
            </thead>
            <tbody class="divide-y divide-[#ECE4D8] font-mono text-[11px]">
              ${rows.slice(0, 6).map(r => `
                <tr class="hover:bg-[#F5EFE6]/70 transition">
                  ${cols.map(c => {
                    const val = r[c];
                    const isNum = typeof val === 'number';
                    return `<td class="px-3.5 py-2.5 whitespace-nowrap ${isNum ? 'text-right font-medium' : ''}">${isNum ? val.toLocaleString() : (val !== null && val !== undefined ? val : '')}</td>`;
                  }).join('')}
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } else {
    tableHtml = `
      <label class="cursor-pointer border-2 border-dashed border-[#E2D9C8] hover:border-[#D4B07B] rounded-2xl p-8 flex flex-col items-center justify-center text-center transition bg-[#FAF7F2]/40 hover:bg-[#FAF7F2]/80 mt-3 group">
        <input type="file" accept=".xlsx,.xls,.csv" onchange="handleCustomFileUpload(event)" class="hidden">
        <div class="w-12 h-12 rounded-2xl bg-[#E8F2EE] group-hover:bg-[#0A261D] group-hover:text-white text-[#0D2B22] flex items-center justify-center mb-3 transition shadow-sm border border-[#D4B07B]/40">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
        </div>
        <p class="text-xs font-bold text-[#0A261D] group-hover:text-[#0A261D]">Nhấp để tải lên tệp (.xlsx, .csv) hoặc kéo thả vào đây</p>
        <p class="text-[11px] text-[#4A635A] mt-1 max-w-sm">Hỗ trợ định dạng bảng tính Excel và CSV. Toàn bộ chỉ số sẽ tự động cập nhật khi tệp được nạp.</p>
      </label>
    `;
  }

  return `
    <div class="space-y-5">
      
      <!-- DUAL-PANE GRID: LEFT FORM (5 COLS) + RIGHT DATA CENTER (7 COLS) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        <!-- PANE 1 (LEFT 5 COLS): THIẾT LẬP BỐI CẢNH & CÂU HỎI KINH DOANH -->
        <div class="lg:col-span-5 glass-card p-6 flex flex-col justify-between space-y-4">
          <div class="space-y-4">
            
            <!-- HEADER -->
            <div class="flex items-center gap-3 border-b border-[#ECE4D8] pb-3">
              <div class="w-9 h-9 rounded-xl bg-[#F5EFE6] text-[#0A261D] flex items-center justify-center shrink-0 border border-[#D4B07B]/40 shadow-sm">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
              </div>
              <div>
                <h2 class="font-bold text-[#0A261D] text-sm md:text-base">Thiết Lập Bối Cảnh Nghiệp Vụ</h2>
                <p class="text-[11px] text-[#4A635A]">Định hướng các chỉ số KPI theo mô hình kinh doanh.</p>
              </div>
            </div>

            <!-- FIELD 1: LOẠI HÌNH DOANH NGHIỆP -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="text-xs font-semibold text-[#0A261D]">Loại hình doanh nghiệp <span class="text-[#0A261D]">*</span></label>
                <span class="text-[9px] font-bold text-[#0A261D] bg-[#F5EFE6] px-2.5 py-0.5 rounded-full border border-[#D4B07B]/40">BẮT BUỘC</span>
              </div>
              <input type="text" id="ctx-company-type" value="${currentBusinessContext.company_type || ''}" placeholder="Ví dụ: Bán lẻ thời trang, SaaS B2B, dịch vụ logistics" class="w-full px-4 py-2.5 text-xs rounded-xl glass-input text-[#0A261D] transition">
            </div>

            <!-- FIELD 2: THÔNG TIN BỔ SUNG -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="text-xs font-semibold text-[#0A261D]">Phạm vi & Thông tin bổ sung</label>
                <span class="text-[9px] text-[#4A635A] font-medium">TÙY CHỌN</span>
              </div>
              <input type="text" id="ctx-notes-input" value="${currentBusinessContext.additional_notes || ''}" placeholder="Ví dụ: Đánh giá hiệu quả 5 kênh bán và danh mục sản phẩm chính 4 quý năm 2025" class="w-full px-4 py-2.5 text-xs rounded-xl glass-input text-[#0A261D] transition">
            </div>

            <!-- FIELD 3: CÂU HỎI KINH DOANH -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="text-xs font-semibold text-[#0A261D]">Bài toán kinh doanh cần phân tích <span class="text-[#0A261D]">*</span></label>
                <button onclick="loadQuickQuestionTemplate('retail')" class="text-[11px] text-[#0A261D] hover:text-[#0A261D] font-bold transition">Nạp mẫu câu hỏi</button>
              </div>
              <textarea id="ctx-questions-input" rows="4" placeholder="Doanh thu theo kênh nào cao nhất?\\nSản phẩm nào mang lại lợi nhuận cao nhất?\\nChi phí chiết khấu ảnh hưởng thế nào đến biên lợi nhuận?" class="w-full px-4 py-2.5 text-xs rounded-xl glass-input text-[#0A261D] resize-none font-sans leading-relaxed transition">${(currentBusinessContext.questions || []).join('\\n')}</textarea>
              <div class="text-[10px] text-[#4A635A] mt-1.5 flex items-center justify-between">
                <span>Nhập tối đa 8 câu hỏi (mỗi câu 1 dòng).</span>
                <span class="text-[#D4B07B] font-semibold">Tự động trả lời ở Bước 3</span>
              </div>
            </div>

          </div>

          <!-- ALERT NOTICE -->
          <div class="p-3.5 rounded-2xl glass-input text-[11px] text-[#0A261D] flex items-center gap-2.5">
            <svg class="w-4 h-4 text-[#0A261D] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Dữ liệu sẽ được bảo toàn nguyên vẹn và xác thực xuyên suốt toàn bộ 4 giai đoạn.</span>
          </div>
        </div>

        <!-- PANE 2 (RIGHT 7 COLS): TRUNG TÂM NGUỒN DỮ LIỆU & SCHEMA HEALTH -->
        <div class="lg:col-span-7 glass-card p-6 flex flex-col justify-between space-y-4">
          <div class="space-y-3.5">
            
            <!-- HEADER -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#ECE4D8] pb-3">
              <div>
                <h2 class="font-bold text-[#0A261D] text-sm md:text-base">Khảo Sát Nguồn Dữ Liệu & Schema</h2>
                <p class="text-[11px] text-[#4A635A]">Tiếp nhận tệp dữ liệu, thẩm định schema và kiểm tra khả năng đọc.</p>
              </div>
            </div>

            <!-- STREAMLINED FILE SELECTION CONTROL -->
            ${fileControlHtml}

            ${sheetChipsHtml}

            <!-- 4 SCHEMA METRIC BADGES (TẤT CẢ VỀ 0 KHI CHƯA CHỌN TỆP) -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
              <div class="p-3 rounded-2xl bg-[#F5EFE6]/70 border border-[#E2D9C8] text-xs">
                <span class="text-[#4A635A] block text-[9px] uppercase font-mono font-semibold">Định dạng</span>
                <span class="font-bold text-[#0A261D]">${isLoaded ? (m.file_format || 'CSV / Excel') : '--'}</span>
              </div>
              <div class="p-3 rounded-2xl bg-[#F5EFE6]/70 border border-[#E2D9C8] text-xs">
                <span class="text-[#4A635A] block text-[9px] uppercase font-mono font-semibold">Quy mô</span>
                <span class="font-bold ${isLoaded ? 'text-[#0A261D]' : 'text-[#4A635A]'} font-mono">${isLoaded ? (m.rows_count || rows.length).toLocaleString() + ' dòng' : '0 dòng'}</span>
              </div>
              <div class="p-3 rounded-2xl bg-[#F5EFE6]/70 border border-[#E2D9C8] text-xs">
                <span class="text-[#4A635A] block text-[9px] uppercase font-mono font-semibold">Số trường</span>
                <span class="font-bold ${isLoaded ? 'text-[#0A261D]' : 'text-[#4A635A]'} font-mono">${isLoaded ? (m.columns_count || cols.length) + ' cột' : '0 cột'}</span>
              </div>
              <div class="p-3 rounded-2xl bg-[#F5EFE6]/70 border border-[#E2D9C8] text-xs ${isLoaded ? 'bg-[#E8F2EE] border-[#10B981]/40' : ''}">
                <span class="${isLoaded ? 'text-[#10B981]' : 'text-[#4A635A]'} block text-[9px] uppercase font-mono font-semibold">Tính sẵn sàng</span>
                <span class="font-bold ${isLoaded ? 'text-[#0A261D]' : 'text-[#4A635A]'}">${isLoaded ? '100% Hợp lệ' : '0% (Chờ tệp)'}</span>
              </div>
            </div>

            <!-- TABLE PREVIEW HOẶC DROPZONE -->
            ${tableHtml}

          </div>

          <!-- PRIMARY ACTION CTA -->
          <div class="pt-3 border-t border-[#ECE4D8] flex items-center justify-between">
            <span class="text-xs text-[#4A635A] font-mono">${isLoaded ? 'Giai đoạn 01/04 hoàn tất khi xác nhận' : 'Chờ nạp nguồn dữ liệu (Số liệu: 0)'}</span>
            <button onclick="confirmConnectionAndAdvance()" class="px-6 py-2.5 rounded-xl font-bold text-xs md:text-sm shadow-lg transition flex items-center gap-2 ${isLoaded ? 'bg-[#0A261D] hover:bg-[#133A2D] text-white shadow-[#0A261D]/20 cursor-pointer' : 'bg-[#F5EFE6] text-[#4A635A]/40 opacity-50 cursor-not-allowed border border-[#E2D9C8]'}" ${!isLoaded ? 'disabled' : ''}>
              <span>${isLoaded ? 'Xác Nhận & Mở Khóa Giai Đoạn 2: Làm Sạch Dữ Liệu' : 'Chờ Chọn Tệp Dữ Liệu Để Tiếp Tục'}</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>
          </div>
        </div>

      </div>

    </div>
  `;
}'''

# Replace the old function using regex
pattern = r'function renderStage1_Connection\(\) \{.*?\n\}\n\n// ================= CHI TIẾT BƯỚC 2'
match = re.search(pattern, code, re.DOTALL)
if match:
    code = code[:match.start()] + new_stage1_replacement + "\n\n// ================= CHI TIẾT BƯỚC 2" + code[match.end():]
    print("Replaced renderStage1_Connection successfully!")
else:
    print("Could not find renderStage1_Connection pattern, trying alternate search...")
    idx1 = code.find('function renderStage1_Connection() {')
    idx2 = code.find('// ================= CHI TIẾT BƯỚC 2')
    if idx1 != -1 and idx2 != -1:
        code = code[:idx1] + new_stage1_replacement + "\n\n" + code[idx2:]
        print("Replaced renderStage1_Connection by substring indices successfully!")

with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("ui/app.js updated with streamlined file selector!")

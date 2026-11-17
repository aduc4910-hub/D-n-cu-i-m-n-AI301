import re

with open('tools/generate_navy_blue_app_js.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update initial currentBusinessContext: start with empty so inputs act as clean frosted glass boxes
pattern_ctx = re.compile(r'let currentBusinessContext = \{.*?\};', re.DOTALL)
new_ctx = '''let currentBusinessContext = {
  company_type: "",
  industry: "",
  time_scope: "",
  additional_notes: "",
  questions: []
};'''
text = pattern_ctx.sub(new_ctx, text, count=1)

# 2. Update updateTopSystemInfo to control the dot element
old_top_info = '''function updateTopSystemInfo(manifest) {
  const projEl = document.getElementById('project-dataset-name');
  if (projEl) {
    if (manifest && manifest.file_name) {
      projEl.textContent = `${manifest.file_name} ${manifest.selected_sheet && manifest.selected_sheet !== 'Default' ? '(' + manifest.selected_sheet + ')' : ''}`;
      projEl.className = "text-[11px] font-bold text-[#2563EB]";
    } else {
      projEl.textContent = "Chờ nạp nguồn dữ liệu (Số liệu về 0)";
      projEl.className = "text-[11px] font-semibold text-[#64748B]";
    }
  }
}'''

new_top_info = '''function updateTopSystemInfo(manifest) {
  const projEl = document.getElementById('project-dataset-name');
  const dotEl = document.getElementById('project-dataset-dot');
  if (projEl) {
    if (manifest && manifest.file_name) {
      projEl.textContent = `${manifest.file_name} ${manifest.selected_sheet && manifest.selected_sheet !== 'Default' ? '(' + manifest.selected_sheet + ')' : ''}`;
      projEl.className = "text-[11px] font-bold text-[#2563EB]";
      if (dotEl) dotEl.className = "w-2 h-2 rounded-full bg-[#10B981] animate-pulse";
    } else {
      projEl.textContent = "Chờ nạp nguồn dữ liệu (Số liệu về 0)";
      projEl.className = "text-[11px] font-semibold text-[#64748B]";
      if (dotEl) dotEl.className = "w-2 h-2 rounded-full bg-slate-400";
    }
  }
}'''
text = text.replace(old_top_info, new_top_info)

# 3. Update initApp: DO NOT call inspectSheetFile on startup!
old_init_app = '''function initApp() {
  const wf = window.SYSTEM_DATA?.workflow_state || {};
  if (wf.workflow_id) {
    const el = document.getElementById('footer-wf-id');
    if (el) el.textContent = wf.workflow_id;
  }

  updateTopSystemInfo(null);
  loadAvailableFilesOnly();
  inspectSheetFile('raw_sales_transactions.csv');
  renderHorizontalPipelineBar();
  renderCurrentWorkspace();
}'''

new_init_app = '''function initApp() {
  const wf = window.SYSTEM_DATA?.workflow_state || {};
  if (wf.workflow_id) {
    const el = document.getElementById('footer-wf-id');
    if (el) el.textContent = wf.workflow_id;
  }

  currentSheetManifest = null;
  currentSelectedFile = null;
  currentSelectedSheet = null;
  sheetStateStatus = "PENDING";
  updateTopSystemInfo(null);
  loadAvailableFilesOnly();
  renderHorizontalPipelineBar();
  renderCurrentWorkspace();
}'''
text = text.replace(old_init_app, new_init_app)

# 4. In inspectSheetFile: if context is empty, auto-populate default business context
old_inspect = '''function inspectSheetFile(fileName, sheetName = null) {
  sheetStateStatus = "PROCESSING";
  currentSelectedFile = fileName;
  currentSelectedSheet = sheetName;
  if (currentStepIdx === 0) renderCurrentWorkspace();'''

new_inspect = '''function inspectSheetFile(fileName, sheetName = null) {
  sheetStateStatus = "PROCESSING";
  currentSelectedFile = fileName;
  currentSelectedSheet = sheetName;
  
  if (!currentBusinessContext.company_type) {
    currentBusinessContext.company_type = "Bán lẻ & Thương mại điện tử (Omnichannel)";
    currentBusinessContext.additional_notes = "Đánh giá hiệu quả 5 kênh bán và danh mục sản phẩm chính 4 quý năm 2025.";
    currentBusinessContext.questions = [
      "Doanh thu theo kênh bán hàng nào cao nhất?",
      "Sản phẩm nào mang lại lợi nhuận cao nhất?",
      "Chi phí chiết khấu ảnh hưởng thế nào đến biên lợi nhuận?"
    ];
  }
  if (currentStepIdx === 0) renderCurrentWorkspace();'''
text = text.replace(old_inspect, new_inspect)

# 5. In loadQuickQuestionTemplate: populate context
old_template = '''function loadQuickQuestionTemplate(type) {
  const el = document.getElementById('ctx-questions-input');
  if (el) {
    el.value = [
      "Doanh thu theo kênh bán hàng nào cao nhất?",
      "Sản phẩm nào mang lại lợi nhuận cao nhất?",
      "Chi phí chiết khấu ảnh hưởng thế nào đến biên lợi nhuận?"
    ].join('\\\\n');
    currentBusinessContext.questions = el.value.split('\\\\n');
  }
}'''

new_template = '''function loadQuickQuestionTemplate(type) {
  currentBusinessContext = {
    company_type: "Bán lẻ & Thương mại điện tử (Omnichannel)",
    industry: "Thiết bị Công nghệ & Điện tử thông minh",
    time_scope: "Năm tài chính 2025 (12 tháng)",
    additional_notes: "Đánh giá hiệu quả 5 kênh bán và danh mục sản phẩm chính 4 quý năm 2025.",
    questions: [
      "Doanh thu theo kênh bán hàng nào cao nhất?",
      "Sản phẩm nào mang lại lợi nhuận cao nhất?",
      "Chi phí chiết khấu ảnh hưởng thế nào đến biên lợi nhuận?"
    ]
  };
  const typeEl = document.getElementById('ctx-company-type');
  const notesEl = document.getElementById('ctx-notes-input');
  const questionsEl = document.getElementById('ctx-questions-input');
  if (typeEl) typeEl.value = currentBusinessContext.company_type;
  if (notesEl) notesEl.value = currentBusinessContext.additional_notes;
  if (questionsEl) questionsEl.value = currentBusinessContext.questions.join('\\n');
}'''
# Check if old_template matches or need pattern replacement
if 'function loadQuickQuestionTemplate' in text:
    pattern_tpl = re.compile(r'function loadQuickQuestionTemplate\(type\)\s*\{.*?\}', re.DOTALL)
    text = pattern_tpl.sub(new_template, text, count=1)

# 6. In resetWorkflowProgression: reset context and metrics to 0
old_reset = '''    currentAnalysisManifest = null;
    reportingStateStatus = "PENDING";
    currentReportingManifest = null;
    
    const demoTxt = document.getElementById('txt-demo-toggle');'''

new_reset = '''    currentAnalysisManifest = null;
    reportingStateStatus = "PENDING";
    currentReportingManifest = null;
    currentBusinessContext = {
      company_type: "",
      industry: "",
      time_scope: "",
      additional_notes: "",
      questions: []
    };
    
    const demoTxt = document.getElementById('txt-demo-toggle');'''
text = text.replace(old_reset, new_reset)

# 7. In renderStage1_Connection: file selection must be STRICT (no default selection when currentSelectedFile is null)
old_sel = "const isSel = (currentSelectedFile === f.file_name) || (!currentSelectedFile && f.file_name === 'raw_sales_transactions.csv');"
new_sel = "const isSel = (currentSelectedFile === f.file_name);"
text = text.replace(old_sel, new_sel)

# 8. In renderStage1_Connection: 4 SCHEMA METRIC BADGES must ALWAYS be visible, showing 0 when not loaded
pattern_badges = re.compile(r'\$\{isLoaded \?\s*`<div class="grid grid-cols-2 sm:grid-cols-4 gap-2\.5 pt-1">.*?</div>\s*`\s*:\s*\'\'\}', re.DOTALL)
new_badges = '''<div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
                <div class="p-3 rounded-2xl glass-input text-xs">
                  <span class="text-[#64748B] block text-[9px] uppercase font-mono font-semibold">Định dạng</span>
                  <span class="font-bold text-[#0B1F3A]">${isLoaded ? (m.file_format || 'CSV / Excel') : '--'}</span>
                </div>
                <div class="p-3 rounded-2xl glass-input text-xs">
                  <span class="text-[#64748B] block text-[9px] uppercase font-mono font-semibold">Quy mô</span>
                  <span class="font-bold ${isLoaded ? 'text-[#0B1F3A]' : 'text-[#64748B]'} font-mono">${isLoaded ? (m.rows_count || 1200).toLocaleString() + ' dòng' : '0 dòng'}</span>
                </div>
                <div class="p-3 rounded-2xl glass-input text-xs">
                  <span class="text-[#64748B] block text-[9px] uppercase font-mono font-semibold">Số trường</span>
                  <span class="font-bold ${isLoaded ? 'text-[#0B1F3A]' : 'text-[#64748B]'} font-mono">${isLoaded ? (m.columns_count || 11) + ' cột' : '0 cột'}</span>
                </div>
                <div class="p-3 rounded-2xl glass-input text-xs ${isLoaded ? 'bg-emerald-50/50 border-emerald-200/60' : ''}">
                  <span class="${isLoaded ? 'text-emerald-600' : 'text-[#64748B]'} block text-[9px] uppercase font-mono font-semibold">Tính sẵn sàng</span>
                  <span class="font-bold ${isLoaded ? 'text-emerald-700' : 'text-[#64748B]'}">${isLoaded ? '100% Hợp lệ' : '0% (Chờ tệp)'}</span>
                </div>
              </div>'''

text = pattern_badges.sub(new_badges, text, count=1)

# 9. Update table preview empty state in Stage 1
old_table_empty = '''      <div class="p-8 text-center border-2 border-dashed border-[#E2E8F0] rounded-2xl mt-3 glass-input">
        <p class="text-xs text-[#64748B]">Chọn một tệp từ danh sách trên để xem trước Schema dữ liệu</p>
      </div>'''

new_table_empty = '''      <div class="p-8 text-center border-2 border-dashed border-[#E2E8F0] rounded-2xl mt-3 glass-input flex flex-col items-center justify-center space-y-2">
        <div class="w-10 h-10 rounded-2xl bg-[#F3F7FC] text-[#64748B] flex items-center justify-center border border-[#E2E8F0]">
          <svg class="w-5 h-5 text-[#2563EB]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
        </div>
        <p class="text-xs font-bold text-[#0B1F3A]">Chưa có dữ liệu nguồn (Các chỉ số về 0)</p>
        <p class="text-[11px] text-[#64748B] max-w-sm">Vui lòng nhấp chọn một tệp danh sách phía trên hoặc tải tệp mới (.xlsx, .csv) để hệ thống tự động cập nhật dữ liệu và hiển thị số liệu.</p>
      </div>'''
text = text.replace(old_table_empty, new_table_empty)

# 10. Update CTA Button text when not loaded
old_cta = '''            <span class="text-xs text-[#64748B] font-mono">Giai đoạn 01/04 hoàn tất khi xác nhận</span>
            <button onclick="confirmConnectionAndAdvance()" class="px-6 py-2.5 rounded-xl font-bold text-xs md:text-sm shadow-lg transition flex items-center gap-2 ${isLoaded ? 'bg-[#2563EB] hover:bg-[#1D4ED8] text-white shadow-blue-600/25' : 'bg-slate-200 text-[#64748B] cursor-not-allowed'}" ${!isLoaded ? 'disabled' : ''}>
              <span>Xác Nhận & Mở Khóa Giai Đoạn 2: Làm Sạch Dữ Liệu</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>'''

new_cta = '''            <span class="text-xs text-[#64748B] font-mono">${isLoaded ? 'Giai đoạn 01/04 hoàn tất khi xác nhận' : 'Chờ nạp nguồn dữ liệu (Số liệu: 0)'}</span>
            <button onclick="confirmConnectionAndAdvance()" class="px-6 py-2.5 rounded-xl font-bold text-xs md:text-sm shadow-lg transition flex items-center gap-2 ${isLoaded ? 'bg-[#2563EB] hover:bg-[#1D4ED8] text-white shadow-blue-600/25 cursor-pointer' : 'bg-slate-200 text-[#64748B] opacity-60 cursor-not-allowed'}" ${!isLoaded ? 'disabled' : ''}>
              <span>${isLoaded ? 'Xác Nhận & Mở Khóa Giai Đoạn 2: Làm Sạch Dữ Liệu' : 'Chờ Chọn Tệp Dữ Liệu Để Tiếp Tục'}</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>'''
text = text.replace(old_cta, new_cta)

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched tools/generate_navy_blue_app_js.py and generate_glass_app_js.py successfully!")

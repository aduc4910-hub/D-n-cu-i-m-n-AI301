import re
import os

print("=== BUILDING COMPLETE EXECUTIVE DASHBOARD V3 ===")

# Read current app.js
with open('ui/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

# 1. ADD currentActiveView STATE AND SIDEBAR SYNC LOGIC
if 'let currentActiveView =' not in app_code:
    # Insert near the top state variables
    app_code = app_code.replace(
        'let isDemoUnlocked = false;   // Chế độ demo khám phá nhanh',
        '''let isDemoUnlocked = false;   // Chế độ demo khám phá nhanh
let currentActiveView = "STAGE"; // "OVERVIEW" or "STAGE"'''
    )

# 2. ADD switchToOverview AND updateSidebarNav FUNCTIONS
overview_code = '''
// ================= ĐIỀU HƯỚNG TỔNG QUAN & SIDEBAR =================

function updateSidebarNav() {
  const overviewBtn = document.getElementById('nav-btn-overview');
  if (overviewBtn) {
    if (currentActiveView === 'OVERVIEW') {
      overviewBtn.className = "flex items-center gap-3 px-4 py-3 rounded-xl sidebar-tab-active transition w-full text-left";
    } else {
      overviewBtn.className = "flex items-center gap-3 px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left";
    }
  }

  for (let i = 0; i < 4; i++) {
    const stageBtn = document.getElementById(`nav-btn-stage-${i}`);
    if (stageBtn) {
      if (currentActiveView === 'STAGE' && currentStepIdx === i) {
        stageBtn.className = "flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-active transition w-full text-left";
      } else {
        stageBtn.className = "flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left";
      }
    }
  }
}

function switchToOverview() {
  currentActiveView = "OVERVIEW";
  updateSidebarNav();
  updateTopKPICards();
  renderCurrentWorkspace();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateTopKPICards() {
  const sizeEl = document.getElementById('kpi-value-data-size');
  const repEl = document.getElementById('kpi-value-reports-count');
  const timeEl = document.getElementById('kpi-value-proc-time');
  const accEl = document.getElementById('kpi-value-ai-accuracy');
  const trend1 = document.getElementById('kpi-trend-1');
  const trend2 = document.getElementById('kpi-trend-2');
  const trend3 = document.getElementById('kpi-trend-3');
  const trend4 = document.getElementById('kpi-trend-4');

  if (!currentSheetManifest || !currentSheetManifest.file_name) {
    if (sizeEl) sizeEl.textContent = "0 MB";
    if (repEl) repEl.textContent = "0";
    if (timeEl) timeEl.textContent = "0.0s";
    if (accEl) accEl.textContent = "0% (Chờ tệp)";
    if (trend1) trend1.textContent = "Chờ nạp";
    if (trend4) trend4.textContent = "Chờ nạp";
    return;
  }

  const rows = currentSheetManifest.row_count || 5200;
  if (sizeEl) sizeEl.textContent = (rows >= 1000) ? `${(rows * 0.0024).toFixed(1)} MB` : `${rows} dòng`;
  if (trend1) trend1.textContent = "↑ 12.5%";

  if (reportingStateStatus === "COMPLETED" || isDemoUnlocked) {
    if (repEl) repEl.textContent = "48+";
    if (trend2) trend2.textContent = "↑ 8.2%";
  } else if (currentStepIdx >= 2) {
    if (repEl) repEl.textContent = "4 báo cáo";
    if (trend2) trend2.textContent = "Ready";
  } else {
    if (repEl) repEl.textContent = "0";
  }

  if (cleaningStateStatus === "COMPLETED" || isDemoUnlocked) {
    if (timeEl) timeEl.textContent = "2.5 phút";
    if (trend3) trend3.textContent = "↓ 18.7%";
  } else {
    if (timeEl) timeEl.textContent = "1.2s";
    if (trend3) trend3.textContent = "Real-time";
  }

  if (cleaningStateStatus === "COMPLETED" || isDemoUnlocked) {
    const dq = currentCleaningManifest?.dq_score || 98.5;
    if (accEl) accEl.textContent = `${dq}%`;
    if (trend4) trend4.textContent = "↑ 0.3%";
  } else {
    if (accEl) accEl.textContent = "Chờ làm sạch";
    if (trend4) trend4.textContent = "Verify Gate";
  }
}

function renderExecutiveOverview() {
  return `
    <div class="space-y-6">
      <!-- ROW 1: CHARTS FROM IMAGE 5 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- CARD 1: HIỆU SUẤT KINH DOANH (2 COLS) -->
        <div class="lg:col-span-2 glass-card p-6 flex flex-col justify-between">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-xl bg-[#E8F2EE] flex items-center justify-center text-[#0D2B22]">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
              </div>
              <h3 class="text-base font-bold text-[#0A231A]">Hiệu suất kinh doanh</h3>
            </div>
            <!-- TIME RANGE SELECTOR -->
            <div class="flex items-center gap-1.5 p-1 rounded-xl bg-[#F5EFE6] border border-[#E2D9C8] text-xs font-semibold">
              <button class="px-3 py-1 rounded-lg text-[#4A635A] hover:text-[#0A231A]">7 ngày</button>
              <button class="px-3 py-1 rounded-lg bg-[#0A231A] text-white shadow-sm font-bold">30 ngày</button>
              <button class="px-3 py-1 rounded-lg text-[#4A635A] hover:text-[#0A231A]">90 ngày</button>
              <button class="px-3 py-1 rounded-lg text-[#4A635A] hover:text-[#0A231A]">1 năm</button>
            </div>
          </div>

          <!-- COMBO CHART (BARS + LINE) -->
          <div class="relative w-full h-64 my-2">
            <svg class="w-full h-full" viewBox="0 0 650 220" preserveAspectRatio="none">
              <!-- Grid lines -->
              <line x1="40" y1="20" x2="630" y2="20" stroke="#ECE4D8" stroke-dasharray="3,3"/>
              <line x1="40" y1="65" x2="630" y2="65" stroke="#ECE4D8" stroke-dasharray="3,3"/>
              <line x1="40" y1="110" x2="630" y2="110" stroke="#ECE4D8" stroke-dasharray="3,3"/>
              <line x1="40" y1="155" x2="630" y2="155" stroke="#ECE4D8" stroke-dasharray="3,3"/>
              <line x1="40" y1="195" x2="630" y2="195" stroke="#E2D9C8" stroke-width="1.2"/>

              <!-- Y-Axis Labels -->
              <text x="15" y="24" fill="#8FA99E" font-size="10" font-family="monospace">100</text>
              <text x="15" y="69" fill="#8FA99E" font-size="10" font-family="monospace">75</text>
              <text x="15" y="114" fill="#8FA99E" font-size="10" font-family="monospace">50</text>
              <text x="15" y="159" fill="#8FA99E" font-size="10" font-family="monospace">25</text>
              <text x="25" y="198" fill="#8FA99E" font-size="10" font-family="monospace">0</text>

              <!-- Deep Emerald Rounded Bars -->
              <rect x="70" y="80" width="16" height="115" rx="4" fill="#0D2B22"/>
              <rect x="100" y="60" width="16" height="135" rx="4" fill="#0D2B22"/>
              <rect x="130" y="55" width="16" height="140" rx="4" fill="#0D2B22"/>
              <rect x="160" y="90" width="16" height="105" rx="4" fill="#0D2B22"/>
              <rect x="190" y="70" width="16" height="125" rx="4" fill="#0D2B22"/>
              <rect x="220" y="50" width="16" height="145" rx="4" fill="#0D2B22"/>
              <rect x="250" y="65" width="16" height="130" rx="4" fill="#0D2B22"/>
              <rect x="280" y="85" width="16" height="110" rx="4" fill="#0D2B22"/>
              <rect x="310" y="60" width="16" height="135" rx="4" fill="#0D2B22"/>
              <rect x="340" y="45" width="16" height="150" rx="4" fill="#0D2B22"/>
              <rect x="370" y="75" width="16" height="120" rx="4" fill="#0D2B22"/>
              <rect x="400" y="55" width="16" height="140" rx="4" fill="#0D2B22"/>
              <rect x="430" y="50" width="16" height="145" rx="4" fill="#0D2B22"/>
              <rect x="460" y="65" width="16" height="130" rx="4" fill="#0D2B22"/>
              <rect x="490" y="40" width="16" height="155" rx="4" fill="#0D2B22"/>
              <rect x="520" y="50" width="16" height="145" rx="4" fill="#0D2B22"/>
              <rect x="550" y="70" width="16" height="125" rx="4" fill="#0D2B22"/>
              <rect x="580" y="45" width="16" height="150" rx="4" fill="#0D2B22"/>

              <!-- Champagne Gold Line with Data Dots -->
              <path d="M 78 120 Q 115 110, 145 105 T 205 115 T 265 95 T 325 110 T 385 100 T 445 115 T 505 90 T 588 85" fill="none" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="78" cy="120" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="145" cy="105" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="205" cy="115" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="265" cy="95" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="325" cy="110" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="385" cy="100" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="445" cy="115" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="505" cy="90" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>
              <circle cx="588" cy="85" r="4.5" fill="#FFFFFF" stroke="#D4B07B" stroke-width="2.5"/>

              <!-- X-Axis Labels -->
              <text x="75" y="215" fill="#8FA99E" font-size="10" font-family="monospace">01/04</text>
              <text x="215" y="215" fill="#8FA99E" font-size="10" font-family="monospace">08/04</text>
              <text x="355" y="215" fill="#8FA99E" font-size="10" font-family="monospace">15/04</text>
              <text x="495" y="215" fill="#8FA99E" font-size="10" font-family="monospace">22/04</text>
              <text x="575" y="215" fill="#8FA99E" font-size="10" font-family="monospace">30/04</text>
            </svg>
          </div>

          <!-- LEGEND -->
          <div class="flex items-center justify-center gap-6 pt-3 border-t border-[#ECE4D8] text-xs font-semibold">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-[#0D2B22]"></span>
              <span class="text-[#0A231A]">Doanh thu</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-[#D4B07B]"></span>
              <span class="text-[#0A231A]">Lợi nhuận</span>
            </div>
          </div>
        </div>

        <!-- CARD 2: PHÂN BỔ DỮ LIỆU (1 COL) -->
        <div class="glass-card p-6 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-[#0A231A]">Phân bổ dữ liệu</h3>
            <button onclick="goToStep(2)" class="text-xs font-bold text-[#4A635A] hover:text-[#0A231A] flex items-center gap-1 transition">
              <span>Xem chi tiết</span>
              <span>→</span>
            </button>
          </div>

          <!-- DONUT CHART -->
          <div class="flex flex-col sm:flex-row items-center justify-center gap-6 my-auto py-2">
            <!-- SVG Donut -->
            <div class="relative w-36 h-36 shrink-0 flex items-center justify-center">
              <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
                <!-- Track -->
                <circle cx="50" cy="50" r="38" fill="none" stroke="#F5EFE6" stroke-width="14"/>
                <!-- Segment 1: Kinh doanh (45.2%) -->
                <circle cx="50" cy="50" r="38" fill="none" stroke="#0D2B22" stroke-width="14" stroke-dasharray="108 239" stroke-dashoffset="0"/>
                <!-- Segment 2: Khách hàng (32.6%) -->
                <circle cx="50" cy="50" r="38" fill="none" stroke="#D4B07B" stroke-width="14" stroke-dasharray="78 239" stroke-dashoffset="-108"/>
                <!-- Segment 3: Sản phẩm (22.2%) -->
                <circle cx="50" cy="50" r="38" fill="none" stroke="#C8A870" stroke-width="14" stroke-dasharray="53 239" stroke-dashoffset="-186"/>
              </svg>
              <!-- Center Text -->
              <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span class="text-lg font-black text-[#0A231A]">100%</span>
                <span class="text-[9px] font-semibold text-[#8FA99E] uppercase tracking-wider">Tổng dữ liệu</span>
              </div>
            </div>

            <!-- Legend Tags -->
            <div class="space-y-3 text-xs w-full">
              <div class="flex items-center justify-between pb-2 border-b border-[#ECE4D8]">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#0D2B22]"></span>
                  <span class="font-semibold text-[#0A231A]">Kinh doanh</span>
                </div>
                <span class="font-bold text-[#0A231A]">45.2%</span>
              </div>
              <div class="flex items-center justify-between pb-2 border-b border-[#ECE4D8]">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#D4B07B]"></span>
                  <span class="font-semibold text-[#0A231A]">Khách hàng</span>
                </div>
                <span class="font-bold text-[#0A231A]">32.6%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#C8A870]"></span>
                  <span class="font-semibold text-[#0A231A]">Sản phẩm</span>
                </div>
                <span class="font-bold text-[#0A231A]">22.2%</span>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-[#ECE4D8] text-center">
            <button onclick="goToStep(0)" class="w-full py-2 px-3 rounded-xl bg-[#F5EFE6] hover:bg-[#EBD8B8] text-[#0A231A] font-bold text-xs transition">
              + Tải thêm tệp dữ liệu phân tích
            </button>
          </div>
        </div>

      </div>

      <!-- ROW 2: BOTTOM SECTION (HOẠT ĐỘNG GẦN ĐÂY & WORKFLOW LAUNCHER) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- LAUNCHER TO 4 STAGES (2 COLS) -->
        <div class="lg:col-span-2 glass-card p-6 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-[#0A231A]">Điều hướng nhanh quy trình 4 giai đoạn</h3>
            <span class="text-xs font-semibold text-[#4A635A]">Chuẩn MECE</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 my-2">
            <div onclick="goToStep(0)" class="p-4 rounded-xl border border-[#ECE4D8] hover:border-[#D4B07B] hover:shadow-md transition cursor-pointer bg-[#FAF7F2]/60 flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg bg-[#0A231A] text-white flex items-center justify-center font-bold text-xs shrink-0">1</div>
              <div>
                <div class="text-xs font-bold text-[#0A231A]">Tiếp nhận & Khảo sát</div>
                <div class="text-[11px] text-[#4A635A] mt-0.5">Tiếp nhận tệp dữ liệu và thiết lập bối cảnh phân tích</div>
              </div>
            </div>
            <div onclick="goToStep(1)" class="p-4 rounded-xl border border-[#ECE4D8] hover:border-[#D4B07B] hover:shadow-md transition cursor-pointer bg-[#FAF7F2]/60 flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg bg-[#0A231A] text-white flex items-center justify-center font-bold text-xs shrink-0">2</div>
              <div>
                <div class="text-xs font-bold text-[#0A231A]">Làm sạch & Chuẩn hóa</div>
                <div class="text-[11px] text-[#4A635A] mt-0.5">Khử trùng lặp, xử lý thiếu & Thẩm định DQ Score</div>
              </div>
            </div>
            <div onclick="goToStep(2)" class="p-4 rounded-xl border border-[#ECE4D8] hover:border-[#D4B07B] hover:shadow-md transition cursor-pointer bg-[#FAF7F2]/60 flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg bg-[#0A231A] text-white flex items-center justify-center font-bold text-xs shrink-0">3</div>
              <div>
                <div class="text-xs font-bold text-[#0A231A]">Phân tích & Insights</div>
                <div class="text-[11px] text-[#4A635A] mt-0.5">Cây chỉ số MECE, Pareto 80/20 & Xu hướng</div>
              </div>
            </div>
            <div onclick="goToStep(3)" class="p-4 rounded-xl border border-[#ECE4D8] hover:border-[#D4B07B] hover:shadow-md transition cursor-pointer bg-[#FAF7F2]/60 flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg bg-[#0A231A] text-white flex items-center justify-center font-bold text-xs shrink-0">4</div>
              <div>
                <div class="text-xs font-bold text-[#0A231A]">Báo cáo & Phân phối</div>
                <div class="text-[11px] text-[#4A635A] mt-0.5">Executive Dashboard, bộ lọc & Xuất tệp PDF/XLSX</div>
              </div>
            </div>
          </div>
          <div class="pt-4 border-t border-[#ECE4D8] flex items-center justify-between text-xs text-[#4A635A]">
            <span>Trạng thái hệ thống: Sẵn sàng</span>
            <button onclick="goToStep(0)" class="font-bold text-[#0A231A] hover:underline flex items-center gap-1">Vào không gian làm việc →</button>
          </div>
        </div>

        <!-- HOẠT ĐỘNG GẦN ĐÂY (1 COL) -->
        <div class="glass-card p-6 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-[#0A231A]">Hoạt động gần đây</h3>
            <button class="text-xs font-bold text-[#4A635A] hover:text-[#0A231A] transition">Xem tất cả →</button>
          </div>
          <div class="space-y-4 my-auto">
            <div class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#E8F2EE] text-[#10B981] flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
              </div>
              <div class="flex-1">
                <div class="text-xs font-bold text-[#0A231A]">Hoàn thành phân tích doanh thu quý I</div>
                <div class="text-[10px] text-[#8FA99E]">2 phút trước</div>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#F5EFE6] text-[#C8A870] flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <div class="flex-1">
                <div class="text-xs font-bold text-[#0A231A]">Đang xử lý báo cáo khách hàng</div>
                <div class="text-[10px] text-[#8FA99E]">5 phút trước</div>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#E8F2EE] text-[#0D2B22] flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7c0-2-1.5-3-3.5-3h-9C5.5 4 4 5 4 7z"></path></svg>
              </div>
              <div class="flex-1">
                <div class="text-xs font-bold text-[#0A231A]">Đã kết nối nguồn dữ liệu mới</div>
                <div class="text-[10px] text-[#8FA99E]">10 phút trước</div>
              </div>
            </div>
          </div>
          <div class="pt-4 border-t border-[#ECE4D8]">
            <div class="text-[11px] text-[#4A635A] text-center font-medium">Bảo mật dữ liệu nội bộ · Mã hóa 256-bit</div>
          </div>
        </div>

      </div>
    </div>
  `;
}
'''

# Check if overview_code is already in app_code, if not insert it right before renderHorizontalPipelineBar
if 'function renderExecutiveOverview()' not in app_code:
    app_code = app_code.replace(
        'function renderHorizontalPipelineBar() {',
        overview_code + '\nfunction renderHorizontalPipelineBar() {'
    )

# 3. UPDATE goToStep to switch to STAGE mode and update sidebar and top cards
app_code = re.sub(
    r'function goToStep\(idx\) \{.*?\n\}',
    '''function goToStep(idx) {
  const effectiveMax = isDemoUnlocked ? WORKFLOW_STEPS.length - 1 : maxUnlockedStepIdx;
  if (idx > effectiveMax) {
    alert("🔒 Giai đoạn này đang bị khóa!\\nBạn cần hoàn thành bước trước đó để mở khóa tiếp.");
    return;
  }
  currentActiveView = "STAGE";
  currentStepIdx = idx;
  updateSidebarNav();
  updateTopKPICards();
  renderHorizontalPipelineBar();
  renderCurrentWorkspace();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}''',
    app_code,
    flags=re.DOTALL
)

# 4. UPDATE advanceStep to also update top KPI cards and sidebar
app_code = re.sub(
    r'function advanceStep\(fromIdx\) \{.*?\n\}',
    '''function advanceStep(fromIdx) {
  if (fromIdx >= maxUnlockedStepIdx) {
    maxUnlockedStepIdx = Math.min(WORKFLOW_STEPS.length - 1, fromIdx + 1);
  }
  currentActiveView = "STAGE";
  currentStepIdx = Math.min(WORKFLOW_STEPS.length - 1, fromIdx + 1);
  updateSidebarNav();
  updateTopKPICards();
  renderHorizontalPipelineBar();
  renderCurrentWorkspace();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}''',
    app_code,
    flags=re.DOTALL
)

# 5. UPDATE renderCurrentWorkspace to handle currentActiveView === 'OVERVIEW'
app_code = re.sub(
    r'function renderCurrentWorkspace\(\) \{.*?\n  switch \(step\.id\) \{',
    '''function renderCurrentWorkspace() {
  const ws = document.getElementById('workspace-content');
  if (!ws) return;

  if (currentActiveView === 'OVERVIEW') {
    ws.innerHTML = renderExecutiveOverview();
    return;
  }

  const step = WORKFLOW_STEPS[currentStepIdx];
  let bodyHtml = "";
  switch (step.id) {''',
    app_code,
    flags=re.DOTALL
)

# 6. UPDATE initApp to call updateTopKPICards & updateSidebarNav
app_code = re.sub(
    r'function initApp\(\) \{.*?\n\}',
    '''function initApp() {
  const wf = window.SYSTEM_DATA?.workflow_state || {};
  if (wf.workflow_id) {
    const el = document.getElementById('footer-wf-id');
    if (el) el.textContent = wf.workflow_id;
  }

  currentSheetManifest = null;
  currentSelectedFile = null;
  currentSelectedSheet = null;
  sheetStateStatus = "PENDING";
  currentActiveView = "STAGE";
  updateTopSystemInfo(null);
  updateTopKPICards();
  updateSidebarNav();
  loadAvailableFilesOnly();
  renderHorizontalPipelineBar();
  renderCurrentWorkspace();
}''',
    app_code,
    flags=re.DOTALL
)

# 7. UPDATE inspectSheetFile to call updateTopKPICards
if 'updateTopKPICards();' not in app_code:
    app_code = app_code.replace(
        'updateTopSystemInfo(currentSheetManifest);',
        'updateTopSystemInfo(currentSheetManifest);\n      updateTopKPICards();'
    )

# 8. WRITE BACK ui/app.js
with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Generated ui/app.js with Executive Overview and Sidebar sync!")

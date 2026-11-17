import os
import re

print("=== STARTING APPLY PERFECT REFERENCE DESIGN ===")

# =========================================================================
# 1. GENERATE PERFECTED ui/index.html
# =========================================================================

index_html = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NexusBI · Executive Business Intelligence Platform</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* ================= NEXUSBI 4K LUXURY DESIGN SYSTEM ================= */
    :root {
      --canvas-ivory: #FAF7F2;
      --card-glass: rgba(255, 255, 255, 0.82);
      --card-border: rgba(226, 217, 200, 0.75);
      --emerald-sidebar: #082218;
      --emerald-dark: #0A261D;
      --emerald-primary: #0D2B22;
      --emerald-accent: #134232;
      --gold-champagne: #D4B07B;
      --gold-deep: #C8A870;
      --surface-cream: #F5EFE6;
      --text-primary: #0A261D;
      --text-muted: #4A635A;
      --text-body: #2C423B;
      --border-subtle: #E2D9C8;
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #FAF7F2; }
    ::-webkit-scrollbar-thumb { background: #D8CEBE; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #0A261D; }

    body {
      background-color: #FAF7F2;
      color: #0A261D;
      min-height: 100vh;
      overflow-x: hidden;
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* ================= FROSTED GLASS CARDS (Ô KÍNH MỜ TRONG SUỐT VỚI BLUR) ================= */
    .glass-card {
      position: relative;
      z-index: 1;
      background: rgba(255, 255, 255, 0.82) !important;
      backdrop-filter: blur(16px) saturate(160%) !important;
      -webkit-backdrop-filter: blur(16px) saturate(160%) !important;
      border: 1px solid rgba(226, 217, 200, 0.75) !important;
      box-shadow: 
        0 14px 35px -8px rgba(10, 35, 26, 0.06),
        0 2px 6px rgba(10, 35, 26, 0.02) !important;
      border-radius: 1.25rem !important;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .glass-card:hover {
      background: rgba(255, 255, 255, 0.90) !important;
      border-color: rgba(212, 176, 123, 0.45) !important;
      box-shadow: 
        0 18px 45px -10px rgba(10, 35, 26, 0.08),
        0 4px 12px rgba(10, 35, 26, 0.03) !important;
    }

    /* ================= FROSTED GLASS INPUTS (Ô NHẬP LIỆU KÍNH MỜ) ================= */
    .glass-input {
      background: rgba(255, 255, 255, 0.85) !important;
      backdrop-filter: blur(12px) saturate(150%) !important;
      -webkit-backdrop-filter: blur(12px) saturate(150%) !important;
      border: 1.5px solid rgba(226, 217, 200, 0.85) !important;
      box-shadow: 
        inset 0 1px 2px rgba(10, 35, 26, 0.02),
        0 1px 3px rgba(10, 35, 26, 0.02) !important;
      border-radius: 0.875rem !important;
      color: #0A261D !important;
      font-weight: 500 !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .glass-input:hover {
      background: rgba(255, 255, 255, 0.95) !important;
      border-color: #C8A870 !important;
      box-shadow: 0 4px 14px rgba(10, 35, 26, 0.05) !important;
    }
    .glass-input:focus, .glass-input:focus-within {
      background: #FFFFFF !important;
      border-color: #0A261D !important;
      box-shadow: 
        0 0 0 3px rgba(10, 35, 26, 0.10),
        0 6px 18px rgba(200, 168, 112, 0.18) !important;
      outline: none !important;
    }

    /* ================= FROSTED GLASS PILLS ================= */
    .glass-pill {
      background: rgba(255, 255, 255, 0.80) !important;
      backdrop-filter: blur(12px) !important;
      -webkit-backdrop-filter: blur(12px) !important;
      border: 1px solid rgba(226, 217, 200, 0.75) !important;
      box-shadow: 0 2px 6px rgba(10, 35, 26, 0.03) !important;
      color: #0A261D !important;
      transition: all 0.2s ease !important;
    }
    .glass-pill:hover {
      background: #F5EFE6 !important;
      border-color: #0A261D !important;
      color: #0A261D !important;
    }

    /* ================= SIDEBAR TABS ================= */
    .sidebar-tab-active {
      background: #EBD9C0 !important;
      color: #0A261D !important;
      font-weight: 700 !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15) !important;
    }
    .sidebar-tab-inactive {
      color: #8FA99E !important;
      font-weight: 500 !important;
    }
    .sidebar-tab-inactive:hover {
      color: #FFFFFF !important;
      background: #11382A !important;
    }
  </style>
  <script src="payload.js?v=12"></script>
  <script src="app.js?v=12"></script>
</head>
<body class="antialiased min-h-screen selection:bg-[#0A261D] selection:text-white flex">

  <!-- ================= LEFT SIDEBAR (EXECUTIVE DARK EMERALD #082218) ================= -->
  <aside class="hidden lg:flex w-64 flex-col justify-between bg-[#082218] text-[#FAF7F2] p-5 border-r border-[#123829] shrink-0 sticky top-0 h-screen z-20">
    <!-- TOP BRAND & NAVIGATION -->
    <div class="flex flex-col gap-6">
      <!-- BRAND LOGO -->
      <div class="flex items-center gap-3 px-2 pt-1 cursor-pointer" onclick="switchToOverview()">
        <div class="flex items-end gap-1 h-7">
          <div class="w-2 h-4 rounded-sm bg-[#D4B07B]"></div>
          <div class="w-2 h-6 rounded-sm bg-[#C8A870]"></div>
          <div class="w-2 h-7 rounded-sm bg-[#FAF7F2]"></div>
        </div>
        <div class="tracking-tight font-black text-2xl text-[#FAF7F2]">
          Nexus<span class="text-[#D4B07B]">BI</span>
        </div>
      </div>

      <!-- NAVIGATION MENU -->
      <nav class="flex flex-col gap-1.5 text-sm" id="sidebar-nav-container">
        <!-- TỔNG QUAN -->
        <button id="nav-btn-overview" onclick="switchToOverview()" class="flex items-center gap-3 px-4 py-3 rounded-xl sidebar-tab-active transition w-full text-left">
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          <span class="flex-1">Tổng quan</span>
        </button>

        <!-- DỮ LIỆU (STAGE 1) -->
        <button id="nav-btn-stage-0" onclick="goToStep(0)" class="flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7c0-2-1.5-3-3.5-3h-9C5.5 4 4 5 4 7zm0 5c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3M4 17c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3"></path></svg>
            <span>Dữ liệu</span>
          </div>
          <span class="text-xs opacity-60">›</span>
        </button>

        <!-- LÀM SẠCH (STAGE 2) -->
        <button id="nav-btn-stage-1" onclick="goToStep(1)" class="flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
            <span>Làm sạch</span>
          </div>
          <span class="text-xs opacity-60">›</span>
        </button>

        <!-- PHÂN TÍCH (STAGE 3) -->
        <button id="nav-btn-stage-2" onclick="goToStep(2)" class="flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <span>Phân tích</span>
          </div>
          <span class="text-xs opacity-60">›</span>
        </button>

        <!-- BÁO CÁO (STAGE 4) -->
        <button id="nav-btn-stage-3" onclick="goToStep(3)" class="flex items-center justify-between px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <span>Báo cáo</span>
          </div>
          <span class="text-xs opacity-60">›</span>
        </button>

        <!-- CÀI ĐẶT -->
        <button onclick="toggleDemoUnlock()" class="flex items-center gap-3 px-4 py-3 rounded-xl sidebar-tab-inactive transition w-full text-left mt-2">
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          <span class="flex-1">Cài đặt / Demo</span>
        </button>
      </nav>
    </div>

    <!-- BOTTOM CTA BANNER (WITH GOLD WAVE LINES) -->
    <div class="p-4 rounded-2xl bg-gradient-to-b from-[#11382A] to-[#082218] border border-[#1B4D3A] relative overflow-hidden shadow-lg">
      <div class="absolute -right-4 -bottom-6 w-24 h-24 rounded-full bg-[#D4B07B]/15 blur-xl"></div>
      <p class="text-xs font-semibold text-[#FAF7F2] leading-relaxed mb-3 relative z-10">
        Khám phá tiềm năng dữ liệu cùng NexusBI
      </p>
      <button onclick="goToStep(0)" class="w-full py-2 px-3 rounded-xl bg-gradient-to-r from-[#D4B07B] to-[#C8A870] hover:from-[#DFBE8A] hover:to-[#D4B07B] text-[#0A261D] font-bold text-xs flex items-center justify-center gap-1.5 shadow-md shadow-[#C8A870]/25 transition relative z-10">
        <span>Bắt đầu ngay</span>
        <span>→</span>
      </button>
    </div>
  </aside>

  <!-- ================= MAIN VIEW CANVAS ================= -->
  <div class="flex-1 flex flex-col min-w-0 relative bg-[#FAF7F2] min-h-screen">
    
    <!-- ================= CRISP 4K AMBIENT SILK RIBBON BACKDROP (NOT BLURRED!) ================= -->
    <div class="absolute top-0 right-0 w-[65vw] max-w-[950px] h-[480px] pointer-events-none overflow-hidden z-0 select-none hidden sm:block">
      <svg viewBox="0 0 950 480" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full object-cover">
        <defs>
          <linearGradient id="silkEmeraldMain" x1="0%" y1="0%" x2="100%" y2="80%">
            <stop offset="0%" stop-color="#061D14" stop-opacity="0.95"/>
            <stop offset="35%" stop-color="#0B2B20" stop-opacity="0.88"/>
            <stop offset="70%" stop-color="#144637" stop-opacity="0.65"/>
            <stop offset="100%" stop-color="#1D5C49" stop-opacity="0.0"/>
          </linearGradient>
          <radialGradient id="silkEmeraldAura" cx="80%" cy="10%" r="70%">
            <stop offset="0%" stop-color="#0E382A" stop-opacity="0.75"/>
            <stop offset="45%" stop-color="#154B3A" stop-opacity="0.4"/>
            <stop offset="85%" stop-color="#FAF7F2" stop-opacity="0"/>
          </radialGradient>
          <linearGradient id="goldThread1" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#C8A870" stop-opacity="0.1"/>
            <stop offset="30%" stop-color="#D4B07B" stop-opacity="0.9"/>
            <stop offset="70%" stop-color="#F2DEBE" stop-opacity="0.95"/>
            <stop offset="100%" stop-color="#D4B07B" stop-opacity="0.2"/>
          </linearGradient>
          <linearGradient id="goldThread2" x1="0%" y1="80%" x2="100%" y2="20%">
            <stop offset="0%" stop-color="#9E7D46" stop-opacity="0"/>
            <stop offset="40%" stop-color="#D4B07B" stop-opacity="0.75"/>
            <stop offset="80%" stop-color="#ECCF9E" stop-opacity="0.85"/>
            <stop offset="100%" stop-color="#C8A870" stop-opacity="0.1"/>
          </linearGradient>
        </defs>

        <!-- Ambient Silk Aura -->
        <rect x="0" y="0" width="950" height="480" fill="url(#silkEmeraldAura)"/>

        <!-- Flowing Emerald Silk Ribbons -->
        <path d="M 120,0 C 260,80 440,15 620,95 C 750,155 860,110 950,140 L 950,0 Z" fill="url(#silkEmeraldMain)"/>
        <path d="M 220,0 C 350,120 520,40 700,145 C 800,200 890,160 950,220 L 950,0 Z" fill="url(#silkEmeraldMain)" opacity="0.8"/>
        <path d="M 340,0 C 460,150 610,70 780,185 C 860,235 910,210 950,260 L 950,0 Z" fill="url(#silkEmeraldMain)" opacity="0.6"/>

        <!-- Flowing Golden Undulating Waves (Image 5 Reference) -->
        <path d="M 150,0 C 300,120 480,35 660,125 C 780,185 880,140 950,180" stroke="url(#goldThread1)" stroke-width="2.2" stroke-linecap="round" fill="none"/>
        <path d="M 190,0 C 330,135 510,50 690,140 C 805,198 895,155 950,200" stroke="url(#goldThread1)" stroke-width="1.8" stroke-linecap="round" fill="none"/>
        <path d="M 235,0 C 365,150 540,65 720,155 C 830,210 910,170 950,220" stroke="url(#goldThread2)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
        <path d="M 285,0 C 405,165 575,80 750,170 C 855,222 925,185 950,240" stroke="url(#goldThread2)" stroke-width="1.2" stroke-linecap="round" fill="none"/>
        <path d="M 340,0 C 450,180 610,95 780,185 C 880,235 935,200 950,260" stroke="url(#goldThread2)" stroke-width="1.0" stroke-linecap="round" fill="none"/>
        <path d="M 400,0 C 500,195 650,110 810,200 C 900,248 945,215 950,280" stroke="url(#goldThread2)" stroke-width="0.8" stroke-linecap="round" fill="none"/>
      </svg>
    </div>

    <!-- MAIN PADDED CONTAINER -->
    <div class="p-4 md:p-8 flex-1 flex flex-col max-w-7xl w-full mx-auto relative z-10">

      <!-- ================= TOP HEADER (GREETING & USER PROFILE) ================= -->
      <header class="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 mb-6 gap-4 border-b border-[#ECE4D8]">
        <div>
          <div class="text-xs md:text-sm text-[#4A635A] font-medium mb-1">Xin chào,</div>
          <h1 class="text-xl md:text-2xl lg:text-3xl font-black text-[#0A261D] tracking-tight">Khám phá giá trị từ dữ liệu</h1>
          <p class="text-xs md:text-sm text-[#4A635A] font-medium mt-1">NexusBI giúp bạn phân tích, trực quan hóa và đưa ra quyết định thông minh hơn.</p>
        </div>

        <div class="flex items-center gap-3 self-end sm:self-auto">
          <!-- QUICK TOGGLES -->
          <button onclick="toggleDemoUnlock()" id="btn-demo-toggle" title="Mở khóa khám phá nhanh" class="px-3.5 py-1.5 rounded-full glass-pill text-[#0A261D] flex items-center gap-1.5 font-bold text-xs transition hover:border-[#0A261D]">
            <svg class="w-3.5 h-3.5 text-[#C8A870]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            <span id="txt-demo-toggle">Demo xem nhanh</span>
          </button>

          <button onclick="resetWorkflowProgression()" title="Bắt đầu lại từ Bước 1" class="p-2 rounded-full glass-pill text-[#4A635A] hover:text-[#DC2626] transition hover:border-[#DC2626]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          </button>

          <!-- AI ASSISTANT -->
          <button onclick="openChatDrawer()" class="px-3.5 py-1.5 rounded-full bg-gradient-to-r from-[#D4B07B] to-[#C8A870] hover:from-[#DFBE8A] hover:to-[#D4B07B] text-[#0A261D] font-bold text-xs shadow-md shadow-[#C8A870]/25 flex items-center gap-1.5 transition">
            <svg class="w-3.5 h-3.5 text-[#0A261D]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Trợ Lý AI</span>
          </button>

          <!-- BELL NOTIFICATION -->
          <button class="relative p-2 rounded-full glass-pill text-[#4A635A] hover:text-[#0A261D]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            <span class="absolute top-1 right-1 w-2 h-2 rounded-full bg-[#EF4444] border-2 border-white"></span>
          </button>

          <!-- USER AVATAR -->
          <div class="flex items-center gap-2 pl-2">
            <div class="w-8 h-8 rounded-full bg-[#11382A] text-[#D4B07B] flex items-center justify-center font-bold text-xs border border-[#D4B07B]/40 shadow-sm">
              NT
            </div>
            <span class="text-xs font-bold text-[#0A261D] hidden md:block">Nguyễn Văn A</span>
            <svg class="w-3.5 h-3.5 text-[#4A635A] hidden md:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
      </header>

      <!-- ================= 4 TOP FROSTED GLASS KPI CARDS (ALL METRICS ZERO INITIALLY) ================= -->
      <section class="grid grid-cols-2 md:grid-cols-4 gap-3.5 md:gap-4 mb-6" id="top-kpi-cards-grid">
        <!-- CARD 1: TỔNG DỮ LIỆU -->
        <div class="glass-card p-4 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <div class="w-8 h-8 rounded-xl bg-[#E8F2EE] flex items-center justify-center text-[#0D2B22]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7c0-2-1.5-3-3.5-3h-9C5.5 4 4 5 4 7z"></path></svg>
            </div>
            <span id="kpi-trend-1" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E8F2EE] text-[#0D2B22]">Chờ nạp</span>
          </div>
          <div class="text-[11px] font-semibold text-[#4A635A]">Tổng dữ liệu</div>
          <div id="kpi-value-data-size" class="text-xl md:text-2xl font-black text-[#0A261D] tracking-tight mt-0.5">0 MB</div>
          <!-- Sparkline -->
          <div class="mt-2.5 h-5 w-full">
            <svg class="w-full h-full" viewBox="0 0 100 20" preserveAspectRatio="none">
              <path d="M0,15 Q25,8 50,13 T100,5" fill="none" stroke="#0D2B22" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
        </div>

        <!-- CARD 2: TỔNG BÁO CÁO -->
        <div class="glass-card p-4 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <div class="w-8 h-8 rounded-xl bg-[#F5EFE6] flex items-center justify-center text-[#C8A870]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <span id="kpi-trend-2" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#F5EFE6] text-[#C8A870]">Chuẩn Minto</span>
          </div>
          <div class="text-[11px] font-semibold text-[#4A635A]">Tổng báo cáo</div>
          <div id="kpi-value-reports-count" class="text-xl md:text-2xl font-black text-[#0A261D] tracking-tight mt-0.5">0</div>
          <!-- Sparkline -->
          <div class="mt-2.5 h-5 w-full">
            <svg class="w-full h-full" viewBox="0 0 100 20" preserveAspectRatio="none">
              <path d="M0,16 Q30,12 60,15 T100,6" fill="none" stroke="#C8A870" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
        </div>

        <!-- CARD 3: THỜI GIAN XỬ LÝ TB -->
        <div class="glass-card p-4 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <div class="w-8 h-8 rounded-xl bg-[#E8F2EE] flex items-center justify-center text-[#134232]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <span id="kpi-trend-3" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E8F2EE] text-[#134232]">Real-time</span>
          </div>
          <div class="text-[11px] font-semibold text-[#4A635A]">Thời gian xử lý TB</div>
          <div id="kpi-value-proc-time" class="text-xl md:text-2xl font-black text-[#0A261D] tracking-tight mt-0.5">0.0s</div>
          <!-- Sparkline -->
          <div class="mt-2.5 h-5 w-full">
            <svg class="w-full h-full" viewBox="0 0 100 20" preserveAspectRatio="none">
              <path d="M0,17 Q35,16 70,8 T100,7" fill="none" stroke="#134232" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
        </div>

        <!-- CARD 4: ĐỘ CHÍNH XÁC AI -->
        <div class="glass-card p-4 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <div class="w-8 h-8 rounded-xl bg-[#F5EFE6] flex items-center justify-center text-[#C8A870]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <span id="kpi-trend-4" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#F5EFE6] text-[#C8A870]">MECE 100%</span>
          </div>
          <div class="text-[11px] font-semibold text-[#4A635A]">Độ chính xác AI</div>
          <div id="kpi-value-ai-accuracy" class="text-xl md:text-2xl font-black text-[#0A261D] tracking-tight mt-0.5">0% (Chờ tệp)</div>
          <!-- Sparkline -->
          <div class="mt-2.5 h-5 w-full">
            <svg class="w-full h-full" viewBox="0 0 100 20" preserveAspectRatio="none">
              <path d="M0,15 Q30,6 60,11 T100,4" fill="none" stroke="#C8A870" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
        </div>
      </section>

      <!-- ================= 4-STAGE PIPELINE STEPPER ("QUY TRÌNH PHÂN TÍCH") ================= -->
      <section class="glass-card p-4 md:p-5 mb-6" id="pipeline-card-container">
        <div class="flex items-center justify-between pb-3 mb-3 border-b border-[#ECE4D8]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[#D4B07B]"></span>
            <h2 class="text-xs md:text-sm font-bold text-[#0A261D]">Quy trình phân tích 4 giai đoạn</h2>
          </div>
          <div class="flex items-center gap-2 text-xs">
            <span id="project-dataset-dot" class="w-2 h-2 rounded-full bg-[#A3B5AE]"></span>
            <span class="text-[11px] font-bold text-[#4A635A]" id="project-dataset-name">Chờ nạp nguồn dữ liệu (Số liệu về 0)</span>
          </div>
        </div>
        <div class="flex items-center justify-between" id="horizontal-pipeline-bar">
          <!-- Dynamically populated by app.js -->
        </div>
      </section>

      <!-- ================= MAIN WORKSPACE CANVAS (FROSTED GLASS DUAL-PANE) ================= -->
      <main id="workspace-content" class="flex-1 mb-6">
        <!-- Rendered dynamically by app.js -->
      </main>

      <!-- ================= FOOTER ================= -->
      <footer class="py-4 border-t border-[#ECE4D8] flex flex-col sm:flex-row items-center justify-between text-xs text-[#4A635A] gap-2 mt-auto">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-[#10B981]"></span>
          <span class="text-[#0A261D] font-semibold">Hệ thống bảo toàn dữ liệu gốc 100% · Kiểm chứng công thức toán học MECE</span>
        </div>
        <div class="flex items-center gap-3 font-mono text-[11px]">
          <span class="text-[#4A635A]">Kiến trúc: 4 Giai đoạn chuẩn</span>
          <span class="text-[#D8CEBE]">|</span>
          <span class="text-[#0A261D] font-bold" id="footer-wf-id">AI301 Final Project</span>
        </div>
      </footer>

    </div>
  </div>

  <!-- ================= AI ASSISTANT DIALOG ================= -->
  <dialog id="ai-chat-dialog" class="bg-transparent backdrop:bg-black/40 backdrop:backdrop-blur-sm p-0 m-auto rounded-3xl max-w-xl w-full border-0 shadow-2xl">
    <div class="glass-card p-6 shadow-2xl flex flex-col space-y-3.5 bg-white border border-[#ECE4D8]">
      <div class="flex items-center justify-between border-b border-[#ECE4D8] pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-[#0A261D] flex items-center justify-center font-bold text-[#D4B07B] text-xs shadow-sm border border-[#D4B07B]/40">AI</div>
          <div>
            <h3 class="text-sm font-bold text-[#0A261D]">Trợ Lý Phân Tích NexusBI</h3>
            <p class="text-[11px] text-[#4A635A]">Hỏi đáp số liệu kinh doanh & kiểm chứng công thức tức thời</p>
          </div>
        </div>
        <button onclick="closeChatDrawer()" class="text-[#4A635A] hover:text-[#0A261D] p-1 rounded-lg hover:bg-[#F5EFE6] transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div id="modal-chat-log" class="h-64 overflow-y-auto space-y-2 p-1 font-sans text-xs">
        <div class="p-3.5 rounded-2xl glass-input text-[#0A261D] mr-8">
          Xin chào! Tôi là Trợ lý Phân tích NexusBI. Bạn có thể hỏi về các chỉ số doanh thu, biên lợi nhuận, hiệu quả theo kênh bán, hoặc yêu cầu so sánh số liệu giữa các quý.
        </div>
      </div>

      <div class="flex items-center gap-2 pt-2 border-t border-[#ECE4D8]">
        <input type="text" id="modal-chat-input" placeholder="Ví dụ: Kênh nào có tỷ suất lợi nhuận cao nhất?" class="flex-1 px-4 py-2.5 text-xs rounded-xl glass-input text-[#0A261D] placeholder:text-[#7A8F87]" onkeydown="if(event.key==='Enter') sendModalChatMessage()">
        <button onclick="sendModalChatMessage()" class="px-4 py-2.5 bg-[#0A261D] hover:bg-[#133A2D] text-white border border-[#D4B07B]/40 rounded-xl text-xs font-bold shadow-sm transition">
          Gửi
        </button>
      </div>
    </div>
  </dialog>

</body>
</html>
'''

with open('ui/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Updated ui/index.html successfully!")

# =========================================================================
# 2. UPDATE ui/app.js: MAKE SURE renderHorizontalPipelineBar HAS THE EXACT ACTIVE STEP CARD
# =========================================================================

with open('ui/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Update renderHorizontalPipelineBar step badges
old_pipeline_fn = re.search(r'function renderHorizontalPipelineBar\(\) \{.*?\n\}', app_code, re.DOTALL)
if old_pipeline_fn:
    new_pipeline_fn = '''function renderHorizontalPipelineBar() {
  const container = document.getElementById('horizontal-pipeline-bar');
  if (!container) return;

  const effectiveMaxUnlocked = isDemoUnlocked ? WORKFLOW_STEPS.length - 1 : maxUnlockedStepIdx;

  let stepsHtml = WORKFLOW_STEPS.map((s, idx) => {
    const isCurrent = idx === currentStepIdx && currentActiveView === "STAGE";
    const isDone = idx < effectiveMaxUnlocked || (idx === effectiveMaxUnlocked && idx === WORKFLOW_STEPS.length - 1 && reportingStateStatus === "COMPLETED");
    const isLocked = idx > effectiveMaxUnlocked;

    let badgeClass = "flex items-center gap-2.5 px-4 py-2.5 rounded-2xl transition cursor-pointer ";
    let numBadge = "";

    if (isCurrent) {
      badgeClass += "bg-[#0A261D] text-white border border-[#D4B07B] shadow-lg shadow-[#0A261D]/25 ring-1 ring-[#D4B07B]/40";
      numBadge = `<span class="w-6 h-6 rounded-xl bg-[#D4B07B] text-[#0A261D] font-black text-xs flex items-center justify-center font-mono">0${s.num}</span>`;
    } else if (isDone) {
      badgeClass += "glass-pill hover:bg-[#F5EFE6] hover:border-[#D4B07B]/60 text-[#0A261D] shadow-sm";
      numBadge = `<span class="w-6 h-6 rounded-xl bg-[#0A261D] text-[#D4B07B] border border-[#D4B07B]/50 font-bold text-xs flex items-center justify-center">✓</span>`;
    } else {
      badgeClass += "text-[#4A635A] opacity-60 cursor-not-allowed";
      numBadge = `<span class="w-6 h-6 rounded-xl bg-[#F5EFE6] text-[#4A635A] font-bold text-xs flex items-center justify-center font-mono border border-[#E2D9C8]">0${s.num}</span>`;
    }

    return `
      <div class="flex items-center gap-2 flex-1 min-w-[210px]">
        <button onclick="goToStep(${idx})" class="${badgeClass} w-full text-left" ${isLocked ? 'disabled' : ''}>
          ${numBadge}
          <div class="truncate">
            <div class="text-xs font-bold leading-tight ${isCurrent ? 'text-white' : isDone ? 'text-[#0A261D]' : 'text-[#4A635A]'}">${s.title}</div>
            <div class="text-[10px] ${isCurrent ? 'text-[#D4B07B] font-medium' : 'text-[#4A635A]'} truncate">${s.subtitle}</div>
          </div>
        </button>
        ${idx < WORKFLOW_STEPS.length - 1 ? `<div class="hidden lg:block w-4 text-center text-slate-300 font-bold">→</div>` : ''}
      </div>
    `;
  }).join('');

  container.innerHTML = `
    <div class="w-full flex flex-col lg:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-2 w-full lg:w-auto overflow-x-auto pb-1 lg:pb-0 flex-1">
        ${stepsHtml}
      </div>
      <div class="shrink-0 flex items-center gap-2 pl-3 border-t lg:border-t-0 lg:border-l border-[#D4B07B]/30 pt-2 lg:pt-0 w-full lg:w-auto justify-between lg:justify-end">
        <span class="text-[11px] font-mono text-[#4A635A] font-medium">Verify Gate:</span>
        <span class="text-[11px] font-bold px-3 py-1 rounded-full glass-pill ${
          currentStepIdx === 0 ? 'text-[#0A261D] border-[#D4B07B]/40 bg-[#F5EFE6]' :
          currentStepIdx === 1 ? 'text-[#0D2B22] border-emerald-100 bg-emerald-50/60' :
          currentStepIdx === 2 ? 'text-[#0D2B22] border-emerald-100 bg-emerald-50/60' :
          'text-[#0D2B22] border-emerald-100 bg-emerald-50/60'
        }">
          ${currentStepIdx === 0 ? 'Sẵn sàng nạp' : currentStepIdx === 1 ? 'DQ 100/100' : currentStepIdx === 2 ? 'Đạt chuẩn 6/6' : 'Hoàn tất 100%'}
        </span>
      </div>
    </div>
  `;
}'''
    app_code = app_code.replace(old_pipeline_fn.group(0), new_pipeline_fn)
    print("Updated renderHorizontalPipelineBar with Image 5 style!")

# Write back app.js
with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("ui/app.js updated successfully!")

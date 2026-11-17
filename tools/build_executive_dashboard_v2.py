import re
import os

print("=== STARTING BUILD EXECUTIVE DASHBOARD V2 ===")

# 1. READ CURRENT ui/index.html & ui/app.js
with open('ui/index.html', 'r', encoding='utf-8') as f:
    html_src = f.read()

with open('ui/app.js', 'r', encoding='utf-8') as f:
    app_src = f.read()

# 2. CREATE ULTRA LUXURY ui/index.html MATCHING IMAGE 5
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
      --card-white: #FFFFFF;
      --card-border: #ECE4D8;
      --emerald-dark: #0A231A;
      --emerald-primary: #0D2B22;
      --emerald-accent: #134232;
      --gold-champagne: #D4B07B;
      --gold-deep: #C8A870;
      --surface-cream: #F5EFE6;
      --text-primary: #0A231A;
      --text-muted: #4A635A;
      --text-body: #2C423B;
      --border-subtle: #E2D9C8;
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #FAF7F2; }
    ::-webkit-scrollbar-thumb { background: #D8CEBE; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #0D2B22; }

    body {
      background-color: #FAF7F2;
      color: #0A231A;
      min-height: 100vh;
      overflow-x: hidden;
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 4K STUDIO SHADOWS & CRISP CARDS */
    .glass-card {
      position: relative;
      background: #FFFFFF !important;
      border: 1px solid #ECE4D8 !important;
      box-shadow: 
        0 10px 30px -5px rgba(10, 35, 26, 0.05),
        0 2px 6px rgba(10, 35, 26, 0.02) !important;
      border-radius: 1.25rem !important;
    }

    /* CRISP INPUTS */
    .glass-input {
      background: #FFFFFF !important;
      border: 1.5px solid #E2D9C8 !important;
      box-shadow: 
        inset 0 1px 2px rgba(10, 35, 26, 0.02),
        0 1px 3px rgba(10, 35, 26, 0.02) !important;
      border-radius: 0.875rem !important;
      color: #0A231A !important;
      font-weight: 500 !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .glass-input:hover {
      background: #FFFFFF !important;
      border-color: #C8A870 !important;
      box-shadow: 0 4px 12px rgba(10, 35, 26, 0.04) !important;
    }
    .glass-input:focus, .glass-input:focus-within {
      background: #FFFFFF !important;
      border-color: #0A231A !important;
      box-shadow: 
        0 0 0 3px rgba(10, 35, 26, 0.10),
        0 6px 18px rgba(200, 168, 112, 0.15) !important;
      outline: none !important;
    }

    /* CRISP PILLS */
    .glass-pill {
      background: #FFFFFF !important;
      border: 1px solid #E2D9C8 !important;
      box-shadow: 0 2px 6px rgba(10, 35, 26, 0.03) !important;
      color: #0A231A !important;
      transition: all 0.2s ease !important;
    }
    .glass-pill:hover {
      background: #F5EFE6 !important;
      border-color: #0A231A !important;
      color: #0A231A !important;
    }

    /* ACTIVE SIDEBAR TAB */
    .sidebar-tab-active {
      background: #EBD8B8 !important;
      color: #0A231A !important;
      font-weight: 700 !important;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
    }
    .sidebar-tab-inactive {
      color: #8FA99E !important;
      font-weight: 500 !important;
    }
    .sidebar-tab-inactive:hover {
      color: #FFFFFF !important;
      background: #133A2D !important;
    }
  </style>
  <script src="payload.js?v=11"></script>
  <script src="app.js?v=11"></script>
</head>
<body class="antialiased min-h-screen selection:bg-[#0A231A] selection:text-white flex">

  <!-- ================= LEFT SIDEBAR (EXECUTIVE DARK EMERALD) ================= -->
  <aside class="hidden lg:flex w-64 flex-col justify-between bg-[#0A231A] text-[#FAF7F2] p-5 border-r border-[#153D30] shrink-0 sticky top-0 h-screen z-20">
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

    <!-- BOTTOM CTA BANNER -->
    <div class="p-4 rounded-2xl bg-gradient-to-b from-[#133A2D] to-[#0A231A] border border-[#205240] relative overflow-hidden shadow-lg">
      <div class="absolute -right-4 -bottom-6 w-24 h-24 rounded-full bg-[#D4B07B]/10 blur-xl"></div>
      <p class="text-xs font-semibold text-[#FAF7F2] leading-relaxed mb-3 relative z-10">
        Khám phá tiềm năng dữ liệu cùng NexusBI
      </p>
      <button onclick="goToStep(0)" class="w-full py-2 px-3 rounded-xl bg-gradient-to-r from-[#D4B07B] to-[#C8A870] hover:from-[#DFBE8A] hover:to-[#D4B07B] text-[#0A231A] font-bold text-xs flex items-center justify-center gap-1.5 shadow-md shadow-[#C8A870]/20 transition relative z-10">
        <span>Bắt đầu ngay</span>
        <span>→</span>
      </button>
    </div>
  </aside>

  <!-- ================= MAIN VIEW CANVAS ================= -->
  <div class="flex-1 flex flex-col min-w-0 relative bg-[#FAF7F2] min-h-screen">
    
    <!-- TOP-RIGHT SILK WAVE BACKDROP (ORGANIC DEEP EMERALD & GOLD MESH) -->
    <div class="absolute top-0 right-0 w-[580px] h-[340px] pointer-events-none overflow-hidden z-0 opacity-90 hidden sm:block">
      <svg viewBox="0 0 580 340" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full object-cover">
        <defs>
          <linearGradient id="silkEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#08231A" stop-opacity="0.85"/>
            <stop offset="55%" stop-color="#144637" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#1E6550" stop-opacity="0.08"/>
          </linearGradient>
          <linearGradient id="silkGold" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#D4B07B" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#C8A870" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#FAF7F2" stop-opacity="0.05"/>
          </linearGradient>
          <filter id="silkBlur" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="30" result="blur"/>
          </filter>
        </defs>
        <path d="M220,0 C360,40 480,10 580,75 L580,0 Z" fill="url(#silkEmerald)" filter="url(#silkBlur)"/>
        <path d="M160,0 C300,105 420,30 580,150 L580,0 Z" fill="url(#silkEmerald)"/>
        <path d="M190,0 C330,135 440,45 580,170" stroke="url(#silkGold)" stroke-width="2.5" stroke-opacity="0.75" fill="none"/>
        <path d="M230,0 C360,145 470,65 580,195" stroke="url(#silkGold)" stroke-width="1.8" stroke-opacity="0.55" fill="none"/>
        <path d="M270,0 C400,155 500,85 580,225" stroke="url(#silkGold)" stroke-width="1.2" stroke-opacity="0.4" fill="none"/>
        <path d="M310,0 C430,165 530,105 580,255" stroke="url(#silkGold)" stroke-width="0.9" stroke-opacity="0.25" fill="none"/>
      </svg>
    </div>

    <!-- MAIN PADDED CONTAINER -->
    <div class="p-4 md:p-8 flex-1 flex flex-col max-w-7xl w-full mx-auto relative z-10">

      <!-- ================= TOP HEADER (GREETING & USER PROFILE) ================= -->
      <header class="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 mb-6 gap-4 border-b border-[#ECE4D8]">
        <div>
          <div class="text-xs md:text-sm text-[#4A635A] font-medium mb-1">Xin chào,</div>
          <h1 class="text-xl md:text-2xl lg:text-3xl font-black text-[#0A231A] tracking-tight">Khám phá giá trị từ dữ liệu</h1>
          <p class="text-xs md:text-sm text-[#4A635A] font-medium mt-1">NexusBI giúp bạn phân tích, trực quan hóa và đưa ra quyết định thông minh hơn.</p>
        </div>

        <div class="flex items-center gap-3 self-end sm:self-auto">
          <!-- QUICK TOGGLES -->
          <button onclick="toggleDemoUnlock()" id="btn-demo-toggle" title="Mở khóa khám phá nhanh" class="px-3.5 py-1.5 rounded-full glass-pill text-[#0A231A] flex items-center gap-1.5 font-bold text-xs transition hover:border-[#0A231A]">
            <svg class="w-3.5 h-3.5 text-[#C8A870]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            <span id="txt-demo-toggle">Demo xem nhanh</span>
          </button>

          <button onclick="resetWorkflowProgression()" title="Bắt đầu lại từ Bước 1" class="p-2 rounded-full glass-pill text-[#4A635A] hover:text-[#DC2626] transition hover:border-[#DC2626]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          </button>

          <!-- AI ASSISTANT -->
          <button onclick="openChatDrawer()" class="px-3.5 py-1.5 rounded-full bg-gradient-to-r from-[#D4B07B] to-[#C8A870] hover:from-[#DFBE8A] hover:to-[#D4B07B] text-[#0A231A] font-bold text-xs shadow-md shadow-[#C8A870]/25 flex items-center gap-1.5 transition">
            <svg class="w-3.5 h-3.5 text-[#0A231A]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Trợ Lý AI</span>
          </button>

          <!-- BELL NOTIFICATION -->
          <button class="relative p-2 rounded-full glass-pill text-[#4A635A] hover:text-[#0A231A]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            <span class="absolute top-1 right-1 w-2 h-2 rounded-full bg-[#EF4444] border-2 border-white"></span>
          </button>

          <!-- USER AVATAR -->
          <div class="flex items-center gap-2 pl-2">
            <div class="w-8 h-8 rounded-full bg-[#133A2D] text-[#D4B07B] flex items-center justify-center font-bold text-xs border border-[#D4B07B]/40 shadow-sm">
              NT
            </div>
            <span class="text-xs font-bold text-[#0A231A] hidden md:block">Nguyễn Văn A</span>
            <svg class="w-3.5 h-3.5 text-[#4A635A] hidden md:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
      </header>

      <!-- ================= 4 TOP KPI METRIC CARDS (ALL METRICS ZERO INITIALLY) ================= -->
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
          <div id="kpi-value-data-size" class="text-xl md:text-2xl font-black text-[#0A231A] tracking-tight mt-0.5">0 MB</div>
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
          <div id="kpi-value-reports-count" class="text-xl md:text-2xl font-black text-[#0A231A] tracking-tight mt-0.5">0</div>
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
          <div id="kpi-value-proc-time" class="text-xl md:text-2xl font-black text-[#0A231A] tracking-tight mt-0.5">0.0s</div>
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
          <div id="kpi-value-ai-accuracy" class="text-xl md:text-2xl font-black text-[#0A231A] tracking-tight mt-0.5">0% (Chờ tệp)</div>
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
            <h2 class="text-xs md:text-sm font-bold text-[#0A231A]">Quy trình phân tích 4 giai đoạn</h2>
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

      <!-- ================= MAIN WORKSPACE CANVAS ================= -->
      <main id="workspace-content" class="flex-1 mb-6">
        <!-- Rendered dynamically by app.js -->
      </main>

      <!-- ================= FOOTER ================= -->
      <footer class="py-4 border-t border-[#ECE4D8] flex flex-col sm:flex-row items-center justify-between text-xs text-[#4A635A] gap-2 mt-auto">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-[#10B981]"></span>
          <span class="text-[#0A231A] font-semibold">Hệ thống bảo toàn dữ liệu gốc 100% · Kiểm chứng công thức toán học MECE</span>
        </div>
        <div class="flex items-center gap-3 font-mono text-[11px]">
          <span class="text-[#4A635A]">Kiến trúc: 4 Giai đoạn chuẩn</span>
          <span class="text-[#D8CEBE]">|</span>
          <span class="text-[#0A231A] font-bold" id="footer-wf-id">AI301 Final Project</span>
        </div>
      </footer>

    </div>
  </div>

  <!-- ================= AI ASSISTANT DIALOG ================= -->
  <dialog id="ai-chat-dialog" class="bg-transparent backdrop:bg-black/40 backdrop:backdrop-blur-sm p-0 m-auto rounded-3xl max-w-xl w-full border-0 shadow-2xl">
    <div class="glass-card p-6 shadow-2xl flex flex-col space-y-3.5 bg-white border border-[#ECE4D8]">
      <div class="flex items-center justify-between border-b border-[#ECE4D8] pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-[#0A231A] flex items-center justify-center font-bold text-[#D4B07B] text-xs shadow-sm border border-[#D4B07B]/40">AI</div>
          <div>
            <h3 class="text-sm font-bold text-[#0A231A]">Trợ Lý Phân Tích NexusBI</h3>
            <p class="text-[11px] text-[#4A635A]">Hỏi đáp số liệu kinh doanh & kiểm chứng công thức tức thời</p>
          </div>
        </div>
        <button onclick="closeChatDrawer()" class="text-[#4A635A] hover:text-[#0A231A] p-1 rounded-lg hover:bg-[#F5EFE6] transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div id="modal-chat-log" class="h-64 overflow-y-auto space-y-2 p-1 font-sans text-xs">
        <div class="p-3.5 rounded-2xl glass-input text-[#0A231A] mr-8">
          Xin chào! Tôi là Trợ lý Phân tích NexusBI. Bạn có thể hỏi về các chỉ số doanh thu, biên lợi nhuận, hiệu quả theo kênh bán, hoặc yêu cầu so sánh số liệu giữa các quý.
        </div>
      </div>

      <div class="flex items-center gap-2 pt-2 border-t border-[#ECE4D8]">
        <input type="text" id="modal-chat-input" placeholder="Ví dụ: Kênh nào có tỷ suất lợi nhuận cao nhất?" class="flex-1 px-4 py-2.5 text-xs rounded-xl glass-input text-[#0A231A] placeholder:text-[#7A8F87]" onkeydown="if(event.key==='Enter') sendModalChatMessage()">
        <button onclick="sendModalChatMessage()" class="px-4 py-2.5 bg-[#0A231A] hover:bg-[#133A2D] text-white border border-[#D4B07B]/40 rounded-xl text-xs font-bold shadow-sm transition">
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
print("Updated ui/index.html with Executive Dark Emerald Sidebar and Canvas!")

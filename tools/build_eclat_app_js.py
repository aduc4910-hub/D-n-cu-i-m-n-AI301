import re

with open('ui/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Systematic replacement to transform to Haute Luxury Editorial (Eclat & Stone aesthetic):
# 1. Colors & Branding:
# Background: #F9F7F2 (Ivory Cream)
# Deep Emerald: #0E3326
# Champagne Gold: #BA9B6A
# Antique Gold Border: border-[#BA9B6A]/30
# Muted Text: text-[#6C7E77]
# Surface: #F5EFE4

# Buttons & Active Chips:
code = code.replace("bg-[#C6A15B] text-[#142D2A]", "bg-[#0E3326] text-[#F9F7F2] border border-[#BA9B6A]")
code = code.replace("bg-[#C6A15B]", "bg-[#0E3326]")
code = code.replace("hover:bg-[#D4AF6A]", "hover:bg-[#134232]")
code = code.replace("shadow-[#C6A15B]/25", "shadow-[#0E3326]/20")
code = code.replace("shadow-[#C6A15B]/20", "shadow-[#0E3326]/15")

# Text replacements:
code = code.replace("text-[#F8F3E8]", "text-[#0E3326]")
code = code.replace("text-[#A3B8B5]", "text-[#6C7E77]")
code = code.replace("text-[#C6A15B]", "text-[#0E3326]")
code = code.replace("text-[#142D2A]", "text-[#0E3326]")

# Borders & Dividers:
code = code.replace("border-[#D8C6A5]/20", "border-[#BA9B6A]/30")
code = code.replace("border-[#D8C6A5]/30", "border-[#BA9B6A]/35")
code = code.replace("border-[#D8C6A5]/35", "border-[#BA9B6A]/40")
code = code.replace("border-[#D8C6A5]/10", "border-[#BA9B6A]/20")
code = code.replace("border-[#D8C6A5]/40", "border-[#BA9B6A]/40")
code = code.replace("border-[#D8C6A5]/15", "border-[#BA9B6A]/25")
code = code.replace("divide-[#D8C6A5]/10", "divide-[#BA9B6A]/15")

# Surfaces & Containers:
code = code.replace("bg-[#1D5C52]/40", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]/30", "bg-[#F5EFE4]/70")
code = code.replace("bg-[#1D5C52]/50", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]/60", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]/70", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]/80", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]/25", "bg-[#F5EFE4]")
code = code.replace("bg-[#1D5C52]", "bg-[#F5EFE4]")
code = code.replace("bg-[#142D2A]/60", "bg-white/80")
code = code.replace("bg-[#142D2A]/80", "bg-white/90")
code = code.replace("bg-[#142D2A]/90", "bg-white/95")
code = code.replace("bg-[#142D2A]/95", "bg-white/95")
code = code.replace("from-[#142D2A]", "from-[#F5EFE4]")
code = code.replace("to-[#142D2A]", "to-[#F5EFE4]")
code = code.replace("hover:bg-[#1D5C52]/50 hover:border-[#C6A15B]/50", "hover:bg-white hover:border-[#0E3326]")

# In Stepper:
code = code.replace("numBadge = `<span class=\"w-6 h-6 rounded-xl bg-[#0E3326]/20 text-[#0E3326] font-bold text-xs flex items-center justify-center font-mono\">0${s.num}</span>`;",
                    "numBadge = `<span class=\"w-6 h-6 rounded-xl bg-[#BA9B6A] text-[#0E3326] font-bold text-xs flex items-center justify-center font-mono\">0${s.num}</span>`;")
code = code.replace("numBadge = `<span class=\"w-6 h-6 rounded-xl bg-[#34D399] text-white font-bold text-xs flex items-center justify-center\">✓</span>`;",
                    "numBadge = `<span class=\"w-6 h-6 rounded-xl bg-[#0E3326] text-[#BA9B6A] border border-[#BA9B6A]/50 font-bold text-xs flex items-center justify-center\">✓</span>`;")
code = code.replace("text-[#0E3326]/80 font-medium", "text-[#BA9B6A]")

# Channel chart & Quarterly trend:
code = code.replace("from-[#0E3326] to-[#D8C6A5]", "from-[#0E3326] via-[#134232] to-[#BA9B6A]")
code = code.replace("bg-[#D8C6A5]/70", "bg-[#BA9B6A]")
code = code.replace("hover:bg-[#D8C6A5]", "hover:bg-[#8C6D3B]")

# Checkmark in files and active chips:
code = code.replace("${isSel ? '<span class=\"text-white font-bold\">✓</span>' : ''}",
                    "${isSel ? '<span class=\"text-[#BA9B6A] font-bold\">✓</span>' : ''}")

# Titles formatting with editorial class:
code = code.replace("<h2 class=\"font-bold text-[#0E3326] text-sm\">",
                    "<h2 class=\"font-editorial font-bold text-[#0E3326] text-base md:text-lg tracking-wide\">")
code = code.replace("<h2 class=\"font-bold text-[#0E3326] text-xs\">",
                    "<h2 class=\"font-editorial font-bold text-[#0E3326] text-sm md:text-base tracking-wide\">")
code = code.replace("<h3 class=\"font-bold text-[#0E3326] text-sm\">",
                    "<h3 class=\"font-editorial font-bold text-[#0E3326] text-base tracking-wide\">")
code = code.replace("<h2 class=\"font-bold text-[#0E3326] text-base\">",
                    "<h2 class=\"font-editorial font-bold text-[#0E3326] text-lg md:text-xl tracking-wide\">")

# KPI Numbers formatting:
code = code.replace("text-xl md:text-2xl font-black text-[#0E3326] mt-1",
                    "font-editorial text-2xl md:text-3xl font-bold text-[#0E3326] mt-1")
code = code.replace("text-xl md:text-2xl font-black text-[#8C6D3B] mt-1",
                    "font-editorial text-2xl md:text-3xl font-bold text-[#8C6D3B] mt-1")

# Cleaned rules checkmarks:
code = code.replace("text-[#34D399]", "text-[#BA9B6A]")
code = code.replace("border-[#34D399]/40", "border-[#BA9B6A]/40")
code = code.replace("border-[#34D399]/30", "border-[#BA9B6A]/30")

# Write to ui/app.js
with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

# Synchronize generator scripts
generator_template = "import os\n\ncode = " + repr(code) + "\n\nwith open('ui/app.js', 'w', encoding='utf-8') as f:\n    f.write(code)\n\nprint('Generated Eclat & Stone Haute Luxury ui/app.js successfully!')\n"

with open('tools/generate_luxury_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

print("Generated Haute Luxury Editorial design for ui/app.js successfully!")

import re

with open('ui/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Systematic replacement to transform to Luxury Modern:
# 1. Active / Primary buttons & chips:
# bg-[#2563EB] text-white -> bg-[#C6A15B] text-[#142D2A]
code = code.replace("bg-[#2563EB] text-white", "bg-[#C6A15B] text-[#142D2A]")
code = code.replace("hover:bg-[#1D4ED8]", "hover:bg-[#D4AF6A]")
code = code.replace("shadow-blue-600/25", "shadow-[#C6A15B]/25")
code = code.replace("shadow-blue-600/20", "shadow-[#C6A15B]/20")

# 2. Primary text / Headings / Subtitles:
# text-[#0B1F3A] -> text-[#F8F3E8]
code = code.replace("text-[#0B1F3A]", "text-[#F8F3E8]")
# text-[#172B4D] -> text-[#F8F3E8]
code = code.replace("text-[#172B4D]", "text-[#F8F3E8]")
# text-[#64748B] -> text-[#A3B8B5]
code = code.replace("text-[#64748B]", "text-[#A3B8B5]")

# 3. Highlights in text:
# text-[#2563EB] -> text-[#C6A15B]
code = code.replace("text-[#2563EB]", "text-[#C6A15B]")
code = code.replace("bg-[#2563EB]", "bg-[#C6A15B]")

# 4. Borders & Dividers:
# border-[#E2E8F0] -> border-[#D8C6A5]/20
code = code.replace("border-[#E2E8F0]", "border-[#D8C6A5]/20")
code = code.replace("divide-[#E2E8F0]", "divide-[#D8C6A5]/10")
code = code.replace("border-[#BFDBFE]", "border-[#D8C6A5]/35")

# 5. Surfaces / Backgrounds:
# bg-[#F3F7FC] -> bg-[#1D5C52]/40
code = code.replace("bg-[#F3F7FC]/80", "bg-[#1D5C52]/30")
code = code.replace("bg-[#F3F7FC]", "bg-[#1D5C52]/40")
code = code.replace("from-[#F3F7FC]", "from-[#142D2A]")

# 6. Table styling adjustments:
code = code.replace("bg-white/70", "bg-[#142D2A]/60")
code = code.replace("bg-white/60", "bg-[#142D2A]/60")
code = code.replace("bg-white/80", "bg-[#142D2A]/80")
code = code.replace("bg-white/90", "bg-[#142D2A]/90")
code = code.replace("hover:bg-white", "hover:bg-[#1D5C52]/50 hover:border-[#C6A15B]/50")

# 7. Channel chart gradient & quarterly bars:
code = code.replace("from-[#2563EB] to-[#38BDF8]", "from-[#C6A15B] to-[#D8C6A5]")
code = code.replace("bg-[#BFDBFE]", "bg-[#1D5C52]/50")
code = code.replace("hover:bg-[#93C5FD]", "hover:bg-[#1D5C52]/80")
code = code.replace("bg-[#93C5FD]", "bg-[#1D5C52]/80")
code = code.replace("hover:bg-[#60A5FA]", "hover:bg-[#1D5C52]")
code = code.replace("bg-[#60A5FA]", "bg-[#D8C6A5]/70")
code = code.replace("hover:bg-[#3B82F6]", "hover:bg-[#D4AF6A]")

# 8. Success / Verify Gate styling:
code = code.replace("bg-emerald-50/50", "bg-[#1D5C52]/50")
code = code.replace("bg-emerald-50/70", "bg-[#1D5C52]/60")
code = code.replace("bg-emerald-50/80", "bg-[#1D5C52]/60")
code = code.replace("bg-emerald-100/80", "bg-[#1D5C52]/80")
code = code.replace("border-emerald-200/60", "border-[#34D399]/30")
code = code.replace("border-emerald-200/80", "border-[#34D399]/40")
code = code.replace("border-emerald-200", "border-[#34D399]/40")
code = code.replace("text-emerald-700", "text-[#34D399]")
code = code.replace("text-emerald-600", "text-[#34D399]")
code = code.replace("bg-emerald-500", "bg-[#34D399]")
code = code.replace("bg-emerald-600", "bg-[#34D399]")
code = code.replace("text-emerald-950", "text-[#F8F3E8]")

# 9. Disabled buttons styling:
code = code.replace("bg-slate-200 text-[#A3B8B5] opacity-60 cursor-not-allowed", "bg-[#1D5C52]/25 text-[#A3B8B5]/40 opacity-50 cursor-not-allowed border border-[#D8C6A5]/10")
code = code.replace("bg-slate-200 text-[#A3B8B5] cursor-not-allowed", "bg-[#1D5C52]/25 text-[#A3B8B5]/40 opacity-50 cursor-not-allowed border border-[#D8C6A5]/10")

# 10. Specific elements:
# In Stepper:
code = code.replace("numBadge = `<span class=\"w-6 h-6 rounded-xl bg-white/20 text-white font-bold text-xs flex items-center justify-center font-mono\">0${s.num}</span>`;",
                    "numBadge = `<span class=\"w-6 h-6 rounded-xl bg-[#142D2A]/20 text-[#142D2A] font-bold text-xs flex items-center justify-center font-mono\">0${s.num}</span>`;")
code = code.replace("text-blue-100", "text-[#142D2A]/80 font-medium")

# In Step 2 DQ Score card:
code = code.replace("bg-gradient-to-tr from-[#142D2A] via-[#142D2A]/80 to-blue-50/50", "bg-gradient-to-tr from-[#142D2A] via-[#1D5C52]/40 to-[#142D2A]")
code = code.replace("to-blue-50/70", "to-[#142D2A]")

# In Step 4 Completed Banner:
code = code.replace("bg-gradient-to-r from-blue-50/80 via-[#142D2A]/90 to-sky-50/80", "bg-gradient-to-r from-[#142D2A] via-[#1D5C52]/50 to-[#142D2A]")

# Write to ui/app.js
with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

# Also update the generators
generator_template = "import os\n\ncode = " + repr(code) + "\n\nwith open('ui/app.js', 'w', encoding='utf-8') as f:\n    f.write(code)\n\nprint('Generated Luxury Modern ui/app.js successfully!')\n"

with open('tools/generate_luxury_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

print("Generated Luxury Modern design for ui/app.js and generators successfully!")

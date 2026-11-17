import re

with open('ui/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any lingering font-editorial with standard modern bold typography for crisp readability
code = code.replace("font-editorial font-bold text-[#0E3326] text-base md:text-lg tracking-wide", "font-bold text-[#0D2B22] text-sm md:text-base")
code = code.replace("font-editorial font-bold text-[#0E3326] text-sm md:text-base tracking-wide", "font-bold text-[#0D2B22] text-xs md:text-sm")
code = code.replace("font-editorial font-bold text-[#0E3326] text-base tracking-wide", "font-bold text-[#0D2B22] text-xs md:text-sm")
code = code.replace("font-editorial font-bold text-[#0E3326] text-lg md:text-xl tracking-wide", "font-bold text-[#0D2B22] text-base")
code = code.replace("font-editorial text-2xl md:text-3xl font-bold text-[#0E3326] mt-1", "text-xl md:text-2xl font-black text-[#0D2B22] mt-1")
code = code.replace("font-editorial text-2xl md:text-3xl font-bold text-[#8C6D3B] mt-1", "text-xl md:text-2xl font-black text-[#8C6D3B] mt-1")
code = code.replace("font-editorial", "")

# Systematic Color Palette mapping:
# 1. Primary Text / Deep Emerald: #0D2B22
code = code.replace("text-[#0E3326]", "text-[#0D2B22]")
code = code.replace("bg-[#0E3326]", "bg-[#0D2B22]")
code = code.replace("hover:bg-[#134232]", "hover:bg-[#164335]")
code = code.replace("border-[#0E3326]", "border-[#0D2B22]")

# 2. Muted Text: #4A635A (crisp and clearly readable)
code = code.replace("text-[#6C7E77]", "text-[#4A635A]")

# 3. Gold Accent: #D4B07B & #C8A870
code = code.replace("text-[#BA9B6A]", "text-[#D4B07B]")
code = code.replace("bg-[#BA9B6A]", "bg-[#D4B07B]")
code = code.replace("border-[#BA9B6A]", "border-[#D4B07B]")

# 4. Borders: #ECE4D8 & #E2D9C8
code = code.replace("border-[#BA9B6A]/30", "border-[#ECE4D8]")
code = code.replace("border-[#BA9B6A]/35", "border-[#E2D9C8]")
code = code.replace("border-[#BA9B6A]/40", "border-[#E2D9C8]")
code = code.replace("border-[#BA9B6A]/50", "border-[#D4B07B]/50")
code = code.replace("border-[#BA9B6A]/20", "border-[#E2D9C8]")
code = code.replace("border-[#BA9B6A]/25", "border-[#ECE4D8]")
code = code.replace("divide-[#BA9B6A]/15", "divide-[#ECE4D8]")

# 5. Stepper refinement to match Image 2:
# Inactive step button:
old_stepper_inactive = 'badgeClass += "text-[#4A635A]/50 opacity-60 cursor-not-allowed";'
new_stepper_inactive = 'badgeClass += "text-[#4A635A] opacity-75 cursor-not-allowed";'
code = code.replace(old_stepper_inactive, new_stepper_inactive)

old_inactive_badge = 'numBadge = `<span class="w-6 h-6 rounded-xl glass-input text-[#4A635A] font-bold text-xs flex items-center justify-center font-mono">0${s.num}</span>`;'
new_inactive_badge = 'numBadge = `<span class="w-6 h-6 rounded-xl bg-[#F5EFE6] text-[#4A635A] font-bold text-xs flex items-center justify-center font-mono border border-[#E2D9C8]">0${s.num}</span>`;'
code = code.replace(old_inactive_badge, new_inactive_badge)

# Inactive step titles should be readable:
code = code.replace("isDone ? 'text-[#0D2B22]' : 'text-[#4A635A]'", "isDone ? 'text-[#0D2B22]' : 'text-[#4A635A]'")

# Active step subtitle in stepper:
code = code.replace("${isCurrent ? 'text-[#D4B07B]' : 'text-[#4A635A]'}", "${isCurrent ? 'text-[#D4B07B] font-medium' : 'text-[#4A635A]'}")

# Stepper arrow:
code = code.replace("text-[#D4B07B]/50 font-bold", "text-[#C8A870] font-bold")

# 6. File chips in Step 1:
# Inactive:
old_chip = "glass-pill hover:bg-white text-[#0D2B22]"
new_chip = "bg-white hover:bg-[#F5EFE6] text-[#0D2B22] border border-[#E2D9C8] shadow-sm font-semibold"
code = code.replace(old_chip, new_chip)

# Selected chip:
old_sel_chip = "bg-[#0D2B22] text-[#F9F7F2] border border-[#D4B07B]"
new_sel_chip = "bg-[#0D2B22] text-white border border-[#D4B07B] shadow-md shadow-[#0D2B22]/20"
code = code.replace(old_sel_chip, new_sel_chip)

# 7. Metric badges in Step 1:
code = code.replace("glass-input text-xs", "bg-[#F5EFE6]/70 border border-[#E2D9C8] p-3 rounded-2xl text-xs")

# 8. Tables:
code = code.replace("bg-white/80 backdrop-blur-md", "bg-white")
code = code.replace("bg-white/90", "bg-white")
code = code.replace("bg-white/95", "bg-white")
code = code.replace("hover:bg-[#F5EFE4]/60", "hover:bg-[#F5EFE6]/70")
code = code.replace("hover:bg-[#F5EFE4]/70", "hover:bg-[#F5EFE6]/70")
code = code.replace("divide-[#ECE4D8]", "divide-[#ECE4D8]")

# 9. Cards in Step 3 & Step 4:
code = code.replace("bg-gradient-to-tr from-[#F5EFE4] via-white to-[#F5EFE4]", "bg-[#F5EFE6]")
code = code.replace("bg-gradient-to-r from-[#F5EFE4] via-white to-[#F5EFE4]", "bg-[#F5EFE6]")

# Write back to ui/app.js
with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

# Synchronize generator scripts
generator_template = "import os\n\ncode = " + repr(code) + "\n\nwith open('ui/app.js', 'w', encoding='utf-8') as f:\n    f.write(code)\n\nprint('Generated Reference Dashboard ui/app.js successfully!')\n"

with open('tools/generate_luxury_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

print("Applied Image 2 Executive Dashboard color system to ui/app.js successfully!")

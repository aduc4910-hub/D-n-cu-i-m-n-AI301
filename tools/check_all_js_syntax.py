import json

with open('ui/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's fix line 525-526 first
old_str = 'alert("🔒 Giai đoạn này đang bị khóa!\nBạn cần hoàn thành bước trước đó để mở khóa tiếp.");'
new_str = 'alert("🔒 Giai đoạn này đang bị khóa!\\nBạn cần hoàn thành bước trước đó để mở khóa tiếp.");'

if old_str in content:
    content = content.replace(old_str, new_str)
    print("Fixed alert string in app.js!")

with open('ui/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Now let's test node or check with a python JS tokenizer or parser
lines = content.split('\n')
for i, line in enumerate(lines):
    # Check if double quote is unclosed on non-template lines
    # simple check: if line contains alert( or starts with string that has unescaped newline
    if 'alert(' in line and not line.strip().endswith(');'):
        print(f"Warning on line {i+1}: {line}")

print("Syntax check completed. Total lines:", len(lines))

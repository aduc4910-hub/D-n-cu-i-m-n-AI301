with open('ui/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect all lines around line 420
lines = text.splitlines()
for i in range(415, 426):
    print(f"{i+1}: {lines[i]}")

with open('ui/app.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

generator_template = "import os\n\ncode = " + repr(js_code) + "\n\nwith open('ui/app.js', 'w', encoding='utf-8') as f:\n    f.write(code)\n\nprint('Generated Frosted Glass UI ui/app.js successfully!')\n"

with open('tools/generate_navy_blue_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

with open('tools/generate_glass_app_js.py', 'w', encoding='utf-8') as f:
    f.write(generator_template)

print('Synchronized generators with current ui/app.js.')

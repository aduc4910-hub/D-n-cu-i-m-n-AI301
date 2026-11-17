import os, re, base64, shutil

def build_artifact():
    with open('ui/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    with open('ui/payload.js', 'r', encoding='utf-8') as f:
        payload = f.read()
    with open('ui/app.js', 'r', encoding='utf-8') as f:
        app = f.read()
    
    inline = f"<script>\n{payload}\n\n{app}\n</script>"
    
    # Replace any payload.js and app.js script tags
    out = re.sub(r'<script src="payload\.js.*?"></script>', '', html)
    out = re.sub(r'<script src="app\.js.*?"></script>', inline, out)
    
    # Inline brand_header_banner.png as base64
    banner_path = 'ui/brand_header_banner.png'
    if os.path.exists(banner_path):
        with open(banner_path, 'rb') as f:
            b64_banner = base64.b64encode(f.read()).decode('ascii')
        out = re.sub(r'src="brand_header_banner\.png.*?"', f'src="data:image/png;base64,{b64_banner}"', out)
        
        # Also copy to artifact directory
        artifact_dir = r"C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630"
        shutil.copyfile(banner_path, os.path.join(artifact_dir, 'brand_header_banner.png'))
    
    out_path = r"C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630\bi_platform_ui.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print("Updated standalone artifact at:", out_path, "Size:", len(out))

if __name__ == "__main__":
    build_artifact()

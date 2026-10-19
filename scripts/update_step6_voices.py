import re, os, time, urllib.request, urllib.parse

def download(text, lang, path):
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={urllib.parse.quote(text)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        with open(path, 'wb') as f:
            f.write(data)
        print(f"Updated {path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {path}: {e}")

with open('src/components/assemblyData.js', 'r', encoding='utf-8') as f:
    text = f.read()

for mod_name, array_name in [('brake', 'ASSEMBLY_STEPS'), ('clutch', 'CLUTCH_ASSEMBLY_STEPS'), ('car', 'FULL_CAR_ASSEMBLY_STEPS'), ('knuckle', 'KNUCKLE_JOINT_STEPS')]:
    m = re.search(r'export const ' + array_name + r'\s*=\s*\[([\s\S]*?)\];', text)
    if not m: continue
    step_blocks = re.findall(r'\{\s*id:\s*(\d+)[\s\S]*?translations:\s*\{([\s\S]*?)\}[\s\S]*?\}', m.group(1))
    for s_id, t_block in step_blocks:
        if s_id == '6':
            for lang in ['en', 'ta', 'ml', 'hi']:
                tm = re.search(rf"{lang}:\s*'([^']+)'", t_block)
                if tm:
                    t_text = tm.group(1)
                    p = f"public/audio/voices/{mod_name}_6_{lang}.mp3"
                    download(t_text, lang, p)
                    time.sleep(0.15)

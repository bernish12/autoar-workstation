import re, os, urllib.request, urllib.parse

with open('src/components/assemblyData.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const ASSEMBLY_STEPS\s*=\s*\[([\s\S]*?)\];', text)
steps = re.findall(r'\{\s*id:\s*(\d+)[\s\S]*?translations:\s*\{([\s\S]*?)\}[\s\S]*?\}', m.group(1))
for s_id, trans in steps:
    en = re.search(r"en:\s*'([^']+)'", trans)
    print(f"Step {s_id}:", en.group(1) if en else 'NONE')

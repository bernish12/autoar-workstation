import re
import os
import time
import urllib.request
import urllib.parse

def clean_and_download(text, lang, output_path):
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        print(f"Already exists: {output_path}")
        return True
    
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={urllib.parse.quote(text)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 500:
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    print(f"Downloaded ({len(data)} bytes): {output_path}")
                    time.sleep(0.15) # avoid rate limit
                    return True
        except Exception as e:
            print(f"Retry {attempt} for {output_path}: {e}")
            time.sleep(1)
    return False

def main():
    target_dir = os.path.join('public', 'audio', 'voices')
    os.makedirs(target_dir, exist_ok=True)
    
    with open('src/components/assemblyData.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find module arrays
    modules = {
        'brake': 'ASSEMBLY_STEPS',
        'clutch': 'CLUTCH_ASSEMBLY_STEPS',
        'engine': 'ENGINE_ASSEMBLY_STEPS',
        'car': 'FULL_CAR_ASSEMBLY_STEPS',
        'knuckle': 'KNUCKLE_JOINT_STEPS'
    }
    
    # Also add standard system alerts
    sys_prompts = {
        'sys_complete': {
            'en': 'Assembly sequence successfully completed. Official ISO Quality Certificate generated.',
            'ta': 'அசெம்பிளி செயல்முறை வெற்றிகரமாக முடிந்தது. அதிகாரப்பூர்வ ஐஎஸ்ஓ தரச் சான்றிதழ் உருவாக்கப்பட்டது.',
            'ml': 'അസംബ്ലി പ്രക്രിയ വിജയകരമായി പൂർത്തിയായി. ഔദ്യോഗിക ഐഎസ്ഒ ഗുണനിലവാര സർട്ടിഫിക്കറ്റ് തയ്യാറാക്കി.',
            'hi': 'असेंबली प्रक्रिया सफलतापूर्वक पूरी हुई। आधिकारिक आईएसओ गुणवत्ता प्रमाणपत्र तैयार किया गया।'
        },
        'sys_defect': {
            'en': 'Quality defect detected. Assembly halted for CMM realignment.',
            'ta': 'கூறு பிழை கண்டறியப்பட்டது. சிஎம்எம் மறுசீரமைப்புக்காக அசெம்பிளி வரிசை நிறுத்தப்பட்டது.',
            'ml': 'ഘടകത്തിൽ പിശക് കണ്ടെത്തി. പുനഃക്രമീകരണത്തിനായി അസംബ്ലി ലൈൻ നിർത്തിവെച്ചു.',
            'hi': 'घटक में दोष पाया गया। पुनः संरेखण के लिए असेंबली रोक दी गई है।'
        },
        'sys_datum': {
            'en': 'Geometric datum alignment verified within ISO tolerance. Assembly line restored.',
            'ta': 'வடிவியல் சீரமைப்பு ஐஎஸ்ஓ சகிப்புத்தன்மைக்குள் சரிபார்க்கப்பட்டது. அசெம்பிளி தொடர்கிறது.',
            'ml': 'ജ്യാമിതീയ ക്രമീകരണം ഐഎസ്ഒ മാനദണ്ഡങ്ങൾക്ക് അനുസൃതമാണെന്ന് ഉറപ്പുവരുത്തി. അസംബ്ലി പുനരാരംഭിച്ചു.',
            'hi': 'ज्यामितीय संरेखण आईएसओ मानक के अनुसार सत्यापित किया गया। असेंबली पुनः शुरू हुई।'
        }
    }

    for sys_key, langs in sys_prompts.items():
        for lang, text in langs.items():
            out_file = os.path.join(target_dir, f"{sys_key}_{lang}.mp3")
            clean_and_download(text, lang, out_file)

    for mod_key, array_name in modules.items():
        # Find array content
        match = re.search(r'export const ' + array_name + r'\s*=\s*\[([\s\S]*?)\];', content)
        if not match:
            print(f"Could not find array {array_name}")
            continue
        
        arr_content = match.group(1)
        # Find all steps
        step_blocks = re.findall(r'\{\s*id:\s*(\d+)[\s\S]*?translations:\s*\{([\s\S]*?)\}[\s\S]*?\}', arr_content)
        print(f"Found {len(step_blocks)} steps for {mod_key}")
        
        for step_id, trans_block in step_blocks:
            for lang in ['en', 'ta', 'ml', 'hi']:
                trans_match = re.search(rf"{lang}:\s*'([^']+)'", trans_block)
                if not trans_match:
                    trans_match = re.search(rf'{lang}:\s*"([^"]+)"', trans_block)
                if trans_match:
                    text = trans_match.group(1)
                    out_file = os.path.join(target_dir, f"{mod_key}_{step_id}_{lang}.mp3")
                    clean_and_download(text, lang, out_file)
                else:
                    print(f"Missing translation for {mod_key} step {step_id} lang {lang}")

    print("Voice pack generation finished!")

if __name__ == '__main__':
    main()

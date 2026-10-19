import re

with open('d:/new web record file/src/components/assemblyData.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of all 24 voiceScript translations
translations_map = {
    # Brake steps
    'Step 1: Inspect the wheel hub bearing and wipe the spindle mounting face clean. Ensure wheel studs are undamaged.': {
        'en': 'Step 1: Inspect the wheel hub bearing and wipe the spindle mounting face clean. Ensure wheel studs are undamaged.',
        'ta': 'படி 1: வீல் ஹப் பேரிங்கை சரிபார்த்து, ஸ்பிண்டில் மேற்பரப்பை சுத்தமாக துடைக்கவும். வீல் ஸ்டட்கள் சேதமடையாமல் இருப்பதை உறுதிசெய்யவும்.',
        'ml': 'ഘട്ടം 1: വീൽ ഹബ് ബെയറിംഗ് പരിശോധിച്ച് സ്പിൻഡിൽ ഉപരിതലം വൃത്തിയാക്കുക. സ്റ്റഡുകൾക്ക് കേടുപാടുകൾ ഇല്ലെന്ന് ഉറപ്പുവരുത്തുക.',
        'hi': 'चरण 1: व्हील हब बेयरिंग का निरीक्षण करें और स्पिंडल सतह को साफ करें। सुनिश्चित करें कि स्टड क्षतिग्रस्त नहीं हैं।'
    },
    'Step 2: Slide the cross-drilled rotor disc over the hub studs. Fasten the locator screw to 15 Newton meters.': {
        'en': 'Step 2: Slide the cross-drilled rotor disc over the hub studs. Fasten the locator screw to 15 Newton meters.',
        'ta': 'படி 2: ரோட்டார் டிஸ்க்கை ஹப் ஸ்டட்கள் மீது பொருத்தவும். லொக்கேட்டர் ஸ்க்ரூவை 15 நியூட்டன் மீட்டர் முறுக்குவிசையில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 2: റോട്ടർ ഡിസ്ക് ഹബ് സ്റ്റഡുകളിലേക്ക് ഘടിപ്പിക്കുക. ലൊക്കേറ്റർ സ്ക്രൂ 15 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 2: रोटर डिस्क को हब स्टड पर स्लाइड करें। लोकेटर स्क्रू को 15 न्यूटन मीटर पर कसें।'
    },
    'Step 3: Align the caliper anchor bracket over the rotor. Torque the two heavy mounting bolts to 75 Newton meters in cross sequence.': {
        'en': 'Step 3: Align the caliper anchor bracket over the rotor. Torque the two heavy mounting bolts to 75 Newton meters in cross sequence.',
        'ta': 'படி 3: காலிபர் பிராக்கெட்டை ரோட்டாரின் மேல் பொருத்தவும். இரண்டு மவுண்டிங் போல்ட்களையும் குறுக்கு வரிசையில் 75 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 3: കാലിപ്പർ ബ്രാക്കറ്റ് റോട്ടറിന് മുകളിൽ ഘടിപ്പിക്കുക. രണ്ട് ബോൾട്ടുകളും 75 ന്യൂട്ടൺ മീറ്ററിൽ ക്രോസ് ക്രമത്തിൽ മുറുക്കുക.',
        'hi': 'चरण 3: कैलीपर ब्रैकेट को रोटर के ऊपर संरेखित करें। दोनों बोल्ट को क्रॉस क्रम में 75 न्यूटन मीटर पर कसें।'
    },
    'Step 4: Slide the inner and outer ceramic brake pads into the stainless bracket abutment clips until firmly seated.': {
        'en': 'Step 4: Slide the inner and outer ceramic brake pads into the stainless bracket abutment clips until firmly seated.',
        'ta': 'படி 4: உள் மற்றும் வெளி செராமிக் பிரேக் பேட்களை பிராக்கெட் கிளிப்புகளில் உறுதியாக அமரும் வரை பொருத்தவும்.',
        'ml': 'ഘട്ടം 4: സെറാമിക് ബ്രേക്ക് പാഡുകൾ ബ്രാക്കറ്റ് ക്ലിപ്പുകളിലേക്ക് കൃത്യമായി ഘടിപ്പിക്കുക.',
        'hi': 'चरण 4: इनर और आउटर सिरेमिक ब्रेक पैड को ब्रैकेट क्लिप में मजबूती से बैठाएं।'
    },
    'Step 5: Lower the red caliper body over the pads. Thread the guide slide pins and torque to 35 Newton meters.': {
        'en': 'Step 5: Lower the red caliper body over the pads. Thread the guide slide pins and torque to 35 Newton meters.',
        'ta': 'படி 5: சிவப்பு காலிபர் பாடியை பேட்களின் மேல் பொருத்தவும். ஸ்லைடு பின்களை 35 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 5: റെഡ് കാലിപ്പർ ബോഡി പാഡുകൾക്ക് മുകളിലേക്ക് ഇറക്കുക. സ്ലൈഡ് പിന്നുകൾ 35 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 5: लाल कैलीपर बॉडी को पैड के ऊपर रखें। गाइड पिन को 35 न्यूटन मीटर पर कसें।'
    },
    'Step 6: Automobile brake assembly complete and certified. All torque specifications verified within tolerance.': {
        'en': 'Step 6: Automobile brake assembly complete and certified. All torque specifications verified within tolerance.',
        'ta': 'படி 6: ஆட்டோமொபைல் பிரேக் அசெம்பிளி வெற்றிகரமாக முடிந்தது. அனைத்து முறுக்குவிசை அளவுகளும் ஐஎஸ்ஓ தரத்தில் சரிபார்க்கப்பட்டது.',
        'ml': 'ഘട്ടം 6: ഓട്ടോമൊബൈൽ ബ്രേക്ക് അസംബ്ലി പൂർത്തിയായി. എല്ലാ ടോർക്ക് സ്പെസിഫിക്കേഷനുകളും പരിശോധിച്ചു.',
        'hi': 'चरण 6: ऑटोमोबाइल ब्रेक असेंबली पूरी और प्रमाणित हुई। सभी टॉर्क विनिर्देश सहनशीलता के भीतर सत्यापित हैं।'
    },

    # Clutch steps
    'Step 1: Inspect the flywheel friction surface for runout and thermal cracks. Degrease thoroughly to prevent clutch slippage.': {
        'en': 'Step 1: Inspect the flywheel friction surface for runout and thermal cracks. Degrease thoroughly to prevent clutch slippage.',
        'ta': 'படி 1: ஃபிளைவீல் உராய்வு மேற்பரப்பில் விரிசல்கள் உள்ளதா என ஆய்வு செய்யவும். கிளட்ச் நழுவாமல் இருக்க சுத்தமாக துடைக்கவும்.',
        'ml': 'ഘട്ടം 1: ഫ്ലൈവീൽ ഉപരിതലം പരിശോധിച്ച് വൃത്തിയാക്കുക. ക്ലച്ച് തെന്നിമാറുന്നത് തടയാൻ നന്നായി തുടയ്ക്കുക.',
        'hi': 'चरण 1: फ्लाईव्हील घर्षण सतह का निरीक्षण करें। क्लच फिसलने से रोकने के लिए अच्छी तरह से साफ करें।'
    },
    'Step 2: Position the friction disc against the flywheel using the alignment arbor tool. Ensure the damper springs face gearbox side.': {
        'en': 'Step 2: Position the friction disc against the flywheel using the alignment arbor tool. Ensure the damper springs face gearbox side.',
        'ta': 'படி 2: அலைன்மென்ட் கருவியைப் பயன்படுத்தி உராய்வு டிஸ்க்கை ஃபிளைவீலுக்கு எதிராக பொருத்தவும். ஸ்பிரிங் கியர்பாக்ஸ் நோக்கி இருப்பதை உறுதிசெய்யவும்.',
        'ml': 'ഘട്ടം 2: അലൈൻമെന്റ് ഉപകരണം ഉപയോഗിച്ച് ഫ്രിക്ഷൻ ഡിസ്ക് ഫ്ലൈവീലിൽ ഘടിപ്പിക്കുക.',
        'hi': 'चरण 2: अलाइनमेंट टूल की मदद से फ्रिक्शन डिस्क को फ्लाईव्हील के सामने रखें। स्प्रिंग गियरबॉक्स की तरफ होनी चाहिए।'
    },
    'Step 3: Lower the cast pressure plate onto the flywheel locating dowel pins. Verify drive straps are undamaged.': {
        'en': 'Step 3: Lower the cast pressure plate onto the flywheel locating dowel pins. Verify drive straps are undamaged.',
        'ta': 'படி 3: பிரஷர் பிளேட்டை ஃபிளைவீல் டவல் பின்களில் பொருத்தவும். டிரைவ் ஸ்ட்ராப்கள் சேதமடையாமல் இருப்பதை உறுதிசெய்யவும்.',
        'ml': 'ഘട്ടം 3: പ്രഷർ പ്ലേറ്റ് ഫ്ലൈവീൽ പിന്നുകളിലേക്ക് താഴ്ത്തുക. ഡ്രൈവ് സ്ട്രാപ്പുകൾ കേടുകൂടാതെയാണെന്ന് ഉറപ്പുവരുത്തുക.',
        'hi': 'चरण 3: प्रेशर प्लेट को फ्लाईव्हील पिन पर रखें। सत्यापित करें कि स्ट्रैप्स सुरक्षित हैं।'
    },
    'Step 4: Seat the diaphragm Belleville spring into the fulcrum ring guides. Inspect all release fingers for uniform height.': {
        'en': 'Step 4: Seat the diaphragm Belleville spring into the fulcrum ring guides. Inspect all release fingers for uniform height.',
        'ta': 'படி 4: டயாபிராம் ஸ்பிரிங்கை ஃபுல்க்ரம் ரிங் வழிகாட்டிகளில் பொருத்தவும். அனைத்து ஃபிங்கர்களும் ஒரே சீரான உயரத்தில் இருப்பதை ஆய்வு செய்யவும்.',
        'ml': 'ഘട്ടം 4: ഡയഫ്രം സ്പ്രിംഗ് കൃത്യമായി ഘടിപ്പിക്കുക. എല്ലാ റിലീസ് ഫിംഗറുകളുടെയും ഉയരം പരിശോധിക്കുക.',
        'hi': 'चरण 4: डायाफ्राम स्प्रिंग को रिंग गाइड में बैठाएं। सभी रिलीज फिंगर्स की एकसमान ऊंचाई का निरीक्षण करें।'
    },
    'Step 5: Install the clutch cover over the locating dowels. Fasten the 6 flange bolts in a star pattern to 25 Newton meters.': {
        'en': 'Step 5: Install the clutch cover over the locating dowels. Fasten the 6 flange bolts in a star pattern to 25 Newton meters.',
        'ta': 'படி 5: கிளட்ச் கவரை டவல் பின்களின் மேல் பொருத்தவும். 6 ஃபிளேன்ஜ் போல்ட்களை நட்சத்திர அமைப்பில் 25 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 5: ക്ലച്ച് കവർ ഘടിപ്പിക്കുക. 6 ഫ്ലേഞ്ച് ബോൾട്ടുകൾ സ്റ്റാർ പാറ്റേണിൽ 25 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 5: क्लच कवर को स्थापित करें। 6 फ्लैंज बोल्ट को स्टार पैटर्न में 25 न्यूटन मीटर पर कसें।'
    },
    'Step 6: Mount the release bearing and verify diaphragm finger clearance. Remove the alignment arbor tool. Clutch assembly is certified.': {
        'en': 'Step 6: Mount the release bearing and verify diaphragm finger clearance. Remove the alignment arbor tool. Clutch assembly is certified.',
        'ta': 'படி 6: ரிலீஸ் பேரிங்கை பொருத்தி இடைவெளியை சரிபார்க்கவும். அலைன்மென்ட் கருவியை அகற்றவும். கிளட்ச் அசெம்பிளி சான்றளிக்கப்பட்டது.',
        'ml': 'ഘട്ടം 6: റിലീസ് ബെയറിംഗ് ഘടിപ്പിക്കുക. അലൈൻമെന്റ് ടൂൾ മാറ്റുക. ക്ലച്ച് അസംബ്ലി സർട്ടിഫൈ ചെയ്തു.',
        'hi': 'चरण 6: रिलीज बेयरिंग लगाएं और क्लीयरेंस जांचें। अलाइनमेंट टूल हटाएं। क्लच असेंबली प्रमाणित है।'
    },

    # Full Car steps
    'Step 1: Position the tubular spaceframe chassis onto the AGV assembly jig. Verify laser alignment datum points across the monocoque.': {
        'en': 'Step 1: Position the tubular spaceframe chassis onto the AGV assembly jig. Verify laser alignment datum points across the monocoque.',
        'ta': 'படி 1: டியூபுலர் சேசிஸை அசெம்பிளி ஜிக்கில் நிலைநிறுத்தவும். லேசர் சீரமைப்பு புள்ளிகளை சரிபார்க்கவும்.',
        'ml': 'ഘട്ടം 1: ട്യൂബുലാർ ഷാസി അസംബ്ലി ജിഗ്ഗിൽ ഘടിപ്പിക്കുക. ലേസർ അലൈൻമെന്റ് പോയിന്റുകൾ പരിശോധിക്കുക.',
        'hi': 'चरण 1: ट्यूबलर चेसिस को असेंबली जिग पर रखें। लेजर अलाइनमेंट बिंदुओं को सत्यापित करें।'
    },
    'Step 2: Lift the mid-engine V8 powertrain into the chassis bay. Fasten the hydraulic mounts to 85 Newton meters in cross sequence.': {
        'en': 'Step 2: Lift the mid-engine V8 powertrain into the chassis bay. Fasten the hydraulic mounts to 85 Newton meters in cross sequence.',
        'ta': 'படி 2: வி8 என்ஜினை சேசிஸ் பேவுக்குள் ஏற்றி பொருத்தவும். ஹைட்ராலிக் மவுண்ட்களை 85 நியூட்டன் மீட்டரில் குறுக்கு வரிசையில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 2: വി8 എഞ്ചിൻ ഷാസിയിലേക്ക് ഉയർത്തി ഘടിപ്പിക്കുക. മൗണ്ടുകൾ 85 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 2: V8 इंजन को चेसिस में लगाएं। हाइड्रोलिक माउंट को 85 न्यूटन मीटर पर कसें।'
    },
    'Step 3: Integrate double wishbone suspension arms and racing coilovers. Torque ball joints and shock tower bolts to 65 Newton meters.': {
        'en': 'Step 3: Integrate double wishbone suspension arms and racing coilovers. Torque ball joints and shock tower bolts to 65 Newton meters.',
        'ta': 'படி 3: சஸ்பென்ஷன் ஆர்ம்ஸ் மற்றும் காயில்ஓவர்களை இணைக்கவும். போல்ட்களை 65 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 3: സസ്പെൻഷൻ ആംസും കോയിൽഓവറുകളും ഘടിപ്പിക്കുക. ബോൾട്ടുകൾ 65 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 3: सस्पेंशन आर्म्स और कॉइलओवर्स जोड़ें। बोल्ट को 65 न्यूटन मीटर पर कसें।'
    },
    'Step 4: Mount ventilated brake rotors and racing calipers across all four wheel hubs. Fasten hydraulic lines to 45 Newton meters.': {
        'en': 'Step 4: Mount ventilated brake rotors and racing calipers across all four wheel hubs. Fasten hydraulic lines to 45 Newton meters.',
        'ta': 'படி 4: நான்கு சக்கரங்களிலும் பிரேக் ரோட்டார்கள் மற்றும் காலிபர்களை பொருத்தவும். ஹைட்ராலிக் குழாய்களை 45 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 4: നാല് വീലുകളിലും ബ്രേക്ക് റോട്ടറുകളും കാലിപ്പർമാരും ഘടിപ്പിക്കുക. പൈപ്പുകൾ 45 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 4: चारों पहियों पर ब्रेक रोटर्स और कैलीपर्स लगाएं। हाइड्रोलिक लाइनों को 45 न्यूटन मीटर पर कसें।'
    },
    'Step 5: Lower the aerodynamic carbon fiber body shell and canopy onto the chassis. Verify flush panel gap tolerances across all exterior seams.': {
        'en': 'Step 5: Lower the aerodynamic carbon fiber body shell and canopy onto the chassis. Verify flush panel gap tolerances across all exterior seams.',
        'ta': 'படி 5: கார்பன் ஃபைபர் பாடி ஷெல்லை சேசிஸ் மீது இறக்கி பொருத்தவும். பேனல் இடைவெளி சகிப்புத்தன்மையை சரிபார்க்கவும்.',
        'ml': 'ഘട്ടം 5: കാർബൺ ഫൈബർ ബോഡി ഷെൽ ഷാസിയിലേക്ക് ഇറക്കുക. പാനൽ വിടവുകൾ കൃത്യമാണെന്ന് പരിശോധിക്കുക.',
        'hi': 'चरण 5: कार्बन फाइबर बॉडी शेल को चेसिस पर रखें। पैनल गैप सहिष्णुता की जांच करें।'
    },
    'Step 6: Mount the forged alloy wheels and performance tires. Torque all wheel lug nuts in a cross star sequence to 120 Newton meters. Vehicle assembly is 100 percent complete.': {
        'en': 'Step 6: Mount the forged alloy wheels and performance tires. Torque all wheel lug nuts in a cross star sequence to 120 Newton meters. Vehicle assembly is 100 percent complete.',
        'ta': 'படி 6: அலாய் வீல்களை பொருத்தவும். அனைத்து லக் நட்டுகளையும் நட்சத்திர அமைப்பில் 120 நியூட்டன் மீட்டரில் இறுக்கவும். வாகனம் 100 சதவீதம் முழுமை பெற்றது.',
        'ml': 'ഘട്ടം 6: അലോയ് വീലുകൾ ഘടിപ്പിക്കുക. എല്ലാ നട്ടുകളും 120 ന്യൂട്ടൺ മീറ്ററിൽ ക്രോസ് സ്റ്റാർ ക്രമത്തിൽ മുറുക്കുക. വാഹനം പൂർത്തിയായി.',
        'hi': 'चरण 6: अलॉय व्हील लगाएं। सभी व्हील नट को क्रॉस स्टार क्रम में 120 न्यूटन मीटर पर कसें। वाहन असेंबली 100 प्रतिशत पूरी है।'
    },

    # Knuckle Joint steps
    'Step 1: Clamp the fork end into the jig. Inspect the upper and lower pin bores for concentricity and burr-free chamfers.': {
        'en': 'Step 1: Clamp the fork end into the jig. Inspect the upper and lower pin bores for concentricity and burr-free chamfers.',
        'ta': 'படி 1: ஃபோர்க் முனையை ஜிக்கில் இறுக்கவும். மேல் மற்றும் கீழ் பின் துளைகள் சீராக உள்ளதா என ஆய்வு செய்யவும்.',
        'ml': 'ഘട്ടം 1: ഫോർക്ക് എൻഡ് ജിഗ്ഗിൽ ഘടിപ്പിക്കുക. മുകളിലെയും താഴത്തെയും ദ്വാരങ്ങൾ പരിശോധിക്കുക.',
        'hi': 'चरण 1: फोर्क एंड को जिग में क्लैंप करें। ऊपरी और निचले पिन छिद्रों का निरीक्षण करें।'
    },
    'Step 2: Slide the single eye end into the fork gap. Align the central bore to form a clean passage for the knuckle pin.': {
        'en': 'Step 2: Slide the single eye end into the fork gap. Align the central bore to form a clean passage for the knuckle pin.',
        'ta': 'படி 2: சிங்கிள் ஐ முனையை ஃபோர்க் இடைவெளியில் பொருத்தவும். நக்கிள் பின் நுழைவதற்கு துளையை சீரமைக்கவும்.',
        'ml': 'ഘട്ടം 2: സിംഗിൾ ഐ എൻഡ് ഫോർക്ക് ഗ്യാപ്പിലേക്ക് കടത്തുക. സെൻട്രൽ ബോർ നേരെയാക്കുക.',
        'hi': 'चरण 2: सिंगल आई एंड को फोर्क गैप में स्लाइड करें। नक्कल पिन के लिए केंद्रीय छिद्र को संरेखित करें।'
    },
    'Step 3: Insert the hardened knuckle pin from the top. Ensure the pin head seats fully flush against the upper fork ear.': {
        'en': 'Step 3: Insert the hardened knuckle pin from the top. Ensure the pin head seats fully flush against the upper fork ear.',
        'ta': 'படி 3: நக்கிள் பின்னை மேலிருந்து செருகவும். பின் தலை மேல் ஃபோர்க் பகுதியில் சரியாக அமர்வதை உறுதிசெய்யவும்.',
        'ml': 'ഘട്ടം 3: നക്കിൾ പിൻ മുകളിൽ നിന്ന് തിരുകുക. പിൻ തല ശരിയായി ഇരിക്കുന്നുണ്ടെന്ന് ഉറപ്പുവരുത്തുക.',
        'hi': 'चरण 3: नक्कल पिन को ऊपर से डालें। सुनिश्चित करें कि पिन हेड पूरी तरह से बैठ गया है।'
    },
    'Step 4: Slide the retention collar over the lower pin spigot. Align the through-hole on the collar with the cross-hole in the pin.': {
        'en': 'Step 4: Slide the retention collar over the lower pin spigot. Align the through-hole on the collar with the cross-hole in the pin.',
        'ta': 'படி 4: காலரை கீழ் பின் பகுதியில் பொருத்தவும். காலரில் உள்ள துளையை பின்னின் துளையுடன் நேராக சீரமைக்கவும்.',
        'ml': 'ഘട്ടം 4: കോളർ താഴത്തെ പിന്നിലേക്ക് കടത്തുക. ദ്വാരങ്ങൾ നേരെയാക്കുക.',
        'hi': 'चरण 4: निचले पिन पर रिटेंशन कॉलर स्लाइड करें। कॉलर के छिद्र को पिन के छिद्र से संरेखित करें।'
    },
    'Step 5: Drive the taper pin through the collar and knuckle pin. Torque locking fastener to 15 Newton meters to prevent pin displacement.': {
        'en': 'Step 5: Drive the taper pin through the collar and knuckle pin. Torque locking fastener to 15 Newton meters to prevent pin displacement.',
        'ta': 'படி 5: டேப்பர் பின்னை காலர் மற்றும் நக்கிள் பின் வழியாக செலுத்தவும். லாக்கிங் நட்டை 15 நியூட்டன் மீட்டரில் இறுக்கவும்.',
        'ml': 'ഘട്ടം 5: ടേപ്പർ പിൻ കോളറിലൂടെ അടിച്ചു കയറ്റുക. ലോക്കിംഗ് ഫാസ്റ്റനർ 15 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
        'hi': 'चरण 5: टेपर पिन को कॉलर और नक्कल पिन से गुजारें। लॉकिंग नट को 15 न्यूटन मीटर पर कसें।'
    },
    'Step 6: Knuckle joint assembly complete and certified. Articulation sweep and tensile load tests passed with zero defects.': {
        'en': 'Step 6: Knuckle joint assembly complete and certified. Articulation sweep and tensile load tests passed with zero defects.',
        'ta': 'படி 6: நக்கிள் ஜாயிண்ட் அசெம்பிளி வெற்றிகரமாக முடிந்தது. இயக்கம் மற்றும் இழுவிசை சோதனைகள் பூஜ்ஜிய பிழையுடன் தேர்ச்சி பெற்றது.',
        'ml': 'ഘട്ടം 6: നക്കിൾ ജോയിന്റ് അസംബ്ലി പൂർത്തിയായി. ടെൻസൈൽ ലോഡ് ടെസ്റ്റുകൾ വിജയകരമായി പൂർത്തിയാക്കി.',
        'hi': 'चरण 6: नक्कल जॉइंट असेंबली पूरी और प्रमाणित हुई। तनाव परीक्षण शून्य दोषों के साथ पास हुए।'
    }
}

# Replace in content:
count = 0
for vs, trans in translations_map.items():
    pattern = "voiceScript: '" + vs + "',"
    replacement = "voiceScript: '" + vs + "',\n    translations: {\n"
    replacement += "      en: " + repr(trans['en']) + ",\n"
    replacement += "      ta: " + repr(trans['ta']) + ",\n"
    replacement += "      ml: " + repr(trans['ml']) + ",\n"
    replacement += "      hi: " + repr(trans['hi']) + "\n"
    replacement += "    },"
    if pattern in content:
        content = content.replace(pattern, replacement)
        count += 1
    else:
        print("Pattern not found:", vs[:30])

with open('d:/new web record file/src/components/assemblyData.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully injected translations into {count} of {len(translations_map)} steps.")

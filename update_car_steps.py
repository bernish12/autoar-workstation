import os

CAR_STEPS_CODE = '''export const FULL_CAR_ASSEMBLY_STEPS = [
  {
    id: 1,
    partKey: 'chassis',
    partName: 'Station 01: BMW M Carbon Core Monocoque Spaceframe & Floorpan',
    partCode: 'BMW-CHS-M01',
    category: 'Trim Line 01 - Structural Carbon Core & Safety Cell',
    material: 'Carbon-Fiber Reinforced Polymer (CFRP) & Ultra High-Tensile Steel',
    tool: 'Laser Coordinate Measuring Machine (CMM) & AGV Hydraulic Dock',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Datum Diagonal Tolerance < 0.5 mm',
    title: 'BMW Carbon Core Spaceframe Fixture & Datum Laser Alignment',
    instruction: 'Rig the BMW Carbon Core monocoque spaceframe onto the main conveyor AGV fixture. Inspect laser datum points, roll-cage welds, crash bulkhead symmetry, and floorpan flatness.',
    voiceScript: 'Step 1: Position the BMW Carbon Core spaceframe chassis onto the AGV assembly jig. Verify laser alignment datum points across the monocoque.',
    translations: {
      en: 'Step 1: Position the BMW Carbon Core spaceframe chassis onto the AGV assembly jig. Verify laser alignment datum points across the monocoque.',
      ta: 'படி 1: பிஎம்டபிள்யூ கார்பன் கோர் மோனோகாக் சேசிஸை அசெம்பிளி ஏஜிவி ஜிக்கில் நிலைநிறுத்தவும். லேசர் சீரமைப்பு புள்ளிகளை சரிபார்க்கவும்.',
      ml: 'ഘട്ടം 1: ബിഎംഡബ്ല്യു കാർബൺ ഷാസി അസംബ്ലി ജിഗ്ഗിൽ ഘടിപ്പിക്കുക. ലേസർ അലൈൻമെന്റ് പരിശോധിക്കുക.',
      hi: 'चरण 1: बीएमडब्ल्यू कार्बन कोर चेसिस को असेंबली जिग पर रखें। लेजर अलाइनमेंट बिंदुओं को सत्यापित करें।'
    },
    tip: 'Ensure all 8 chassis jig clamping pins seat fully before initiating the electrical harness routing cycle.',
    colorTag: '#0066b1',
    specs: [
      { label: 'Platform Architecture', value: 'BMW CLAR Carbon Core' },
      { label: 'Wheelbase (Nominal)', value: '2857 mm' },
      { label: 'Torsional Rigidity', value: '42,000 Nm/deg' },
      { label: 'Safety Cell Standard', value: 'FIA Appendix J / BMW M Spec' }
    ],
    defectConfig: {
      defectName: 'BMW Carbon Core CMM Datum Twist Defect',
      defectType: 'Chassis Torsional Warpage',
      paramName: 'Z-Datum Offset',
      nominal: 0.0,
      defectInitial: 2.8,
      tolerance: 0.5,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 3.5,
      stepSize: 0.1,
      instruction: 'Clamp AGV fixture hydraulic locating pins to bring spaceframe datum within 0.5 mm.'
    }
  },
  {
    id: 2,
    partKey: 'wiring',
    partName: 'Station 02: BMW 48V/12V Main Electrical Harness & HV Busway',
    partCode: 'BMW-HAR-M02',
    category: 'Trim Line 02 - Electrical Backbone & High-Voltage Architecture',
    material: 'Oxygen-Free Copper Braided Harness & Cross-Linked Polyethylene (XLPE)',
    tool: 'Acoustic Connector Verification Pen & Optical Terminal Scanner',
    targetTorque: 12,
    requiresTorque: true,
    tolerance: 'Connector Seating Click < 0.2 mm',
    title: 'BMW M Main Cabin Wiring Harness & HV Busway Routing (12 Nm)',
    instruction: 'Route the high-voltage 48V orange busway trunk along the central transmission tunnel. Lay main 12V cabin wiring loom along floor sills, snap into chassis retainers, and torque master ECU terminal to 12 Nm.',
    voiceScript: 'Step 2: Lay the 48V high-voltage busway and main cabin wiring loom into floor channels. Fasten master ECU grounds to 12 Newton meters.',
    translations: {
      en: 'Step 2: Lay the 48V high-voltage busway and main cabin wiring loom into floor channels. Fasten master ECU grounds to 12 Newton meters.',
      ta: 'படி 2: 48V ஹை-வோல்டேஜ் மற்றும் மெயின் ஒயரிங் ஹார்னஸை சேசிஸ் சேனல்களில் பதித்து, ஈசியு எர்த் நட்டை 12 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 2: 48V ഹൈ-വോൾട്ടേജ് മെയിൻ വയറിങ് ഹാർനെസ് ഷാസിയിൽ റൂട്ട് ചെയ്യുക. ഇസിയു കണക്ടർ 12 ന്യൂട്ടൺ മീറ്ററിൽ ഉറപ്പിക്കുക.',
      hi: 'चरण 2: 48V हाई-वोल्टेज और मुख्य केबिन वायरिंग लूम को चेसिस चैनलों में बिछाएं। मास्टर ईसीयू को 12 न्यूटन मीटर पर कसें।'
    },
    tip: 'Listen for dual audible clicks on all waterproof bulkhead grommets before advancing conveyor.',
    colorTag: '#f59e0b',
    specs: [
      { label: 'Busway Architecture', value: '48V Mild-Hybrid + 12V CAN-FD / Ethernet' },
      { label: 'Total Loom Length', value: '4.2 km Copper Core' },
      { label: 'Ground Terminal Torque', value: '12 Nm (±0.8 Nm)' },
      { label: 'Ingress Protection', value: 'IP67 / IP6K9K Waterproof' }
    ],
    defectConfig: {
      defectName: 'High-Voltage Cable Loom Seating Dislodgement',
      defectType: 'Wiring Channel Retention Clearance',
      paramName: 'Conduit Gap',
      nominal: 0.0,
      defectInitial: 3.2,
      tolerance: 0.8,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 4.0,
      stepSize: 0.2,
      instruction: 'Press wiring harness retention clips into floorpan slots until flush.'
    }
  },
  {
    id: 3,
    partKey: 'cockpit',
    partName: 'Station 03: BMW Curved Display, Magnesium Beam & M-Cockpit Module',
    partCode: 'BMW-CKP-M03',
    category: 'Trim Line 03 - Cockpit Module & Electronic User Interface',
    material: 'Die-Cast Magnesium AM60B, Anti-Reflective Chemically Toughened Glass',
    tool: 'Robotic Cockpit Manipulator & Multi-Axis Nutrunner',
    targetTorque: 45,
    requiresTorque: true,
    tolerance: 'Beam Lateral Gap < 0.6 mm',
    title: 'BMW Curved Display & Cockpit Cross-Car Beam Installation (45 Nm)',
    instruction: 'Robotically swing the pre-assembled cockpit module through the windshield opening. Fasten the structural magnesium cross-car beam to A-pillar brackets with 4 high-tensile bolts torqued to 45 Nm.',
    voiceScript: 'Step 3: Robotically dock the BMW Curved Display and cockpit cross beam into the A-pillars. Torque mounting bolts to 45 Newton meters.',
    translations: {
      en: 'Step 3: Robotically dock the BMW Curved Display and cockpit cross beam into the A-pillars. Torque mounting bolts to 45 Newton meters.',
      ta: 'படி 3: பிஎம்டபிள்யூ கர்வ்ட் டிஸ்ப்ளே கொண்ட காக்பிட் மாட்யூலை ஏ-பில்லரில் பொருத்தி, 4 போல்ட்களையும் 45 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 3: ബിഎംഡബ്ല്യു കർവ്ഡ് ഡിസ്‌പ്ലേയുള്ള കോക്ക്പിറ്റ് മൊഡ്യൂൾ ഘടിപ്പിക്കുക. ബോൾട്ടുകൾ 45 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 3: बीएमडब्ल्यू कर्व्ड डिस्प्ले और कॉकपिट मॉड्यूल को ए-पिलर्स में लगाएं। 45 न्यूटन मीटर पर बोल्ट कसें।'
    },
    tip: 'Verify zero harness pinch between magnesium cross-car beam and firewall crash pad.',
    colorTag: '#00f0ff',
    specs: [
      { label: 'Cross-Car Beam', value: 'High-Rigidity Die-Cast Magnesium' },
      { label: 'Display Panel', value: '12.3" + 14.9" BMW Curved Display' },
      { label: 'A-Pillar Fasteners', value: '4x M10 Grade 10.9 (45 Nm)' },
      { label: 'Operating System', value: 'BMW iDrive 8.5 Digital Architecture' }
    ],
    defectConfig: {
      defectName: 'Cockpit Cross-Car Beam Lateral Alignment Error',
      defectType: 'A-Pillar Mount Transverse Runout',
      paramName: 'Beam Offset',
      nominal: 0.0,
      defectInitial: 2.4,
      tolerance: 0.5,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 3.0,
      stepSize: 0.1,
      instruction: 'Adjust robotic gantry alignment pins to eliminate cross-car beam offset.'
    }
  },
  {
    id: 4,
    partKey: 'powertrain',
    partName: 'Station 04: "Die Hochzeit" - BMW M TwinPower Turbo V8 Marriage',
    partCode: 'BMW-PWR-S63',
    category: 'Mechanical Line 01 - Powertrain Marriage (Die Hochzeit)',
    material: 'Alu-Silicon Closed-Deck Block, Twin-Scroll Turbos & CFRP Driveshaft',
    tool: 'Hydraulic Marriage Pallet Lift & Multi-Spindle Nutrunner',
    targetTorque: 85,
    requiresTorque: true,
    tolerance: 'Mount Angular Runout < 0.2 deg',
    title: 'BMW M-Power Engine Marriage & Subframe Docking (85 Nm)',
    instruction: 'Elevate BMW 4.4L M TwinPower Turbo V8 engine, 8-speed M-Steptronic transmission, and front subframe via hydraulic marriage lift into engine bay. Torque 4 active hydraulic engine mounts in cross sequence to 85 Nm.',
    voiceScript: 'Step 4: Lift the BMW M TwinPower Turbo V8 powertrain into the chassis bay. Fasten the hydraulic mounts to 85 Newton meters in cross sequence.',
    translations: {
      en: 'Step 4: Lift the BMW M TwinPower Turbo V8 powertrain into the chassis bay. Fasten the hydraulic mounts to 85 Newton meters in cross sequence.',
      ta: 'படி 4: பிஎம்டபிள்யூ வி8 என்ஜினை சேசிஸ் பே-க்குள் ஏற்றி, ஹைட்ராலிக் மவுண்ட்களை 85 நியூட்டன் மீட்டரில் குறுக்கு அமைப்பில் இறுக்கவும்.',
      ml: 'ഘട്ടം 4: ബിഎംഡബ്ല്യു വി8 എം എഞ്ചിൻ ഷാസിയിലേക്ക് ഉയർത്തി ഘടിപ്പിക്കുക. മൗണ്ടുകൾ 85 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 4: बीएमडब्ल्यू एम ट्विनपावर टर्बो V8 इंजन को चेसिस में लगाएं। हाइड्रोलिक माउंट को 85 न्यूटन मीटर पर कसें।'
    },
    tip: 'Check rear M-Differential carbon driveshaft clearance against subframe before torquing mounts.',
    colorTag: '#ef4444',
    specs: [
      { label: 'Engine Architecture', value: '4.4L 90° V8 M TwinPower Turbo' },
      { label: 'Transmission', value: '8-Speed M-Steptronic with Drivelogic' },
      { label: 'Active Mount Torque', value: '85 Nm (±3.0 Nm)' },
      { label: 'Driveshaft Spec', value: 'Single-Piece CFRP Carbon Tube' }
    ],
    defectConfig: {
      defectName: 'Powertrain Marriage Hydraulic Mount Cant',
      defectType: 'Engine Subframe Angular Misalignment',
      paramName: 'Tilt Angle Offset',
      nominal: 0.0,
      defectInitial: 3.1,
      tolerance: 0.3,
      unit: '°',
      minVal: 0.0,
      maxVal: 4.0,
      stepSize: 0.1,
      instruction: 'Level the AGV hydraulic marriage lift to align all 4 subframe locating dowels.'
    }
  },
  {
    id: 5,
    partKey: 'suspension',
    partName: 'Station 05: BMW M-Adaptive Double Wishbone Suspension & Sway Bars',
    partCode: 'BMW-SUS-M05',
    category: 'Mechanical Line 02 - Driveline & Adaptive M-Chassis Running Gear',
    material: 'Forged 6082-T6 Aluminum Links & Active Electronic Damper Valving',
    tool: 'Multi-Spindle Suspension Nutrunner & Camber Gauge',
    targetTorque: 65,
    requiresTorque: true,
    tolerance: 'Camber Angle Tolerance ± 0.05°',
    title: 'BMW M-Adaptive Suspension & Anti-Roll Bar Torquing (65 Nm)',
    instruction: 'Bolt upper and lower forged control arms into chassis pick-up points. Mount high-rate M-Adaptive electronic coilovers to shock towers and torque ball-joint pinch bolts to 65 Nm at curb-height ride position.',
    voiceScript: 'Step 5: Bolt the adaptive M suspension control arms and coilovers. Fasten suspension pinch bolts to 65 Newton meters at curb ride height.',
    translations: {
      en: 'Step 5: Bolt the adaptive M suspension control arms and coilovers. Fasten suspension pinch bolts to 65 Newton meters at curb ride height.',
      ta: 'படி 5: அடாப்டிவ் எம் சஸ்பென்ஷன் ஆர்ம்ஸ் மற்றும் காயில்-ஓவர்களை பொருத்தி, போல்ட்களை 65 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 5: അഡാപ്റ്റീവ് എം സസ്പെൻഷൻ കൺട്രോൾ ആമുകൾ ഘടിപ്പിക്കുക. ബോൾട്ടുകൾ 65 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 5: अडेप्टिव एम सस्पेंशन कंट्रोल आर्म्स लगाएं। 65 न्यूटन मीटर पर सस्पेंशन बोल्ट कसें।'
    },
    tip: 'Always torque suspension fasteners at curb-height ride position to eliminate bushing pre-load.',
    colorTag: '#d97706',
    specs: [
      { label: 'Front Suspension', value: 'Adaptive M Double-Wishbone' },
      { label: 'Rear Suspension', value: 'Five-Link Lightweight M-Axle' },
      { label: 'Damper Architecture', value: 'Active EDC Magnetic Valving' },
      { label: 'Fastener Torque', value: '65 Nm (Grade 10.9 M10)' }
    ],
    defectConfig: {
      defectName: 'Adaptive Suspension Camber Eccentricity Defect',
      defectType: 'Front Wheel Hub Camber Runout',
      paramName: 'Camber Angle',
      nominal: -1.5,
      defectInitial: 1.2,
      tolerance: 0.1,
      unit: '°',
      minVal: -2.0,
      maxVal: 2.0,
      stepSize: 0.1,
      instruction: 'Rotate lower wishbone eccentric camber cam to establish -1.5° M-track camber.'
    }
  },
  {
    id: 6,
    partKey: 'exhaust',
    partName: 'Station 06: BMW M Dual-Branch Exhaust System & Quad Muffler Canister',
    partCode: 'BMW-EXH-M06',
    category: 'Underbody Line 01 - Exhaust System & Thermal Insulation',
    material: '1.4828 Heat-Resistant Stainless Steel & Inconel Resonator Sections',
    tool: 'Underbody Exhaust Lift & Pneumatic V-Band Nutrunner',
    targetTorque: 40,
    requiresTorque: true,
    tolerance: 'Exhaust Hanger Clearance > 15 mm',
    title: 'BMW M Dual-Branch Exhaust & Quad Muffler Installation (40 Nm)',
    instruction: 'Raise the dual-branch stainless steel exhaust system into underbody tunnel. Connect twin downpipes to turbo outlets, install V-band flange clamps torqued to 40 Nm, and hang quad-pipe rear muffler onto rubber isolators.',
    voiceScript: 'Step 6: Lift the dual-branch stainless exhaust system into the tunnel. Torque V-band clamps to 40 Newton meters.',
    translations: {
      en: 'Step 6: Lift the dual-branch stainless exhaust system into the tunnel. Torque V-band clamps to 40 Newton meters.',
      ta: 'படி 6: இரட்டை எக்ஸாஸ்ட் அமைப்பை அண்டர்பாடியில் பொருத்தி, வி-பேண்ட் கிளாம்ப்களை 40 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 6: എക്‌സ്‌ഹോസ്റ്റ് സിസ്റ്റം ഷാസിയിലേക്ക് ഘടിപ്പിക്കുക. വി-ബാൻഡ് ക്ലാമ്പുകൾ 40 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 6: ड्यूल-ब्रांच एग्जॉस्ट सिस्टम को अंडरबॉडी में लगाएं। वी-बैंड क्लैंप को 40 न्यूटन मीटर पर कसें।'
    },
    tip: 'Ensure electronic active sound butterfly flap harness clicks securely into rear heat shield port.',
    colorTag: '#64748b',
    specs: [
      { label: 'Exhaust Layout', value: 'Dual-Pipe System with X-Crossover' },
      { label: 'Tailpipe Finish', value: 'Quad 100mm Black Chrome M Tips' },
      { label: 'V-Band Torque', value: '40 Nm (±2.0 Nm)' },
      { label: 'Sound Actuation', value: 'Twin Electronic Variable Flaps' }
    ],
    defectConfig: {
      defectName: 'Exhaust Heat Shield Clearance Defect',
      defectType: 'Underbody Acoustic Contact Clearance',
      paramName: 'Shield Air Gap',
      nominal: 18.0,
      defectInitial: 4.5,
      tolerance: 2.0,
      unit: 'mm',
      minVal: 4.0,
      maxVal: 22.0,
      stepSize: 0.5,
      instruction: 'Reposition exhaust isolator hanger brackets to achieve 18 mm thermal clearance.'
    }
  },
  {
    id: 7,
    partKey: 'brake',
    partName: 'Station 07: BMW M Carbon-Ceramic 4-Corner Brake Assembly',
    partCode: 'BMW-BRK-CCB',
    category: 'Underbody Line 02 - Carbon-Ceramic High-Performance Brakes',
    material: 'Carbon-Silicon Carbide (C/SiC) & Monobloc Forged Aluminum Calipers',
    tool: 'Hydraulic Caliper Torque Wrench & Optical Thickness Gauge',
    targetTorque: 115,
    requiresTorque: true,
    tolerance: 'Rotor Lateral Runout < 0.015 mm',
    title: 'BMW M Carbon-Ceramic Calipers & Rotors Assembly (115 Nm)',
    instruction: 'Slide 400mm front and 380mm rear cross-drilled carbon-ceramic ventilated rotors onto wheel hubs. Mount 6-piston front and 4-piston rear M-Gold monobloc calipers, torquing radial carrier bolts to 115 Nm.',
    voiceScript: 'Step 7: Slide the carbon ceramic rotors onto the hubs. Fasten the 6-piston M calipers to 115 Newton meters.',
    translations: {
      en: 'Step 7: Slide the carbon ceramic rotors onto the hubs. Fasten the 6-piston M calipers to 115 Newton meters.',
      ta: 'படி 7: கார்பன்-செராமிக் ரோட்டர்களை வீல் ஹப்பில் பொருத்தி, 6-பிஸ்டன் எம் கேலிப்பர்களை 115 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 7: കാർബൺ സെറാമിക് ബ്രേക്ക് റോട്ടറുകൾ ഘടിപ്പിക്കുക. കാലിപ്പറുകൾ 115 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 7: कार्बन-सिरेमिक रोटर्स को हब पर लगाएं। 6-पिस्टन कैलिपर्स को 115 न्यूटन मीटर पर कसें।'
    },
    tip: 'Never allow hard tool contact against the carbon-ceramic rotor friction ring to avoid micro-fracturing.',
    colorTag: '#eab308',
    specs: [
      { label: 'Front Brake Spec', value: '400 x 38 mm Carbon-Silicon Carbide (C/SiC)' },
      { label: 'Rear Brake Spec', value: '380 x 28 mm Carbon-Silicon Carbide (C/SiC)' },
      { label: 'Caliper Architecture', value: '6-Piston Front / 4-Piston Rear Monobloc' },
      { label: 'Radial Bolt Torque', value: '115 Nm (High-Tensile Steel)' }
    ],
    defectConfig: {
      defectName: 'Carbon Ceramic Rotor Lateral Runout Defect',
      defectType: 'Brake Disc Axial Runout Error',
      paramName: 'Rotor Runout',
      nominal: 0.01,
      defectInitial: 0.08,
      tolerance: 0.015,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.12,
      stepSize: 0.005,
      instruction: 'Clean hub contact face and reseat rotor retention fasteners to eliminate runout.'
    }
  },
  {
    id: 8,
    partKey: 'seats',
    partName: 'Station 08: BMW M Carbon Lightweight Racing Bucket Seats',
    partCode: 'BMW-INT-M08',
    category: 'Interior Line 01 - M Carbon Bucket Seats & Safety Ergonomics',
    material: 'Autoclave CFRP Shell, High-Density Foam & Merino Fine-Grain Leather',
    tool: 'Overhead Seat Gantry Crane & Smart Torq-Driver',
    targetTorque: 48,
    requiresTorque: true,
    tolerance: 'Track Alignment Parallelism < 0.4 mm',
    title: 'BMW M Carbon Bucket Seats Installation & Rail Fastening (48 Nm)',
    instruction: 'Lower driver and passenger M Carbon racing bucket seats via overhead assisted gantry into cabin. Align guide pins into floorpan tracks, torque 4 floor bolts per seat to 48 Nm, and connect pyrotechnic pre-tensioner harnesses.',
    voiceScript: 'Step 8: Lower the M Carbon racing bucket seats into the cabin. Torque seat track bolts to 48 Newton meters.',
    translations: {
      en: 'Step 8: Lower the M Carbon racing bucket seats into the cabin. Torque seat track bolts to 48 Newton meters.',
      ta: 'படி 8: எம் கார்பன் பக்கெட் சீட்களை கேபினுக்குள் இறக்கி, சீட் டிராக் போல்ட்களை 48 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 8: എം കാർബൺ ബക്കറ്റ് സീറ്റുകൾ ഇൻസ്റ്റാൾ ചെയ്യുക. ട്രാക്ക് ബോൾട്ടുകൾ 48 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 8: एम कार्बन बकेट सीटों को केबिन में लगाएं। सीट ट्रैक बोल्ट को 48 न्यूटन मीटर पर कसें।'
    },
    tip: 'Confirm electronic harness connector locking tab clicks green before initiating seat memory calibration.',
    colorTag: '#3b82f6',
    specs: [
      { label: 'Seat Construction', value: 'Visible CFRP Carbon Fiber Shell' },
      { label: 'Weight Reduction', value: '9.6 kg lighter than standard M-Seats' },
      { label: 'Floor Track Bolts', value: '8x M10 Micro-encapsulated (48 Nm)' },
      { label: 'Safety System', value: 'Dual-Stage Side Airbags + Active Belts' }
    ],
    defectConfig: {
      defectName: 'Seat Track Parallelism Distortion',
      defectType: 'Seat Rail Longitudinal Alignment',
      paramName: 'Track Skew',
      nominal: 0.0,
      defectInitial: 1.8,
      tolerance: 0.4,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.5,
      stepSize: 0.1,
      instruction: 'Loosen front locator pins and slide seat forward to true track parallelism.'
    }
  },
  {
    id: 9,
    partKey: 'glazing',
    partName: 'Station 09: BMW Acoustic Curved Windshield & Hofmeister Glazing',
    partCode: 'BMW-GLZ-M09',
    category: 'Glazing Line 01 - Automated Windshield & Acoustic Glazing',
    material: 'Laminated Acoustic Safety Glass & Polyurethane Structural Adhesive',
    tool: 'Robotic Glass Applicator with Heated Adhesive Nozzle',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Adhesive Bead Profile 10.5 mm (± 0.5 mm)',
    title: 'BMW Acoustic Curved Windshield & Rear Window Glazing',
    instruction: 'Robotically dispense a continuous triangular polyurethane adhesive bead along the windshield flange. Lower the acoustic curved windshield and fastback rear glass backlight with optical vision guidance (< 0.5 mm flushness).',
    voiceScript: 'Step 9: Robotically dispense adhesive bead and press the acoustic curved windshield and rear glass into position.',
    translations: {
      en: 'Step 9: Robotically dispense adhesive bead and press the acoustic curved windshield and rear glass into position.',
      ta: 'படி 9: ரோபோடிக் முறையில் அக்ரிலிக் பசை பூசி, வளைந்த முன்பக்க கண்ணாடியை மற்றும் பின்பக்க கண்ணாடியை பொருத்தவும்.',
      ml: 'ഘട്ടം 9: റോബോട്ടിക് ഗ്ലാസ് ആപ്ലിക്കേറ്റർ ഉപയോഗിച്ച് അക്കൗസ്റ്റിക് വിൻഡ്ഷീൽഡ് ഒട്ടിക്കുക.',
      hi: 'चरण 9: रोबोटिक रूप से एडहेसिव लगाएं और कर्व्ड विंडशील्ड और रियर ग्लास को सटीक रूप से सेट करें।'
    },
    tip: 'Ensure humidity and chamber temperature remain within DIN EN ISO 9001 specs for optimal adhesive curing.',
    colorTag: '#38bdf8',
    specs: [
      { label: 'Front Windshield', value: 'Acoustic Membrane Laminated Glass' },
      { label: 'Rear Backlight', value: 'Integrated Defroster Heated Tempered Glass' },
      { label: 'Quarter Windows', value: 'Signature BMW Hofmeister Kink Glass' },
      { label: 'Adhesive Specification', value: 'DOW Betaseal High-Modulus Polyurethane' }
    ],
    defectConfig: {
      defectName: 'Windshield Flushness Seam Step Defect',
      defectType: 'A-Pillar Glass Seam Gap',
      paramName: 'Flush Step Error',
      nominal: 0.0,
      defectInitial: 2.2,
      tolerance: 0.5,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 3.0,
      stepSize: 0.1,
      instruction: 'Adjust vacuum suction cup depth to seat glass flush with roof rail.'
    }
  },
  {
    id: 10,
    partKey: 'doors',
    partName: 'Station 10: BMW Lightweight Aluminum Doors & M Aero Mirrors',
    partCode: 'BMW-DRS-M10',
    category: 'Body Line 01 - Aerodynamic Doors & M Twin-Stalk Mirrors',
    material: 'High-Strength Formed Aluminum Alloy & Autoclave Carbon Mirror Shells',
    tool: 'Multi-Axis Door Hinge Nutrunner & Optical Gap/Flush Gauge',
    targetTorque: 35,
    requiresTorque: true,
    tolerance: 'Door Gap & Flushness 0.9 mm (± 0.2 mm)',
    title: 'BMW Lightweight Doors & M Aero Mirrors Installation (35 Nm)',
    instruction: 'Robotically hang driver and passenger frameless lightweight aluminum doors onto A and B pillar hinges. Torque hinge bolts to 35 Nm, attach M aerodynamic twin-stalk side mirrors, and calibrate weatherstrip seals.',
    voiceScript: 'Step 10: Hang the aluminum doors onto pillar hinges. Torque door hinge bolts to 35 Newton meters and verify flush panel seams.',
    translations: {
      en: 'Step 10: Hang the aluminum doors onto pillar hinges. Torque door hinge bolts to 35 Newton meters and verify flush panel seams.',
      ta: 'படி 10: அலுமினிய கதவுகளை ஹிஞ்சில் மாட்டி, 35 நியூட்டன் மீட்டரில் இறுக்கி, எம்-மிரர்களை பொருத்தவும்.',
      ml: 'ഘട്ടം 10: അലുമിനിയം ഡോറുകൾ ഘടിപ്പിച്ച് 35 ന്യൂട്ടൺ മീറ്ററിൽ ബോൾട്ടുകൾ മുറുക്കുക.',
      hi: 'चरण 10: एल्यूमीनियम दरवाजों को हिंज पर लगाएं। 35 न्यूटन मीटर पर बोल्ट कसें और एम-मिरर लगाएं।'
    },
    tip: 'Check that frameless window glass drops 15 mm upon door handle touch for seamless weatherstrip clearance.',
    colorTag: '#6366f1',
    specs: [
      { label: 'Door Construction', value: 'Lightweight Extruded Aluminum Skin' },
      { label: 'Side Mirrors', value: 'M Aerodynamic Twin-Stalk with Upper Winglet' },
      { label: 'Hinge Fasteners', value: '4x M8 Grade 10.9 (35 Nm)' },
      { label: 'Door Gap Standard', value: '0.8 - 1.0 mm Uniform Perimeter' }
    ],
    defectConfig: {
      defectName: 'Door Flushness Seam Over-Flush Defect',
      defectType: 'B-Pillar Door Edge Flushness Error',
      paramName: 'Door Seam Flushness',
      nominal: 0.9,
      defectInitial: 3.4,
      tolerance: 0.3,
      unit: 'mm',
      minVal: 0.5,
      maxVal: 4.0,
      stepSize: 0.1,
      instruction: 'Adjust door hinge striker plate depth to seat door flush at 0.9 mm.'
    }
  },
  {
    id: 11,
    partKey: 'body',
    partName: 'Station 11: BMW M Carbon Body Shell, Power Dome Hood & Kidney Grille',
    partCode: 'BMW-BDY-M11',
    category: 'Exterior Finishing - Aerodynamics, Kidney Grille & Lighting',
    material: 'Autoclave-Cured CFRP, Marina Bay Blue Metallic Clearcoat & Polycarbonate',
    tool: 'Robotic Vacuum Gantry & Optical Laser Panel Gauge',
    targetTorque: 25,
    requiresTorque: true,
    tolerance: 'Panel Flushness & Gap < 0.9 mm',
    title: 'BMW Carbon Body Shell, Power Dome Hood & Kidney Grille (25 Nm)',
    instruction: 'Robotically lower aerodynamic BMW carbon body shell over spaceframe. Latch iconic double kidney grilles with active air flaps, sculpted M power dome hood, laser headlights, front splitter, and rear carbon diffuser.',
    voiceScript: 'Step 11: Lower the aerodynamic BMW carbon body shell with signature kidney grilles and power dome hood onto the chassis.',
    translations: {
      en: 'Step 11: Lower the aerodynamic BMW carbon body shell with signature kidney grilles and power dome hood onto the chassis.',
      ta: 'படி 11: பிஎம்டபிள்யூ கிட்னி கிரில் மற்றும் பவர் டோம் ஹூட் கொண்ட ஏரோடைனமிக் கார்பன் பாடி ஷெல்லை சேசிஸ் மீது இறக்கி பொருத்தவும்.',
      ml: 'ഘട്ടം 11: ബിഎംഡബ്ല്യു കിഡ്നി ഗ്രിൽ ഉള്ള കാർബൺ ബോഡി ഷെൽ ഇറക്കി ഘടിപ്പിക്കുക.',
      hi: 'चरण 11: बीएमडब्ल्यू सिग्नेचर किडनी ग्रिल और पावर डोम हुड वाले कार्बन फाइबर बॉडी शेल को चेसिस पर लगाएं।'
    },
    tip: 'Verify active kidney grille electronic flap stepper motors cycle freely from 0° to 90° before fastener torque.',
    colorTag: '#0066b1',
    specs: [
      { label: 'Aero Package', value: 'BMW M High-Downforce Carbon Package' },
      { label: 'Exterior Paint', value: 'Marina Bay Blue Metallic (High-Gloss Clearcoat)' },
      { label: 'Roof Construction', value: 'CFRP Exposed Carbon Weave with Center Channel' },
      { label: 'Fasteners', value: 'Front Fascia Bolts to 25 Nm' }
    ],
    defectConfig: {
      defectName: 'BMW Carbon Canopy Seam Flushness Gap Error',
      defectType: 'Aerodynamic Monocoque Panel Gap',
      paramName: 'Exterior Seam Gap',
      nominal: 0.9,
      defectInitial: 3.6,
      tolerance: 0.3,
      unit: 'mm',
      minVal: 0.9,
      maxVal: 4.0,
      stepSize: 0.1,
      instruction: 'Adjust gantry vacuum suction height to seat body shell seam within 0.9 mm class-A spec.'
    }
  },
  {
    id: 12,
    partKey: 'wheel',
    partName: 'Station 12: Fluids Vacuum Fill, M-Forged Style 826M Wheels & Dyno Sign-Off',
    partCode: 'BMW-WHL-826M',
    category: 'Final Line - Rolling Chassis, Dyno Test & Master Certification',
    material: 'Forged 6061-T6 Aluminum Alloy & Silica Radial Compound',
    tool: 'Multi-Spindle 5-Lug Smart Torque Wrench & EOL Dynamometer',
    targetTorque: 120,
    requiresTorque: true,
    tolerance: 'Lug Torque 120 Nm (±2.0 Nm)',
    title: 'BMW M-Forged Wheels Fastening (120 Nm) & Master Sign-Off',
    instruction: 'Vacuum-fill brake fluid, engine coolant, and refrigerant. Mount 19-inch front and 20-inch rear BMW M-Forged Style 826M light alloy wheels onto hub studs. Torque all lug nuts in cross-star sequence (1-3-5-2-4) to 120 Nm. Complete master dynamometer roll test and issue official BMW AG Master Quality Certificate.',
    voiceScript: 'Step 12: Mount the BMW M-Forged alloy wheels and performance tires. Torque all wheel lug nuts in a cross star sequence to 120 Newton meters. BMW assembly is 100 percent complete and certified.',
    translations: {
      en: 'Step 12: Mount the BMW M-Forged alloy wheels and performance tires. Torque all wheel lug nuts in a cross star sequence to 120 Newton meters. BMW assembly is 100 percent complete and certified.',
      ta: 'படி 12: பிஎம்டபிள்யூ எம்-அலாய் சக்கரங்களை பொருத்தவும். லக் நட்டுகளை நட்சத்திர அமைப்பில் 120 நியூட்டன் மீட்டரில் இறுக்கவும். பிஎம்டபிள்யூ 12-ஸ்டேஷன் அசெம்பிளி வெற்றிகரமாக முடிந்தது.',
      ml: 'ഘട്ടം 12: ബിഎംഡബ്ല്യു എം-ഫോർജ്ഡ് അലോയ് വീലുകൾ ഘടിപ്പിക്കുക. ലഗ് നട്ടുകൾ 120 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക. ബിഎംഡബ്ല്യു അസംബ്ലി പൂർത്തിയായി.',
      hi: 'चरण 12: बीएमडब्ल्यू एम-फोर्ज्ड अलॉय व्हील्स लगाएं। सभी व्हील नट्स को स्टार पैटर्न में 120 न्यूटन मीटर पर कसें। बीएमडब्ल्यू असेंबली 100% पूरी हुई।'
    },
    tip: 'Always tighten in diagonal cross-star sequence (1-3-5-2-4) to guarantee uniform wheel hub contact.',
    colorTag: '#10b981',
    specs: [
      { label: 'Front M-Wheels', value: '19 x 9.5J Style 826M | 275/35 ZR19' },
      { label: 'Rear M-Wheels', value: '20 x 10.5J Style 826M | 285/30 ZR20' },
      { label: 'Lug Nut Target Torque', value: '120 Nm (Criss-Cross Star Pattern)' },
      { label: 'Certification Status', value: 'BMW AG Dingolfing Quality Passed (ISO 9001 / IATF 16949)' }
    ],
    defectConfig: {
      defectName: 'BMW Forged Wheel Hub Seat Runout & Lug Cant',
      defectType: 'Forged Wheel Rim Eccentricity',
      paramName: 'Rim Seating Angle',
      nominal: 90.0,
      defectInitial: 71.7,
      tolerance: 1.0,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Cross-torque all 5 lug nuts in star pattern to seat wheel flush at 90.0°.'
    }
  }
];'''

target_file = r"d:\new web record file\src\components\assemblyData.js"
with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "export const FULL_CAR_ASSEMBLY_STEPS = ["
end_marker = "export const KNUCKLE_JOINT_STEPS = ["

s_idx = content.find(start_marker)
e_idx = content.find(end_marker)

if s_idx == -1 or e_idx == -1:
    print(f"Error finding markers: s_idx={s_idx}, e_idx={e_idx}")
else:
    new_content = content[:s_idx] + CAR_STEPS_CODE + "\n\n" + content[e_idx:]
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated FULL_CAR_ASSEMBLY_STEPS to 12 Industry 4.0 Stations!")

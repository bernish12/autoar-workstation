// Automotive Disc Brake System Assembly Specification Data
// Industry 4.0 Standard Work Instructions (SWI) - Brembo Tier-1 OEM Corner Module
export const ASSEMBLY_STEPS = [
  {
    id: 1,
    partKey: 'hub',
    partName: 'Station 01: Steering Knuckle & Wheel Hub Bearing Hydraulic Press',
    partCode: 'KNK-BRG-842',
    category: 'Tier-1 Chassis Line - Bearing Assembly Cell',
    material: 'Forged High-Carbon Steel (SAE 1045) & EN-GJS-500',
    tool: '35 kN Servo-Hydraulic Press & Laser Runout Gauge',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Radial Play < 0.02 mm',
    title: 'Wheel Hub Bearing Press-Fit & Preload Verification',
    instruction: 'Load steering knuckle onto automated fixture. Press double-row angular contact bearing into knuckle bore under 35 kN servo-load. Monitor displacement curve to verify zero axial wobble.',
    voiceScript: 'Station 1: Press the double-row wheel bearing into the steering knuckle under 35 kilonewtons. Verify radial play is within 0.02 millimeters.',
    translations: {
      en: 'Station 1: Press the double-row wheel bearing into the steering knuckle under 35 kilonewtons. Verify radial play is within 0.02 millimeters.',
      ta: 'படி 1: ஸ்டீயரிங் நக்கிள் உள் துளையில் வீல் பேரிங்கை 35 கிலோநியூட்டன் அழுத்தத்தில் பொருத்தவும். ரேடியல் இடைவெளி 0.02 மிமீக்குள் இருப்பதை உறுதிசெய்யவும்.',
      ml: 'ഘട്ടം 1: സ്റ്റിയറിംഗ് നക്കിളിലേക്ക് വീൽ ബെയറിംഗ് 35 കിലോന്യൂട്ടൺ പ്രസ്സിൽ ഘടിപ്പിക്കുക.',
      hi: 'चरण 1: स्टीयरिंग नॉकल में व्हील बेयरिंग को 35 किलोन्यूटन प्रेस से फिट करें।'
    },
    tip: 'Ensure the wheel hub spins smoothly with zero axial play before advancing to stud press-fitting.',
    colorTag: '#00f0ff',
    telemetry: {
      stationCode: 'KUKA-CELL-01',
      robotType: 'FANUC M-20iD Press Robot',
      toolBrand: 'Promess 35kN Servo-Electric Press',
      cycleTime: '28s Takt',
      laserRunout: '0.012 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 10, 20, 35]
    },
    specs: [
      { label: 'Servo Press Load', value: '35 kN Continuous' },
      { label: 'Bearing Type', value: 'Double-Row Angular Contact' },
      { label: 'Runout Tolerance', value: '±0.02 mm Radial' },
      { label: 'Hub Center Bore', value: '67.1 mm H7' }
    ],
    defectConfig: {
      defectName: 'Spindle Bearing Radial Play Defect',
      defectType: 'Axial Wobble & Radial Runout',
      paramName: 'Radial Play',
      nominal: 0.02,
      defectInitial: 0.18,
      tolerance: 0.03,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.25,
      stepSize: 0.01,
      instruction: 'Adjust spindle locking nut to preload the tapered bearing within 0.03 mm.'
    }
  },
  {
    id: 2,
    partKey: 'studs',
    partName: 'Station 02: Bearing Retaining Circlip & 5x Wheel Studs Press-Fit',
    partCode: 'STD-CIR-505',
    category: 'Chassis / Hub Fastener Cell',
    material: 'Grade 10.9 High-Tensile Boron Steel',
    tool: 'Multi-Ram Hydraulic Stud Press & Snap-Ring Pneumatic Gripper',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Stud Perpendicularity ±0.1 mm',
    title: 'Snap-Ring Seating & Multi-Stud 40 kN Hydraulic Press',
    instruction: 'Seat the hardened circlip into the knuckle retention groove. Feed 5x M12 wheel studs and press simultaneously into hub flange at 40 kN force. Verify full stud head seating.',
    voiceScript: 'Station 2: Snap the retaining circlip into place and press all 5 wheel studs with 40 kilonewtons hydraulic force.',
    translations: {
      en: 'Station 2: Snap the retaining circlip into place and press all 5 wheel studs with 40 kilonewtons hydraulic force.',
      ta: 'படி 2: பேரிங் லாக் சர்கிளிப்பை பொருத்தி, 5 வீல் ஸ்டட்களையும் 40 கிலோநியூட்டன் விசையில் ஹைட்ராலிக் முறையில் அழுத்தவும்.',
      ml: 'ഘട്ടം 2: സർക്ലിപ്പ് ഉറപ്പിച്ച് 5 വീൽ സ്റ്റഡുകളും ഹൈഡ്രോളിക് ആയി പ്രസ് ചെയ്യുക.',
      hi: 'चरण 2: सर्कलिप लगाएं और 5 व्हील स्टड्स को 40 किलोन्यूटन बल से प्रेस करें।'
    },
    tip: 'Optical sensors verify each of the 5 stud serrations are fully bottomed out against hub rear shoulder.',
    colorTag: '#38bdf8',
    telemetry: {
      stationCode: 'KUKA-CELL-02',
      robotType: '5-Axis Multi-Ram Hydraulic Head',
      toolBrand: 'Tox Pressotechnik 40kN',
      cycleTime: '22s Takt',
      laserRunout: '0.008 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 15, 30, 40]
    },
    specs: [
      { label: 'Stud Pitch Circle (PCD)', value: '5 x 114.3 mm' },
      { label: 'Stud Thread Spec', value: 'M12 x 1.5 Grade 10.9' },
      { label: 'Ram Insertion Load', value: '40 kN Synchronous' },
      { label: 'Circlip Retention Groove', value: 'DIN 472 Retaining' }
    ],
    defectConfig: {
      defectName: 'Wheel Stud Seating Depth Disparity',
      defectType: 'Axial Stud Shoulder Flange Gap',
      paramName: 'Stud Flange Gap',
      nominal: 0.0,
      defectInitial: 1.4,
      tolerance: 0.1,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.0,
      stepSize: 0.1,
      instruction: 'Increase press ram stroke to seat all 5 stud heads flush with hub flange.'
    }
  },
  {
    id: 3,
    partKey: 'abs_sensor',
    partName: 'Station 03: ABS/ESC Magnetic Tone Ring & Hall Sensor Docking',
    partCode: 'ABS-HAL-300',
    category: 'Active Safety & Telematics Line',
    material: 'Neodymium Multipole Magnetic Encoder Ring',
    tool: 'Keyence Optical Air-Gap Micrometer & Torx T25 Driver',
    targetTorque: 8,
    requiresTorque: true,
    tolerance: 'Air Gap 0.5 - 0.8 mm',
    title: 'Wheel Speed Tone Ring Seating & Hall-Effect Sensor Docking',
    instruction: 'Seat magnetic multipole tone ring onto wheel hub inner shoulder. Insert Hall-effect wheel speed sensor into knuckle port, torque M6 fastener to 8 Nm, and verify air gap is within 0.8 mm.',
    voiceScript: 'Station 3: Install the ABS tone ring and dock the Hall-effect speed sensor. Fasten to 8 Newton-meters and verify air gap is under 0.8 millimeters.',
    translations: {
      en: 'Station 3: Install the ABS tone ring and dock the Hall-effect speed sensor. Fasten to 8 Newton-meters and verify air gap is under 0.8 millimeters.',
      ta: 'படி 3: ஏபிஎஸ் டோன் ரிங்கை பொருத்தி, ஹால்-எஃபெக்ட் ஸ்பீட் சென்சாரை 8 நியூட்டன் மீட்டரில் இறுக்கவும். இடைவெளி 0.8 மிமீக்குள் இருப்பதை சரிபார்க்கவும்.',
      ml: 'ഘട്ടം 3: എബിഎസ് സെൻസർ ഘടിപ്പിച്ച് 8 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 3: एबीएस टोन रिंग और हॉल सेंसर लगाएं। 8 न्यूटन मीटर पर कसें और एयर गैप जांचें।'
    },
    tip: 'Optical micrometer interlock blocks the line if tone ring magnetic pole pitch exceeds 48 pole pairs.',
    colorTag: '#60a5fa',
    telemetry: {
      stationCode: 'KUKA-CELL-03',
      robotType: 'Staubli TX2-60 Clean Fastener',
      toolBrand: 'Keyence LK-G5000 Laser + Desoutter DC',
      cycleTime: '18s Takt',
      laserRunout: 'Air Gap: 0.65 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 3, 6, 8]
    },
    specs: [
      { label: 'Sensor Technology', value: 'Dual Hall-Effect Active' },
      { label: 'Target Sensor Air-Gap', value: '0.65 mm (±0.15 mm)' },
      { label: 'Torque Spec', value: '8 Nm (M6 T25 Torx)' },
      { label: 'Magnetic Pole Count', value: '48 Polar Pairs' }
    ],
    defectConfig: {
      defectName: 'ABS Sensor Air-Gap Tolerance Error',
      defectType: 'Sensor Probe Distance Disparity',
      paramName: 'Air Gap',
      nominal: 0.65,
      defectInitial: 1.85,
      tolerance: 0.15,
      unit: 'mm',
      minVal: 0.3,
      maxVal: 2.2,
      stepSize: 0.05,
      instruction: 'Adjust sensor mounting shim to restore 0.65 mm air gap to magnetic encoder.'
    }
  },
  {
    id: 4,
    partKey: 'rotor',
    partName: 'Station 04: 320mm Ventilated Cross-Drilled Rotor Disc Seating',
    partCode: 'BRK-ROT-320',
    category: 'Braking Friction System',
    material: 'High-Thermal Grey Cast Iron (G3000) & Anti-Corrosion Geomet Coat',
    tool: 'T30 Torx Driver & Keyence 360° Laser DTV Scanner',
    targetTorque: 15,
    requiresTorque: true,
    tolerance: 'DTV < 0.008 mm • Lateral Runout < 0.015 mm',
    title: 'Ventilated Rotor Disc Installation & Laser DTV Runout Scan',
    instruction: 'Robotically transfer 320mm ventilated rotor disc onto the 5 hub studs. Fasten T30 countersunk locating screw to 15 Nm. Run automated 360° laser sweep to verify runout < 0.015 mm.',
    voiceScript: 'Station 4: Mount the 320mm ventilated rotor disc. Fasten the locator screw to 15 Newton-meters and scan 360-degree runout.',
    translations: {
      en: 'Station 4: Mount the 320mm ventilated rotor disc. Fasten the locator screw to 15 Newton-meters and scan 360-degree runout.',
      ta: 'படி 4: 320மிமீ வென்டிலேட்டட் ரோட்டார் டிஸ்க்கை ஹப் ஸ்டட்கள் மீது பொருத்தி 15 நியூட்டன் மீட்டரில் இறுக்கவும். லேசர் ஸ்கேன் மூலம் ரன்-அவுட்டை சரிபார்க்கவும்.',
      ml: 'ഘട്ടം 4: 320 എംഎം വെന്റിലേറ്റഡ് റോട്ടർ ഡിസ്ക് ഘടിപ്പിച്ച് 15 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 4: 320 मिमी रोटर डिस्क लगाएं। लोकेटर स्क्रू को 15 न्यूटन मीटर पर कसें और रनआउट स्कैन करें।'
    },
    tip: 'Ensure internal cooling directional vanes match wheel rotation orientation for maximum airflow.',
    colorTag: '#38bdf8',
    telemetry: {
      stationCode: 'KUKA-CELL-04',
      robotType: 'KUKA KR 16 R1610 Handling Robot',
      toolBrand: 'Atlas Copco Tensor STB + Keyence 3D',
      cycleTime: '32s Takt',
      laserRunout: 'Runout: 0.007 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 4, 10, 15]
    },
    specs: [
      { label: 'Outer Diameter', value: '320 mm' },
      { label: 'Nominal Thickness', value: '28.0 mm' },
      { label: 'Disc Thickness Variation (DTV)', value: '< 0.008 mm' },
      { label: 'Fastener Torque', value: '15 Nm (T30 Torx)' }
    ],
    defectConfig: {
      defectName: 'Ventilated Rotor Disc Lateral Runout',
      defectType: 'Rotor Face Wobble & Runout',
      paramName: 'Lateral Runout',
      nominal: 0.015,
      defectInitial: 0.24,
      tolerance: 0.02,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.30,
      stepSize: 0.01,
      instruction: 'Re-seat rotor disc onto hub studs and clean rust scale from contact face.'
    }
  },
  {
    id: 5,
    partKey: 'bracket',
    partName: 'Station 05: Ductile Iron Caliper Anchor Mounting Bracket',
    partCode: 'CLP-BRK-105',
    category: 'Structural Suspension Torque Member',
    material: 'Ductile Nodular Iron (ASTM A536)',
    tool: 'Atlas Copco Wireless DC Angle Nutrunner (M12 Socket)',
    targetTorque: 115,
    requiresTorque: true,
    tolerance: 'Angular Orthogonality ±0.2° • Torque Target ±2%',
    title: 'Caliper Anchor Bracket DC Angle-Nutrunner Torquing (115 Nm)',
    instruction: 'Position the ductile iron torque member over rotor flange onto knuckle boss ears. Thread two Grade 10.9 M12 flange bolts with pre-applied micro-encapsulated threadlocker. Torque to 115 Nm in cross sequence.',
    voiceScript: 'Station 5: Position the caliper anchor bracket and torque the two Grade 10.9 bolts to 115 Newton-meters using the DC angle nutrunner.',
    translations: {
      en: 'Station 5: Position the caliper anchor bracket and torque the two Grade 10.9 bolts to 115 Newton-meters using the DC angle nutrunner.',
      ta: 'படி 5: காலிபர் ஆங்கர் பிராக்கெட்டை நக்கிள் மேல் பொருத்தி, இரண்டு M12 போல்ட்களையும் டிசி நட்ரன்னர் மூலம் 115 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 5: കാലിപ്പർ ആങ്കർ ബ്രാക്കറ്റ് 115 ന്യൂട്ടൺ മീറ്ററിൽ ഡിസി നട്ട്റണ്ണർ ഉപയോഗിച്ച് മുറുക്കുക.',
      hi: 'चरण 5: कैलीपर ब्रैकेट लगाएं और दो M12 बोल्ट को 115 न्यूटन मीटर पर कसें।'
    },
    tip: 'Atlas Copco DC tool aborts if torque-angle curve falls outside 112 to 118 Nm window.',
    colorTag: '#fbbf24',
    telemetry: {
      stationCode: 'KUKA-CELL-05',
      robotType: 'Universal Robots UR10e Cobot Nutrunner',
      toolBrand: 'Atlas Copco Tensor Revo DC Spindle',
      cycleTime: '36s Takt',
      laserRunout: 'Squareness: 89.9° [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 30, 85, 115]
    },
    specs: [
      { label: 'Bolt Thread', value: '2x M12 x 1.5 Grade 10.9' },
      { label: 'Target Torque', value: '115 Nm (Angle Monitored)' },
      { label: 'Mounting Spread', value: '142 mm Precision Datum' },
      { label: 'Threadlocker', value: 'Micro-encapsulated DIN 267-27' }
    ],
    defectConfig: {
      defectName: 'Caliper Bracket Mounting Flange Gap',
      defectType: 'Bracket Flange Seating Gap',
      paramName: 'Seating Gap',
      nominal: 0.0,
      defectInitial: 1.8,
      tolerance: 0.1,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.5,
      stepSize: 0.1,
      instruction: 'Torque bracket bolts equally to eliminate knuckle bracket gap.'
    }
  },
  {
    id: 6,
    partKey: 'shims_clips',
    partName: 'Station 06: Stainless Abutment Clips & Polyurea Synthetic Grease',
    partCode: 'CLP-ABT-06',
    category: 'Noise, Vibration & Harshness (NVH) Sub-Cell',
    material: '301 Full-Hard Stainless Spring Steel & Polyurea Synthetic Grease',
    tool: 'Pneumatic Clip Insertion Tool & Metered Micro-Grease Injector',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Grease Mass: 0.15g ± 0.02g • Zero Contact with Rotor Face',
    title: 'Anti-Rattle Abutment Spring Snapping & Micro-Grease Dosing',
    instruction: 'Snap 4 stainless steel abutment guide spring clips into caliper bracket pad abutment channels. Dispense 0.15g high-temperature polyurea grease strictly onto guide lands to eliminate pad chatter.',
    voiceScript: 'Station 6: Snap the stainless abutment clips into the bracket channels and dispense 0.15 grams of synthetic high-temp grease.',
    translations: {
      en: 'Station 6: Snap the stainless abutment clips into the bracket channels and dispense 0.15 grams of synthetic high-temp grease.',
      ta: 'படி 6: துருப்பிடிக்காத ஸ்பிரிங் கிளிப்புகளை பிராக்கெட் பள்ளங்களில் பொருத்தி, 0.15 கிராம் உயர்-வெப்பநிலை சிந்தெடிக் கிரீஸை துல்லியமாக பூசவும்.',
      ml: 'ഘട്ടം 6: സ്റ്റെയിൻലെസ്സ് അബട്ട്മെന്റ് ക്ലിപ്പുകൾ ഘടിപ്പിച്ച് 0.15 ഗ്രാം ഹൈ-ടെമ്പ് ഗ്രീസ് പുരട്ടുക.',
      hi: 'चरण 6: स्टेनलेस क्लिप्स लगाएं और 0.15 ग्राम हाई-टेम्परेचर ग्रीस लगाएं।'
    },
    tip: 'Poka-Yoke vision camera checks clip spring tension and validates zero grease contamination on rotor friction surface.',
    colorTag: '#a855f7',
    telemetry: {
      stationCode: 'KUKA-CELL-06',
      robotType: 'FANUC LR Mate 200iD Dispenser',
      toolBrand: 'Nordson EFD Micro-Dosing Valve',
      cycleTime: '24s Takt',
      laserRunout: 'Grease Mass: 0.152g [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Clip Material', value: 'AISI 301 Stainless Spring Steel' },
      { label: 'Grease Formulation', value: 'Polyurea Base (-40°C to +260°C)' },
      { label: 'Dispensed Dosing', value: '0.15 g (±0.02 g metered)' },
      { label: 'Vision Inspection', value: 'Cognex In-Sight 2D OCR/Blob' }
    ],
    defectConfig: {
      defectName: 'Abutment Clip Seating Gap Displacement',
      defectType: 'Spring Clip Angular Misalignment',
      paramName: 'Clip Seating Gap',
      nominal: 0.0,
      defectInitial: 1.6,
      tolerance: 0.1,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.5,
      stepSize: 0.1,
      instruction: 'Press abutment clip tangs completely into bracket locating slot.'
    }
  },
  {
    id: 7,
    partKey: 'pads',
    partName: 'Station 07: Carbon-Ceramic Brake Friction Pads & NVH Shims',
    partCode: 'PAD-CRM-922',
    category: 'Friction Material & NVH System',
    material: 'Carbon-Ceramic Matrix with Multi-Layer Vulcanized Shims',
    tool: 'Cobot Gripper & Electronic Pad Wear Sensor Probe',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Pad Free-Slide Clearance 0.15 - 0.30 mm',
    title: 'Ceramic Friction Pads Insertion & Wear Sensor Docking',
    instruction: 'Slide inboard and outboard carbon-ceramic friction pads into the greased abutment clips. Dock electronic two-stage pad wear sensor wire into backing plate slot. Verify smooth slide with zero binding.',
    voiceScript: 'Station 7: Insert the carbon-ceramic brake pads into the bracket clips and connect the electronic wear sensor harness.',
    translations: {
      en: 'Station 7: Insert the carbon-ceramic brake pads into the bracket clips and connect the electronic wear sensor harness.',
      ta: 'படி 7: கார்பன்-செராமிக் பிரேக் பேட்களை கிளிப்களில் செலுத்தி, எலக்ட்ரானிக் பேட் தேய்மான சென்சாரை இணைக்கவும்.',
      ml: 'ഘട്ടം 7: കാർബൺ-സെറാമിക് ബ്രേക്ക് പാഡുകൾ ഘടിപ്പിച്ച് വെയർ സെൻസർ ബന്ധിപ്പിക്കുക.',
      hi: 'चरण 7: कार्बन-सिरेमिक ब्रेक पैड्स लगाएं और वेयर सेंसर हार्नेस कनेक्ट करें।'
    },
    tip: 'Ensure the multi-layer rubberized stainless shims face outward towards the caliper pistons.',
    colorTag: '#f97316',
    telemetry: {
      stationCode: 'KUKA-CELL-07',
      robotType: 'Universal Robots UR5e Pad Inserter',
      toolBrand: 'Schunk Co-act Gripper + Fluke Continuity',
      cycleTime: '26s Takt',
      laserRunout: 'Slide Drag: 0.18 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Friction Material', value: 'Carbon-Ceramic Semi-Metallic' },
      { label: 'Pad Thickness (New)', value: '18.5 mm (Lining + Plate)' },
      { label: 'Pad Wear Limit', value: '3.0 mm' },
      { label: 'Wear Sensor Connector', value: 'Gold-Plated Sealed Delphi 2-Pin' }
    ],
    defectConfig: {
      defectName: 'Ceramic Pad Slide Clearance Binding',
      defectType: 'Pad Abutment Jam Error',
      paramName: 'Slide Clearance',
      nominal: 0.22,
      defectInitial: 0.01,
      tolerance: 0.08,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.40,
      stepSize: 0.02,
      instruction: 'Relieve abutment clip tension to allow smooth 0.22 mm pad free-slide.'
    }
  },
  {
    id: 8,
    partKey: 'caliper',
    partName: 'Station 08: Brembo Monobloc 4-Piston Caliper Body & Guide Pins',
    partCode: 'CLP-RED-440',
    category: 'Hydraulic Actuation Assembly',
    material: 'Die-Cast Aluminum-Silicon Alloy (AlSi7Mg) Red Powder Coat',
    tool: 'Digital DC Nutrunner & Caliper Guide Sleeve Arbor',
    targetTorque: 35,
    requiresTorque: true,
    tolerance: 'Guide Pin Perpendicularity 90.0° ± 0.5°',
    title: 'Monobloc Caliper Fitment & Guide Slider Pin Torquing (35 Nm)',
    instruction: 'Lower red monobloc caliper body over the brake pads onto guide pin sleeves. Insert two stainless guide slider pins and torque to 35 Nm with angle yield confirmation.',
    voiceScript: 'Station 8: Mount the red Brembo monobloc caliper over the pads and torque the guide slider pins to 35 Newton-meters.',
    translations: {
      en: 'Station 8: Mount the red Brembo monobloc caliper over the pads and torque the guide slider pins to 35 Newton-meters.',
      ta: 'படி 8: ரெட் காலிப்பர் பாடியை பேட்களின் மேல் இறக்கி, கைடு ஸ்லைடர் பின்களை 35 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 8: റെഡ് കാലിപ്പർ ബോഡി ഘടിപ്പിച്ച് ഗൈഡ് പിന്നുകൾ 35 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 8: लाल कैलीपर बॉडी लगाएं और गाइड पिन को 35 न्यूटन मीटर पर कसें।'
    },
    tip: 'Verify EPDM piston dust boots are untorn and guide slider rubber bushings are properly seated.',
    colorTag: '#f43f5e',
    telemetry: {
      stationCode: 'KUKA-CELL-08',
      robotType: 'KUKA KR 10 R1100 Dual-Arm Caliper Cell',
      toolBrand: 'Atlas Copco Tensor STB 35Nm DC',
      cycleTime: '38s Takt',
      laserRunout: 'Slider Angle: 90.1° [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 12, 28, 35]
    },
    specs: [
      { label: 'Piston Configuration', value: 'Quad Opposed (4x 40mm) Phenolic' },
      { label: 'Caliper Monobloc Casting', value: 'AlSi7Mg Heat-Treated T6' },
      { label: 'Guide Pin Torque', value: '35 Nm (M9 Hex Drive)' },
      { label: 'Slider Bushing Material', value: 'EPDM High-Temperature Rubber' }
    ],
    defectConfig: {
      defectName: 'Guide Slider Pin Angular Displacement',
      defectType: 'Caliper Slider Pin Binding',
      paramName: 'Slide Pin Angle',
      nominal: 90.0,
      defectInitial: 71.7,
      tolerance: 1.5,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Re-align guide pin bushing sleeve to 90.0° factory tolerance.'
    }
  },
  {
    id: 9,
    partKey: 'banjo_line',
    partName: 'Station 09: Hydraulic Banjo Line & Dual Annealed Copper Washers',
    partCode: 'HYD-BNJ-102',
    category: 'Hydraulic Fluid Circuit',
    material: 'Braided Stainless Steel Fluid Hose & Annealed Soft Copper Washers',
    tool: 'Torque Wrench & Optical Washer Orientation Camera',
    targetTorque: 28,
    requiresTorque: true,
    tolerance: 'Washer Crush Compression 0.18 mm',
    title: 'Banjo Fluid Fitting Assembly & Bleeder Valve Insertion',
    instruction: 'Position braided brake hose banjo fitting between two fresh annealed copper crush washers. Thread M10 banjo bolt into caliper inlet port and torque to 28 Nm. Install bleeder valve screw to 12 Nm.',
    voiceScript: 'Station 9: Connect the hydraulic brake hose banjo bolt with dual copper crush washers and torque to 28 Newton-meters.',
    translations: {
      en: 'Station 9: Connect the hydraulic brake hose banjo bolt with dual copper crush washers and torque to 28 Newton-meters.',
      ta: 'படி 9: பிரேக் ஹோஸ் பேஞ்சோ போல்ட்டை இரண்டு தாமிர வாஷர்களுடன் இணைத்து 28 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 9: ബ്രേക്ക് ഹോസ് ബാൻജോ ബോൾട്ട് 28 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 9: हाइड्रोलिक ब्रेक नली बैंजो बोल्ट को 28 न्यूटन मीटर पर कसें।'
    },
    tip: 'Never reuse copper crush washers; freshly annealed soft copper provides an impermeable hydraulic seal.',
    colorTag: '#ec4899',
    telemetry: {
      stationCode: 'KUKA-CELL-09',
      robotType: 'Staubli Fastening Cell 09',
      toolBrand: 'Desoutter Delta Torque 28Nm',
      cycleTime: '25s Takt',
      laserRunout: 'Washer Compression: 0.18 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 10, 22, 28]
    },
    specs: [
      { label: 'Banjo Bolt Thread', value: 'M10 x 1.0 Pitch Grade 8.8' },
      { label: 'Washer Material', value: 'Annealed High-Purity Copper CW024A' },
      { label: 'Banjo Torque Spec', value: '28 Nm' },
      { label: 'Bleeder Screw Torque', value: '12 Nm (with EPDM cap)' }
    ],
    defectConfig: {
      defectName: 'Banjo Bolt Copper Washer Crush Defect',
      defectType: 'Crush Washer Cocking & Tilt',
      paramName: 'Washer Tilt Angle',
      nominal: 90.0,
      defectInitial: 78.4,
      tolerance: 1.0,
      unit: '°',
      minVal: 75.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Square copper crush washers evenly before tightening banjo bolt.'
    }
  },
  {
    id: 10,
    partKey: 'qc_drag',
    partName: 'Station 10: 160 Bar Helium Leak Decay & Dynamic Drag Torque Dyno',
    partCode: 'EOL-BRK-990',
    category: 'End-of-Line Quality Assurance & IATF 16949 Certification',
    material: 'Fully Certified Brake Corner Sub-Assembly',
    tool: 'Vacuum Helium Chamber & Automated Dyno Drag Sensor',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Helium Leak < 1.0x10^-4 mbar·L/s • Drag Torque < 1.2 Nm',
    title: '160 Bar Pressure Holding, Drag Torque & Laser QR Etching',
    instruction: 'Chamber leak test caliper at 160 Bar pressure with zero decay. Spin hub at 200 RPM to verify unpressurized drag torque is below 1.2 Nm. Laser etch 2D DataMatrix QR code with full MES traceability.',
    voiceScript: 'Station 10: Final Quality Station. Caliper passes 160 Bar helium leak test and drag torque dyno. IATF 16949 certificate issued.',
    translations: {
      en: 'Station 10: Final Quality Station. Caliper passes 160 Bar helium leak test and drag torque dyno. IATF 16949 certificate issued.',
      ta: 'படி 10: இறுதி தரக் கட்டுப்பாடு. 160 பார் பிரஷர் லீக் சோதனை மற்றும் டிராக் டார்க் சோதனை வெற்றிகரமாக முடிந்தது. ஐஏடிஎஃப் சான்றிதழ் வழங்கப்பட்டது.',
      ml: 'ഘട്ടം 10: അവസാന ക്വാളിറ്റി ടെസ്റ്റ്. 160 ബാർ ലീക്ക് ടെസ്റ്റും ഡ്രാഗ് ടോർക്ക് ടെസ്റ്റും പൂർത്തിയായി.',
      hi: 'चरण 10: अंतिम गुणवत्ता नियंत्रण। 160 बार हीलियम लीक टेस्ट और ड्रैग टॉर्क टेस्ट सफलतापूर्वक पास हुआ।'
    },
    tip: 'Component passed all 10 Tier-1 stations with zero defects; ready for robot marriage onto vehicle chassis line.',
    colorTag: '#10b981',
    telemetry: {
      stationCode: 'KUKA-CELL-10 (EOL)',
      robotType: 'Automated Dyno & Laser Marking Cell',
      toolBrand: 'Pfeiffer Helium Vacuum + Trumpf TruMark',
      cycleTime: '45s Takt',
      laserRunout: 'Drag Torque: 0.85 Nm [PASS]',
      heliumDecay: '160 Bar (0.00 Bar/s) [PASS]',
      torqueCurve: [0, 40, 100, 160]
    },
    specs: [
      { label: 'Leak Chamber Pressure', value: '160 Bar (2,320 PSI) Helium' },
      { label: 'Unloaded Drag Torque', value: '0.85 Nm (< 1.2 Nm Target)' },
      { label: 'MES Traceability', value: 'Laser 2D DataMatrix QR Code' },
      { label: 'IATF 16949 Status', value: '100% PASSED (Zero Defect)' }
    ],
    defectConfig: {
      defectName: 'Residual Pad Drag Torque Error',
      defectType: 'Excessive Pad Pre-contact Friction',
      paramName: 'Drag Torque',
      nominal: 0.8,
      defectInitial: 3.4,
      tolerance: 0.4,
      unit: 'Nm',
      minVal: 0.2,
      maxVal: 4.0,
      stepSize: 0.1,
      instruction: 'Cycle caliper hydraulic pistons to seat square in bores and relieve drag torque.'
    }
  }
];

// Automotive Single-Plate Dry Clutch & Pressure Plate Assembly Data
// Industry 4.0 Standard Work Instructions (SWI) - Schaeffler LuK SAC Tier-1 OEM Standard
export const CLUTCH_ASSEMBLY_STEPS = [
  {
    id: 1,
    partKey: 'pilot_bearing',
    partName: 'Station 01: Engine Crankshaft Output Flange & Needle Pilot Bearing',
    partCode: 'PLT-BRG-200',
    category: 'Crankshaft Interface & Pilot Bearing Cell',
    material: 'Case-Hardened Chromium Steel (100Cr6) & Lithium Grease',
    tool: '12 kN Servo Press & Laser Depth Gauge',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Press Depth Flush ±0.1 mm',
    title: 'Needle Pilot Bearing Hydraulic Press-Fit into Crankshaft Bore',
    instruction: 'Inspect engine crankshaft pilot recess for burrs. Apply light film of high-temperature synthetic grease. Press needle pilot bearing into crank bore under 12 kN servo-force flush with datum face.',
    voiceScript: 'Station 1: Press the needle roller pilot bearing into the crankshaft bore with 12 kilonewtons servo-press force.',
    translations: {
      en: 'Station 1: Press the needle roller pilot bearing into the crankshaft bore with 12 kilonewtons servo-press force.',
      ta: 'படி 1: கிரான்க்ஷாஃப்ட் துளையில் நீடில் பைலட் பேரிங்கை 12 கிலோநியூட்டன் அழுத்தத்தில் பொருத்தவும்.',
      ml: 'ഘട്ടം 1: ക്രാങ്ക് ഷാഫ്റ്റിലേക്ക് പൈലറ്റ് ബെയറിംഗ് 12 കിലോന്യൂട്ടൺ പ്രസ്സിൽ ഘടിപ്പിക്കുക.',
      hi: 'चरण 1: क्रैंकशाफ्ट बोर में पायलट बेयरिंग को 12 किलोन्यूटन सर्वो-प्रेस से लगाएं।'
    },
    tip: 'Laser depth gauge ensures the bearing is pressed dead-flush without cocking or needle damage.',
    colorTag: '#00f0ff',
    telemetry: {
      stationCode: 'LUK-CELL-01',
      robotType: 'FANUC M-10iD Insertion Robot',
      toolBrand: 'Kistler 12kN Servo-Press NC',
      cycleTime: '22s Takt',
      laserRunout: 'Depth: 0.04 mm flush [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 4, 8, 12]
    },
    specs: [
      { label: 'Bearing Type', value: 'Drawn Cup Needle Roller (Sealed)' },
      { label: 'Shaft Outer Diameter', value: '20.0 mm H6' },
      { label: 'Insertion Force', value: '12 kN Peak Servo' },
      { label: 'Grease Pre-fill', value: 'Lithium Complex NLGI 2 (0.4g)' }
    ],
    defectConfig: {
      defectName: 'Needle Pilot Bearing Seating Cocking',
      defectType: 'Pilot Bearing Angular Misalignment',
      paramName: 'Bore Angle',
      nominal: 90.0,
      defectInitial: 77.2,
      tolerance: 1.0,
      unit: '°',
      minVal: 72.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Square pilot bearing driver arbor perpendicular to crankshaft centerline.'
    }
  },
  {
    id: 2,
    partKey: 'flywheel',
    partName: 'Station 02: Dual-Mass Flywheel (DMF) Primary Mass & Starter Ring Runout',
    partCode: 'DMF-MCH-520',
    category: 'Primary Drive & Rotational Inertia Line',
    material: 'Ductile Cast Iron (EN-GJS-400-15) & Induction-Hardened Ring Gear',
    tool: 'Surface Micrometer & Keyence Optical Runout Sensor',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Friction Face Runout < 0.05 mm • Backlash 8° - 12°',
    title: 'Dual-Mass Flywheel Friction Surface Inspection & Backlash Check',
    instruction: 'Mount Dual-Mass Flywheel (DMF) onto crankshaft pilot hub. Verify secondary mass rotational arc spring free-play backlash is within 8° to 12°. Laser scan friction face runout (< 0.05 mm).',
    voiceScript: 'Station 2: Mount the Dual-Mass Flywheel. Verify arc spring free-play backlash is between 8 and 12 degrees and scan friction face runout.',
    translations: {
      en: 'Station 2: Mount the Dual-Mass Flywheel. Verify arc spring free-play backlash is between 8 and 12 degrees and scan friction face runout.',
      ta: 'படி 2: டூயல்-மாஸ் ஃபிளைவீலை பொருத்தவும். ஆர்க் ஸ்பிரிங் பேக்லாஷ் 8 முதல் 12 டிகிரிக்குள் உள்ளதா என சரிபார்த்து ரன்-அவுட்டை அளவிடவும்.',
      ml: 'ഘട്ടം 2: ഡ്യുവൽ മാസ് ഫ്ലൈവീൽ ഘടിപ്പിക്കുക. ആർക്ക് സ്പ്രിംഗ് ബാക്ക്ലാഷ് പരിശോധിക്കുക.',
      hi: 'चरण 2: डुअल-मास फ्लाईव्हील लगाएं। बैकलाश 8 से 12 डिग्री के बीच जांचें और रनआउट स्कैन करें।'
    },
    tip: 'Degrease friction face with solvent; any grease residue on DMF causes immediate clutch judder.',
    colorTag: '#38bdf8',
    telemetry: {
      stationCode: 'LUK-CELL-02',
      robotType: 'KUKA KR 30-3 Heavy Handler',
      toolBrand: 'Keyence Optical + Renishaw Dial CMM',
      cycleTime: '30s Takt',
      laserRunout: 'Runout: 0.024 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Flywheel Architecture', value: 'Schaeffler Dual-Mass (DMF)' },
      { label: 'Outside Diameter', value: '280 mm Precision Ground' },
      { label: 'Starter Ring Teeth', value: '110 Induction-Hardened' },
      { label: 'Permissible Runout', value: '< 0.05 mm Max' }
    ],
    defectConfig: {
      defectName: 'Flywheel Friction Face Lateral Runout',
      defectType: 'Flywheel Surface Runout',
      paramName: 'Friction Face Runout',
      nominal: 0.03,
      defectInitial: 0.32,
      tolerance: 0.05,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.40,
      stepSize: 0.01,
      instruction: 'Re-seat DMF onto crankshaft pilot shoulder to eliminate face runout.'
    }
  },
  {
    id: 3,
    partKey: 'crank_bolts',
    partName: 'Station 03: DMF to Crankshaft Two-Stage Angle Stretch Bolting',
    partCode: 'CRK-BLT-808',
    category: 'High-Torque Powertrain Bolting Cell',
    material: 'Grade 12.9 High-Tensile Micro-Alloyed Stretch Steel',
    tool: 'Multi-Spindle Synchronized DC Angle Nutrunner',
    targetTorque: 60,
    requiresTorque: true,
    tolerance: 'Stage 1: 60 Nm ± 2 Nm • Stage 2: +90° Angle Turn',
    title: 'Flywheel to Crankshaft Multi-Spindle Torque-Angle Fastening',
    instruction: 'Robotically feed 8x Grade 12.9 M10 stretch bolts. Synchronized multi-spindle DC nutrunner tightens diagonally: Stage 1 snug torque to 60 Nm, followed by Stage 2 precise 90° angle yield turn.',
    voiceScript: 'Station 3: Fasten the 8 flywheel crankshaft bolts in two stages: 60 Newton-meters torque followed by a 90-degree angle turn.',
    translations: {
      en: 'Station 3: Fasten the 8 flywheel crankshaft bolts in two stages: 60 Newton-meters torque followed by a 90-degree angle turn.',
      ta: 'படி 3: 8 கிரான்க்ஷாஃப்ட் போல்ட்களையும் இரண்டு நிலைகளில் இறுக்கவும்: முதலில் 60 நியூட்டன் மீட்டர், பின்னர் 90 டிகிரி ஆங்கிள் டர்ன்.',
      ml: 'ഘട്ടം 3: 8 ഫ്ലൈവീൽ ബോൾട്ടുകൾ 60 ന്യൂട്ടൺ മീറ്ററും തുടർന്ന് 90 ഡിഗ്രി ആംഗിളും മുറുക്കുക.',
      hi: 'चरण 3: फ्लाईव्हील के 8 बोल्ट्स को दो चरणों में कसें: 60 न्यूटन मीटर टॉर्क और फिर 90 डिग्री एंगल टर्न।'
    },
    tip: 'Angle-yield stretch bolts ensure permanent clamp force under extreme engine torsional oscillations.',
    colorTag: '#60a5fa',
    telemetry: {
      stationCode: 'LUK-CELL-03',
      robotType: '8-Spindle Multi-Head DC Gantry',
      toolBrand: 'Atlas Copco Power Focus 6000',
      cycleTime: '35s Takt',
      laserRunout: 'Angle Yield: 90.2° [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 20, 45, 60]
    },
    specs: [
      { label: 'Bolt Spec', value: '8x M10 x 1.0 Grade 12.9 Stretch' },
      { label: 'Stage 1 Snug Torque', value: '60 Nm (Criss-Cross)' },
      { label: 'Stage 2 Angle Yield', value: '+90° (±2° window)' },
      { label: 'Pre-applied Sealant', value: 'Loctite 204 Dri-Loc' }
    ],
    defectConfig: {
      defectName: 'Crank Bolt Angle Yield Discrepancy',
      defectType: 'Insufficient Angle-Controlled Turn',
      paramName: 'Yield Angle',
      nominal: 90.0,
      defectInitial: 62.0,
      tolerance: 3.0,
      unit: '°',
      minVal: 50.0,
      maxVal: 100.0,
      stepSize: 1.0,
      instruction: 'Complete the +90° angle turn to achieve full yield tension on crank stretch bolts.'
    }
  },
  {
    id: 4,
    partKey: 'spline_grease',
    partName: 'Station 04: Transmission Input Spline Cleaning & MoS2 Anti-Fretting Paste',
    partCode: 'SPL-MOS-04',
    category: 'Tribological Lubrication Sub-Cell',
    material: 'Molybdenum Disulphide (MoS2) Micro-Particle Synthetic Paste',
    tool: 'Robotic Automated Metered Spline Brush Nozzle',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Dispensed Mass: 0.15 g ± 0.03 g (Zero Excess)',
    title: 'Transmission Input Splines MoS2 Micro-Dosing Application',
    instruction: 'Brush 0.15g MoS2 synthetic anti-fretting paste onto the 23-tooth splines. Clean off all excess paste with vacuum wipe to prevent centrifugal contamination onto friction facings.',
    voiceScript: 'Station 4: Apply 0.15 grams of MoS2 anti-fretting paste to the transmission input splines and wipe off all excess.',
    translations: {
      en: 'Station 4: Apply 0.15 grams of MoS2 anti-fretting paste to the transmission input splines and wipe off all excess.',
      ta: 'படி 4: டிரான்ஸ்மிஷன் இன்புட் ஸ்ப்லைன்களில் 0.15 கிராம் MoS2 பேஸ்ட்டை பூசி, அதிகப்படியான பேஸ்ட்டை துடைக்கவும்.',
      ml: 'ഘട്ടം 4: ഇൻപുട്ട് സ്പ്ലൈനുകളിൽ 0.15 ഗ്രാം MoS2 പേസ്റ്റ് പുരട്ടുക.',
      hi: 'चरण 4: इनपुट स्प्लाइन्स पर 0.15 ग्राम MoS2 एंटी-फ्रेटिंग पेस्ट लगाएं और अतिरिक्त पेस्ट पोंछ लें।'
    },
    tip: 'Excess grease thrown off by centrifugal force onto the friction disc will destroy clutch grip.',
    colorTag: '#fbbf24',
    telemetry: {
      stationCode: 'LUK-CELL-04',
      robotType: 'Staubli TS60 Scara Dispenser',
      toolBrand: 'Walther Pilot Micro-Grease Injector',
      cycleTime: '18s Takt',
      laserRunout: 'Paste Mass: 0.148g [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Lubricant Base', value: 'High-Load MoS2 (Castrol Olista)' },
      { label: 'Target Mass', value: '0.15 g Precision Micro-Dose' },
      { label: 'Spline Teeth', value: '23 Teeth DIN 5480 Profile' },
      { label: 'Poka-Yoke Vision', value: 'UV Fluorescent Dye Inspection' }
    ],
    defectConfig: {
      defectName: 'Spline Grease Centrifugal Overdose',
      defectType: 'Excess Lubricant Mass Hazard',
      paramName: 'Grease Mass',
      nominal: 0.15,
      defectInitial: 0.85,
      tolerance: 0.05,
      unit: 'g',
      minVal: 0.05,
      maxVal: 1.0,
      stepSize: 0.05,
      instruction: 'Vacuum wipe excess spline paste down to 0.15g factory standard.'
    }
  },
  {
    id: 5,
    partKey: 'friction_disc',
    partName: 'Station 05: Organic Friction Disc Poka-Yoke Orientation Check',
    partCode: 'FDS-ORG-280',
    category: 'Kinetic Drive Friction Core',
    material: 'Non-Asbestos Ceramic-Organic Composite & Chromoly Springs',
    tool: 'Cognex AI Vision Orientation Camera & Pneumatic Mandrel',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Spline Axial Runout < 0.2 mm • Zero Inversion',
    title: 'Friction Disc Orientation Verification ("Gearbox Side") & Placement',
    instruction: 'Robotically transfer 280mm friction disc. Vision sensor verifies "Getriebeseite / Gearbox Side" stamping faces transmission outward. Place disc against flywheel friction face.',
    voiceScript: 'Station 5: Verify the friction disc gearbox side orientation using the optical camera and position the disc against the flywheel.',
    translations: {
      en: 'Station 5: Verify the friction disc gearbox side orientation using the optical camera and position the disc against the flywheel.',
      ta: 'படி 5: உராய்வு டிஸ்க்கின் கியர்பாக்ஸ் திசையை ஆப்டிகல் கேமரா மூலம் உறுதிசெய்து, ஃபிளைவீலுக்கு எதிராக பொருத்தவும்.',
      ml: 'ഘട്ടം 5: ഫ്രിക്ഷൻ ഡിസ്കിന്റെ ഗിയർബോക്സ് വശം പരിശോധിച്ച് ഫ്ലൈവീലിൽ ഘടിപ്പിക്കുക.',
      hi: 'चरण 5: फ्रिक्शन डिस्क के गियरबॉक्स साइड ओरिएंटेशन की जांच करें और इसे फ्लाईव्हील के सामने रखें।'
    },
    tip: 'Installing the friction disc backward causes catastrophic mechanical lockup and destroys the clutch hub.',
    colorTag: '#f59e0b',
    telemetry: {
      stationCode: 'LUK-CELL-05',
      robotType: 'Universal Robots UR10e with Vacuum Suction',
      toolBrand: 'Cognex In-Sight 8405 Vision Camera',
      cycleTime: '24s Takt',
      laserRunout: 'Orientation: 100% CONFIRMED [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Lining Outer Diameter', value: '280 mm Organic Facing' },
      { label: 'Torsion Dampers', value: '6 Encapsulated Chromoly Coils' },
      { label: 'Spline Profile', value: '23 Splines x 1.0 Mod' },
      { label: 'Thickness (Compressed)', value: '8.4 mm (±0.2 mm)' }
    ],
    defectConfig: {
      defectName: 'Friction Disc Spline Hub Eccentricity',
      defectType: 'Spline Hub Off-Center',
      paramName: 'Hub Eccentricity',
      nominal: 0.0,
      defectInitial: 2.4,
      tolerance: 0.2,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 3.0,
      stepSize: 0.1,
      instruction: 'Center clutch disc using pilot alignment tool before tightening pressure plate.'
    }
  },
  {
    id: 6,
    partKey: 'mandrel_lock',
    partName: 'Station 06: Pneumatic Centering Mandrel Coaxial Locking (< 0.05 mm)',
    partCode: 'MND-CTR-106',
    category: 'High-Precision Concentric Alignment Cell',
    material: 'Hardened Tool Steel Mandrel (HRC 62)',
    tool: 'Pneumatic Expanding Alignment Arbor & Laser Concentricity Gauge',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Hub-to-Crankshaft Concentricity < 0.05 mm',
    title: 'Centering Arbor Mandrel Coaxial Alignment & Pilot Insertion',
    instruction: 'Advance expanding pneumatic centering arbor through the clutch disc spline hub into the crankshaft needle pilot bearing. Expand collet to lock friction disc perfectly dead-center (< 0.05 mm coaxiality).',
    voiceScript: 'Station 6: Insert the pneumatic alignment mandrel into the pilot bearing and expand collet to center the clutch disc within 0.05 millimeters.',
    translations: {
      en: 'Station 6: Insert the pneumatic alignment mandrel into the pilot bearing and expand collet to center the clutch disc within 0.05 millimeters.',
      ta: 'படி 6: அலைன்மென்ட் மாண்ட்ரலை பைலட் பேரிங்கில் செலுத்தி, கிளட்ச் டிஸ்க்கை 0.05 மிமீ துல்லியத்தில் மையப்படுத்தவும்.',
      ml: 'ഘട്ടം 6: അലൈൻമെന്റ് മാൻഡ്രൽ ഉപയോഗിച്ച് ക്ലച്ച് ഡിസ്ക് 0.05 എംഎം കൃത്യതയിൽ കേന്ദ്രീകരിക്കുക.',
      hi: 'चरण 6: अलाइनमेंट मैंड्रेल को पायलट बेयरिंग में डालें और क्लच डिस्क को 0.05 मिमी के भीतर केंद्रित करें।'
    },
    tip: 'Disc must remain clamped dead-center by the arbor until all 6 cover bolts are fully torqued.',
    colorTag: '#a855f7',
    telemetry: {
      stationCode: 'LUK-CELL-06',
      robotType: 'Staubli TX2-90 Precision Manipulator',
      toolBrand: 'Suhner Pneumatic Expanding Mandrel',
      cycleTime: '20s Takt',
      laserRunout: 'Concentricity: 0.018 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Mandrel Pilot Spigot', value: '20.00 mm Precision Ground (h6)' },
      { label: 'Expansion Mechanism', value: 'Pneumatic 6-Segment Collet' },
      { label: 'Target Concentricity', value: '< 0.05 mm Coaxial' },
      { label: 'Clamping Pressure', value: '6 Bar Air Supply' }
    ],
    defectConfig: {
      defectName: 'Centering Mandrel Radial Runout',
      defectType: 'Arbor Center Displacement',
      paramName: 'Radial Runout',
      nominal: 0.02,
      defectInitial: 0.45,
      tolerance: 0.05,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.60,
      stepSize: 0.02,
      instruction: 'Adjust centering arbor fixture until radial runout is within 0.05 mm.'
    }
  },
  {
    id: 7,
    partKey: 'pressure_plate',
    partName: 'Station 07: Pearlitic Cast Iron Pressure Plate Clamping Ring & Drive Straps',
    partCode: 'PRP-CAS-280',
    category: 'Clamping Force Transmission',
    material: 'High-Thermal Pearlitic Grey Iron & Spring Steel Drive Straps',
    tool: 'Hydraulic Riveting Press & Dial Dynamic Balance Rig',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Fulcrum Flatness < 0.1 mm • Balance < 15 g·mm',
    title: 'Cast Iron Pressure Plate Flange Alignment & Strap Riveting',
    instruction: 'Position cast iron friction ring over centered clutch disc onto flywheel locating dowels. Fasten triple tangential spring-steel drive straps using high-tonnage hydraulic riveting press. Verify unbalance < 15 g·mm.',
    voiceScript: 'Station 7: Align the cast iron pressure plate onto the flywheel dowel pins and rivet the tangential drive straps.',
    translations: {
      en: 'Station 7: Align the cast iron pressure plate onto the flywheel dowel pins and rivet the tangential drive straps.',
      ta: 'படி 7: பிரஷர் பிளேட்டை ஃபிளைவீல் டவல் பின்களில் பொருத்தி, டிரைவ் ஸ்ட்ராப்களை ஹைட்ராலிக் முறையில் ரிவெட் செய்யவும்.',
      ml: 'ഘട്ടം 7: പ്രഷർ പ്ലേറ്റ് ഫ്ലൈവീൽ പിന്നുകളിൽ ഘടിപ്പിച്ച് ഡ്രൈവ് സ്ട്രാപ്പുകൾ റിവറ്റ് ചെയ്യുക.',
      hi: 'चरण 7: प्रेशर प्लेट को फ्लाईव्हील पिन पर रखें और ड्राइव स्ट्रैप्स को रिवेट करें।'
    },
    tip: 'Ensure the ground pearlitic friction face sits completely flush against the newly centered friction disc.',
    colorTag: '#ec4899',
    telemetry: {
      stationCode: 'LUK-CELL-07',
      robotType: 'FANUC M-20iD Heavy Gripper',
      toolBrand: 'BalTec Radial Riveting Machine',
      cycleTime: '34s Takt',
      laserRunout: 'Dynamic Unbalance: 8 g·mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Clamping Load', value: '7,200 N Nominal' },
      { label: 'Thermal Mass Capacity', value: '380 kJ Heat Sink' },
      { label: 'Drive Strap Material', value: 'Multi-Leaf High-Tensile 50CrV4' },
      { label: 'Dynamic Balance Target', value: '< 15 g·mm Residual' }
    ],
    defectConfig: {
      defectName: 'Cast Pressure Plate Fulcrum Cocking',
      defectType: 'Pressure Plate Angular Tilt',
      paramName: 'Fulcrum Angle',
      nominal: 90.0,
      defectInitial: 81.2,
      tolerance: 1.0,
      unit: '°',
      minVal: 78.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Evenly tighten pressure plate drive straps to restore 90.0° fulcrum flatness.'
    }
  },
  {
    id: 8,
    partKey: 'diaphragm_spring',
    partName: 'Station 08: Belleville Diaphragm Spring Fulcrum Wire Rings Seating',
    partCode: 'DIA-BLV-400',
    category: 'Linear Spring Clamping Mechanism',
    material: '51CrV4 High-Yield Chrome-Vanadium Spring Steel',
    tool: 'Hydraulic Fulcrum Ring Press & Keyence Multi-Laser Finger Profiler',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Finger Height Uniformity ±0.2 mm',
    title: 'Diaphragm Spring Fulcrum Seat Positioning & Finger Co-planarity Check',
    instruction: 'Seat conical Belleville spring into circular wire fulcrum rings. Multi-laser sensor sweeps all 18 release fingers to verify tip heights are co-planar within 0.2 mm (eliminates clutch chatter and release drag).',
    voiceScript: 'Station 8: Seat the diaphragm spring into fulcrum guides and verify all 18 release fingers are co-planar within 0.2 millimeters.',
    translations: {
      en: 'Station 8: Seat the diaphragm spring into fulcrum guides and verify all 18 release fingers are co-planar within 0.2 millimeters.',
      ta: 'படி 8: டயாபிராம் ஸ்பிரிங்கை ஃபுல்க்ரம் வழிகாட்டிகளில் பொருத்தி, 18 ஃபிங்கர்களும் 0.2 மிமீக்குள் ஒரே சீரான உயரத்தில் இருப்பதை உறுதிசெய்யவும்.',
      ml: 'ഘട്ടം 8: ഡയഫ്രം സ്പ്രിംഗ് ഘടിപ്പിച്ച് 18 റിലീസ് ഫിംഗറുകളുടെയും ഉയരം പരിശോധിക്കുക.',
      hi: 'चरण 8: डायाफ्राम स्प्रिंग को रिंग गाइड में बैठाएं और सभी 18 रिलीज फिंगर्स की एकसमान ऊंचाई 0.2 मिमी के भीतर सत्यापित करें।'
    },
    tip: 'Uneven release finger heights cause clutch chatter, partial release, and gear grinding.',
    colorTag: '#fb7185',
    telemetry: {
      stationCode: 'LUK-CELL-08',
      robotType: 'Staubli TX2-60 Spring Placer',
      toolBrand: 'Keyence LJ-X8000 3D Laser Profiler',
      cycleTime: '26s Takt',
      laserRunout: 'Finger Tip Height Spread: 0.14 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Release Fingers', value: '18 Slotted Petals' },
      { label: 'Spring Rate Curve', value: 'Negative Rate Over-Center' },
      { label: 'Fulcrum Wire Rings', value: 'Dual Hardened Steel (Ø 3.0mm)' },
      { label: 'Release Actuation Load', value: '1,450 N at Bearing' }
    ],
    defectConfig: {
      defectName: 'Diaphragm Spring Fingers Height Runout',
      defectType: 'Spring Finger Height Deviation',
      paramName: 'Fingers Height Runout',
      nominal: 0.2,
      defectInitial: 1.9,
      tolerance: 0.3,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.5,
      stepSize: 0.1,
      instruction: 'Inspect diaphragm spring temper; replace or re-level fingers to within 0.3 mm.'
    }
  },
  {
    id: 9,
    partKey: 'sac_ratchet',
    partName: 'Station 09: Self-Adjusting Clutch (SAC) Sensor Spring Ratchet Reset',
    partCode: 'SAC-RTC-300',
    category: 'Self-Adjusting Clutch Mechanism',
    material: 'PA66 Glass-Filled Polyamide & Spring Steel Ratchet Sensor',
    tool: 'LuK Automated SAC Preload Compression Rig',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Ratchet Stop Zero Position ±0.05 mm',
    title: 'SAC Adjusting Ring Pre-Tensioning & Ratchet Lockout',
    instruction: 'Engage automated SAC compression fixture. Depress diaphragm spring to compress sensor spring ring. Rotate internal ramped adjustment ring to zero-wear factory stop and engage ratchet lockout pawl.',
    voiceScript: 'Station 9: Compress the diaphragm spring using the SAC tool and reset the self-adjusting ratchet ring to factory zero position.',
    translations: {
      en: 'Station 9: Compress the diaphragm spring using the SAC tool and reset the self-adjusting ratchet ring to factory zero position.',
      ta: 'படி 9: எஸ்ஏசி டூல் மூலம் டயாபிராம் ஸ்பிரிங்கை அழுத்தி, செல்ஃப்-அட்ஜஸ்டிங் ராச்செட் ரிங்கை பூஜ்ஜிய நிலைக்கு ரீசெட் செய்யவும்.',
      ml: 'ഘട്ടം 9: എസ്എസി ടൂൾ ഉപയോഗിച്ച് ഡയഫ്രം സ്പ്രിംഗ് പ്രസ്സ് ചെയ്ത് റാച്ചറ്റ് റിംഗ് റീസെറ്റ് ചെയ്യുക.',
      hi: 'चरण 9: एसएसी टूल का उपयोग करके डायाफ्राम स्प्रिंग को संपीड़ित करें और शाफ़्ट रिंग को शून्य स्थिति पर रीसेट करें।'
    },
    tip: 'If SAC ratchet is not reset to zero, the clutch will permanently slip from Day 1.',
    colorTag: '#eab308',
    telemetry: {
      stationCode: 'LUK-CELL-09',
      robotType: 'KUKA KR 10 R1100 SAC Cell',
      toolBrand: 'Schaeffler LuK Automated SAC Tooling',
      cycleTime: '30s Takt',
      laserRunout: 'SAC Ratchet Gap: 0.00 mm [LOCKED]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'SAC Mechanism', value: 'Schaeffler LuK Sensor Spring' },
      { label: 'Ramp Wedge Angle', value: '12° Precision Low-Friction' },
      { label: 'Wear Compensation Travel', value: '4.5 mm Automatic Over Life' },
      { label: 'Lockout Verification', value: 'Vision Laser Pawl Check' }
    ],
    defectConfig: {
      defectName: 'SAC Ratchet Spring Pre-tension Gap',
      defectType: 'Adjusting Ring Premature Unlocking',
      paramName: 'Ratchet Gap',
      nominal: 0.0,
      defectInitial: 1.8,
      tolerance: 0.1,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 2.5,
      stepSize: 0.1,
      instruction: 'Compress SAC tool fully until adjusting ring locks flush against factory stop.'
    }
  },
  {
    id: 10,
    partKey: 'cover_qc',
    partName: 'Station 10: Stamped Steel Cover 3-Stage Star Torquing & EOL 7.2 kN Dyno',
    partCode: 'CVR-EOL-100',
    category: 'End-of-Line Transmission Assurance & IATF 16949 Certification',
    material: 'High-Strength Deep-Draw Steel (DD14) & Sealed Release Bearing',
    tool: 'Multi-Spindle DC Nutrunner & Automated Actuation Dyno Bench',
    targetTorque: 25,
    requiresTorque: true,
    tolerance: 'Criss-Cross Torque: 25 Nm ± 1 Nm • Clamp Load: 7,200 N',
    title: 'Clutch Cover Star Torquing, Mandrel Extraction & 7.2 kN Dyno Certification',
    instruction: 'Fit stamped steel cover over 3 dowel pins. Multi-spindle tool torques 6x M8 bolts diagonally (10 Nm ➔ 25 Nm). Extract alignment arbor smoothly. Dyno bench verifies 7,200 N clamp load and 1.8 mm release lift.',
    voiceScript: 'Station 10: Final Quality Station. Torque the 6 cover bolts to 25 Newton-meters in a star pattern. Mandrel extracted and clutch certified on 7.2 kilonewton dyno.',
    translations: {
      en: 'Station 10: Final Quality Station. Torque the 6 cover bolts to 25 Newton-meters in a star pattern. Mandrel extracted and clutch certified on 7.2 kilonewton dyno.',
      ta: 'படி 10: இறுதி தரக் கட்டுப்பாடு. 6 கவர் போல்ட்களையும் 25 நியூட்டன் மீட்டரில் இறுக்கவும். அலைன்மென்ட் டூல் அகற்றப்பட்டு 7,200 நியூட்டன் டைனோவில் கிளட்ச் சான்றளிக்கப்பட்டது.',
      ml: 'ഘട്ടം 10: അവസാന ക്വാളിറ്റി ടെസ്റ്റ്. 6 കവർ ബോൾട്ടുകൾ 25 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക. 7.2 കിലോന്യൂട്ടൺ ഡൈനോയിൽ ക്ലച്ച് സർട്ടിഫൈ ചെയ്തു.',
      hi: 'चरण 10: अंतिम गुणवत्ता नियंत्रण। क्लच कवर के 6 बोल्ट्स को स्टार पैटर्न में 25 न्यूटन मीटर पर कसें। मैंड्रेल निकालें और 7.2 किलोन्यूटन डायनो पर प्रमाणित करें।'
    },
    tip: 'Smooth hand extraction of the alignment arbor confirms the clutch friction plate is dead centered.',
    colorTag: '#10b981',
    telemetry: {
      stationCode: 'LUK-CELL-10 (EOL)',
      robotType: 'Dyno Test Bench & Multi-Spindle Cell',
      toolBrand: 'Atlas Copco 6-Spindle + Kistler Dyno',
      cycleTime: '48s Takt',
      laserRunout: 'Clamp Force: 7,240 N [PASS]',
      heliumDecay: 'Release Stroke: 2.1 mm [PASS]',
      torqueCurve: [0, 8, 18, 25]
    },
    specs: [
      { label: 'Bolt Spec', value: '6x M8 x 1.25 Grade 10.9 Flange' },
      { label: 'Fastener Torque', value: '25 Nm (Star Sequence)' },
      { label: 'Clamping Force Verified', value: '7,200 N (±250 N)' },
      { label: 'Release Lift Clearance', value: '2.1 mm (> 1.8 mm spec)' }
    ],
    defectConfig: {
      defectName: 'Stamped Cover Dowel Pin Seating Mismatch',
      defectType: 'Cover Alignment Dowel Gap',
      paramName: 'Dowel Gap',
      nominal: 0.0,
      defectInitial: 2.2,
      tolerance: 0.2,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 3.0,
      stepSize: 0.1,
      instruction: 'Press stamped cover firmly over all 3 locating dowel pins before bolting.'
    }
  }
];

export const FULL_CAR_ASSEMBLY_STEPS = [
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
];

export const KNUCKLE_JOINT_STEPS = [
  {
    id: 1,
    partKey: 'fork_end',
    partName: 'Double-Eye Fork End & Rod',
    partCode: 'KCL-FRK-01',
    category: 'Kinematic Linkage / Fork Sub-Assembly',
    material: 'Forged Carbon Steel (AISI 1045)',
    tool: 'Bore Dial Gauge & Heavy AGV Clamp Rig',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Fork Ear Gap 38.0 ± 0.2 mm',
    title: 'Fork End Fixture Clamping & Eye Bore Inspection',
    instruction: 'Secure the double-eye fork end in the kinematic assembly jig. Measure the fork opening gap and verify the upper and lower 30mm coaxial pin bores.',
    voiceScript: 'Step 1: Clamp the fork end into the jig. Inspect the upper and lower pin bores for concentricity and burr-free chamfers.',
    translations: {
      en: 'Step 1: Clamp the fork end into the jig. Inspect the upper and lower pin bores for concentricity and burr-free chamfers.',
      ta: 'படி 1: ஃபோர்க் முனையை ஜிக்கில் இறுக்கவும். மேல் மற்றும் கீழ் பின் துளைகள் சீராக உள்ளதா என ஆய்வு செய்யவும்.',
      ml: 'ഘട്ടം 1: ഫോർക്ക് എൻഡ് ജിഗ്ഗിൽ ഘടിപ്പിക്കുക. മുകളിലെയും താഴത്തെയും ദ്വാരങ്ങൾ പരിശോധിക്കുക.',
      hi: 'चरण 1: फोर्क एंड को जिग में क्लैंप करें। ऊपरी और निचले पिन छिद्रों का निरीक्षण करें।'
    },
    tip: 'Ensure the fork ear gap matches the design nominal width of 1.25d (37.5 - 38.0 mm) before inserting the eye end.',
    colorTag: '#00f0ff',
    specs: [
      { label: 'Rod Diameter (d)', value: '30 mm' },
      { label: 'Fork Ear Thickness', value: '22.5 mm (0.75d)' },
      { label: 'Bore Diameter (d1)', value: '30 mm (H7 Fit)' },
      { label: 'Fork Gap Spread', value: '38.0 mm' }
    ],
    defectConfig: {
      defectName: 'Fork End Pin Bore Misalignment',
      defectType: 'Coaxial Bore Runout',
      paramName: 'Bore Alignment Angle',
      nominal: 90.0,
      defectInitial: 74.2,
      tolerance: 1.0,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Adjust fork fixture hydraulic clamping jaws to restore 90.0° coaxial bore alignment.'
    }
  },
  {
    id: 2,
    partKey: 'eye_end',
    partName: 'Single-Eye Rod End Interlocking',
    partCode: 'KCL-EYE-02',
    category: 'Kinematic Linkage / Eye Sub-Assembly',
    material: 'Forged Carbon Steel (AISI 1045)',
    tool: 'Feeler Gauge & Feeder Slide Rail',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Lateral Clearance 0.5 - 1.0 mm Equalized',
    title: 'Single Eye End Insertion & Bore Alignment',
    instruction: 'Slide the single-eye rod end into the fork end opening. Align the 30mm central eye bore coaxially with both fork ear bores to form a continuous cylindrical passage.',
    voiceScript: 'Step 2: Slide the single eye end into the fork gap. Align the central bore to form a clean passage for the knuckle pin.',
    translations: {
      en: 'Step 2: Slide the single eye end into the fork gap. Align the central bore to form a clean passage for the knuckle pin.',
      ta: 'படி 2: சிங்கிள் ஐ முனையை ஃபோர்க் இடைவெளியில் பொருத்தவும். நக்கிள் பின் நுழைவதற்கு துளையை சீரமைக்கவும்.',
      ml: 'ഘട്ടം 2: സിംഗിൾ ഐ എൻഡ് ഫോർക്ക് ഗ്യാപ്പിലേക്ക് കടത്തുക. സെൻട്രൽ ബോർ നേരെയാക്കുക.',
      hi: 'चरण 2: सिंगल आई एंड को फोर्क गैप में स्लाइड करें। नक्कल पिन के लिए केंद्रीय छिद्र को संरेखित करें।'
    },
    tip: 'Coat the eye mating faces with anti-friction molybdenum disulfide paste to prevent galling during articulation.',
    colorTag: '#38bdf8',
    specs: [
      { label: 'Eye Thickness (t)', value: '37.5 mm (1.25d)' },
      { label: 'Outer Eye Diameter (D)', value: '60 mm (2d)' },
      { label: 'Bore Fit Class', value: 'ISO H7/f7 Precision Clearance' },
      { label: 'Axial Running Clearance', value: '0.5 mm Total' }
    ],
    defectConfig: {
      defectName: 'Single Eye End Axial Tilt Error',
      defectType: 'Eye Face Orthogonality',
      paramName: 'Insertion Angle',
      nominal: 90.0,
      defectInitial: 72.8,
      tolerance: 1.0,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Re-align the single-eye rod horizontally until concentric with the fork ears at 90.0°.'
    }
  },
  {
    id: 3,
    partKey: 'knuckle_pin',
    partName: 'Hardened Knuckle Pivot Pin (30mm)',
    partCode: 'KCL-PIN-03',
    category: 'Pivot Fulcrum & Shear Pin',
    material: 'Case-Hardened Alloy Steel (SAE 8620, 58 HRC)',
    tool: 'Hydraulic Pin Press & Digital Micrometer',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Pin Diameter 30.0 mm (h6 Tolerance)',
    title: 'Knuckle Pivot Pin Insertion & Shoulder Seating',
    instruction: 'Insert the 30mm cylindrical knuckle pin downward through the upper fork ear, central eye, and lower fork ear until the enlarged pin head rests flush against the top ear.',
    voiceScript: 'Step 3: Insert the hardened knuckle pin from the top. Ensure the pin head seats fully flush against the upper fork ear.',
    translations: {
      en: 'Step 3: Insert the hardened knuckle pin from the top. Ensure the pin head seats fully flush against the upper fork ear.',
      ta: 'படி 3: நக்கிள் பின்னை மேலிருந்து செருகவும். பின் தலை மேல் ஃபோர்க் பகுதியில் சரியாக அமர்வதை உறுதிசெய்யவும்.',
      ml: 'ഘട്ടം 3: നക്കിൾ പിൻ മുകളിൽ നിന്ന് തിരുകുക. പിൻ തല ശരിയായി ഇരിക്കുന്നുണ്ടെന്ന് ഉറപ്പുവരുത്തുക.',
      hi: 'चरण 3: नक्कल पिन को ऊपर से डालें। सुनिश्चित करें कि पिन हेड पूरी तरह से बैठ गया है।'
    },
    tip: 'Verify that the pin bottom spigot extends past the lower fork ear with the cross-hole fully exposed.',
    colorTag: '#f59e0b',
    specs: [
      { label: 'Pin Diameter (d1)', value: '30 mm (h6 fit)' },
      { label: 'Pin Head Diameter (d2)', value: '45 mm (1.5d)' },
      { label: 'Pin Head Thickness', value: '15 mm (0.5d)' },
      { label: 'Total Pin Length', value: '115 mm' }
    ],
    defectConfig: {
      defectName: 'Knuckle Pin Verticality Runout',
      defectType: 'Pin Axis Cocking',
      paramName: 'Pin Axis Angle',
      nominal: 90.0,
      defectInitial: 78.4,
      tolerance: 1.0,
      unit: '°',
      minVal: 75.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Press the knuckle pin square into the fork ears to eliminate angular cocking.'
    }
  },
  {
    id: 4,
    partKey: 'collar',
    partName: 'Collar Retention Ring',
    partCode: 'KCL-CLR-04',
    category: 'Axial Retention System',
    material: 'Mild Steel (IS 2062)',
    tool: 'Snap-Fit Guide & Feeler Gauge',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Collar Bore 30.2 mm (H8 Fit)',
    title: 'Collar Retention Ring Slide-Fit Positioning',
    instruction: 'Slide the circular retention collar onto the lower protruding pin spigot until it seats against the underside of the lower fork ear. Align the radial taper pin cross-holes.',
    voiceScript: 'Step 4: Slide the retention collar over the lower pin spigot. Align the through-hole on the collar with the cross-hole in the pin.',
    translations: {
      en: 'Step 4: Slide the retention collar over the lower pin spigot. Align the through-hole on the collar with the cross-hole in the pin.',
      ta: 'படி 4: காலரை கீழ் பின் பகுதியில் பொருத்தவும். காலரில் உள்ள துளையை பின்னின் துளையுடன் நேராக சீரமைக்கவும்.',
      ml: 'ഘട്ടം 4: കോളർ താഴത്തെ പിന്നിലേക്ക് കടത്തുക. ദ്വാരങ്ങൾ നേരെയാക്കുക.',
      hi: 'चरण 4: निचले पिन पर रिटेंशन कॉलर स्लाइड करें। कॉलर के छिद्र को पिन के छिद्र से संरेखित करें।'
    },
    tip: 'Ensure the cross-hole in the collar lines up precisely with the hole in the pin before inserting the taper pin.',
    colorTag: '#fb7185',
    specs: [
      { label: 'Collar Outer Diameter (d3)', value: '45 mm (1.5d)' },
      { label: 'Collar Thickness (t2)', value: '15 mm (0.5d)' },
      { label: 'Cross-Hole Diameter', value: '7.5 mm (0.25d)' },
      { label: 'Surface Treatment', value: 'Black Oxide Anti-Corrosion' }
    ],
    defectConfig: {
      defectName: 'Collar Radial Cross-Hole Misalignment',
      defectType: 'Cross-Hole Angular Runout',
      paramName: 'Cross-Hole Angle',
      nominal: 90.0,
      defectInitial: 76.5,
      tolerance: 1.5,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Rotate the collar on the pin spigot until the taper pin cross-hole is aligned at 90.0°.'
    }
  },
  {
    id: 5,
    partKey: 'taper_pin',
    partName: 'Taper Split Pin / Cotter Pin (1:30 Taper)',
    partCode: 'KCL-TPR-05',
    category: 'Positive Mechanical Locking',
    material: 'High-Tensile Drawn Spring Steel',
    tool: 'Soft-Faced Brass Drift & Calibrated Torque Driver',
    targetTorque: 15,
    requiresTorque: true,
    tolerance: 'Taper Ratio 1:30 (±0.02 mm/m)',
    title: 'Taper Pin Press-Fit & Split End Locking (15 Nm)',
    instruction: 'Drive the 1:30 taper pin into the aligned cross-holes through collar and main pin. Tighten locking collar set fastener to 15 Newton-meters and splay the split end.',
    voiceScript: 'Step 5: Drive the taper pin through the collar and knuckle pin. Torque locking fastener to 15 Newton meters to prevent pin displacement.',
    translations: {
      en: 'Step 5: Drive the taper pin through the collar and knuckle pin. Torque locking fastener to 15 Newton meters to prevent pin displacement.',
      ta: 'படி 5: டேப்பர் பின்னை காலர் மற்றும் நக்கிள் பின் வழியாக செலுத்தவும். லாக்கிங் நட்டை 15 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 5: ടേപ്പർ പിൻ കോളറിലൂടെ അടിച്ചു കയറ്റുക. ലോക്കിംഗ് ഫാസ്റ്റനർ 15 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 5: टेपर पिन को कॉलर और नक्कल पिन से गुजारें। लॉकिंग नट को 15 न्यूटन मीटर पर कसें।'
    },
    tip: 'Always drive the taper pin from the larger diameter side and bend the split ends outward by at least 30 degrees.',
    colorTag: '#eab308',
    specs: [
      { label: 'Nominal Mean Diameter (d4)', value: '7.5 mm' },
      { label: 'Standard Taper Ratio', value: '1 in 30 Taper' },
      { label: 'Total Taper Pin Length', value: '55 mm' },
      { label: 'Locking Fastener Torque', value: '15 Nm' }
    ],
    defectConfig: {
      defectName: 'Taper Pin Incomplete Seating Defect',
      defectType: 'Taper Pin Projection Depth',
      paramName: 'Seating Angle',
      nominal: 90.0,
      defectInitial: 71.7,
      tolerance: 1.0,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Drive the taper pin square to the collar axis until fully wedged at 90.0°.'
    }
  },
  {
    id: 6,
    partKey: 'complete',
    partName: 'Kinematic Swivel Angle & Load Certification',
    partCode: 'KCL-QCK-06',
    category: 'End-of-Line Quality Assurance',
    material: 'Complete Kinematic Joint Module',
    tool: 'Digital Inclinometer & 30 kN Tensile Test Rig',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Angular Articulation ±45°, Zero Seizure',
    title: 'Kinematic Swivel Freedom & Tensile Load Certification',
    instruction: 'Perform dynamic articulation test across full ±45° angular pivot sweep. Apply 25 kN proof tensile load test. Verify zero binding, zero taper pin looseness, and issue ISO QC Certificate.',
    voiceScript: 'Step 6: Knuckle joint assembly complete and certified. Articulation sweep and tensile load tests passed with zero defects.',
    translations: {
      en: 'Step 6: Knuckle joint assembly complete and certified. Articulation sweep and tensile load tests passed with zero defects.',
      ta: 'படி 6: நக்கிள் ஜாயிண்ட் அசெம்பிளி வெற்றிகரமாக முடிந்தது. இயக்கம் மற்றும் இழுவிசை சோதனைகள் பூஜ்ஜிய பிழையுடன் தேர்ச்சி பெற்றது.',
      ml: 'ഘട്ടം 6: നക്കിൾ ജോയിന്റ് അസംബ്ലി പൂർത്തിയായി. ടെൻസൈൽ ലോഡ് ടെസ്റ്റുകൾ വിജയകരമായി പൂർത്തിയാക്കി.',
      hi: 'चरण 6: नक्कल जॉइंट असेंबली पूरी और प्रमाणित हुई। तनाव परीक्षण शून्य दोषों के साथ पास हुए।'
    },
    tip: 'Ensure joint swivels freely by hand with zero binding before dispatching to link mechanism assembly.',
    colorTag: '#10b981',
    specs: [
      { label: 'Total Assembly Weight', value: '6.4 kg' },
      { label: 'Maximum Angular Articulation', value: '±45° Full Sweep' },
      { label: 'Design Tensile Capacity', value: '35 kN (Factor of Safety 4)' },
      { label: 'Inspection Status', value: 'PASSED (Zero Defects)' }
    ],
    defectConfig: {
      defectName: 'Kinematic Articulation Binding Error',
      defectType: 'Swivel Plane Orthogonality',
      paramName: 'Swivel Angle',
      nominal: 90.0,
      defectInitial: 75.0,
      tolerance: 1.0,
      unit: '°',
      minVal: 70.0,
      maxVal: 90.0,
      stepSize: 0.5,
      instruction: 'Re-align joint axis to allow unobstructed 90.0° perpendicular articulation.'
    }
  }
];

// BMW S58 TwinPower Turbo 3.0L Inline-6 DOHC High-Performance Engine Core Assembly Data
// Industry 4.0 Standard Work Instructions (SWI) - BMW M Division Powertrain Plant Munich
export const ENGINE_ASSEMBLY_STEPS = [
  {
    id: 1,
    partKey: 'engine_block',
    partName: 'Station 01: Closed-Deck Aluminum Engine Block & Main Journal Bearings',
    partCode: 'S58-BLK-01',
    category: 'Powertrain Line - Engine Core Cell',
    material: 'High-Strength AlSiCu Alloy with Wire-Arc LDS Coated Cylinder Bores',
    tool: 'Laser Bore Profilometer & Ultrasonic Wash Tank',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Bore Diameter 84.0 mm ±0.005 mm',
    title: 'Closed-Deck Engine Block Alignment & Main Bearing Shell Seating',
    instruction: 'Load the S58 closed-deck engine block onto the build rotisserie. Install 7 tri-layer lower main bearing shells with assembly lubricant. Scan bore roundness with laser CMM (< 0.005 mm).',
    voiceScript: 'Station 1: Load the S58 closed-deck engine block onto the build rotisserie. Install 7 tri-layer lower main bearing shells with assembly lubricant.',
    translations: {
      en: 'Station 1: Load the S58 closed-deck engine block onto the build rotisserie. Install 7 tri-layer lower main bearing shells with assembly lubricant.',
      ta: 'படி 1: S58 க்ளோஸ்டு-டெக் என்ஜின் பிளாக்கை அசெம்பிளி ஸ்டாண்டில் ஏற்றவும். 7 மெயின் பேரிங் ஷெல்களை லுப்ரிகண்ட் பூசி பொருத்தவும்.',
      ml: 'ഘട്ടം 1: എഞ്ചിൻ ബ്ലോക്ക് സ്റ്റാൻഡിൽ ഘടിപ്പിച്ച് മെയിൻ ബെയറിംഗുകൾ വെയ്ക്കുക.',
      hi: 'चरण 1: एस58 क्लोज्ड-डेक इंजन ब्लॉक को माउंट करें और 7 मुख्य बेयरिंग लगाएं।'
    },
    tip: 'Ensure LDS wire-arc coated bore crosshatch hone angle is 45° for optimal oil retention.',
    colorTag: '#00f0ff',
    telemetry: {
      stationCode: 'BMW-ENG-01',
      robotType: 'KUKA Titan Heavy Handling Robot',
      toolBrand: 'Keyence Optical CMM + Kistler Servo',
      cycleTime: '35s Takt',
      laserRunout: 'Bore Roundness: 0.003 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Engine Architecture', value: '3.0L Inline-6 TwinPower Turbo (S58)' },
      { label: 'Cylinder Bore', value: '84.0 mm (LDS Wire-Arc Coated)' },
      { label: 'Block Construction', value: 'Closed-Deck Deep Skirt Aluminum' },
      { label: 'Main Bearing Count', value: '7 Hardened Journal Saddles' }
    ],
    defectConfig: {
      defectName: 'Cylinder Bore LDS Roundness Defect',
      defectType: 'Cylinder Bore Out-of-Round',
      paramName: 'Bore Roundness',
      nominal: 0.005,
      defectInitial: 0.045,
      tolerance: 0.010,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.06,
      stepSize: 0.002,
      instruction: 'Re-hone cylinder bore wire-arc coating to restore circularity under 0.010 mm.'
    }
  },
  {
    id: 2,
    partKey: 'crankshaft',
    partName: 'Station 02: Forged 42CrMo4 Counterweighted Crankshaft Installation',
    partCode: 'S58-CRK-02',
    category: 'Cranktrain Dynamics Cell',
    material: 'Micro-Finished Forged 42CrMo4 Steel with Induction-Hardened Fillets',
    tool: 'Overhead Soft-Grip Crane & Mitutoyo Dial Thrust Gauge',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'End-Float Thrust Clearance 0.08 - 0.16 mm',
    title: 'Crankshaft Lowering & Axial Thrust Bearing Measurement',
    instruction: 'Carefully lower the forged steel crankshaft onto the 7 main journals. Verify crankshaft end-float axial clearance is within 0.08 to 0.16 mm using magnetic dial indicator.',
    voiceScript: 'Station 2: Carefully lower the forged steel crankshaft onto the main journals. Verify crankshaft end-float axial clearance is within 0.16 millimeters.',
    translations: {
      en: 'Station 2: Carefully lower the forged steel crankshaft onto the main journals. Verify crankshaft end-float axial clearance is within 0.16 millimeters.',
      ta: 'படி 2: ஃபோர்ஜ்டு ஸ்டீல் கிரான்க்ஷாஃப்ட்டை மெயின் ஜர்னல்களில் இறக்கவும். ஆக்சியல் எண்ட்-ஃப்ளோட் இடைவெளி 0.16 மிமீக்குள் இருப்பதை உறுதிசெய்யவும்.',
      ml: 'ഘട്ടം 2: ക്രാങ്ക് ഷാഫ്റ്റ് ജേർണലുകളിൽ കൃത്യമായി ഘടിപ്പിക്കുക.',
      hi: 'चरण 2: जालीदार स्टील क्रैंकशाफ्ट लगाएं और एंड-फ्लोट क्लीयरेंस 0.16 मिमी जांचें।'
    },
    tip: 'Coat crankshaft journals with synthetic assembly paste; never rotate dry bearings.',
    colorTag: '#38bdf8',
    telemetry: {
      stationCode: 'BMW-ENG-02',
      robotType: 'ABB IRB 6700 Crane Robot',
      toolBrand: 'Mitutoyo 543 Digital Dial Gauge',
      cycleTime: '28s Takt',
      laserRunout: 'End-Float: 0.11 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Crankshaft Material', value: '42CrMo4 Forged High-Carbon Steel' },
      { label: 'Crankpin Throw Spacing', value: '120° (Perfect 6-Cylinder Balance)' },
      { label: 'Thrust Clearance', value: '0.08 - 0.16 mm Specification' },
      { label: 'Main Journal Diameter', value: '56.0 mm Ground' }
    ],
    defectConfig: {
      defectName: 'Crankshaft Axial Thrust Clearance Error',
      defectType: 'Axial End-Float Disparity',
      paramName: 'End-Float',
      nominal: 0.11,
      defectInitial: 0.38,
      tolerance: 0.05,
      unit: 'mm',
      minVal: 0.05,
      maxVal: 0.45,
      stepSize: 0.01,
      instruction: 'Fit oversized axial thrust bearing washers to restore 0.11 mm end-float.'
    }
  },
  {
    id: 3,
    partKey: 'bedplate',
    partName: 'Station 03: Main Bearing Bedplate Ladder Frame & 14x Stretch Bolts',
    partCode: 'S58-BED-03',
    category: 'Cranktrain Clamping & Structural Cell',
    material: 'Cast Aluminum Structural Ladder Frame & Grade 12.9 Fasteners',
    tool: 'Atlas Copco Multi-Spindle DC Electric Nutrunner',
    targetTorque: 25,
    requiresTorque: true,
    tolerance: 'Torque 25 Nm + 70° Angle',
    title: 'Structural Lower Bedplate Clamping & Torque-to-Yield Angle Protocol',
    instruction: 'Position structural ladder bedplate. Fasten all 14 main bearing cap stretch bolts to 25 Nm in center-outward sequence, then apply final 70° angle torque stage.',
    voiceScript: 'Station 3: Position the structural ladder bedplate. Fasten all 14 main bearing cap stretch bolts to 25 Newton-meters plus 70 degrees.',
    translations: {
      en: 'Station 3: Position the structural ladder bedplate. Fasten all 14 main bearing cap stretch bolts to 25 Newton-meters plus 70 degrees.',
      ta: 'படி 3: லேடர் பெட்பிளேட்டை வைத்து, 14 மெயின் கேப் போல்ட்களையும் 25 நியூட்டன் மீட்டர் மற்றும் 70 டிகிரி ஆங்கிளில் இறுக்கவும்.',
      ml: 'ഘട്ടം 3: ബെഡ്‌പ്ലേറ്റ് ഉറപ്പിച്ച് 14 ബോൾട്ടുകൾ 25 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 3: बेडप्लेट लगाएं और सभी 14 मुख्य कैप बोल्ट को 25 न्यूटन मीटर और 70 डिग्री पर कसें।'
    },
    tip: 'Electronic DC nutrunner logs yield angle curve into MES to prevent bolt over-stretch.',
    colorTag: '#60a5fa',
    telemetry: {
      stationCode: 'BMW-ENG-03',
      robotType: 'Atlas Copco 14-Spindle Synchronous Cell',
      toolBrand: 'Atlas Copco Tensor Revo DC',
      cycleTime: '22s Takt',
      laserRunout: 'Bolt Stretch: 0.22 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 10, 20, 25]
    },
    specs: [
      { label: 'Fastener Grade', value: 'Grade 12.9 High-Tensile Stretch Bolt' },
      { label: 'Torque Protocol', value: '25 Nm + 70° Yield Rotation' },
      { label: 'Main Cap Count', value: '7 Integral Cross-Bolted Webs' },
      { label: 'Bedplate Material', value: 'Cast A380 High-Rigidity Aluminum' }
    ],
    defectConfig: {
      defectName: 'Bedplate Main Bolt Preload Disparity',
      defectType: 'Stretch Bolt Insufficient Angle',
      paramName: 'Tightening Angle',
      nominal: 70.0,
      defectInitial: 38.0,
      tolerance: 5.0,
      unit: '°',
      minVal: 30.0,
      maxVal: 80.0,
      stepSize: 2.0,
      instruction: 'Complete secondary 70.0° angle torque to achieve design bolt stretch.'
    }
  },
  {
    id: 4,
    partKey: 'connecting_rods',
    partName: 'Station 04: 6x Forged 4340 H-Beam Connecting Rods & ARP Bolts',
    partCode: 'S58-ROD-04',
    category: 'Reciprocating Powertrain Cell',
    material: 'Forged 4340 Chromoly Steel H-Beam with Fractured Split Caps',
    tool: 'ARP Stretch Gauge & Digital Angle Torque Wrench',
    targetTorque: 45,
    requiresTorque: true,
    tolerance: 'Rod Bolt Stretch 0.14 - 0.16 mm',
    title: 'H-Beam Connecting Rod Installation & ARP Rod Bolt Stretch',
    instruction: 'Assemble forged H-beam connecting rods onto crankshaft rod pins. Torque ARP 2000 bolts to 45 Nm and verify bolt stretch using micrometer gauge (0.14 - 0.16 mm).',
    voiceScript: 'Station 4: Assemble the forged H-beam connecting rods onto the crank pins. Torque rod bolts to 45 Newton-meters and verify bolt stretch.',
    translations: {
      en: 'Station 4: Assemble the forged H-beam connecting rods onto the crank pins. Torque rod bolts to 45 Newton-meters and verify bolt stretch.',
      ta: 'படி 4: ஃபோர்ஜ்டு ஹெச்-பீம் கனெக்டிங் ராடுகளை கிரான்க் பின்களில் பொருத்தி, போல்ட்களை 45 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 4: കണക്റ്റിംഗ് റോഡുകൾ 45 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 4: एच-बीम कनेक्टिंग रॉड लगाएं और 45 न्यूटन मीटर पर कसें।'
    },
    tip: 'Fractured split rod caps must mate with micro-interlocking surfaces; never reverse caps.',
    colorTag: '#818cf8',
    telemetry: {
      stationCode: 'BMW-ENG-04',
      robotType: 'Staubli TX2-90 Precision Assembly',
      toolBrand: 'Desoutter Delta DC + ARP Stretch Micrometer',
      cycleTime: '32s Takt',
      laserRunout: 'Bolt Stretch: 0.152 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 15, 30, 45]
    },
    specs: [
      { label: 'Rod Geometry', value: 'H-Beam High-RPM Lightweight Forging' },
      { label: 'Fastener Spec', value: 'ARP 2000 3/8" Aircraft Fasteners' },
      { label: 'Small End Bushing', value: 'Ampco 45 High-Load Bronze' },
      { label: 'Target Bolt Stretch', value: '0.15 mm (±0.01 mm)' }
    ],
    defectConfig: {
      defectName: 'Connecting Rod Cap Alignment Shift',
      defectType: 'Fractured Cap Joint Misalignment',
      paramName: 'Joint Gap',
      nominal: 0.0,
      defectInitial: 0.08,
      tolerance: 0.01,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.10,
      stepSize: 0.005,
      instruction: 'Re-seat cracked-cap interlocking teeth flush before final torquing.'
    }
  },
  {
    id: 5,
    partKey: 'pistons',
    partName: 'Station 05: 6x Forged Aluminum Pistons & 3-Piece Ring Packs',
    partCode: 'S58-PST-05',
    category: 'Combustion Chamber Assembly Cell',
    material: 'Forged Aluminum Alloy with Grafal Anti-Friction Skirt Coating',
    tool: 'Tapered Billet Piston Ring Compressor & Brass Drift Mallet',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Piston Ring End-Gap 0.28 - 0.35 mm',
    title: 'Piston Ring Staggering & Smooth Cylinder Bore Insertion',
    instruction: 'Stagger the 3 piston ring end-gaps at 120-degree intervals. Use tapered ring compressor to guide pistons into cylinders 1 through 6. Push wrist pins through rod small ends.',
    voiceScript: 'Station 5: Stagger the 3 piston ring end-gaps at 120-degree intervals. Use the tapered ring compressor to guide pistons into cylinders 1 through 6.',
    translations: {
      en: 'Station 5: Stagger the 3 piston ring end-gaps at 120-degree intervals. Use the tapered ring compressor to guide pistons into cylinders 1 through 6.',
      ta: 'படி 5: பிஸ்டன் ரிங் இடைவெளிகளை 120 டிகிரியில் ஒழுங்குபடுத்தி, பிஸ்டன்களை சிலிண்டர் துளைகளில் தட்டவும்.',
      ml: 'ഘട്ടം 5: പിസ്റ്റൺ റിംഗ് കംപ്രസർ ഉപയോഗിച്ച് പിസ്റ്റണുകൾ സിലിണ്ടറിലേക്ക് ഘടിപ്പിക്കുക.',
      hi: 'चरण 5: पिस्टन रिंग्स को 120 डिग्री पर सेट करें और पिस्टन को सिलेंडरों में डालें।'
    },
    tip: 'Ensure piston crown arrow points toward timing chain at front (+Z) of engine block.',
    colorTag: '#a78bfa',
    telemetry: {
      stationCode: 'BMW-ENG-05',
      robotType: 'FANUC M-10iD Piston Insertion Cell',
      toolBrand: 'Wiseco Billet 84mm Tapered Guide',
      cycleTime: '30s Takt',
      laserRunout: 'Ring Gap: 0.31 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Piston Manufacturing', value: 'Forged 2618 High-Silicon Alloy' },
      { label: 'Skirt Coating', value: 'Grafal Low-Friction Graphite' },
      { label: 'Wrist Pin Architecture', value: 'Full-Floating DLC Coated' },
      { label: 'Compression Ratio', value: '9.3:1 Turbo Optimized' }
    ],
    defectConfig: {
      defectName: 'Piston Ring End-Gap Clearance Disparity',
      defectType: 'Insufficient Top Ring Gap',
      paramName: 'Ring End-Gap',
      nominal: 0.30,
      defectInitial: 0.12,
      tolerance: 0.05,
      unit: 'mm',
      minVal: 0.10,
      maxVal: 0.45,
      stepSize: 0.02,
      instruction: 'File top compression ring end-gap to achieve 0.30 mm thermal clearance.'
    }
  },
  {
    id: 6,
    partKey: 'oil_pan',
    partName: 'Station 06: Structural Aluminum Oil Sump Pan & Windage Baffle',
    partCode: 'S58-OIL-06',
    category: 'Lubrication & Lower Sealing Cell',
    material: 'Die-Cast Aluminum with Integrated Baffle & Rubber Gasket',
    tool: 'Loctite Automated RTV Silicone Dispenser & Cordless Nutrunner',
    targetTorque: 12,
    requiresTorque: true,
    tolerance: 'Torque 12 Nm Cross-Pattern',
    title: 'Oil Sump Pan Sealing & Track Windage Tray Installation',
    instruction: 'Mount oil pickup strainer and install aluminum oil pan. Fasten 22 perimeter bolts to 12 Nm in cross pattern. Torque magnetic drain plug to 25 Nm.',
    voiceScript: 'Station 6: Mount the oil pickup strainer and install the aluminum oil pan. Fasten 22 perimeter bolts to 12 Newton-meters in a cross pattern.',
    translations: {
      en: 'Station 6: Mount the oil pickup strainer and install the aluminum oil pan. Fasten 22 perimeter bolts to 12 Newton-meters in a cross pattern.',
      ta: 'படி 6: ஆயில் பிக்கப் டியூபை பொருத்தி, ஆயில் பானை 22 போல்ட்களுடன் 12 நியூட்டன் மீட்டரில் இறுக்கவும்.',
      ml: 'ഘട്ടം 6: ഓയിൽ പാൻ 12 ന്യൂട്ടൺ മീറ്ററിൽ ഘടിപ്പിക്കുക.',
      hi: 'चरण 6: ऑयल पैन लगाएं और 22 बोल्ट को 12 न्यूटन मीटर पर कसें।'
    },
    tip: 'Anti-surge baffle baffles prevent oil pump starvation during high lateral G-force cornering.',
    colorTag: '#c084fc',
    telemetry: {
      stationCode: 'BMW-ENG-06',
      robotType: 'Staubli TS2-60 Dispenser Robot',
      toolBrand: 'Loctite 5970 RTV Robot + Atlas Copco',
      cycleTime: '24s Takt',
      laserRunout: 'Gasket Bead: 1.8 mm [PASS]',
      heliumDecay: '0.00 mbar/s [HERMETIC]',
      torqueCurve: [0, 4, 8, 12]
    },
    specs: [
      { label: 'Oil Capacity', value: '6.5 Liters (0W-30 Synthetic)' },
      { label: 'Sump Design', value: 'Deep Rear Track Baffled Sump' },
      { label: 'Perimeter Bolts', value: '22x M6 Grade 8.8 (12 Nm)' },
      { label: 'Drain Plug', value: 'Magnetic Neodymium M12' }
    ],
    defectConfig: {
      defectName: 'Oil Pan Gasket Flange Bead Defect',
      defectType: 'Silicone Sealant Bead Discontinuity',
      paramName: 'Bead Width',
      nominal: 2.0,
      defectInitial: 0.6,
      tolerance: 0.4,
      unit: 'mm',
      minVal: 0.4,
      maxVal: 3.0,
      stepSize: 0.2,
      instruction: 'Dispense continuous 2.0 mm silicone bead along oil pan perimeter sealing face.'
    }
  },
  {
    id: 7,
    partKey: 'head_gasket',
    partName: 'Station 07: Multi-Layer Steel (MLS) Cylinder Head Gasket',
    partCode: 'S58-GSK-07',
    category: 'High-Pressure Combustion Sealing Cell',
    material: '5-Layer Embossed Stainless Steel with Viton Micro-Seal Coating',
    tool: 'Optical Datum Pin Aligners & Cleanroom Handling Gloves',
    targetTorque: 0,
    requiresTorque: false,
    tolerance: 'Dowel Pin Fit Class H7/h6',
    title: 'MLS Head Gasket Alignment over Hardened Precision Dowels',
    instruction: 'Align 5-layer Multi-Layer Steel head gasket over cylinder block locating dowels. Verify combustion fire-rings are perfectly concentric with cylinder bores.',
    voiceScript: 'Station 7: Align the 5-layer Multi-Layer Steel head gasket over the cylinder block locating dowels. Verify combustion fire-rings are perfectly concentric.',
    translations: {
      en: 'Station 7: Align the 5-layer Multi-Layer Steel head gasket over the cylinder block locating dowels. Verify combustion fire-rings are perfectly concentric.',
      ta: 'படி 7: 5-அடுக்கு MLS ஹெட் கேஸ்கெட்டை டோவல் பின்கள் மீது சீராக பொருத்தவும்.',
      ml: 'ഘട്ടം 7: മൾട്ടി-ലെയർ സ്റ്റീൽ ഹെഡ് ഗാസ്കറ്റ് ഡോവൽ പിന്നുകളിൽ കൃത്യമായി വെയ്ക്കുക.',
      hi: 'चरण 7: 5-परत वाले एमएलएस हेड गास्केट को डॉवेल पिन पर संरेखित करें।'
    },
    tip: 'Never touch MLS gasket sealing beads with bare hands; oils cause combustion gas micro-leaks.',
    colorTag: '#e879f9',
    telemetry: {
      stationCode: 'BMW-ENG-07',
      robotType: 'Staubli TX2-60 Vacuum Handler',
      toolBrand: 'Keyence Optical Vision Inspector',
      cycleTime: '16s Takt',
      laserRunout: 'Dowel Concentricity: 0.012 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 0, 0, 0]
    },
    specs: [
      { label: 'Gasket Technology', value: '5-Layer Spring Stainless Steel (MLS)' },
      { label: 'Compressed Thickness', value: '0.85 mm Precision' },
      { label: 'Coating', value: 'High-Temperature Viton Elastomer' },
      { label: 'Combustion Sealing', value: 'Laser-Welded Stopper Layer' }
    ],
    defectConfig: {
      defectName: 'Head Gasket Combustion Ring Offset',
      defectType: 'Fire-Ring Bore Eccentricity',
      paramName: 'Bore Offset',
      nominal: 0.0,
      defectInitial: 0.42,
      tolerance: 0.05,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.50,
      stepSize: 0.02,
      instruction: 'Re-seat MLS gasket over alignment dowels to ensure 0.0 mm bore concentricity.'
    }
  },
  {
    id: 8,
    partKey: 'cylinder_head',
    partName: 'Station 08: High-Flow DOHC 24-Valve Cylinder Head & 14x Studs',
    partCode: 'S58-HED-08',
    category: 'Cylinder Head & Valve Cell',
    material: 'Cast Aluminum Monoblock with CNC Machined Combustion Chambers',
    tool: 'Automatic Multi-Stage Angle Torque Controller',
    targetTorque: 40,
    requiresTorque: true,
    tolerance: 'Torque 40 Nm + 90° + 90°',
    title: 'Cylinder Head Monoblock Docking & Multi-Stage Torque Protocol',
    instruction: 'Dock 24-valve aluminum cylinder head. Fasten 14 head studs to 40 Nm, then apply two 90-degree angle stages from center outward in spiral sequence.',
    voiceScript: 'Station 8: Dock the 24-valve aluminum cylinder head. Fasten 14 head studs to 40 Newton-meters, then apply two 90-degree angle stages from center outward.',
    translations: {
      en: 'Station 8: Dock the 24-valve aluminum cylinder head. Fasten 14 head studs to 40 Newton-meters, then apply two 90-degree angle stages from center outward.',
      ta: 'படி 8: 24-வால்வ் சிலிண்டர் ஹெட்டை பொருத்தி, 14 ஹெட் ஸ்டட்களை 40 நியூட்டன் மீட்டரிலும் தொடர்ந்து இரண்டு 90 டிகிரி ஆங்கிளிலும் இறுக்கவும்.',
      ml: 'ഘട്ടം 8: സിലിണ്ടർ ഹെഡ് 40 ന്യൂട്ടൺ മീറ്ററിലും തുടർന്ന് രണ്ട് 90 ഡിഗ്രി ആംഗിളിലും മുറുക്കുക.',
      hi: 'चरण 8: 24-वाल्व सिलेंडर हेड लगाएं। 14 हेड स्टड को 40 न्यूटन मीटर और दो 90 डिग्री चरणों में कसें।'
    },
    tip: 'Spiral torquing order from center to edges prevents warping of the precision machined deck face.',
    colorTag: '#f472b6',
    telemetry: {
      stationCode: 'BMW-ENG-08',
      robotType: 'ABB IRB 4600 Robot Gantry',
      toolBrand: 'Atlas Copco Multi-Nutrunner Head Station',
      cycleTime: '38s Takt',
      laserRunout: 'Deck Flatness: 0.015 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 15, 30, 40]
    },
    specs: [
      { label: 'Cylinder Head Casting', value: 'AlSi10Mg Gravity Die Cast' },
      { label: 'Valve Configuration', value: '4 Valves Per Cylinder (24V Total)' },
      { label: 'Head Stud Fasteners', value: '14x High-Tensile M10 Torx' },
      { label: 'Tightening Protocol', value: '40 Nm + 90° + 90° Angle' }
    ],
    defectConfig: {
      defectName: 'Cylinder Head Deck Warpage Defect',
      defectType: 'Deck Face Planar Distortion',
      paramName: 'Deck Flatness',
      nominal: 0.02,
      defectInitial: 0.15,
      tolerance: 0.03,
      unit: 'mm',
      minVal: 0.0,
      maxVal: 0.20,
      stepSize: 0.01,
      instruction: 'Loosen and re-torque head studs in strict center-outward spiral sequence.'
    }
  },
  {
    id: 9,
    partKey: 'camshafts',
    partName: 'Station 09: Dual Overhead Camshafts (DOHC) & Double-VANOS Phasers',
    partCode: 'S58-CAM-09',
    category: 'Valvetrain Timing Control Cell',
    material: 'Assembled Hollow Camshafts with Induction-Hardened Steel Lobes',
    tool: 'Cam Timing Alignment Fixture & Torque Screwdriver',
    targetTorque: 10,
    requiresTorque: true,
    tolerance: 'Cam Journal Oil Clearance 0.035 - 0.055 mm',
    title: 'DOHC Camshaft Journals Seating & Double-VANOS Phaser Alignment',
    instruction: 'Seat intake and exhaust camshafts in matching numbered bearing caps. Torque caps to 10 Nm and lock VANOS variable phasers with precision alignment tool.',
    voiceScript: 'Station 9: Seat intake and exhaust camshafts in matching numbered bearing caps. Torque caps to 10 Newton-meters and lock VANOS variable phasers.',
    translations: {
      en: 'Station 9: Seat intake and exhaust camshafts in matching numbered bearing caps. Torque caps to 10 Newton-meters and lock VANOS variable phasers.',
      ta: 'படி 9: இன்டேக் மற்றும் எக்ஸ்ஹாஸ்ட் கேம்ஷாஃப்ட்களை பொருத்தி, கேப்ஸ்களை 10 நியூட்டன் மீட்டரில் இறுக்கி வானோஸ் ஸ்ப்ராக்கெட்களை லாக் செய்யவும்.',
      ml: 'ഘട്ടം 9: കാംഷാഫ്റ്റുകൾ ഘടിപ്പിച്ച് 10 ന്യൂട്ടൺ മീറ്ററിൽ മുറുക്കുക.',
      hi: 'चरण 9: इनटेक और एग्जॉस्ट कैमशाफ्ट लगाएं और कैप्स को 10 न्यूटन मीटर पर कसें।'
    },
    tip: 'Ensure camshaft base circles are pointed away from lifters before torquing bearing caps down.',
    colorTag: '#fb7185',
    telemetry: {
      stationCode: 'BMW-ENG-09',
      robotType: 'Staubli TX2-90 Precision Handler',
      toolBrand: 'BMW OEM Cam Timing Alignment Jig',
      cycleTime: '30s Takt',
      laserRunout: 'Cam Runout: 0.008 mm [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 4, 7, 10]
    },
    specs: [
      { label: 'Cam Architecture', value: 'DOHC Double Overhead Camshafts' },
      { label: 'Valvetrain Technology', value: 'Double-VANOS Variable Cam Timing' },
      { label: 'Intake Valve Lift', value: '10.2 mm Maximum' },
      { label: 'Exhaust Valve Lift', value: '9.8 mm Maximum' }
    ],
    defectConfig: {
      defectName: 'Camshaft Journal Oil Clearance Defect',
      defectType: 'Cam Bearing Clearance Too Tight',
      paramName: 'Oil Clearance',
      nominal: 0.045,
      defectInitial: 0.015,
      tolerance: 0.010,
      unit: 'mm',
      minVal: 0.01,
      maxVal: 0.08,
      stepSize: 0.005,
      instruction: 'Fit calibrated cam cap shims to restore 0.045 mm hydrodynamic oil clearance.'
    }
  },
  {
    id: 10,
    partKey: 'timing_chain',
    partName: 'Station 10: Duplex Roller Timing Chain, Slipper Guides & Tensioner',
    partCode: 'S58-TIM-10',
    category: 'Synchronous Drive & Timing Cell',
    material: 'Hardened Alloy Bush Roller Chain & Polyamide Low-Friction Guides',
    tool: 'BMW Engine Timing Tool Kit & Hydraulic Pre-Tensioner Pin Puller',
    targetTorque: 20,
    requiresTorque: true,
    tolerance: 'Timing Sync ±0.5 Crank Degrees',
    title: 'Crankshaft-to-Cam Synchronous Timing Chain Installation',
    instruction: 'Route duplex timing chain around crank and cam sprockets. Install composite guide rails and release hydraulic chain tensioner pin. Rotate crank 720° to verify sync.',
    voiceScript: 'Station 10: Route the duplex timing chain around crank and cam sprockets. Install composite guide rails and release the hydraulic chain tensioner pin.',
    translations: {
      en: 'Station 10: Route the duplex timing chain around crank and cam sprockets. Install composite guide rails and release the hydraulic chain tensioner pin.',
      ta: 'படி 10: டைமிங் செயினை ஸ்ப்ராக்கெட்களை சுற்றி பொருத்தி, கைடு ரெயில்களை அமைத்து ஹைட்ராலிக் டென்ஷனர் பின்னை விடுவிக்கவும்.',
      ml: 'ഘട്ടം 10: ടൈമിംഗ് ചെയിനും ഗൈഡുകളും ഘടിപ്പിച്ച് ടെൻഷനർ റിലീസ് ചെയ്യുക.',
      hi: 'चरण 10: टाइमिंग चेन लगाएं, गाइड रेल फिट करें और हाइड्रोलिक टेंशनर पिन छोड़ें।'
    },
    tip: 'Ensure TDC (Top Dead Center) timing pin is locked in crankshaft flywheel flange during chain setup.',
    colorTag: '#f97316',
    telemetry: {
      stationCode: 'BMW-ENG-10',
      robotType: 'FANUC LR Mate 200iD Timing Robot',
      toolBrand: 'BMW Spec S58 Crank/Cam Lock Kit',
      cycleTime: '34s Takt',
      laserRunout: 'Timing Error: +0.2° [PASS]',
      heliumDecay: 'N/A',
      torqueCurve: [0, 8, 14, 20]
    },
    specs: [
      { label: 'Chain Type', value: 'Heavy-Duty 8mm Duplex Roller Chain' },
      { label: 'Tensioner', value: 'Hydraulic Oil-Damped Spring Loaded' },
      { label: 'Guide Material', value: 'Glass-Fiber Reinforced Polyamide 66' },
      { label: 'Timing Tolerance', value: '±0.5° Camshaft Phase Sync' }
    ],
    defectConfig: {
      defectName: 'Cam-to-Crank Timing Phase Tooth Offset',
      defectType: 'Timing Chain 1-Tooth Retard Error',
      paramName: 'Timing Offset',
      nominal: 0.0,
      defectInitial: 7.5,
      tolerance: 1.0,
      unit: '°',
      minVal: -10.0,
      maxVal: 10.0,
      stepSize: 1.0,
      instruction: 'Re-align chain timing marks with laser index on VANOS cam sprockets.'
    }
  },
  {
    id: 11,
    partKey: 'valve_cover',
    partName: 'Station 11: Magnesium Valve Cover & 6x Direct Ignition Coil Packs',
    partCode: 'S58-COV-11',
    category: 'Upper Engine Dress & Ignition Cell',
    material: 'Ultralight Die-Cast Magnesium with Carbon Fiber M-Power Shield',
    tool: 'Cordless Micro-Torque Driver (T30 Torx)',
    targetTorque: 9,
    requiresTorque: true,
    tolerance: 'Torque 9 Nm Consistent',
    title: 'Magnesium Valve Cover Sealing & Coil-on-Plug Ignition Modules',
    instruction: 'Install magnesium valve cover with pre-molded elastomer seal. Fasten perimeter Torx bolts to 9 Nm and insert 6 direct ignition coil packs with silicone dielectric boots.',
    voiceScript: 'Station 11: Install the magnesium valve cover with pre-molded elastomer seal. Fasten perimeter Torx bolts to 9 Newton-meters and insert 6 ignition coils.',
    translations: {
      en: 'Station 11: Install the magnesium valve cover with pre-molded elastomer seal. Fasten perimeter Torx bolts to 9 Newton-meters and insert 6 ignition coils.',
      ta: 'படி 11: மெக்னீசியம் வால்வ் கவரை பொருத்தி 9 நியூட்டன் மீட்டரில் இறுக்கவும். 6 இக்னிஷன் காயில்களை செருகவும்.',
      ml: 'ഘട്ടം 11: വാൽവ് കവർ 9 ന്യൂട്ടൺ മീറ്ററിൽ ഘടിപ്പിച്ച് ഇഗ്നിഷൻ കോയിലുകൾ സ്ഥാപിക്കുക.',
      hi: 'चरण 11: मैग्नीशियम वाल्व कवर 9 न्यूटन मीटर पर लगाएं और 6 इग्निशन कॉइल्स लगाएं।'
    },
    tip: 'Magnesium valve cover isolates valvetrain acoustics and reduces top-end center of gravity.',
    colorTag: '#eab308',
    telemetry: {
      stationCode: 'BMW-ENG-11',
      robotType: 'Staubli TS2-80 Fastener Robot',
      toolBrand: 'Desoutter Micro-Torque T30 Driver',
      cycleTime: '26s Takt',
      laserRunout: 'Coil Insertion: 24.0 mm flush [PASS]',
      heliumDecay: '0.00 mbar/s [HERMETIC]',
      torqueCurve: [0, 3, 6, 9]
    },
    specs: [
      { label: 'Cover Construction', value: 'High-Pressure Die-Cast Magnesium' },
      { label: 'Ignition Architecture', value: 'Direct Coil-on-Plug (COP) 6x' },
      { label: 'PCV System', value: 'Integrated Oil Cyclone Separator' },
      { label: 'Cover Shield', value: 'Real Pre-Preg Carbon Fiber' }
    ],
    defectConfig: {
      defectName: 'Valve Cover Perimeter Seal Disparity',
      defectType: 'Elastomer Gasket Pinching',
      paramName: 'Gasket Compression',
      nominal: 1.2,
      defectInitial: 0.3,
      tolerance: 0.2,
      unit: 'mm',
      minVal: 0.2,
      maxVal: 1.8,
      stepSize: 0.1,
      instruction: 'Evenly tighten perimeter Torx bolts to 9 Nm to compress gasket to 1.2 mm.'
    }
  },
  {
    id: 12,
    partKey: 'turbocharger',
    partName: 'Station 12: Twin-Scroll Exhaust Turbocharger & Electronic Wastegate',
    partCode: 'S58-TRB-12',
    category: 'Forced Induction & Exhaust Cell',
    material: 'Inconel Heat-Resistant Turbine Housing & Billet Milled Compressor',
    tool: 'High-Temp Copper Anti-Seize Applicator & V-Band Torque Wrench',
    targetTorque: 35,
    requiresTorque: true,
    tolerance: 'Turbine Shaft Radial Play < 0.04 mm',
    title: 'Twin-Scroll Turbocharger Mounting & Electronic Wastegate Calibration',
    instruction: 'Mount twin-scroll turbocharger onto divided exhaust manifold. Fasten Inconel studs to 35 Nm. Connect electronic wastegate actuator and oil feed/drain lines. Engine assembly certified!',
    voiceScript: 'Station 12: Mount the twin-scroll turbocharger onto the divided exhaust manifold. Fasten Inconel studs to 35 Newton-meters and connect the electronic wastegate. Engine assembly successfully certified!',
    translations: {
      en: 'Station 12: Mount the twin-scroll turbocharger onto the divided exhaust manifold. Fasten Inconel studs to 35 Newton-meters and connect the electronic wastegate. Engine assembly successfully certified!',
      ta: 'படி 12: இரட்டை-ஸ்க்ரோல் டர்போசார்ஜரை எக்ஸ்ஹாஸ்ட் மேனிஃபோல்டில் பொருத்தி, 35 நியூட்டன் மீட்டரில் இறுக்கவும். என்ஜின் அசெம்பிளி வெற்றிகரமாக முடிந்தது!',
      ml: 'ഘട്ടം 12: ട്വിൻ-സ്ക്രോൾ ടർബോചാർജർ 35 ന്യൂട്ടൺ മീറ്ററിൽ ഘടിപ്പിക്കുക. എഞ്ചിൻ അസംബ്ലി പൂർത്തിയായി.',
      hi: 'चरण 12: ट्विन-स्क्रॉल टर्बोचार्जर लगाएं और 35 न्यूटन मीटर पर कसें। इंजन असेंबली पूरी हुई!'
    },
    tip: 'Pre-prime turbocharger center bearing cartridge with 20ml fresh engine oil before first start.',
    colorTag: '#10b981',
    telemetry: {
      stationCode: 'BMW-ENG-12',
      robotType: 'KUKA KR 30-3 Heavy Handler',
      toolBrand: 'Atlas Copco High-Temp V-Band Wrench',
      cycleTime: '36s Takt',
      laserRunout: 'Radial Play: 0.022 mm [PASS]',
      heliumDecay: '0.00 mbar/s [HERMETIC]',
      torqueCurve: [0, 12, 24, 35]
    },
    specs: [
      { label: 'Turbo Technology', value: 'Mono-Scroll Divided Twin-Scroll Housing' },
      { label: 'Turbine Wheel', value: 'Inconel 713C Superalloy' },
      { label: 'Compressor Wheel', value: 'Billet CNC Forged Aluminum' },
      { label: 'Wastegate Control', value: 'High-Speed Electronic Servo Motor' }
    ],
    defectConfig: {
      defectName: 'Turbine Shaft Radial Free-Play Defect',
      defectType: 'Excessive Journal Bearing Play',
      paramName: 'Shaft Play',
      nominal: 0.025,
      defectInitial: 0.12,
      tolerance: 0.02,
      unit: 'mm',
      minVal: 0.01,
      maxVal: 0.15,
      stepSize: 0.005,
      instruction: 'Inspect CHRA ceramic bearings to eliminate shaft wobble below 0.04 mm.'
    }
  }
];

export const COMPONENT_MODULES = {
  brake: {
    id: 'brake',
    title: '🏎️ Ventilated Disc Brake Assembly (Braking Module)',
    subTitle: '320mm Front Axle Vented Rotor & Brembo Caliper',
    cadFileName: 'Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj',
    cadPath: '/models/Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj',
    steps: ASSEMBLY_STEPS
  },
  clutch: {
    id: 'clutch',
    title: '⚙️ Clutch & Pressure Plate Assembly (Transmission Module)',
    subTitle: '280mm Single-Plate Dry Clutch & Diaphragm Belleville Spring',
    cadFileName: 'Automotive_Clutch_and_Pressure_Plate_Assembly.obj',
    cadPath: '/models/Automotive_Clutch_and_Pressure_Plate_Assembly.obj',
    steps: CLUTCH_ASSEMBLY_STEPS
  },
  engine: {
    id: 'engine',
    title: '⚡ BMW S58 TwinPower Turbo Engine Core (Powertrain Module)',
    subTitle: '3.0L Inline-6 DOHC · Closed-Deck Block · Forged Crank · H-Beam Rods · MLS Gasket · Twin-Scroll Turbo',
    cadFileName: 'BMW_S58_TwinPower_Turbo_Engine_Core.obj',
    cadPath: '/models/BMW_S58_TwinPower_Turbo_Engine_Core.obj',
    steps: ENGINE_ASSEMBLY_STEPS
  },
  car: {
    id: 'car',
    title: '🏎️ BMW M-Series Complete Body Assembly (M Division Engineering)',
    subTitle: 'Carbon Core Chassis · 4.4L V8 TwinTurbo · M-Adaptive Suspension · Kidney Grille · M-Forged Wheels',
    cadFileName: 'BMW_M_Series_Complete_Body_Assembly.obj',
    cadPath: '/models/BMW_M_Series_Complete_Body_Assembly.obj',
    steps: FULL_CAR_ASSEMBLY_STEPS
  },
  knuckle: {
    id: 'knuckle',
    title: '🦾 Mechanical Knuckle Joint Assembly (Kinematic Linkage)',
    subTitle: 'Fork End, Eye End, 30mm Pivot Pin, Collar & 1:30 Taper Split Pin',
    cadFileName: 'Knuckle_Joint_Assembly.obj',
    cadPath: '/models/Knuckle_Joint_Assembly.obj',
    steps: KNUCKLE_JOINT_STEPS
  }
};


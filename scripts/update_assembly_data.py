import os

new_brake_and_clutch_content = '''// Automotive Disc Brake System Assembly Specification Data
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
'''

with open('src/components/assemblyData.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find export const FULL_CAR_ASSEMBLY_STEPS
marker = 'export const FULL_CAR_ASSEMBLY_STEPS'
idx = content.find(marker)
if idx == -1:
    print('Error: Could not find marker!')
    exit(1)

rest_of_file = content[idx:]
full_new_content = new_brake_and_clutch_content + '\n' + rest_of_file

with open('src/components/assemblyData.js', 'w', encoding='utf-8') as f:
    f.write(full_new_content)

print('Successfully updated assemblyData.js! Total characters:', len(full_new_content))

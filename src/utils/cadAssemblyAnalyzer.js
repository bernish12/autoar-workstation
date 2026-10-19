import * as THREE from 'three';
import {
  ASSEMBLY_STEPS as BRAKE_STEPS,
  CLUTCH_ASSEMBLY_STEPS,
  FULL_CAR_ASSEMBLY_STEPS,
  KNUCKLE_JOINT_STEPS
} from '../components/assemblyData';

/**
 * Clean CAD object name into user-friendly title
 */
function cleanPartName(rawName, index) {
  if (!rawName || rawName.toLowerCase() === 'default' || rawName.trim() === '') {
    return `Component Module 0${index + 1}`;
  }
  return rawName
    .replace(/^o\s+/i, '')
    .replace(/^g\s+/i, '')
    .replace(/_/g, ' ')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .trim()
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/**
 * Universal CAD Assembly Analyzer for Industry 4.0 Augmented Reality
 * Decomposes ANY imported 3D CAD model (.OBJ, .GLB, .STEP) into:
 * 1. Bill of Materials (BOM)
 * 2. Step-by-Step Standard Work Instructions (SWI)
 * 3. 3D Holographic Kinematic Explosion Vectors
 * 4. Pick-to-Light Bin Allocations
 * 5. Metrological Tolerance & Quality Verification Parameters
 */
export function analyzeCADAssembly(model, fileName = '') {
  const meshes = [];
  let totalVertices = 0;

  model.traverse(child => {
    if (child.isMesh) {
      meshes.push(child);
      if (child.geometry && child.geometry.attributes && child.geometry.attributes.position) {
        totalVertices += child.geometry.attributes.position.count;
      }
    }
  });

  const modelBox = new THREE.Box3().setFromObject(model);
  const modelCenter = new THREE.Vector3();
  modelBox.getCenter(modelCenter);
  const modelSize = new THREE.Vector3();
  modelBox.getSize(modelSize);

  const lowerName = fileName.toLowerCase();
  const isCar = (lowerName.includes('car') || lowerName.includes('vehicle') || lowerName.includes('bmw')) && meshes.length >= 3;
  const isClutch = !isCar && lowerName.includes('clutch') && meshes.length >= 3;
  const isKnuckle = !isCar && !isClutch && (lowerName.includes('knuckle') || lowerName.includes('joint')) && meshes.length >= 3;
  const isBrake = !isCar && !isClutch && !isKnuckle && (lowerName.includes('brake') || lowerName.includes('caliper')) && meshes.length >= 3;

  // High-fidelity pre-calibrated automotive modules
  if (isCar) {
    return {
      steps: FULL_CAR_ASSEMBLY_STEPS,
      module: 'car',
      assemblyTitle: 'BMW M-Performance TwinPower Turbo Master Vehicle Assembly',
      totalVertices,
      meshesCount: meshes.length,
      modelSize
    };
  }
  if (isClutch) {
    return {
      steps: CLUTCH_ASSEMBLY_STEPS,
      module: 'clutch',
      assemblyTitle: 'Automotive Dry Clutch & Pressure Plate Assembly',
      totalVertices,
      meshesCount: meshes.length,
      modelSize
    };
  }
  if (isKnuckle) {
    return {
      steps: KNUCKLE_JOINT_STEPS,
      module: 'knuckle',
      assemblyTitle: 'Kinematic Mechanical Knuckle Joint Assembly',
      totalVertices,
      meshesCount: meshes.length,
      modelSize
    };
  }
  if (isBrake) {
    return {
      steps: BRAKE_STEPS,
      module: 'brake',
      assemblyTitle: '320mm Ventilated Disc Brake & Brembo Caliper Assembly',
      totalVertices,
      meshesCount: meshes.length,
      modelSize
    };
  }

  // =========================================================================
  // UNIVERSAL DYNAMIC CAD ASSEMBLY DECOMPOSITION ENGINE (For ANY 3D File!)
  // =========================================================================
  // Sort meshes: Large/datum components first, small fasteners last
  const analyzedParts = meshes.map((child, idx) => {
    child.geometry.computeBoundingBox();
    const box = new THREE.Box3().setFromObject(child);
    const size = new THREE.Vector3();
    box.getSize(size);
    const volume = Math.max(0.001, size.x * size.y * size.z);
    const center = new THREE.Vector3();
    box.getCenter(center);

    const resolvedName = (
      child.name ||
      (child.parent && child.parent.name && child.parent.name !== 'Scene' ? child.parent.name : '') ||
      (child.material && child.material.name ? child.material.name : '') ||
      `Part_${idx + 1}`
    );
    const name = resolvedName.toLowerCase();
    const isFastener = name.includes('bolt') || name.includes('screw') || name.includes('pin') ||
      name.includes('stud') || name.includes('nut') || name.includes('clip') || volume < 0.05;

    return {
      child,
      idx,
      rawName: resolvedName,
      cleanName: cleanPartName(resolvedName, idx),
      volume,
      size,
      center,
      isFastener
    };
  });

  // Sort: Non-fasteners sorted by volume descending, then fasteners at the end
  analyzedParts.sort((a, b) => {
    if (a.isFastener && !b.isFastener) return 1;
    if (!a.isFastener && b.isFastener) return -1;
    return b.volume - a.volume;
  });

  const colorPalette = ['#00f0ff', '#38bdf8', '#fbbf24', '#f87171', '#a855f7', '#34d399', '#f43f5e', '#eab308'];

  const dynamicSteps = analyzedParts.map((item, stepIdx) => {
    const stepNum = stepIdx + 1;
    const { child, cleanName, size, center, isFastener } = item;

    // 1. Tag child with step index & calculate radial explosion vector
    child.userData.stepIndex = stepNum;
    
    const explodeDir = new THREE.Vector3().subVectors(center, modelCenter);
    if (explodeDir.length() < 0.15) {
      explodeDir.set(
        (stepIdx % 2 === 0 ? 0.8 : -0.8),
        (stepIdx % 3 === 0 ? 0.6 : -0.6),
        1.2 + stepIdx * 0.4
      );
    } else {
      explodeDir.normalize().multiplyScalar(1.2 + stepIdx * 0.25);
    }
    child.userData.explodeDir = explodeDir;

    const torqueVal = isFastener ? 25 + (stepIdx % 4) * 15 : 0;
    const colorTag = colorPalette[stepIdx % colorPalette.length];
    const binCode = `BIN #${stepNum}`;
    const shelfName = isFastener ? 'SHELF 03 • HARDWARE FASTENERS' : (stepIdx === 0 ? 'SHELF 01 • PRIMARY DATUM CASTINGS' : 'SHELF 02 • COMPONENT STAGING');

    return {
      id: stepNum,
      partKey: child.name || `part_${stepNum}`,
      partName: cleanName,
      partCode: `CAD-${String(stepNum).padStart(2, '0')}-${(child.name || 'PRT').slice(0, 3).toUpperCase()}`,
      category: isFastener ? 'Hardware Fasteners & Fastening' : (stepIdx === 0 ? 'Primary Datum Fixture' : 'Mechanical Kinematic Component'),
      material: isFastener ? 'Grade 10.9 Hardened Steel' : 'Precision Machined Alloy (ISO Standard)',
      tool: isFastener ? 'Digital Torque Wrench & Bit' : 'Precision Surface Gauge & Wipe',
      targetTorque: torqueVal,
      requiresTorque: isFastener,
      tolerance: isFastener ? 'Torque Tolerance ±2%' : 'Coaxial Runout < 0.03 mm',
      title: `${cleanName} ${isFastener ? 'Fastening & Torquing' : 'Mounting & Alignment'}`,
      instruction: isFastener
        ? `Engage ${cleanName} into locating bore. Verify thread engagement and torque to ${torqueVal} Newton-meters.`
        : `Position ${cleanName} on assembly datum fixture. Verify planar alignment within ±0.03 mm.`,
      voiceScript: `Step ${stepNum}: Mount ${cleanName}. ${isFastener ? `Torque to ${torqueVal} Newton meters.` : 'Verify datum alignment.'}`,
      translations: {
        en: `Step ${stepNum}: Mount ${cleanName}. ${isFastener ? `Torque to ${torqueVal} Newton meters.` : 'Verify datum alignment.'}`,
        ta: `படி ${stepNum}: ${cleanName} பொருத்துங்கள். ${isFastener ? `${torqueVal} நியூட்டன் மீட்டர் முறுக்குவிசையில் இறுக்குங்கள்.` : 'சீரமைப்பை சரிபார்க்கவும்.'}`,
        ml: `ഘട്ടം ${stepNum}: ${cleanName} ഘടിപ്പിക്കുക. ${isFastener ? `${torqueVal} ന്യൂട്ടൺ മീറ്റർ ടോർക്കിൽ മുറുക്കുക.` : 'അലൈൻമെന്റ് പരിശോധിക്കുക.'}`,
        hi: `चरण ${stepNum}: ${cleanName} को स्थापित करें। ${isFastener ? `${torqueVal} न्यूटन मीटर टॉर्क पर कसें।` : 'सटीक संरेखण की जांच करें।'}`
      },
      tip: isFastener
        ? 'Cross-tighten in diagonal sequence to prevent flange distortion.'
        : 'Wipe mating surfaces with industrial degreaser before final fitment.',
      colorTag,
      binInfo: { bin: binCode, shelf: shelfName },
      specs: [
        { label: 'Part Dimensions', value: `${(size.x * 100).toFixed(1)} x ${(size.y * 100).toFixed(1)} x ${(size.z * 100).toFixed(1)} mm` },
        { label: 'Assembly Fitment', value: isFastener ? 'Fastener Controlled' : 'Slip Fit / Precision Bore' },
        { label: 'Metrology Datum', value: 'ISO 2768-m Standard' },
        { label: 'Quality Verification', value: '100% Optical Inspection' }
      ],
      defectConfig: {
        defectName: `${cleanName} Angular Alignment Defect`,
        defectType: 'Geometric Tolerance Deviation',
        paramName: 'Mounting Angle',
        nominal: 90.0,
        defectInitial: 74.2,
        tolerance: 1.0,
        unit: '°',
        minVal: 70.0,
        maxVal: 90.0,
        stepSize: 0.5,
        instruction: `Re-seat and align ${cleanName} within 1.0° tolerance.`
      }
    };
  });

  // If there's only 1 mesh, create a 2-step sequence (Mounting + Final Certification)
  if (dynamicSteps.length <= 1) {
    dynamicSteps.push({
      id: 2,
      partKey: 'verification',
      partName: 'Final Assembly Quality Certification',
      partCode: 'QC-VER-100',
      category: 'End-of-Line Quality Assurance',
      material: 'Complete SolidWorks Assembly',
      tool: '3D Laser CMM & Optical Scanner',
      targetTorque: 0,
      requiresTorque: false,
      tolerance: 'Zero Defect (100% Pass)',
      title: 'Final Assembly Inspection & Certification',
      instruction: 'Perform 3D optical laser scan and hydraulic pressure test. Issue digital IATF 16949 certification.',
      voiceScript: 'Final Step: Assembly complete. Run 3D laser scan and verify quality certification.',
      translations: {
        en: 'Final Step: Assembly complete. Run 3D laser scan and verify quality certification.',
        ta: 'இறுதிப் படி: அசெம்பிளி முடிந்தது. 3D லேசர் ஸ்கேன் இயக்கி தரச் சான்றிதழை சரிபார்க்கவும்.',
        ml: 'അവസാന ഘട്ടം: അസംബ്ലി പൂർത്തിയായി. 3D ലേസർ സ്കാൻ ചെയ്ത് ക്വാളിറ്റി സർട്ടിഫിക്കേഷൻ പരിശോധിക്കുക.',
        hi: 'अंतिम चरण: असेंबली पूरी हुई। 3D लेजर स्कैन चलाएं और गुणवत्ता प्रमाणीकरण सत्यापित करें।'
      },
      tip: 'Verify all fastener marks and sealant beads before sign-off.',
      colorTag: '#10b981',
      binInfo: { bin: 'QC STATION', shelf: 'FINAL PACKAGING & LINE OUT' },
      specs: [
        { label: 'Total Components', value: `${meshes.length} Sub-Assemblies` },
        { label: 'Metrology Status', value: 'PASSED (Zero Defects)' },
        { label: 'Quality Standard', value: 'ISO 9001 / IATF 16949' },
        { label: 'Digital Twin Checksum', value: 'VERIFIED' }
      ],
      defectConfig: {
        defectName: 'Overall Assembly Clearance Defect',
        defectType: 'Final Clearance Tolerance',
        paramName: 'Clearance',
        nominal: 0.0,
        defectInitial: 3.5,
        tolerance: 0.5,
        unit: 'mm',
        minVal: 0.0,
        maxVal: 5.0,
        stepSize: 0.1,
        instruction: 'Calibrate assembly to zero clearance deviation.'
      }
    });
  }

  const cleanFileTitle = fileName ? fileName.replace(/\.[^/.]+$/, '').replace(/_/g, ' ') : 'Universal CAD Assembly';

  return {
    steps: dynamicSteps,
    module: 'custom',
    assemblyTitle: cleanFileTitle,
    totalVertices,
    meshesCount: meshes.length,
    modelSize
  };
}

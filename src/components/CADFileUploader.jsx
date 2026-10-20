import React, { useState, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { soundFx } from '../utils/audio';

export function applyPBRMaterials(obj) {
  // 1. Propagate group names down to child meshes so OBJLoader groups are fully identified
  obj.traverse(child => {
    if ((child.isGroup || child.type === 'Group' || child.type === 'Object3D') && child.name) {
      child.children.forEach(c => {
        if (!c.name || c.name === 'default' || c.name === '') {
          c.name = child.name;
        }
      });
    }
  });

  obj.traverse(child => {
    if (child.isMesh) {
      const resolvedName = (
        child.name ||
        (child.parent && child.parent.name && child.parent.name !== 'Scene' ? child.parent.name : '') ||
        (child.material && child.material.name ? child.material.name : '') ||
        ''
      );
      if (!child.name && resolvedName) {
        child.name = resolvedName;
      }
      const name = resolvedName.toLowerCase();
      child.castShadow = true;
      child.receiveShadow = true;

      // 0. Brembo Raised White Racing Emblem
      if (name.includes('emblem') || name.includes('branding')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xffffff,
          metalness: 0.1,
          roughness: 0.2,
          emissive: new THREE.Color(0xffffff),
          emissiveIntensity: 0.35,
          name: 'bremboBadgeMat'
        });
      }
      // 1. Cross-drilled ventilation holes and slotted racing grooves (High-contrast deep carbon)
      else if (name.includes('crossdrilled') || name.includes('slotted') || name.includes('groove')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x151921, // Deep contrasting carbon steel chamfer
          metalness: 0.88,
          roughness: 0.38,
          name: 'drilledGrooveMat'
        });
      }
      // 2. Floating Bobbins & Hardware Fasteners
      else if (name.includes('bobbin') || name.includes('hardware')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xe2e8f0, // Polished Stainless Steel Bobbins
          metalness: 0.95,
          roughness: 0.12,
          name: 'bobbinMat'
        });
      }
      // 3. Chrome Hydraulic Pistons
      else if (name.includes('piston')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf8fafc, // Mirror Polished Chrome Pistons
          metalness: 0.98,
          roughness: 0.06,
          name: 'pistonMat'
        });
      }
      // 4. Anodized Bell Hat (Gunmetal Titanium)
      else if (name.includes('hat') || name.includes('bell')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x1e2430, // Gunmetal Anodized Aluminum Bell
          metalness: 0.76,
          roughness: 0.28,
          name: 'hatMat'
        });
      }
      // 5. ABS Tone Ring & Active Sensor
      else if (name.includes('abs') || name.includes('tone') || name.includes('sensor')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x334155,
          metalness: 0.82,
          roughness: 0.28,
          name: 'absSensorMat'
        });
      }
      // 6. Stainless Anti-Rattle Shims & Spring Clips
      else if (name.includes('shim') || name.includes('spring') || name.includes('clip')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xcfd8dc, // Silver Spring Steel
          metalness: 0.92,
          roughness: 0.16,
          name: 'shimClipMat'
        });
      }
      // 7. Caliper Body (Brembo Corsa Racing Red with High-Gloss Clearcoat)
      else if (name.includes('caliper') || name.includes('cylinder') || name.includes('red')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xd91424, // Authentic Brembo Corsa Racing Red
          metalness: 0.18,
          roughness: 0.14,
          clearcoat: 1.0,
          clearcoatRoughness: 0.05,
          name: 'caliperMat'
        });
      }
      // 8. 320mm Ventilated Friction Rings (Bright Machined Steel)
      else if (name.includes('rotor') || name.includes('disc') || name.includes('vanes')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xd8dde4, // High-Carbon Lathe-Turned Alloy Steel
          metalness: 0.88,
          roughness: 0.22,
          name: 'rotorMat'
        });
      }
      // 9. Wheel Hub and Spindle (Forged Steel)
      else if (name.includes('hub') || name.includes('spindle')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x94a3b8, // Forged Heavy Alloy Steel
          metalness: 0.84,
          roughness: 0.24,
          name: 'hubMat'
        });
      }
      // 10. Bolts, Studs & Chrome Lug Nuts
      else if (name.includes('bolt') || name.includes('stud') || name.includes('fastener') || name.includes('pin') || name.includes('nut')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xffffff, // Mirror Chrome Fasteners & Lug Nuts
          metalness: 0.98,
          roughness: 0.05,
          name: 'boltMat'
        });
      }
      // 11. Caliper Mounting Anchor Bracket (Cast Ductile Iron)
      else if (name.includes('bracket')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x334155, // Cast Ductile Iron Mounting Bracket
          metalness: 0.78,
          roughness: 0.35,
          name: 'bracketMat'
        });
      }
      // 12. Ceramic Brake Pads
      else if (name.includes('pad')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x475569, // Sintered High-Friction Ceramic Matrix
          metalness: 0.40,
          roughness: 0.65,
          name: 'padMat'
        });
      }
      // 5. Clutch: Pilot Bearing & Needle Rollers
      else if (name.includes('pilot') || name.includes('needle')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xcfd8dc, // Hardened 100Cr6 Chromium Bearing Steel
          metalness: 0.94,
          roughness: 0.12,
          name: 'pilotBearingMat'
        });
      }
      // 6. Clutch: Dual-Mass Flywheel & Starter Ring
      else if (name.includes('flywheel') || name.includes('dmf') || name.includes('ring_gear')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x94a3b8, // Heavy Ductile Cast Iron
          metalness: 0.82,
          roughness: 0.26,
          name: 'flywheelMat'
        });
      }
      // 7. Clutch: Crankshaft Stretch Bolts
      else if (name.includes('crank') && name.includes('bolt')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x1e293b, // Grade 12.9 Black Oxide High-Tensile Steel
          metalness: 0.92,
          roughness: 0.28,
          name: 'crankBoltMat'
        });
      }
      // 8. Clutch: Transmission Input Spline Shaft
      else if (name.includes('spline') || name.includes('input_shaft')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x475569, // MoS2 Micro-Dosed Hardened Spline Steel
          metalness: 0.88,
          roughness: 0.32,
          name: 'splineShaftMat'
        });
      }
      // 9. Clutch: Friction Disc lining & dampening springs
      else if (name.includes('friction') || name.includes('damper')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x334155, // High-Friction Organic Composite
          metalness: 0.35,
          roughness: 0.65,
          name: 'frictionDiscMat'
        });
      }
      // 10. Clutch: Centering Arbor Alignment Mandrel
      else if (name.includes('mandrel') || name.includes('arbor')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x06b6d4, // Anodized Cobalt Cyan Tool Steel
          metalness: 0.85,
          roughness: 0.18,
          clearcoat: 0.85,
          clearcoatRoughness: 0.08,
          name: 'mandrelMat'
        });
      }
      // 11. Clutch: Cast Iron Pressure Plate Clamping Ring
      else if (name.includes('pressure') || name.includes('clamping')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xd1d5db, // Ground Flat Pearlitic Grey Cast Iron
          metalness: 0.85,
          roughness: 0.20,
          name: 'pressurePlateMat'
        });
      }
      // 12. Clutch: Diaphragm Belleville Spring Fingers (Tempered Blue Spring Steel)
      else if (name.includes('diaphragm') || (name.includes('spring') && !name.includes('damper') && !name.includes('sac'))) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x3b82f6, // Tempered Blue Spring Steel Fingers
          metalness: 0.92,
          roughness: 0.15,
          name: 'diaphragmMat'
        });
      }
      // 13. Clutch: SAC Adjuster Ratchet Ring
      else if (name.includes('sac') || name.includes('ratchet')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf59e0b, // PA66 Glass-Filled Polyamide & Steel Ratchet
          metalness: 0.72,
          roughness: 0.24,
          name: 'sacRatchetMat'
        });
      }
      // 14. Clutch: Stamped Steel Cover Housing (Gold-Zinc Dichromate)
      else if (name.includes('cover') || name.includes('housing')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xeab308, // Automotive Yellow-Zinc Dichromate Gold Finish
          metalness: 0.78,
          roughness: 0.22,
          clearcoat: 0.70,
          clearcoatRoughness: 0.12,
          name: 'clutchCoverMat'
        });
      }
      // 15. Clutch: Release Bearing (Mirror Chrome)
      else if (name.includes('bearing') || name.includes('release')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf8fafc, // Polished Chrome Bearing Steel
          metalness: 0.98,
          roughness: 0.06,
          name: 'bearingMat'
        });
      }

      // 12. Full Car: BMW M-Series Specific Components
      else if (name.includes('kidney') || name.includes('grille_fascia')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x09090b, // High-Gloss Shadowline Black & Chrome Trim
          metalness: 0.95,
          roughness: 0.05,
          clearcoat: 1.0,
          clearcoatRoughness: 0.03,
          name: 'bmwGrilleMat'
        });
      }
      else if (name.includes('headlight') || name.includes('laser')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xe0f2fe, // BMW Icon Adaptive LED / Laserlight
          emissive: 0x00f0ff,
          emissiveIntensity: 0.45,
          transparent: true,
          opacity: 0.85,
          roughness: 0.06,
          metalness: 0.15,
          name: 'bmwHeadlightMat'
        });
      }
      else if (name.includes('glass') || name.includes('greenhouse') || name.includes('windshield') || name.includes('glazing')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x0f172a, // Lightweight Acoustic Sun-Protection Smoked Glass
          transparent: true,
          opacity: 0.45,
          roughness: 0.04,
          metalness: 0.15,
          transmission: 0.45,
          ior: 1.52,
          name: 'bmwGlassMat'
        });
      }
      else if (name.includes('wiring') || name.includes('harness')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf97316, // High-Voltage 48V Automotive Orange Conduit & Copper Loom
          metalness: 0.40,
          roughness: 0.35,
          name: 'bmwWiringMat'
        });
      }
      else if (name.includes('seat')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x18181b, // M Carbon Racing Bucket Shell & Merino Leather
          metalness: 0.50,
          roughness: 0.50,
          name: 'bmwSeatMat'
        });
      }
      else if (name.includes('door')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x0f4c81, // BMW Marina Bay Blue Metallic Door Panels
          metalness: 0.92,
          roughness: 0.08,
          clearcoat: 1.0,
          clearcoatRoughness: 0.04,
          name: 'bmwDoorMat'
        });
      }
      else if (name.includes('exhaust')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xffffff, // Polished Quad Chrome / Stainless Steel Exhaust Tailpipes
          metalness: 0.98,
          roughness: 0.05,
          name: 'bmwExhaustMat'
        });
      }
      else if (name.includes('interior') || name.includes('cockpit')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x18181b, // Merino Black Leather & M Carbon Cockpit
          metalness: 0.35,
          roughness: 0.60,
          name: 'bmwInteriorMat'
        });
      }
      else if (name.includes('tire')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x111827, // Michelin Pilot Sport 4S Silica Radial Rubber
          metalness: 0.10,
          roughness: 0.80,
          name: 'bmwTireMat'
        });
      }
      else if (name.includes('forged') || name.includes('alloy') || (name.includes('wheel') && !name.includes('flywheel'))) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x1e293b, // M-Forged Bicolor Double-Spoke Style 826M
          metalness: 0.88,
          roughness: 0.18,
          clearcoat: 0.85,
          clearcoatRoughness: 0.08,
          name: 'bmwWheelMat'
        });
      }
      else if (name.includes('diffuser') || name.includes('splitter') || name.includes('aerodynamics')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x18181b, // Autoclave-Cured CFRP Carbon Fiber Aero
          metalness: 0.85,
          roughness: 0.32,
          name: 'bmwCarbonAeroMat'
        });
      }
      // BMW M Marina Bay Blue Metallic Body Shell & Power Dome Hood
      else if (name.includes('body') || name.includes('shell') || name.includes('hood') || name.includes('powerdome') || name.includes('canopy') || name.includes('spoiler') || name.includes('mirror')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x0f4c81, // Authentic BMW M Marina Bay Blue Metallic
          metalness: 0.92,
          roughness: 0.08,
          clearcoat: 1.0,
          clearcoatRoughness: 0.04,
          name: 'bmwBodyShellMat'
        });
      }
      // BMW Carbon Core & Lightweight Spaceframe
      else if (name.includes('chassis') || name.includes('spaceframe') || name.includes('frame') || name.includes('cage')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x1e293b, // Dark Carbon Core Composite & Satin Frame
          metalness: 0.85,
          roughness: 0.25,
          name: 'bmwChassisMat'
        });
      }
      // BMW S58 TwinPower Turbo Engine Core Specific Components
      else if (name.includes('block') || name.includes('cylinder_bank')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x94a3b8, // Closed-Deck AlSiCu Cast Aluminum Block
          metalness: 0.84,
          roughness: 0.22,
          name: 'engineBlockMat'
        });
      }
      else if (name.includes('crankshaft') || name.includes('crankpin')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf1f5f9, // Micro-Finished Forged 42CrMo4 Steel
          metalness: 0.96,
          roughness: 0.08,
          name: 'crankshaftMat'
        });
      }
      else if (name.includes('bedplate')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x64748b, // High-Rigidity Cast Aluminum Bedplate
          metalness: 0.82,
          roughness: 0.26,
          name: 'bedplateMat'
        });
      }
      else if (name.includes('connecting_rod') || name.includes('h_beam') || name.includes('rod')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xcfd8dc, // Forged 4340 Chromoly Steel H-Beam
          metalness: 0.90,
          roughness: 0.16,
          name: 'rodMat'
        });
      }
      else if (name.includes('piston')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xd4d4d8, // Forged 2618 Aluminum Alloy with Grafal Skirt
          metalness: 0.88,
          roughness: 0.14,
          name: 'pistonMat'
        });
      }
      else if (name.includes('oil_sump') || name.includes('oil_pan') || name.includes('sump')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x475569, // Cast Aluminum Oil Pan Sump
          metalness: 0.78,
          roughness: 0.30,
          name: 'oilPanMat'
        });
      }
      else if (name.includes('gasket') || name.includes('mls')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xb45309, // 5-Layer Embossed Stainless Steel with Viton Fire-Rings
          metalness: 0.92,
          roughness: 0.14,
          name: 'headGasketMat'
        });
      }
      else if (name.includes('cylinder_head') || name.includes('dohc_head') || (name.includes('head') && !name.includes('headlight'))) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xa1a1aa, // CNC Ported Aluminum Cylinder Head
          metalness: 0.84,
          roughness: 0.22,
          name: 'cylinderHeadMat'
        });
      }
      else if (name.includes('camshaft') || name.includes('vanos') || name.includes('cam')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf8fafc, // Induction-Hardened Steel Camshaft & VANOS Sprockets
          metalness: 0.96,
          roughness: 0.08,
          name: 'camshaftMat'
        });
      }
      else if (name.includes('timing_chain') || name.includes('chain')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x94a3b8, // Hardened Alloy Steel Duplex Roller Chain
          metalness: 0.94,
          roughness: 0.10,
          name: 'timingChainMat'
        });
      }
      else if (name.includes('valve_cover') || name.includes('coils')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x18181b, // Ultralight Die-Cast Magnesium with M-Power Carbon Shield
          metalness: 0.80,
          roughness: 0.24,
          clearcoat: 0.60,
          clearcoatRoughness: 0.12,
          name: 'valveCoverMat'
        });
      }
      else if (name.includes('turbo') || name.includes('turbocharger') || name.includes('turbine')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xd97706, // Inconel Heat-Resistant Turbine Housing & Billet Compressor
          metalness: 0.94,
          roughness: 0.12,
          clearcoat: 0.85,
          clearcoatRoughness: 0.08,
          name: 'turboMat'
        });
      }
      // BMW S58 / S63 M TwinPower Turbo Engine & Drivetrain
      else if (name.includes('powertrain') || name.includes('engine') || name.includes('trans')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x475569, // Cast Aluminum Engine Block with M-Carbon Styling
          metalness: 0.88,
          roughness: 0.18,
          name: 'bmwPowertrainMat'
        });
      }
      // BMW M-Adaptive Suspension Links & Multi-link
      else if (name.includes('suspension') || name.includes('axle') || name.includes('subframe') || name.includes('coil')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xd97706, // M-Performance Metallic Gold Anodized
          metalness: 0.88,
          roughness: 0.16,
          name: 'bmwSuspensionMat'
        });
      }

      // 17. Knuckle Joint: Double Eye Fork End (SAE 1045 Forged Machine Steel)
      else if (name.includes('fork')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0x8899a6, // Crisp Forged Machine Steel (bright silver-grey)
          metalness: 0.76,
          roughness: 0.20,
          clearcoat: 0.70,
          clearcoatRoughness: 0.10,
          name: 'forkEndMat'
        });
      }
      // 18. Knuckle Joint: Single Eye End (SAE 1045 Milled Steel)
      else if (name.includes('eye')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xa1b0be, // Precision Milled Satin Steel (bright contrast)
          metalness: 0.80,
          roughness: 0.18,
          clearcoat: 0.70,
          clearcoatRoughness: 0.10,
          name: 'eyeEndMat'
        });
      }
      // 19. Knuckle Joint: Main Cylindrical Knuckle Pin (Mirror Chrome Bearing Steel)
      else if (name.includes('knuckle_pin') || (name.includes('pin') && !name.includes('taper'))) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xf8fafc, // Mirror Polished Chrome Bearing Pin Steel
          metalness: 0.96,
          roughness: 0.06,
          name: 'knucklePinMat'
        });
      }
      // 20. Knuckle Joint: Retention Locking Collar (Golden Bronze)
      else if (name.includes('collar')) {
        child.material = new THREE.MeshPhysicalMaterial({
          color: 0xf59e0b, // Precision Anodized Golden Bronze Retention Collar
          metalness: 0.86,
          roughness: 0.18,
          clearcoat: 0.50,
          name: 'collarMat'
        });
      }
      // 21. Knuckle Joint: 1:30 Taper Split Pin (Bright Cadmium Gold)
      else if (name.includes('taper')) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xfbbf24, // Bright Cadmium-Plated Taper Split Pin
          metalness: 0.94,
          roughness: 0.12,
          name: 'taperPinMat'
        });
      }
      // General high-precision machine alloy fallback
      else {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xa0aec0,
          metalness: 0.82,
          roughness: 0.22
        });
      }

      // Guarantee double-sided rendering for all CAD geometry
      if (child.material) {
        child.material.side = THREE.DoubleSide;
        child.material.shadowSide = THREE.DoubleSide;
      }

      // Cache pristine original PBR material for clean restoring
      child.userData.pbrMaterial = child.material.clone();
    }
  });
}

export default function CADFileUploader({ onModelLoaded }) {
  const [dragActive, setDragActive] = useState(false);
  const [loadedFileInfo, setLoadedFileInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (file) => {
    setErrorMsg('');
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['gltf', 'glb', 'obj'].includes(ext)) {
      setErrorMsg('Unsupported format. Please upload SolidWorks export in .GLB, .GLTF, or .OBJ format.');
      return;
    }

    setLoading(true);
    soundFx.playClick();

    const reader = new FileReader();

    if (ext === 'glb') {
      reader.readAsArrayBuffer(file);
      reader.onload = (e) => {
        const loader = new GLTFLoader();
        loader.parse(
          e.target.result,
          '',
          (gltf) => {
            applyPBRMaterials(gltf.scene);
            setLoading(false);
            setLoadedFileInfo({
              name: file.name,
              size: (file.size / 1024).toFixed(1) + ' KB',
              format: ext.toUpperCase(),
              object: gltf.scene,
              source: 'File Explorer'
            });
            soundFx.playSuccess();
            if (onModelLoaded) onModelLoaded(gltf.scene, file.name);
          },
          (err) => {
            setLoading(false);
            setErrorMsg('Failed to parse GLB file: ' + err.message);
          }
        );
      };
    } else if (ext === 'obj') {
      reader.readAsText(file);
      reader.onload = (e) => {
        try {
          const loader = new OBJLoader();
          const obj = loader.parse(e.target.result);
          // Apply realistic PBR materials
          applyPBRMaterials(obj);

          setLoading(false);
          setLoadedFileInfo({
            name: file.name,
            size: (file.size / 1024).toFixed(1) + ' KB',
            format: ext.toUpperCase(),
            object: obj,
            source: 'File Explorer (D:\\solidworks\\)'
          });
          soundFx.playSuccess();
          if (onModelLoaded) onModelLoaded(obj, file.name);
        } catch (err) {
          setLoading(false);
          setErrorMsg('Failed to parse OBJ file: ' + err.message);
        }
      };
    }
  };

  const loadPredefinedModel = async (url, fileName) => {
    setLoading(true);
    soundFx.playClick();
    setErrorMsg('');
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('File not found: ' + url);
      const text = await response.text();
      const loader = new OBJLoader();
      const obj = loader.parse(text);

      // Enhance with professional PBR materials for realistic look
      applyPBRMaterials(obj);

      setLoading(false);
      setLoadedFileInfo({
        name: fileName,
        size: (text.length / 1024).toFixed(1) + ' KB',
        format: 'OBJ',
        object: obj,
        source: 'D:\\solidworks\\' + fileName
      });
      soundFx.playSuccess();
      if (onModelLoaded) onModelLoaded(obj, fileName);
    } catch (err) {
      setLoading(false);
      setErrorMsg('Error loading predefined CAD model: ' + err.message);
    }
  };

  return (
    <div className="cad-uploader-container">
      <div className="uploader-header">
        <span className="upload-icon">📂</span>
        <div>
          <h3>IMPORT CUSTOM SOLIDWORKS / CAD 3D MODEL</h3>
          <p>Drag & drop models exported from SolidWorks, or 1-click load our drawn CAD assembly</p>
        </div>
      </div>

      {/* File Explorer Direct Selection Banner */}
      <div className="file-explorer-action-box" style={{ background: 'linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.85))', border: '1px solid var(--border-glow)', borderRadius: '10px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <div style={{ fontSize: '13px', color: 'var(--cyan-glow)', fontWeight: '800', fontFamily: 'var(--font-brand)', letterSpacing: '1px' }}>
              📁 FILE EXPLORER CAD MODEL SELECTION:
            </div>
            <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '2px', fontFamily: 'var(--font-mono)' }}>
              Target Directory: <span style={{ color: '#38bdf8', fontWeight: '700' }}>D:\solidworks\</span>
            </div>
          </div>
          <span style={{ background: 'rgba(0,240,255,0.1)', border: '1px solid var(--cyan-glow)', color: 'var(--cyan-glow)', padding: '3px 10px', borderRadius: '12px', fontSize: '11px', fontFamily: 'var(--font-mono)', fontWeight: '700' }}>
            ⚡ 100% DRAWN MODEL DRIVEN
          </span>
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {/* Main button to open Windows File Explorer */}
          <button
            style={{
              flex: '1 1 280px',
              background: 'linear-gradient(135deg, #0284c7, #2563eb)',
              color: '#ffffff',
              padding: '14px 18px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '13px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              boxShadow: '0 4px 14px rgba(2, 132, 199, 0.4)'
            }}
            onClick={() => inputRef.current && inputRef.current.click()}
            disabled={loading}
          >
            <span style={{ fontSize: '18px' }}>📂</span>
            <span>OPEN FILE EXPLORER & SELECT DRAWN FILE</span>
          </button>

          {/* Direct 1-Click Load for Brake Assembly */}
          <button
            style={{
              flex: '1 1 240px',
              background: 'linear-gradient(135deg, #059669, #10b981)',
              color: '#ffffff',
              padding: '12px 16px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '12px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)'
            }}
            onClick={() => loadPredefinedModel('/models/Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj', 'Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj')}
            disabled={loading}
          >
            <span style={{ fontSize: '16px' }}>🏎️</span>
            <span>LOAD DRAWN BRAKE ASSEMBLY (.OBJ)</span>
          </button>

          {/* Direct 1-Click Load for Clutch Assembly */}
          <button
            style={{
              flex: '1 1 240px',
              background: 'linear-gradient(135deg, #d97706, #f59e0b)',
              color: '#ffffff',
              padding: '12px 16px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '12px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(245, 158, 11, 0.4)'
            }}
            onClick={() => loadPredefinedModel('/models/Automotive_Clutch_and_Pressure_Plate_Assembly.obj', 'Automotive_Clutch_and_Pressure_Plate_Assembly.obj')}
            disabled={loading}
          >
            <span style={{ fontSize: '16px' }}>⚙️</span>
            <span>LOAD DRAWN CLUTCH ASSEMBLY (.OBJ)</span>
          </button>

          {/* Direct 1-Click Load for BMW S58 Engine Assembly */}
          <button
            style={{
              flex: '1 1 240px',
              background: 'linear-gradient(135deg, #f59e0b, #ef4444)',
              color: '#ffffff',
              padding: '12px 16px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '12px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(245, 158, 11, 0.4)'
            }}
            onClick={() => loadPredefinedModel('/models/BMW_S58_TwinPower_Turbo_Engine_Core.obj', 'BMW_S58_TwinPower_Turbo_Engine_Core.obj')}
            disabled={loading}
          >
            <span style={{ fontSize: '16px' }}>⚡</span>
            <span>LOAD BMW S58 3.0L TURBO ENGINE CORE (.OBJ)</span>
          </button>
          <button
            style={{
              flex: '1 1 240px',
              background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
              color: '#ffffff',
              padding: '12px 16px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '12px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(2, 132, 199, 0.4)'
            }}
            onClick={() => loadPredefinedModel('/models/BMW_M_Series_Complete_Body_Assembly.obj', 'BMW_M_Series_Complete_Body_Assembly.obj')}
            disabled={loading}
          >
            <span style={{ fontSize: '16px' }}>🏎️</span>
            <span>LOAD BMW M-SERIES COMPLETE BODY ASSEMBLY (.OBJ)</span>
          </button>

          {/* Direct 1-Click Load for Knuckle Joint Assembly */}
          <button
            style={{
              flex: '1 1 240px',
              background: 'linear-gradient(135deg, #7c3aed, #8b5cf6)',
              color: '#ffffff',
              padding: '12px 16px',
              borderRadius: '8px',
              fontWeight: '800',
              fontSize: '12px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 4px 14px rgba(139, 92, 246, 0.4)'
            }}
            onClick={() => loadPredefinedModel('/models/Knuckle_Joint_Assembly.obj', 'Knuckle_Joint_Assembly.obj')}
            disabled={loading}
          >
            <span style={{ fontSize: '16px' }}>🦾</span>
            <span>LOAD DRAWN KNUCKLE JOINT (.OBJ)</span>
          </button>
        </div>

        <div style={{ fontSize: '11px', color: '#64748b', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span>💡 Tip:</span>
          <span>Click the blue button to open File Explorer (choose <strong>Knuckle_Joint_Assembly.obj</strong>, <strong>Automotive_Full_Vehicle_Chassis_and_Body_Assembly.obj</strong>, <strong>Automotive_Clutch_and_Pressure_Plate_Assembly.obj</strong>, or <strong>Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj</strong> from <strong>D:\solidworks\</strong>)!</span>
        </div>
      </div>

      <div
        className={`dropzone-card ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current && inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".gltf,.glb,.obj"
          style={{ display: 'none' }}
          onChange={handleChange}
        />

        <div className="dropzone-content">
          <div className="cloud-icon">{dragActive ? '📥' : '☁️'}</div>
          <h4>{loading ? 'PARSING 3D CAD DATA...' : dragActive ? 'RELEASE TO DROP FILE HERE!' : 'DROP SOLIDWORKS 3D FILE HERE OR CLICK TO BROWSE'}</h4>
          <p style={{ marginTop: '6px' }}>
            <strong>How to Drag:</strong> Open <code>D:\solidworks\</code> in Windows ➔ Left-click & drag <strong>Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj</strong> ➔ Drop into this box!
          </p>
          <p style={{ color: 'var(--cyan-glow)', marginTop: '4px', fontSize: '11px', fontWeight: '700' }}>
            ✨ Or SIMPLY CLICK anywhere inside this dashed box to open File Explorer!
          </p>
          <div className="format-pills" style={{ marginTop: '12px' }}>
            <span>Target: D:\solidworks\Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj</span>
            <span>.OBJ / .GLB</span>
          </div>
        </div>
      </div>

      {errorMsg && <div className="uploader-error">⚠️ {errorMsg}</div>}

      {loadedFileInfo && (
        <div className="loaded-file-card">
          <div className="file-meta-row">
            <span className="file-icon">📦</span>
            <div className="file-details">
              <strong>{loadedFileInfo.name}</strong>
              <div className="file-sub">Format: {loadedFileInfo.format} • Size: {loadedFileInfo.size}</div>
            </div>
            <span className="pill-ready">READY IN AR</span>
          </div>
        </div>
      )}

      {/* Guide for SolidWorks Export */}
      <div className="solidworks-export-guide">
        <h4>💡 HOW TO EXPORT FROM SOLIDWORKS:</h4>
        <ol>
          <li>Open your Part or Assembly in SolidWorks.</li>
          <li>Click <strong>File ➔ Save As</strong>.</li>
          <li>In <em>Save as type</em> dropdown, select <strong>GLTF (*.glb)</strong> or <strong>Wavefront OBJ (*.obj)</strong>.</li>
          <li>Drag that file into this box to see it live in Augmented Reality!</li>
        </ol>
      </div>
    </div>
  );
}

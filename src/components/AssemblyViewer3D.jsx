import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

export default function AssemblyViewer3D({
  currentStep,
  explodedPercent,
  isDefectSimulated,
  defectAngleOffset = 0,
  isXRayMode,
  isAutoRotate,
  isARMode,
  isProjectedARMode = true,
  activePartKey,
  cameraStreamActive,
  customModel,
  customModelName,
  effectiveModule,
  customCADParams,
  showAllParts = false
}) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const controlsRef = useRef(null);
  const partsRef = useRef({});
  const arrowsRef = useRef([]);
  const defectBoxRef = useRef(null);
  const reqIdRef = useRef(null);
  const customModelGroupRef = useRef(null);
  const ghostMatRef = useRef(null);
  const xrayMatRef = useRef(null);
  const projectedARGroupRef = useRef(null);
  const brakeClampJigRef = useRef(null);
  const clutchStandJigRef = useRef(null);
  const clutchClampGroupRef = useRef(null);
  const carSkilletJigRef = useRef(null);
  const knuckleViseJigRef = useRef(null);
  const engineRotisserieJigRef = useRef(null);
  const laserScanRef = useRef(null);

  const isAutoRotateRef = useRef(isAutoRotate);
  isAutoRotateRef.current = isAutoRotate;

  const isProjectedARModeRef = useRef(isProjectedARMode);
  isProjectedARModeRef.current = isProjectedARMode;

  const isXRayModeRef = useRef(isXRayMode);
  isXRayModeRef.current = isXRayMode;

  const isDefectSimulatedRef = useRef(isDefectSimulated);
  isDefectSimulatedRef.current = isDefectSimulated;

  const defectAngleOffsetRef = useRef(defectAngleOffset);
  defectAngleOffsetRef.current = defectAngleOffset;

  const explodedPercentRef = useRef(explodedPercent);
  explodedPercentRef.current = explodedPercent;

  const currentStepRef = useRef(currentStep);
  currentStepRef.current = currentStep;

  const stepTransitionTimeRef = useRef(performance.now());
  useEffect(() => {
    stepTransitionTimeRef.current = performance.now();
  }, [currentStep]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // --- Scene & Camera Setup ---
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // Close, crisp 3/4 isometric camera framing facing workpiece center
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(1.8, 1.2, 4.4);
    let renderer = null;
    const glCanvas = document.createElement('canvas');

    try {
      renderer = new THREE.WebGLRenderer({
        canvas: glCanvas,
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance'
      });
    } catch (e1) {
      console.warn('High-performance WebGL context failed, trying default WebGL fallback...', e1);
      try {
        renderer = new THREE.WebGLRenderer({
          canvas: glCanvas,
          antialias: false,
          alpha: true,
          powerPreference: 'default',
          failIfMajorPerformanceCaveat: false
        });
      } catch (e2) {
        console.error('All WebGL context creations failed:', e2);
      }
    }

    if (!renderer) {
      console.error('WebGL is unavailable in this browser session');
      const banner = document.createElement('div');
      banner.style.cssText = 'position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#080c14;color:#94a3b8;font-family:sans-serif;padding:24px;text-align:center;z-index:10;';
      banner.innerHTML = `
        <div style="font-size:3rem;margin-bottom:12px;">🏎️</div>
        <h3 style="color:#f8fafc;margin:0 0 8px 0;font-size:1.2rem;font-weight:700;">3D Graphics Accelerator Reset</h3>
        <p style="max-width:440px;font-size:0.9rem;line-height:1.6;margin:0 0 16px 0;color:#94a3b8;">
          Your browser's WebGL graphics memory is momentarily locked by background tabs. Click below to reinitialize the 3D workstation.
        </p>
        <button id="btn-retry-webgl" style="background:linear-gradient(135deg, #00d4ff, #0077ff);color:#030712;border:none;padding:10px 22px;border-radius:8px;font-weight:700;font-size:0.95rem;cursor:pointer;box-shadow:0 0 20px rgba(0,212,255,0.4);">
          ⚡ REINITIALIZE 3D WORKSTATION
        </button>
      `;
      container.appendChild(banner);
      banner.querySelector('#btn-retry-webgl')?.addEventListener('click', () => {
        window.location.reload();
      });
      return;
    }

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05; // Balanced, photorealistic studio tone mapping
    rendererRef.current = renderer;

    // Setup Photorealistic HDR Studio Environment for PBR Reflections
    try {
      const pmremGenerator = new THREE.PMREMGenerator(renderer);
      pmremGenerator.compileEquirectangularShader();
      const roomEnv = new RoomEnvironment();
      scene.environment = pmremGenerator.fromScene(roomEnv, 0.04).texture;
    } catch (hdrErr) {
      console.warn('HDR RoomEnvironment fallback to ambient lights:', hdrErr);
    }

    // Ghost Hologram Material for upcoming unassembled parts
    ghostMatRef.current = new THREE.MeshStandardMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.07,
      roughness: 0.35,
      metalness: 0.15,
      wireframe: false,
      depthWrite: false,
      side: THREE.DoubleSide
    });

    // Technical X-Ray Holographic Wireframe Material
    xrayMatRef.current = new THREE.MeshStandardMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.45,
      emissive: 0x002233,
      emissiveIntensity: 0.45,
      side: THREE.DoubleSide
    });

    container.appendChild(renderer.domElement);

    // Orbit Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 12;
    controls.minDistance = 1.2;
    controls.target.set(0, 0, 0);
    controlsRef.current = controls;

    // --- Studio Grade Multi-Angle PBR Lighting (Balanced, True-Color) ---
    // Dome Sky/Ground Ambient fill
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e293b, 0.65);
    scene.add(hemiLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.35);
    scene.add(ambientLight);

    // Front-Facing Key Light (Direct illumination on front and 3/4 faces)
    const frontKeyLight = new THREE.DirectionalLight(0xffffff, 1.7);
    frontKeyLight.position.set(3.5, 4.5, 5.5);
    frontKeyLight.castShadow = true;
    frontKeyLight.shadow.mapSize.width = 1024;
    frontKeyLight.shadow.mapSize.height = 1024;
    scene.add(frontKeyLight);

    // Left Fill Light (Soft cool fill to illuminate left recesses)
    const fillLight = new THREE.DirectionalLight(0xbae6fd, 0.8);
    fillLight.position.set(-5, 3.5, 3.5);
    scene.add(fillLight);

    // Top Overhead Softbox
    const topFill = new THREE.DirectionalLight(0xfff7ed, 0.6);
    topFill.position.set(0, 7, 0.5);
    scene.add(topFill);

    // Cyan Industrial Rim Accent (Back-left rim edge shine)
    const blueRimLight = new THREE.DirectionalLight(0x00f0ff, 0.5);
    blueRimLight.position.set(-4, -2, -4);
    scene.add(blueRimLight);

    // Studio Ground Grid (only visible in studio mode)
    const gridHelper = new THREE.GridHelper(10, 20, 0x00f0ff, 0x1e293b);
    gridHelper.position.y = -1.6;
    gridHelper.name = 'studioGrid';
    scene.add(gridHelper);

    // --- Industrial Assembly Workstation Tooling Fixture Jig (Werkstückträger) ---
    const fixtureGroup = new THREE.Group();
    fixtureGroup.name = 'fixtureJig';

    const fixtureMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      metalness: 0.85,
      roughness: 0.35,
      name: 'fixturePlateMat'
    });
    const fixtureAccentMat = new THREE.MeshStandardMaterial({
      color: 0x0ea5e9,
      metalness: 0.9,
      roughness: 0.2
    });
    const clampAmberMat = new THREE.MeshStandardMaterial({
      color: 0xd97706,
      metalness: 0.6,
      roughness: 0.4
    });

    // 1. Heavy Precision Milled Cast-Iron Tooling Workbench Base Plate
    const basePlateGeo = new THREE.BoxGeometry(6.6, 0.22, 5.6);
    const basePlateMesh = new THREE.Mesh(basePlateGeo, fixtureMat);
    basePlateMesh.position.set(0, -1.6, 0);
    basePlateMesh.receiveShadow = true;
    fixtureGroup.add(basePlateMesh);

    // 4 Heavy-Duty Workstation Bench Legs with Leveling Feet
    for (const [lx, lz] of [[-3.0, -2.5], [3.0, -2.5], [-3.0, 2.5], [3.0, 2.5]]) {
      const legGeo = new THREE.CylinderGeometry(0.14, 0.16, 1.6, 16);
      const legMesh = new THREE.Mesh(legGeo, fixtureMat);
      legMesh.position.set(lx, -2.45, lz);
      fixtureGroup.add(legMesh);

      // Leveling foot pad
      const footGeo = new THREE.CylinderGeometry(0.24, 0.28, 0.12, 16);
      const footMesh = new THREE.Mesh(footGeo, new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 }));
      footMesh.position.set(lx, -3.25, lz);
      fixtureGroup.add(footMesh);
    }

    // 2. Machined T-Slots along table surface
    for (const zOff of [-1.6, 0, 1.6]) {
      const tSlotGeo = new THREE.BoxGeometry(6.6, 0.05, 0.14);
      const tSlotMesh = new THREE.Mesh(tSlotGeo, new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.9 }));
      tSlotMesh.position.set(0, -1.48, zOff);
      fixtureGroup.add(tSlotMesh);
    }

    // 3. Four Heavy Precision Corner Fixture Clamp Lugs with M16 Guide Dowels
    for (const [cx, cz] of [[-3.0, -2.5], [3.0, -2.5], [-3.0, 2.5], [3.0, 2.5]]) {
      const lugGeo = new THREE.CylinderGeometry(0.18, 0.22, 0.32, 16);
      const lugMesh = new THREE.Mesh(lugGeo, fixtureAccentMat);
      lugMesh.position.set(cx, -1.44, cz);
      fixtureGroup.add(lugMesh);
    }

    // 4. Dedicated Brake Assembly Precision Tooling Pedestal & Clamp Jig
    const brakeClampJig = new THREE.Group();
    brakeClampJig.name = 'brakeClampJig';

    // Massive upright column with clean stance (sleek & accurate to CAD standards)
    const uprightGeo = new THREE.BoxGeometry(0.92, 1.45, 0.85);
    const uprightMesh = new THREE.Mesh(uprightGeo, fixtureMat);
    uprightMesh.position.set(0, -0.85, -0.65);
    uprightMesh.castShadow = true;
    uprightMesh.receiveShadow = true;
    brakeClampJig.add(uprightMesh);

    // Left and Right Triangular Gusset Reinforcement Ribs
    for (const xSide of [-0.52, 0.52]) {
      const gussetGeo = new THREE.BoxGeometry(0.14, 1.15, 0.65);
      const gussetMesh = new THREE.Mesh(gussetGeo, fixtureMat);
      gussetMesh.position.set(xSide, -0.95, -0.65);
      brakeClampJig.add(gussetMesh);
    }

    // Heavy Spindle Collar / Clamp Bushing
    const collarGeo = new THREE.CylinderGeometry(0.58, 0.58, 0.32, 28);
    collarGeo.rotateX(Math.PI / 2);
    const collarMesh = new THREE.Mesh(collarGeo, fixtureAccentMat);
    collarMesh.position.set(0, -0.20, -0.65);
    collarMesh.castShadow = true;
    brakeClampJig.add(collarMesh);

    // Precision Retaining Ring Collar
    const ringGeo = new THREE.CylinderGeometry(0.61, 0.61, 0.08, 28);
    ringGeo.rotateX(Math.PI / 2);
    const ringMesh = new THREE.Mesh(ringGeo, new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.95, roughness: 0.15 }));
    ringMesh.position.set(0, -0.20, -0.49);
    brakeClampJig.add(ringMesh);

    // Toggle Clamp Lever
    const clampArmGeo = new THREE.BoxGeometry(0.14, 0.55, 0.10);
    const clampArmMesh = new THREE.Mesh(clampArmGeo, clampAmberMat);
    clampArmMesh.position.set(0.38, 0.12, -0.65);
    clampArmMesh.rotation.z = 0.4;
    brakeClampJig.add(clampArmMesh);

    // 4 Precision Anchor Hex Bolts Bolted to Workbench Bed
    for (const [bx, bz] of [[-0.45, -0.32], [0.45, -0.32], [-0.45, -0.98], [0.45, -0.98]]) {
      const boltGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.14, 12);
      const boltMesh = new THREE.Mesh(boltGeo, new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 }));
      boltMesh.position.set(bx, -1.48, bz);
      brakeClampJig.add(boltMesh);
    }

    fixtureGroup.add(brakeClampJig);
    brakeClampJigRef.current = brakeClampJig;

    // 5. Dedicated Clutch Engine Simulator Stand & 3-Jaw Radial Toggle Clamp Jig
    const clutchStandJig = new THREE.Group();
    clutchStandJig.name = 'clutchStandJig';
    clutchStandJig.visible = false;

    // Heavy vertical riser pedestal column
    const clutchColGeo = new THREE.BoxGeometry(0.55, 1.45, 0.55);
    const clutchColMesh = new THREE.Mesh(clutchColGeo, fixtureMat);
    clutchColMesh.position.set(0, -0.82, -0.65);
    clutchColMesh.castShadow = true;
    clutchColMesh.receiveShadow = true;
    clutchStandJig.add(clutchColMesh);

    // Crankcase rear engine bellhousing backplate simulator (recessed safely behind workpiece)
    const engineBossGeo = new THREE.CylinderGeometry(1.35, 1.35, 0.06, 36);
    engineBossGeo.rotateX(Math.PI / 2);
    const engineBossMesh = new THREE.Mesh(engineBossGeo, new THREE.MeshStandardMaterial({
      color: 0x334155,
      metalness: 0.82,
      roughness: 0.32
    }));
    engineBossMesh.position.set(0, 0.06, -0.60);
    clutchStandJig.add(engineBossMesh);

    // Machined Crankshaft output flange datum socket
    const crankFlangeGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.06, 28);
    crankFlangeGeo.rotateX(Math.PI / 2);
    const crankFlangeMesh = new THREE.Mesh(crankFlangeGeo, new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.95, roughness: 0.18 }));
    crankFlangeMesh.position.set(0, 0.06, -0.54);
    clutchStandJig.add(crankFlangeMesh);

    // Recessed Crankshaft Pilot Pocket Bore (cavity where pilot bearing seats flush)
    const pilotPocketGeo = new THREE.CylinderGeometry(0.16, 0.16, 0.08, 24);
    pilotPocketGeo.rotateX(Math.PI / 2);
    const pilotPocketMesh = new THREE.Mesh(pilotPocketGeo, new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 }));
    pilotPocketMesh.position.set(0, 0.06, -0.52);
    clutchStandJig.add(pilotPocketMesh);

    // 3 Radial Pneumatic Clamping Arms holding Flywheel (grouped to engage dynamically from Step 2)
    const clutchClampGroup = new THREE.Group();
    clutchClampGroup.name = 'clutchClampGroup';
    for (const angle of [Math.PI / 2, Math.PI * 7 / 6, Math.PI * 11 / 6]) {
      const clampRad = 1.28;
      const armX = Math.cos(angle) * clampRad;
      const armY = 0.06 + Math.sin(angle) * clampRad;
      
      const armGeo = new THREE.BoxGeometry(0.12, 0.28, 0.16);
      const armMesh = new THREE.Mesh(armGeo, clampAmberMat);
      armMesh.position.set(armX, armY, -0.28);
      armMesh.rotation.z = angle - Math.PI / 2;
      clutchClampGroup.add(armMesh);

      // Clamp rubber contact tip securely touching outer starter ring gear at r=1.215
      const tipGeo = new THREE.BoxGeometry(0.14, 0.08, 0.18);
      const tipMesh = new THREE.Mesh(tipGeo, new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 }));
      const tipX = Math.cos(angle) * 1.215;
      const tipY = 0.06 + Math.sin(angle) * 1.215;
      tipMesh.position.set(tipX, tipY, -0.28);
      tipMesh.rotation.z = angle - Math.PI / 2;
      clutchClampGroup.add(tipMesh);
    }
    clutchStandJig.add(clutchClampGroup);
    clutchClampGroupRef.current = clutchClampGroup;

    fixtureGroup.add(clutchStandJig);
    clutchStandJigRef.current = clutchStandJig;

    // 6. Dedicated Car Chassis 4-Post Hydraulic Skillet AGV Lift Stand
    const carSkilletJig = new THREE.Group();
    carSkilletJig.name = 'carSkilletJig';
    carSkilletJig.visible = false;

    for (const [posX, posZ] of [[-1.2, -0.85], [1.2, -0.85], [-1.2, 0.85], [1.2, 0.85]]) {
      const postBaseGeo = new THREE.BoxGeometry(0.28, 0.95, 0.28);
      const postBaseMesh = new THREE.Mesh(postBaseGeo, fixtureMat);
      postBaseMesh.position.set(posX, -1.05, posZ);
      carSkilletJig.add(postBaseMesh);

      const ramGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.5, 16);
      const ramMesh = new THREE.Mesh(ramGeo, new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.95, roughness: 0.1 }));
      ramMesh.position.set(posX, -0.5, posZ);
      carSkilletJig.add(ramMesh);

      const padGeo = new THREE.BoxGeometry(0.32, 0.08, 0.32);
      const padMesh = new THREE.Mesh(padGeo, fixtureAccentMat);
      padMesh.position.set(posX, -0.25, posZ);
      carSkilletJig.add(padMesh);
    }

    fixtureGroup.add(carSkilletJig);
    carSkilletJigRef.current = carSkilletJig;

    // 7. Dedicated Mechanical Knuckle Joint Swivel Vise Stand
    const knuckleViseJig = new THREE.Group();
    knuckleViseJig.name = 'knuckleViseJig';
    knuckleViseJig.visible = false;

    const viseBaseGeo = new THREE.BoxGeometry(0.7, 0.85, 0.8);
    const viseBaseMesh = new THREE.Mesh(viseBaseGeo, fixtureMat);
    viseBaseMesh.position.set(0, -1.1, 0);
    knuckleViseJig.add(viseBaseMesh);

    const viseJawGeo = new THREE.BoxGeometry(0.55, 0.32, 0.18);
    for (const zOffset of [-0.22, 0.22]) {
      const jawMesh = new THREE.Mesh(viseJawGeo, fixtureAccentMat);
      jawMesh.position.set(0, -0.6, zOffset);
      knuckleViseJig.add(jawMesh);
    }

    fixtureGroup.add(knuckleViseJig);
    knuckleViseJigRef.current = knuckleViseJig;

    // 8. Dedicated Motorized Engine Rollover Assembly Rotisserie Stand
    const engineRotisserieJig = new THREE.Group();
    engineRotisserieJig.name = 'engineRotisserieJig';
    engineRotisserieJig.visible = false;

    // Dual heavy vertical A-frame upright columns (Front at Z = +1.22, Rear at Z = -1.22)
    for (const zPos of [-1.22, 1.22]) {
      const columnGeo = new THREE.BoxGeometry(0.24, 1.15, 0.24);
      const columnMesh = new THREE.Mesh(columnGeo, fixtureMat);
      columnMesh.position.set(0, -0.78, zPos);
      engineRotisserieJig.add(columnMesh);

      // 360-degree rotating pivot head & clamping disc
      const pivotHeadGeo = new THREE.CylinderGeometry(0.16, 0.16, 0.14, 24);
      pivotHeadGeo.rotateX(Math.PI / 2);
      const pivotHeadMesh = new THREE.Mesh(pivotHeadGeo, fixtureAccentMat);
      pivotHeadMesh.position.set(0, -0.05, zPos);
      engineRotisserieJig.add(pivotHeadMesh);

      // 4 adjustable tubular engine block mounting arms
      for (const [armX, armY] of [[-0.28, -0.18], [0.28, -0.18], [-0.28, 0.12], [0.28, 0.12]]) {
        const armGeo = new THREE.BoxGeometry(0.06, 0.06, 0.16);
        const armMesh = new THREE.Mesh(armGeo, new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 }));
        armMesh.position.set(armX, armY, zPos + (zPos < 0 ? 0.12 : -0.12));
        engineRotisserieJig.add(armMesh);
      }
    }
    fixtureGroup.add(engineRotisserieJig);
    engineRotisserieJigRef.current = engineRotisserieJig;

    scene.add(fixtureGroup);

    // --- Projected AR Light Guide Systems Laser Layer on Workstation ---
    const projectedARGroup = new THREE.Group();
    projectedARGroup.name = 'projectedARLayer';

    // Projected laser grid plane hovering 2mm above fixture
    const laserGridTexture = new THREE.GridHelper(6.2, 32, 0x10b981, 0x00f0ff);
    laserGridTexture.position.set(0, -1.50, 0);
    projectedARGroup.add(laserGridTexture);

    // Projected circular laser datum target ring around spindle center
    const laserTargetRingGeo = new THREE.RingGeometry(0.85, 0.90, 48);
    laserTargetRingGeo.rotateX(-Math.PI / 2);
    const laserTargetRingMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85
    });
    const laserTargetRing = new THREE.Mesh(laserTargetRingGeo, laserTargetRingMat);
    laserTargetRing.position.set(0, -1.49, 0);
    projectedARGroup.add(laserTargetRing);

    // Projected Crosshairs
    const chMat = new THREE.LineBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.85 });
    const chGeoX = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-2.8, -1.49, 0), new THREE.Vector3(2.8, -1.49, 0)]);
    const chGeoZ = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -1.49, -2.4), new THREE.Vector3(0, -1.49, 2.4)]);
    projectedARGroup.add(new THREE.Line(chGeoX, chMat));
    projectedARGroup.add(new THREE.Line(chGeoZ, chMat));

    scene.add(projectedARGroup);
    projectedARGroupRef.current = projectedARGroup;

    // --- Build Procedural High-Precision Automobile Disc Brake Assembly ---
    const parts = {};

    // 1. Wheel Hub & Spindle Group
    const hubGroup = new THREE.Group();
    hubGroup.name = 'hub';

    const steelMat = new THREE.MeshStandardMaterial({
      color: 0x8a9ba8,
      metalness: 0.85,
      roughness: 0.25,
      name: 'steelMat'
    });
    const darkSteelMat = new THREE.MeshStandardMaterial({
      color: 0x334155,
      metalness: 0.9,
      roughness: 0.35
    });

    // Spindle shaft
    const spindleGeo = new THREE.CylinderGeometry(0.35, 0.45, 1.2, 32);
    spindleGeo.rotateX(Math.PI / 2);
    const spindleMesh = new THREE.Mesh(spindleGeo, darkSteelMat);
    spindleMesh.castShadow = true;
    hubGroup.add(spindleMesh);

    // Hub mounting flange disc
    const flangeGeo = new THREE.CylinderGeometry(1.05, 1.05, 0.2, 36);
    flangeGeo.rotateX(Math.PI / 2);
    const flangeMesh = new THREE.Mesh(flangeGeo, steelMat);
    flangeMesh.position.z = 0.2;
    flangeMesh.castShadow = true;
    flangeMesh.receiveShadow = true;
    hubGroup.add(flangeMesh);

    // Center grease cap / snout
    const centerCapGeo = new THREE.CylinderGeometry(0.38, 0.42, 0.4, 32);
    centerCapGeo.rotateX(Math.PI / 2);
    const centerCapMesh = new THREE.Mesh(centerCapGeo, steelMat);
    centerCapMesh.position.z = 0.45;
    hubGroup.add(centerCapMesh);

    // 5 Wheel Lug Studs (Threaded M12 bolts arranged radially)
    const studMat = new THREE.MeshStandardMaterial({ color: 0xd1d5db, metalness: 0.95, roughness: 0.2 });
    const studRadius = 0.75;
    for (let i = 0; i < 5; i++) {
      const angle = (i * 2 * Math.PI) / 5;
      const studGeo = new THREE.CylinderGeometry(0.065, 0.065, 0.7, 16);
      studGeo.rotateX(Math.PI / 2);
      const studMesh = new THREE.Mesh(studGeo, studMat);
      studMesh.position.set(Math.cos(angle) * studRadius, Math.sin(angle) * studRadius, 0.5);
      studMesh.castShadow = true;
      hubGroup.add(studMesh);
    }
    scene.add(hubGroup);
    parts.hub = { group: hubGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(0, 0, -0.6) };

    // 2. Ventilated Cross-Drilled Brake Rotor Group
    const rotorGroup = new THREE.Group();
    rotorGroup.name = 'rotor';

    const rotorFrictionMat = new THREE.MeshStandardMaterial({
      color: 0xc4cbd4,
      metalness: 0.88,
      roughness: 0.22,
      name: 'rotorMat'
    });

    // Rotor Hat (Center bell)
    const hatGeo = new THREE.CylinderGeometry(0.85, 0.95, 0.35, 36);
    hatGeo.rotateX(Math.PI / 2);
    const hatMesh = new THREE.Mesh(hatGeo, darkSteelMat);
    hatMesh.position.z = 0.25;
    rotorGroup.add(hatMesh);

    // Ventilated Double Disc - Outer face & Inner face
    const discOuterRadius = 1.9;
    const discInnerRadius = 1.05;

    // Outer friction disc
    const outerRingGeo = new THREE.RingGeometry(discInnerRadius, discOuterRadius, 48);
    const outerDiscExtrude = new THREE.CylinderGeometry(discOuterRadius, discOuterRadius, 0.08, 48);
    outerDiscExtrude.rotateX(Math.PI / 2);
    const outerDiscMesh = new THREE.Mesh(outerDiscExtrude, rotorFrictionMat);
    outerDiscMesh.position.z = 0.45;
    outerDiscMesh.castShadow = true;
    rotorGroup.add(outerDiscMesh);

    // Inner friction disc
    const innerDiscMesh = new THREE.Mesh(outerDiscExtrude, rotorFrictionMat);
    innerDiscMesh.position.z = 0.32;
    innerDiscMesh.castShadow = true;
    rotorGroup.add(innerDiscMesh);

    // 18 Radial Ventilating Cooling Vanes between discs
    const vaneMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.8, roughness: 0.5 });
    for (let i = 0; i < 20; i++) {
      const angle = (i * 2 * Math.PI) / 20;
      const vaneGeo = new THREE.BoxGeometry(0.7, 0.04, 0.08);
      const vaneMesh = new THREE.Mesh(vaneGeo, vaneMat);
      const r = 1.45;
      vaneMesh.position.set(Math.cos(angle) * r, Math.sin(angle) * r, 0.385);
      vaneMesh.rotation.z = angle + 0.3; // Curved ventilation flow
      rotorGroup.add(vaneMesh);
    }

    // Cross-drilled aesthetic holes on rotor surface (Simulated with dark recessed pins)
    const holeMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
    for (let r = 1.25; r <= 1.75; r += 0.22) {
      for (let i = 0; i < 12; i++) {
        const angle = (i * 2 * Math.PI) / 12 + (r * 1.5);
        const holeGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.12, 12);
        holeGeo.rotateX(Math.PI / 2);
        const holeMesh = new THREE.Mesh(holeGeo, holeMat);
        holeMesh.position.set(Math.cos(angle) * r, Math.sin(angle) * r, 0.455);
        rotorGroup.add(holeMesh);
      }
    }

    scene.add(rotorGroup);
    parts.rotor = { group: rotorGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(0, 0, 0.8) };

    // 3. Caliper Anchor Mounting Bracket Group
    const bracketGroup = new THREE.Group();
    bracketGroup.name = 'bracket';

    const bracketMat = new THREE.MeshStandardMaterial({
      color: 0x374151,
      metalness: 0.75,
      roughness: 0.45,
      name: 'bracketMat'
    });

    // U-shaped bridge wrapping around the top edge of rotor
    const bridgeGeo = new THREE.BoxGeometry(1.6, 0.5, 0.6);
    const bridgeMesh = new THREE.Mesh(bridgeGeo, bracketMat);
    bridgeMesh.position.set(0.6, 1.6, 0.4);
    bridgeMesh.rotation.z = -0.35;
    bridgeMesh.castShadow = true;
    bracketGroup.add(bridgeMesh);

    // Two mounting ears
    const earGeo = new THREE.BoxGeometry(0.35, 0.6, 0.3);
    const ear1 = new THREE.Mesh(earGeo, bracketMat);
    ear1.position.set(0.05, 1.85, 0.2);
    bracketGroup.add(ear1);

    const ear2 = new THREE.Mesh(earGeo, bracketMat);
    ear2.position.set(1.2, 1.3, 0.2);
    bracketGroup.add(ear2);

    scene.add(bracketGroup);
    parts.bracket = { group: bracketGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(0.5, 0.6, 1.5) };

    // 4. Dual Brake Pads Group (Inner & Outer)
    const padsGroup = new THREE.Group();
    padsGroup.name = 'pads';

    const frictionMat = new THREE.MeshStandardMaterial({
      color: 0x262626,
      roughness: 0.85,
      metalness: 0.1
    });
    const padBackingMat = new THREE.MeshStandardMaterial({
      color: 0x94a3b8,
      metalness: 0.9,
      roughness: 0.25
    });

    // Outer Pad (Front)
    const outerPadGroup = new THREE.Group();
    const padFrictionGeo = new THREE.BoxGeometry(1.2, 0.45, 0.12);
    const outerFriction = new THREE.Mesh(padFrictionGeo, frictionMat);
    outerFriction.position.set(0, 0, 0);
    const outerBacking = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.52, 0.05), padBackingMat);
    outerBacking.position.set(0, 0, 0.08);
    outerPadGroup.add(outerFriction);
    outerPadGroup.add(outerBacking);
    outerPadGroup.position.set(0.65, 1.58, 0.56);
    outerPadGroup.rotation.z = -0.35;
    padsGroup.add(outerPadGroup);

    // Inner Pad (Back)
    const innerPadGroup = new THREE.Group();
    const innerFriction = new THREE.Mesh(padFrictionGeo, frictionMat);
    const innerBacking = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.52, 0.05), padBackingMat);
    innerBacking.position.set(0, 0, -0.08);
    innerPadGroup.add(innerFriction);
    innerPadGroup.add(innerBacking);
    innerPadGroup.position.set(0.65, 1.58, 0.22);
    innerPadGroup.rotation.z = -0.35;
    padsGroup.add(innerPadGroup);

    scene.add(padsGroup);
    parts.pads = { group: padsGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(0.7, 0.7, 2.3) };

    // 5. Brembo Red Performance Caliper Body Group
    const caliperGroup = new THREE.Group();
    caliperGroup.name = 'caliper';

    const redCaliperMat = new THREE.MeshStandardMaterial({
      color: 0xef4444, // Vibrant racing red
      metalness: 0.45,
      roughness: 0.2,
      clearcoat: 0.9,
      clearcoatRoughness: 0.1,
      name: 'caliperMat'
    });

    // Main sculpted caliper body shell
    const caliperMainGeo = new THREE.BoxGeometry(1.7, 0.75, 0.7);
    const caliperMain = new THREE.Mesh(caliperMainGeo, redCaliperMat);
    caliperMain.position.set(0.68, 1.62, 0.42);
    caliperMain.rotation.z = -0.35;
    caliperMain.castShadow = true;
    caliperGroup.add(caliperMain);

    // Piston cylinder chambers (Dual opposed bulge)
    const pistonBulgeGeo = new THREE.CylinderGeometry(0.24, 0.24, 0.22, 24);
    pistonBulgeGeo.rotateX(Math.PI / 2);
    const piston1 = new THREE.Mesh(pistonBulgeGeo, redCaliperMat);
    piston1.position.set(0.35, 1.8, 0.78);
    caliperGroup.add(piston1);

    const piston2 = new THREE.Mesh(pistonBulgeGeo, redCaliperMat);
    piston2.position.set(0.95, 1.5, 0.78);
    caliperGroup.add(piston2);

    // Hydraulic Bleeder Nipple & Fluid Inlet Bolt
    const bleederGeo = new THREE.CylinderGeometry(0.04, 0.05, 0.25, 12);
    const bleederMat = new THREE.MeshStandardMaterial({ color: 0xd4d4d8, metalness: 0.9, roughness: 0.2 });
    const bleederMesh = new THREE.Mesh(bleederGeo, bleederMat);
    bleederMesh.position.set(0.4, 2.05, 0.55);
    caliperGroup.add(bleederMesh);

    // "BREMBO / AUTO-AR" Racing Badge Plate
    const badgeGeo = new THREE.PlaneGeometry(0.9, 0.2);
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(0, 0, 256, 64);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 28px Rajdhani, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('AUTO-AR RACING', 128, 32);
    const badgeTexture = new THREE.CanvasTexture(canvas);
    const badgeMat = new THREE.MeshBasicMaterial({ map: badgeTexture });
    const badgeMesh = new THREE.Mesh(badgeGeo, badgeMat);
    badgeMesh.position.set(0.68, 1.62, 0.78);
    badgeMesh.rotation.z = -0.35;
    caliperGroup.add(badgeMesh);

    scene.add(caliperGroup);
    parts.caliper = { group: caliperGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(0.9, 0.9, 3.2) };

    // 6. Fasteners / Guide Pin Bolts Group
    const boltsGroup = new THREE.Group();
    boltsGroup.name = 'bolts';
    const hexBoltGeo = new THREE.CylinderGeometry(0.09, 0.09, 0.5, 6); // 6-sided hex head
    hexBoltGeo.rotateX(Math.PI / 2);
    const hexBoltMat = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.95, roughness: 0.15 });

    const bolt1 = new THREE.Mesh(hexBoltGeo, hexBoltMat);
    bolt1.position.set(0.05, 1.85, 0.85);
    boltsGroup.add(bolt1);

    const bolt2 = new THREE.Mesh(hexBoltGeo, hexBoltMat);
    bolt2.position.set(1.2, 1.3, 0.85);
    boltsGroup.add(bolt2);

    scene.add(boltsGroup);
    parts.bolts = { group: boltsGroup, basePos: new THREE.Vector3(0, 0, 0), explodeDir: new THREE.Vector3(1.2, 1.2, 4.0) };

    partsRef.current = parts;
    Object.values(parts).forEach(p => {
      if (p.group) p.group.visible = false;
    });

    // --- Defect Simulation Wireframe Hazard Box ---
    const defectBoxGeo = new THREE.BoxGeometry(1.8, 1.2, 1.2);
    const defectWireGeo = new THREE.WireframeGeometry(defectBoxGeo);
    const defectLineMat = new THREE.LineBasicMaterial({ color: 0xff0044, linewidth: 2 });
    const defectBox = new THREE.LineSegments(defectWireGeo, defectLineMat);
    defectBox.position.set(0.68, 1.62, 0.42);
    defectBox.visible = false;
    scene.add(defectBox);
    defectBoxRef.current = defectBox;

    // --- 3D Precision Laser Scanning Beam (Keyence CMM Optical Scanner Simulation) ---
    const laserScanGroup = new THREE.Group();
    laserScanGroup.name = 'laserScanBeam';

    // Translucent Laser Sheet
    const laserSheetGeo = new THREE.PlaneGeometry(3.0, 3.0);
    laserSheetGeo.rotateX(Math.PI / 2);
    const laserSheetMat = new THREE.MeshBasicMaterial({
      color: 0xff0044,
      transparent: true,
      opacity: 0.22,
      side: THREE.DoubleSide
    });
    const laserSheetMesh = new THREE.Mesh(laserSheetGeo, laserSheetMat);
    laserScanGroup.add(laserSheetMesh);

    // Focused Glowing Laser Crosshair Lines
    const laserLineGeoX = new THREE.CylinderGeometry(0.012, 0.012, 3.0, 16);
    laserLineGeoX.rotateZ(Math.PI / 2);
    const laserLineMat = new THREE.MeshBasicMaterial({ color: 0xff0044, transparent: true, opacity: 0.95 });
    const laserLineX = new THREE.Mesh(laserLineGeoX, laserLineMat);
    laserScanGroup.add(laserLineX);

    const laserLineGeoZ = new THREE.CylinderGeometry(0.012, 0.012, 3.0, 16);
    laserLineGeoZ.rotateX(Math.PI / 2);
    const laserLineZ = new THREE.Mesh(laserLineGeoZ, laserLineMat);
    laserScanGroup.add(laserLineZ);

    laserScanGroup.visible = false;
    scene.add(laserScanGroup);
    laserScanRef.current = { group: laserScanGroup, sheetMat: laserSheetMat, lineMat: laserLineMat };

    // --- Directional 3D AR Guide Arrows ---
    const arrowGroup = new THREE.Group();
    arrowGroup.name = 'guideArrow';
    const arrowHeadGeo = new THREE.ConeGeometry(0.07, 0.20, 16);
    arrowHeadGeo.rotateX(Math.PI / 2);
    const arrowShaftGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.32, 16);
    arrowShaftGeo.rotateX(Math.PI / 2);
    const arrowMat = new THREE.MeshStandardMaterial({
      color: 0x00f0ff,
      emissive: 0x006688,
      emissiveIntensity: 0.45,
      transparent: true,
      opacity: 0.65
    });
    const arrowHead = new THREE.Mesh(arrowHeadGeo, arrowMat);
    arrowHead.position.z = -0.25;
    const arrowShaft = new THREE.Mesh(arrowShaftGeo, arrowMat);
    arrowShaft.position.z = -0.08;
    arrowGroup.add(arrowHead);
    arrowGroup.add(arrowShaft);
    arrowGroup.position.set(0, 0, 2.2);
    scene.add(arrowGroup);
    arrowsRef.current = [arrowGroup];

    // --- Animation Loop ---
    let clock = new THREE.Clock();

    const animate = () => {
      reqIdRef.current = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Controls update with dynamic autoRotate from ref
      controls.autoRotate = Boolean(isAutoRotateRef.current);
      controls.autoRotateSpeed = 2.4;
      controls.update();

      // Projected AR Laser Layer visibility & subtle pulse
      if (projectedARGroupRef.current) {
        projectedARGroupRef.current.visible = Boolean(isProjectedARModeRef.current);
        const ring = projectedARGroupRef.current.children[1];
        if (ring) {
          ring.scale.setScalar(1.0 + Math.sin(elapsedTime * 3.5) * 0.035);
        }
      }

      // Guide arrow pulsing & floating animation (only when model is loaded)
      if (arrowGroup) {
        arrowGroup.visible = Boolean(customModelGroupRef.current);
        arrowGroup.position.z = 1.8 + Math.sin(elapsedTime * 4) * 0.15;
      }

      // Defect hazard flashing
      if (defectBoxRef.current && defectBoxRef.current.visible) {
        defectBoxRef.current.rotation.y = Math.sin(elapsedTime * 6) * 0.08;
        defectLineMat.color.setHex(Math.floor(elapsedTime * 5) % 2 === 0 ? 0xff0044 : 0xffaa00);
      }

      // Real-Time 3D Laser CMM Sweep Animation across Workpiece
      if (laserScanRef.current && laserScanRef.current.group) {
        if (isDefectSimulatedRef.current) {
          laserScanRef.current.group.visible = true;
          // Sweeps vertically up and down through the 3D component geometry
          laserScanRef.current.group.position.y = 0.06 + Math.sin(elapsedTime * 3.0) * 1.05;

          const dev = Math.abs(defectAngleOffsetRef.current || 0);
          const isPass = dev <= 1.0;
          const laserColor = isPass ? 0x10b981 : (dev <= 4.0 ? 0xf59e0b : 0xff0044);
          laserScanRef.current.sheetMat.color.setHex(laserColor);
          laserScanRef.current.lineMat.color.setHex(laserColor);
          laserScanRef.current.sheetMat.opacity = 0.24 + Math.sin(elapsedTime * 8) * 0.12;
        } else {
          laserScanRef.current.group.visible = false;
        }
      }

      // Real-Time Kinematic Fly-in Assembly & Dyno Rotor Spin Animations
      if (customModelGroupRef.current) {
        const now = performance.now();
        const stepElapsed = (now - (stepTransitionTimeRef.current || now)) / 1000.0;
        const flyDuration = 0.65; // 650ms smooth fly-in
        const flyProgress = Math.min(1.0, Math.max(0.0, stepElapsed / flyDuration));
        const easeFly = 1.0 - Math.pow(1.0 - flyProgress, 3);
        const flyFactor = (1.0 - easeFly);
        const activeStep = currentStepRef.current || 1;
        const explodeFactor = (explodedPercentRef.current || 0) / 100;
        const isSpinning = Boolean(isAutoRotateRef.current);

        customModelGroupRef.current.traverse(child => {
          if (child.isMesh && child.userData.initialPos) {
            const partStep = child.userData.computedStep || 1;
            const isTarget = partStep === activeStep;
            const compDir = child.userData.compDir || new THREE.Vector3(0, 0, 0);

            if (explodeFactor >= 0.01) {
              child.position.copy(child.userData.initialPos).addScaledVector(compDir, explodeFactor);
            } else if (isTarget && flyFactor > 0.001) {
              // Smooth kinematic insertion trajectory from disassembly axis
              child.position.copy(child.userData.initialPos).addScaledVector(compDir, flyFactor * 1.4);
              const n = (child.name || '').toLowerCase();
              if (n.includes('bolt') || n.includes('stud') || n.includes('pin')) {
                child.rotation.z = (child.userData.initialRotZ || 0) + (flyFactor * Math.PI * 4);
              }
            } else {
              child.position.copy(child.userData.initialPos);
            }

            // Realistic Dyno Rotor Spin when 360 Spin is active
            if (isSpinning && explodeFactor < 0.01) {
              const n = (child.name || '').toLowerCase();
              if (n.includes('rotor') || n.includes('disc') || n.includes('vanes') || n.includes('hub') || n.includes('stud') || n.includes('hat') || n.includes('bell') || n.includes('crossdrilled') || n.includes('slotted') || n.includes('bobbin') || n.includes('nut')) {
                child.rotation.z += 0.02;
              }
            }
          }
        });
      }

      renderer.render(scene, camera);
    };

    animate();

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w === 0 || h === 0) return;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(handleResize) : null;
    if (ro) ro.observe(container);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (ro) ro.disconnect();
      if (reqIdRef.current) cancelAnimationFrame(reqIdRef.current);
      if (renderer) {
        if (renderer.domElement && container.contains(renderer.domElement)) {
          container.removeChild(renderer.domElement);
        }
        try {
          renderer.dispose();
        } catch (dispErr) {}
      }
    };
  }, []);

  // --- Dynamic Prop Updates: Exploded View, Active Highlight, X-Ray, Defect ---
  useEffect(() => {
    const parts = partsRef.current;
    if (!parts || Object.keys(parts).length === 0) return;

    const explodeFactor = (explodedPercent || 0) / 100;

    Object.entries(parts).forEach(([key, partData]) => {
      const { group, basePos, explodeDir } = partData;

      // Update position along exploded axis
      group.position.x = basePos.x + explodeDir.x * explodeFactor;
      group.position.y = basePos.y + explodeDir.y * explodeFactor;
      group.position.z = basePos.z + explodeDir.z * explodeFactor;

      // Sequential step visibility check
      const stepOrder = ['hub', 'rotor', 'bracket', 'pads', 'caliper', 'bolts'];
      const partIndex = stepOrder.indexOf(key);

      // All models must come from selected files; procedural parts are strictly hidden
      group.visible = false;

      // Active component glow highlight
      const isActive = key === activePartKey;
      group.traverse(child => {
        if (child.isMesh && child.material) {
          if (isXRayMode) {
            if (xrayMatRef.current) {
              if (!child.userData.origMat) child.userData.origMat = child.material;
              child.material = xrayMatRef.current;
            } else {
              child.material.transparent = true;
              child.material.opacity = 0.35;
              child.material.wireframe = true;
            }
          } else {
            if (child.userData.origMat) {
              child.material = child.userData.origMat;
            }
            child.material.transparent = false;
            child.material.wireframe = false;
            if (isActive && !isDefectSimulated) {
              child.material.emissive = new THREE.Color(0x00f0ff);
              child.material.emissiveIntensity = 0.28;
            } else if (child.material.name === 'steelMat' || child.material.name === 'rotorMat') {
              child.material.emissive = new THREE.Color(0x000000);
              child.material.emissiveIntensity = 0;
            }
          }
        }
      });
    });

    // Defect Simulation Handling (Caliper or Rotor tilted incorrectly)
    if (defectBoxRef.current) {
      defectBoxRef.current.visible = isDefectSimulated;
    }
    if (parts.caliper && parts.caliper.group) {
      if (isDefectSimulated) {
        parts.caliper.group.rotation.z = -0.35 + 0.32; // Misaligned by 18.3 degrees!
        parts.caliper.group.position.y += 0.15;
      } else {
        parts.caliper.group.rotation.z = -0.35;
      }
    }
  }, [explodedPercent, currentStep, isDefectSimulated, isXRayMode, activePartKey, showAllParts]);

  // Studio Grid visibility based on AR Mode
  useEffect(() => {
    if (!sceneRef.current) return;
    const grid = sceneRef.current.getObjectByName('studioGrid');
    if (grid) {
      grid.visible = !isARMode || isProjectedARMode;
    }
    if (arrowsRef.current && arrowsRef.current[0]) {
      arrowsRef.current[0].visible = Boolean(customModel) && currentStep < 13 && !isDefectSimulated && !showAllParts && (explodedPercent || 0) < 5;
    }
  }, [isARMode, isProjectedARMode, currentStep, isDefectSimulated, customModel, showAllParts, explodedPercent]);

  // Dynamic 3D Holographic Insertion Guide Trajectory (Light Guide Systems Mode)
  useEffect(() => {
    if (!arrowsRef.current || !arrowsRef.current[0]) return;
    const arrow = arrowsRef.current[0];
    const key = (activePartKey || '').toLowerCase();

    // Default positioning outside workpiece
    arrow.position.set(0, 0, 2.2);
    arrow.rotation.set(0, 0, 0);

    // Knuckle Joint real mechanical trajectories
    if (key.includes('fork')) {
      arrow.position.set(0, 0.4, 2.0);
      arrow.rotation.set(0, 0, 0); // Aiming at fixture datum
    } else if (key.includes('eye')) {
      arrow.position.set(2.2, 0, 0.4);
      arrow.rotation.set(0, 0, Math.PI / 2); // Sliding horizontally into fork gap
    } else if (key.includes('pin') && !key.includes('taper')) {
      arrow.position.set(0, 2.2, 0.4);
      arrow.rotation.set(Math.PI, 0, 0); // Plunging downward into coaxial bore
    } else if (key.includes('collar')) {
      arrow.position.set(0, -2.0, 0.4);
      arrow.rotation.set(0, 0, 0); // Sliding upward onto lower pin spigot
    } else if (key.includes('taper')) {
      arrow.position.set(0, -0.6, 2.0);
      arrow.rotation.set(0, Math.PI / 2, 0); // Driving into transverse cross-hole
    } else if (key.includes('hub')) {
      arrow.position.set(0, 0, 2.2);
      arrow.rotation.set(0, 0, 0);
    } else if (key.includes('rotor')) {
      arrow.position.set(0, 0, 2.4);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('bracket')) {
      arrow.position.set(0.8, 2.2, 2.0);
      arrow.rotation.set(Math.PI * 0.7, 0, 0);
    } else if (key.includes('pad')) {
      arrow.position.set(0.8, 2.0, 1.8);
      arrow.rotation.set(0, Math.PI / 2, 0);
    } else if (key.includes('caliper')) {
      arrow.position.set(1.1, 2.3, 2.3);
      arrow.rotation.set(Math.PI * 0.8, 0, 0);
    } else if (key.includes('bolt')) {
      arrow.position.set(0.8, 2.0, 2.5);
      arrow.rotation.set(Math.PI, 0, 0);
    }
    // Automotive 12-Station Trajectories
    else if (key.includes('chassis')) {
      arrow.position.set(0, -1.0, 0);
      arrow.rotation.set(0, 0, 0);
    } else if (key.includes('wiring') || key.includes('harness')) {
      arrow.position.set(0, 0.8, 0);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('cockpit')) {
      arrow.position.set(0.6, 1.4, 0);
      arrow.rotation.set(Math.PI * 0.75, 0, 0);
    } else if (key.includes('powertrain') || key.includes('engine')) {
      arrow.position.set(1.2, -1.2, 0);
      arrow.rotation.set(0, 0, 0); // Hydraulic marriage lift ascending from below
    } else if (key.includes('suspension')) {
      arrow.position.set(1.4, 0.8, 1.5);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('exhaust')) {
      arrow.position.set(-0.8, -1.2, 0);
      arrow.rotation.set(0, 0, 0);
    } else if (key.includes('seat')) {
      arrow.position.set(-0.2, 1.6, 0);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('glazing') || key.includes('glass')) {
      arrow.position.set(0.5, 1.8, 0);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('door')) {
      arrow.position.set(0.2, 0.4, 2.2);
      arrow.rotation.set(0, -Math.PI / 2, 0);
    } else if (key.includes('body')) {
      arrow.position.set(0, 2.4, 0);
      arrow.rotation.set(Math.PI, 0, 0);
    } else if (key.includes('wheel') || key.includes('tire')) {
      arrow.position.set(0, 0, 2.5);
      arrow.rotation.set(0, -Math.PI / 2, 0);
    }
  }, [activePartKey, currentStep]);

  // Handle Dynamic Custom CAD Parameters from CAD Drawing Studio
  useEffect(() => {
    if (!customCADParams) return;
    const parts = partsRef.current;
    if (!parts) return;

    if (customCADParams.outerDiameter && parts.rotor && parts.rotor.group) {
      const scale = customCADParams.outerDiameter / 320;
      parts.rotor.group.scale.set(scale, scale, 1);
    }
    if (customCADParams.caliperColor && parts.caliper && parts.caliper.group) {
      parts.caliper.group.traverse(child => {
        if (child.isMesh && child.material && child.material.name === 'caliperMat') {
          child.material.color.set(customCADParams.caliperColor);
        }
      });
    }
  }, [customCADParams]);

  // Handle Custom Uploaded SolidWorks 3D Model
  useEffect(() => {
    if (!sceneRef.current) return;
    const scene = sceneRef.current;

    // Remove old custom model if present
    if (customModelGroupRef.current) {
      scene.remove(customModelGroupRef.current);
      customModelGroupRef.current = null;
    }

    if (customModel) {
      const box = new THREE.Box3().setFromObject(customModel);
      const size = new THREE.Vector3();
      box.getSize(size);
      const maxDim = Math.max(size.x, size.y, size.z);
      const targetDim = 2.45; // Comfortably framed inside viewport with generous margin
      const scale = maxDim > 0 ? targetDim / maxDim : 1;
      customModel.scale.set(scale, scale, scale);

      // Accurately center scaled model at (0, 0, 0)
      box.setFromObject(customModel);
      const center = new THREE.Vector3();
      box.getCenter(center);
      customModel.position.sub(center);
      customModel.position.y += 0.06; // Rests squarely on machined fixture jig

      // Cache initial positions and rotations for smooth explode & real defect animations
      customModel.traverse(child => {
        if (child.isMesh) {
          child.userData.initialPos = child.position.clone();
          child.userData.initialRotZ = child.rotation.z;
          child.userData.initialRotX = child.rotation.x;
          child.userData.initialRotY = child.rotation.y;
        }
      });

      // Hide default parts to spotlight the uploaded CAD model
      if (partsRef.current) {
        Object.values(partsRef.current).forEach(p => {
          if (p.group) p.group.visible = false;
        });
      }

      // Dynamically display the authentic dedicated workstation stand for each module
      const isEngine = (effectiveModule === 'engine') || (customModelName && (customModelName.toLowerCase().includes('engine') || customModelName.toLowerCase().includes('s58') || customModelName.toLowerCase().includes('b58')));
      const isCar = !isEngine && ((effectiveModule === 'car') || (customModelName && customModelName.toLowerCase().includes('bmw')));
      const isClutch = (effectiveModule === 'clutch') || (customModelName && (customModelName.toLowerCase().includes('clutch') || customModelName.toLowerCase().includes('flywheel')));
      const isKnuckle = (effectiveModule === 'knuckle') || (customModelName && (customModelName.toLowerCase().includes('knuckle') || customModelName.toLowerCase().includes('joint')));
      const isBrake = !customModel || (effectiveModule === 'brake') || (customModelName && (customModelName.toLowerCase().includes('brake') || customModelName.toLowerCase().includes('caliper')));

      if (brakeClampJigRef.current) brakeClampJigRef.current.visible = isBrake && !isClutch && !isCar && !isKnuckle && !isEngine;
      if (clutchStandJigRef.current) clutchStandJigRef.current.visible = isClutch;
      if (carSkilletJigRef.current) carSkilletJigRef.current.visible = isCar;
      if (knuckleViseJigRef.current) knuckleViseJigRef.current.visible = isKnuckle;
      if (engineRotisserieJigRef.current) engineRotisserieJigRef.current.visible = isEngine;

      scene.add(customModel);
      customModelGroupRef.current = customModel;
    } else {
      // Keep procedural parts hidden - assembly must be loaded from File Explorer
      if (partsRef.current) {
        Object.values(partsRef.current).forEach(p => {
          if (p.group) p.group.visible = false;
        });
      }
      if (brakeClampJigRef.current) brakeClampJigRef.current.visible = true;
      if (clutchStandJigRef.current) clutchStandJigRef.current.visible = false;
      if (carSkilletJigRef.current) carSkilletJigRef.current.visible = false;
      if (knuckleViseJigRef.current) knuckleViseJigRef.current.visible = false;
      if (engineRotisserieJigRef.current) engineRotisserieJigRef.current.visible = false;
    }
  }, [customModel, effectiveModule, customModelName]);

  // Handle Dynamic Interactions on Uploaded Custom CAD Model (Explode, Steps, Defect, X-Ray)
  useEffect(() => {
    if (!customModelGroupRef.current) return;
    const model = customModelGroupRef.current;
    const explodeFactor = (explodedPercent || 0) / 100;

    model.traverse(child => {
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

        // 1. Exploded View Displacement along functional or computed axes
        if (child.userData.initialPos) {
          let explodeDir = child.userData.explodeDir ? child.userData.explodeDir.clone() : new THREE.Vector3(0, 0, 0);

          if (!child.userData.explodeDir) {
            // S58 3.0L Inline-6 TwinPower Turbo Engine Core mappings
            if (name.includes('block') || name.includes('cylinder_bank')) explodeDir.set(0, 0, 0); // Station 1: Block datum
            else if (name.includes('crankshaft')) explodeDir.set(0, -1.2, 0); // Station 2: Crank drops down
            else if (name.includes('bedplate')) explodeDir.set(0, -1.8, 0); // Station 3: Bedplate drops down
            else if (name.includes('rod')) explodeDir.set(0, -0.6, 0); // Station 4: Connecting rods
            else if (name.includes('piston')) explodeDir.set(0, 1.2, 0); // Station 5: Pistons rise up
            else if (name.includes('oil_pan') || name.includes('sump')) explodeDir.set(0, -2.6, 0); // Station 6: Oil pan drops down
            else if (name.includes('gasket') || name.includes('mls')) explodeDir.set(0, 1.7, 0); // Station 7: MLS gasket lifts up
            else if (name.includes('cylinder_head') || name.includes('dohc_head')) explodeDir.set(0, 2.3, 0); // Station 8: Cylinder head lifts up
            else if (name.includes('camshaft') || name.includes('vanos')) explodeDir.set(0, 2.9, 0); // Station 9: Camshafts lift up
            else if (name.includes('timing_chain') || name.includes('chain')) explodeDir.set(0, 1.2, 1.6); // Station 10: Timing chain slides forward
            else if (name.includes('valve_cover') || name.includes('coils')) explodeDir.set(0, 3.6, 0); // Station 11: Valve cover lifts up
            else if (name.includes('turbo') || name.includes('turbocharger')) explodeDir.set(-2.5, 1.2, 0); // Station 12: Turbocharger explodes outward
            // Disc Brake mappings (Radial & axial disassembly vectors)
            else if (name.includes('hub') || name.includes('spindle')) explodeDir.set(0, 0, 0);
            else if (name.includes('stud') || name.includes('circlip') || name.includes('nut')) explodeDir.set(0, 0, 1.2);
            else if (name.includes('abs') || name.includes('tone') || name.includes('sensor')) explodeDir.set(-1.0, 0.8, -0.2);
            else if (name.includes('rotor') || name.includes('vanes') || name.includes('disc') || name.includes('hat') || name.includes('bell') || name.includes('crossdrilled') || name.includes('slotted') || name.includes('bobbin')) explodeDir.set(0, 0, 2.2);
            else if (name.includes('bracket')) explodeDir.set(0.4, 1.2, 0.4);
            else if (name.includes('shim') || name.includes('clip') || name.includes('spring')) explodeDir.set(0.4, 1.5, 1.6);
            else if (name.includes('pad')) explodeDir.set(0.4, 1.6, 2.4);
            else if (name.includes('caliper') || name.includes('housing') || name.includes('piston') || name.includes('emblem')) explodeDir.set(0.8, 2.2, 1.0);
            else if (name.includes('bolt') || name.includes('guide')) explodeDir.set(1.2, 2.8, 1.8);
            else if (name.includes('bleeder') || name.includes('banjo')) explodeDir.set(0.8, 2.6, 0.6);
            // Clutch Assembly mappings (Axial transmission insertion & forward explosion)
            else if (name.includes('pilot') || name.includes('needle')) explodeDir.set(0, 0, 1.4);
            else if (name.includes('flywheel') || name.includes('dmf') || name.includes('ring_gear')) explodeDir.set(0, 0, 2.0);
            else if (name.includes('crank') || (name.includes('bolt') && !name.includes('cover') && !name.includes('flange'))) explodeDir.set(0, 0, 2.6);
            else if (name.includes('spline') || name.includes('input_shaft')) explodeDir.set(0, 0, 3.2);
            else if (name.includes('friction') || name.includes('damper')) explodeDir.set(0, 0, 3.8);
            else if (name.includes('mandrel') || name.includes('arbor')) explodeDir.set(0, 0, 4.4);
            else if (name.includes('pressure') || name.includes('clamping')) explodeDir.set(0, 0, 5.0);
            else if (name.includes('diaphragm') || (name.includes('spring') && !name.includes('damper') && !name.includes('sac'))) explodeDir.set(0, 0, 5.6);
            else if (name.includes('sac') || name.includes('ratchet')) explodeDir.set(0, 0, 6.2);
            else if (name.includes('cover') || name.includes('bearing') || name.includes('release')) explodeDir.set(0, 0, 6.8);
            // Full Car 12-Station Assembly mappings (Multi-directional industrial explosion)
            else if (name.includes('chassis') || name.includes('spaceframe') || name.includes('frame') || name.includes('cage')) explodeDir.set(0, -1.2, 0); // Station 1: Chassis floorpan lowers
            else if (name.includes('wiring') || name.includes('harness')) explodeDir.set(0, -0.6, 0.4); // Station 2: Wiring loom
            else if (name.includes('cockpit') || name.includes('instrument')) explodeDir.set(0.6, 1.0, 0); // Station 3: Cockpit module lifts forward
            else if (name.includes('powertrain') || name.includes('trans')) explodeDir.set(0, -0.8, 0); // Station 4: Engine marriage lowers
            else if (name.includes('suspension') || name.includes('subframe') || name.includes('coil') || name.includes('drivetrain')) explodeDir.set(0, -0.5, child.position.z >= 0 ? 0.6 : -0.6); // Station 5: Suspension
            else if (name.includes('exhaust') || name.includes('muffler') || name.includes('downpipe')) explodeDir.set(-0.6, -0.9, 0); // Station 6: Exhaust drops underbody
            else if (name.includes('brake') || name.includes('caliper') || name.includes('rotor')) explodeDir.set(0, 0, child.position.z >= 0 ? 1.6 : -1.6); // Station 7: Brakes explode sideways
            else if (name.includes('seat') || name.includes('bucket')) explodeDir.set(0, 1.2, child.position.z >= 0 ? 0.35 : -0.35); // Station 8: Seats lift up
            else if (name.includes('glass') || name.includes('greenhouse') || name.includes('windshield') || name.includes('glazing')) explodeDir.set(0, 1.8, 0); // Station 9: Glass lifts up
            else if (name.includes('door') || name.includes('mirror')) explodeDir.set(0, 0, child.position.z >= 0 ? 1.8 : -1.8); // Station 10: Doors & mirrors explode laterally
            else if (name.includes('body') || name.includes('shell') || name.includes('hood') || name.includes('powerdome') || name.includes('canopy') || name.includes('spoiler') || name.includes('grille') || name.includes('fascia') || name.includes('headlight') || name.includes('bumper') || name.includes('aerodynamics') || name.includes('diffuser')) explodeDir.set(0, 2.5, 0); // Station 11: Outer carbon body shell lifts up
            else if (name.includes('wheel') || name.includes('tire') || name.includes('alloy') || name.includes('forged') || name.includes('rolling')) explodeDir.set(0, 0, child.position.z >= 0 ? 2.8 : -2.8); // Station 12: Wheels & tires explode outward
            // Knuckle Joint Assembly mappings (Orthogonal kinematic explosion)
            else if (name.includes('fork')) explodeDir.set(-2.0, 0, 0);
            else if (name.includes('eye')) explodeDir.set(2.0, 0, 0);
            else if (name.includes('knuckle_pin') || (name.includes('pin') && !name.includes('taper'))) explodeDir.set(0, 2.5, 0);
            else if (name.includes('collar')) explodeDir.set(0, -1.6, 0);
            else if (name.includes('taper')) explodeDir.set(0, -1.6, 1.8);
          }

          // Scale compensation: ensures visible, dramatic exploded view regardless of CAD import units
          const modelScale = (customModel && customModel.scale && customModel.scale.x > 0) ? customModel.scale.x : 1;
          const compensatedDir = explodeDir.clone().divideScalar(modelScale);
          child.userData.compDir = compensatedDir;
          child.position.copy(child.userData.initialPos).addScaledVector(compensatedDir, explodeFactor);
        }

        // 2. Sequential Step Visibility & Holographic Ghosting
        let partStep = child.userData.stepIndex || 12;
        if (!child.userData.stepIndex) {
          const isEngine = (effectiveModule === 'engine') || (customModelName && (customModelName.toLowerCase().includes('engine') || customModelName.toLowerCase().includes('s58') || customModelName.toLowerCase().includes('b58')));
          const isCar = !isEngine && ((effectiveModule === 'car') || (customModelName && customModelName.toLowerCase().includes('bmw')) || name.includes('bmw'));
          const isClutch = (effectiveModule === 'clutch') || (customModelName && (customModelName.toLowerCase().includes('clutch') || customModelName.toLowerCase().includes('flywheel')));
          const isBrake = (effectiveModule === 'brake') || (customModelName && (customModelName.toLowerCase().includes('brake') || customModelName.toLowerCase().includes('caliper')));

          if (isEngine) {
            if (name.includes('block') || name.includes('cylinder_bank')) partStep = 1;
            else if (name.includes('crankshaft')) partStep = 2;
            else if (name.includes('bedplate')) partStep = 3;
            else if (name.includes('rod')) partStep = 4;
            else if (name.includes('piston')) partStep = 5;
            else if (name.includes('oil_pan') || name.includes('sump')) partStep = 6;
            else if (name.includes('gasket') || name.includes('mls')) partStep = 7;
            else if (name.includes('cylinder_head') || name.includes('dohc_head')) partStep = 8;
            else if (name.includes('camshaft') || name.includes('vanos')) partStep = 9;
            else if (name.includes('timing_chain') || name.includes('chain')) partStep = 10;
            else if (name.includes('valve_cover') || name.includes('coils')) partStep = 11;
            else if (name.includes('turbo') || name.includes('turbocharger')) partStep = 12;
            else partStep = 1;
          } else if (isCar) {
            if (name.includes('chassis') || name.includes('spaceframe') || name.includes('frame') || name.includes('cage')) partStep = 1;
            else if (name.includes('wiring') || name.includes('harness')) partStep = 2;
            else if (name.includes('cockpit') || name.includes('instrument')) partStep = 3;
            else if (name.includes('powertrain') || name.includes('engine') || name.includes('trans')) partStep = 4;
            else if (name.includes('suspension') || name.includes('subframe') || name.includes('coil') || name.includes('drivetrain')) partStep = 5;
            else if (name.includes('exhaust') || name.includes('muffler') || name.includes('downpipe')) partStep = 6;
            else if (name.includes('brake') || name.includes('caliper') || name.includes('rotor')) partStep = 7;
            else if (name.includes('seat') || name.includes('bucket')) partStep = 8;
            else if (name.includes('glass') || name.includes('greenhouse') || name.includes('windshield') || name.includes('glazing')) partStep = 9;
            else if (name.includes('door') || name.includes('mirror')) partStep = 10;
            else if (name.includes('body') || name.includes('shell') || name.includes('hood') || name.includes('powerdome') || name.includes('canopy') || name.includes('spoiler') || name.includes('grille') || name.includes('fascia') || name.includes('headlight') || name.includes('bumper') || name.includes('aerodynamics') || name.includes('diffuser')) partStep = 11;
            else if (name.includes('wheel') || name.includes('tire') || name.includes('alloy') || name.includes('forged') || name.includes('rolling')) partStep = 12;
          } else if (isBrake) {
            if (name.includes('hub') || name.includes('spindle')) partStep = 1;
            else if (name.includes('stud') || name.includes('circlip') || name.includes('nut')) partStep = 2;
            else if (name.includes('abs') || name.includes('tone') || name.includes('sensor')) partStep = 3;
            else if (name.includes('rotor') || name.includes('vanes') || name.includes('disc') || name.includes('hat') || name.includes('bell') || name.includes('crossdrilled') || name.includes('slotted') || name.includes('bobbin')) partStep = 4;
            else if (name.includes('bracket')) partStep = 5;
            else if (name.includes('clip') || name.includes('shim') || name.includes('spring')) partStep = 6;
            else if (name.includes('pad')) partStep = 7;
            else if (name.includes('caliper') || name.includes('housing') || name.includes('piston') || name.includes('emblem') || name.includes('branding')) partStep = 8;
            else if (name.includes('bolt') || name.includes('guide')) partStep = 9;
            else if (name.includes('bleeder') || name.includes('banjo') || name.includes('pipe') || name.includes('valve')) partStep = 10;
            else partStep = 4;
          } else if (isClutch) {
            if (name.includes('pilot') || name.includes('needle')) partStep = 1;
            else if (name.includes('flywheel') || name.includes('dmf') || name.includes('ring_gear')) partStep = 2;
            else if (name.includes('crank') || (name.includes('bolt') && !name.includes('cover') && !name.includes('flange'))) partStep = 3;
            else if (name.includes('spline') || name.includes('input_shaft')) partStep = 4;
            else if (name.includes('friction') || name.includes('damper')) partStep = 5;
            else if (name.includes('mandrel') || name.includes('arbor')) partStep = 6;
            else if (name.includes('pressure') || name.includes('clamping')) partStep = 7;
            else if (name.includes('diaphragm') || (name.includes('spring') && !name.includes('damper') && !name.includes('sac'))) partStep = 8;
            else if (name.includes('sac') || name.includes('ratchet')) partStep = 9;
            else if (name.includes('cover') || name.includes('bearing') || name.includes('release')) partStep = 10;
            else partStep = 2;
          } else {
            if (name.includes('fork')) partStep = 1;
            else if (name.includes('eye')) partStep = 2;
            else if (name.includes('pin') && !name.includes('taper')) partStep = 3;
            else if (name.includes('collar')) partStep = 4;
            else if (name.includes('taper')) partStep = 5;
            else partStep = 6;
          }
        }

        child.userData.computedStep = partStep;

        const isFullyAssembledView = showAllParts || explodeFactor >= 0.05;
        const isPartAssembled = partStep < currentStep;
        const isTargetStep = partStep === currentStep;
        const isUpcoming = partStep > currentStep;

        if (isXRayMode) {
          child.visible = true;
          if (xrayMatRef.current) {
            child.material = xrayMatRef.current;
          } else {
            if (child.userData.pbrMaterial) {
              child.material = child.userData.pbrMaterial.clone();
            }
            child.material.transparent = true;
            child.material.opacity = 0.35;
            child.material.wireframe = true;
          }
        } else if (isFullyAssembledView) {
          // Exploded or Full-Solid view: all parts visible in full realistic PBR
          child.visible = true;
          if (child.userData.pbrMaterial) {
            child.material = child.userData.pbrMaterial;
          }
          child.material.transparent = false;
          child.material.wireframe = false;
          child.material.emissive = new THREE.Color(0x000000);
          child.material.emissiveIntensity = 0;
        } else if (isTargetStep) {
          // The part being assembled right now in THIS STEP!
          child.visible = true;
          if (child.userData.pbrMaterial) {
            child.material = child.userData.pbrMaterial;
          }
          child.material.transparent = false;
          child.material.wireframe = false;
          // Ultra-crisp AR edge highlight glow (0.16) so realistic textures remain pristine!
          if (!isDefectSimulated) {
            child.material.emissive = new THREE.Color(0x00f0ff);
            child.material.emissiveIntensity = 0.16;
          } else {
            child.material.emissive = new THREE.Color(0xff0044);
            child.material.emissiveIntensity = 0.35;
          }
        } else if (isPartAssembled) {
          // Assembled in earlier steps: firmly in place in the assembly
          child.visible = true;
          if (child.userData.pbrMaterial) {
            child.material = child.userData.pbrMaterial;
          }
          child.material.transparent = false;
          child.material.wireframe = false;
          child.material.emissive = new THREE.Color(0x000000);
          child.material.emissiveIntensity = 0;
        } else if (isUpcoming) {
          if (isARMode || isProjectedARMode) {
            // Projected AR Ghost Hologram: Shows ONLY immediate next mating part (currentStep + 1) as subtle reference
            // Eliminates visual clutter so operator sees the active step with 100% clarity!
            if (partStep === currentStep + 1) {
              child.visible = true;
              if (ghostMatRef.current) {
                child.material = ghostMatRef.current;
              }
            } else {
              child.visible = false;
            }
          } else {
            // In pure clean assembly view: upcoming parts hidden
            child.visible = false;
          }
        }

        // 3. Real Metrological Defect Deformation (Physically tilts the ACTIVE step's part in 3D!)
        if (partStep === currentStep) {
          if (isDefectSimulated) {
            const rotDelta = THREE.MathUtils.degToRad(defectAngleOffset);
            child.rotation.z = (child.userData.initialRotZ || 0) + rotDelta;
            child.rotation.x = (child.userData.initialRotX || 0) + (rotDelta * 0.35);

            // Dynamically position the CMM 3D Laser Inspection Wireframe Box around the active part
            if (defectBoxRef.current) {
              defectBoxRef.current.visible = true;
              defectBoxRef.current.position.copy(child.position);
              const absDev = Math.abs(defectAngleOffset);
              if (absDev <= 1.0) {
                defectBoxRef.current.material.color.setHex(0x10b981); // Emerald Green
              } else if (absDev <= 4.0) {
                defectBoxRef.current.material.color.setHex(0xf59e0b); // Warning Amber
              } else {
                defectBoxRef.current.material.color.setHex(0xff0044); // Defect Red
              }
            }
          } else {
            child.rotation.z = child.userData.initialRotZ || 0;
            child.rotation.x = child.userData.initialRotX || 0;
          }
        }
      }
    });

    // Toggle Flywheel hold-down clamps: engaged when Flywheel is seated (Step 2 and above)
    if (clutchClampGroupRef.current) {
      clutchClampGroupRef.current.visible = currentStep >= 2;
    }

    if (!isDefectSimulated && defectBoxRef.current) {
      defectBoxRef.current.visible = false;
    }
  }, [customModel, explodedPercent, currentStep, isDefectSimulated, defectAngleOffset, isXRayMode, activePartKey, showAllParts, isProjectedARMode, isARMode]);

  return (
    <div
      ref={mountRef}
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        cursor: 'grab',
        touchAction: 'none'
      }}
    />
  );
}

import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { soundFx } from '../utils/audio';

export default function CADDrawingStudio({ onSendToAR }) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const meshGroupRef = useRef(null);

  // Parametric CAD Dimensions
  const [componentType, setComponentType] = useState('rotor'); // 'rotor' | 'caliper' | 'piston' | 'knuckle'
  const [outerDiameter, setOuterDiameter] = useState(320); // 260 - 380 mm
  const [discThickness, setDiscThickness] = useState(28); // 18 - 36 mm
  const [lugCount, setLugCount] = useState(5); // 4 or 5
  const [vaneCount, setVaneCount] = useState(24); // 12 - 36
  const [hasCrossDrilled, setHasCrossDrilled] = useState(true);
  const [caliperPistonCount, setCaliperPistonCount] = useState(4); // 2, 4, 6
  const [caliperColor, setCaliperColor] = useState('#ef4444');
  const [knuckleRodDia, setKnuckleRodDia] = useState(30); // 20 - 50 mm
  const [knuckleExploded, setKnuckleExploded] = useState(false);
  const [wireframeMode, setWireframeMode] = useState(false);
  const [exportNotice, setExportNotice] = useState('');

  // Three.js CAD Viewport Initialization
  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a101d);
    sceneRef.current = scene;

    const width = container.clientWidth;
    const height = container.clientHeight;

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(3.5, 2.8, 4.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    rendererRef.current = renderer;
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Blueprint Ground Grid
    const grid = new THREE.GridHelper(10, 30, 0x00f0ff, 0x1e293b);
    grid.position.y = -1.2;
    scene.add(grid);

    // CAD Studio Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.8);
    dirLight.position.set(5, 8, 5);
    scene.add(dirLight);

    const blueLight = new THREE.DirectionalLight(0x00f0ff, 1.2);
    blueLight.position.set(-5, -2, -3);
    scene.add(blueLight);

    // Group for dynamic procedural CAD mesh
    const meshGroup = new THREE.Group();
    scene.add(meshGroup);
    meshGroupRef.current = meshGroup;

    let reqId;
    const animate = () => {
      reqId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(reqId);
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Re-build 3D CAD Geometry whenever dimensions change
  useEffect(() => {
    const group = meshGroupRef.current;
    if (!group) return;

    // Clear old geometry
    while (group.children.length > 0) {
      const obj = group.children[0];
      group.remove(obj);
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
        else obj.material.dispose();
      }
    }

    const scaleFactor = outerDiameter / 320; // relative scale

    if (componentType === 'rotor') {
      // 1. Hat / Center bell
      const hatGeo = new THREE.CylinderGeometry(0.8 * scaleFactor, 0.9 * scaleFactor, 0.35, 36);
      hatGeo.rotateX(Math.PI / 2);
      const hatMat = new THREE.MeshStandardMaterial({
        color: 0x334155,
        metalness: 0.9,
        roughness: 0.35,
        wireframe: wireframeMode
      });
      const hatMesh = new THREE.Mesh(hatGeo, hatMat);
      hatMesh.position.z = 0.2;
      group.add(hatMesh);

      // 2. Stud Holes & PCD
      const studHoleMat = new THREE.MeshBasicMaterial({ color: 0x050811, wireframe: wireframeMode });
      for (let i = 0; i < lugCount; i++) {
        const angle = (i * 2 * Math.PI) / lugCount;
        const studHoleGeo = new THREE.CylinderGeometry(0.065, 0.065, 0.4, 16);
        studHoleGeo.rotateX(Math.PI / 2);
        const studHole = new THREE.Mesh(studHoleGeo, studHoleMat);
        const r = 0.65 * scaleFactor;
        studHole.position.set(Math.cos(angle) * r, Math.sin(angle) * r, 0.22);
        group.add(studHole);
      }

      // 3. Ventilated Rotor Disc Plates
      const discR = (outerDiameter / 320) * 1.85;
      const t = (discThickness / 28) * 0.08;

      const frictionMat = new THREE.MeshStandardMaterial({
        color: 0xc4cbd4,
        metalness: 0.88,
        roughness: 0.2,
        wireframe: wireframeMode
      });

      // Outer face
      const disc1Geo = new THREE.CylinderGeometry(discR, discR, t, 48);
      disc1Geo.rotateX(Math.PI / 2);
      const disc1 = new THREE.Mesh(disc1Geo, frictionMat);
      disc1.position.z = 0.45;
      group.add(disc1);

      // Inner face
      const disc2 = new THREE.Mesh(disc1Geo, frictionMat);
      disc2.position.z = 0.45 - (t * 2.2);
      group.add(disc2);

      // 4. Ventilating Air Vanes
      const vaneMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.8, roughness: 0.4, wireframe: wireframeMode });
      for (let i = 0; i < vaneCount; i++) {
        const angle = (i * 2 * Math.PI) / vaneCount;
        const vaneGeo = new THREE.BoxGeometry(0.65 * scaleFactor, 0.035, t * 1.5);
        const vane = new THREE.Mesh(vaneGeo, vaneMat);
        const vr = 1.35 * scaleFactor;
        vane.position.set(Math.cos(angle) * vr, Math.sin(angle) * vr, 0.45 - t);
        vane.rotation.z = angle + 0.35;
        group.add(vane);
      }

      // 5. Cross-drilled holes
      if (hasCrossDrilled) {
        const drillMat = new THREE.MeshBasicMaterial({ color: 0x050811 });
        for (let r = 1.2; r <= 1.7; r += 0.25) {
          for (let i = 0; i < 12; i++) {
            const angle = (i * 2 * Math.PI) / 12 + (r * 1.4);
            const holeGeo = new THREE.CylinderGeometry(0.032, 0.032, t * 2, 12);
            holeGeo.rotateX(Math.PI / 2);
            const hole = new THREE.Mesh(holeGeo, drillMat);
            hole.position.set(Math.cos(angle) * r * scaleFactor, Math.sin(angle) * r * scaleFactor, 0.45);
            group.add(hole);
          }
        }
      }
    } else if (componentType === 'caliper') {
      // Monoblock Caliper Housing CAD
      const caliperMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(caliperColor),
        metalness: 0.5,
        roughness: 0.25,
        wireframe: wireframeMode
      });

      const bodyGeo = new THREE.BoxGeometry(2.0, 0.9, 0.8);
      const body = new THREE.Mesh(bodyGeo, caliperMat);
      group.add(body);

      // Piston cylinders
      const pistonMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.95, roughness: 0.15, wireframe: wireframeMode });
      const pistonSpacing = 1.5 / caliperPistonCount;
      for (let i = 0; i < caliperPistonCount; i++) {
        const px = -0.75 + (i * pistonSpacing) + (pistonSpacing / 2);
        const pGeo = new THREE.CylinderGeometry(0.18, 0.18, 0.3, 24);
        pGeo.rotateX(Math.PI / 2);
        const piston = new THREE.Mesh(pGeo, pistonMat);
        piston.position.set(px, 0.1, 0.45);
        group.add(piston);
      }
    } else if (componentType === 'piston') {
      // Engine Piston CAD
      const crownMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.85, roughness: 0.25, wireframe: wireframeMode });
      const crownGeo = new THREE.CylinderGeometry(1.0, 1.0, 1.4, 36);
      const crown = new THREE.Mesh(crownGeo, crownMat);
      group.add(crown);

      // Piston Rings
      const ringMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.95 });
      [-0.2, 0.0, 0.2].forEach(y => {
        const ringGeo = new THREE.TorusGeometry(1.01, 0.02, 8, 36);
        ringGeo.rotateX(Math.PI / 2);
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.y = y;
        group.add(ring);
      });

      // Wrist Pin Hole
      const pinHoleGeo = new THREE.CylinderGeometry(0.25, 0.25, 2.1, 24);
      pinHoleGeo.rotateZ(Math.PI / 2);
      const pinHole = new THREE.Mesh(pinHoleGeo, new THREE.MeshBasicMaterial({ color: 0x050811 }));
      pinHole.position.y = -0.3;
      group.add(pinHole);
    } else if (componentType === 'knuckle') {
      // --- Mechanical Knuckle Joint Assembly ---
      // Standard Empirical Machine Design Dimensions:
      // d = rod diameter, d1 = pin diameter = d, D = outer eye = 2d, t = eye thickness = 1.25d
      const s = knuckleRodDia / 30; // Scale relative to 30mm standard
      const explodeOffset = knuckleExploded ? 1.4 * s : 0;

      const forkMat = new THREE.MeshStandardMaterial({
        color: 0x475569,
        metalness: 0.85,
        roughness: 0.3,
        wireframe: wireframeMode
      });
      const eyeMat = new THREE.MeshStandardMaterial({
        color: 0x94a3b8,
        metalness: 0.9,
        roughness: 0.22,
        wireframe: wireframeMode
      });
      const pinMat = new THREE.MeshStandardMaterial({
        color: 0xe2e8f0,
        metalness: 0.95,
        roughness: 0.15,
        wireframe: wireframeMode
      });

      // 1. FORK END (Left Clevis / Double Eye)
      const forkGroup = new THREE.Group();
      // Left cylindrical rod shaft
      const forkRodGeo = new THREE.CylinderGeometry(0.3 * s, 0.3 * s, 1.8 * s, 32);
      forkRodGeo.rotateZ(Math.PI / 2);
      const forkRod = new THREE.Mesh(forkRodGeo, forkMat);
      forkRod.position.x = -1.4 * s;
      forkGroup.add(forkRod);

      // Octagonal transition collar
      const forkCollarGeo = new THREE.CylinderGeometry(0.42 * s, 0.42 * s, 0.3 * s, 8);
      forkCollarGeo.rotateZ(Math.PI / 2);
      const forkCollar = new THREE.Mesh(forkCollarGeo, forkMat);
      forkCollar.position.x = -0.55 * s;
      forkGroup.add(forkCollar);

      // Upper Fork Ear
      const upperEarGeo = new THREE.CylinderGeometry(0.55 * s, 0.55 * s, 0.28 * s, 32);
      const upperEar = new THREE.Mesh(upperEarGeo, forkMat);
      upperEar.position.set(0, 0.5 * s, 0);
      forkGroup.add(upperEar);

      // Lower Fork Ear
      const lowerEarGeo = new THREE.CylinderGeometry(0.55 * s, 0.55 * s, 0.28 * s, 32);
      const lowerEar = new THREE.Mesh(lowerEarGeo, forkMat);
      lowerEar.position.set(0, -0.5 * s, 0);
      forkGroup.add(lowerEar);

      // Fork bridge back connecting ears to rod
      const forkBridgeGeo = new THREE.BoxGeometry(0.7 * s, 1.25 * s, 0.65 * s);
      const forkBridge = new THREE.Mesh(forkBridgeGeo, forkMat);
      forkBridge.position.set(-0.35 * s, 0, 0);
      forkGroup.add(forkBridge);

      group.add(forkGroup);

      // 2. EYE END (Right Rod / Single Eye)
      const eyeGroup = new THREE.Group();
      // Right cylindrical rod shaft
      const eyeRodGeo = new THREE.CylinderGeometry(0.3 * s, 0.3 * s, 1.8 * s, 32);
      eyeRodGeo.rotateZ(Math.PI / 2);
      const eyeRod = new THREE.Mesh(eyeRodGeo, eyeMat);
      eyeRod.position.x = 1.4 * s + explodeOffset;
      eyeGroup.add(eyeRod);

      // Octagonal transition collar
      const eyeCollarGeo = new THREE.CylinderGeometry(0.42 * s, 0.42 * s, 0.3 * s, 8);
      eyeCollarGeo.rotateZ(Math.PI / 2);
      const eyeCollar = new THREE.Mesh(eyeCollarGeo, eyeMat);
      eyeCollar.position.x = 0.55 * s + explodeOffset;
      eyeGroup.add(eyeCollar);

      // Single Eye Body (Fits snugly inside the fork gap)
      const singleEyeGeo = new THREE.CylinderGeometry(0.55 * s, 0.55 * s, 0.62 * s, 32);
      const singleEye = new THREE.Mesh(singleEyeGeo, eyeMat);
      singleEye.position.set(explodeOffset, 0, 0);
      eyeGroup.add(singleEye);

      group.add(eyeGroup);

      // 3. KNUCKLE PIN
      const pinGroup = new THREE.Group();
      // Main pin shank passing through ears and eye
      const pinShankGeo = new THREE.CylinderGeometry(0.28 * s, 0.28 * s, 1.8 * s, 32);
      const pinShank = new THREE.Mesh(pinShankGeo, pinMat);
      pinGroup.add(pinShank);

      // Large Pin Head at the top
      const pinHeadGeo = new THREE.CylinderGeometry(0.45 * s, 0.45 * s, 0.22 * s, 32);
      const pinHead = new THREE.Mesh(pinHeadGeo, pinMat);
      pinHead.position.y = 0.95 * s;
      pinGroup.add(pinHead);

      // 4. BOTTOM COLLAR & SPLIT TAPER PIN
      const bottomCollarGeo = new THREE.CylinderGeometry(0.42 * s, 0.42 * s, 0.18 * s, 32);
      const bottomCollar = new THREE.Mesh(bottomCollarGeo, pinMat);
      bottomCollar.position.y = -0.8 * s;
      pinGroup.add(bottomCollar);

      // Split Pin
      const splitPinGeo = new THREE.CylinderGeometry(0.04 * s, 0.04 * s, 0.7 * s, 16);
      splitPinGeo.rotateZ(Math.PI / 2);
      const splitPin = new THREE.Mesh(splitPinGeo, forkMat);
      splitPin.position.y = -0.8 * s;
      pinGroup.add(splitPin);

      // If exploded view active: lift pin up!
      if (knuckleExploded) {
        pinGroup.position.y = 1.6 * s;
      }

      group.add(pinGroup);
    }
  }, [componentType, outerDiameter, discThickness, lugCount, vaneCount, hasCrossDrilled, caliperPistonCount, caliperColor, knuckleRodDia, knuckleExploded, wireframeMode]);

  // Handle Export to AR
  const handleExportToAR = () => {
    soundFx.playSuccess();
    setExportNotice('✓ CAD Geometry compiled and deployed into AR Assembly line!');
    setTimeout(() => setExportNotice(''), 3500);

    if (onSendToAR) {
      onSendToAR({
        componentType,
        outerDiameter,
        discThickness,
        lugCount,
        vaneCount,
        hasCrossDrilled,
        caliperColor,
        caliperPistonCount
      });
    }
  };

  // Download .OBJ CAD file
  const handleDownloadOBJ = () => {
    soundFx.playClick();
    const group = meshGroupRef.current;
    if (!group) return;

    let objContent = `# AutoAR Parametric CAD Export - ${componentType.toUpperCase()}\n# Generated on ${new Date().toISOString()}\n`;
    let vertexOffset = 1;

    group.traverse(child => {
      if (child.isMesh && child.geometry) {
        const geo = child.geometry.toNonIndexed ? child.geometry.toNonIndexed() : child.geometry;
        const pos = geo.attributes.position;
        if (!pos) return;

        objContent += `\no ${child.name || 'mesh_part'}\n`;
        for (let i = 0; i < pos.count; i++) {
          const v = new THREE.Vector3(pos.getX(i), pos.getY(i), pos.getZ(i));
          v.applyMatrix4(child.matrixWorld);
          objContent += `v ${v.x.toFixed(4)} ${v.y.toFixed(4)} ${v.z.toFixed(4)}\n`;
        }
        for (let i = 0; i < pos.count; i += 3) {
          objContent += `f ${vertexOffset + i} ${vertexOffset + i + 1} ${vertexOffset + i + 2}\n`;
        }
        vertexOffset += pos.count;
      }
    });

    const blob = new Blob([objContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AutoAR_${componentType}_CAD_Model.obj`;
    a.click();
    URL.revokeObjectURL(url);
    soundFx.playSuccess();
  };

  return (
    <div className="cad-studio-wrap">
      {/* CAD Studio Controls Sidebar */}
      <div className="cad-controls-panel">
        <div className="cad-panel-header">
          <span className="cad-icon">📐</span>
          <div>
            <h3>3D CAD PARAMETRIC MODELER</h3>
            <p>SolidWorks-Equivalent Browser Drafting Studio</p>
          </div>
        </div>

        {/* Component Selector */}
        <div className="cad-field-group">
          <label>SELECT COMPONENT TO DRAW:</label>
          <div className="cad-btn-row">
            <button
              className={`btn-cad-tab ${componentType === 'rotor' ? 'active' : ''}`}
              onClick={() => { setComponentType('rotor'); soundFx.playClick(); }}
            >
              Disc Rotor
            </button>
            <button
              className={`btn-cad-tab ${componentType === 'caliper' ? 'active' : ''}`}
              onClick={() => { setComponentType('caliper'); soundFx.playClick(); }}
            >
              Brake Caliper
            </button>
            <button
              className={`btn-cad-tab ${componentType === 'piston' ? 'active' : ''}`}
              onClick={() => { setComponentType('piston'); soundFx.playClick(); }}
            >
              Engine Piston
            </button>
            <button
              className={`btn-cad-tab ${componentType === 'knuckle' ? 'active' : ''}`}
              onClick={() => { setComponentType('knuckle'); soundFx.playClick(); }}
            >
              Knuckle Joint
            </button>
          </div>
        </div>

        {/* Dynamic Sliders based on selected component */}
        {componentType === 'rotor' && (
          <div className="cad-parameters-box">
            <h4>ROTOR DIMENSION SPECIFICATIONS</h4>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Outer Diameter (Ø):</span>
                <span className="font-mono text-cyan">{outerDiameter} mm</span>
              </div>
              <input
                type="range"
                min="260"
                max="380"
                step="5"
                value={outerDiameter}
                onChange={(e) => setOuterDiameter(Number(e.target.value))}
              />
            </div>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Nominal Thickness (t):</span>
                <span className="font-mono text-cyan">{discThickness} mm</span>
              </div>
              <input
                type="range"
                min="20"
                max="36"
                step="1"
                value={discThickness}
                onChange={(e) => setDiscThickness(Number(e.target.value))}
              />
            </div>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>PCD Lug Pattern:</span>
                <span className="font-mono text-gold">{lugCount} x 114.3 mm</span>
              </div>
              <div className="cad-toggle-btn-row">
                <button
                  className={lugCount === 4 ? 'active' : ''}
                  onClick={() => setLugCount(4)}
                >
                  4-Lug Pattern
                </button>
                <button
                  className={lugCount === 5 ? 'active' : ''}
                  onClick={() => setLugCount(5)}
                >
                  5-Lug Pattern
                </button>
              </div>
            </div>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Ventilation Air Vanes:</span>
                <span className="font-mono text-cyan">{vaneCount} Vanes</span>
              </div>
              <input
                type="range"
                min="12"
                max="32"
                step="2"
                value={vaneCount}
                onChange={(e) => setVaneCount(Number(e.target.value))}
              />
            </div>

            <div className="cad-param-row-checkbox">
              <label>
                <input
                  type="checkbox"
                  checked={hasCrossDrilled}
                  onChange={(e) => setHasCrossDrilled(e.target.checked)}
                />
                <span>Include CNC Cross-Drilled Cooling Holes</span>
              </label>
            </div>
          </div>
        )}

        {componentType === 'caliper' && (
          <div className="cad-parameters-box">
            <h4>CALIPER HOUSING SPECIFICATIONS</h4>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Piston Configuration:</span>
                <span className="font-mono text-cyan">{caliperPistonCount} Pistons</span>
              </div>
              <div className="cad-toggle-btn-row">
                <button className={caliperPistonCount === 2 ? 'active' : ''} onClick={() => setCaliperPistonCount(2)}>2-Piston</button>
                <button className={caliperPistonCount === 4 ? 'active' : ''} onClick={() => setCaliperPistonCount(4)}>4-Piston</button>
                <button className={caliperPistonCount === 6 ? 'active' : ''} onClick={() => setCaliperPistonCount(6)}>6-Piston</button>
              </div>
            </div>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Finish Color:</span>
              </div>
              <div className="cad-color-picker-row">
                {['#ef4444', '#f59e0b', '#06b6d4', '#10b981', '#1e293b'].map(c => (
                  <div
                    key={c}
                    className={`color-swatch ${caliperColor === c ? 'active' : ''}`}
                    style={{ backgroundColor: c }}
                    onClick={() => setCaliperColor(c)}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {componentType === 'knuckle' && (
          <div className="cad-parameters-box">
            <h4>KNUCKLE JOINT MACHINE DESIGN (SAE / DIN)</h4>

            <div className="cad-param-row">
              <div className="cad-param-label">
                <span>Rod Diameter (d):</span>
                <span className="font-mono text-cyan">{knuckleRodDia} mm</span>
              </div>
              <input
                type="range"
                min="20"
                max="50"
                step="2"
                value={knuckleRodDia}
                onChange={(e) => setKnuckleRodDia(Number(e.target.value))}
              />
            </div>

            {/* Standard Machine Design Empirical Proportions */}
            <div className="cad-proportions-grid" style={{ background: 'rgba(15,23,42,0.8)', padding: '8px', borderRadius: '4px', fontSize: '10px' }}>
              <div style={{ color: 'var(--text-dim)', marginBottom: '4px' }}>EMPIRICAL PROPORTIONS:</div>
              <div>• Pin Diameter (d1 = d): <strong className="text-cyan font-mono">{knuckleRodDia} mm</strong></div>
              <div>• Outer Eye Dia (D = 2d): <strong className="text-gold font-mono">{knuckleRodDia * 2} mm</strong></div>
              <div>• Single Eye Thick (t = 1.25d): <strong className="font-mono">{(knuckleRodDia * 1.25).toFixed(1)} mm</strong></div>
              <div>• Fork Ear Thick (t1 = 0.75d): <strong className="font-mono">{(knuckleRodDia * 0.75).toFixed(1)} mm</strong></div>
            </div>

            <div className="cad-param-row">
              <button
                className="btn-cad-tab active"
                style={{ width: '100%', marginTop: '6px' }}
                onClick={() => { setKnuckleExploded(!knuckleExploded); soundFx.playClick(); }}
              >
                {knuckleExploded ? '🔗 Assemble Knuckle Joint' : '💥 Explode Joint (Pin & Eye)'}
              </button>
            </div>
          </div>
        )}

        {/* View Options */}
        <div className="cad-view-options">
          <label>
            <input
              type="checkbox"
              checked={wireframeMode}
              onChange={(e) => setWireframeMode(e.target.checked)}
            />
            <span>Wireframe CAD Tessellation Mode</span>
          </label>
        </div>

        {/* Action Buttons */}
        <div className="cad-actions-col">
          <button className="btn-send-to-ar" onClick={handleExportToAR}>
            🚀 Send to AR Assembly Workstation
          </button>
          <button className="btn-download-cad" onClick={handleDownloadOBJ}>
            💾 Download 3D CAD File (.OBJ)
          </button>
        </div>

        {exportNotice && <div className="cad-export-notice">{exportNotice}</div>}
      </div>

      {/* CAD 3D Drafting Canvas */}
      <div className="cad-viewport-wrap">
        <div ref={mountRef} className="cad-three-container" />

        {/* Blueprint Callout Badge Overlay */}
        <div className="cad-dimension-badge">
          <div className="badge-title">AUTOCAD / SOLIDWORKS DIGITAL TWIN EXPORT</div>
          <div className="badge-data font-mono">
            <span>SCALE: 1:1</span>
            <span>TOLERANCE: ±0.05 mm</span>
            <span>STANDARD: ISO 2768-m</span>
          </div>
        </div>
      </div>
    </div>
  );
}

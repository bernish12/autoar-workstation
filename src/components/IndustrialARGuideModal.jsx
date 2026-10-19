import React from 'react';

export default function IndustrialARGuideModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="industrial-ar-modal-card">
        {/* Modal Header */}
        <div className="ar-modal-header">
          <div className="ar-modal-brand">
            <span className="ar-brand-badge">⚡ INDUSTRIAL AR</span>
            <div>
              <h3>AUGMENTED REALITY (AR) IN AUTOMOTIVE ASSEMBLY</h3>
              <p>How Real-World Smart Glasses & Projected Lasers Guide Operators with Zero Errors</p>
            </div>
          </div>
          <button className="btn-close-modal" onClick={onClose}>✕</button>
        </div>

        {/* Visual Real Factory Banner */}
        <div className="ar-visual-hero-banner">
          <div className="ar-banner-image-container">
            <img
              src="/ar_factory_real_demo.jpg"
              alt="Real World AR Automotive Assembly in Factory"
              className="ar-banner-img"
            />
            <div className="ar-banner-overlay-tags">
              <span className="ar-tag tag-green">✔ Real-Time AR Hologram: Rotor & Caliper</span>
              <span className="ar-tag tag-cyan">✔ IoT Bluetooth Torque: 110 Nm Verified</span>
              <span className="ar-tag tag-amber">✔ Wearable Smart Glass: 6-DoF Optical Tracking</span>
            </div>
          </div>
        </div>

        {/* Core Pillars Grid */}
        <div className="ar-pillars-grid">
          {/* Pillar 1: Digital Overlay */}
          <div className="ar-pillar-card">
            <div className="pillar-icon-box">🥽</div>
            <h4>1. Digital Overlay (Digital Twin on Real World)</h4>
            <p>
              In traditional manufacturing, operators consult 200-page paper binders or 2D blueprints.
              With industrial AR (<strong>PTC Vuforia Studio</strong> & <strong>Dassault DELMIA</strong>),
              3D CAD data is spatially tracked and overlaid directly onto the physical workpiece in real time through AR smart glasses (HoloLens 2, RealWear), tablets, or WebXR browsers.
            </p>
            <div className="pillar-tech-badge">
              <span>AutoAR Implementation:</span> Three.js PBR WebGL 2.0 + Live 1080p Camera Stream + 6-DoF Spatial Pose Tracking
            </div>
          </div>

          {/* Pillar 2: Projected Work Instructions (Light Guide Systems) */}
          <div className="ar-pillar-card">
            <div className="pillar-icon-box">📽️</div>
            <h4>2. Projected Work Instructions & Pick-to-Light</h4>
            <p>
              As showcased by <strong>Light Guide Systems</strong>, industrial overhead projection systems beam high-intensity laser lines, animated insertion arrows, part outlines, and pick-to-light bin indicators directly onto factory assembly benches.
              Workers never have to guess which fastener or hole comes next.
            </p>
            <div className="pillar-tech-badge">
              <span>AutoAR Implementation:</span> 3D Dynamic Laser Mating Vectors + Pick-to-Light Shelf Telemetry + Real-Time Insertion Chevrons
            </div>
          </div>

          {/* Pillar 3: Hands-Free Voice Operation */}
          <div className="ar-pillar-card">
            <div className="pillar-icon-box">🎙️</div>
            <h4>3. Hands-Free Voice Operation</h4>
            <p>
              Assembly operators wear heavy protective gloves and hold tools (pneumatic torque wrenches, mallets).
              They cannot touch a screen or keyboard. Leading platforms (<strong>RealWear HMT-1</strong>, <strong>Tulip Interfaces</strong>) rely on speech recognition so operators advance steps hands-free by speaking.
            </p>
            <div className="pillar-tech-badge">
              <span>AutoAR Implementation:</span> Web Speech API Recognition ("Next Step", "Explode", "Torque", "CMM Scan")
            </div>
          </div>

          {/* Pillar 4: Error Reduction & Poka-Yoke Quality Verification */}
          <div className="ar-pillar-card">
            <div className="pillar-icon-box">🔬</div>
            <h4>4. Error Reduction & Poka-Yoke Verification</h4>
            <p>
              Connected worker platforms (<strong>Tulip</strong>, <strong>Workerbase</strong>, <strong>Cognex Vision</strong>) prevent assembly defects before they leave the station.
              Computer vision scans part orientation, verifies calibrated fastener torque, and halts the line if a dimensional defect is detected.
            </p>
            <div className="pillar-tech-badge">
              <span>AutoAR Implementation:</span> Real-Time Laser CMM Metrology + IoT Torque Wrench Lock + ISO 9001 Digital QC Certificate
            </div>
          </div>
        </div>

        {/* Industrial Software Ecosystem Comparison Table */}
        <div className="ar-software-comparison-box">
          <h4>🏭 INDUSTRIAL AR SOFTWARE COMPARISON MATRIX</h4>
          <table className="ar-matrix-table">
            <thead>
              <tr>
                <th>Software Platform</th>
                <th>Primary Use Case</th>
                <th>Hardware Target</th>
                <th>AutoAR Equivalent Feature</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>PTC Vuforia Studio</strong></td>
                <td>Model Target 3D CAD Tracking & 3D Work Instructions</td>
                <td>HoloLens 2, iPad Pro, Android</td>
                <td>SolidWorks .OBJ/.GLB Direct Import & 3D Interactive Explosion</td>
              </tr>
              <tr>
                <td><strong>Light Guide Systems</strong></td>
                <td>Projected Augmented Work Instructions & Pick-to-Light</td>
                <td>Industrial Ceiling Laser Projectors</td>
                <td>Projected Laser Guidance & Animated Mating Chevrons</td>
              </tr>
              <tr>
                <td><strong>Tulip Interfaces / Workerbase</strong></td>
                <td>No-Code Connected Worker Shop Floor & IoT Torque</td>
                <td>Touch Terminals, Smart Tools</td>
                <td>Smart IoT Torque Wrench Simulator & Cycle Stopwatch</td>
              </tr>
              <tr>
                <td><strong>Dassault DELMIA Augmented Exp</strong></td>
                <td>Aerospace & Automotive Complex Kinematic Assembly</td>
                <td>Wearable Smart Glasses, CMM Rigs</td>
                <td>Real Laser CMM Realignment & Kinematic Swivel Inspection</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="ar-modal-footer">
          <div className="footer-citation">
            Reference: <a href="https://www.youtube.com/watch?v=7EQD7AMwCfI" target="_blank" rel="noreferrer">Projected Work Instructions (Augmented Reality) Explained - Light Guide Systems</a>
          </div>
          <button className="btn-close-accent" onClick={onClose}>
            ✓ UNDERSTOOD & RETURN TO AR WORKSTATION
          </button>
        </div>
      </div>
    </div>
  );
}

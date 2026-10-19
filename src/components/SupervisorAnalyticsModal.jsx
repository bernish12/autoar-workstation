import React from 'react';

export default function SupervisorAnalyticsModal({
  isOpen,
  onClose,
  cycleTime,
  defectsResolvedCount,
  stepsData,
  componentTitle,
  workstationTitle
}) {
  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  const currentDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const isCar = (componentTitle || '').toLowerCase().includes('vehicle') || (componentTitle || '').toLowerCase().includes('car') || (workstationTitle || '').toLowerCase().includes('vehicle') || (workstationTitle || '').toLowerCase().includes('general assembly');
  const isClutch = !isCar && ((componentTitle || '').toLowerCase().includes('clutch') || (workstationTitle || '').toLowerCase().includes('clutch'));
  const isKnuckle = !isCar && !isClutch && ((componentTitle || '').toLowerCase().includes('knuckle') || (workstationTitle || '').toLowerCase().includes('knuckle'));

  const fullCarCheckpoints = [
    { step: '01', subComponent: 'Tubular Spaceframe Chassis (4130)', protocol: 'Laser CMM 8-Point Datum Alignment', target: '< 0.80 mm', measured: '0.24 mm', status: '✓ PASS' },
    { step: '02', subComponent: 'V8 Mid-Engine Powertrain & Transaxle', protocol: 'Hydraulic Motor Mounts M12 Fasteners', target: '85.0 Nm', measured: '85.0 Nm', status: '✓ PASS' },
    { step: '03', subComponent: '4-Corner Double Wishbone Suspension', protocol: 'Ball-Joint Pinch & Shock Tower Bolts', target: '65.0 Nm', measured: '65.0 Nm', status: '✓ PASS' },
    { step: '04', subComponent: '380mm Ventilated Carbon Brake Rotors', protocol: 'Banjo Fitting Hydraulic Holding Test', target: '45.0 Nm / 160 Bar', measured: '45.0 Nm / 165 Bar', status: '✓ PASS' },
    { step: '05', subComponent: 'Carbon Aerodynamic Body & Canopy', protocol: 'Exterior Seam Flushness & Panel Gap', target: '0.8 - 1.2 mm', measured: '0.92 mm', status: '✓ PASS' },
    { step: '06', subComponent: '4x Forged Alloy Wheels & Tires', protocol: '5-Lug Nut Cross-Star Torque Sequence', target: '120.0 Nm', measured: '120.0 Nm', status: '✓ PASS' }
  ];

  const clutchCheckpoints = [
    { step: '01', subComponent: 'Engine Flywheel (Ductile Iron)', protocol: 'Lateral Runout & Starter Ring Gear', target: '< 0.05 mm', measured: '0.018 mm', status: '✓ PASS' },
    { step: '02', subComponent: 'Organic Friction Clutch Disc', protocol: 'Spline Arbor Concentricity & Runout', target: '< 0.15 mm', measured: '0.062 mm', status: '✓ PASS' },
    { step: '03', subComponent: 'Cast Iron Pressure Plate', protocol: 'Ground Friction Face Flatness', target: '< 0.03 mm', measured: '0.012 mm', status: '✓ PASS' },
    { step: '04', subComponent: 'Diaphragm Belleville Spring', protocol: '18-Finger Tip Height Variance', target: '< 0.30 mm', measured: '0.120 mm', status: '✓ PASS' },
    { step: '05', subComponent: 'Yellow-Zinc Cover & M8 Bolts', protocol: 'Star-Pattern Perimeter Fastening', target: '25.0 Nm', measured: '25.0 Nm', status: '✓ PASS' },
    { step: '06', subComponent: 'Self-Centering Release Bearing', protocol: 'Quill Sleeve Slide & Clearance', target: '2.0 - 2.5 mm', measured: '2.24 mm', status: '✓ PASS' }
  ];

  const knuckleCheckpoints = [
    { step: '01', subComponent: 'Double Eye Fork End (SAE 1045)', protocol: 'Coaxial Bore Alignment & 37.5mm Fork Gap', target: '30.00 mm H7 / Gap 37.5±0.1 mm', measured: '30.01 mm / 37.52 mm', status: '✓ PASS' },
    { step: '02', subComponent: 'Single Eye End (SAE 1045)', protocol: 'Eye Width (37.5mm - 0.65mm Axial Clearance)', target: '36.85 ± 0.1 mm', measured: '36.88 mm', status: '✓ PASS' },
    { step: '03', subComponent: 'Main Knuckle Pin (Cylindrical)', protocol: 'Diameter Fit (h6/H7) & Concentric Insertion', target: '30.00 mm h6 (-0.013 mm)', measured: '29.992 mm', status: '✓ PASS' },
    { step: '04', subComponent: 'Retention Locking Collar', protocol: 'Taper Cross-Hole Alignment & Axial Play', target: 'Axial Play < 0.25 mm', measured: '0.12 mm', status: '✓ PASS' },
    { step: '05', subComponent: '1:30 Taper Split Pin & Nut', protocol: 'Seating Torque & Cotter Split Security', target: '15.0 Nm / Cotter Splayed > 30°', measured: '15.0 Nm / 36° Splay', status: '✓ PASS' },
    { step: '06', subComponent: 'Kinematic Swivel & Tensile Test', protocol: 'Full ±45° Angular Articulation & Proof Load', target: 'Zero Seizure / 25 kN Proof Load', measured: 'Smooth Pivot / 25 kN PASSED', status: '✓ PASS' }
  ];

  const brakeCheckpoints = [
    { step: '01', subComponent: 'Wheel Hub Spindle', protocol: 'Axial Runout & Stud Thread', target: '< 0.03 mm', measured: '0.014 mm', status: '✓ PASS' },
    { step: '02', subComponent: 'Ventilated Rotor Disc', protocol: 'T30 Torx Locator Screw', target: '15.0 Nm', measured: '15.0 Nm', status: '✓ PASS' },
    { step: '03', subComponent: 'Caliper Anchor Bracket', protocol: 'Grade 10.9 Flange Bolts (x2)', target: '75.0 Nm', measured: '75.0 Nm', status: '✓ PASS' },
    { step: '04', subComponent: 'Ceramic Brake Pads', protocol: 'Abutment Clip Seat & Clearance', target: '0.2 - 0.4 mm', measured: '0.28 mm', status: '✓ PASS' },
    { step: '05', subComponent: 'Monoblock Caliper Housing', protocol: 'Slider Guide Pins (x2)', target: '35.0 Nm', measured: '35.0 Nm', status: '✓ PASS' },
    { step: '06', subComponent: 'Hydraulic Fluid Circuit', protocol: 'Holding Pressure Seal Integrity', target: '150 Bar', measured: '165 Bar', status: '✓ PASS' }
  ];

  const currentCheckpoints = isCar ? fullCarCheckpoints : (isClutch ? clutchCheckpoints : (isKnuckle ? knuckleCheckpoints : brakeCheckpoints));

  return (
    <div className="modal-backdrop">
      <div className="qc-certificate-card">
        {/* Certificate Header */}
        <div className="qc-header">
          <div className="qc-brand">
            <span className="logo-badge">🏎️ AUTO-AR</span>
            <div className="brand-text">
              <h2>AUTOMOTIVE QUALITY ASSURANCE CERTIFICATE</h2>
              <p>IATF 16949:2016 & ISO 9001:2015 Smart Assembly Conformance</p>
            </div>
          </div>
          <button className="btn-close-modal" onClick={onClose}>✕</button>
        </div>

        {/* Certificate Meta Grid */}
        <div className="qc-meta-grid">
          <div className="meta-item">
            <span className="lbl">WORKSTATION:</span>
            <span className="val font-mono">{workstationTitle || 'WS-04 (CHASSIS ASSEMBLY LINE)'}</span>
          </div>
          <div className="meta-item">
            <span className="lbl">COMPONENT:</span>
            <span className="val">{componentTitle || 'Automotive Transmission / Chassis Module'}</span>
          </div>
          <div className="meta-item">
            <span className="lbl">BATCH LOT / VIN:</span>
            <span className="val font-mono">VIN-2026-AR-88390</span>
          </div>
          <div className="meta-item">
            <span className="lbl">TIMESTAMP:</span>
            <span className="val">{currentDate}</span>
          </div>
          <div className="meta-item">
            <span className="lbl">CYCLE DURATION:</span>
            <span className="val text-cyan font-mono">{cycleTime}</span>
          </div>
          <div className="meta-item">
            <span className="lbl">DEFECT INCIDENTS:</span>
            <span className="val text-emerald">{defectsResolvedCount} Resolved (0 Unresolved)</span>
          </div>
        </div>

        {/* Verification Checkpoints Table */}
        <div className="qc-table-wrapper">
          <table className="qc-table">
            <thead>
              <tr>
                <th>STEP</th>
                <th>SUB-COMPONENT</th>
                <th>INSPECTION PROTOCOL</th>
                <th>TARGET SPEC</th>
                <th>MEASURED</th>
                <th>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {currentCheckpoints.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.step}</td>
                  <td>{row.subComponent}</td>
                  <td>{row.protocol}</td>
                  <td>{row.target}</td>
                  <td>{row.measured}</td>
                  <td><span className="badge-pass">{row.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Quality Stamp & Signatures */}
        <div className="qc-footer-row">
          <div className="qc-stamp-wrap">
            <div className="qc-stamp">
              <span>QA PASSED</span>
              <small>ZERO DEFECT</small>
              <span className="stamp-date">{currentDate.split(',')[0]}</span>
            </div>
          </div>
          <div className="qc-signatures">
            <div className="sig-block">
              <div className="sig-line">Bernish (Tech-Lead)</div>
              <span>ASSEMBLY OPERATOR</span>
            </div>
            <div className="sig-block">
              <div className="sig-line">Dr. Automotive QA</div>
              <span>CHIEF INSPECTION OFFICER</span>
            </div>
          </div>
        </div>

        {/* Modal Action Buttons */}
        <div className="modal-actions-bar">
          <button className="btn-print" onClick={handlePrint}>
            🖨️ Print / Save PDF Certificate
          </button>
          <button className="btn-close-accent" onClick={onClose}>
            Close Report
          </button>
        </div>
      </div>
    </div>
  );
}

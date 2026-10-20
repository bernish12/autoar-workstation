import React, { useState, useEffect, useRef } from 'react';
import { soundFx } from '../utils/audio';

export default function AROverlayHUD({
  isARMode,
  isProjectedARMode,
  isDefectSimulated,
  currentStepData,
  totalSteps = 6,
  defectValue,
  onAdjustDefectValue,
  onResolveDefect,
  onVoiceCommand,
  isVoiceListening,
  onToggleVoiceListening,
  lastVoiceCommand,
  onOpenARArchitectureModal
}) {
  const [telemetry, setTelemetry] = useState({
    x: 0.142,
    y: -0.028,
    z: 0.485,
    pitch: 1.2,
    roll: -0.4,
    fps: 60
  });

  const [speechSupported, setSpeechSupported] = useState(false);
  const [isTelemetryExpanded, setIsTelemetryExpanded] = useState(false);
  const recognitionRef = useRef(null);

  // Micro-jitter simulation for authentic AR telemetry look
  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry({
        x: (0.14 + (Math.random() - 0.5) * 0.006).toFixed(3),
        y: (-0.03 + (Math.random() - 0.5) * 0.005).toFixed(3),
        z: (0.48 + (Math.random() - 0.5) * 0.004).toFixed(3),
        pitch: (1.2 + (Math.random() - 0.5) * 0.2).toFixed(1),
        roll: (-0.4 + (Math.random() - 0.5) * 0.2).toFixed(1),
        fps: Math.floor(58 + Math.random() * 4)
      });
    }, 450);
    return () => clearInterval(interval);
  }, []);

  // Web Speech API Industrial Hands-Free Voice Listener
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }
    setSpeechSupported(true);

    if (isVoiceListening) {
      let active = true;
      let recognition = null;

      const initRecognition = () => {
        try {
          const rec = new SpeechRecognition();
          rec.continuous = true;
          rec.interimResults = false;
          rec.lang = 'en-IN'; // Indian English + Tanglish / Tamil phonetic support

          let lastCmdTime = 0;
          rec.onresult = (event) => {
            // Acoustic Echo Cancellation: ignore microphone while system voice assistant is speaking
            if (soundFx.isSpeaking) {
              return;
            }
            const now = Date.now();
            if (now - lastCmdTime < 1200) {
              return; // Debounce rapid repeat commands
            }

            const lastIdx = event.results.length - 1;
            const transcript = event.results[lastIdx][0].transcript.trim().toLowerCase();
            console.log('[AR Voice Heard]:', transcript);
            lastCmdTime = now;

            // Comprehensive Tamil & English Voice Command Dictionary
            if (transcript.includes('next') || transcript.includes('aduthu') || transcript.includes('adutha') || transcript.includes('forward') || transcript.includes('அடுத்து')) {
              onVoiceCommand && onVoiceCommand('next', 'Next Step (அடுத்த படி)');
            } else if (transcript.includes('previous') || transcript.includes('back') || transcript.includes('munnadi') || transcript.includes('pinnadi') || transcript.includes('முன்னாடி')) {
              onVoiceCommand && onVoiceCommand('prev', 'Previous Step (முந்தைய படி)');
            } else if (transcript.includes('explode') || transcript.includes('expand') || transcript.includes('split') || transcript.includes('piri') || transcript.includes('viri') || transcript.includes('பிரி')) {
              onVoiceCommand && onVoiceCommand('explode', 'Explode View (பிரி)');
            } else if (transcript.includes('assemble') || transcript.includes('collapse') || transcript.includes('join') || transcript.includes('serthu') || transcript.includes('ser') || transcript.includes('poruthu') || transcript.includes('சேர்')) {
              onVoiceCommand && onVoiceCommand('assemble', 'Assemble Model (சேர்)');
            } else if (transcript.includes('torque') || transcript.includes('fasten') || transcript.includes('tight') || transcript.includes('bolt') || transcript.includes('screw') || transcript.includes('irukku') || transcript.includes('முறுக்கு')) {
              onVoiceCommand && onVoiceCommand('torque', 'Fasten Torque (முறுக்கு)');
            } else if (transcript.includes('scan') || transcript.includes('defect') || transcript.includes('laser') || transcript.includes('check') || transcript.includes('paaru') || transcript.includes('ஸ்கேன்')) {
              onVoiceCommand && onVoiceCommand('scan', 'Laser CMM Scan (ஸ்கேன்)');
            } else if (transcript.includes('calibrate') || transcript.includes('realign') || transcript.includes('resolve') || transcript.includes('fix') || transcript.includes('sari') || transcript.includes('சரி')) {
              onVoiceCommand && onVoiceCommand('calibrate', 'Auto-Calibrate (சரிசெய்)');
            } else if (transcript.includes('xray') || transcript.includes('x-ray') || transcript.includes('transparent') || transcript.includes('எக்ஸ்ரே')) {
              onVoiceCommand && onVoiceCommand('xray', 'Toggle X-Ray (எக்ஸ்ரே)');
            } else if (transcript.includes('rotate') || transcript.includes('spin') || transcript.includes('suthu') || transcript.includes('thiruppu') || transcript.includes('turn') || transcript.includes('சுத்து')) {
              onVoiceCommand && onVoiceCommand('rotate', '360° Spin (சுழற்று)');
            } else if (transcript.includes('camera') || transcript.includes('cam') || transcript.includes('ar') || transcript.includes('கேமரா')) {
              onVoiceCommand && onVoiceCommand('camera', 'AR Camera (கேமரா)');
            } else if (transcript.includes('repeat') || transcript.includes('again') || transcript.includes('guide') || transcript.includes('voice') || transcript.includes('audio') || transcript.includes('pesu') || transcript.includes('sollu') || transcript.includes('kelu') || transcript.includes('பேசு')) {
              onVoiceCommand && onVoiceCommand('repeat', 'Repeat Audio Guide (வழிகாட்டல் பேசு)');
            } else if (transcript.includes('certificate') || transcript.includes('report') || transcript.includes('qc') || transcript.includes('pass') || transcript.includes('சான்றிதழ்')) {
              onVoiceCommand && onVoiceCommand('certificate', 'Open QC Certificate (சான்றிதழ்)');
            } else if (transcript.includes('qr') || transcript.includes('barcode') || transcript.includes('poka') || transcript.includes('part scan') || transcript.includes('கியூஆர்') || transcript.includes('பார்கோடு')) {
              onVoiceCommand && onVoiceCommand('qr', 'Scan Part QR (கியூஆர் ஸ்கேனர்)');
            }
          };

          rec.onerror = (e) => {
            console.warn('[AR Voice Error]:', e.error);
            // If mic stopped or errored out, try restarting if user still has voice on
            if (active && (e.error === 'no-speech' || e.error === 'network')) {
              try { rec.stop(); } catch(_) {}
            }
          };

          rec.onend = () => {
            // Keep continuously listening without dying when worker pauses speaking!
            if (active && isVoiceListening) {
              setTimeout(() => {
                if (active) {
                  try { rec.start(); } catch(_) {}
                }
              }, 400);
            }
          };

          rec.start();
          recognition = rec;
          recognitionRef.current = rec;
        } catch (err) {
          console.warn('Speech recognition start failed:', err);
        }
      };

      initRecognition();

      return () => {
        active = false;
        if (recognition) {
          try { recognition.stop(); } catch(_) {}
        }
      };
    } else {
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch(_) {}
        recognitionRef.current = null;
      }
    }
  }, [isVoiceListening, onVoiceCommand]);

  const cfg = currentStepData?.defectConfig || {
    defectName: 'Component Angular Misalignment',
    defectType: 'Geometric Tolerance Deviation',
    paramName: 'Seating Angle',
    nominal: 90.0,
    defectInitial: 71.7,
    tolerance: 1.0,
    unit: '°',
    minVal: 70.0,
    maxVal: 90.0,
    stepSize: 0.5,
    instruction: 'Align component to factory datum tolerance.'
  };

  const currentVal = typeof defectValue === 'number' ? defectValue : cfg.defectInitial;
  const deviation = Math.abs(currentVal - cfg.nominal);
  const isWithinTol = deviation <= cfg.tolerance;

  const handleStepChange = (delta) => {
    if (!onAdjustDefectValue) return;
    const nextVal = Math.max(cfg.minVal, Math.min(cfg.maxVal, +(currentVal + delta).toFixed(2)));
    onAdjustDefectValue(nextVal);
  };

  const handleAutoCalibrate = () => {
    if (!onAdjustDefectValue) return;
    onAdjustDefectValue(cfg.nominal);
  };

  // Derive Pick-to-Light Bin Code based on partKey/id
  const getBinCode = () => {
    const key = (currentStepData?.partKey || '').toLowerCase();
    if (key.includes('fork')) return { bin: 'BIN K-01', shelf: 'SHELF 01 • FORK CASTINGS' };
    if (key.includes('eye')) return { bin: 'BIN K-02', shelf: 'SHELF 01 • SINGLE EYE RODS' };
    if (key.includes('pin') && !key.includes('taper')) return { bin: 'BIN K-03', shelf: 'SHELF 02 • 30mm HARDENED PIVOT PINS' };
    if (key.includes('collar')) return { bin: 'BIN K-04', shelf: 'SHELF 02 • RETENTION COLLARS' };
    if (key.includes('taper')) return { bin: 'BIN K-05', shelf: 'SHELF 03 • 1:30 TAPER SPLIT PINS' };
    if (key.includes('hub')) return { bin: 'BIN B-01', shelf: 'SHELF 01 • FORGED WHEEL HUBS' };
    if (key.includes('rotor')) return { bin: 'BIN B-02', shelf: 'SHELF 01 • 320mm VENTED ROTORS' };
    if (key.includes('bracket')) return { bin: 'BIN B-03', shelf: 'SHELF 02 • ANCHOR BRACKETS' };
    if (key.includes('pad')) return { bin: 'BIN B-04', shelf: 'SHELF 02 • CERAMIC BRAKE PADS' };
    if (key.includes('caliper')) return { bin: 'BIN B-05', shelf: 'SHELF 03 • MONOBLOCK CALIPERS' };
    if (key.includes('flywheel')) return { bin: 'BIN C-01', shelf: 'SHELF 01 • DUCTILE FLYWHEELS' };
    if (key.includes('friction')) return { bin: 'BIN C-02', shelf: 'SHELF 01 • CLUTCH FRICTION DISCS' };
    if (key.includes('pressure')) return { bin: 'BIN C-03', shelf: 'SHELF 02 • PRESSURE PLATES' };
    if (key.includes('diaphragm')) return { bin: 'BIN C-04', shelf: 'SHELF 02 • BELLEVILLE SPRINGS' };
    if (key.includes('cover')) return { bin: 'BIN C-05', shelf: 'SHELF 03 • STAMPED COVERS' };
    return { bin: `BIN #${currentStepData?.id || 1}`, shelf: 'MAIN WORKBENCH STORAGE' };
  };

  const binInfo = getBinCode();

  return (
    <div className={`ar-hud-overlay ${isDefectSimulated ? 'defect-active' : ''} ${isProjectedARMode ? 'projected-ar-mode' : ''}`}>
      {/* 4 Corner Tech Brackets */}
      <div className="hud-corner top-left"></div>
      <div className="hud-corner top-right"></div>
      <div className="hud-corner bottom-left"></div>
      <div className="hud-corner bottom-right"></div>

      {/* Unified Industrial AR Top Master Bar - Sleek & Uncluttered Capsule */}
      <div className="hud-top-master-bar">
        <div className="hud-master-capsule">
          <span className="pwi-pulse-dot"></span>
          <span className="pwi-step-tag font-mono">
            STEP {String(currentStepData?.id || 1).padStart(2, '0')}/{String(totalSteps).padStart(2, '0')}
          </span>
          <span className="pwi-divider">•</span>
          <span className="pwi-part-name" title={currentStepData?.partName}>
            {currentStepData?.partName || 'Assembly Station'}
          </span>
          <div className="pwi-pick-pill" title={binInfo.shelf}>
            <span className="bin-code font-mono">{binInfo.bin}</span>
          </div>
          <div className="hud-capsule-divider"></div>
          <div className="hud-compact-telemetry">
            <span className="telemetry-badge font-mono">99.8% AR</span>
            <span className="telemetry-badge-fps font-mono">{telemetry.fps} FPS</span>
          </div>
        </div>
      </div>

      {/* Voice Recognition Badge Notification */}
      {lastVoiceCommand && (
        <div className="last-command-badge" style={{ position: 'absolute', top: '54px', right: '20px', zIndex: 30 }}>
          <span className="cmd-icon">🗣️</span>
          <span>RECOGNIZED: "<strong>{lastVoiceCommand.toUpperCase()}</strong>" ✓</span>
        </div>
      )}

      {/* Live Industry 4.0 Factory Telemetry & Atlas Copco Curve Card */}
      <div className={`hud-telemetry-panel ${isTelemetryExpanded ? 'expanded' : 'collapsed'}`}>
        <div className="telemetry-panel-header" onClick={() => setIsTelemetryExpanded(!isTelemetryExpanded)}>
          <div className="telemetry-hdr-left">
            <span className="telemetry-pulse-icon">⚡</span>
            <span className="telemetry-title font-mono">INDUSTRY 4.0 LIVE TELEMETRY</span>
            <span className="station-badge font-mono">
              {currentStepData?.telemetry?.stationCode || `STN-0${currentStepData?.id || 1}`}
            </span>
          </div>
          <button className="btn-toggle-telemetry" title={isTelemetryExpanded ? "Collapse Telemetry" : "Expand Telemetry"}>
            {isTelemetryExpanded ? '▲ HIDE' : '▼ LIVE METRICS'}
          </button>
        </div>

        {isTelemetryExpanded && (
          <div className="telemetry-panel-body">
            {/* Cell & Robot Identity */}
            <div className="telemetry-cell-row">
              <span className="cell-label font-mono">ROBOT & TOOL:</span>
              <span className="cell-val text-cyan">
                {currentStepData?.telemetry?.robotType || 'FANUC M-20iD'} • {currentStepData?.telemetry?.toolBrand || 'Atlas Copco Tensor DC'}
              </span>
            </div>

            {/* Dynamic Atlas Copco Torque-Angle SVG Curve */}
            <div className="telemetry-curve-box">
              <div className="curve-header">
                <span className="curve-lbl font-mono">ATLAS COPCO DC TORQUE-ANGLE CURVE</span>
                <span className="curve-status text-emerald font-mono">
                  {currentStepData?.requiresTorque ? `TARGET: ${currentStepData.targetTorque} Nm [PASS]` : 'SERVO LOAD: IN SPEC'}
                </span>
              </div>
              <svg className="torque-angle-svg" viewBox="0 0 240 64" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="torqueGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.8" />
                    <stop offset="70%" stopColor="#38bdf8" stopOpacity="0.9" />
                    <stop offset="100%" stopColor="#10b981" stopOpacity="1" />
                  </linearGradient>
                  <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.25" />
                    <stop offset="100%" stopColor="#00f0ff" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                {/* Horizontal reference grid lines */}
                <line x1="0" y1="16" x2="240" y2="16" stroke="rgba(255,255,255,0.08)" strokeDasharray="3,3" />
                <line x1="0" y1="36" x2="240" y2="36" stroke="rgba(255,255,255,0.08)" strokeDasharray="3,3" />
                <line x1="0" y1="56" x2="240" y2="56" stroke="rgba(255,255,255,0.15)" />
                {/* Dynamic Curve Path */}
                <path
                  d="M 10 56 Q 60 55, 95 44 T 175 22 Q 200 15, 225 15"
                  fill="none"
                  stroke="url(#torqueGrad)"
                  strokeWidth="2.5"
                  className="live-curve-stroke"
                />
                <path
                  d="M 10 56 Q 60 55, 95 44 T 175 22 Q 200 15, 225 15 L 225 56 Z"
                  fill="url(#areaGrad)"
                />
                {/* Snug point, yield point, target points */}
                <circle cx="95" cy="44" r="2.5" fill="#38bdf8" />
                <circle cx="175" cy="22" r="2.5" fill="#fbbf24" />
                <circle cx="225" cy="15" r="4" fill="#10b981" className="target-pulse-circle" />
                {/* Annotations */}
                <text x="12" y="62" fill="rgba(255,255,255,0.4)" fontSize="7" fontFamily="monospace">0°</text>
                <text x="90" y="52" fill="#38bdf8" fontSize="6.5" fontFamily="monospace">SNUG</text>
                <text x="160" y="32" fill="#fbbf24" fontSize="6.5" fontFamily="monospace">YIELD</text>
                <text x="195" y="10" fill="#10b981" fontSize="7" fontWeight="bold" fontFamily="monospace">OK [PASS]</text>
              </svg>
              <div className="curve-footer">
                <span className="curve-legend-item"><span className="legend-dot snug"></span> Snug Torque</span>
                <span className="curve-legend-item"><span className="legend-dot yield"></span> Angle Yield</span>
                <span className="curve-legend-item"><span className="legend-dot target"></span> Target Lock</span>
              </div>
            </div>

            {/* Live Sensor Metrics Grid */}
            <div className="telemetry-metrics-row">
              <div className="telemetry-stat">
                <span className="stat-label">KEYENCE LASER:</span>
                <span className="stat-value font-mono text-cyan">
                  {currentStepData?.telemetry?.laserRunout || '< 0.015 mm [PASS]'}
                </span>
              </div>
              <div className="telemetry-stat">
                <span className="stat-label">TAKT TIME:</span>
                <span className="stat-value font-mono text-amber">
                  {currentStepData?.telemetry?.cycleTime || '30s Takt'}
                </span>
              </div>
              {currentStepData?.telemetry?.heliumDecay && currentStepData.telemetry.heliumDecay !== 'N/A' && (
                <div className="telemetry-stat full-width">
                  <span className="stat-label">HELIUM DECAY:</span>
                  <span className="stat-value font-mono text-emerald">
                    {currentStepData.telemetry.heliumDecay}
                  </span>
                </div>
              )}
            </div>

            {/* Poka-Yoke Machine Vision Status */}
            <div className="poka-yoke-status-bar">
              <span className="poka-dot"></span>
              <span className="poka-txt font-mono">POKA-YOKE OPTICAL INTERLOCK: ARMED & VERIFIED</span>
            </div>
          </div>
        )}
      </div>

      {/* Subtle Computer Vision AI Optical Alignment Reticle */}
      <div className="hud-center-reticle">
        <div className="reticle-ring outer-ring"></div>
        <div className="reticle-ring inner-ring"></div>
        <div className="crosshair-h"></div>
        <div className="crosshair-v"></div>
        <div className="reticle-center-dot"></div>

        {/* Dynamic Computer Vision Laser Scan Line */}
        <div className="cv-laser-scan-line"></div>

        {/* Machine Vision Bounding Box corners */}
        <div className="cv-bbox-corner cv-tl"></div>
        <div className="cv-bbox-corner cv-tr"></div>
        <div className="cv-bbox-corner cv-bl"></div>
        <div className="cv-bbox-corner cv-br"></div>
      </div>

      {/* Real-Time Interactive AR Laser CMM Metrology & Realignment Console */}
      {isDefectSimulated && (
        <div className="cmm-defect-console">
          <div className={`cmm-console-card ${isWithinTol ? 'status-pass' : 'status-alert'}`}>
            {/* Header */}
            <div className="cmm-header-row">
              <div className="cmm-title-wrap">
                <span className={`cmm-indicator-light ${isWithinTol ? 'green-pulse' : 'red-strobe'}`}></span>
                <div>
                  <h4>{isWithinTol ? 'LASER CMM: TOLERANCE ATTAINED' : 'CRITICAL QUALITY DEFECT DETECTED'}</h4>
                  <p className="cmm-sub-type">{cfg.defectType} • {currentStepData?.partName}</p>
                </div>
              </div>
              <span className={`cmm-status-pill ${isWithinTol ? 'pill-pass' : 'pill-halt'}`}>
                {isWithinTol ? '✓ TOLERANCE VERIFIED' : '⛔ ASSEMBLY LINE HALTED'}
              </span>
            </div>

            {/* Metrology Gauge Comparison */}
            <div className="cmm-metrics-grid">
              <div className="metric-box current-val">
                <span className="metric-lbl">MEASURED {cfg.paramName.toUpperCase()}</span>
                <span className="metric-num font-mono">
                  {currentVal.toFixed(cfg.unit === 'mm' ? 2 : 1)} <small>{cfg.unit}</small>
                </span>
                <span className={`metric-dev ${isWithinTol ? 'text-emerald' : 'text-rose'}`}>
                  Δ = {(currentVal - cfg.nominal).toFixed(2)} {cfg.unit}
                </span>
              </div>

              <div className="metric-box nominal-val">
                <span className="metric-lbl">TARGET FACTORY SPEC</span>
                <span className="metric-num font-mono text-cyan">
                  {cfg.nominal.toFixed(cfg.unit === 'mm' ? 2 : 1)} <small>{cfg.unit}</small>
                </span>
                <span className="metric-dev text-muted">
                  TOLERANCE: ±{cfg.tolerance} {cfg.unit}
                </span>
              </div>

              <div className="metric-box protocol-val">
                <span className="metric-lbl">INSPECTION PROTOCOL</span>
                <span className="protocol-badge">DIN ISO 2768-mK</span>
                <span className="standard-sub">Laser Interferometry</span>
              </div>
            </div>

            {/* Interactive Realignment Tool (Operator Direct Control) */}
            <div className="cmm-alignment-tool">
              <div className="tool-hdr">
                <span>🎯 OPERATOR REAL-TIME REALIGNMENT DIAL (DRAG TO ROTATE 3D MESH):</span>
                <span className="target-aim-hint">
                  Target: <strong>{cfg.nominal}{cfg.unit}</strong> (Zone: {(cfg.nominal - cfg.tolerance).toFixed(1)} to {(cfg.nominal + cfg.tolerance).toFixed(1)}{cfg.unit})
                </span>
              </div>

              <div className="slider-control-row">
                <span className="range-min">{cfg.minVal}{cfg.unit}</span>
                <input
                  type="range"
                  className="cmm-range-slider"
                  min={cfg.minVal}
                  max={cfg.maxVal}
                  step={cfg.stepSize}
                  value={currentVal}
                  onChange={(e) => onAdjustDefectValue && onAdjustDefectValue(parseFloat(e.target.value))}
                />
                <span className="range-max">{cfg.maxVal}{cfg.unit}</span>
              </div>

              {/* Stepper Buttons & Auto-Calibrate */}
              <div className="cmm-steppers-row">
                <button className="btn-step" onClick={() => handleStepChange(-5)}>
                  ◄ -5{cfg.unit}
                </button>
                <button className="btn-step" onClick={() => handleStepChange(-0.5)}>
                  ◄ -0.5{cfg.unit}
                </button>
                <button className="btn-step" onClick={() => handleStepChange(+0.5)}>
                  +0.5{cfg.unit} ►
                </button>
                <button className="btn-step" onClick={() => handleStepChange(+5)}>
                  +5{cfg.unit} ►
                </button>
                <button className="btn-auto-calib" onClick={handleAutoCalibrate}>
                  ⚡ Auto-Calibrate to Datum ({cfg.nominal}{cfg.unit})
                </button>
              </div>
            </div>

            {/* Instruction & Resolution Row */}
            <div className="cmm-footer-action-row">
              <div className="cmm-instruction-note">
                <span className="info-icon">💡</span>
                <span>{cfg.instruction}</span>
              </div>

              <button
                className={`btn-lock-cmm ${isWithinTol ? 'btn-enabled' : 'btn-disabled'}`}
                disabled={!isWithinTol}
                onClick={onResolveDefect}
              >
                {isWithinTol ? '✓ LOCK TOLERANCE & CLEAR ERROR' : `⚠️ REALIGN WITHIN ±${cfg.tolerance}${cfg.unit} TO UNLOCK`}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Bottom AR Alignment Guidance */}
      <div className="hud-bottom-guide">
        <div className="hud-guide-pill">
          <span className="guide-icon">🎯</span>
          <span>KEEP CAMERA CENTERED ON WORKBENCH FIXTURE • LIGHT GUIDE ILLUMINATION: OPTIMAL (340 LUX)</span>
        </div>
      </div>
    </div>
  );
}

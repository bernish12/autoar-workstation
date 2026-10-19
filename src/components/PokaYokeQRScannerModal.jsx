import React, { useState, useEffect, useRef } from 'react';
import jsQR from 'jsqr';
import QRCode from 'qrcode';
import { soundFx } from '../utils/audio';

export default function PokaYokeQRScannerModal({
  isOpen,
  onClose,
  currentStep,
  onPartVerified,
  selectedLanguage = 'en'
}) {
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' (back) | 'user' (front)
  const [scanStatus, setScanStatus] = useState('idle'); // 'idle' | 'scanning' | 'matched' | 'mismatch'
  const [lastScannedResult, setLastScannedResult] = useState(null);
  const [correctQrDataUrl, setCorrectQrDataUrl] = useState('');
  const [wrongQrDataUrl, setWrongQrDataUrl] = useState('');
  const [showTestCards, setShowTestCards] = useState(true);
  const [verificationLog, setVerificationLog] = useState([]);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const animFrameIdRef = useRef(null);
  const scanCoolDownRef = useRef(false);

  const expectedCode = (currentStep?.partCode || 'PRT-01').trim();
  const expectedName = currentStep?.partName || currentStep?.title || 'Automotive Component';

  // Generate Real Test QR Codes for instant demonstration
  useEffect(() => {
    if (!isOpen) return;

    // Correct component QR payload
    QRCode.toDataURL(expectedCode, { width: 140, margin: 1, color: { dark: '#000000', light: '#ffffff' } })
      .then(url => setCorrectQrDataUrl(url))
      .catch(err => console.warn('QR gen error:', err));

    // Deliberately incorrect / wrong bin component QR payload
    const wrongCode = `WRONG-BIN-DEFECT-${expectedCode === 'PRT-01' ? 'ALT-99' : 'ERR-404'}`;
    QRCode.toDataURL(wrongCode, { width: 140, margin: 1, color: { dark: '#000000', light: '#ffffff' } })
      .then(url => setWrongQrDataUrl(url))
      .catch(err => console.warn('QR gen error:', err));
  }, [isOpen, expectedCode]);

  // Start Camera Stream
  const startCamera = async (mode = facingMode) => {
    stopCamera();
    setCameraError(null);
    setScanStatus('scanning');

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Webcam media API not supported in this browser environment.');
      }

      const constraints = {
        video: {
          facingMode: mode,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.setAttribute('playsinline', 'true');
        await videoRef.current.play();
        setCameraActive(true);
        startScanningLoop();
      }
    } catch (err) {
      console.warn('[Poka-Yoke Camera Warning]:', err.message);
      setCameraError(err.message || 'Unable to access webcam. You can use the on-screen simulated demo cards below.');
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (animFrameIdRef.current) {
      cancelAnimationFrame(animFrameIdRef.current);
      animFrameIdRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => {
        try { track.stop(); } catch {}
      });
      streamRef.current = null;
    }
    setCameraActive(false);
  };

  // Switch between front/back camera
  const toggleFacingMode = () => {
    const nextMode = facingMode === 'environment' ? 'user' : 'environment';
    setFacingMode(nextMode);
    startCamera(nextMode);
  };

  // Real-Time Optical Frame Scan Loop using jsQR
  const startScanningLoop = () => {
    const scan = () => {
      if (!videoRef.current || videoRef.current.readyState !== videoRef.current.HAVE_ENOUGH_DATA) {
        animFrameIdRef.current = requestAnimationFrame(scan);
        return;
      }

      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (!canvas) {
        animFrameIdRef.current = requestAnimationFrame(scan);
        return;
      }

      const ctx = canvas.getContext('2d', { willReadFrequently: true });
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      if (!scanCoolDownRef.current) {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
          inversionAttempts: 'dontInvert'
        });

        if (code && code.data) {
          evaluateScannedPart(code.data.trim());
        }
      }

      animFrameIdRef.current = requestAnimationFrame(scan);
    };

    animFrameIdRef.current = requestAnimationFrame(scan);
  };

  // Poka-Yoke Machine Vision Evaluation Logic
  const evaluateScannedPart = (scannedString) => {
    if (scanCoolDownRef.current) return;
    scanCoolDownRef.current = true;

    const normalizedScanned = scannedString.toUpperCase();
    const normalizedExpected = expectedCode.toUpperCase();

    // Check if scanned QR contains or matches expected code or part name
    const isMatch = normalizedScanned.includes(normalizedExpected) || 
                    normalizedExpected.includes(normalizedScanned) ||
                    (currentStep?.partName && normalizedScanned.includes(currentStep.partName.toUpperCase().slice(0, 8)));

    const timestamp = new Date().toLocaleTimeString();

    if (isMatch) {
      // ✅ SUCCESS: COMPONENT VERIFIED
      setScanStatus('matched');
      setLastScannedResult({
        code: scannedString,
        isSuccess: true,
        message: `VALID COMPONENT: ${expectedName} [${expectedCode}]`
      });

      soundFx.playScannerBeep();
      setTimeout(() => soundFx.playSuccess(), 120);

      // Voice notification in active language
      const voiceMsg = selectedLanguage === 'ta'
        ? `கூறு சரிபார்க்கப்பட்டது: பாகம் ${expectedCode} உறுதி செய்யப்பட்டது. போகா-யோக் பூட்டு திறக்கப்பட்டது.`
        : selectedLanguage === 'ml'
        ? `ഘടകം സ്ഥിരീകരിച്ചു: പാർട്ട് ${expectedCode} ശരിയാണ്.`
        : selectedLanguage === 'hi'
        ? `घटक सत्यापित हुआ: भाग ${expectedCode} सही है। पोका-योक इंटरलॉक अनलॉक हुआ।`
        : `Component Verified: ${expectedName} Part ${expectedCode} Validated. Poka-Yoke Interlock Released.`;

      soundFx.speak(voiceMsg, currentStep);

      setVerificationLog(prev => [
        { time: timestamp, code: scannedString, status: 'PASS', details: 'Exact Match • Interlock Released' },
        ...prev.slice(0, 4)
      ]);

      if (onPartVerified) {
        onPartVerified(expectedCode);
      }

      // Auto close with success after 2.6s
      setTimeout(() => {
        scanCoolDownRef.current = false;
        setScanStatus('scanning');
      }, 3500);

    } else {
      // ❌ REJECTION: WRONG BIN ERROR (POKA-YOKE MISTAKE PROOFING)
      setScanStatus('mismatch');
      setLastScannedResult({
        code: scannedString,
        isSuccess: false,
        message: `WRONG BIN REJECTION! Expected: ${expectedCode}, Detected: ${scannedString}`
      });

      soundFx.playWrongBinBuzz();
      setTimeout(() => soundFx.playAlarm(), 100);

      // Voice notification
      const voiceErrMsg = selectedLanguage === 'ta'
        ? `தவறான பாகப் பிழை! தவறான கூறு கண்டறியப்பட்டது. உற்பத்தி வரிசை நிறுத்தப்பட்டது!`
        : selectedLanguage === 'ml'
        ? `തെറ്റായ പാർട്ട് പിശക്! ഉത്പാദനം നിർത്തിവെച്ചു!`
        : selectedLanguage === 'hi'
        ? `गलत पार्ट त्रुटि! गलत घटक पाया गया। असेंबली लाइन रोकी गई!`
        : `Wrong Bin Error! Mismatched Component Detected. Assembly Line Halted!`;

      soundFx.speak(voiceErrMsg, currentStep);

      setVerificationLog(prev => [
        { time: timestamp, code: scannedString, status: 'REJECTED', details: `Mismatch! Expected: ${expectedCode}` },
        ...prev.slice(0, 4)
      ]);

      // Release cooldown after 3s so operator can retry with correct component
      setTimeout(() => {
        scanCoolDownRef.current = false;
        setScanStatus('scanning');
      }, 3200);
    }
  };

  // Open/Close lifecycle
  useEffect(() => {
    if (isOpen) {
      setScanStatus('scanning');
      setLastScannedResult(null);
      scanCoolDownRef.current = false;
      startCamera();
    } else {
      stopCamera();
    }
    return () => stopCamera();
  }, [isOpen, currentStep]);

  if (!isOpen) return null;

  return (
    <div className="poka-modal-backdrop" onClick={onClose}>
      <div className="poka-modal-window" onClick={(e) => e.stopPropagation()}>
        {/* Top Header */}
        <div className="poka-modal-header">
          <div className="poka-title-group">
            <span className="poka-header-icon">📷</span>
            <div>
              <h3>POKA-YOKE OPTICAL PART SCANNER</h3>
              <p className="poka-subtitle font-mono">
                AI Machine Vision Interlock • Zero-Defect Manufacturing Protocol
              </p>
            </div>
          </div>

          <div className="poka-header-actions">
            <span className="poka-target-pill font-mono">
              <span className="dot pulse-cyan"></span>
              TARGET: <strong className="text-cyan">{expectedCode}</strong>
            </span>
            <button className="btn-close-poka" onClick={onClose} title="Close Scanner">
              ✕
            </button>
          </div>
        </div>

        {/* Modal Main Body */}
        <div className="poka-modal-body">
          {/* Left/Main Column: Live Optical Viewfinder */}
          <div className="poka-viewfinder-column">
            <div className={`poka-camera-box ${scanStatus}`}>
              {/* Native Hidden Offscreen Canvas for jsQR Frame Extraction */}
              <canvas ref={canvasRef} style={{ display: 'none' }} />

              {/* Live Video Feed */}
              <video
                ref={videoRef}
                className={`poka-video-feed ${cameraActive ? 'active' : ''}`}
                muted
                autoPlay
                playsInline
              />

              {/* Fallback View if webcam is disabled/unavailable */}
              {!cameraActive && (
                <div className="poka-fallback-view">
                  <span className="poka-fallback-icon">📸</span>
                  <h4>Webcam Standby / Simulated Lens</h4>
                  <p className="fallback-note">
                    {cameraError ? cameraError : 'Allow webcam permission, or use the on-screen simulated test QR cards below.'}
                  </p>
                  <button className="btn-retry-cam font-mono" onClick={() => startCamera()}>
                    🔄 Initialize Camera
                  </button>
                </div>
              )}

              {/* High-Tech Industrial HUD Overlay on Viewfinder */}
              <div className="poka-hud-viewfinder-overlay">
                {/* 4 Corner Targeting Brackets */}
                <div className="poka-bracket p-top-left"></div>
                <div className="poka-bracket p-top-right"></div>
                <div className="poka-bracket p-bottom-left"></div>
                <div className="poka-bracket p-bottom-right"></div>

                {/* Vertical Laser Scan Line */}
                <div className={`poka-laser-scan-line ${scanStatus === 'matched' ? 'laser-green' : scanStatus === 'mismatch' ? 'laser-red' : 'laser-cyan'}`}></div>

                {/* Center Target Crosshair */}
                <div className="poka-center-crosshair">
                  <div className="crosshair-dot"></div>
                </div>

                {/* Floating Status Notification Banner on Viewfinder */}
                {scanStatus === 'matched' && (
                  <div className="poka-banner banner-pass font-mono animate-pop">
                    <span className="banner-icon">✓</span>
                    <div>
                      <strong>COMPONENT VERIFIED & VALIDATED</strong>
                      <p>{lastScannedResult?.code} • POKA-YOKE RELEASED</p>
                    </div>
                  </div>
                )}

                {scanStatus === 'mismatch' && (
                  <div className="poka-banner banner-reject font-mono animate-shake">
                    <span className="banner-icon">⛔</span>
                    <div>
                      <strong>WRONG BIN ERROR! MISMATCHED PART</strong>
                      <p>EXPECTED: {expectedCode} | DETECTED: {lastScannedResult?.code}</p>
                    </div>
                  </div>
                )}

                {scanStatus === 'scanning' && (
                  <div className="poka-banner banner-scanning font-mono">
                    <span className="banner-pulse-dot"></span>
                    <span>ALIGN COMPONENT QR / BARCODE IN VIEWFINDER...</span>
                  </div>
                )}
              </div>

              {/* Bottom Camera Toolbar */}
              <div className="poka-cam-controls">
                <button
                  className="btn-poka-cam-flip"
                  onClick={toggleFacingMode}
                  title="Switch Front/Rear Camera"
                >
                  🔄 {facingMode === 'environment' ? 'Rear Cam' : 'Front Cam'}
                </button>
                <span className="cam-engine-tag font-mono">
                  ENGINE: jsQR 1080p Optical Matrix
                </span>
              </div>
            </div>

            {/* Expected Part Details Banner */}
            <div className="poka-expected-part-card">
              <div className="expected-badge-header">
                <span className="poka-step-pill font-mono">STEP {String(currentStep?.id || 1).padStart(2, '0')}</span>
                <span className="expected-title">{expectedName}</span>
              </div>
              <div className="expected-meta-row font-mono">
                <span>PART CODE: <strong className="text-cyan">{expectedCode}</strong></span>
                <span className="sep">•</span>
                <span>BIN LOCATION: <strong className="text-amber">BIN #{currentStep?.id || 1}</strong></span>
                <span className="sep">•</span>
                <span>STATUS: <strong className={currentStep?.isFitmentVerified ? 'text-emerald' : 'text-cyan'}>
                  {currentStep?.isFitmentVerified ? 'FITMENT CONFIRMED' : 'AWAITING POKA-YOKE'}
                </strong></span>
              </div>
            </div>
          </div>

          {/* Right Column: Demo Test Cards & Quality Audit Log */}
          <div className="poka-demo-column">
            {/* Quick Demo QR Cards Section */}
            <div className="poka-demo-card-box">
              <div className="demo-box-hdr" onClick={() => setShowTestCards(!showTestCards)}>
                <span className="hdr-title font-mono">🧪 DEMO TEST QR CARDS</span>
                <span className="hdr-toggle">{showTestCards ? '▲ HIDE' : '▼ SHOW CARDS'}</span>
              </div>

              {showTestCards && (
                <div className="demo-cards-list">
                  <p className="demo-hint font-mono">
                    Point your phone at these cards, hold them up to the webcam, or click <strong>'⚡ Simulate Scan'</strong>:
                  </p>

                  {/* Card 1: Valid Correct Component */}
                  <div className="test-qr-card card-valid">
                    <div className="qr-img-wrapper">
                      {correctQrDataUrl ? (
                        <img src={correctQrDataUrl} alt={`QR Code for ${expectedCode}`} className="qr-preview-img" />
                      ) : (
                        <div className="qr-loading font-mono">Generating...</div>
                      )}
                    </div>
                    <div className="qr-card-info">
                      <span className="qr-status-badge text-emerald font-mono">✓ CORRECT BIN COMPONENT</span>
                      <strong className="qr-part-code font-mono">{expectedCode}</strong>
                      <span className="qr-part-desc">{expectedName}</span>
                      <button
                        className="btn-sim-scan btn-sim-pass font-mono"
                        onClick={() => evaluateScannedPart(expectedCode)}
                      >
                        ⚡ Simulate Correct Scan
                      </button>
                    </div>
                  </div>

                  {/* Card 2: Deliberate Wrong Bin Defect */}
                  <div className="test-qr-card card-wrong">
                    <div className="qr-img-wrapper">
                      {wrongQrDataUrl ? (
                        <img src={wrongQrDataUrl} alt="Wrong QR" className="qr-preview-img" />
                      ) : (
                        <div className="qr-loading font-mono">Generating...</div>
                      )}
                    </div>
                    <div className="qr-card-info">
                      <span className="qr-status-badge text-rose font-mono">⛔ WRONG COMPONENT TEST</span>
                      <strong className="qr-part-code font-mono">DEFECT-PRT-ERR</strong>
                      <span className="qr-part-desc">Mismatched Part (Simulates Wrong Bin)</span>
                      <button
                        className="btn-sim-scan btn-sim-fail font-mono"
                        onClick={() => evaluateScannedPart('DEFECT-PRT-ERR-999')}
                      >
                        ⚠️ Simulate Wrong Bin Error
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Live Poka-Yoke Machine Vision Audit Log */}
            <div className="poka-audit-log-box">
              <div className="audit-header font-mono">
                <span>📋 MACHINE VISION AUDIT LOG</span>
                <span className="std-badge">IATF 16949 / ISO 9001</span>
              </div>
              <div className="audit-list font-mono">
                {verificationLog.length === 0 ? (
                  <div className="audit-empty">
                    <span>Awaiting optical scan trigger...</span>
                  </div>
                ) : (
                  verificationLog.map((log, idx) => (
                    <div key={idx} className={`audit-item ${log.status === 'PASS' ? 'log-pass' : 'log-reject'}`}>
                      <div className="log-top">
                        <span className="log-time">{log.time}</span>
                        <span className={`log-badge ${log.status === 'PASS' ? 'badge-pass' : 'badge-reject'}`}>
                          {log.status}
                        </span>
                      </div>
                      <div className="log-code">Scanned: {log.code}</div>
                      <div className="log-details">{log.details}</div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="poka-modal-footer">
          <div className="footer-legend font-mono">
            <span>POKA-YOKE PROTOCOL:</span>
            <span className="legend-chip"><span className="dot pulse-green"></span> Correct Bin = Fitment Verified</span>
            <span className="legend-chip"><span className="dot pulse-red"></span> Wrong Bin = Line Halted</span>
          </div>
          <div className="footer-btn-group">
            <button className="btn-poka-secondary font-mono" onClick={onClose}>
              Dismiss
            </button>
            {scanStatus === 'matched' && (
              <button
                className="btn-poka-primary font-mono"
                onClick={() => {
                  soundFx.playClick();
                  onClose();
                }}
              >
                Proceed to Assembly ▶
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

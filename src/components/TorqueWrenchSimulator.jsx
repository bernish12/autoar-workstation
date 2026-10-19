import React, { useState, useEffect } from 'react';
import { soundFx } from '../utils/audio';

export default function TorqueWrenchSimulator({
  stepData,
  currentTorque,
  setCurrentTorque,
  isTorqueVerified,
  setIsTorqueVerified
}) {
  const target = stepData?.targetTorque || 50;
  const isNeeded = stepData?.requiresTorque || false;
  const [isPressing, setIsPressing] = useState(false);

  // Handle continuous press or click tightening (Always call hook unconditionally)
  useEffect(() => {
    if (!isNeeded) return;
    let timer = null;
    if (isPressing && currentTorque < target) {
      timer = setInterval(() => {
        setCurrentTorque(prev => {
          const increment = Math.max(1, Math.round(target / 18));
          const nextVal = Math.min(target, prev + increment);
          soundFx.playTorqueClick(nextVal / target);
          if (nextVal >= target) {
            setIsTorqueVerified(true);
            soundFx.playSuccess();
            setIsPressing(false);
          }
          return nextVal;
        });
      }, 75);
    }
    return () => clearInterval(timer);
  }, [isPressing, currentTorque, target, setCurrentTorque, setIsTorqueVerified, isNeeded]);

  // If this step doesn't require torque fastening (e.g. visual inspection or pad clip fitment)
  if (!isNeeded) {
    return (
      <div className={`torque-box no-torque ${isTorqueVerified ? 'torque-verified' : ''}`}>
        <div className="torque-header">
          <div className="tool-badge">
            <span className="icon">🛠️</span>
            <span>FASTENER PROTOCOL</span>
          </div>
          <span className={`status-pill ${isTorqueVerified ? 'pill-pass' : 'pill-wait'}`}>
            {isTorqueVerified ? '✓ FITMENT CONFIRMED' : 'AWAITING SEATING'}
          </span>
        </div>
        
        <div className="manual-fitment-body">
          <p className="manual-protocol-desc">Non-threaded precision fitment • Manual alignment & seating</p>
          
          <button
            className={`btn-seat-action ${isTorqueVerified ? 'seated-done' : 'seat-ready'}`}
            onClick={() => {
              setIsTorqueVerified(true);
              soundFx.playSuccess();
            }}
          >
            <span className="icon">{isTorqueVerified ? '✓' : '⚡'}</span>
            <span>{isTorqueVerified ? 'Step Tolerance & Fitment Verified' : 'Simulate Component Fitment & Seating'}</span>
          </button>
        </div>
      </div>
    );
  }

  const handleAutoTorque = () => {
    let val = currentTorque;
    const interval = setInterval(() => {
      val += Math.max(2, Math.round(target / 12));
      if (val >= target) {
        val = target;
        clearInterval(interval);
        setCurrentTorque(target);
        setIsTorqueVerified(true);
        soundFx.playSuccess();
      } else {
        setCurrentTorque(val);
        soundFx.playTorqueClick(val / target);
      }
    }, 60);
  };

  const handleResetTorque = () => {
    setCurrentTorque(0);
    setIsTorqueVerified(false);
    soundFx.playClick();
  };

  // Percentage for circular gauge
  const progressPercent = Math.min(100, Math.round((currentTorque / target) * 100));
  const strokeDashoffset = 251.2 - (251.2 * progressPercent) / 100;

  return (
    <div className={`torque-box ${isTorqueVerified ? 'torque-verified' : ''}`}>
      <div className="torque-header">
        <div className="tool-badge">
          <span className="icon">🔧</span>
          <span>SMART IOT TORQUE WRENCH</span>
        </div>
        <span className={`status-pill ${isTorqueVerified ? 'pill-pass' : 'pill-wait'}`}>
          {isTorqueVerified ? '✓ TORQUE LOCKED' : 'AWAITING FASTENING'}
        </span>
      </div>

      <div className="torque-display-row">
        {/* Radial SVG Gauge */}
        <div className="radial-gauge-wrap">
          <svg className="radial-gauge" viewBox="0 0 100 100">
            {/* Background circle track */}
            <circle
              className="gauge-track"
              cx="50"
              cy="50"
              r="40"
              fill="transparent"
              stroke="#1e293b"
              strokeWidth="9"
            />
            {/* Active progress stroke */}
            <circle
              className="gauge-progress"
              cx="50"
              cy="50"
              r="40"
              fill="transparent"
              stroke={isTorqueVerified ? '#10b981' : progressPercent > 70 ? '#f59e0b' : '#00f0ff'}
              strokeWidth="9"
              strokeDasharray="251.2"
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
          <div className="gauge-center-text">
            <span className="gauge-value">{currentTorque}</span>
            <span className="gauge-unit">Nm</span>
          </div>
        </div>

        {/* Target Specs & Status */}
        <div className="torque-meta-col">
          <div className="torque-target-row">
            <span className="lbl">Target Spec:</span>
            <span className="val text-gold">{target} Nm (±1.5 Nm)</span>
          </div>
          <div className="torque-target-row">
            <span className="lbl">Fastener Grade:</span>
            <span className="val">ISO 898-1 Class 10.9</span>
          </div>
          <div className="torque-target-row">
            <span className="lbl">Tool ID:</span>
            <span className="val font-mono">ATLAS-COPCO-W09</span>
          </div>

          <div className="torque-actions-grid">
            <button
              className={`btn-torque-press ${isPressing ? 'active' : ''}`}
              onMouseDown={() => setIsPressing(true)}
              onMouseUp={() => setIsPressing(false)}
              onTouchStart={() => setIsPressing(true)}
              onTouchEnd={() => setIsPressing(false)}
              disabled={isTorqueVerified}
            >
              🔩 {isTorqueVerified ? 'Tightened (Pass)' : 'Hold / Press to Torque'}
            </button>
            <button
              className="btn-auto-torque"
              onClick={handleAutoTorque}
              disabled={isTorqueVerified}
            >
              ⚡ Auto Fasten
            </button>
            {isTorqueVerified && (
              <button className="btn-reset-torque" onClick={handleResetTorque}>
                ↺ Reset
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

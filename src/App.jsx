import React, { useState, useEffect, useRef } from 'react';
import { ASSEMBLY_STEPS, CLUTCH_ASSEMBLY_STEPS, FULL_CAR_ASSEMBLY_STEPS, KNUCKLE_JOINT_STEPS, COMPONENT_MODULES } from './components/assemblyData';
import AssemblyViewer3D from './components/AssemblyViewer3D';
import AROverlayHUD from './components/AROverlayHUD';
import TorqueWrenchSimulator from './components/TorqueWrenchSimulator';
import SupervisorAnalyticsModal from './components/SupervisorAnalyticsModal';
import IndustrialARGuideModal from './components/IndustrialARGuideModal';
import PokaYokeQRScannerModal from './components/PokaYokeQRScannerModal';
import CADFileUploader, { applyPBRMaterials } from './components/CADFileUploader';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import { soundFx } from './utils/audio';
import { analyzeCADAssembly } from './utils/cadAssemblyAnalyzer';
import './App.css';

export default function App() {
  const [selectedModule, setSelectedModule] = useState(null); // 'brake' | 'clutch' | 'car' | 'knuckle' | 'custom'
  const [activeTab, setActiveTab] = useState('assembly'); // 'assembly' | 'upload'
  const [customCADParams, setCustomCADParams] = useState(null);
  const [customModel, setCustomModel] = useState(null);
  const [customModelName, setCustomModelName] = useState('');
  const [dynamicSteps, setDynamicSteps] = useState(null);
  const [cadStats, setCadStats] = useState(null);
  const [assemblyTitle, setAssemblyTitle] = useState('');
  const [isVaultMenuOpen, setIsVaultMenuOpen] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [explodedPercent, setExplodedPercent] = useState(0);
  const [isDefectSimulated, setIsDefectSimulated] = useState(false);
  const [defectValue, setDefectValue] = useState(null);
  const [defectsResolvedCount, setDefectsResolvedCount] = useState(0);
  const [isXRayMode, setIsXRayMode] = useState(false);
  const [isAutoRotate, setIsAutoRotate] = useState(false);
  const [isARMode, setIsARMode] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isProjectedARMode, setIsProjectedARMode] = useState(true);
  const [isVoiceListening, setIsVoiceListening] = useState(true);
  const [lastVoiceCommand, setLastVoiceCommand] = useState('');
  const [isARGuideModalOpen, setIsARGuideModalOpen] = useState(false);
  const [isQRScannerOpen, setIsQRScannerOpen] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [speechEnabled, setSpeechEnabled] = useState(true);
  const [currentTorque, setCurrentTorque] = useState(0);
  const [isTorqueVerified, setIsTorqueVerified] = useState(false);
  const [cycleTimeSeconds, setCycleTimeSeconds] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(true);
  const [isQCModalOpen, setIsQCModalOpen] = useState(false);
  const [isAutoPlaying, setIsAutoPlaying] = useState(false);
  const [showAllParts, setShowAllParts] = useState(false);
  const [isStageCardDismissed, setIsStageCardDismissed] = useState(false);
  const [cameraFacingMode, setCameraFacingMode] = useState('environment'); // 'environment' (rear) | 'user' (selfie)
  const [selectedVoiceLanguage, setSelectedVoiceLanguage] = useState('en'); // 'en' | 'ta' | 'ml' | 'hi'
  const [isVoiceSpeaking, setIsVoiceSpeaking] = useState(false);
  const [speakingText, setSpeakingText] = useState('');
  const [isZenMode, setIsZenMode] = useState(false);

  const videoRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const mainFileInputRef = useRef(null);

  // Auto-detect module from customModelName to guarantee 100% accurate steps
  const detectModule = (name) => {
    if (!name) return selectedModule;
    const lower = name.toLowerCase();
    if (lower.includes('car') || lower.includes('vehicle') || lower.includes('bmw')) return 'car';
    if (lower.includes('clutch')) return 'clutch';
    if (lower.includes('knuckle') || lower.includes('joint')) return 'knuckle';
    if (lower.includes('brake') || lower.includes('rotor') || lower.includes('caliper')) return 'brake';
    return selectedModule;
  };

  const effectiveModule = customModelName ? detectModule(customModelName) : selectedModule;

  useEffect(() => {
    if (customModelName) {
      const detected = detectModule(customModelName);
      if (detected !== selectedModule) {
        setSelectedModule(detected);
      }
    }
  }, [customModelName]);

  const stepsList = dynamicSteps || (
    customModel ? (
      effectiveModule === 'car'
        ? FULL_CAR_ASSEMBLY_STEPS
        : (effectiveModule === 'clutch'
          ? CLUTCH_ASSEMBLY_STEPS
          : (effectiveModule === 'knuckle' ? KNUCKLE_JOINT_STEPS : ASSEMBLY_STEPS))
    ) : []
  );
  const currentStep = stepsList[currentStepIndex] || stepsList[0] || null;

  // Dynamic Metrology Defect Configuration & Live Angle Offset for 3D Mesh
  const currentDefectCfg = currentStep?.defectConfig || {
    nominal: 90.0,
    defectInitial: 71.7,
    tolerance: 1.0,
    defectName: 'Component Misalignment'
  };
  const liveDefectVal = typeof defectValue === 'number' ? defectValue : currentDefectCfg.nominal;
  const defectAngleOffset = isDefectSimulated ? (liveDefectVal - currentDefectCfg.nominal) : 0;

  // Unified CAD Model Ingestion & Analysis
  const processLoadedCAD = (model, fileName) => {
    applyPBRMaterials(model);

    const analysis = analyzeCADAssembly(model, fileName);
    setDynamicSteps(analysis.steps);
    setCadStats({
      meshesCount: analysis.meshesCount,
      totalVertices: analysis.totalVertices
    });
    setAssemblyTitle(analysis.assemblyTitle);
    setSelectedModule(analysis.module);

    setCustomModel(model);
    setCustomModelName(fileName);
    setCurrentStepIndex(0);
    setCompletedSteps([]);
    setActiveTab('assembly');
    setIsStageCardDismissed(true);
    soundFx.playSuccess();
  };

  // Process raw File object from Windows File Explorer or Drag & Drop
  const handleFileProcess = (file) => {
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['obj', 'glb', 'gltf', 'stl'].includes(ext)) {
      alert('Please select a 3D CAD Assembly file (.OBJ, .GLB, .GLTF, or .STL).');
      return;
    }

    soundFx.playClick();
    const reader = new FileReader();

    if (ext === 'obj') {
      reader.readAsText(file);
      reader.onload = (ev) => {
        try {
          const loader = new OBJLoader();
          const obj = loader.parse(ev.target.result);
          processLoadedCAD(obj, file.name);
        } catch (err) {
          alert('Failed to parse OBJ model: ' + err.message);
        }
      };
    } else if (ext === 'glb' || ext === 'gltf') {
      reader.readAsArrayBuffer(file);
      reader.onload = (ev) => {
        try {
          const loader = new GLTFLoader();
          loader.parse(ev.target.result, '', (gltf) => {
            processLoadedCAD(gltf.scene, file.name);
          });
        } catch (err) {
          alert('Failed to parse GLTF/GLB model: ' + err.message);
        }
      };
    } else if (ext === 'stl') {
      reader.readAsArrayBuffer(file);
      reader.onload = (ev) => {
        try {
          const loader = new STLLoader();
          const geometry = loader.parse(ev.target.result);
          const material = new THREE.MeshStandardMaterial({
            color: 0x94a3b8,
            metalness: 0.8,
            roughness: 0.25
          });
          const mesh = new THREE.Mesh(geometry, material);
          mesh.name = file.name.replace(/\.[^/.]+$/, "");
          const group = new THREE.Group();
          group.add(mesh);
          processLoadedCAD(group, file.name);
        } catch (err) {
          alert('Failed to parse STL model: ' + err.message);
        }
      };
    }
  };

  // Handle direct file selection from Windows File Explorer input
  const handleMainFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileProcess(e.target.files[0]);
    }
    e.target.value = '';
  };

  // Drag and Drop handlers
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileProcess(e.dataTransfer.files[0]);
    }
  };

  // Unload current CAD file to stage another
  const handleUnloadCAD = () => {
    soundFx.playClick();
    setCustomModel(null);
    setCustomModelName('');
    setDynamicSteps(null);
    setCadStats(null);
    setAssemblyTitle('');
    setSelectedModule(null);
    setCurrentStepIndex(0);
    setCompletedSteps([]);
    setIsDefectSimulated(false);
    setIsStageCardDismissed(false);
  };

  // Direct 1-Click Load for files in D:\solidworks\
  const handleLoadSpecificCAD = async (moduleId, playSound = true) => {
    if (playSound) soundFx.playClick();
    const fileName = moduleId === 'car'
      ? 'BMW_M_Series_Complete_Body_Assembly.obj'
      : (moduleId === 'clutch'
        ? 'Automotive_Clutch_and_Pressure_Plate_Assembly.obj'
        : (moduleId === 'knuckle'
          ? 'Knuckle_Joint_Assembly.obj'
          : 'Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj'));
    const fileUrl = `/models/${fileName}`;

    try {
      const resp = await fetch(fileUrl);
      if (!resp.ok) throw new Error('File not found: ' + fileUrl);
      const text = await resp.text();
      const loader = new OBJLoader();
      const obj = loader.parse(text);
      processLoadedCAD(obj, fileName);
    } catch (err) {
      console.warn('CAD loading error:', err);
    }
  };

  // --- Assembly Cycle Stopwatch ---
  useEffect(() => {
    let timer = null;
    if (isTimerRunning) {
      timer = setInterval(() => {
        setCycleTimeSeconds(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isTimerRunning]);

  const formatCycleTime = (totalSecs) => {
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // --- Audio / Voice Synchronization ---
  useEffect(() => {
    soundFx.soundEnabled = soundEnabled;
    soundFx.speechEnabled = speechEnabled;
  }, [soundEnabled, speechEnabled]);

  // Subscribe to speech playback state & unlock browser audio on first user gesture
  useEffect(() => {
    const handleSpeaking = (speaking, lang, text) => {
      setIsVoiceSpeaking(speaking);
      setSpeakingText(speaking ? text : '');
    };
    soundFx.addSpeakingListener(handleSpeaking);

    const unlockAudio = () => {
      soundFx.initContext();
      if ('speechSynthesis' in window && window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }
    };
    window.addEventListener('click', unlockAudio, { once: true });
    window.addEventListener('touchstart', unlockAudio, { once: true });

    return () => {
      soundFx.removeSpeakingListener(handleSpeaking);
      window.removeEventListener('click', unlockAudio);
      window.removeEventListener('touchstart', unlockAudio);
    };
  }, []);



  // Global Keyboard Navigation Shortcuts (ArrowRight / Space -> Next, ArrowLeft -> Prev, 'Z' -> Zen, 'E' -> Explode, 'T' -> Torque)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        handleNextStep();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        handlePrevStep();
      } else if (e.key === 'z' || e.key === 'Z') {
        e.preventDefault();
        soundFx.playClick();
        setIsZenMode(prev => !prev);
      } else if (e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        soundFx.playClick();
        setExplodedPercent(prev => prev === 0 ? 80 : 0);
      } else if (e.key === 'x' || e.key === 'X') {
        e.preventDefault();
        soundFx.playClick();
        setIsXRayMode(prev => !prev);
      } else if (e.key === 't' || e.key === 'T') {
        e.preventDefault();
        if (currentStep?.requiresTorque) {
          soundFx.playSuccess();
          setCurrentTorque(currentStep.targetTorque || 45);
          setIsTorqueVerified(true);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentStepIndex, isTorqueVerified, currentStep, isZenMode, stepsList]);

  // When language or module changes: preload offline voice packs and update controller language
  const prevLangRef = useRef(selectedVoiceLanguage);
  useEffect(() => {
    soundFx.setLanguage(selectedVoiceLanguage);
    soundFx.preloadVoicePacks(effectiveModule, selectedVoiceLanguage);
    // Only re-speak if the user actively switched the language, not on initial mount
    if (prevLangRef.current !== selectedVoiceLanguage) {
      prevLangRef.current = selectedVoiceLanguage;
      if (speechEnabled && currentStep?.voiceScript) {
        soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule);
      }
    }
  }, [selectedVoiceLanguage, effectiveModule]);

  // Trigger voice narration and set step torque on step change
  useEffect(() => {
    if (!currentStep || !customModel) return;
    const isStepDone = completedSteps.includes(currentStepIndex + 1);
    if (!isStepDone) {
      setCurrentTorque(0);
      setIsTorqueVerified(!currentStep.requiresTorque);
    } else {
      setIsTorqueVerified(true);
      setCurrentTorque(currentStep.targetTorque || 0);
    }
    setIsDefectSimulated(false);
    setDefectValue(null);

    if (speechEnabled && currentStep.voiceScript) {
      soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule);
    }
  }, [currentStepIndex, currentStep?.id, effectiveModule]);


  // --- Real Camera Stream Management ---
  const startCamera = async (targetFacing = cameraFacingMode) => {
    try {
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: targetFacing },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });
      mediaStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setIsCameraActive(true);
      setIsARMode(true);
      soundFx.playSuccess();
    } catch (err) {
      console.warn('Camera access denied or unavailable. Fallback to synthetic AR scene.', err);
      setIsARMode(true);
      setIsCameraActive(false);
    }
  };

  const flipCamera = async () => {
    soundFx.playClick();
    const nextFacing = cameraFacingMode === 'environment' ? 'user' : 'environment';
    setCameraFacingMode(nextFacing);
    if (isCameraActive) {
      await startCamera(nextFacing);
    }
  };

  const stopCamera = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
    setIsARMode(false);
    soundFx.playClick();
  };

  const toggleARMode = () => {
    soundFx.playClick();
    if (!isARMode) {
      startCamera();
    } else {
      stopCamera();
    }
  };

  // --- Step Navigation Logic ---
  const handleNextStep = () => {
    if (!currentStep) return;

    // Check torque verification if step requires torque
    if (!isTorqueVerified && currentStep.requiresTorque) {
      if (isZenMode) {
        // In Zen View, auto-apply the required target torque with chime so workflow never freezes
        const targetTorque = currentStep.targetTorque || 45;
        setCurrentTorque(targetTorque);
        setIsTorqueVerified(true);
        soundFx.playSuccess();
      } else {
        soundFx.playAlarm();
        soundFx.speak('Please complete the required torque before proceeding to the next step.', null, effectiveModule);
        return;
      }
    }

    soundFx.playSuccess();
    if (currentStepIndex < stepsList.length - 1) {
      const nextIndex = currentStepIndex + 1;
      setCurrentStepIndex(nextIndex);
      setExplodedPercent(0);
      const nextStep = stepsList[nextIndex];
      const isNextDone = completedSteps.includes(nextIndex + 1);
      if (isNextDone) {
        setIsTorqueVerified(true);
        setCurrentTorque(nextStep.targetTorque || 0);
      } else {
        // If next step does not require torque, it is automatically verified
        setIsTorqueVerified(!nextStep.requiresTorque);
        setCurrentTorque(0);
      }
      setCompletedSteps(prev => [...new Set([...prev, nextIndex + 1])]);
      if (nextIndex === stepsList.length - 1) {
        setIsTimerRunning(false);
      }
    } else {
      // Reached final step: Automatically pop up the official Quality Assurance Certificate
      setIsTimerRunning(false);
      setIsQCModalOpen(true);
      if (speechEnabled) {
        soundFx.speak('Assembly sequence successfully completed. Official ISO Quality Certificate generated.', null, effectiveModule);
      }
    }
  };

  const handlePrevStep = () => {
    soundFx.playClick();
    if (currentStepIndex > 0) {
      const prevIndex = currentStepIndex - 1;
      setCurrentStepIndex(prevIndex);
      setExplodedPercent(0);
      const prevStep = stepsList[prevIndex];
      setIsTorqueVerified(true);
      setCurrentTorque(prevStep.targetTorque || 0);
    }
  };

  const handleSelectStep = (index) => {
    soundFx.playClick();
    setCurrentStepIndex(index);
    setExplodedPercent(0);
    const targetStep = stepsList[index];
    const isStepDone = completedSteps.includes(index + 1);
    if (isStepDone) {
      setIsTorqueVerified(true);
      setCurrentTorque(targetStep.targetTorque || 0);
    } else {
      setIsTorqueVerified(!targetStep.requiresTorque);
      setCurrentTorque(0);
    }
  };

  // --- Real-Time CMM Defect Simulation & Laser Realignment Controls ---
  const handleToggleDefect = () => {
    if (!currentStep) return;
    if (!isDefectSimulated) {
      const initVal = currentStep.defectConfig ? currentStep.defectConfig.defectInitial : 71.7;
      setDefectValue(initVal);
      setIsDefectSimulated(true);
      soundFx.playAlarm();
      if (speechEnabled) {
        soundFx.speak('Quality defect detected. Assembly halted for CMM realignment.', null, effectiveModule);
      }
    } else {
      handleResolveDefect();
    }
  };

  const handleResolveDefect = () => {
    setIsDefectSimulated(false);
    setDefectValue(null);
    setDefectsResolvedCount(prev => prev + 1);
    soundFx.playSuccess();
    if (speechEnabled) {
      soundFx.speak('Geometric datum alignment verified within ISO tolerance. Assembly line restored.', null, effectiveModule);
    }
  };


  // --- Industrial Hands-Free Voice Command Execution ---
  const handleVoiceCommand = (cmdType, spokenText) => {
    soundFx.playClick();
    setLastVoiceCommand(spokenText);

    if (cmdType === 'next') {
      // If current step requires torque and hasn't been torqued yet, auto-verify for smooth voice operation
      if (currentStep && currentStep.requiresTorque && !isTorqueVerified) {
        setCurrentTorque(currentStep.targetTorque);
        setIsTorqueVerified(true);
        soundFx.playSuccess();
        setTimeout(() => {
          handleNextStep();
        }, 350);
      } else {
        handleNextStep();
      }
    } else if (cmdType === 'prev') {
      handlePrevStep();
    } else if (cmdType === 'explode') {
      setExplodedPercent(75);
      soundFx.playSuccess();
    } else if (cmdType === 'assemble') {
      setExplodedPercent(0);
      soundFx.playSuccess();
    } else if (cmdType === 'torque') {
      if (currentStep && currentStep.requiresTorque) {
        setCurrentTorque(currentStep.targetTorque);
        setIsTorqueVerified(true);
        soundFx.playSuccess();
      }
    } else if (cmdType === 'scan') {
      handleToggleDefect();
    } else if (cmdType === 'calibrate') {
      handleResolveDefect();
    } else if (cmdType === 'xray') {
      setIsXRayMode(prev => !prev);
      soundFx.playClick();
    } else if (cmdType === 'rotate') {
      setIsAutoRotate(prev => !prev);
      soundFx.playClick();
    } else if (cmdType === 'camera') {
      toggleARMode();
      soundFx.playClick();
    } else if (cmdType === 'repeat' || cmdType === 'guide' || cmdType === 'speak') {
      if (currentStep?.voiceScript) {
        soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule);
      }
    } else if (cmdType === 'certificate') {
      setIsQCModalOpen(true);
      soundFx.playSuccess();
    } else if (cmdType === 'qr' || cmdType === 'barcode') {
      setIsQRScannerOpen(true);
      soundFx.playClick();
    }
  };

  // --- Real Poka-Yoke Machine Vision Part Verification Callback ---
  const handlePartQRVerified = (verifiedCode) => {
    setIsTorqueVerified(true);
    setCompletedSteps(prev => [...new Set([...prev, currentStepIndex + 1])]);
    soundFx.playSuccess();
  };

  // --- Auto-Play Sequence (For instant wow demo in viva) ---
  const handleAutoPlay = () => {
    if (isAutoPlaying) return;
    setIsAutoPlaying(true);
    setCurrentStepIndex(0);
    setExplodedPercent(0);

    let step = 0;
    const interval = setInterval(() => {
      step++;
      if (step < stepsList.length) {
        setCurrentStepIndex(step);
        setCompletedSteps(prev => [...new Set([...prev, step + 1])]);
      } else {
        clearInterval(interval);
        setIsAutoPlaying(false);
        setIsTimerRunning(false);
        setIsQCModalOpen(true);
      }
    }, 4500);
  };

  // Calculate overall progress percentage safely
  const progressPercent = stepsList.length > 0 ? Math.round(((currentStepIndex + 1) / stepsList.length) * 100) : 0;

  return (
    <div
      className="autoar-app"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      {/* Hidden Native File Input for Windows File Explorer */}
      <input
        ref={mainFileInputRef}
        type="file"
        accept=".obj,.glb,.gltf,.stl"
        style={{ display: 'none' }}
        onChange={handleMainFileSelect}
      />

      {/* Top Cockpit Header */}
      <header className="autoar-header">
        <div className="header-left">
          <div className="brand-logo">
            <span className="car-icon">🏎️</span>
            <div className="brand-text">
              <div className="brand-title">AutoAR <span className="brand-tag">4.0</span></div>
              <div className="brand-sub">AR ASSEMBLY LINE</div>
            </div>
          </div>
        </div>

        <div className="header-center">
          {/* Quick Assembly Switcher Pills */}
          <div className="header-quick-cad-switch">
            <button
              className={`btn-cad-pill ${effectiveModule === 'brake' ? 'active' : ''}`}
              onClick={() => handleLoadSpecificCAD('brake')}
              title="Load 320mm Ventilated Disc Brake"
            >
              🏎️ Brake
            </button>
            <button
              className={`btn-cad-pill ${effectiveModule === 'clutch' ? 'active' : ''}`}
              onClick={() => handleLoadSpecificCAD('clutch')}
              title="Load Automotive Clutch System"
            >
              ⚙️ Clutch
            </button>
            <button
              className={`btn-cad-pill ${effectiveModule === 'knuckle' ? 'active' : ''}`}
              onClick={() => handleLoadSpecificCAD('knuckle')}
              title="Load Kinematic Knuckle Joint"
            >
              🦾 Knuckle
            </button>
            <button
              className={`btn-cad-pill ${effectiveModule === 'car' ? 'active' : ''}`}
              onClick={() => handleLoadSpecificCAD('car')}
              title="Load BMW M4 High-Performance Vehicle Assembly"
            >
              🏎️ BMW M4
            </button>
          </div>

          {/* Active CAD File Indicator Pill */}
          {customModelName ? (
            <div className="active-cad-chip loaded" title={`Loaded Model: ${customModelName}`}>
              <span className="dot pulse-green"></span>
              <span className="chip-filename font-mono">
                {customModelName.length > 16 ? customModelName.substring(0, 14) + '...' : customModelName}
              </span>
              <button
                className="btn-header-change-cad font-mono"
                onClick={handleUnloadCAD}
                title="Unload current CAD model to upload your own"
              >
                📂 Import
              </button>
            </div>
          ) : (
            <button
              className="btn-header-import-direct font-mono"
              onClick={() => {
                soundFx.playClick();
                mainFileInputRef.current?.click();
              }}
              title="Open File Explorer to load your 3D CAD model (.obj, .glb, .stl)"
            >
              <span className="dot pulse-cyan"></span>
              <span>📂 Import CAD</span>
            </button>
          )}
        </div>

        <div className="header-right">
          {/* Unified Audio, Mic & Multi-Language Suite */}
          <div className="header-audio-suite">
            <button
              className={`btn-audio-mini ${soundEnabled ? 'active' : 'muted'}`}
              onClick={() => {
                const next = !soundEnabled;
                setSoundEnabled(next);
                soundFx.soundEnabled = next;
                if (next) soundFx.playSuccess();
              }}
              title={soundEnabled ? 'Sound Effects Active (Click to Mute)' : 'Sound Effects Muted (Click to Enable)'}
            >
              {soundEnabled ? '🔊' : '🔇'}
            </button>

            <button
              className={`btn-voice-mini ${isVoiceListening ? 'listening' : ''}`}
              onClick={() => setIsVoiceListening(!isVoiceListening)}
              title={isVoiceListening ? 'Voice Control Active (Listening...)' : 'Click to Enable Hands-Free Voice Control'}
            >
              <span className="mic-glyph">{isVoiceListening ? '🎙️' : '🎤'}</span>
              <span className="mic-txt font-mono">{isVoiceListening ? 'LIVE' : 'MIC'}</span>
              {isVoiceListening && <span className="mic-pulse-dot"></span>}
            </button>

            <button
              className={`btn-audio-mini ${speechEnabled ? 'active' : 'muted'}`}
              onClick={() => {
                const next = !speechEnabled;
                setSpeechEnabled(next);
                soundFx.speechEnabled = next;
                if (next && currentStep?.voiceScript) {
                  soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule, true);
                } else if (!next) {
                  soundFx.stopSpeech();
                }
              }}
              title={speechEnabled ? 'Voice Assistant Active (Click to Mute)' : 'Voice Assistant Muted (Click to Unmute & Speak)'}
            >
              {speechEnabled ? '🗣️' : '🤫'}
            </button>

            <div className="suite-divider"></div>

            <div className={`suite-lang-box ${isVoiceSpeaking ? 'speaking-active' : ''}`} title="Voice Assistant Guidance Language">
              <span className="lang-icon">{isVoiceSpeaking ? '🔊' : '🌐'}</span>
              <select
                className="suite-lang-select font-mono"
                value={selectedVoiceLanguage}
                onChange={(e) => {
                  const newLang = e.target.value;
                  soundFx.playClick();
                  setSelectedVoiceLanguage(newLang);
                  setSpeechEnabled(true);
                  soundFx.speechEnabled = true;
                  soundFx.setLanguage(newLang);
                  if (currentStep?.voiceScript) {
                    soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule, true);
                  }
                }}
              >
                <option value="en">EN</option>
                <option value="ta">தமிழ்</option>
                <option value="ml">മലയാളം</option>
                <option value="hi">हिन्दी</option>
              </select>
            </div>
          </div>

          <div className="timer-badge font-mono" title="Station Cycle Timer">
            <span className="timer-icon">⏱️</span>
            <span className="timer-text">{formatCycleTime(cycleTimeSeconds)}</span>
          </div>

          <div className="header-actions-suite">
            <button
              className={`btn-mode-toggle ${isARMode ? 'active-ar' : ''}`}
              onClick={toggleARMode}
              title="Toggle Live Camera AR Overlay"
            >
              {isARMode ? '📷 AR Cam' : '🏢 3D Studio'}
            </button>

            {isARMode && (
              <button
                className="btn-flip-camera"
                onClick={flipCamera}
                title={`Switch camera (Current: ${cameraFacingMode === 'environment' ? 'Rear Camera' : 'Selfie Camera'})`}
              >
                🔄 Flip
              </button>
            )}

            <button
              className="btn-qc-report"
              onClick={() => setIsQCModalOpen(true)}
              title="View IATF 16949 / ISO 9001 Digital QC Certificate"
            >
              📋 QC Cert
            </button>

            <button
              className={`btn-zen-toggle ${isZenMode ? 'active-zen' : ''}`}
              onClick={() => {
                soundFx.playClick();
                setIsZenMode(!isZenMode);
              }}
              title={isZenMode ? 'Exit Zen Mode (Show Panels)' : 'Enter Zen Mode (Full 3D CAD Focus)'}
            >
              {isZenMode ? '⛶ Exit' : '✨ Zen'}
            </button>

            <button
              className="btn-hud-info-chip"
              onClick={() => setIsARGuideModalOpen(true)}
              title="Learn how PTC Vuforia, DELMIA, Tulip and Light Guide Systems work in real assembly"
            >
              ⚡ How AR Works
            </button>
          </div>
        </div>
      </header>

      {/* Main Assembly Workstation Grid */}
      <main className={`autoar-main-grid ${isZenMode ? 'zen-mode' : ''}`}>
        {/* Left Column: Interactive Step Timeline */}
        <aside className="steps-sidebar">
          <div className="sidebar-header">
            <h3>ASSEMBLY SEQUENCE</h3>
            <span className="step-counter font-mono">
              {stepsList.length > 0 ? `${currentStepIndex + 1} / ${stepsList.length}` : '0 / 0'}
            </span>
          </div>
          <div className="sidebar-assembly-badge font-mono" title={assemblyTitle || 'No CAD Loaded'}>
            <span className={`dot ${customModel ? 'pulse-green' : 'pulse-amber'}`}></span>
            <span>{assemblyTitle || 'Awaiting CAD Import'}</span>
          </div>

          <div className="steps-list">
            {stepsList.length === 0 ? (
              <div className="no-cad-steps-empty">
                <div className="empty-box-icon">📋</div>
                <div className="empty-box-title font-mono">ASSEMBLY SEQUENCE</div>
                <div className="empty-box-sub">
                  Awaiting CAD import. Steps will populate automatically when a model is loaded.
                </div>
              </div>
            ) : (
              stepsList.map((step, idx) => {
                const isActive = idx === currentStepIndex;
                const isCompleted = completedSteps.includes(idx + 1);

                return (
                  <div
                    key={step.id}
                    className={`step-card ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
                    onClick={() => handleSelectStep(idx)}
                  >
                    <div className="step-card-num font-mono">
                      {isCompleted && !isActive ? '✓' : `0${step.id}`}
                    </div>
                    <div className="step-card-info">
                      <div className="step-card-title">{step.title || step.partName}</div>
                      <div className="step-card-sub">
                        <span>{step.partCode}</span>
                        {step.requiresTorque && (
                          <span className="torque-tag">{step.targetTorque} Nm</span>
                        )}
                      </div>
                    </div>
                    {isActive && <div className="step-indicator-chevron">▶</div>}
                  </div>
                );
              })
            )}
          </div>

          {/* Quick Auto-Play Demo */}
          <div className="sidebar-footer">
            <button
              className="btn-autoplay"
              onClick={handleAutoPlay}
              disabled={isAutoPlaying || !customModel}
            >
              {isAutoPlaying ? '⏳ Playing Sequence...' : '▶ Auto-Demonstrate All Steps'}
            </button>
          </div>
        </aside>

        {/* Center Viewport: AR Video / 3D Canvas / HUD */}
        <section className="viewport-center">
          {/* Background Camera Video Stream (when active) */}
          <video
            ref={videoRef}
            className={`ar-camera-feed ${isCameraActive ? 'visible' : ''}`}
            playsInline
            muted
            autoPlay
          />

          {/* Fallback Synthetic Workshop Background (when camera off) */}
          {!isCameraActive && (
            <div className={`synthetic-workshop-bg ${isARMode ? 'ar-grid-mode' : ''}`} />
          )}

          {/* Three.js 3D WebGL Canvas Layer */}
          <div className="three-canvas-container">
            <AssemblyViewer3D
              currentStep={currentStepIndex + 1}
              explodedPercent={explodedPercent}
              isDefectSimulated={isDefectSimulated}
              defectAngleOffset={defectAngleOffset}
              isXRayMode={isXRayMode}
              isAutoRotate={isAutoRotate}
              isARMode={isARMode}
              isProjectedARMode={isProjectedARMode}
              activePartKey={currentStep?.partKey || ''}
              cameraStreamActive={isCameraActive}
              customModel={customModel}
              customModelName={customModelName}
              effectiveModule={effectiveModule}
              customCADParams={customCADParams}
              showAllParts={showAllParts}
            />
          </div>

          {/* High-Tech Empty State Overlay when No CAD Loaded */}
          {!customModel && !isStageCardDismissed && (
            <div className="viewport-empty-cad-stage">
              <div className="empty-stage-card">
                <button
                  className="btn-dismiss-stage-card"
                  onClick={() => {
                    soundFx.playClick();
                    setIsStageCardDismissed(true);
                  }}
                  title="Hide overlay to view full 3D workspace"
                >
                  ✕
                </button>

                <div className="stage-laser-badge font-mono">
                  <span className="dot pulse-cyan"></span>
                  <span>WORKSTATION READY</span>
                </div>

                <div className="stage-hero-icon-wrapper">
                  <span className="stage-hero-icon">💠</span>
                </div>

                <h2 className="stage-title">Import 3D CAD Assembly</h2>
                <p className="stage-desc">
                  Drag & drop your <strong>.OBJ</strong>, <strong>.GLB</strong>, or <strong>.STL</strong> file here, or click to browse from your PC.
                </p>
                
                <button
                  className="btn-stage-explorer font-mono"
                  onClick={() => { soundFx.playClick(); mainFileInputRef.current?.click(); }}
                >
                  <span className="btn-icon">📂</span>
                  <span>OPEN FILE EXPLORER</span>
                </button>

                <div className="stage-samples-inline">
                  <span className="samples-tag font-mono">QUICK SAMPLES:</span>
                  <button
                    className="stage-sample-pill"
                    onClick={() => handleLoadSpecificCAD('brake')}
                    title="Load 320mm Ventilated Disc Brake"
                  >
                    🏎️ Disc Brake
                  </button>
                  <button
                    className="stage-sample-pill"
                    onClick={() => handleLoadSpecificCAD('clutch')}
                    title="Load Clutch & Pressure Plate"
                  >
                    ⚙️ Clutch
                  </button>
                  <button
                    className="stage-sample-pill"
                    onClick={() => handleLoadSpecificCAD('knuckle')}
                    title="Load Kinematic Knuckle Joint"
                  >
                    🦾 Knuckle
                  </button>
                  <button
                    className="stage-sample-pill"
                    onClick={() => handleLoadSpecificCAD('car')}
                    title="Load BMW M-Power High-Performance Automobile Assembly"
                  >
                    🏎️ BMW M-Series
                  </button>
                </div>

              </div>
            </div>
          )}

          {/* Floating 'Open CAD' badge if user dismissed the card to see the 3D workspace */}
          {!customModel && isStageCardDismissed && (
            <div className="minimized-stage-launcher">
              <button
                className="btn-reopen-stage font-mono"
                onClick={() => {
                  soundFx.playClick();
                  setIsStageCardDismissed(false);
                }}
                title="Show CAD import card"
              >
                <span>📂 IMPORT CAD MODEL</span>
              </button>
              <button
                className="btn-reopen-explorer font-mono"
                onClick={() => {
                  soundFx.playClick();
                  mainFileInputRef.current?.click();
                }}
                title="Open Windows File Explorer"
              >
                <span>📂 BROWSE PC</span>
              </button>
            </div>
          )}

          {/* Futuristic AR HUD Overlay with Real-Time CMM Metrology */}
          {customModel && currentStep && (
            <AROverlayHUD
              isARMode={isARMode}
              isProjectedARMode={isProjectedARMode}
              isDefectSimulated={isDefectSimulated}
              currentStepData={currentStep}
              totalSteps={stepsList.length}
              defectValue={liveDefectVal}
              onAdjustDefectValue={setDefectValue}
              onResolveDefect={handleResolveDefect}
              onVoiceCommand={handleVoiceCommand}
              isVoiceListening={isVoiceListening}
              onToggleVoiceListening={() => setIsVoiceListening(prev => !prev)}
              lastVoiceCommand={lastVoiceCommand}
              onOpenARArchitectureModal={() => setIsARGuideModalOpen(true)}
            />
          )}

          {/* Viewport Floating Quick Tools Bar */}
          <div className="viewport-quick-tools">
            {/* Quick Step Navigation for seamless 3D & Zen Mode walkthrough */}
            <div className="dock-step-nav-group">
              <button
                className="btn-dock-step btn-dock-prev"
                onClick={handlePrevStep}
                disabled={currentStepIndex === 0 || stepsList.length === 0}
                title="Previous Step"
              >
                ◀ Prev
              </button>
              <span className="dock-step-count font-mono">
                {stepsList.length > 0 ? `${String(currentStepIndex + 1).padStart(2, '0')}/${String(stepsList.length).padStart(2, '0')}` : '00/00'}
              </span>
              <button
                className="btn-dock-step btn-dock-next"
                onClick={handleNextStep}
                disabled={stepsList.length === 0}
                title={currentStepIndex === stepsList.length - 1 ? 'Finish & Certify' : 'Next Step'}
              >
                {currentStepIndex === stepsList.length - 1 ? 'Certify ✓' : 'Next ▶'}
              </button>
              {currentStep && currentStep.requiresTorque && (
                <button
                  className={`btn-dock-torque ${isTorqueVerified ? 'verified' : ''}`}
                  onClick={() => {
                    soundFx.playSuccess();
                    setCurrentTorque(currentStep.targetTorque || 45);
                    setIsTorqueVerified(true);
                  }}
                  title="Apply required torque (Nm)"
                >
                  🔧 {isTorqueVerified ? `${currentStep.targetTorque || 45} Nm ✓` : `Torque (${currentStep.targetTorque || 45} Nm)`}
                </button>
              )}
            </div>

            <div className="dock-vertical-divider"></div>

            <div className="quick-tool-slider-wrap">
              <span className="tool-lbl">💥 EXPLODED VIEW:</span>
              <input
                type="range"
                min="0"
                max="100"
                value={explodedPercent}
                onChange={(e) => setExplodedPercent(Number(e.target.value))}
                className="explode-slider"
                disabled={stepsList.length === 0}
              />
              <span className="explode-val font-mono">{explodedPercent}%</span>
              <button
                className="btn-tiny"
                disabled={stepsList.length === 0}
                onClick={() => {
                  soundFx.playClick();
                  setExplodedPercent(explodedPercent === 0 ? 80 : 0);
                }}
              >
                {explodedPercent === 0 ? 'Explode' : 'Collapse'}
              </button>
            </div>

            <div className="quick-tool-btn-group">
              <button
                className={`btn-tool-chip ${showAllParts ? 'active' : ''}`}
                onClick={() => {
                  soundFx.playClick();
                  setShowAllParts(!showAllParts);
                }}
                disabled={stepsList.length === 0}
                title="Toggle between full solid assembly and step focus"
              >
                {showAllParts ? '👁️ Full Solid (ON)' : '👻 Ghost Focus (AR)'}
              </button>
              <button
                className={`btn-tool-chip ${isProjectedARMode ? 'active' : ''}`}
                onClick={() => {
                  soundFx.playClick();
                  setIsProjectedARMode(!isProjectedARMode);
                }}
                title="Toggle Light Guide Systems Projected Work Instructions & Laser Workbench Grid"
              >
                {isProjectedARMode ? '📽️ Projected AR (ON)' : '📽️ Projected AR'}
              </button>
              <button
                className={`btn-tool-chip ${isXRayMode ? 'active' : ''}`}
                onClick={() => {
                  soundFx.playClick();
                  setIsXRayMode(!isXRayMode);
                }}
                disabled={stepsList.length === 0}
                title="Toggle Internal Clearances & Wireframe"
              >
                {isXRayMode ? '🦴 X-Ray (ON)' : '🦴 X-Ray View'}
              </button>
              <button
                className={`btn-tool-chip ${isAutoRotate ? 'active' : ''}`}
                onClick={() => {
                  soundFx.playClick();
                  setIsAutoRotate(!isAutoRotate);
                }}
                title="360 Turntable Spin"
              >
                {isAutoRotate ? '🔄 Spinning 360°' : '🔄 360° Spin'}
              </button>
              <button
                className={`btn-tool-chip btn-defect-trigger ${isDefectSimulated ? 'defect-on' : ''}`}
                onClick={() => {
                  soundFx.playClick();
                  handleToggleDefect();
                }}
                disabled={stepsList.length === 0}
                title="Trigger Real-Time Laser CMM Defect Scan"
              >
                {isDefectSimulated ? '🔬 Close CMM Scan' : '🔬 Laser CMM Defect Scan'}
              </button>
              <button
                className="btn-tool-chip btn-qr-scan-trigger"
                onClick={() => {
                  soundFx.playClick();
                  setIsQRScannerOpen(true);
                }}
                disabled={stepsList.length === 0}
                title="Scan component QR / Barcode with webcam (Poka-Yoke Machine Vision)"
              >
                📱 QR Scanner
              </button>
            </div>
          </div>
        </section>

        {/* Right Column: Active Step Instruction, Tool & Torque Console */}
        <aside className="instruction-sidebar">
          {!customModel || !currentStep ? (
            <div className="active-part-card awaiting-cad">
              <div className="part-header-tag" style={{ borderLeftColor: '#00f0ff' }}>
                <span className="category-text">WORKSTATION STAGING</span>
                <h2>Awaiting CAD Assembly Model</h2>
                <span className="part-number font-mono">STATUS: STANDBY</span>
              </div>

              <div className="instruction-body">
                <div className="instruction-heading">
                  <span className="guide-icon">📥</span>
                  <span>STANDBY PROTOCOL</span>
                </div>
                <p className="instruction-text">
                  Workstation datum fixture is calibrated. Select or drop a 3D CAD model (.OBJ, .GLB, or .STL) in the center viewport to generate step-by-step assembly instructions and quality protocols.
                </p>

                <div className="assembly-tip-box">
                  <span className="tip-icon">💡</span>
                  <span><strong>Workstation Note:</strong> Zero inbuilt models active. Models load directly from your computer files.</span>
                </div>
              </div>
            </div>
          ) : (
            <>
              {/* Active Part Header */}
              <div className="active-part-card">
                <div className="part-header-tag" style={{ borderLeftColor: currentStep.colorTag || '#00f0ff' }}>
                  <span className="category-text">{currentStep.category || 'Mechanical Component'}</span>
                  <h2>{currentStep.partName || currentStep.title}</h2>
                  <span className="part-number font-mono">{currentStep.partCode || 'PRT-01'}</span>
                </div>

                {/* Step Instruction Box */}
                <div className="instruction-body">
                  <div className="instruction-heading">
                    <span className="guide-icon">📖</span>
                    <span>STANDARD WORK INSTRUCTION (SWI)</span>
                    <button
                      className={`btn-step-voice-play ${isVoiceSpeaking ? 'playing' : ''}`}
                      onClick={() => {
                        if (currentStep?.voiceScript) {
                          setSpeechEnabled(true);
                          soundFx.speechEnabled = true;
                          soundFx.speak(currentStep.voiceScript, currentStep, effectiveModule, true);
                        }
                      }}
                      title="Play step assembly voice narration"
                    >
                      <span className="voice-btn-icon">{isVoiceSpeaking ? '🔊' : '🗣️'}</span>
                      <span className="font-mono">
                        {isVoiceSpeaking ? 'SPEAKING...' : 'HEAR AUDIO GUIDE'}
                      </span>
                    </button>
                  </div>
                  <p className="instruction-text">{currentStep.instruction || 'Inspect component datum and align with fixture jig.'}</p>

                  <div className="assembly-tip-box">
                    <span className="tip-icon">💡</span>
                    <span><strong>Pro-Tip:</strong> {currentStep.tip || 'Verify smooth fitment before applying torque.'}</span>
                  </div>
                </div>

                {/* Engineering Specifications Grid */}
                {currentStep.specs && currentStep.specs.length > 0 && (
                  <div className="specs-grid">
                    {currentStep.specs.map((item, i) => (
                      <div key={i} className="spec-tile">
                        <span className="spec-lbl">{item.label}</span>
                        <span className="spec-val font-mono">{item.value}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Smart IoT Torque Wrench Module & Poka-Yoke QR Validator */}
              <div className="tool-console-card">
                <TorqueWrenchSimulator
                  stepData={currentStep}
                  currentTorque={currentTorque}
                  setCurrentTorque={setCurrentTorque}
                  isTorqueVerified={isTorqueVerified}
                  setIsTorqueVerified={setIsTorqueVerified}
                />

                <button
                  className="btn-open-qr-scanner font-mono"
                  onClick={() => {
                    soundFx.playClick();
                    setIsQRScannerOpen(true);
                  }}
                  title="Scan component QR / Barcode with webcam to verify correct bin (Poka-Yoke)"
                >
                  <span>📷 SCAN PART QR (POKA-YOKE)</span>
                </button>
              </div>

              {/* Step Action Buttons */}
              <div className="step-actions-footer">
                <button
                  className="btn-action btn-prev"
                  onClick={handlePrevStep}
                  disabled={currentStepIndex === 0}
                >
                  ◀ Previous
                </button>

                <button
                  className={`btn-action btn-next ${isTorqueVerified ? 'ready' : 'waiting'}`}
                  onClick={handleNextStep}
                >
                  {currentStepIndex === stepsList.length - 1 ? 'Finish & Certify ✓' : 'Next Step ▶'}
                </button>
              </div>
            </>
          )}
        </aside>
      </main>

      {/* Bottom Status / Telemetry Footer */}
      <footer className="autoar-footer">
        <div className="footer-left">
          <span className="status-dot"></span>
          <span>AR ENGINE: WebGL 2.0 / Three.js PBR • ZERO INSTALLATION ACTIVE</span>
        </div>
        <div className="footer-center">
          <div className="progress-bar-wrap">
            <div className="progress-bar-track">
              <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }}></div>
            </div>
            <span className="progress-label font-mono">{progressPercent}% COMPLETE</span>
          </div>
        </div>
        <div className="footer-right">
          <span className="operator-id">OPERATOR: BERNISH (MECH-AUTO-TECH)</span>
          <span className="separator">|</span>
          <span className="iso-badge">ISO 9001 / IATF 16949 COMPLIANT</span>
        </div>
      </footer>

      {/* Quality Assurance Certificate Modal */}
      <SupervisorAnalyticsModal
        isOpen={isQCModalOpen}
        onClose={() => setIsQCModalOpen(false)}
        cycleTime={formatCycleTime(cycleTimeSeconds)}
        defectsResolvedCount={defectsResolvedCount}
        stepsData={stepsList}
        componentTitle={
          effectiveModule === 'car'
            ? 'BMW M-Performance Sports Car Assembly (M4/M8 GTE)'
            : (effectiveModule === 'clutch'
              ? 'Automotive Single-Plate Dry Clutch & Pressure Plate Assembly (280mm)'
              : (effectiveModule === 'knuckle'
                ? 'Heavy-Duty Mechanical Knuckle Joint Assembly (30mm Pin)'
                : 'Ventilated Disc Brake & Caliper Assembly (320mm Front Axle)'))
        }
        workstationTitle={
          effectiveModule === 'car'
            ? 'BMW DINGOLFING PLANT • ASSEMBLY LINE 01 (M-SERIES MARRIAGE)'
            : (effectiveModule === 'clutch'
              ? 'WS-02 (TRANSMISSION CLUTCH MODULE)'
              : (effectiveModule === 'knuckle'
                ? 'WS-03 (KINEMATIC KNUCKLE JOINT LINE)'
                : 'WS-04 (CHASSIS BRAKE LINE)'))
        }
      />

      {/* Industrial AR Architecture Guide Modal (Explaining PTC Vuforia, DELMIA, Tulip & Light Guide Systems) */}
      <IndustrialARGuideModal
        isOpen={isARGuideModalOpen}
        onClose={() => setIsARGuideModalOpen(false)}
      />

      {/* Poka-Yoke Optical Machine Vision QR & Barcode Component Scanner Modal */}
      <PokaYokeQRScannerModal
        isOpen={isQRScannerOpen}
        onClose={() => setIsQRScannerOpen(false)}
        currentStep={currentStep}
        onPartVerified={handlePartQRVerified}
        selectedLanguage={selectedVoiceLanguage}
      />
    </div>
  );
}

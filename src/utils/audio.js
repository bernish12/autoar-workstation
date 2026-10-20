// Web Audio API Synthesizer, Offline Multi-Language Voice Packs & Speech Synthesis for AutoAR Studio

class SoundController {
  constructor() {
    this.audioCtx = null;
    this.soundEnabled = true;
    this.speechEnabled = true;
    this.currentLanguage = 'en'; // Default English ('en' | 'ta' | 'ml' | 'hi')
    this.currentAudio = null;
    this.isSpeaking = false;
    this.speakingListeners = new Set();
    this.audioCache = new Map();
    this.activeSpeakId = 0;
  }

  setLanguage(langCode) {
    if (['en', 'ta', 'ml', 'hi'].includes(langCode)) {
      this.currentLanguage = langCode;
    }
  }

  // Pre-buffer voice pack audio into memory for instant, zero-latency playback
  preloadVoicePacks(mod = 'brake', lang = this.currentLanguage) {
    if (typeof window === 'undefined') return;
    const maxSteps = mod === 'car' ? 12 : (mod === 'knuckle' ? 6 : 10);
    for (let i = 1; i <= maxSteps; i++) {
      const url = `/audio/voices/${mod}_${i}_${lang}.mp3`;
      if (!this.audioCache.has(url)) {
        try {
          const audio = new Audio();
          audio.preload = 'auto';
          audio.src = url;
          this.audioCache.set(url, audio);
        } catch {}
      }
    }
    ['sys_complete', 'sys_defect', 'sys_datum', 'sys_torque_req'].forEach(key => {
      const url = `/audio/voices/${key}_${lang}.mp3`;
      if (!this.audioCache.has(url)) {
        try {
          const audio = new Audio();
          audio.preload = 'auto';
          audio.src = url;
          this.audioCache.set(url, audio);
        } catch {}
      }
    });
  }

  addSpeakingListener(callback) {
    if (typeof callback === 'function') {
      this.speakingListeners.add(callback);
    }
  }

  removeSpeakingListener(callback) {
    this.speakingListeners.delete(callback);
  }

  notifySpeaking(isSpeaking, lang = this.currentLanguage, text = '') {
    this.isSpeaking = isSpeaking;
    this.speakingListeners.forEach(cb => {
      try { cb(isSpeaking, lang, text); } catch {}
    });
  }

  // Stop any active speech or voice pack playback
  stopSpeech() {
    if (this.currentAudio) {
      try {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
      } catch {}
      this.currentAudio = null;
    }
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
      } catch {}
    }
    this.notifySpeaking(false);
  }

  // Multi-Language Voice Guidance Engine (Offline Audio Packs -> Direct TTS -> SpeechSynthesis)
  speak(text, stepObj = null, moduleKey = null) {
    if (!this.speechEnabled) return;

    // Mutex token: invalidate any pending or asynchronous audio from prior steps
    const speakId = ++this.activeSpeakId;

    // Immediately stop any prior speech or audio playback
    this.stopSpeech();

    const lang = this.currentLanguage || 'en';

    // 1. Determine localized text
    let textToSpeak = text;
    if (lang !== 'en') {
      if (stepObj && stepObj.translations && stepObj.translations[lang]) {
        textToSpeak = stepObj.translations[lang];
      } else {
        textToSpeak = this.localizeText(text, lang, stepObj);
      }
    }

    // 2. Check for Pre-Recorded Native Voice Pack Audio (100% Reliable Offline)
    let preAudioFile = null;

    // Check system alerts
    if (text.includes('Assembly sequence successfully completed')) {
      preAudioFile = `/audio/voices/sys_complete_${lang}.mp3`;
    } else if (text.includes('Quality defect detected')) {
      preAudioFile = `/audio/voices/sys_defect_${lang}.mp3`;
    } else if (text.includes('Geometric datum alignment verified')) {
      preAudioFile = `/audio/voices/sys_datum_${lang}.mp3`;
    } else if (text.includes('Please complete the required torque')) {
      preAudioFile = `/audio/voices/sys_torque_req_${lang}.mp3`;
    } else if (stepObj && stepObj.id) {
      // Determine standard module key
      let mod = moduleKey;
      if (!mod) {
        const code = (stepObj.partCode || '').toUpperCase();
        const key = (stepObj.partKey || '').toLowerCase();
        if (code.includes('BRK') || code.includes('ROT') || code.includes('CAL') || code.includes('WH-') || key.includes('brake') || key.includes('hub')) {
          mod = 'brake';
        } else if (code.includes('CLT') || code.includes('FLY') || code.includes('PRS') || key.includes('clutch')) {
          mod = 'clutch';
        } else if (code.includes('CAR') || code.includes('FRM') || code.includes('CHS') || code.includes('ENG') || key.includes('chassis') || key.includes('engine')) {
          mod = 'car';
        } else if (code.includes('KNK') || code.includes('STE') || code.includes('STR') || key.includes('knuckle') || key.includes('tie')) {
          mod = 'knuckle';
        }
      }

      const maxSteps = mod === 'car' ? 12 : (mod === 'knuckle' ? 6 : 10);
      if (mod && stepObj.id >= 1 && stepObj.id <= maxSteps) {
        preAudioFile = `/audio/voices/${mod}_${stepObj.id}_${lang}.mp3`;
      }
    }

    // If pre-recorded voice pack audio exists, play it directly
    if (preAudioFile) {
      this.playVoiceAudioFile(preAudioFile, textToSpeak, lang, () => {
        // Fallback to dynamic TTS if file fails to load
        if (this.activeSpeakId === speakId) {
          this.fallbackSpeak(textToSpeak, lang, stepObj, speakId);
        }
      }, speakId);
      return;
    }

    // If no pre-recorded audio file (e.g. custom imported CAD), use dynamic TTS engine
    this.fallbackSpeak(textToSpeak, lang, stepObj, speakId);
  }

  // Play pre-recorded or dynamically fetched audio file with zero latency
  playVoiceAudioFile(audioUrl, spokenText, lang, onFallback, speakId = null) {
    if (speakId && this.activeSpeakId !== speakId) return;

    try {
      let audio = this.audioCache.get(audioUrl);
      if (!audio) {
        audio = new Audio();
        audio.preload = 'auto';
        audio.src = audioUrl;
        this.audioCache.set(audioUrl, audio);
      } else {
        try {
          audio.pause();
          audio.currentTime = 0;
        } catch {}
      }

      this.currentAudio = audio;
      this.notifySpeaking(true, lang, spokenText);

      audio.onended = () => {
        if (this.currentAudio === audio) {
          this.currentAudio = null;
        }
        this.notifySpeaking(false, lang);
      };

      audio.onerror = () => {
        if (this.currentAudio === audio) {
          this.currentAudio = null;
        }
        if (speakId && this.activeSpeakId !== speakId) return;
        if (onFallback) onFallback();
        else this.notifySpeaking(false, lang);
      };

      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch((err) => {
          console.warn('Audio play error, falling back:', err);
          if (this.currentAudio === audio) {
            this.currentAudio = null;
          }
          if (speakId && this.activeSpeakId !== speakId) return;
          if (onFallback) onFallback();
          else this.notifySpeaking(false, lang);
        });
      }
    } catch {
      if (speakId && this.activeSpeakId !== speakId) return;
      if (onFallback) onFallback();
    }
  }

  // Dynamic TTS streaming fallback for custom CAD models (Zero delay on production)
  fallbackSpeak(textToSpeak, lang, stepObj, speakId = null) {
    if (speakId && this.activeSpeakId !== speakId) return;

    const isLocal = typeof window !== 'undefined' && 
      (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

    if (isLocal) {
      // In local dev with Vite dev server, proxy handles /api/tts
      const ttsUrl = `/api/tts?ie=UTF-8&tl=${lang}&client=tw-ob&q=${encodeURIComponent(textToSpeak)}`;
      this.playVoiceAudioFile(ttsUrl, textToSpeak, lang, () => {
        if (!speakId || this.activeSpeakId === speakId) {
          this.synthesizeSpeech(textToSpeak, lang, stepObj, speakId);
        }
      }, speakId);
    } else {
      // In production static hosting (Render), /api/tts is not available.
      // Go directly to browser Web Speech Synthesis instantly!
      this.synthesizeSpeech(textToSpeak, lang, stepObj, speakId);
    }
  }

  // Browser Web Speech Synthesis fallback
  synthesizeSpeech(textToSpeak, lang, stepObj, speakId = null) {
    if (speakId && this.activeSpeakId !== speakId) return;
    if (!('speechSynthesis' in window)) {
      this.notifySpeaking(false, lang);
      return;
    }

    try {
      window.speechSynthesis.cancel();

      const voices = window.speechSynthesis.getVoices() || [];
      const langCodeMap = {
        en: 'en-US',
        ta: 'ta-IN',
        ml: 'ml-IN',
        hi: 'hi-IN'
      };
      const targetLangCode = langCodeMap[lang] || 'en-US';

      // Check if browser has a native voice for this language
      let matchingVoice = null;
      if (voices.length > 0) {
        matchingVoice = voices.find(v => v.lang && (
          v.lang.toLowerCase().startsWith(lang) ||
          v.lang.toLowerCase().replace('_', '-').startsWith(targetLangCode.toLowerCase())
        ));
      }

      let speechText = textToSpeak;
      let speechLang = targetLangCode;

      // If Windows/Browser has NO regional voice installed (e.g. only English Microsoft Zira/David),
      // Romanize the text phonetically so English voice can pronounce the Tamil/Malayalam/Hindi words clearly instead of silence!
      if (!matchingVoice && lang !== 'en') {
        matchingVoice = voices.find(v => v.lang.startsWith('en')) || voices[0] || null;
        speechLang = 'en-US';
        speechText = this.romanizePhonetics(textToSpeak, lang, stepObj);
      }

      const utterance = new SpeechSynthesisUtterance(speechText);
      utterance.lang = speechLang;
      utterance.rate = lang === 'ta' || lang === 'ml' ? 0.95 : 1.0;
      utterance.pitch = 1.0;
      if (matchingVoice) {
        utterance.voice = matchingVoice;
      }

      this.notifySpeaking(true, lang, textToSpeak);

      utterance.onend = () => {
        this.notifySpeaking(false, lang);
      };
      utterance.onerror = () => {
        this.notifySpeaking(false, lang);
      };

      window.speechSynthesis.speak(utterance);
    } catch {
      this.notifySpeaking(false, lang);
    }
  }

  // Romanized phonetics fallback for English voice engines (prevents silence on Windows)
  romanizePhonetics(text, lang, stepObj) {
    const stepNum = stepObj?.id || '1';
    const partName = stepObj?.partName || 'Component';
    const torqueVal = stepObj?.targetTorque || null;

    if (lang === 'ta') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `Padi ${stepNum}: ${partName} poruthavum. ${torqueVal} Newton meter torque-il irukkavum.`;
      }
      return `Padi ${stepNum}: ${partName} poruthavum. Seeraamaippai saripaarkkavum.`;
    }

    if (lang === 'ml') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `Ghattam ${stepNum}: ${partName} ghatikkuka. ${torqueVal} Newton meter torque-il murukkuka.`;
      }
      return `Ghattam ${stepNum}: ${partName} nannaayi ghatikkuka. Alignment parishodhikkuka.`;
    }

    if (lang === 'hi') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `Charan ${stepNum}: ${partName} ko sthaapit karein. ${torqueVal} Newton meter torque par kasein.`;
      }
      return `Charan ${stepNum}: ${partName} ko sthaapit karein. Sanrekhan ki jaanch karein.`;
    }

    return text;
  }

  // Universal real-time localization engine for any CAD import & system alerts
  localizeText(text, targetLang, stepObj = null) {
    if (!text) return '';

    // Standard system prompts
    if (text.includes('Assembly sequence successfully completed')) {
      if (targetLang === 'ta') return 'அசெம்பிளி செயல்முறை வெற்றிகரமாக முடிந்தது. அதிகாரப்பூர்வ ஐஎஸ்ஓ தரச் சான்றிதழ் உருவாக்கப்பட்டது.';
      if (targetLang === 'ml') return 'അസംബ്ലി പ്രക്രിയ വിജയകരമായി പൂർത്തിയായി. ഔദ്യോഗിക ഐഎസ്ഒ ഗുണനിലവാര സർട്ടിഫിക്കറ്റ് തയ്യാറാക്കി.';
      if (targetLang === 'hi') return 'असेंबली प्रक्रिया सफलतापूर्वक पूरी हुई। आधिकारिक आईएसओ गुणवत्ता प्रमाणपत्र तैयार किया गया।';
    }

    if (text.includes('Quality defect detected')) {
      if (targetLang === 'ta') return 'கூறு பிழை கண்டறியப்பட்டது. சிஎம்எம் மறுசீரமைப்புக்காக அசெம்பிளி வரிசை நிறுத்தப்பட்டது.';
      if (targetLang === 'ml') return 'ഘടകത്തിൽ പിശക് കണ്ടെത്തി. പുനഃക്രമീകരണത്തിനായി അസംബ്ലി ലൈൻ നിർത്തിവെച്ചു.';
      if (targetLang === 'hi') return 'घटक में दोष पाया गया। पुनः संरेखण के लिए असेंबली रोक दी गई है।';
    }

    if (text.includes('Geometric datum alignment verified')) {
      if (targetLang === 'ta') return 'வடிவியல் சீரமைப்பு ஐஎஸ்ஓ சகிப்புத்தன்மைக்குள் சரிபார்க்கப்பட்டது. அசெம்பிளி தொடர்கிறது.';
      if (targetLang === 'ml') return 'ജ്യാമിതീയ ക്രമീകരണം ഐഎസ്ഒ മാനദണ്ഡങ്ങൾക്ക് അനുസൃതമാണെന്ന് ഉറப்பുവരുത്തി. അസംബ്ലി പുനராരംഭിച്ചു.';
      if (targetLang === 'hi') return 'ज्यामितीय संरेखण आईएसओ मानक के अनुसार सत्यापित किया गया। असेंबली पुनः शुरू हुई।';
    }

    // Dynamic extraction for custom CAD models ("Step X: Mount ... Torque to ...")
    const stepMatch = text.match(/Step\s*(\d+)/i);
    const stepNum = stepMatch ? stepMatch[1] : (stepObj?.id || '1');
    const partName = stepObj?.partName || 'பாகம்';

    const torqueMatch = text.match(/Torque to\s*(\d+)\s*Newton meters/i);
    const torqueVal = torqueMatch ? torqueMatch[1] : (stepObj?.targetTorque || null);

    if (targetLang === 'ta') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `படி ${stepNum}: ${partName} பொருத்துங்கள். ${torqueVal} நியூட்டன் மீட்டர் முறுக்குவிசையில் இறுக்குங்கள்.`;
      }
      return `படி ${stepNum}: ${partName} பொருத்துங்கள். துல்லியமான சீரமைப்பை சரிபார்க்கவும்.`;
    }

    if (targetLang === 'ml') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `ഘട്ടം ${stepNum}: ${partName} ഘടിപ്പിക്കുക. ${torqueVal} ന്യൂട്ടൺ മീറ്റർ ടോർക്കിൽ മുറുക്കുക.`;
      }
      return `ഘട്ടം ${stepNum}: ${partName} കൃത്യമായി ഘടിപ്പിക്കുക. അലൈൻമെന്റ് പരിശോധിക്കുക.`;
    }

    if (targetLang === 'hi') {
      if (torqueVal && Number(torqueVal) > 0) {
        return `चरण ${stepNum}: ${partName} को स्थापित करें। ${torqueVal} न्यूटन मीटर टॉर्क पर कसें।`;
      }
      return `चरण ${stepNum}: ${partName} को स्थापित करें। सटीक संरेखण की जांच करें।`;
    }

    return text;
  }

  initContext() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  // Futuristic micro click
  playClick() {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1200, this.audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(400, this.audioCtx.currentTime + 0.04);
      gain.gain.setValueAtTime(0.12, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.04);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + 0.04);
    } catch {
      // Audio context error fallback
    }
  }

  // Mechanical torque wrench ratchet sound
  playTorqueClick(pitchMultiplier = 1.0) {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'triangle';
      const baseFreq = 850 * pitchMultiplier;
      osc.frequency.setValueAtTime(baseFreq, this.audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(120, this.audioCtx.currentTime + 0.035);
      gain.gain.setValueAtTime(0.2, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.035);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + 0.035);
    } catch {
      // Fallback
    }
  }

  // Pleasant success chime for step completion
  playSuccess() {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
      notes.forEach((freq, idx) => {
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + idx * 0.08);
        gain.gain.setValueAtTime(0.15, now + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.35);
        osc.connect(gain);
        gain.connect(this.audioCtx.destination);
        osc.start(now + idx * 0.08);
        osc.stop(now + idx * 0.08 + 0.35);
      });
    } catch {
      // Fallback
    }
  }

  // Defect / Warning siren
  playAlarm() {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(880, now);
      osc.frequency.setValueAtTime(440, now + 0.15);
      osc.frequency.setValueAtTime(880, now + 0.3);
      osc.frequency.setValueAtTime(440, now + 0.45);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.6);
    } catch {
      // Fallback
    }
  }

  // Authentic high-tech Zebra/Honeywell barcode scanner laser chirp
  playScannerBeep() {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(2450, now);
      osc.frequency.setValueAtTime(2600, now + 0.03);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch {}
  }

  // Industrial Poka-Yoke rejection buzzer
  playWrongBinBuzz() {
    if (!this.soundEnabled) return;
    try {
      this.initContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(160, now);
      osc.frequency.setValueAtTime(140, now + 0.12);
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch {}
  }
}

export const soundFx = new SoundController();

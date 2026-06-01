/**
 * TTS Client - Xu ly Text-to-Speech
 */

const axios = require('axios');

class TTSClient {
  constructor(apiKey = null, provider = 'google') {
    this.apiKey = apiKey || process.env.TTS_API_KEY;
    this.provider = provider; // 'google', 'azure', 'elevenlabs'
    this.cache = new Map();
    
    // Text normalization
    this.abbreviations = {
      'ko': 'khong',
      'dc': 'duoc',
      'mng': 'moi nguoi',
      'j': 'gi',
      'khum': 'khong',
      'k': 'khong',
      'tks': 'cam on',
      'thx': 'cam on',
      'ok': 'duoc'
    };
    
    this.emojiPattern = /[\u1F600-\u1F64F]|[\u1F300-\u1F5FF]|[\u1F680-\u1F6FF]|[\u1F1E0-\u1F1FF]/g;
  }

  /**
   * Normalize text before TTS
   */
  normalizeText(text) {
    // Remove emojis
    text = text.replace(this.emojiPattern, '');
    
    // Replace abbreviations
    for (const [abbr, full] of Object.entries(this.abbreviations)) {
      const regex = new RegExp(`\\b${abbr}\\b`, 'gi');
      text = text.replace(regex, full);
    }
    
    // Ensure punctuation
    if (!text.match(/[.!?]$/)) {
      text += '.';
    }
    
    return text;
  }

  /**
   * Generate speech
   */
  async generateSpeech(text, emotion = '[CUTE]', options = {}) {
    try {
      // Normalize text
      const normalizedText = this.normalizeText(text);
      
      // Check cache
      const cacheKey = `${normalizedText}_${emotion}`;
      if (this.cache.has(cacheKey)) {
        return this.cache.get(cacheKey);
      }
      
      // Get audio based on provider
      let audioUrl;
      
      if (this.provider === 'google') {
        audioUrl = await this._generateWithGoogle(normalizedText, emotion);
      } else if (this.provider === 'elevenlabs') {
        audioUrl = await this._generateWithElevenLabs(normalizedText, emotion);
      } else {
        audioUrl = await this._generateWithAzure(normalizedText, emotion);
      }
      
      // Cache result
      this.cache.set(cacheKey, audioUrl);
      
      return audioUrl;
    } catch (error) {
      console.error(`TTS generation error: ${error.message}`);
      // Return mock URL for demo
      return `mock://audio/${Date.now()}.wav`;
    }
  }

  /**
   * Generate with Google TTS
   */
  async _generateWithGoogle(text, emotion) {
    const voiceMap = {
      '[CUTE]': 'female-1',
      '[YANDERE]': 'female-2',
      '[TSUNDERE]': 'female-3',
      '[TROLL]': 'female-4',
      '[GENKI]': 'female-5',
      '[EXCITED]': 'female-1',
      '[COMFORT]': 'female-2',
      '[SERIOUS]': 'female-3'
    };
    
    // Mock implementation
    return `https://tts-mock.example.com/audio/${emotion.replace(/[\[\]]/g, '')}.wav`;
  }

  /**
   * Generate with ElevenLabs
   */
  async _generateWithElevenLabs(text, emotion) {
    // Mock implementation
    return `https://elevenlabs-mock.example.com/audio/${emotion.replace(/[\[\]]/g, '')}.mp3`;
  }

  /**
   * Generate with Azure
   */
  async _generateWithAzure(text, emotion) {
    // Mock implementation
    return `https://azure-tts-mock.example.com/audio/${emotion.replace(/[\[\]]/g, '')}.wav`;
  }

  /**
   * Create audio chunks from text
   */
  createAudioChunks(text) {
    const chunks = [];
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    
    let cumulativeTime = 0;
    
    for (const sentence of sentences) {
      const words = sentence.trim().split(/\s+/);
      const duration = words.length * 100; // 100ms per word estimate
      
      chunks.push({
        text: sentence.trim(),
        startTime: cumulativeTime,
        endTime: cumulativeTime + duration,
        wordCount: words.length
      });
      
      cumulativeTime += duration;
    }
    
    return chunks;
  }
}

module.exports = new TTSClient();

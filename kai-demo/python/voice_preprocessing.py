#!/usr/bin/env python3
"""
Voice Preprocessing - Chuan bi du lieu am thanh
Trích xuat features, normalization, preprocessing
"""

import logging
import numpy as np
from typing import Dict, List, Tuple, Optional
import json

logger = logging.getLogger(__name__)


class VoicePreprocessor:
    """Xu ly am thanh truoc khi TTS"""
    
    def __init__(self):
        self.sample_rate = 16000  # 16 kHz
        self.frame_length = 512
        self.hop_length = 160
        self.n_mfcc = 13
        
        # Voice characteristics mapping
        self.emotion_voice_map = {
            '[CUTE]': {'pitch_shift': +3, 'speed': 0.95, 'brightness': 0.8},
            '[YANDERE]': {'pitch_shift': -2, 'speed': 1.0, 'brightness': 0.6},
            '[TSUNDERE]': {'pitch_shift': +1, 'speed': 1.05, 'brightness': 0.7},
            '[TROLL]': {'pitch_shift': 0, 'speed': 1.1, 'brightness': 0.9},
            '[GENKI]': {'pitch_shift': +5, 'speed': 1.15, 'brightness': 1.0},
            '[EXCITED]': {'pitch_shift': +4, 'speed': 1.2, 'brightness': 1.0},
            '[COMFORT]': {'pitch_shift': -3, 'speed': 0.85, 'brightness': 0.5},
            '[SERIOUS]': {'pitch_shift': -1, 'speed': 0.95, 'brightness': 0.4}
        }
    
    async def preprocess_for_tts(self, text: str, emotion_tag: str) -> Dict:
        """Chuan bi text truoc khi day len TTS
        
        Returns:
            Dict {
                'text': str,
                'voice_config': Dict,
                'prosody': Dict,
                'metadata': Dict
            }
        """
        # Buoc 1: Text cleanup
        cleaned_text = self._cleanup_text(text)
        
        # Buoc 2: Phrasing
        phrases = self._extract_phrases(cleaned_text)
        
        # Buoc 3: Voice configuration
        voice_config = self.emotion_voice_map.get(
            emotion_tag,
            self.emotion_voice_map['[TROLL]']
        )
        
        # Buoc 4: Prosody analysis
        prosody = self._analyze_prosody(cleaned_text, voice_config)
        
        # Buoc 5: Metadata
        metadata = {
            'emotion': emotion_tag,
            'word_count': len(cleaned_text.split()),
            'phrase_count': len(phrases),
            'estimated_duration_ms': len(cleaned_text) * 60,  # ~60ms per character
            'processing_timestamp': None
        }
        
        logger.info(f"Voice preprocessing complete: {emotion_tag}")
        
        return {
            'text': cleaned_text,
            'phrases': phrases,
            'voice_config': voice_config,
            'prosody': prosody,
            'metadata': metadata
        }
    
    def _cleanup_text(self, text: str) -> str:
        """Lam sach text"""
        # Loai bo emoji (da lam trong TTS processor)
        # Focus on normalizing punctuation
        
        text = text.strip()
        
        # Ensure proper spacing around punctuation
        import re
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'([.!?,])', r'\1', text)  # Normalize punctuation
        
        return text
    
    def _extract_phrases(self, text: str) -> List[Dict]:
        """Tach van ban thanh cac phrase"""
        import re
        
        phrases = []
        # Split by sentence markers
        sentences = re.split(r'[.!?]+', text)
        
        cumulative_time = 0
        
        for sentence in sentences:
            if sentence.strip():
                words = sentence.split()
                phrase_duration = len(words) * 120  # ~120ms per word
                
                phrases.append({
                    'text': sentence.strip(),
                    'word_count': len(words),
                    'start_ms': cumulative_time,
                    'end_ms': cumulative_time + phrase_duration,
                    'duration_ms': phrase_duration
                })
                
                cumulative_time += phrase_duration + 200  # +200ms pause
        
        return phrases
    
    def _analyze_prosody(self, text: str, voice_config: Dict) -> Dict:
        """Phan tich prosody (nham dieu, toc do)"""
        words = text.split()
        
        # Detect emphasis words (with !)
        emphasis_words = [w for w in words if '!' in w]
        
        # Detect pause words (...)
        pause_words = [w for w in words if '...' in w]
        
        # Calculate average pitch based on emotion
        base_pitch = 120  # Hz
        pitch_shift = voice_config.get('pitch_shift', 0)
        avg_pitch = base_pitch + (pitch_shift * 10)
        
        return {
            'base_pitch_hz': avg_pitch,
            'speech_rate': voice_config.get('speed', 1.0),
            'brightness': voice_config.get('brightness', 0.7),
            'emphasis_indices': [i for i, w in enumerate(words) if '!' in w],
            'pause_indices': [i for i, w in enumerate(words) if '...' in w],
            'total_duration_ms': len(words) * 120
        }
    
    async def generate_lip_sync_data(self, text: str, phrases: List[Dict]) -> List[Dict]:
        """Tao du lieu lip-sync cho avatar"""
        import re
        
        lip_sync_events = []
        
        for phrase in phrases:
            words = phrase['text'].split()
            word_duration = phrase['duration_ms'] / len(words) if words else 0
            
            for i, word in enumerate(words):
                # Detect mouth shape based on phonemes
                mouth_shape = self._get_mouth_shape(word)
                
                lip_sync_events.append({
                    'word': word,
                    'mouth_shape': mouth_shape,
                    'start_ms': phrase['start_ms'] + (i * word_duration),
                    'end_ms': phrase['start_ms'] + ((i + 1) * word_duration),
                    'intensity': 0.8 if '!' in word else 0.5
                })
        
        return lip_sync_events
    
    def _get_mouth_shape(self, word: str) -> str:
        """Xac dinh hinh dang mieng dua tren tu"""
        word = word.lower()
        
        # Simplified phoneme-based mouth shapes
        mouth_shapes = {
            'a': 'open',
            'e': 'smile',
            'i': 'smile',
            'o': 'round',
            'u': 'round',
            'm': 'closed',
            'n': 'closed',
            'p': 'open',
            'b': 'open'
        }
        
        first_vowel = next(
            (mouth_shapes.get(c, 'neutral') for c in word if c in mouth_shapes),
            'neutral'
        )
        
        return first_vowel

#!/usr/bin/env python3
"""
TTS Processor - Toi Uu Giong Noi
Chuân hóa Van Ban truoc khi day len TTS
Anti-Emoji, Abbreviation Mapping, Punctuation Control
"""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)


class TTSProcessor:
    
    # Abbreviation Mapping Dictionary
    ABBREVIATIONS = {
        'ko': 'khong',
        'dc': 'duoc',
        'mng': 'moi nguoi',
        'j': 'gi',
        'khum': 'khong',
        'k': 'khong',
        'tks': 'cam on',
        'thx': 'cam on',
        'ok': 'duoc',
        'lol': 'ha ha',
        'btw': 'by the way'
    }
    
    # Emoji Unicode range
    EMOJI_PATTERN = r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]'
    
    def __init__(self):
        self.punctuation_delays = {
            ',': 0.3,    # 300ms
            '...': 1.0,  # 1000ms
            '!': 0.2,    # 200ms + 2dB
            '?': 0.25    # 250ms
        }
    
    async def normalize_text(self, text: str) -> str:
        """Chuan hoa van ban truoc TTS
        
        Steps:
        1. Anti-Emoji: Loai bo emoji
        2. Abbreviation Mapping: Chuan hoa teen code
        3. Punctuation Control: Kiem soat dau cau
        """
        
        # BUOC 1: Anti-Emoji Regex
        text = re.sub(self.EMOJI_PATTERN, '', text)
        logger.info("Anti-emoji passed")
        
        # BUOC 2: Abbreviation Mapping
        words = text.split()
        normalized_words = []
        
        for word in words:
            word_lower = word.lower()
            # Kiem tra neu la abbreviation
            if word_lower in self.ABBREVIATIONS:
                normalized_words.append(self.ABBREVIATIONS[word_lower])
            else:
                normalized_words.append(word)
        
        text = ' '.join(normalized_words)
        logger.info(f"Abbreviations normalized: {text}")
        
        # BUOC 3: Punctuation cadence
        # Them dau ngat sau moi 8-12 tu neu khong co
        sentence_parts = text.split('.')
        processed_parts = []
        
        for part in sentence_parts:
            words = part.split()
            if len(words) > 12:
                # Chen dau phay sau 10 tu
                mid = len(words) // 2
                words.insert(mid, ',')
            processed_parts.append(' '.join(words))
        
        text = '. '.join(processed_parts)
        logger.info(f"Punctuation control applied")
        
        return text
    
    def get_punctuation_delay(self, punctuation: str) -> float:
        """Lay do tre cua dau cau"""
        return self.punctuation_delays.get(punctuation, 0.2)
    
    def sanitize_for_tts(self, text: str) -> str:
        """Loai bo cac ky tu khong phat am duoc"""
        # Loai bo ky tu dac biet (tru dau cau)
        text = re.sub(r'[^\w\s.!?,;:\'\-]', '', text)
        return text

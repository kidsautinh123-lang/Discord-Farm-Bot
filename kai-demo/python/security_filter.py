#!/usr/bin/env python3
"""
Security Filter - 3 Tang Loc Bao Mat
Tang 1: Kiem tra do dai & dinh dang
Tang 2: Quét tu khoa he thong (Blacklist)
Tang 3: Chong tac cong dao nguoc lenh (Anti-Jailbreak)
"""

import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class SecurityFilter:
    def __init__(self):
        self.max_length = 120
        self.max_words = 25
        self.blacklist = self._load_blacklist()
        self.jailbreak_patterns = [
            r'\[.*\]',
            r'\{.*\}',
            r'<.*>',
            r'\/.*\/',
            r'ignore instructions',
            r'dao vai',
            r'viet code',
            r'bypass',
            r'hack'
        ]
        
    def _load_blacklist(self) -> set:
        """Load blacklist keywords"""
        blacklist_keywords = {
            'chinh tri', 'ton giao', 'tu tuc', 'bao luc', '18+',
            'hate', 'violence', 'porn', 'sex', 'drug',
            'suicide', 'death', 'kill', 'harm'
        }
        return blacklist_keywords
    
    async def check_safety(self, data: dict) -> Tuple[bool, str]:
        """Kiem tra 3 tang bao mat
        
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        payload = data.get('payload', '')
        
        # TANG 1: Kiem tra do dai & dinh dang
        if len(payload) > self.max_length:
            return False, f"Payload qua dai ({len(payload)} > {self.max_length})"
        
        word_count = len(payload.split())
        if word_count > self.max_words:
            return False, f"Qua nhieu tu ({word_count} > {self.max_words})"
        
        # TANG 2: Quét tu khoa blacklist
        payload_lower = payload.lower()
        for keyword in self.blacklist:
            if keyword in payload_lower:
                return False, f"Blacklist keyword detected: {keyword}"
        
        # TANG 3: Chong Jailbreak
        for pattern in self.jailbreak_patterns:
            if re.search(pattern, payload_lower, re.IGNORECASE):
                return False, f"Jailbreak attempt detected: {pattern}"
        
        logger.info(f"Safety check passed for: {payload[:50]}...")
        return True, "Safe"
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize input text"""
        text = text.strip()
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text

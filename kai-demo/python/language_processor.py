#!/usr/bin/env python3
"""
Multi-Language Support - Ho tro da ngon ngu
Viet, English, Chinese, Japanese, Korean
"""

import logging
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class Language(Enum):
    """Cac ngon ngu ho tro"""
    VIETNAMESE = "vi"
    ENGLISH = "en"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_TRADITIONAL = "zh-TW"
    JAPANESE = "ja"
    KOREAN = "ko"


class LanguageProcessor:
    """Xu ly da ngon ngu"""
    
    def __init__(self):
        self.current_language = Language.VIETNAMESE
        
        # Translation dictionary - Tien hanh chi can
        self.translations = {
            Language.VIETNAMESE: {
                'greeting': 'Chao ban',
                'goodbye': 'Tam biet',
                'thank_you': 'Cam on',
                'sorry': 'Xin loi',
                'yes': 'Vang',
                'no': 'Khong'
            },
            Language.ENGLISH: {
                'greeting': 'Hello',
                'goodbye': 'Goodbye',
                'thank_you': 'Thank you',
                'sorry': 'Sorry',
                'yes': 'Yes',
                'no': 'No'
            },
            Language.CHINESE_SIMPLIFIED: {
                'greeting': '你好',
                'goodbye': '再见',
                'thank_you': '谢谢',
                'sorry': '对不起',
                'yes': '是的',
                'no': '不'
            },
            Language.JAPANESE: {
                'greeting': 'こんにちは',
                'goodbye': 'さようなら',
                'thank_you': 'ありがとう',
                'sorry': 'ごめんなさい',
                'yes': 'はい',
                'no': 'いいえ'
            },
            Language.KOREAN: {
                'greeting': '안녕하세요',
                'goodbye': '안녕히 가세요',
                'thank_you': '감사합니다',
                'sorry': '죄송합니다',
                'yes': '네',
                'no': '아니요'
            }
        }
        
        # TTS voice configs per language
        self.tts_voice_config = {
            Language.VIETNAMESE: {
                'voice_id': 'vi-VN-NhanNeural',
                'pitch': 0,
                'rate': 1.0
            },
            Language.ENGLISH: {
                'voice_id': 'en-US-AvaNeural',
                'pitch': 0,
                'rate': 1.0
            },
            Language.CHINESE_SIMPLIFIED: {
                'voice_id': 'zh-CN-XiaoxiaoNeural',
                'pitch': 0,
                'rate': 1.0
            },
            Language.JAPANESE: {
                'voice_id': 'ja-JP-NanamiNeural',
                'pitch': 0,
                'rate': 1.0
            },
            Language.KOREAN: {
                'voice_id': 'ko-KR-SunHiNeural',
                'pitch': 0,
                'rate': 1.0
            }
        }
    
    async def detect_language(self, text: str) -> Language:
        """Phat hien ngon ngu cua text"""
        # Simple detection based on characters
        
        if any('\u4e00' <= c <= '\u9fff' for c in text):  # Chinese
            return Language.CHINESE_SIMPLIFIED
        elif any('\u3040' <= c <= '\u309f' for c in text):  # Hiragana
            return Language.JAPANESE
        elif any('\uac00' <= c <= '\ud7af' for c in text):  # Hangul
            return Language.KOREAN
        elif any('\u00e0' <= c <= '\u00ff' or c in 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ' for c in text.lower()):
            return Language.VIETNAMESE
        else:
            return Language.ENGLISH  # Default
    
    async def translate_text(self, text: str, source_lang: Language,
                            target_lang: Language) -> str:
        """Dich van ban giua cac ngon ngu
        
        Mock implementation - trong thuc te dung API nhu Google Translate
        """
        
        if source_lang == target_lang:
            return text
        
        logger.info(f"Translating from {source_lang.value} to {target_lang.value}")
        
        # Mock translation - trong thuc te goi API
        mock_translation = f"[{target_lang.value}] {text}"
        return mock_translation
    
    def set_language(self, language: Language):
        """Thay doi ngon ngu hien tai"""
        self.current_language = language
        logger.info(f"Language set to: {language.value}")
    
    def get_translation(self, key: str) -> str:
        """Lay ban dich cua mot key"""
        return self.translations.get(
            self.current_language, {}
        ).get(key, key)
    
    def get_tts_config(self, language: Language = None) -> Dict:
        """Lay config TTS cho ngon ngu"""
        lang = language or self.current_language
        return self.tts_voice_config.get(lang, {})
    
    async def prepare_for_tts(self, text: str, emotion_tag: str) -> Dict:
        """Chuan bi text cho TTS voi language support"""
        # Detect language
        detected_lang = await self.detect_language(text)
        
        # Get TTS config
        tts_config = self.get_tts_config(detected_lang)
        
        # Add emotion-specific adjustments
        emotion_adjustments = {
            '[EXCITED]': {'rate': 1.2, 'pitch': 5},
            '[COMFORT]': {'rate': 0.85, 'pitch': -5},
            '[SERIOUS]': {'rate': 0.95, 'pitch': 0}
        }
        
        adjustments = emotion_adjustments.get(emotion_tag, {})
        
        # Merge configs
        final_config = {**tts_config, **adjustments}
        
        return {
            'text': text,
            'language': detected_lang.value,
            'voice_id': final_config.get('voice_id'),
            'pitch': final_config.get('pitch', 0),
            'rate': final_config.get('rate', 1.0),
            'emotion': emotion_tag
        }

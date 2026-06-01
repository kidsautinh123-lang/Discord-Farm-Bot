#!/usr/bin/env python3
"""
LLM Router - Dinh Tuyen Lai Giua Local va Cloud LLM
Local: Xu ly cac yeu cau don gian, phuc tap < 200ms
Cloud: Xu ly logic cao, gift, khoa hoc
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMRouter:
    
    # Tu khoa kich hoat Local LLM
    LOCAL_KEYWORDS = [
        'trau', 'tan tinh', 'ru choi', 'giao tiep',
        'chat', 'hello', 'hi', 'ban khoe'
    ]
    
    # Tu khoa kich hoat Cloud LLM
    CLOUD_KEYWORDS = [
        'khoa hoc', 'hoc thuat', 'logic', 'xu ly',
        'van de', 'giai quyet', 'tu van'
    ]
    
    def __init__(self):
        self.local_latency_max = 0.2  # 200ms
        self.cloud_failover_timeout = 2.0  # 2s
    
    async def route_and_generate(self, payload: str, emotion_tag: str, 
                                  user_name: str, platform: str) -> str:
        """Dinh tuyen va sinh phan hoi
        
        Args:
            payload: noi dung tin nhan
            emotion_tag: [TAG] cam xuc
            user_name: ten user
            platform: TikTok hoac YouTube
        
        Returns:
            Generated response
        """
        payload_lower = payload.lower()
        
        # Kiem tra routing
        use_local = self._should_use_local(payload_lower, emotion_tag)
        
        if use_local:
            logger.info("Routing to Local LLM")
            return await self._generate_local(payload, emotion_tag, user_name)
        else:
            logger.info("Routing to Cloud LLM")
            return await self._generate_cloud(payload, emotion_tag, user_name)
    
    def _should_use_local(self, payload_lower: str, emotion_tag: str) -> bool:
        """Quet tu khoa de quyet dinh routing"""
        # Check cloud keywords first
        for keyword in self.CLOUD_KEYWORDS:
            if keyword in payload_lower:
                return False
        
        # Check local keywords
        for keyword in self.LOCAL_KEYWORDS:
            if keyword in payload_lower:
                return True
        
        # Mac dinh: neu co [EXCITED] hay SERIOUS thi dung Cloud
        if '[EXCITED]' in emotion_tag or '[SERIOUS]' in emotion_tag:
            return False
        
        return True
    
    async def _generate_local(self, payload: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Local LLM"""
        # Danh gia: Tao response don gian
        responses = {
            '[CUTE]': f'Cam on {user_name} tran qua, em thich lam :)',
            '[YANDERE]': f'{user_name}... anh chi co em la khong?',
            '[TSUNDERE]': f'K... kem chi khong? Thua cai',
            '[TROLL]': f'Hihi, {user_name} ngau the',
            '[GENKI]': f'Yay! {user_name} choi game cung em!',
            '[COMFORT]': f'Co em day, {user_name} khong buon nha',
            '[SERIOUS]': f'Dung {user_name}, dieu nay rat quan trong',
            '[EXCITED]': f'Thank you {user_name}! Em rat cam on!'
        }
        
        return responses.get(emotion_tag, f'Em hieu {user_name} roi')
    
    async def _generate_cloud(self, payload: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Cloud LLM (Gemini)"""
        # Mock response tu Cloud LLM
        logger.info(f"Calling Cloud LLM (Gemini) for: {payload[:50]}...")
        
        cloud_response = (
            f"[{emotion_tag[1:-1]}] Phan hoi chi tiet tu Cloud LLM cho: "
            f"{user_name} - {payload}"
        )
        
        return cloud_response

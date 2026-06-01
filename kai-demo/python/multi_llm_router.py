#!/usr/bin/env python3
"""
Multi-LLM Router - Chay song song nhieu mo hinh LLM
Gemini 2.0, Claude 3, Local LLaMA, GPT-4o Mini, Mistral
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class LLMProviderType(Enum):
    """Loai nha cung cap LLM"""
    GEMINI_2_FLASH = "gemini-2.0-flash"
    CLAUDE_3 = "claude-3-opus"
    LOCAL_LLAMA = "local-llama-7b"
    GPT_4O_MINI = "gpt-4o-mini"
    MISTRAL = "mistral-7b"


@dataclass
class LLMResponse:
    """Ket qua tu mot LLM"""
    provider: LLMProviderType
    content: str
    latency_ms: float
    quality_score: float
    tokens_used: int
    error: Optional[str] = None
    is_cached: bool = False


@dataclass
class MultiLLMResult:
    """Ket qua cuoi cung tu nhieu LLM"""
    best_response: str
    best_provider: LLMProviderType
    all_responses: List[LLMResponse]
    total_latency_ms: float
    consensus_score: float
    recommended_emotion_tag: str


class MultiLLMRouter:
    """Router chay nhieu LLM song song"""
    
    def __init__(self):
        self.providers = {
            LLMProviderType.GEMINI_2_FLASH: GeminiProvider(),
            LLMProviderType.CLAUDE_3: ClaudeProvider(),
            LLMProviderType.LOCAL_LLAMA: LocalLlamaProvider(),
            LLMProviderType.GPT_4O_MINI: GPTProvider(),
            LLMProviderType.MISTRAL: MistralProvider()
        }
        
        # Priority ranking
        self.priority = {
            LLMProviderType.GEMINI_2_FLASH: 1,
            LLMProviderType.CLAUDE_3: 2,
            LLMProviderType.LOCAL_LLAMA: 3,
            LLMProviderType.GPT_4O_MINI: 4,
            LLMProviderType.MISTRAL: 5
        }
        
        self.response_cache = {}
        self.cache_ttl = 3600  # 1 gio
    
    async def generate_parallel(self, prompt: str, emotion_tag: str, 
                                user_name: str, platform: str) -> MultiLLMResult:
        """Chay nhieu LLM song song
        
        Args:
            prompt: Noi dung can sinh
            emotion_tag: [TAG] cam xuc
            user_name: Ten user
            platform: TikTok / YouTube
        
        Returns:
            MultiLLMResult voi tat ca cac phan hoi
        """
        start_time = time.time()
        
        # Tao cache key
        cache_key = f"{prompt}_{emotion_tag}_{platform}"
        
        # Kiem tra cache
        if cache_key in self.response_cache:
            cached_result = self.response_cache[cache_key]
            if time.time() - cached_result['timestamp'] < self.cache_ttl:
                logger.info(f"Cache hit: {cache_key[:50]}...")
                return cached_result['result']
        
        # Chay tat ca LLM song song
        tasks = []
        for provider_type, provider in self.providers.items():
            task = self._call_llm_with_timeout(
                provider=provider,
                provider_type=provider_type,
                prompt=prompt,
                emotion_tag=emotion_tag,
                user_name=user_name
            )
            tasks.append(task)
        
        # Chay song song
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Xu ly ket qua
        valid_responses = []
        for resp in responses:
            if isinstance(resp, LLMResponse):
                valid_responses.append(resp)
            else:
                logger.error(f"LLM call failed: {resp}")
        
        # Tinh total latency
        total_latency = (time.time() - start_time) * 1000
        
        # Chon phan hoi tot nhat
        best_response = self._select_best_response(valid_responses, emotion_tag)
        
        # Tinh consensus score
        consensus = self._calculate_consensus(valid_responses)
        
        # Tao ket qua
        result = MultiLLMResult(
            best_response=best_response.content,
            best_provider=best_response.provider,
            all_responses=valid_responses,
            total_latency_ms=total_latency,
            consensus_score=consensus,
            recommended_emotion_tag=emotion_tag
        )
        
        # Luu cache
        self.response_cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
        
        logger.info(f"Multi-LLM generation complete. Best: {best_response.provider.value}")
        return result
    
    async def _call_llm_with_timeout(self, provider, provider_type: LLMProviderType,
                                      prompt: str, emotion_tag: str, user_name: str) -> LLMResponse:
        """Goi LLM voi timeout"""
        try:
            start_time = time.time()
            
            content = await asyncio.wait_for(
                provider.generate(prompt, emotion_tag, user_name),
                timeout=5.0
            )
            
            latency = (time.time() - start_time) * 1000
            
            return LLMResponse(
                provider=provider_type,
                content=content,
                latency_ms=latency,
                quality_score=await self._score_response(content, emotion_tag),
                tokens_used=len(content.split())
            )
        except asyncio.TimeoutError:
            logger.warning(f"Timeout: {provider_type.value}")
            return LLMResponse(
                provider=provider_type,
                content="",
                latency_ms=5000,
                quality_score=0.0,
                tokens_used=0,
                error="Timeout"
            )
        except Exception as e:
            logger.error(f"LLM error {provider_type.value}: {str(e)}")
            return LLMResponse(
                provider=provider_type,
                content="",
                latency_ms=0,
                quality_score=0.0,
                tokens_used=0,
                error=str(e)
            )
    
    def _select_best_response(self, responses: List[LLMResponse], 
                               emotion_tag: str) -> LLMResponse:
        """Chon phan hoi tot nhat"""
        # Filter valid responses
        valid = [r for r in responses if r.content and not r.error]
        
        if not valid:
            # Neu khong co response hop le, tra ve response nhanh nhat
            return min(responses, key=lambda r: r.latency_ms)
        
        # Score dua tren: quality, latency, priority
        scores = []
        for resp in valid:
            score = (
                resp.quality_score * 0.5 +  # Quality 50%
                (1 - min(resp.latency_ms / 5000, 1)) * 0.3 +  # Speed 30%
                (1 / self.priority[resp.provider]) * 0.2  # Priority 20%
            )
            scores.append((score, resp))
        
        # Tra ve response co score cao nhat
        return max(scores, key=lambda x: x[0])[1]
    
    def _calculate_consensus(self, responses: List[LLMResponse]) -> float:
        """Tinh do dong thuan giua cac LLM"""
        valid_responses = [r for r in responses if r.content and not r.error]
        
        if len(valid_responses) < 2:
            return 1.0 if valid_responses else 0.0
        
        # Tinh similarity giua cac response
        total_similarity = 0
        comparisons = 0
        
        for i, resp1 in enumerate(valid_responses):
            for resp2 in valid_responses[i+1:]:
                similarity = self._calculate_similarity(
                    resp1.content,
                    resp2.content
                )
                total_similarity += similarity
                comparisons += 1
        
        if comparisons == 0:
            return 0.5
        
        return total_similarity / comparisons
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Tinh do tuong tu giua 2 van ban"""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    async def _score_response(self, content: str, emotion_tag: str) -> float:
        """Cham diem chat luong response"""
        score = 0.5  # Base score
        
        # Bo sung neu co ten
        if "[NAME]" in content:
            score += 0.1
        
        # Bo sung neu co dau ngat
        if any(p in content for p in ['.', ',', '!', '?']):
            score += 0.1
        
        # Bo sung neu co buffer word
        if any(word in content.lower() for word in ['nha', 'ne', 'um', 'haha']):
            score += 0.1
        
        # Bo sung theo emotion tag
        if emotion_tag in content or emotion_tag.replace('[', '').replace(']', '') in content:
            score += 0.2
        
        return min(score, 1.0)


class GeminiProvider:
    """Gemini 2.0 Flash - Xu ly logic cao, khoa hoc"""
    
    async def generate(self, prompt: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Gemini"""
        # Mock implementation - trong thuc te goi API Gemini
        await asyncio.sleep(0.3)  # Simulate latency
        
        response = f"[{emotion_tag[1:-1]}] Gemini response: Dieu nay rat quan trong - {prompt[:50]}. Em se gup {user_name} giai quyet van de nay."
        return response


class ClaudeProvider:
    """Claude 3 - Creative writing, cam xuc sau"""
    
    async def generate(self, prompt: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Claude"""
        await asyncio.sleep(0.4)  # Simulate latency
        
        response = f"[{emotion_tag[1:-1]}] Claude phan hoi: {user_name} a, em hieu cam xuc cua anh. {prompt[:40]}... Em luon ben canh anh nhe."
        return response


class LocalLlamaProvider:
    """Local LLaMA - Chat nhanh, thả thính"""
    
    async def generate(self, prompt: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Local LLaMA"""
        await asyncio.sleep(0.15)  # Nhanh nhat
        
        response = f"[{emotion_tag[1:-1]}] {user_name} dep trai qua nha! {prompt}... Hihi :)"
        return response


class GPTProvider:
    """GPT-4o Mini - Xu ly tinh huong phuc tap"""
    
    async def generate(self, prompt: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang GPT-4o Mini"""
        await asyncio.sleep(0.35)  # Simulate latency
        
        response = f"[{emotion_tag[1:-1]}] GPT phan hoi: Chao {user_name}, em phan tich van de: {prompt[:50]}... Diem de xuat: ..."
        return response


class MistralProvider:
    """Mistral - Du phong, backup"""
    
    async def generate(self, prompt: str, emotion_tag: str, user_name: str) -> str:
        """Sinh phan hoi bang Mistral"""
        await asyncio.sleep(0.32)  # Simulate latency
        
        response = f"[{emotion_tag[1:-1]}] Mistral: {user_name} em hieu roi. {prompt}. Hanh dong: ..."
        return response

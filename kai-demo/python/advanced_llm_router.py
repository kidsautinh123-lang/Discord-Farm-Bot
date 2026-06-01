#!/usr/bin/env python3
"""
Advanced LLM Router - Tich hop Multi-LLM va Context Learning
Chay nhieu mo hinh LLM song song voi context va learning
"""

import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime

from multi_llm_router import MultiLLMRouter, MultiLLMResult
from context_learning import ContextLearner

logger = logging.getLogger(__name__)


class AdvancedLLMRouter:
    """Router LLM nang cao - Multi-model + Learning"""
    
    def __init__(self):
        self.multi_llm = MultiLLMRouter()
        self.context_learner = ContextLearner(max_context_window=20)
        self.performance_metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'average_latency_ms': 0
        }
    
    async def generate_intelligent_response(self, payload: str, emotion_tag: str,
                                            user_name: str, platform: str) -> Dict:
        """Sinh phan hoi thong minh bang nhieu LLM
        
        Returns:
            Dict {
                'response': str,
                'provider': str,
                'emotion': str,
                'latency_ms': float,
                'quality_score': float,
                'consensus': float,
                'all_provider_responses': list
            }
        """
        self.performance_metrics['total_requests'] += 1
        
        # Predicted emotion tu context learning
        predicted_emotion = self.context_learner.predict_emotion(user_name, payload)
        
        # Neu khong co emotion, dung predicted
        if emotion_tag == '[TROLL]':
            emotion_tag = predicted_emotion
        
        logger.info(f"Predicted emotion: {predicted_emotion}")
        
        # Tao enhanced prompt voi context
        enhanced_prompt = self.context_learner.get_ai_prompt_enhancement(
            user_name,
            payload
        )
        
        logger.info(f"Enhanced prompt length: {len(enhanced_prompt)} chars")
        
        # Chay nhieu LLM song parallel
        multi_result = await self.multi_llm.generate_parallel(
            prompt=enhanced_prompt,
            emotion_tag=emotion_tag,
            user_name=user_name,
            platform=platform
        )
        
        # Luu vao context learning
        self.context_learner.add_interaction({
            'user_name': user_name,
            'platform': platform,
            'payload': payload,
            'emotion_tag': emotion_tag,
            'response': multi_result.best_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Cap nhat metrics
        self.performance_metrics['average_latency_ms'] = (
            (self.performance_metrics['average_latency_ms'] * 
             (self.performance_metrics['total_requests'] - 1) +
             multi_result.total_latency_ms) /
            self.performance_metrics['total_requests']
        )
        
        # Chuan bi output
        return {
            'response': multi_result.best_response,
            'provider': multi_result.best_provider.value,
            'emotion': emotion_tag,
            'latency_ms': multi_result.total_latency_ms,
            'quality_score': multi_result.all_responses[0].quality_score 
                if multi_result.all_responses else 0.5,
            'consensus': multi_result.consensus_score,
            'user_summary': self.context_learner.get_user_summary(user_name),
            'all_provider_responses': [
                {
                    'provider': r.provider.value,
                    'content': r.content[:100] + '...' if len(r.content) > 100 else r.content,
                    'latency_ms': r.latency_ms,
                    'quality': r.quality_score,
                    'error': r.error
                }
                for r in multi_result.all_responses
            ]
        }
    
    def get_performance_stats(self) -> Dict:
        """Lay thong ke hieu nang"""
        return {
            'metrics': self.performance_metrics,
            'total_users': len(self.context_learner.user_preferences),
            'emotional_distribution': self.context_learner.emotional_patterns,
            'context_window_size': len(self.context_learner.context_window)
        }
    
    def get_user_analytics(self, user_name: str) -> Dict:
        """Lay analytics chi tiet ve user"""
        return self.context_learner.get_user_summary(user_name)

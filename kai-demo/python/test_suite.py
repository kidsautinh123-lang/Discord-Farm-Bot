#!/usr/bin/env python3
"""
Testing Suite - Unit Tests va Integration Tests
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Import modules to test
from multi_llm_router import MultiLLMRouter, LLMProviderType
from context_learning import ContextLearner
from sentiment_analyzer import SentimentAnalyzer, SentimentScore, MoodType
from error_handling import CircuitBreaker, RetryStrategy, FallbackHandler


class TestMultiLLMRouter:
    """Test Multi-LLM Router"""
    
    @pytest.fixture
    def router(self):
        return MultiLLMRouter()
    
    @pytest.mark.asyncio
    async def test_generate_parallel(self, router):
        """Test parallel LLM generation"""
        result = await router.generate_parallel(
            prompt="Xin chao",
            emotion_tag="[CUTE]",
            user_name="test_user",
            platform="TikTok"
        )
        
        assert result.best_response is not None
        assert result.best_provider is not None
        assert result.total_latency_ms > 0
        assert result.consensus_score >= 0
    
    @pytest.mark.asyncio
    async def test_response_quality_scoring(self, router):
        """Test response quality scoring"""
        score = await router._score_response(
            "[CUTE] Em rat vui nha!",
            "[CUTE]"
        )
        
        assert score > 0.5
        assert score <= 1.0


class TestContextLearner:
    """Test Context Learning"""
    
    @pytest.fixture
    def learner(self):
        return ContextLearner()
    
    def test_add_interaction(self, learner):
        """Test adding interaction"""
        learner.add_interaction({
            'user_name': 'user1',
            'platform': 'TikTok',
            'payload': 'Em yeu anh',
            'emotion_tag': '[YANDERE]',
            'response': 'Anh cung yeu em'
        })
        
        assert len(learner.context_window) == 1
        assert learner.user_preferences['user1']['interaction_count'] == 1
    
    def test_predict_emotion(self, learner):
        """Test emotion prediction"""
        learner.add_interaction({
            'user_name': 'user1',
            'platform': 'TikTok',
            'payload': 'Em yeu anh',
            'emotion_tag': '[YANDERE]',
            'response': 'Anh cung yeu em'
        })
        
        predicted = learner.predict_emotion('user1', 'Em yeu anh rat nhieu')
        assert predicted == '[YANDERE]'


class TestSentimentAnalyzer:
    """Test Sentiment Analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        return SentimentAnalyzer()
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment(self, analyzer):
        """Test sentiment analysis"""
        # Positive sentiment
        sentiment, confidence = await analyzer.analyze_sentiment("Em yeu anh rat nhieu")
        assert sentiment == SentimentScore.VERY_POSITIVE or sentiment == SentimentScore.POSITIVE
        
        # Negative sentiment
        sentiment, confidence = await analyzer.analyze_sentiment("Em ghet dieu nay")
        assert sentiment == SentimentScore.VERY_NEGATIVE or sentiment == SentimentScore.NEGATIVE
    
    @pytest.mark.asyncio
    async def test_detect_mood(self, analyzer):
        """Test mood detection"""
        mood, intensity = await analyzer.detect_mood("Hahahaha!!!")
        assert mood == MoodType.EXCITED
        assert intensity > 0


class TestErrorHandling:
    """Test Error Handling"""
    
    @pytest.mark.asyncio
    async def test_circuit_breaker(self):
        """Test circuit breaker"""
        cb = CircuitBreaker(failure_threshold=2)
        
        async def failing_func():
            raise Exception("Test error")
        
        # First failure
        with pytest.raises(Exception):
            await cb.call(failing_func)
        
        assert cb.failure_count == 1
    
    @pytest.mark.asyncio
    async def test_retry_strategy(self):
        """Test retry strategy"""
        retry = RetryStrategy(max_retries=2, base_delay_ms=10)
        
        call_count = 0
        async def sometimes_failing():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Fail")
            return "Success"
        
        result = await retry.execute(sometimes_failing)
        assert result == "Success"
        assert call_count == 2
    
    @pytest.mark.asyncio
    async def test_fallback_handler(self):
        """Test fallback handler"""
        handler = FallbackHandler()
        
        async def primary():
            raise Exception("Primary failed")
        
        async def fallback():
            return "Fallback success"
        
        handler.add_fallback(fallback)
        
        result = await handler.execute(primary)
        assert result == "Fallback success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
Real-Time Sentiment Analysis - Phat hien cam xuc, tinh trang, du doan trang thai
"""

import logging
from typing import Dict, Tuple, Optional, List
from enum import Enum
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class SentimentScore(Enum):
    """Diem sentiment"""
    VERY_NEGATIVE = -2.0
    NEGATIVE = -1.0
    NEUTRAL = 0.0
    POSITIVE = 1.0
    VERY_POSITIVE = 2.0


class MoodType(Enum):
    """Loai tinh trang"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    CALM = "calm"
    EXCITED = "excited"
    CONFUSED = "confused"


class SentimentAnalyzer:
    """Phan tich sentiment va tinh trang real-time"""
    
    def __init__(self):
        # Positive words
        self.positive_words = {
            'yeu': 2.0, 'dep': 1.5, 'xinh': 1.5, 'tot': 1.0,
            'tuyyet': 2.0, 'tuyet': 2.0, 'super': 1.5, 'awesome': 1.5,
            'cam on': 1.0, 'vui': 1.5, 'hanh phuc': 2.0, 'hanh phuc': 2.0
        }
        
        # Negative words
        self.negative_words = {
            'ghet': -2.0, 'tuc': -1.5, 'dang': -1.0, 'khong': -0.5,
            'xau': -1.5, 'toi': -1.0, 'buon': -1.5, 'af': -1.0,
            'khong the': -1.5, 'that hoa': -1.0
        }
        
        # Emotional indicators
        self.emotional_patterns = {
            r'\.\.\.$': {'intensity': 0.8, 'type': 'hesitation'},
            r'!!!+': {'intensity': 2.0, 'type': 'excitement'},
            r'\?\?+': {'intensity': 1.5, 'type': 'confusion'},
            r'haha|hihi|hehe': {'intensity': 1.5, 'type': 'happiness'},
            r':(': {'intensity': -1.5, 'type': 'sadness'},
            r':\)': {'intensity': 1.0, 'type': 'happiness'}
        }
        
        # Mood history
        self.mood_history: List[Dict] = []
        self.sentiment_history: List[Dict] = []
    
    async def analyze_sentiment(self, text: str) -> Tuple[SentimentScore, float]:
        """Phan tich sentiment cua text
        
        Returns:
            (sentiment_score, confidence)
        """
        text_lower = text.lower()
        
        # Calculate base sentiment
        positive_score = 0
        negative_score = 0
        
        # Check positive words
        for word, score in self.positive_words.items():
            if word in text_lower:
                positive_score += score
        
        # Check negative words
        for word, score in self.negative_words.items():
            if word in text_lower:
                negative_score += abs(score)
        
        # Calculate net sentiment
        net_sentiment = positive_score - negative_score
        
        # Normalize
        if net_sentiment > 1.5:
            sentiment = SentimentScore.VERY_POSITIVE
        elif net_sentiment > 0.5:
            sentiment = SentimentScore.POSITIVE
        elif net_sentiment < -1.5:
            sentiment = SentimentScore.VERY_NEGATIVE
        elif net_sentiment < -0.5:
            sentiment = SentimentScore.NEGATIVE
        else:
            sentiment = SentimentScore.NEUTRAL
        
        # Calculate confidence
        confidence = min(abs(net_sentiment) / 5.0, 1.0)
        
        logger.info(f"Sentiment: {sentiment.name} (confidence: {confidence:.2f})")
        
        return sentiment, confidence
    
    async def detect_mood(self, text: str) -> Tuple[MoodType, float]:
        """Phat hien tinh trang cua user
        
        Returns:
            (mood_type, intensity)
        """
        text_lower = text.lower()
        
        max_intensity = 0
        detected_mood = MoodType.CALM
        
        # Check emotional patterns
        for pattern, info in self.emotional_patterns.items():
            if re.search(pattern, text_lower):
                intensity = info['intensity']
                
                if abs(intensity) > max_intensity:
                    max_intensity = abs(intensity)
                    
                    pattern_type = info['type']
                    if pattern_type == 'excitement':
                        detected_mood = MoodType.EXCITED
                    elif pattern_type == 'confusion':
                        detected_mood = MoodType.CONFUSED
                    elif pattern_type == 'sadness':
                        detected_mood = MoodType.SAD
                    elif pattern_type == 'happiness':
                        detected_mood = MoodType.HAPPY
        
        # Normalize intensity
        intensity = min(max_intensity / 2.0, 1.0)
        
        logger.info(f"Mood: {detected_mood.value} (intensity: {intensity:.2f})")
        
        return detected_mood, intensity
    
    async def predict_emotional_state(self, user_name: str, 
                                       recent_texts: List[str]) -> Dict:
        """Du doan tinh trang cam xuc cua user
        
        Returns:
            Dict {
                'current_state': str,
                'trend': str,
                'risk_level': str,
                'recommendation': str
            }
        """
        
        if not recent_texts:
            return {
                'current_state': 'unknown',
                'trend': 'unknown',
                'risk_level': 'low',
                'recommendation': 'Need more data'
            }
        
        # Analyze latest text
        latest_sentiment, latest_confidence = await self.analyze_sentiment(
            recent_texts[-1]
        )
        latest_mood, latest_intensity = await self.detect_mood(recent_texts[-1])
        
        # Analyze trend (last 3-5 texts)
        sentiment_scores = []
        for text in recent_texts[-5:]:
            sentiment, _ = await self.analyze_sentiment(text)
            sentiment_scores.append(sentiment.value)
        
        # Calculate trend
        if len(sentiment_scores) >= 2:
            trend_diff = sentiment_scores[-1] - sentiment_scores[0]
            if trend_diff > 0.5:
                trend = "improving"
            elif trend_diff < -0.5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "unknown"
        
        # Detect risk (very negative or very anxious)
        risk_level = "low"
        if latest_sentiment in [SentimentScore.VERY_NEGATIVE, SentimentScore.NEGATIVE]:
            risk_level = "high"
        elif latest_mood in [MoodType.ANXIOUS, MoodType.ANGRY]:
            risk_level = "medium"
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            latest_mood, latest_sentiment, risk_level
        )
        
        state_data = {
            'user_name': user_name,
            'current_state': latest_mood.value,
            'current_sentiment': latest_sentiment.name,
            'trend': trend,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }
        
        self.mood_history.append(state_data)
        
        logger.info(f"Emotional state prediction: {state_data['current_state']}")
        
        return state_data
    
    def _generate_recommendation(self, mood: MoodType, 
                                 sentiment: SentimentScore,
                                 risk_level: str) -> str:
        """Tao goi y dua tren tinh trang"""
        
        if risk_level == "high":
            return f"Em cam thay {mood.value} qua, em se an ui va ho tro anh nha!"
        elif mood == MoodType.EXCITED:
            return f"Wow! Anh rat vui thinz! Em cung vui theo!"
        elif mood == MoodType.CONFUSED:
            return f"Anh co bit khong hieu dieu gi khong? Em giup anh giai dap nha!"
        elif mood == MoodType.CALM:
            return f"Anh tinh trang binh yen, em thich dieu nay!"
        else:
            return f"Em luon ben canh anh, chung ta se vua qua!"
    
    def get_mood_report(self, user_name: str, days: int = 7) -> Dict:
        """Lay bao cao tinh trang trong thoi gian"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        relevant_history = [
            item for item in self.mood_history
            if item['user_name'] == user_name and
            datetime.fromisoformat(item['timestamp']) > cutoff_date
        ]
        
        if not relevant_history:
            return {'user_name': user_name, 'data': []}
        
        return {
            'user_name': user_name,
            'period_days': days,
            'total_interactions': len(relevant_history),
            'mood_distribution': self._calculate_distribution(relevant_history),
            'sentiment_trend': self._calculate_trend(relevant_history),
            'latest_state': relevant_history[-1]
        }
    
    def _calculate_distribution(self, history: List[Dict]) -> Dict:
        """Tinh phan bo tinh trang"""
        distribution = {}
        for item in history:
            mood = item['current_state']
            distribution[mood] = distribution.get(mood, 0) + 1
        return distribution
    
    def _calculate_trend(self, history: List[Dict]) -> str:
        """Tinh xu huong sentiment"""
        if len(history) < 2:
            return "insufficient_data"
        
        sentiments = [item['current_sentiment'] for item in history]
        first_sentiment = SentimentScore[sentiments[0]].value
        last_sentiment = SentimentScore[sentiments[-1]].value
        
        diff = last_sentiment - first_sentiment
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        else:
            return "stable"

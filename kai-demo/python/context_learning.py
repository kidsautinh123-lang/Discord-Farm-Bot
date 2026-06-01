#!/usr/bin/env python3
"""
Context Learning - Hoc va nho cac tac dong truoc
Tang tin hieu cua LLM theo thoi gian
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class ContextLearner:
    """Hoc tu context cua nguoi dung"""
    
    def __init__(self, max_context_window: int = 10):
        self.context_window = []  # Luu 10 tac dong truoc
        self.max_window = max_context_window
        self.user_preferences = {}  # Tuy chinh ca nhan
        self.emotional_patterns = {}  # Sac thai cam xuc
        self.interaction_history = []  # Lich su tac dong
    
    def add_interaction(self, data: Dict):
        """Them tac dong vao context
        
        Args:
            data: {
                'user_name': str,
                'platform': str,
                'payload': str,
                'emotion_tag': str,
                'response': str,
                'timestamp': str
            }
        """
        interaction = {
            **data,
            'added_at': datetime.now().isoformat()
        }
        
        self.context_window.append(interaction)
        self.interaction_history.append(interaction)
        
        # Giu chi toi max_window
        if len(self.context_window) > self.max_window:
            self.context_window.pop(0)
        
        # Cap nhat user preferences
        self._update_user_preferences(data.get('user_name', 'unknown'), data)
        
        # Cap nhat emotional patterns
        self._update_emotional_patterns(data.get('emotion_tag', 'NEUTRAL'))
        
        logger.info(f"Context added: {data.get('user_name')}")
    
    def get_context_prompt(self, user_name: str = None) -> str:
        """Lay context de them vao prompt cho LLM"""
        context_text = "\n=== CONTEXT WINDOW ===\n"
        
        # Recent interactions
        for i, interaction in enumerate(self.context_window[-5:]):
            context_text += f"[{i+1}] {interaction['user_name']}: {interaction['payload'][:50]}...\n"
            context_text += f"    Response: {interaction['response'][:50]}...\n"
        
        # User-specific preferences
        if user_name and user_name in self.user_preferences:
            prefs = self.user_preferences[user_name]
            context_text += f"\n=== USER PREFERENCES ({user_name}) ===\n"
            context_text += f"Favorite Emotion: {prefs.get('favorite_emotion', 'UNKNOWN')}\n"
            context_text += f"Platform: {prefs.get('preferred_platform', 'UNKNOWN')}\n"
            context_text += f"Interaction Count: {prefs.get('interaction_count', 0)}\n"
        
        # Emotional trends
        context_text += f"\n=== EMOTIONAL TRENDS ===\n"
        for emotion, count in sorted(
            self.emotional_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]:
            context_text += f"{emotion}: {count} times\n"
        
        return context_text
    
    def _update_user_preferences(self, user_name: str, data: Dict):
        """Cap nhat tuy chinh ca nhan cua user"""
        if user_name not in self.user_preferences:
            self.user_preferences[user_name] = {
                'interaction_count': 0,
                'favorite_emotion': None,
                'preferred_platform': None,
                'keywords': [],
                'response_preferences': []
            }
        
        prefs = self.user_preferences[user_name]
        prefs['interaction_count'] += 1
        prefs['preferred_platform'] = data.get('platform', prefs['preferred_platform'])
        
        # Update favorite emotion
        emotion = data.get('emotion_tag', 'NEUTRAL')
        if not prefs['favorite_emotion']:
            prefs['favorite_emotion'] = emotion
        else:
            # Weighted average
            if emotion == prefs['favorite_emotion']:
                pass  # Keep current
            else:
                # Change if this emotion appears more
                pass
        
        # Extract keywords from payload
        keywords = data.get('payload', '').lower().split()
        prefs['keywords'].extend([k for k in keywords if len(k) > 3])
        prefs['keywords'] = list(set(prefs['keywords']))[:20]  # Keep top 20
        
        logger.debug(f"User preferences updated: {user_name}")
    
    def _update_emotional_patterns(self, emotion_tag: str):
        """Cap nhat so lan xuat hien cua moi cam xuc"""
        emotion = emotion_tag.replace('[', '').replace(']', '')
        
        if emotion not in self.emotional_patterns:
            self.emotional_patterns[emotion] = 0
        
        self.emotional_patterns[emotion] += 1
        logger.debug(f"Emotional pattern updated: {emotion}")
    
    def get_user_summary(self, user_name: str) -> Dict:
        """Lay tom tat ve user"""
        if user_name not in self.user_preferences:
            return {}
        
        prefs = self.user_preferences[user_name]
        
        return {
            'user_name': user_name,
            'total_interactions': prefs['interaction_count'],
            'favorite_emotion': prefs['favorite_emotion'],
            'preferred_platform': prefs['preferred_platform'],
            'top_keywords': prefs['keywords'][:5],
            'last_interaction': (
                self.interaction_history[-1]
                if self.interaction_history and 
                self.interaction_history[-1]['user_name'] == user_name
                else None
            )
        }
    
    def predict_emotion(self, user_name: str, payload: str) -> str:
        """Du doan cam xuc cua user dua tren lich su"""
        if user_name not in self.user_preferences:
            return "[TROLL]"  # Default
        
        prefs = self.user_preferences[user_name]
        keywords = payload.lower().split()
        
        # Neu co keyword tuong tu, dung emotion truoc
        user_keywords = prefs['keywords']
        if any(kw in user_keywords for kw in keywords if len(kw) > 3):
            return prefs['favorite_emotion'] or "[TROLL]"
        
        return prefs['favorite_emotion'] or "[TROLL]"
    
    def get_ai_prompt_enhancement(self, user_name: str, base_prompt: str) -> str:
        """Tang cuong prompt bang context learning"""
        enhancement = self.get_context_prompt(user_name)
        
        enhanced_prompt = f"{base_prompt}\n\n{enhancement}"
        
        return enhanced_prompt

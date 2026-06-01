#!/usr/bin/env python3
"""
Rate Limiting va API Key Management
"""

import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class RateLimitTier(Enum):
    """Cac tier rate limiting"""
    FREE = {'requests_per_minute': 10, 'requests_per_day': 1000}
    PRO = {'requests_per_minute': 100, 'requests_per_day': 100000}
    ENTERPRISE = {'requests_per_minute': 1000, 'requests_per_day': 10000000}


class RateLimiter:
    """Rate limiting per user"""
    
    def __init__(self):
        self.user_quotas: Dict[str, Dict] = {}
        self.request_history: Dict[str, list] = {}
    
    def add_user(self, user_id: str, tier: RateLimitTier = RateLimitTier.FREE):
        """Them user voi tier"""
        limits = tier.value
        
        self.user_quotas[user_id] = {
            'tier': tier.name,
            'per_minute': limits['requests_per_minute'],
            'per_day': limits['requests_per_day'],
            'requests_used_today': 0,
            'reset_time': datetime.now() + timedelta(days=1)
        }
        
        self.request_history[user_id] = []
        logger.info(f"User added: {user_id} (tier: {tier.name})")
    
    def check_rate_limit(self, user_id: str) -> tuple[bool, Optional[str]]:
        """Kiem tra xem user co vuot rate limit khong
        
        Returns:
            (is_allowed, error_message)
        """
        if user_id not in self.user_quotas:
            return False, "User not found"
        
        quota = self.user_quotas[user_id]
        
        # Reset if needed
        if datetime.now() > quota['reset_time']:
            quota['requests_used_today'] = 0
            quota['reset_time'] = datetime.now() + timedelta(days=1)
        
        # Check per-day limit
        if quota['requests_used_today'] >= quota['per_day']:
            return False, f"Daily limit exceeded ({quota['per_day']})"
        
        # Check per-minute limit
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        recent_requests = [
            ts for ts in self.request_history[user_id]
            if ts > one_minute_ago
        ]
        
        if len(recent_requests) >= quota['per_minute']:
            return False, f"Per-minute limit exceeded ({quota['per_minute']})"
        
        # Increment counters
        quota['requests_used_today'] += 1
        self.request_history[user_id].append(now)
        
        return True, None
    
    def get_quota_status(self, user_id: str) -> Dict:
        """Lay trang thai quota cua user"""
        if user_id not in self.user_quotas:
            return {}
        
        quota = self.user_quotas[user_id]
        
        return {
            'tier': quota['tier'],
            'requests_used_today': quota['requests_used_today'],
            'daily_limit': quota['per_day'],
            'remaining_today': quota['per_day'] - quota['requests_used_today'],
            'reset_time': quota['reset_time'].isoformat()
        }


class APIKeyManager:
    """Quan ly API keys"""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict] = {}
    
    def generate_api_key(self, user_id: str) -> str:
        """Tao API key cho user"""
        import uuid
        
        api_key = str(uuid.uuid4())
        
        self.api_keys[api_key] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'is_active': True
        }
        
        logger.info(f"API key generated for {user_id}")
        return api_key
    
    def validate_api_key(self, api_key: str) -> tuple[bool, Optional[str]]:
        """Kiem tra API key co hop le khong
        
        Returns:
            (is_valid, user_id)
        """
        if api_key not in self.api_keys:
            return False, None
        
        key_data = self.api_keys[api_key]
        
        if not key_data['is_active']:
            return False, None
        
        # Update last_used
        key_data['last_used'] = datetime.now().isoformat()
        
        return True, key_data['user_id']
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Thu hoi API key"""
        if api_key in self.api_keys:
            self.api_keys[api_key]['is_active'] = False
            logger.info(f"API key revoked: {api_key}")
            return True
        return False
    
    def get_key_info(self, api_key: str) -> Optional[Dict]:
        """Lay info cua API key"""
        return self.api_keys.get(api_key)

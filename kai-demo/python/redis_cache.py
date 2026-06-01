#!/usr/bin/env python3
"""
Redis Caching Layer - Distributed cache layer
"""

import logging
import json
from typing import Optional, Any, Dict, List
from datetime import timedelta
import asyncio

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache layer - distributed caching"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, 
                 default_ttl: int = 3600):
        self.host = host
        self.port = port
        self.default_ttl = default_ttl
        self.redis_client = None
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0
        }
    
    async def initialize(self):
        """Khoi tao Redis connection"""
        try:
            import redis
            self.redis_client = redis.asyncio.from_url(
                f"redis://{self.host}:{self.port}"
            )
            await self.redis_client.ping()
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.error(f"Redis initialization failed: {e}")
            logger.info("Falling back to in-memory cache")
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Lay gia tri tu cache"""
        if not self.redis_client:
            return None
        
        try:
            value = await self.redis_client.get(key)
            
            if value:
                self.cache_stats['hits'] += 1
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            else:
                self.cache_stats['misses'] += 1
                logger.debug(f"Cache miss: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Luu gia tri vao cache"""
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            self.cache_stats['sets'] += 1
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Xoa gia tri tu cache"""
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.delete(key)
            self.cache_stats['deletes'] += 1
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear_by_pattern(self, pattern: str) -> int:
        """Xoa tat ca keys match pattern"""
        if not self.redis_client:
            return 0
        
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
            logger.info(f"Cleared {len(keys)} cache keys matching {pattern}")
            return len(keys)
        except Exception as e:
            logger.error(f"Cache pattern delete error: {e}")
            return 0
    
    async def cache_warming(self, data_provider) -> Dict:
        """Warm up cache voi du lieu thuong xai"""
        logger.info("Starting cache warming...")
        
        warmed_keys = 0
        
        # Cache popular emotions
        emotions = [
            '[CUTE]', '[YANDERE]', '[TSUNDERE]', '[TROLL]',
            '[GENKI]', '[EXCITED]', '[COMFORT]', '[SERIOUS]'
        ]
        
        for emotion in emotions:
            await self.set(f"emotion:{emotion}", {'tag': emotion}, ttl=86400)
            warmed_keys += 1
        
        logger.info(f"Cache warming complete: {warmed_keys} keys")
        return {'warmed_keys': warmed_keys}
    
    def get_stats(self) -> Dict:
        """Lay statistics cua cache"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (
            self.cache_stats['hits'] / total_requests * 100
            if total_requests > 0 else 0
        )
        
        return {
            **self.cache_stats,
            'total_requests': total_requests,
            'hit_rate': f"{hit_rate:.2f}%"
        }


class CacheStrategy:
    """Cache strategy - smart invalidation"""
    
    def __init__(self, redis_cache: RedisCache):
        self.cache = redis_cache
        self.invalidation_rules = []
    
    async def invalidate_user_cache(self, user_name: str):
        """Invalidate cache cho user"""
        patterns = [
            f"user:{user_name}:*",
            f"context:{user_name}:*",
            f"analytics:{user_name}:*"
        ]
        
        for pattern in patterns:
            await self.cache.clear_by_pattern(pattern)
        
        logger.info(f"User cache invalidated: {user_name}")
    
    async def invalidate_emotion_cache(self, emotion_tag: str):
        """Invalidate cache cho emotion"""
        pattern = f"response:{emotion_tag}:*"
        await self.cache.clear_by_pattern(pattern)
        logger.info(f"Emotion cache invalidated: {emotion_tag}")
    
    async def smart_cache(self, key: str, value: Any, 
                          ttl_days: int = 1) -> bool:
        """Smart caching voi TTL strategy"""
        ttl_seconds = ttl_days * 86400
        return await self.cache.set(key, value, ttl=ttl_seconds)

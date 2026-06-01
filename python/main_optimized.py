#!/usr/bin/env python3
"""
Main Optimized Version - Phiên bản chính tối ưu
Sử dụng tất cả các module tối ưu hóa
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import os

from security_filter import SecurityFilter
from llm_router import LLMRouter
from emotion_tagger import EmotionTagger
from tts_processor import TTSProcessor
from memory_manager import MemoryManager
from anti_desync import AntiDesyncProtocol
from redis_cache import RedisCache
from monitoring import MonitoringEngine
from advanced_logger import AdvancedLogger

# ============= Logging Setup =============
logger = AdvancedLogger(__name__)

# ============= Data Classes =============
@dataclass
class ProcessingMetrics:
    """Lưu trữ metrics xử lý"""
    total_processed: int = 0
    total_blocked: int = 0
    avg_latency: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    errors: int = 0
    emotion_distribution: Dict[str, int] = field(default_factory=dict)
    platform_stats: Dict[str, int] = field(default_factory=dict)


class KaiDemoSystemOptimized:
    """Hệ thống KAI tối ưu hóa hoàn toàn"""
    
    def __init__(self):
        """Khởi tạo hệ thống với tất cả tính năng tối ưu"""
        
        # ============= Queue Setup =============
        self.input_queue = asyncio.Queue(maxsize=2000)
        self.output_queue = asyncio.Queue(maxsize=1000)
        self.priority_queue = asyncio.PriorityQueue(maxsize=500)
        
        # ============= Core Modules =============
        self.security_filter = SecurityFilter()
        self.llm_router = LLMRouter()
        self.emotion_tagger = EmotionTagger()
        self.tts_processor = TTSProcessor()
        self.memory_manager = MemoryManager()
        self.anti_desync = AntiDesyncProtocol()
        
        # ============= Optimization Modules =============
        self.redis_cache = RedisCache()
        self.monitoring = MonitoringEngine()
        self.metrics = ProcessingMetrics()
        
        # ============= Runtime State =============
        self.is_running = False
        self.cooldown_period = 2.5
        self.last_output_time = 0
        self.start_time = time.time()
        
        # ============= Configuration =============
        self.cache_ttl = int(os.getenv('CACHE_TTL', 3600))
        self.batch_size = int(os.getenv('BATCH_SIZE', 10))
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.enable_cache = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
        self.enable_monitoring = os.getenv('ENABLE_MONITORING', 'true').lower() == 'true'
        
        logger.info(f"🚀 KAI System Optimized initialized")
        logger.info(f"📋 Config: cache_ttl={self.cache_ttl}s, batch_size={self.batch_size}, max_retries={self.max_retries}")
    
    # ============= Initialization =============
    
    async def initialize(self):
        """Khởi tạo tất cả modules"""
        logger.info('🚀 Initializing KAI Demo System (Optimized)...')
        
        try:
            # Khởi tạo Database
            await self.memory_manager.initialize()
            logger.info('✅ Memory Manager initialized')
            
            # Khởi tạo Redis Cache
            if self.enable_cache:
                await self.redis_cache.connect()
                logger.info('✅ Redis Cache connected')
            
            # Khởi tạo Monitoring
            if self.enable_monitoring:
                await self.monitoring.start()
                logger.info('✅ Monitoring Engine started')
            
            logger.info('✅ System ready!')
            
        except Exception as e:
            logger.error(f"❌ Initialization failed: {str(e)}", exc_info=True)
            raise
    
    # ============= Input Management =============
    
    async def add_input(self, data: Dict, priority: int = 0):
        """Thêm dữ liệu vào hàng đợi với priority"""
        try:
            data['received_at'] = time.time()
            
            if priority > 0:
                await self.priority_queue.put((priority, data))
                logger.debug(f"Priority input from {data['platform']} added (priority={priority})")
            else:
                await self.input_queue.put(data)
                logger.debug(f"Input from {data['platform']} added to queue")
                
        except asyncio.QueueFull:
            logger.warning(f"⚠️ Input queue full, dropping data from {data.get('platform', 'unknown')}")
            self.metrics.errors += 1
    
    async def _get_next_input(self) -> Optional[Dict]:
        """Lấy input tiếp theo (ưu tiên priority queue)"""
        try:
            if not self.priority_queue.empty():
                _, data = self.priority_queue.get_nowait()
                return data
            
            return await asyncio.wait_for(self.input_queue.get(), timeout=0.5)
        except asyncio.TimeoutError:
            return None
        except asyncio.QueueEmpty:
            return None
    
    # ============= Cache Management =============
    
    async def _get_cached_response(self, cache_key: str) -> Optional[Dict]:
        """Lấy phản hồi từ cache"""
        if not self.enable_cache:
            return None
        
        try:
            cached_data = await self.redis_cache.get(cache_key)
            if cached_data:
                self.metrics.cache_hits += 1
                logger.debug(f"🎯 Cache hit: {cache_key}")
                return cached_data
            
            self.metrics.cache_misses += 1
            return None
        except Exception as e:
            logger.error(f"Cache retrieval error: {str(e)}")
            return None
    
    async def _set_cache(self, cache_key: str, data: Dict, ttl: Optional[int] = None):
        """Lưu trữ dữ liệu vào cache"""
        if not self.enable_cache:
            return
        
        try:
            ttl = ttl or self.cache_ttl
            await self.redis_cache.set(cache_key, data, ttl=ttl)
            logger.debug(f"💾 Cached: {cache_key} (TTL={ttl}s)")
        except Exception as e:
            logger.error(f"Cache storage error: {str(e)}")
    
    def _generate_cache_key(self, payload: str, emotion: str) -> str:
        """Tạo cache key từ payload và emotion"""
        import hashlib
        key_source = f"{payload.lower()}:{emotion}"
        hash_key = hashlib.md5(key_source.encode()).hexdigest()
        return f"kai:response:{hash_key}"
    
    # ============= Security & Validation =============
    
    async def _check_safety_with_retry(self, data: Dict) -> tuple:
        """Kiểm tra bảo mật với retry logic"""
        for attempt in range(self.max_retries):
            try:
                is_safe, reason = await self.security_filter.check_safety(data)
                return is_safe, reason
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Security check failed after {self.max_retries} attempts: {str(e)}")
                    return False, f"Security check error: {str(e)}"
                await asyncio.sleep(0.1 * (attempt + 1))
        
        return False, "Security check failed"
    
    # ============= Processing Pipeline =============
    
    async def process_pipeline(self):
        """Pipeline xử lý chính với tất cả tối ưu hóa"""
        logger.info("🔄 Starting processing pipeline...")
        
        while self.is_running:
            start_time = time.time()
            
            try:
                # 1. Lấy input
                input_data = await self._get_next_input()
                if not input_data:
                    await asyncio.sleep(0.1)
                    continue
                
                logger.info(f"📥 Processing: {input_data['payload'][:50]}...")
                
                # 2. Kiểm tra bảo mật
                is_safe, reason = await self._check_safety_with_retry(input_data)
                if not is_safe:
                    logger.warning(f"🚫 Blocked: {reason}")
                    self.metrics.total_blocked += 1
                    continue
                
                # 3. Gắn thẻ cảm xúc
                emotion_tag = await self.emotion_tagger.tag_emotion(
                    input_data['payload'],
                    input_data.get('type', 'chat')
                )
                logger.info(f"🎭 Emotion: {emotion_tag}")
                
                self.metrics.emotion_distribution[emotion_tag] = \
                    self.metrics.emotion_distribution.get(emotion_tag, 0) + 1
                
                # 4. Cache key
                cache_key = self._generate_cache_key(input_data['payload'], emotion_tag)
                
                # 5. Kiểm tra cache
                cached_llm_response = await self._get_cached_response(cache_key)
                
                if cached_llm_response:
                    llm_response = cached_llm_response
                    logger.info("✨ Using cached response")
                else:
                    # 6. LLM Response
                    llm_response = await self.llm_router.route_and_generate(
                        payload=input_data['payload'],
                        emotion_tag=emotion_tag,
                        user_name=input_data['user_raw_name'],
                        platform=input_data['platform']
                    )
                    
                    await self._set_cache(cache_key, llm_response)
                
                # 7. Chuẩn hóa text
                normalized_text = await self.tts_processor.normalize_text(llm_response)
                
                # 8. Audio chunks
                audio_chunks = await self.anti_desync.prepare_chunks(
                    text=normalized_text,
                    emotion_tag=emotion_tag
                )
                
                # 9. Lưu DB
                await self.memory_manager.save_interaction({
                    'platform': input_data['platform'],
                    'emotion_tag': emotion_tag,
                    'content': llm_response,
                    'user_name': input_data['user_raw_name'],
                    'timestamp': datetime.now().isoformat()
                })
                
                # 10. Output
                output_data = {
                    'emotion_tag': emotion_tag,
                    'text': normalized_text,
                    'audio_chunks': audio_chunks,
                    'user_name': input_data['user_raw_name'],
                    'platform': input_data['platform'],
                    'timestamp': datetime.now().isoformat()
                }
                
                # 11. Cooldown
                await self._apply_cooldown()
                
                # 12. Output queue
                try:
                    self.output_queue.put_nowait(output_data)
                    logger.info('✅ Output pushed')
                    self.metrics.total_processed += 1
                except asyncio.QueueFull:
                    logger.warning('⚠️ Output queue full')
                    self.metrics.errors += 1
                
                # 13. Metrics
                processing_time = time.time() - start_time
                self.metrics.avg_latency = (
                    (self.metrics.avg_latency * (self.metrics.total_processed - 1) + processing_time) 
                    / max(1, self.metrics.total_processed)
                )
                
                platform = input_data.get('platform', 'unknown')
                self.metrics.platform_stats[platform] = \
                    self.metrics.platform_stats.get(platform, 0) + 1
                
                # Log metrics định kỳ
                if self.metrics.total_processed % 10 == 0:
                    logger.log_metrics({
                        'processed': self.metrics.total_processed,
                        'blocked': self.metrics.total_blocked,
                        'latency': f"{self.metrics.avg_latency:.3f}s",
                        'cache_hit_rate': f"{(self.metrics.cache_hits / max(1, self.metrics.cache_hits + self.metrics.cache_misses) * 100):.1f}%"
                    })
                
            except asyncio.TimeoutError:
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"❌ Pipeline error: {str(e)}", exc_info=True)
                self.metrics.errors += 1
                await asyncio.sleep(0.5)
    
    # ============= Cooldown =============
    
    async def _apply_cooldown(self):
        """Áp dụng cooldown"""
        elapsed = time.time() - self.last_output_time
        if elapsed < self.cooldown_period:
            wait_time = self.cooldown_period - elapsed
            await asyncio.sleep(wait_time)
        self.last_output_time = time.time()
    
    # ============= Output =============
    
    async def get_output(self) -> Optional[Dict]:
        """Lấy output"""
        try:
            return self.output_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    # ============= Metrics =============
    
    def get_metrics(self) -> Dict:
        """Lấy metrics"""
        uptime = time.time() - self.start_time
        return {
            'status': 'running' if self.is_running else 'stopped',
            'uptime': f"{uptime:.1f}s",
            'processed': self.metrics.total_processed,
            'blocked': self.metrics.total_blocked,
            'latency': f"{self.metrics.avg_latency:.3f}s",
            'cache_hits': self.metrics.cache_hits,
            'cache_hit_rate': f"{(self.metrics.cache_hits / max(1, self.metrics.cache_hits + self.metrics.cache_misses) * 100):.1f}%",
            'errors': self.metrics.errors,
            'emotions': self.metrics.emotion_distribution,
            'platforms': self.metrics.platform_stats
        }
    
    # ============= Shutdown =============
    
    async def shutdown(self):
        """Dừng hệ thống"""
        logger.info("🛑 Shutting down...")
        self.is_running = False
        
        try:
            if self.enable_cache:
                await self.redis_cache.close()
            await self.memory_manager.close()
            if self.enable_monitoring:
                await self.monitoring.stop()
            
            logger.info("✅ Shutdown complete")
            logger.info(f"📊 Final metrics: {json.dumps(self.get_metrics(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            logger.error(f"❌ Shutdown error: {str(e)}")
    
    async def run(self):
        """Chạy hệ thống"""
        self.is_running = True
        await self.initialize()
        
        try:
            await self.process_pipeline()
        except KeyboardInterrupt:
            logger.info('⌨️ Keyboard interrupt')
        finally:
            await self.shutdown()


async def main():
    """Main"""
    system = KaiDemoSystemOptimized()
    
    run_task = asyncio.create_task(system.run())
    
    test_data = {
        'platform': 'TikTok',
        'user_raw_name': 'user123',
        'payload': 'Em yeu anh rat nhieu nha',
        'type': 'chat'
    }
    
    await asyncio.sleep(2)
    await system.add_input(test_data)
    await asyncio.sleep(60)
    
    system.is_running = False
    
    try:
        await asyncio.wait_for(run_task, timeout=10)
    except asyncio.TimeoutError:
        run_task.cancel()


if __name__ == '__main__':
    asyncio.run(main())

#!/usr/bin/env python3
"""
KAI-DEMO: Main System Orchestrator
He thong dieu phoi chinh xu ly luong du lieu tu nhieu nen tang
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

from security_filter import SecurityFilter
from llm_router import LLMRouter
from emotion_tagger import EmotionTagger
from tts_processor import TTSProcessor
from memory_manager import MemoryManager
from anti_desync import AntiDesyncProtocol

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KaiDemoSystem:
    def __init__(self):
        self.input_queue = asyncio.Queue(maxsize=1000)
        self.output_queue = asyncio.Queue(maxsize=500)
        
        self.security_filter = SecurityFilter()
        self.llm_router = LLMRouter()
        self.emotion_tagger = EmotionTagger()
        self.tts_processor = TTSProcessor()
        self.memory_manager = MemoryManager()
        self.anti_desync = AntiDesyncProtocol()
        
        self.is_running = False
        self.cooldown_period = 2.5
        self.last_output_time = 0
        
    async def initialize(self):
        logger.info('Initializing KAI Demo System...')
        await self.memory_manager.initialize()
        logger.info('System ready!')
        
    async def add_input(self, data: Dict):
        try:
            await self.input_queue.put(data)
            logger.info(f"Input from {data['platform']} added to queue")
        except asyncio.QueueFull:
            logger.warning('Input queue full, dropping data')
    
    async def process_pipeline(self):
        while self.is_running:
            try:
                input_data = await asyncio.wait_for(
                    self.input_queue.get(), 
                    timeout=1.0
                )
                
                logger.info(f"Processing: {input_data['payload'][:50]}...")
                
                is_safe, reason = await self.security_filter.check_safety(input_data)
                if not is_safe:
                    logger.warning(f"Blocked: {reason}")
                    continue
                
                emotion_tag = await self.emotion_tagger.tag_emotion(
                    input_data['payload'],
                    input_data.get('type', 'chat')
                )
                logger.info(f"Emotion detected: {emotion_tag}")
                
                llm_response = await self.llm_router.route_and_generate(
                    payload=input_data['payload'],
                    emotion_tag=emotion_tag,
                    user_name=input_data['user_raw_name'],
                    platform=input_data['platform']
                )
                logger.info(f"LLM response: {llm_response[:50]}...")
                
                normalized_text = await self.tts_processor.normalize_text(llm_response)
                logger.info(f"Normalized text: {normalized_text[:50]}...")
                
                audio_chunks = await self.anti_desync.prepare_chunks(
                    text=normalized_text,
                    emotion_tag=emotion_tag
                )
                logger.info(f"Prepared {len(audio_chunks)} audio chunks")
                
                await self.memory_manager.save_interaction({
                    'platform': input_data['platform'],
                    'emotion_tag': emotion_tag,
                    'content': llm_response,
                    'timestamp': datetime.now().isoformat()
                })
                
                output_data = {
                    'emotion_tag': emotion_tag,
                    'text': normalized_text,
                    'audio_chunks': audio_chunks,
                    'user_name': input_data['user_raw_name'],
                    'timestamp': datetime.now().isoformat()
                }
                
                await self._apply_cooldown()
                
                try:
                    self.output_queue.put_nowait(output_data)
                    logger.info('Output data pushed successfully')
                except asyncio.QueueFull:
                    logger.warning('Output queue full')
                    
            except asyncio.TimeoutError:
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Pipeline error: {str(e)}", exc_info=True)
                await asyncio.sleep(0.5)
    
    async def _apply_cooldown(self):
        elapsed = asyncio.get_event_loop().time() - self.last_output_time
        if elapsed < self.cooldown_period:
            await asyncio.sleep(self.cooldown_period - elapsed)
        self.last_output_time = asyncio.get_event_loop().time()
    
    async def get_output(self) -> Optional[Dict]:
        try:
            return self.output_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    async def run(self):
        self.is_running = True
        await self.initialize()
        
        try:
            await self.process_pipeline()
        except KeyboardInterrupt:
            logger.info('Stopping system...')
        finally:
            self.is_running = False
            await self.memory_manager.close()


async def main():
    system = KaiDemoSystem()
    process_task = asyncio.create_task(system.run())
    
    test_data = {
        'platform': 'TikTok',
        'user_raw_name': 'user123',
        'payload': 'Em yeu anh rat nhieu nha',
        'type': 'chat'
    }
    
    await asyncio.sleep(1)
    await system.add_input(test_data)
    
    await asyncio.sleep(30)
    system.is_running = False
    
    try:
        await asyncio.wait_for(process_task, timeout=5)
    except asyncio.TimeoutError:
        process_task.cancel()


if __name__ == '__main__':
    asyncio.run(main())

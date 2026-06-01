#!/usr/bin/env python3
"""
Anti-Desync Protocol - Chong Lech Pha Van Ban va Giong Noi
Quy tac:
1. Linear Semantic Monotony - Khong doi cam xuc dot ngot
2. Clause-by-Clause Streaming - Cat doan theo dau cau
3. Anti-Stall Structural - Cam co tuc danh sach, bang bieu
4. Word-level Lip-Sync - Dong bo frame theo tu
"""

import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class AntiDesyncProtocol:
    
    # Cac dau ngat (clause delimiters)
    DELIMITERS = ['.', ',', '!', '?', '...']
    
    # Cac dau cau tru (punctuation prohibitions)
    PROHIBITED_PATTERNS = [
        r'^\s*[-*+]',  # Bullet points
        r'^\s*\d+\.',  # Numbered lists
        r'```',         # Code blocks
        r'\[\[.*\]\]',  # Double brackets
        r'\{\{.*\}\}',  # Double braces
        r'\[([^\]]+)\]\(',  # Markdown links
    ]
    
    def __init__(self):
        self.max_clause_length = 12  # toi da 12 tu
        self.min_clause_length = 4   # toi thieu 4 tu
    
    async def prepare_chunks(self, text: str, emotion_tag: str) -> List[Dict]:
        """Chuan bi cac chunk am thanh de phat
        
        Returns:
            List cua audio chunks voi thong tin timing
        """
        
        # QUAT LY 1: Linear Semantic Monotony
        text = await self._enforce_linear_semantics(text, emotion_tag)
        logger.info("Linear semantics enforced")
        
        # QUAT LY 2: Clause-by-Clause Chunking
        chunks = await self._create_chunks(text)
        logger.info(f"Created {len(chunks)} chunks")
        
        # QUAT LY 3: Anti-Stall Structural Check
        chunks = await self._remove_prohibited_structures(chunks)
        
        # QUAT LY 4: Word-level Lip-Sync Info
        chunks = await self._add_lip_sync_timestamps(chunks)
        
        return chunks
    
    async def _enforce_linear_semantics(self, text: str, emotion_tag: str) -> str:
        """Cam doi cam xuc thay doi dot ngot trong cung mot cau"""
        
        # Neu muon doi emotion, phai cat cau bang '.'
        # Them dau cat neu can thiet
        
        # Kiểm tra xem có emoji hoặc special chars khiến thay đổi cảm xúc
        # Nếu có, thêm dấu chấm ngăn cách
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        processed = []
        
        for sentence in sentences:
            # Kiem tra doc dai cau
            words = sentence.split()
            if len(words) > 15:
                # Cat doan thanh 2 cau
                mid = len(words) // 2
                first_part = ' '.join(words[:mid]) + '.'
                second_part = ' '.join(words[mid:]) + '.'
                processed.extend([first_part, second_part])
            else:
                processed.append(sentence)
        
        text = ' '.join(processed)
        return text
    
    async def _create_chunks(self, text: str) -> List[Dict]:
        """Tao chunks theo dau cau"""
        
        chunks = []
        current_chunk = ""
        word_count = 0
        
        words = text.split()
        
        for word in words:
            current_chunk += word + " "
            word_count += 1
            
            # Kiem tra neu co dau ngat
            has_delimiter = any(delim in word for delim in self.DELIMITERS)
            
            if has_delimiter or word_count >= self.max_clause_length:
                if word_count >= self.min_clause_length:
                    chunks.append({
                        'text': current_chunk.strip(),
                        'word_count': word_count,
                        'duration_ms': word_count * 100  # Ước tính 100ms/từ
                    })
                    current_chunk = ""
                    word_count = 0
        
        # Them chunk cuoi cung
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'word_count': word_count,
                'duration_ms': word_count * 100
            })
        
        return chunks
    
    async def _remove_prohibited_structures(self, chunks: List[Dict]) -> List[Dict]:
        """Loai bo cac co tuc danh sach, bang bieu, code"""
        
        cleaned_chunks = []
        
        for chunk in chunks:
            text = chunk['text']
            is_prohibited = False
            
            for pattern in self.PROHIBITED_PATTERNS:
                if re.search(pattern, text):
                    logger.warning(f"Prohibited structure found: {pattern}")
                    is_prohibited = True
                    break
            
            if not is_prohibited:
                cleaned_chunks.append(chunk)
        
        return cleaned_chunks
    
    async def _add_lip_sync_timestamps(self, chunks: List[Dict]) -> List[Dict]:
        """Them thong tin lip-sync timeline"""
        
        cumulative_time = 0
        
        for chunk in chunks:
            chunk['start_time_ms'] = cumulative_time
            chunk['end_time_ms'] = cumulative_time + chunk['duration_ms']
            
            # Them word-level boundaries
            words = chunk['text'].split()
            word_duration = chunk['duration_ms'] / len(words) if words else 0
            
            chunk['word_timestamps'] = []
            for i, word in enumerate(words):
                chunk['word_timestamps'].append({
                    'word': word,
                    'start_ms': cumulative_time + (i * word_duration),
                    'end_ms': cumulative_time + ((i + 1) * word_duration)
                })
            
            cumulative_time = chunk['end_time_ms']
        
        return chunks

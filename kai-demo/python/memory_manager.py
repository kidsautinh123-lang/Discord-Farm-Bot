#!/usr/bin/env python3
"""
Memory Manager - QL Ky Uc & Tu Don Dep (SQLite)
CRUD operations + Self-cleaning khi vuot 30MB
"""

import sqlite3
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class MemoryManager:
    
    def __init__(self, db_path: str = 'bekai_history.db', max_size_mb: int = 30):
        self.db_path = db_path
        self.max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        self.conn = None
        self.context_window = 5  # Nho 5 tin nhan truoc
    
    async def initialize(self):
        """Khoi tao database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Tao bang stream_logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stream_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    emotion_tag TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_name TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tao index
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON stream_logs(timestamp)
            ''')
            
            self.conn.commit()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"DB init error: {e}")
    
    async def save_interaction(self, data: Dict):
        """Luu tac dong vao database
        
        Args:
            data: {
                'platform': str,
                'emotion_tag': str,
                'content': str,
                'user_name': str (optional),
                'timestamp': str (optional)
            }
        """
        if not self.conn:
            logger.warning("Database not initialized")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO stream_logs 
                (platform, emotion_tag, content, user_name, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('platform', 'unknown'),
                data.get('emotion_tag', 'NEUTRAL'),
                data.get('content', ''),
                data.get('user_name', 'anonymous'),
                data.get('timestamp', datetime.now().isoformat())
            ))
            
            self.conn.commit()
            logger.info(f"Interaction saved: {data['emotion_tag']}")
            
            # Kiem tra self-cleaning
            await self._check_and_clean()
            
        except Exception as e:
            logger.error(f"Save interaction error: {e}")
    
    async def _check_and_clean(self):
        """Tu don dep khi vuot 30MB"""
        import os
        
        try:
            file_size = os.path.getsize(self.db_path)
            
            if file_size > self.max_size:
                logger.info(f"Database size {file_size} bytes exceeds limit")
                await self._cleanup_old_logs()
                
        except Exception as e:
            logger.error(f"Check and clean error: {e}")
    
    async def _cleanup_old_logs(self):
        """Xoa 200 log cu nhat va vacuum"""
        if not self.conn:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Delete oldest 200 records
            cursor.execute('''
                DELETE FROM stream_logs WHERE id IN (
                    SELECT id FROM stream_logs 
                    ORDER BY id ASC LIMIT 200
                )
            ''')
            
            # VACUUM database
            cursor.execute('VACUUM')
            
            self.conn.commit()
            logger.info("Database cleaned and vacuumed")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
    
    async def get_context_window(self, limit: int = None) -> List[Dict]:
        """Lay context window - 5 tin nhan truoc"""
        if not self.conn:
            return []
        
        limit = limit or self.context_window
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT platform, emotion_tag, content, user_name, timestamp
                FROM stream_logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    'platform': row[0],
                    'emotion_tag': row[1],
                    'content': row[2],
                    'user_name': row[3],
                    'timestamp': row[4]
                }
                for row in reversed(rows)
            ]
            
        except Exception as e:
            logger.error(f"Get context error: {e}")
            return []
    
    async def close(self):
        """Dong ket noi database"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

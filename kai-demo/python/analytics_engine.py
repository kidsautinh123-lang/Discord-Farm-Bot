#!/usr/bin/env python3
"""
Database Optimization - Aggregated Analytics va Trend Analysis
"""

import logging
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnalyticsMetric:
    """Metric cho analytics"""
    metric_name: str
    value: float
    timestamp: str
    user_id: Optional[str] = None
    emotion_tag: Optional[str] = None


class AnalyticsEngine:
    """Xu ly analytics va trend analysis"""
    
    def __init__(self, db_path: str = 'kai_analytics.db'):
        self.db_path = db_path
        self.conn = None
        self._init_analytics_db()
    
    def _init_analytics_db(self):
        """Khoi tao analytics database"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Table cho aggregated metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                user_id TEXT,
                emotion_tag TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table cho daily aggregates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_aggregates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_requests INTEGER,
                average_latency REAL,
                total_users INTEGER,
                dominant_emotion TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON analytics_metrics(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotion ON analytics_metrics(emotion_tag)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON analytics_metrics(timestamp)')
        
        self.conn.commit()
        logger.info("Analytics database initialized")
    
    def record_metric(self, metric: AnalyticsMetric):
        """Ghi nhan mot metric"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics_metrics 
            (metric_name, value, user_id, emotion_tag, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            metric.metric_name,
            metric.value,
            metric.user_id,
            metric.emotion_tag,
            metric.timestamp
        ))
        
        self.conn.commit()
    
    def get_aggregated_stats(self, days: int = 7) -> Dict:
        """Lay thong ke hop nhat trong nhung ngay gaan day"""
        cursor = self.conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Total requests
        cursor.execute('''
            SELECT COUNT(*) FROM analytics_metrics 
            WHERE timestamp > ?
        ''', (cutoff_date,))
        total_requests = cursor.fetchone()[0]
        
        # Average latency
        cursor.execute('''
            SELECT AVG(value) FROM analytics_metrics 
            WHERE metric_name = 'latency_ms' AND timestamp > ?
        ''', (cutoff_date,))
        avg_latency = cursor.fetchone()[0] or 0
        
        # Unique users
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM analytics_metrics 
            WHERE timestamp > ?
        ''', (cutoff_date,))
        unique_users = cursor.fetchone()[0]
        
        # Emotion distribution
        cursor.execute('''
            SELECT emotion_tag, COUNT(*) FROM analytics_metrics 
            WHERE emotion_tag IS NOT NULL AND timestamp > ?
            GROUP BY emotion_tag
        ''', (cutoff_date,))
        emotion_dist = dict(cursor.fetchall())
        
        return {
            'period_days': days,
            'total_requests': total_requests,
            'average_latency_ms': round(avg_latency, 2),
            'unique_users': unique_users,
            'emotion_distribution': emotion_dist
        }
    
    def get_user_trend(self, user_id: str, days: int = 30) -> List[Dict]:
        """Lay trend cua user trong nhung ngay gaan day"""
        cursor = self.conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT DATE(timestamp) as date, 
                   COUNT(*) as request_count,
                   AVG(value) as avg_metric
            FROM analytics_metrics
            WHERE user_id = ? AND timestamp > ?
            GROUP BY DATE(timestamp)
            ORDER BY date ASC
        ''', (user_id, cutoff_date))
        
        trends = []
        for row in cursor.fetchall():
            trends.append({
                'date': row[0],
                'request_count': row[1],
                'avg_metric': round(row[2], 2) if row[2] else 0
            })
        
        return trends
    
    def generate_daily_aggregate(self, date: str):
        """Generate daily aggregate stats"""
        cursor = self.conn.cursor()
        
        start_date = date
        end_date = (datetime.fromisoformat(date) + timedelta(days=1)).isoformat()
        
        # Get stats for the day
        cursor.execute('''
            SELECT COUNT(*), AVG(value), COUNT(DISTINCT user_id)
            FROM analytics_metrics
            WHERE DATE(timestamp) = ?
        ''', (date,))
        
        total_requests, avg_latency, total_users = cursor.fetchone()
        
        # Get dominant emotion
        cursor.execute('''
            SELECT emotion_tag FROM analytics_metrics
            WHERE DATE(timestamp) = ?
            GROUP BY emotion_tag
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ''', (date,))
        
        dominant_emotion = cursor.fetchone()
        dominant_emotion = dominant_emotion[0] if dominant_emotion else None
        
        # Store aggregate
        cursor.execute('''
            INSERT INTO daily_aggregates 
            (date, total_requests, average_latency, total_users, dominant_emotion)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            date,
            total_requests or 0,
            avg_latency or 0,
            total_users or 0,
            dominant_emotion
        ))
        
        self.conn.commit()
        logger.info(f"Daily aggregate generated: {date}")
    
    def predict_trend(self, user_id: str, metric: str = 'engagement') -> Dict:
        """Predict trend cua user"""
        cursor = self.conn.cursor()
        
        # Get last 30 days data
        cursor.execute('''
            SELECT DATE(timestamp), COUNT(*) FROM analytics_metrics
            WHERE user_id = ? 
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp) DESC
            LIMIT 30
        ''', (user_id,))
        
        data = cursor.fetchall()
        
        if len(data) < 2:
            return {'user_id': user_id, 'trend': 'insufficient_data'}
        
        # Simple trend calculation
        recent_avg = sum(row[1] for row in data[:7]) / 7 if len(data) >= 7 else data[0][1]
        older_avg = sum(row[1] for row in data[-7:]) / 7 if len(data) >= 14 else data[-1][1]
        
        trend_diff = recent_avg - older_avg
        
        if trend_diff > older_avg * 0.2:
            trend = 'increasing'
        elif trend_diff < -older_avg * 0.2:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'user_id': user_id,
            'metric': metric,
            'trend': trend,
            'recent_average': round(recent_avg, 2),
            'older_average': round(older_avg, 2),
            'change_percentage': round((trend_diff / older_avg * 100) if older_avg > 0 else 0, 2)
        }

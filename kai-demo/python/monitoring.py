#!/usr/bin/env python3
"""
Monitoring va Logging - ELK Stack, Prometheus, Centralized Logging
"""

import logging
import json
from typing import Dict, Optional
from datetime import datetime
from enum import Enum
import os

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Cap do log"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CentralizedLogger:
    """Centralized logging system"""
    
    def __init__(self, service_name: str = "kai-demo",
                 log_file: str = "logs/kai_demo.log"):
        self.service_name = service_name
        self.log_file = log_file
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging co file, console va structured"""
        # Create logs directory
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Setup formatters
        json_formatter = JsonFormatter(self.service_name)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup handlers
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(json_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    def log_event(self, level: LogLevel, message: str, 
                  context: Optional[Dict] = None):
        """Log event voi context"""
        log_func = getattr(logger, level.value.lower())
        
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        
        log_func(message)


class JsonFormatter(logging.Formatter):
    """JSON formatter cho structured logging"""
    
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'service': self.service_name,
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)


class MetricsCollector:
    """Collect metrics cho Prometheus"""
    
    def __init__(self):
        self.metrics = {}
        self.counters = {}
        self.gauges = {}
        self.histograms = {}
    
    def increment_counter(self, name: str, value: int = 1, 
                         labels: Optional[Dict] = None):
        """Increment counter"""
        key = f"{name}_{json.dumps(labels or {})}"
        self.counters[key] = self.counters.get(key, 0) + value
    
    def set_gauge(self, name: str, value: float, 
                  labels: Optional[Dict] = None):
        """Set gauge value"""
        key = f"{name}_{json.dumps(labels or {})}"
        self.gauges[key] = value
    
    def observe_histogram(self, name: str, value: float, 
                         labels: Optional[Dict] = None):
        """Observe histogram value"""
        key = f"{name}_{json.dumps(labels or {})}"
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
    
    def get_metrics_summary(self) -> Dict:
        """Get summary cua tat ca metrics"""
        histogram_summary = {}
        for key, values in self.histograms.items():
            if values:
                histogram_summary[key] = {
                    'count': len(values),
                    'sum': sum(values),
                    'avg': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                }
        
        return {
            'counters': self.counters,
            'gauges': self.gauges,
            'histograms': histogram_summary
        }
    
    def export_prometheus_format(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        # Export counters
        for key, value in self.counters.items():
            lines.append(f"{key} {value}")
        
        # Export gauges
        for key, value in self.gauges.items():
            lines.append(f"{key} {value}")
        
        return "\n".join(lines)


class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.logger = CentralizedLogger()
    
    def track_request(self, user_id: str, endpoint: str, 
                     latency_ms: float, status_code: int):
        """Track API request"""
        self.metrics_collector.increment_counter(
            'http_requests_total',
            labels={'endpoint': endpoint, 'status': status_code}
        )
        
        self.metrics_collector.observe_histogram(
            'http_request_duration_ms',
            latency_ms,
            labels={'endpoint': endpoint}
        )
        
        self.logger.log_event(
            LogLevel.INFO,
            f"Request completed",
            context={
                'user_id': user_id,
                'endpoint': endpoint,
                'latency_ms': latency_ms,
                'status': status_code
            }
        )
    
    def track_error(self, error_type: str, error_message: str, 
                   context: Optional[Dict] = None):
        """Track error"""
        self.metrics_collector.increment_counter(
            'errors_total',
            labels={'type': error_type}
        )
        
        self.logger.log_event(
            LogLevel.ERROR,
            f"{error_type}: {error_message}",
            context=context
        )
    
    def get_dashboard_data(self) -> Dict:
        """Get data for monitoring dashboard"""
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.metrics_collector.get_metrics_summary()
        }

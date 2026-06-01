#!/usr/bin/env python3
"""
Advanced Logger Module - Ghi nhật ký nâng cao
Hỗ trợ file logging, structured logging, log levels
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json


class AdvancedLogger:
    """Logger nâng cao với nhiều tính năng"""
    
    # Log levels
    DEBUG = logging.DEBUG        # 10
    INFO = logging.INFO          # 20
    WARNING = logging.WARNING    # 30
    ERROR = logging.ERROR        # 40
    CRITICAL = logging.CRITICAL  # 50
    
    def __init__(self, name: str):
        """Khởi tạo logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Tạo thư mục logs nếu không tồn tại
        log_dir = Path(os.getenv('LOG_DIR', 'logs'))
        log_dir.mkdir(exist_ok=True)
        
        # Console Handler
        self._setup_console_handler()
        
        # File Handler
        self._setup_file_handlers(log_dir)
    
    def _setup_console_handler(self):
        """Thiết lập console output"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(os.getenv('CONSOLE_LOG_LEVEL', 'INFO'))
        
        # Formatter với màu
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handlers(self, log_dir: Path):
        """Thiết lập file output"""
        
        # General log file (rotating)
        general_log = log_dir / 'kai-system.log'
        general_handler = RotatingFileHandler(
            general_log,
            maxBytes=int(os.getenv('LOG_MAX_BYTES', 10*1024*1024)),  # 10MB
            backupCount=int(os.getenv('LOG_BACKUP_COUNT', 5))
        )
        general_handler.setLevel(logging.DEBUG)
        general_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        general_handler.setFormatter(general_formatter)
        self.logger.addHandler(general_handler)
        
        # Error log file (daily rotation)
        error_log = log_dir / 'kai-errors.log'
        error_handler = TimedRotatingFileHandler(
            error_log,
            when='midnight',
            interval=1,
            backupCount=int(os.getenv('LOG_BACKUP_COUNT', 5))
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
        
        # Performance log file
        perf_log = log_dir / 'kai-performance.log'
        perf_handler = RotatingFileHandler(
            perf_log,
            maxBytes=int(os.getenv('LOG_MAX_BYTES', 10*1024*1024)),
            backupCount=3
        )
        perf_handler.setLevel(logging.INFO)
        perf_formatter = logging.Formatter(
            '%(asctime)s - %(message)s'
        )
        perf_handler.setFormatter(perf_formatter)
        self.perf_logger = logging.getLogger(f"{self.logger.name}.performance")
        self.perf_logger.addHandler(perf_handler)
    
    # ============= Logging Methods =============
    
    def debug(self, msg: str, *args, **kwargs):
        """Debug level"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """Info level"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """Warning level"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """Error level"""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """Critical level"""
        self.logger.critical(msg, *args, **kwargs)
    
    # ============= Structured Logging =============
    
    def log_json(self, level: int, data: dict):
        """Log structured JSON"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        self.logger.log(level, f"JSON: {json_str}")
    
    def log_metrics(self, metrics: dict):
        """Log metrics"""
        msg = " | ".join([f"{k}={v}" for k, v in metrics.items()])
        self.perf_logger.info(msg)
    
    def log_performance(self, operation: str, duration: float, status: str = 'success'):
        """Log performance data"""
        msg = f"[{status.upper()}] {operation}: {duration:.3f}s"
        self.perf_logger.info(msg)
    
    def log_exception(self, msg: str = "", exc_info=True):
        """Log exception"""
        self.logger.exception(msg or "Exception occurred", exc_info=exc_info)
    
    # ============= Utility Methods =============
    
    def set_level(self, level):
        """Thay đổi log level"""
        self.logger.setLevel(level)
    
    def add_custom_handler(self, handler: logging.Handler):
        """Thêm custom handler"""
        self.logger.addHandler(handler)
    
    def get_logger(self):
        """Lấy underlying logger"""
        return self.logger

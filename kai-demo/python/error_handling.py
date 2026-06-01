#!/usr/bin/env python3
"""
Advanced Error Handling - Circuit Breaker, Retry, Fallback
"""

import asyncio
import logging
from typing import Callable, Any, Optional, List
from enum import Enum
from datetime import datetime, timedelta
import functools

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit Breaker pattern - ngat ket noi khi co loi"""
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout_sec: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_sec
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
        self.last_success_time = None
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Goi ham thong qua circuit breaker"""
        
        # Check if should attempt recovery
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker attempting recovery")
            else:
                raise Exception(f"Circuit breaker OPEN for {self.recovery_timeout}s")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_recovery(self) -> bool:
        """Check xem co the phuc hoi khong"""
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time > 
            timedelta(seconds=self.recovery_timeout)
        )
    
    def _on_success(self):
        """Xu ly thanh cong"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_success_time = datetime.now()
        logger.info("Circuit breaker: Success")
    
    def _on_failure(self):
        """Xu ly that bai"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error(f"Circuit breaker OPEN after {self.failure_count} failures")
        else:
            logger.warning(f"Failure count: {self.failure_count}/{self.failure_threshold}")


class RetryStrategy:
    """Retry voi exponential backoff"""
    
    def __init__(self, max_retries: int = 3, 
                 base_delay_ms: float = 100,
                 max_delay_ms: float = 5000):
        self.max_retries = max_retries
        self.base_delay = base_delay_ms / 1000  # Convert to seconds
        self.max_delay = max_delay_ms / 1000
    
    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Chay function voi retry"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries + 1}")
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = min(
                        self.base_delay * (2 ** attempt),
                        self.max_delay
                    )
                    logger.warning(f"Retry after {delay:.2f}s: {str(e)}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All retries failed: {str(e)}")
        
        raise last_exception


class FallbackHandler:
    """Fallback mechanism - dung thay the khi chinh fail"""
    
    def __init__(self):
        self.fallback_chain: List[Callable] = []
    
    def add_fallback(self, func: Callable) -> 'FallbackHandler':
        """Them fallback function"""
        self.fallback_chain.append(func)
        return self
    
    async def execute(self, primary_func: Callable, 
                      *args, **kwargs) -> Any:
        """Chay primary, neu fail thi chay fallback"""
        
        try:
            logger.info("Executing primary function")
            return await primary_func(*args, **kwargs)
        except Exception as primary_error:
            logger.error(f"Primary failed: {str(primary_error)}")
            
            for i, fallback_func in enumerate(self.fallback_chain):
                try:
                    logger.info(f"Executing fallback {i + 1}")
                    return await fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    logger.warning(f"Fallback {i + 1} failed: {str(fallback_error)}")
            
            logger.error("All fallbacks exhausted")
            raise primary_error


def with_resilience(max_retries: int = 3, 
                    circuit_breaker: Optional[CircuitBreaker] = None):
    """Decorator for resilient functions"""
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            retry = RetryStrategy(max_retries=max_retries)
            
            if circuit_breaker:
                return await circuit_breaker.call(
                    retry.execute, func, *args, **kwargs
                )
            else:
                return await retry.execute(func, *args, **kwargs)
        
        return wrapper
    
    return decorator

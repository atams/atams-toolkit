"""
Rate Limiting System
In-memory rate limiting based on IP address

Features:
- Configurable requests per window
- In-memory storage (no external dependencies)
- Automatic cleanup of expired entries
- Can be enabled/disabled via config
"""
import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from atams.logging import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    In-memory rate limiter using sliding window

    Storage format:
    {
        "client_ip": (request_count, window_start_time)
    }
    """

    def __init__(self, requests: int = 100, window: int = 60):
        """
        Initialize rate limiter

        Args:
            requests: Maximum requests allowed per window
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.clients: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Check if request is allowed for client

        Args:
            client_id: Client identifier (usually IP address)

        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        current_time = time.time()
        count, window_start = self.clients[client_id]

        # Check if window has expired
        if current_time - window_start >= self.window:
            # Reset window
            self.clients[client_id] = (1, current_time)
            return True, self.requests - 1

        # Window still active
        if count >= self.requests:
            # Rate limit exceeded
            return False, 0

        # Increment counter
        self.clients[client_id] = (count + 1, window_start)
        return True, self.requests - (count + 1)

    def cleanup_expired(self):
        """Remove expired entries to prevent memory leak"""
        current_time = time.time()
        expired_clients = [
            client_id for client_id, (_, window_start) in self.clients.items()
            if current_time - window_start >= self.window * 2
        ]

        for client_id in expired_clients:
            del self.clients[client_id]


def create_rate_limiter(requests: int = 100, window: int = 60):
    """Factory function untuk create RateLimiter"""
    return RateLimiter(requests, window)


def create_rate_limit_middleware(rate_limit_enabled: bool, requests: int, window: int):
    """
    Factory function untuk create RateLimitMiddleware dengan konfigurasi

    Args:
        rate_limit_enabled: Flag untuk enable/disable rate limiting
        requests: Maximum requests per window
        window: Time window in seconds

    Returns:
        Configured RateLimitMiddleware class
    """
    class ConfiguredRateLimitMiddleware(BaseHTTPMiddleware):
        """
        Middleware to enforce rate limiting

        Features:
        - Rate limit based on client IP
        - Add rate limit headers to response
        - Return 429 when limit exceeded
        - Periodic cleanup of expired entries
        """

        def __init__(self, app):
            super().__init__(app)
            self.rate_limiter = create_rate_limiter(requests, window)
            self.cleanup_counter = 0
            self.enabled = rate_limit_enabled
            self.requests_limit = requests
            self.window_seconds = window

        async def dispatch(self, request: Request, call_next) -> Response:
            # Skip rate limiting if disabled
            if not self.enabled:
                return await call_next(request)

            # Skip rate limiting for docs and openapi
            if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
                return await call_next(request)

            # Get client IP
            client_ip = request.client.host if request.client else "unknown"

            # Check rate limit
            is_allowed, remaining = self.rate_limiter.is_allowed(client_ip)

            if not is_allowed:
                logger.warning(
                    f"Rate limit exceeded for {client_ip}",
                    extra={
                        'extra_data': {
                            'client_ip': client_ip,
                            'path': request.url.path,
                            'method': request.method
                        }
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "message": "Rate limit exceeded",
                        "limit": self.requests_limit,
                        "window": f"{self.window_seconds}s",
                        "retry_after": self.window_seconds
                    }
                )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Window"] = f"{self.window_seconds}s"

            # Periodic cleanup (every 100 requests)
            self.cleanup_counter += 1
            if self.cleanup_counter >= 100:
                self.rate_limiter.cleanup_expired()
                self.cleanup_counter = 0

            return response

    return ConfiguredRateLimitMiddleware

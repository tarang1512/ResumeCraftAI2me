"""
Upstox API Client with rate limiting and error handling
"""

import time
import requests
from typing import Optional, Dict, Any, Callable
from functools import wraps

from upstox_bot.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    # Upstox Rate Limits (adjust based on your plan)
    DEFAULT_RATE = 0.1  # 10 requests per second = 0.1 seconds per request
    
    def __init__(self, rate: float = DEFAULT_RATE):
        self.rate = rate
        self.last_call = 0
    
    def wait(self):
        """Wait if necessary to maintain rate limit"""
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.rate:
            sleep_time = self.rate - elapsed
            time.sleep(sleep_time)
        self.last_call = time.time()


class UpstoxAPIError(Exception):
    """Custom exception for Upstox API errors"""
    
    def __init__(self, message: str, status_code: int = None, response: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


def retry_on_exception(max_retries: int = 3, exceptions: tuple = (Exception,)):
    """Decorator to retry API calls on failure - skips retry on 4xx client errors"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    # Don't retry on 4xx client errors (400-499)
                    status_code = None
                    if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                        status_code = e.response.status_code
                    elif hasattr(e, 'status_code'):
                        status_code = e.status_code
                    
                    if status_code and 400 <= status_code < 500:
                        logger.debug(f"Client error {status_code}, not retrying: {e}")
                        raise
                    
                    if attempt == max_retries - 1:
                        raise
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


class UpstoxClient:
    """Main API client for Upstox"""
    
    SANDBOX_BASE_URL = "https://api.sandbox.upstox.com/v2"
    PRODUCTION_BASE_URL = "https://api.upstox.com/v2"
    
    def __init__(self, auth, environment: str = None):
        """
        Initialize API client
        
        Args:
            auth: UpstoxAuth instance
            environment: "sandbox" or "production" (defaults to auth.environment)
        """
        self.environment = environment or auth.environment or "sandbox"
        self.base_url = self.PRODUCTION_BASE_URL if self.environment == "production" else self.SANDBOX_BASE_URL
        self.auth = auth
        self.rate_limiter = RateLimiter()
        self.session = requests.Session()
        self.timeout = 30
        
        logger.info(f"UpstoxClient initialized ({environment} environment)")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with rate limiting and error handling"""
        self.rate_limiter.wait()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.auth.get_auth_headers()
        headers.update(kwargs.pop('headers', {}))
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self._make_request(method, endpoint, **kwargs)
            
            response.raise_for_status()
            
            # Handle empty responses
            if not response.content:
                return {}
            
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {url}")
            raise UpstoxAPIError(f"Request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise UpstoxAPIError(f"Connection error: {e}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            try:
                error_data = e.response.json()
                logger.error(f"Error details: {error_data}")
            except:
                pass
            raise UpstoxAPIError(str(e), e.response.status_code, e.response)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise UpstoxAPIError(f"Unexpected error: {e}")
    
    @retry_on_exception(max_retries=3, exceptions=(UpstoxAPIError,))
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request("GET", endpoint, **kwargs)
    
    @retry_on_exception(max_retries=3, exceptions=(UpstoxAPIError,))
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request("POST", endpoint, **kwargs)
    
    @retry_on_exception(max_retries=3, exceptions=(UpstoxAPIError,))
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request"""
        return self._make_request("PUT", endpoint, **kwargs)
    
    @retry_on_exception(max_retries=3, exceptions=(UpstoxAPIError,))
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint, **kwargs)

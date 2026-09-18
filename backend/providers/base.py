from abc import ABC, abstractmethod
from typing import Dict, Any
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger("UrbanIQ.Provider")

class BaseProvider(ABC):
    def __init__(self, name: str, cache_ttl: int = 300):
        self.name = name
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_time = {}

    @abstractmethod
    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch raw data"""
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data to common schema"""
        pass

    def get_fallback_data(self, **kwargs) -> Dict[str, Any]:
        """Return fallback data"""
        return {}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    def _fetch_with_retry(self, **kwargs):
        return self.fetch_data(**kwargs)

    def get_data(self, **kwargs) -> Dict[str, Any]:
        """Standardized response format"""
        cache_key = str(kwargs)
        now = time.time()

        # 1. Check cache
        if cache_key in self._cache and (now - self._cache_time.get(cache_key, 0) < self.cache_ttl):
            return {
                "source": self.name,
                "fetched_at": self._cache_time[cache_key],
                "freshness_seconds": round(now - self._cache_time[cache_key], 4),
                "location": kwargs.get("location", "Lahore"),
                "status": "cached",
                "normalized_fields": self._cache[cache_key]
            }

        fetch_start = now
        status = "unavailable"
        normalized = {}
        
        # 2. Fetch live data with retries
        try:
            raw_data = self._fetch_with_retry(**kwargs)
            if raw_data:
                normalized = self.normalize(raw_data)
                status = "live"
                # Update cache
                self._cache[cache_key] = normalized
                self._cache_time[cache_key] = fetch_start
            else:
                raw_data = self.get_fallback_data(**kwargs)
                normalized = self.normalize(raw_data) if raw_data else {}
                status = "fallback" if raw_data else "unavailable"
        except Exception as e:
            logger.warning(f"{self.name} fetch failed: {e}. Using fallback.")
            raw_data = self.get_fallback_data(**kwargs)
            normalized = self.normalize(raw_data) if raw_data else {}
            status = "fallback" if raw_data else "unavailable"

        return {
            "source": self.name,
            "fetched_at": fetch_start,
            "freshness_seconds": round(time.time() - fetch_start, 4),
            "location": kwargs.get("location", "Lahore"),
            "status": status,
            "normalized_fields": normalized
        }

"""In-memory TTL cache suitable for a single-user personal deployment."""
from __future__ import annotations

import asyncio
import functools
import hashlib
import inspect
import time
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Dict, Optional, TypeVar

T = TypeVar("T")


class TTLCache:
    """A small in-memory LRU cache with per-entry TTL expiry."""

    def __init__(self, maxsize: int = 128) -> None:
        self._maxsize = int(maxsize)
        self._store: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()
        self._lock = asyncio.Lock()

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < time.monotonic():
            self._store.pop(key, None)
            return None
        # refresh LRU position
        self._store.move_to_end(key)
        return value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        expires_at = time.monotonic() + max(0, int(ttl_seconds))
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = (expires_at, value)
        while len(self._store) > self._maxsize:
            self._store.popitem(last=False)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def invalidate_prefix(self, prefix: str) -> None:
        for k in [k for k in self._store.keys() if k.startswith(prefix)]:
            self._store.pop(k, None)

    def clear(self) -> None:
        self._store.clear()


# ---------------------------------------------------------------------------
# Shared default cache + decorator
# ---------------------------------------------------------------------------

_default_cache = TTLCache(maxsize=256)


def get_default_cache() -> TTLCache:
    return _default_cache


def _make_key(func_name: str, args: tuple, kwargs: Dict[str, Any]) -> str:
    # Skip the first arg if it looks like "self" (an instance of any class
    # with __dict__) to keep keys stable across service instances.
    sig_args = args
    if sig_args and hasattr(sig_args[0], "__dict__") and not isinstance(
        sig_args[0], (str, int, float, bytes)
    ):
        sig_args = sig_args[1:]
    # Drop AsyncSession-like arguments — they aren't part of the logical key
    filtered_args = tuple(
        a for a in sig_args if type(a).__name__ != "AsyncSession"
    )
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if type(v).__name__ != "AsyncSession"
    }
    raw = f"{func_name}:{filtered_args}:{sorted(filtered_kwargs.items())}"
    digest = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return f"{func_name}:{digest}"


def cache_response(ttl: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator caching async (or sync) function results for ``ttl`` seconds."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        is_coro = inspect.iscoroutinefunction(func)

        if is_coro:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = _make_key(func.__name__, args, kwargs)
                hit = _default_cache.get(key)
                if hit is not None:
                    return hit
                result = await func(*args, **kwargs)
                _default_cache.set(key, result, ttl)
                return result

            async_wrapper.__wrapped__ = func  # type: ignore[attr-defined]
            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(func.__name__, args, kwargs)
            hit = _default_cache.get(key)
            if hit is not None:
                return hit
            result = func(*args, **kwargs)
            _default_cache.set(key, result, ttl)
            return result

        sync_wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return sync_wrapper

    return decorator

"""Tests for core.cache: TTLCache + cache_response decorator."""
from __future__ import annotations

import asyncio
import time
from unittest.mock import patch

import pytest

from core.cache import TTLCache, _default_cache, _make_key, cache_response


# ---------------------------------------------------------------------------
# TTLCache unit tests
# ---------------------------------------------------------------------------

class TestTTLCache:
    def setup_method(self):
        self.cache = TTLCache(maxsize=4)

    def test_get_set_round_trip(self):
        self.cache.set("k1", "v1", ttl_seconds=60)
        assert self.cache.get("k1") == "v1"

    def test_get_missing_key_returns_none(self):
        assert self.cache.get("nonexistent") is None

    def test_ttl_expiry(self):
        """After TTL elapses the entry should be evicted on read."""
        self.cache.set("exp", 42, ttl_seconds=1)
        # Patch time.monotonic to jump forward
        real_mono = time.monotonic
        with patch("core.cache.time.monotonic", side_effect=lambda: real_mono() + 2):
            assert self.cache.get("exp") is None

    def test_lru_eviction(self):
        """When maxsize is exceeded the oldest (LRU) entry is evicted."""
        for i in range(4):
            self.cache.set(f"k{i}", i, ttl_seconds=60)
        # All 4 present
        assert self.cache.get("k0") == 0
        # Insert 5th -> k1 should be evicted (k0 was just refreshed by get)
        self.cache.set("k4", 4, ttl_seconds=60)
        assert self.cache.get("k1") is None
        assert self.cache.get("k4") == 4

    def test_invalidate(self):
        self.cache.set("a", 1, ttl_seconds=60)
        self.cache.invalidate("a")
        assert self.cache.get("a") is None

    def test_invalidate_prefix(self):
        self.cache.set("user:1", "alice", ttl_seconds=60)
        self.cache.set("user:2", "bob", ttl_seconds=60)
        self.cache.set("post:1", "hello", ttl_seconds=60)
        self.cache.invalidate_prefix("user:")
        assert self.cache.get("user:1") is None
        assert self.cache.get("user:2") is None
        assert self.cache.get("post:1") == "hello"

    def test_clear(self):
        self.cache.set("a", 1, ttl_seconds=60)
        self.cache.set("b", 2, ttl_seconds=60)
        self.cache.clear()
        assert self.cache.get("a") is None
        assert self.cache.get("b") is None

    def test_overwrite_existing_key(self):
        self.cache.set("k", "old", ttl_seconds=60)
        self.cache.set("k", "new", ttl_seconds=60)
        assert self.cache.get("k") == "new"


# ---------------------------------------------------------------------------
# _make_key tests
# ---------------------------------------------------------------------------

class TestMakeKey:
    def test_strips_self_arg(self):
        class Svc:
            pass
        svc = Svc()
        k1 = _make_key("fn", (svc, "a"), {})
        k2 = _make_key("fn", ("a",), {})
        assert k1 == k2

    def test_strips_async_session_arg(self):
        class AsyncSession:
            pass
        sess = AsyncSession()
        k1 = _make_key("fn", ("a", sess), {})
        k2 = _make_key("fn", ("a",), {})
        assert k1 == k2

    def test_different_args_different_keys(self):
        k1 = _make_key("fn", ("a",), {})
        k2 = _make_key("fn", ("b",), {})
        assert k1 != k2

    def test_different_functions_different_keys(self):
        k1 = _make_key("fn_a", ("x",), {})
        k2 = _make_key("fn_b", ("x",), {})
        assert k1 != k2

    def test_kwargs_included(self):
        k1 = _make_key("fn", (), {"days": 30})
        k2 = _make_key("fn", (), {"days": 7})
        assert k1 != k2


# ---------------------------------------------------------------------------
# cache_response decorator tests
# ---------------------------------------------------------------------------

class TestCacheResponseDecorator:
    def setup_method(self):
        _default_cache.clear()

    def test_sync_function_cached(self):
        call_count = 0

        @cache_response(ttl=60)
        def compute(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert compute(5) == 10
        assert call_count == 1  # second call served from cache

    def test_sync_different_args_separate_entries(self):
        call_count = 0

        @cache_response(ttl=60)
        def compute(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert compute(3) == 6
        assert call_count == 2

    async def test_async_function_cached(self):
        call_count = 0

        @cache_response(ttl=60)
        async def compute_async(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 3

        assert await compute_async(4) == 12
        assert await compute_async(4) == 12
        assert call_count == 1

    def test_wrapped_attribute_preserved(self):
        @cache_response(ttl=60)
        def fn():
            pass

        assert hasattr(fn, "__wrapped__")

    def teardown_method(self):
        _default_cache.clear()

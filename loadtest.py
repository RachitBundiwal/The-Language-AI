"""Load test: fire N concurrent requests to various endpoints and report stats."""
import asyncio
import statistics
import sys
import time
from collections import defaultdict

import httpx

BASE = "http://localhost:8000"
CONCURRENCY = 120


async def hit(client, method, path, **kw):
    t0 = time.perf_counter()
    try:
        r = await client.request(method, BASE + path, timeout=60.0, **kw)
        return (path, r.status_code, (time.perf_counter() - t0) * 1000, None)
    except Exception as e:
        return (path, 0, (time.perf_counter() - t0) * 1000, type(e).__name__)


async def run_scenario(name, make_req, n):
    print(f"\n{'='*60}\n{name} — {n} concurrent\n{'='*60}")
    async with httpx.AsyncClient(http2=False) as client:
        t0 = time.perf_counter()
        results = await asyncio.gather(*(make_req(client, i) for i in range(n)))
        wall = time.perf_counter() - t0

    by_code = defaultdict(int)
    latencies = []
    errors = defaultdict(int)
    for _path, code, ms, err in results:
        by_code[code] += 1
        if err:
            errors[err] += 1
        else:
            latencies.append(ms)

    ok = by_code.get(200, 0)
    print(f"Wall time: {wall:.2f}s  |  Throughput: {n/wall:.1f} req/s")
    print(f"Status: {dict(by_code)}")
    if errors:
        print(f"Errors: {dict(errors)}")
    if latencies:
        latencies.sort()
        p50 = latencies[len(latencies)//2]
        p95 = latencies[int(len(latencies)*0.95)]
        p99 = latencies[int(len(latencies)*0.99)]
        print(f"Latency ms — min:{min(latencies):.0f} p50:{p50:.0f} p95:{p95:.0f} p99:{p99:.0f} max:{max(latencies):.0f}")
    print(f"Success rate: {ok}/{n} ({100*ok/n:.1f}%)")


async def main():
    # Warm up
    async with httpx.AsyncClient() as c:
        await c.get(BASE + "/health", timeout=10.0)

    # --- Scenario 1: cheap DB read (lessons list) ---
    await run_scenario(
        "Lessons list (DB read)",
        lambda c, i: hit(c, "GET", "/api/v1/lessons/"),
        CONCURRENCY,
    )

    # --- Scenario 2: analytics (heavier, cached) ---
    await run_scenario(
        "Analytics full (DB aggregations, cached 60s)",
        lambda c, i: hit(c, "GET", "/api/v1/analytics/full"),
        CONCURRENCY,
    )

    # --- Scenario 3: mixed workload (health + lessons + analytics + achievements) ---
    paths = [
        "/health",
        "/api/v1/lessons/",
        "/api/v1/analytics/achievements",
        "/api/v1/analytics/heatmap",
        "/api/v1/progress/stats",
        "/api/v1/exams/readiness",
        "/api/v1/lessons/1",
        "/api/v1/voice/voices",
    ]
    await run_scenario(
        "Mixed read workload",
        lambda c, i: hit(c, "GET", paths[i % len(paths)]),
        CONCURRENCY,
    )

    # --- Scenario 4: Groq LLM chat (expensive external call) ---
    async def chat(c, i):
        return await hit(
            c, "POST", "/api/v1/conversation/chat",
            json={"scenario": "bakery", "level": "A1",
                  "message": f"Hallo ich will brot Nummer {i}", "history": []},
            headers={"Content-Type": "application/json"},
        )
    await run_scenario("Chat/LLM (Groq external)", chat, CONCURRENCY)

    # --- Scenario 5: vocab write (DB writes) ---
    async def add_vocab(c, i):
        return await hit(
            c, "POST", "/api/v1/progress/vocabulary/add",
            json={"german_word": f"TestWort{i}", "english_translation": f"word{i}"},
            headers={"Content-Type": "application/json"},
        )
    await run_scenario("Vocab add (DB writes)", add_vocab, CONCURRENCY)


if __name__ == "__main__":
    asyncio.run(main())

"""One-shot database seed script for Sprechen.

Run:  python scripts/seed_db.py
Idempotent: if lessons already exist, it prints a notice and exits cleanly.
"""
from __future__ import annotations

import asyncio
import os
import sys

# Ensure the backend root is on sys.path when invoked as `python scripts/seed_db.py`
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sqlalchemy import func, select  # noqa: E402

from models.database import AsyncSessionLocal, init_db  # noqa: E402
from models.orm_models import Lesson  # noqa: E402


async def main() -> int:
    await init_db()

    try:
        from data.lesson_seeds import seed_default_lessons  # type: ignore
    except Exception as exc:
        print(f"ERROR: could not import lesson seeds: {exc}")
        return 1

    async with AsyncSessionLocal() as session:
        try:
            upserted = await seed_default_lessons(session)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            print(f"ERROR: seeding failed: {exc}")
            return 1

    print(f"Database ready: {upserted} lessons upserted")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

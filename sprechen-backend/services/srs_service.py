"""SuperMemo-2 spaced-repetition service."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import VocabularyCard


def calculate_next_review(card: VocabularyCard, quality: int) -> dict:
    """SM-2 algorithm. Returns the new SRS state for the card.

    Args:
        card: existing VocabularyCard (read its current ease/interval/reps).
        quality: 0..5 self-assessed recall quality.
    """
    quality = max(0, min(5, int(quality)))

    repetitions = int(card.repetitions or 0)
    interval = int(card.interval_days or 1)
    ease = float(card.ease_factor or 2.5)

    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = max(1, round(interval * ease))
        repetitions += 1

    ease = max(
        1.3,
        ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02),
    )

    next_review_at = datetime.utcnow() + timedelta(days=interval)

    return {
        "next_review_at": next_review_at,
        "interval_days": interval,
        "ease_factor": round(ease, 4),
        "repetitions": repetitions,
    }


async def get_due_cards(db: AsyncSession) -> List[VocabularyCard]:
    """Cards whose next_review_at <= now, soonest first, capped at 50."""
    stmt = (
        select(VocabularyCard)
        .where(VocabularyCard.next_review_at <= datetime.utcnow())
        .order_by(VocabularyCard.next_review_at.asc())
        .limit(50)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def bulk_add_from_lesson(
    vocab_list: List[dict], lesson_id: int, db: AsyncSession
) -> List[VocabularyCard]:
    """Insert new cards from a lesson, skipping any german_word already present."""
    if not vocab_list:
        return []

    incoming_words = {v.get("word", "").strip() for v in vocab_list if v.get("word")}
    if not incoming_words:
        return []

    existing_stmt = select(VocabularyCard.german_word).where(
        VocabularyCard.german_word.in_(incoming_words)
    )
    existing = {
        row[0] for row in (await db.execute(existing_stmt)).all()
    }

    new_cards: List[VocabularyCard] = []
    for v in vocab_list:
        word = (v.get("word") or "").strip()
        if not word or word in existing:
            continue
        new_cards.append(
            VocabularyCard(
                german_word=word,
                english_translation=v.get("translation", ""),
                example_sentence=v.get("example"),
                phonetic=v.get("phonetic"),
                source_lesson_id=lesson_id,
            )
        )

    if new_cards:
        db.add_all(new_cards)
        await db.commit()
        for c in new_cards:
            await db.refresh(c)
    return new_cards

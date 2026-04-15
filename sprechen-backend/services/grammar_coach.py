"""Grammar analysis and targeted practice for the Sprechen learner."""
from __future__ import annotations

import json
import re
from typing import List, Optional

import structlog
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from models.orm_models import GrammarError

logger = structlog.get_logger(__name__)


GRAMMAR_RULES = {
    "noun_gender": {
        "id": "noun_gender",
        "name": "Substantivgenus (der/die/das)",
        "explanation": (
            "Jedes deutsche Substantiv hat ein grammatisches Geschlecht: "
            "maskulin (der), feminin (die) oder neutrum (das). "
            "Das Genus bestimmt Artikel, Pronomen und Adjektivendungen."
        ),
        "formula": "Substantiv → der / die / das",
        "examples": [
            "der Tisch (table, masculine)",
            "die Lampe (lamp, feminine)",
            "das Buch (book, neuter)",
        ],
        "difficulty": "A1",
    },
    "nominative_case": {
        "id": "nominative_case",
        "name": "Nominativ",
        "explanation": (
            "Der Nominativ ist der Fall des Subjekts. Er antwortet auf die Frage "
            "'Wer oder was?'. Artikel: der/die/das, ein/eine/ein."
        ),
        "formula": "Subjekt + Verb + ... → 'Wer/was macht etwas?'",
        "examples": [
            "Der Mann liest.",
            "Eine Frau kommt.",
            "Das Kind schläft.",
        ],
        "difficulty": "A1",
    },
    "accusative_case": {
        "id": "accusative_case",
        "name": "Akkusativ",
        "explanation": (
            "Der Akkusativ ist der Fall des direkten Objekts. Er antwortet auf "
            "'Wen oder was?'. Maskulin ändert sich: der → den, ein → einen."
        ),
        "formula": "Subjekt + Verb + Akkusativobjekt",
        "examples": [
            "Ich sehe den Mann.",
            "Sie kauft einen Apfel.",
            "Wir lesen das Buch.",
        ],
        "difficulty": "A2",
    },
    "dative_case": {
        "id": "dative_case",
        "name": "Dativ",
        "explanation": (
            "Der Dativ ist der Fall des indirekten Objekts. Er antwortet auf "
            "'Wem?'. Artikel: dem/der/dem, einem/einer/einem. Plural: den ...n."
        ),
        "formula": "Subjekt + Verb + Dativobjekt + Akkusativobjekt",
        "examples": [
            "Ich gebe dem Kind einen Apfel.",
            "Er hilft seiner Mutter.",
            "Wir danken den Lehrern.",
        ],
        "difficulty": "A2",
    },
    "genitive_case": {
        "id": "genitive_case",
        "name": "Genitiv",
        "explanation": (
            "Der Genitiv zeigt Besitz oder Zugehörigkeit ('wessen?'). Artikel: "
            "des/der/des, eines/einer/eines. Maskulin/Neutrum bekommen meist -s/-es."
        ),
        "formula": "Substantiv + des/der/des + Substantiv(-s)",
        "examples": [
            "Das Auto des Mannes ist neu.",
            "Die Farbe der Blume ist rot.",
            "Der Titel des Buches ist lang.",
        ],
        "difficulty": "B1",
    },
    "present_tense_regular": {
        "id": "present_tense_regular",
        "name": "Präsens (regelmäßige Verben)",
        "explanation": (
            "Regelmäßige Verben im Präsens haben feste Endungen: "
            "-e, -st, -t, -en, -t, -en für ich/du/er/wir/ihr/sie."
        ),
        "formula": "Stamm + Endung (-e/-st/-t/-en/-t/-en)",
        "examples": [
            "ich lerne, du lernst, er lernt",
            "wir spielen, ihr spielt, sie spielen",
            "ich arbeite, du arbeitest (mit -e- bei -t/-d Stamm)",
        ],
        "difficulty": "A1",
    },
    "present_tense_irregular": {
        "id": "present_tense_irregular",
        "name": "Präsens (unregelmäßige Verben)",
        "explanation": (
            "Viele Verben ändern den Stammvokal in der 2./3. Person Singular: "
            "a → ä, e → i/ie."
        ),
        "formula": "Vokalwechsel im Stamm bei du/er/sie/es",
        "examples": [
            "fahren: ich fahre, du fährst, er fährt",
            "sprechen: ich spreche, du sprichst, er spricht",
            "lesen: ich lese, du liest, er liest",
        ],
        "difficulty": "A1",
    },
    "perfekt_haben": {
        "id": "perfekt_haben",
        "name": "Perfekt mit haben",
        "explanation": (
            "Die meisten Verben bilden das Perfekt mit 'haben' + Partizip II. "
            "Das Partizip steht am Satzende."
        ),
        "formula": "Subjekt + haben + ... + Partizip II",
        "examples": [
            "Ich habe das Buch gelesen.",
            "Wir haben Pizza gegessen.",
            "Sie hat einen Brief geschrieben.",
        ],
        "difficulty": "A2",
    },
    "perfekt_sein": {
        "id": "perfekt_sein",
        "name": "Perfekt mit sein",
        "explanation": (
            "Verben der Bewegung oder Zustandsänderung bilden das Perfekt mit "
            "'sein' + Partizip II. Auch 'sein', 'bleiben', 'werden'."
        ),
        "formula": "Subjekt + sein + ... + Partizip II",
        "examples": [
            "Ich bin nach Berlin gefahren.",
            "Er ist früh aufgestanden.",
            "Wir sind zu Hause geblieben.",
        ],
        "difficulty": "A2",
    },
    "praeteritum": {
        "id": "praeteritum",
        "name": "Präteritum",
        "explanation": (
            "Das Präteritum ist die schriftliche Vergangenheitsform. In der "
            "gesprochenen Sprache benutzt man es vor allem bei sein, haben und "
            "Modalverben."
        ),
        "formula": "Stamm + (-te für regelmäßig) / unregelmäßiger Stamm",
        "examples": [
            "Ich war gestern müde.",
            "Wir hatten viel zu tun.",
            "Er konnte nicht kommen.",
        ],
        "difficulty": "B1",
    },
    "futur_I": {
        "id": "futur_I",
        "name": "Futur I",
        "explanation": (
            "Futur I drückt Zukunft, Absicht oder Vermutung aus. Es wird mit "
            "'werden' + Infinitiv gebildet. In der Umgangssprache nutzt man oft Präsens."
        ),
        "formula": "Subjekt + werden + ... + Infinitiv",
        "examples": [
            "Ich werde morgen nach Hamburg fahren.",
            "Er wird wohl zu Hause sein.",
            "Wir werden bald heiraten.",
        ],
        "difficulty": "A2",
    },
    "modal_verbs": {
        "id": "modal_verbs",
        "name": "Modalverben",
        "explanation": (
            "Modalverben (können, müssen, dürfen, wollen, sollen, mögen) "
            "verändern die Bedeutung anderer Verben. Der Infinitiv steht am Satzende."
        ),
        "formula": "Subjekt + Modalverb + ... + Infinitiv",
        "examples": [
            "Ich kann gut Deutsch sprechen.",
            "Du musst die Hausaufgaben machen.",
            "Wir wollen ins Kino gehen.",
        ],
        "difficulty": "A2",
    },
    "reflexive_verbs": {
        "id": "reflexive_verbs",
        "name": "Reflexive Verben",
        "explanation": (
            "Reflexive Verben verlangen ein Reflexivpronomen (mich, dich, sich, "
            "uns, euch, sich), das meist im Akkusativ steht."
        ),
        "formula": "Subjekt + Verb + Reflexivpronomen",
        "examples": [
            "Ich wasche mich jeden Morgen.",
            "Er freut sich über das Geschenk.",
            "Wir beeilen uns.",
        ],
        "difficulty": "A2",
    },
    "separable_verbs": {
        "id": "separable_verbs",
        "name": "Trennbare Verben",
        "explanation": (
            "Bei trennbaren Verben wird das Präfix im Hauptsatz vom Verb getrennt "
            "und steht am Satzende. Im Nebensatz bleibt das Verb zusammen."
        ),
        "formula": "Verb steht an Position 2, Präfix am Satzende",
        "examples": [
            "Ich rufe dich morgen an.",
            "Der Zug kommt um acht Uhr an.",
            "Sie steht jeden Tag früh auf.",
        ],
        "difficulty": "A2",
    },
    "adjective_endings_nominative": {
        "id": "adjective_endings_nominative",
        "name": "Adjektivendungen im Nominativ",
        "explanation": (
            "Nach bestimmtem Artikel: -e (der gute Mann, die gute Frau, das gute Kind). "
            "Nach unbestimmtem Artikel: -er/-e/-es."
        ),
        "formula": "Artikel + Adjektiv + Substantiv",
        "examples": [
            "Der nette Mann hilft mir.",
            "Eine schöne Frau singt.",
            "Ein kleines Kind spielt.",
        ],
        "difficulty": "A2",
    },
    "adjective_endings_accusative": {
        "id": "adjective_endings_accusative",
        "name": "Adjektivendungen im Akkusativ",
        "explanation": (
            "Im Akkusativ ändert sich nur die maskuline Form: -en. Feminin und "
            "neutrum bleiben wie im Nominativ."
        ),
        "formula": "den/einen + Adjektiv-en + Substantiv (mask.)",
        "examples": [
            "Ich sehe den netten Mann.",
            "Sie kauft eine schöne Tasche.",
            "Er liest ein interessantes Buch.",
        ],
        "difficulty": "A2",
    },
    "adjective_endings_dative": {
        "id": "adjective_endings_dative",
        "name": "Adjektivendungen im Dativ",
        "explanation": (
            "Im Dativ enden Adjektive nach Artikel meist auf -en. Plural-Substantive "
            "bekommen ein zusätzliches -n."
        ),
        "formula": "dem/der/dem + Adjektiv-en + Substantiv",
        "examples": [
            "Ich helfe dem alten Mann.",
            "Sie spricht mit der netten Frau.",
            "Wir spielen mit den kleinen Kindern.",
        ],
        "difficulty": "B1",
    },
    "word_order_V2": {
        "id": "word_order_V2",
        "name": "Verbposition im Hauptsatz (V2)",
        "explanation": (
            "Im deutschen Hauptsatz steht das konjugierte Verb immer an Position 2, "
            "egal was an Position 1 steht."
        ),
        "formula": "[Position 1] [Verb] [Subjekt/Rest] ...",
        "examples": [
            "Heute gehe ich ins Kino.",
            "Morgen fährt er nach Berlin.",
            "Ich lese ein Buch.",
        ],
        "difficulty": "A1",
    },
    "subordinate_word_order": {
        "id": "subordinate_word_order",
        "name": "Verbposition im Nebensatz",
        "explanation": (
            "In Nebensätzen mit Konjunktionen wie 'weil', 'dass', 'wenn', 'obwohl' "
            "steht das konjugierte Verb am Ende."
        ),
        "formula": "..., Konjunktion + Subjekt + ... + Verb",
        "examples": [
            "Ich bleibe zu Hause, weil ich krank bin.",
            "Er sagt, dass er morgen kommt.",
            "Wenn es regnet, nehme ich den Schirm.",
        ],
        "difficulty": "B1",
    },
    "konjunktiv_II": {
        "id": "konjunktiv_II",
        "name": "Konjunktiv II",
        "explanation": (
            "Konjunktiv II drückt Wünsche, Hypothesen und höfliche Bitten aus. "
            "Synthetisch: wäre, hätte, könnte, müsste. Analytisch: würde + Infinitiv."
        ),
        "formula": "wäre/hätte/könnte ... ODER würde + Infinitiv",
        "examples": [
            "Ich hätte gerne einen Kaffee.",
            "An deiner Stelle würde ich das nicht tun.",
            "Wenn ich Zeit hätte, würde ich kommen.",
        ],
        "difficulty": "B2",
    },
}


class GrammarCoach:
    def __init__(self) -> None:
        self._settings = get_settings()
        from groq import AsyncGroq

        self._client = AsyncGroq(api_key=self._settings.groq_api_key or "missing-key")

    # ---------- analyze ----------
    async def analyze_text(self, text: str, db: AsyncSession) -> dict:
        rule_ids = ", ".join(GRAMMAR_RULES.keys())
        prompt = (
            "Du bist ein deutscher Grammatiklehrer. Analysiere den folgenden "
            "Text auf Grammatikfehler.\n\n"
            f"TEXT:\n{text}\n\n"
            "Antworte NUR mit JSON in genau diesem Format:\n"
            "{\n"
            '  "errors": [\n'
            '    {"original": "fehlerhafter Satzteil", "corrected": "korrekte Form", '
            '"rule_id": "<einer dieser IDs>", "explanation": "kurze Erklärung auf Deutsch"}\n'
            "  ],\n"
            '  "score": <0-100 Gesamtbewertung>\n'
            "}\n\n"
            f"Verfügbare rule_id Werte: {rule_ids}"
        )
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
        except Exception as exc:
            logger.error("grammar_analyze_failed", error=str(exc))
            return {"errors": [], "score": 0, "error": "analysis_unavailable"}

        errors = data.get("errors") or []
        for err in errors:
            try:
                db.add(
                    GrammarError(
                        rule_id=err.get("rule_id", "unknown"),
                        original_text=err.get("original", ""),
                        corrected_text=err.get("corrected", ""),
                    )
                )
            except Exception:
                continue
        try:
            await db.commit()
        except Exception:
            await db.rollback()

        return {
            "errors": errors,
            "score": float(data.get("score", 0)),
        }

    # ---------- weak areas ----------
    async def get_weak_areas(self, db: AsyncSession) -> List[dict]:
        stmt = (
            select(GrammarError.rule_id, func.count(GrammarError.id).label("c"))
            .group_by(GrammarError.rule_id)
            .order_by(desc("c"))
            .limit(3)
        )
        rows = (await db.execute(stmt)).all()
        out: List[dict] = []
        for rule_id, count in rows:
            out.append(
                {
                    "rule_id": rule_id,
                    "count": int(count),
                    "rule": GRAMMAR_RULES.get(rule_id),
                }
            )
        return out

    # ---------- targeted exercise ----------
    async def generate_targeted_exercise(self, rule_id: str, level: str) -> dict:
        rule = GRAMMAR_RULES.get(rule_id)
        if rule is None:
            return {"error": f"unknown rule_id '{rule_id}'"}

        prompt = (
            f"Erstelle eine fill_in_blank Übung für die Grammatikregel "
            f"'{rule['name']}' auf dem Niveau {level}.\n"
            f"Regel: {rule['explanation']}\n"
            f"Formel: {rule['formula']}\n\n"
            "Gib NUR JSON zurück:\n"
            '{"type":"fill_in_blank","sentence_with_blank":"Satz mit ___","'
            'options":["a","b","c","d"],"correct_index":0,"hint":"kurzer Hinweis"}'
        )
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=400,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
            data.setdefault("type", "fill_in_blank")
            return data
        except Exception as exc:
            logger.error("targeted_exercise_failed", error=str(exc))
            return {"error": "generation_failed"}


_grammar_coach: Optional[GrammarCoach] = None


def get_grammar_coach() -> GrammarCoach:
    global _grammar_coach
    if _grammar_coach is None:
        _grammar_coach = GrammarCoach()
    return _grammar_coach

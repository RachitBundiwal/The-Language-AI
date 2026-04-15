"""Pydantic schemas describing the full structure of a Sprechen lesson."""
from __future__ import annotations

from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


# ---------- Vocabulary / phonetics ----------
class Vocabulary(BaseModel):
    word: str
    translation: str
    phonetic: Optional[str] = None
    example_sentence: str


class PhonemeHint(BaseModel):
    phoneme: str
    tip: str


# ---------- Dialogue ----------
class DialogueTurn(BaseModel):
    role: Literal["native", "learner"]
    german: str
    english: str
    vocabulary: List[Vocabulary] = Field(default_factory=list)
    pronunciation_tips: List[PhonemeHint] = Field(default_factory=list)


# ---------- Grammar ----------
class GrammarExample(BaseModel):
    german: str
    english: str
    breakdown: Optional[str] = None


class GrammarFocus(BaseModel):
    rule_name: str
    explanation: str
    formula: str
    examples: List[GrammarExample]
    common_mistakes: List[str] = Field(default_factory=list)


# ---------- Exercises (discriminated union on "type") ----------
class FillInBlankExercise(BaseModel):
    type: Literal["fill_in_blank"] = "fill_in_blank"
    sentence_with_blank: str
    options: List[str]
    correct_index: int
    hint: str = ""


class MultipleChoiceExercise(BaseModel):
    type: Literal["multiple_choice"] = "multiple_choice"
    question: str
    options: List[str]
    correct_index: int
    explanation: str = ""


class ArrangeWordsExercise(BaseModel):
    type: Literal["arrange_words"] = "arrange_words"
    scrambled_words: List[str]
    correct_sentence: str
    hint: str = ""


class TranslateExercise(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    type: Literal["translate"] = "translate"
    source_text: str
    source_lang: str
    target_lang: str
    model_answer: str


class SpeakingPromptExercise(BaseModel):
    type: Literal["speaking_prompt"] = "speaking_prompt"
    prompt_text: str
    expected_topic: str
    min_words: int = 20


class ListeningExercise(BaseModel):
    type: Literal["listening"] = "listening"
    audio_script: str
    questions: List[dict]


Exercise = Annotated[
    Union[
        FillInBlankExercise,
        MultipleChoiceExercise,
        ArrangeWordsExercise,
        TranslateExercise,
        SpeakingPromptExercise,
        ListeningExercise,
    ],
    Field(discriminator="type"),
]


# ---------- Full lesson ----------
class LessonDetail(BaseModel):
    id: int
    title: str
    level: str
    scenario: str
    topic: str
    learning_objectives: List[str]
    estimated_minutes: int
    cultural_note: str
    dialogue: List[DialogueTurn]
    grammar_focus: GrammarFocus
    exercises: List[Exercise]
    vocabulary_list: List[Vocabulary]

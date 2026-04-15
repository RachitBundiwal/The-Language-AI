"""Authentic German lesson seed data for Sprechen.

30 lessons across A1, A2, B1, B2 — each a real CEFR-aligned mini-lesson
with dialogue, grammar focus, vocabulary, exercises, and a cultural note.
"""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Helper builders keep each lesson dict short and consistent.
def _t(role: str, de: str, en: str) -> dict:
    return {"role": role, "german": de, "english": en, "vocabulary": [], "pronunciation_tips": []}


def _v(word: str, translation: str, example: str, phonetic: str | None = None) -> dict:
    return {
        "word": word,
        "translation": translation,
        "phonetic": phonetic,
        "example_sentence": example,
    }


def _ex_fib(sentence: str, options: list, correct: int, hint: str) -> dict:
    return {
        "type": "fill_in_blank",
        "sentence_with_blank": sentence,
        "options": options,
        "correct_index": correct,
        "hint": hint,
    }


def _ex_mc(question: str, options: list, correct: int, explanation: str) -> dict:
    return {
        "type": "multiple_choice",
        "question": question,
        "options": options,
        "correct_index": correct,
        "explanation": explanation,
    }


def _ex_arr(scrambled: list, correct_sentence: str, hint: str) -> dict:
    return {
        "type": "arrange_words",
        "scrambled_words": scrambled,
        "correct_sentence": correct_sentence,
        "hint": hint,
    }


def _ex_tr(source: str, model: str, src_lang: str = "en", tgt_lang: str = "de") -> dict:
    return {
        "type": "translate",
        "source_text": source,
        "source_lang": src_lang,
        "target_lang": tgt_lang,
        "model_answer": model,
    }


def _ex_sp(prompt: str, topic: str, min_words: int = 25) -> dict:
    return {
        "type": "speaking_prompt",
        "prompt_text": prompt,
        "expected_topic": topic,
        "min_words": min_words,
    }


def _gex(de: str, en: str, breakdown: str | None = None) -> dict:
    return {"german": de, "english": en, "breakdown": breakdown}


# =====================================================================
# A1 — 8 lessons
# =====================================================================

LESSON_01 = {
    "title": "Guten Morgen! Sich vorstellen",
    "level": "A1",
    "scenario": "free",
    "topic": "Sich vorstellen und kennenlernen",
    "learning_objectives": [
        "Sich auf Deutsch vorstellen können (Name, Herkunft, Beruf, Hobbys)",
        "Das Verb 'sein' im Präsens vollständig konjugieren",
        "Höflich nach Name, Herkunft und Beruf fragen",
    ],
    "estimated_minutes": 12,
    "cultural_note": (
        "In Germany, it's normal to shake hands when meeting someone for the "
        "first time, even in casual settings. Maintain eye contact and use "
        "the person's last name with 'Herr' or 'Frau' until invited to use "
        "the first name."
    ),
    "dialogue": [
        _t("native", "Guten Morgen! Ich heiße Maria. Wie heißt du?",
           "Good morning! My name is Maria. What's your name?"),
        _t("learner", "Guten Morgen, Maria. Ich heiße Hans. Freut mich, dich kennenzulernen.",
           "Good morning, Maria. My name is Hans. Nice to meet you."),
        _t("native", "Freut mich auch, Hans. Woher kommst du?",
           "Nice to meet you too, Hans. Where are you from?"),
        _t("learner", "Ich komme aus Indien, aus Mumbai. Und du?",
           "I come from India, from Mumbai. And you?"),
        _t("native", "Ich komme aus München. Was machst du beruflich?",
           "I come from Munich. What do you do for a living?"),
        _t("learner", "Ich bin Software-Ingenieur. Und du, was ist dein Beruf?",
           "I'm a software engineer. And you, what's your profession?"),
        _t("native", "Ich bin Lehrerin hier an der Sprachschule. Was sind deine Hobbys?",
           "I'm a teacher here at the language school. What are your hobbies?"),
        _t("learner", "Ich lese gerne und ich spiele Cricket. Was machst du in deiner Freizeit?",
           "I like to read and I play cricket. What do you do in your free time?"),
    ],
    "grammar_focus": {
        "rule_name": "Das Verb 'sein' im Präsens",
        "explanation": (
            "Das wichtigste deutsche Verb ist unregelmäßig. Du musst alle sechs "
            "Formen auswendig lernen: ich bin, du bist, er/sie/es ist, wir sind, "
            "ihr seid, sie/Sie sind."
        ),
        "formula": "Subjekt + Form von 'sein' + Ergänzung",
        "examples": [
            _gex("Ich bin Hans.", "I am Hans."),
            _gex("Du bist Studentin.", "You are a student."),
            _gex("Wir sind aus Deutschland.", "We are from Germany."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich bin Student sein.' — sein wird nicht doppelt benutzt.",
            "Falsch: 'Du bin nett.' — Personalpronomen und Verb müssen übereinstimmen.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ Hans.", ["bin", "bist", "ist", "sind"], 0,
                "Erste Person Singular von 'sein'."),
        _ex_mc("Woher kommen Sie?",
               ["Aus Berlin.", "Auf Berlin.", "Im Berlin.", "Bei Berlin."], 0,
               "Bei Herkunft benutzt man die Präposition 'aus'."),
        _ex_arr(["ist", "Mein", "Maria", "Müller", "Name"],
                "Mein Name ist Maria Müller.",
                "Verb an Position 2 im Hauptsatz."),
        _ex_tr("What is your name?", "Wie heißen Sie?"),
        _ex_sp("Stell dich vor: Sage deinen Namen, woher du kommst, was du beruflich machst und was deine Hobbys sind.",
               "self-introduction", 30),
    ],
    "vocabulary_list": [
        _v("der Name", "the name", "Mein Name ist Hans."),
        _v("kommen aus", "to come from", "Ich komme aus Mumbai."),
        _v("der Beruf", "the profession", "Was ist dein Beruf?"),
        _v("das Hobby", "the hobby", "Mein Hobby ist Lesen."),
        _v("heißen", "to be called", "Wie heißt du?"),
        _v("wohnen", "to live (reside)", "Ich wohne in Berlin."),
        _v("studieren", "to study (university)", "Ich studiere Informatik."),
        _v("arbeiten", "to work", "Sie arbeitet bei Siemens."),
        _v("alt sein", "to be old (age)", "Ich bin 28 Jahre alt."),
        _v("die Sprache", "the language", "Deutsch ist eine schöne Sprache."),
        _v("lernen", "to learn", "Ich lerne Deutsch."),
        _v("verstehen", "to understand", "Ich verstehe nicht alles."),
    ],
}

LESSON_02 = {
    "title": "Im Café — Zahlen und Bestellen",
    "level": "A1",
    "scenario": "restaurant",
    "topic": "Bestellen und bezahlen",
    "learning_objectives": [
        "Im Café höflich bestellen können",
        "Zahlen von 1 bis 20 verstehen und sprechen",
        "Nach dem Preis fragen und bezahlen",
    ],
    "estimated_minutes": 12,
    "cultural_note": (
        "Tipping (Trinkgeld) in Germany is informal: round up the bill or add "
        "5–10%. You usually tell the server the total amount you want to pay "
        "instead of leaving cash on the table. Say 'Stimmt so' if you want them "
        "to keep the change."
    ),
    "dialogue": [
        _t("native", "Guten Tag! Was darf es sein?",
           "Good day! What would you like?"),
        _t("learner", "Guten Tag. Ich möchte bitte einen Kaffee und ein Stück Apfelkuchen.",
           "Good day. I'd like a coffee and a piece of apple cake, please."),
        _t("native", "Sehr gerne. Möchten Sie den Kaffee mit Milch und Zucker?",
           "Of course. Would you like the coffee with milk and sugar?"),
        _t("learner", "Mit Milch, bitte. Ohne Zucker. Was kostet das zusammen?",
           "With milk, please. No sugar. How much is it altogether?"),
        _t("native", "Der Kaffee kostet drei Euro fünfzig und der Kuchen vier Euro. Das macht sieben Euro fünfzig.",
           "The coffee is three fifty and the cake is four euros. That's seven fifty."),
        _t("learner", "Hier sind zehn Euro. Stimmt so, danke.",
           "Here's ten euros. Keep the change, thank you."),
        _t("native", "Vielen Dank! Einen schönen Tag noch.",
           "Thank you very much! Have a nice day."),
    ],
    "grammar_focus": {
        "rule_name": "Höfliche Bestellung mit 'möchten'",
        "explanation": (
            "Um etwas höflich zu bestellen, benutzt man 'ich möchte' (Konjunktiv II "
            "von 'mögen'). Der Akkusativ steht hinter dem Verb. 'Das kostet...' "
            "fragt nach dem Preis."
        ),
        "formula": "Ich möchte + Akkusativobjekt + bitte",
        "examples": [
            _gex("Ich möchte einen Kaffee, bitte.", "I would like a coffee, please."),
            _gex("Wir möchten die Rechnung.", "We would like the bill."),
            _gex("Was kostet das Stück Kuchen?", "How much is the piece of cake?"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich will Kaffee.' — direkt, unhöflich. Besser: 'Ich möchte einen Kaffee.'",
            "Falsch: 'einen Kaffee kostet'. Richtig: 'Der Kaffee kostet'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ einen Kaffee, bitte.",
                ["möchte", "möchtest", "mag", "habe"], 0,
                "Erste Person Singular der höflichen Form."),
        _ex_mc("Was bedeutet 'Stimmt so'?",
               ["Keep the change.", "It's correct.", "I agree.", "Pay later."], 0,
               "Idiomatisch beim Bezahlen — der Rest ist Trinkgeld."),
        _ex_arr(["kostet", "Wie", "viel", "das"],
                "Wie viel kostet das?",
                "Frageform mit 'wie viel' am Anfang."),
        _ex_tr("How much is the coffee?", "Was kostet der Kaffee?"),
        _ex_sp("Bestelle in einem Café einen Kaffee und ein Stück Kuchen, frage nach dem Preis und bezahle.",
               "ordering at a cafe", 30),
    ],
    "vocabulary_list": [
        _v("der Kaffee", "the coffee", "Ich trinke gerne Kaffee."),
        _v("der Kuchen", "the cake", "Der Apfelkuchen schmeckt gut."),
        _v("bestellen", "to order", "Ich bestelle einen Tee."),
        _v("kosten", "to cost", "Was kostet das?"),
        _v("bezahlen", "to pay", "Ich möchte bitte bezahlen."),
        _v("das Wechselgeld", "the change", "Hier ist Ihr Wechselgeld."),
        _v("bitte", "please", "Einen Tee, bitte."),
        _v("danke", "thank you", "Vielen Dank!"),
        _v("der Kellner", "the waiter", "Der Kellner ist sehr freundlich."),
        _v("die Rechnung", "the bill", "Die Rechnung, bitte."),
    ],
}

LESSON_03 = {
    "title": "Farben und Kleidung einkaufen",
    "level": "A1",
    "scenario": "supermarket",
    "topic": "Kleidung und Farben",
    "learning_objectives": [
        "Farben auf Deutsch nennen",
        "Nach Größen und Farben fragen",
        "Adjektive im Nominativ richtig dekliniert verwenden",
    ],
    "estimated_minutes": 13,
    "cultural_note": (
        "German clothing sizes differ from US/Indian sizes. Quick reference: "
        "US S = DE 36 (women) / DE 46 (men); US M = DE 38 / 48; US L = DE 40 / 50. "
        "Shoe sizes also differ: US 9 (men) ≈ DE 42."
    ),
    "dialogue": [
        _t("native", "Guten Tag, kann ich Ihnen helfen?",
           "Good day, can I help you?"),
        _t("learner", "Ja, ich suche eine rote Jacke. Haben Sie die in Größe 38?",
           "Yes, I'm looking for a red jacket. Do you have it in size 38?"),
        _t("native", "Einen Moment, bitte. Ja, hier ist eine rote Jacke in Größe 38.",
           "One moment, please. Yes, here is a red jacket in size 38."),
        _t("learner", "Darf ich sie anprobieren? Und haben Sie auch einen blauen Pullover?",
           "May I try it on? And do you also have a blue sweater?"),
        _t("native", "Natürlich. Die Umkleidekabine ist dort drüben. Der blaue Pullover kostet 35 Euro.",
           "Of course. The fitting room is over there. The blue sweater costs 35 euros."),
        _t("learner", "Sehr gut. Ich nehme die Jacke und den Pullover.",
           "Very good. I'll take the jacket and the sweater."),
    ],
    "grammar_focus": {
        "rule_name": "Adjektivendungen im Nominativ (unbestimmter Artikel)",
        "explanation": (
            "Nach 'ein/eine/ein' bekommt das Adjektiv die Endung des fehlenden "
            "Artikels: -er (mask.), -e (fem.), -es (neut.)."
        ),
        "formula": "ein + Adjektiv + Substantiv → -er/-e/-es",
        "examples": [
            _gex("ein roter Pullover", "a red sweater", "mask. → -er"),
            _gex("eine rote Jacke", "a red jacket", "fem. → -e"),
            _gex("ein rotes Hemd", "a red shirt", "neut. → -es"),
        ],
        "common_mistakes": [
            "Falsch: 'eine rot Jacke'. Richtig: 'eine rote Jacke'.",
            "Falsch: 'ein rote Pullover'. Richtig: 'ein roter Pullover'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich suche einen ___ Pullover.",
                ["blauer", "blaue", "blaues", "blau"], 0,
                "Maskulin, Nominativ, unbestimmt."),
        _ex_mc("Welche Farbe hat der Himmel?",
               ["blau", "rot", "grün", "gelb"], 0,
               "Standardantwort: der Himmel ist blau."),
        _ex_arr(["eine", "möchte", "Ich", "Jacke", "rote"],
                "Ich möchte eine rote Jacke.",
                "Ich + Verb + Akkusativobjekt mit Adjektiv."),
        _ex_tr("Do you have this in size 40?", "Haben Sie das in Größe 40?"),
        _ex_sp("Du bist im Bekleidungsgeschäft. Frage nach einer Hose in deiner Größe und Lieblingsfarbe.",
               "shopping for clothes", 25),
    ],
    "vocabulary_list": [
        _v("die Jacke", "the jacket", "Die Jacke ist warm."),
        _v("der Pullover", "the sweater", "Der Pullover ist weich."),
        _v("die Hose", "the trousers", "Die Hose ist neu."),
        _v("das Hemd", "the shirt", "Das Hemd ist weiß."),
        _v("die Größe", "the size", "Welche Größe haben Sie?"),
        _v("anprobieren", "to try on", "Darf ich das anprobieren?"),
        _v("rot", "red", "Ich mag rote Schuhe."),
        _v("blau", "blue", "Der Himmel ist blau."),
        _v("grün", "green", "Das Gras ist grün."),
        _v("schwarz", "black", "Die Tasche ist schwarz."),
        _v("weiß", "white", "Mein Hemd ist weiß."),
        _v("die Umkleidekabine", "the fitting room", "Wo ist die Umkleidekabine?"),
    ],
}

LESSON_04 = {
    "title": "Meine Familie vorstellen",
    "level": "A1",
    "scenario": "free",
    "topic": "Familie und Possessivpronomen",
    "learning_objectives": [
        "Familienmitglieder benennen",
        "Possessivpronomen im Nominativ verwenden",
        "Das Alter und den Beruf von Familienmitgliedern angeben",
    ],
    "estimated_minutes": 12,
    "cultural_note": (
        "German families tend to be smaller than in many other cultures. "
        "When asked about siblings, it's normal to give a one-sentence answer "
        "rather than a long story. 'Schwiegereltern' (in-laws) and 'Geschwister' "
        "(siblings) are common everyday words."
    ),
    "dialogue": [
        _t("native", "Hast du Geschwister?",
           "Do you have siblings?"),
        _t("learner", "Ja, ich habe einen Bruder und eine Schwester. Mein Bruder heißt Raj und meine Schwester heißt Priya.",
           "Yes, I have a brother and a sister. My brother's name is Raj and my sister's name is Priya."),
        _t("native", "Wie alt sind sie?",
           "How old are they?"),
        _t("learner", "Mein Bruder ist 32 Jahre alt und meine Schwester ist 25. Und du? Hast du auch Geschwister?",
           "My brother is 32 years old and my sister is 25. And you? Do you also have siblings?"),
        _t("native", "Nein, ich bin Einzelkind. Aber ich habe viele Cousinen. Was machen deine Eltern beruflich?",
           "No, I'm an only child. But I have many cousins. What do your parents do for a living?"),
        _t("learner", "Mein Vater ist Lehrer und meine Mutter ist Ärztin. Sie wohnen in Mumbai.",
           "My father is a teacher and my mother is a doctor. They live in Mumbai."),
    ],
    "grammar_focus": {
        "rule_name": "Possessivpronomen im Nominativ",
        "explanation": (
            "Possessivpronomen zeigen Besitz: mein/dein/sein/ihr/unser/euer/ihr. "
            "Im Nominativ enden sie wie der unbestimmte Artikel: -∅ (mask.), "
            "-e (fem.), -∅ (neut.), -e (Plural)."
        ),
        "formula": "mein/dein/... + (-e bei fem. und Plural) + Substantiv",
        "examples": [
            _gex("Mein Bruder ist groß.", "My brother is tall.", "mask. → mein"),
            _gex("Meine Schwester ist klein.", "My sister is short.", "fem. → meine"),
            _gex("Mein Kind spielt.", "My child is playing.", "neut. → mein"),
        ],
        "common_mistakes": [
            "Falsch: 'meine Bruder'. Richtig: 'mein Bruder' (mask.).",
            "Falsch: 'mein Schwester'. Richtig: 'meine Schwester' (fem.).",
        ],
    },
    "exercises": [
        _ex_fib("___ Mutter ist Ärztin.",
                ["Meine", "Mein", "Meines", "Meiner"], 0,
                "Mutter ist feminin → meine."),
        _ex_mc("Wie sagt man 'my brother' auf Deutsch?",
               ["mein Bruder", "meine Bruder", "meines Bruder", "meinem Bruder"], 0,
               "Bruder ist maskulin und steht im Nominativ."),
        _ex_arr(["habe", "Ich", "Schwester", "eine"],
                "Ich habe eine Schwester.",
                "haben + Akkusativ."),
        _ex_tr("My father is a teacher.", "Mein Vater ist Lehrer."),
        _ex_sp("Beschreibe deine Familie: Wer gehört dazu, wie alt sind sie und was machen sie beruflich?",
               "family introduction", 35),
    ],
    "vocabulary_list": [
        _v("die Familie", "the family", "Meine Familie ist groß."),
        _v("der Vater", "the father", "Mein Vater arbeitet."),
        _v("die Mutter", "the mother", "Meine Mutter kocht gut."),
        _v("der Bruder", "the brother", "Ich habe einen Bruder."),
        _v("die Schwester", "the sister", "Meine Schwester studiert."),
        _v("die Eltern", "the parents", "Meine Eltern wohnen in Indien."),
        _v("die Geschwister", "the siblings", "Hast du Geschwister?"),
        _v("das Kind", "the child", "Das Kind spielt im Garten."),
        _v("der Großvater", "the grandfather", "Mein Großvater ist 80."),
        _v("die Großmutter", "the grandmother", "Meine Großmutter backt Kuchen."),
        _v("verheiratet", "married", "Sie ist verheiratet."),
        _v("ledig", "single", "Mein Bruder ist ledig."),
    ],
}

LESSON_05 = {
    "title": "Im Restaurant essen gehen",
    "level": "A1",
    "scenario": "restaurant",
    "topic": "Im Restaurant bestellen",
    "learning_objectives": [
        "Eine Speisekarte verstehen und auswählen",
        "Höflich bestellen mit 'Ich hätte gerne...'",
        "Diätwünsche und Sonderwünsche äußern",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "German restaurants do not split bills automatically. Tell the server "
        "'zusammen' (together, one bill) or 'getrennt' (separately, each person "
        "pays their own). Vegetarian and vegan options are increasingly common, "
        "but in traditional Gasthäuser you may still need to ask explicitly."
    ),
    "dialogue": [
        _t("native", "Guten Abend, haben Sie eine Reservierung?",
           "Good evening, do you have a reservation?"),
        _t("learner", "Ja, auf den Namen Sharma, einen Tisch für zwei Personen.",
           "Yes, under the name Sharma, a table for two people."),
        _t("native", "Sehr gut. Hier ist die Speisekarte. Möchten Sie schon etwas trinken?",
           "Very good. Here is the menu. Would you like something to drink already?"),
        _t("learner", "Ich hätte gerne ein Mineralwasser. Haben Sie vegetarische Gerichte?",
           "I would like a sparkling water. Do you have vegetarian dishes?"),
        _t("native", "Selbstverständlich. Heute empfehle ich die Pilzpfanne mit Kartoffeln.",
           "Of course. Today I recommend the mushroom pan with potatoes."),
        _t("learner", "Das klingt gut. Ich nehme die Pilzpfanne, ohne Sahne bitte.",
           "That sounds good. I'll have the mushroom pan, without cream please."),
    ],
    "grammar_focus": {
        "rule_name": "Höfliche Bestellung: 'Ich hätte gerne...'",
        "explanation": (
            "'Ich hätte gerne' ist eine sehr höfliche Bestellform (Konjunktiv II "
            "von 'haben'). Mit 'Bringen Sie mir bitte...' gibt man eine höfliche "
            "Anweisung. 'Ohne...' drückt einen Sonderwunsch aus."
        ),
        "formula": "Ich hätte gerne + Akkusativobjekt (+ Sonderwunsch)",
        "examples": [
            _gex("Ich hätte gerne ein Bier.", "I'd like a beer."),
            _gex("Bringen Sie mir bitte die Speisekarte.", "Please bring me the menu."),
            _gex("Ohne Fleisch, bitte.", "Without meat, please."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich habe gerne'. Richtig: 'Ich hätte gerne' (Konjunktiv II).",
            "Falsch: 'Ohne Fleisch bitte zu essen'. Einfach: 'Ohne Fleisch, bitte.'",
        ],
    },
    "exercises": [
        _ex_fib("___ gerne einen Salat.",
                ["Ich hätte", "Ich habe", "Ich bin", "Ich will"], 0,
                "Höflich bestellen mit Konjunktiv II."),
        _ex_mc("Wie sagt man höflich 'ich will einen Tisch'?",
               ["Ich hätte gerne einen Tisch.", "Ich gebe einen Tisch.",
                "Ich bin ein Tisch.", "Ich Tisch will."], 0,
               "Konjunktiv II ist die höflichste Form."),
        _ex_arr(["die", "bitte", "Rechnung,", "Bringen", "mir", "Sie"],
                "Bringen Sie mir bitte die Rechnung.",
                "Imperativ + Dativ + Akkusativ."),
        _ex_tr("Could I have the menu, please?", "Könnte ich bitte die Speisekarte haben?"),
        _ex_sp("Bestelle ein Abendessen in einem Restaurant. Wähle eine Vorspeise, ein Hauptgericht und ein Getränk.",
               "ordering dinner", 40),
    ],
    "vocabulary_list": [
        _v("die Speisekarte", "the menu", "Die Speisekarte, bitte."),
        _v("die Vorspeise", "the starter", "Als Vorspeise nehme ich Suppe."),
        _v("das Hauptgericht", "the main course", "Mein Hauptgericht ist Fisch."),
        _v("die Nachspeise", "the dessert", "Zur Nachspeise gibt es Eis."),
        _v("vegetarisch", "vegetarian", "Ich esse vegetarisch."),
        _v("das Mineralwasser", "the sparkling water", "Ein Mineralwasser, bitte."),
        _v("das Bier", "the beer", "Ein Bier vom Fass, bitte."),
        _v("die Rechnung", "the bill", "Die Rechnung, bitte."),
        _v("zusammen", "together (one bill)", "Wir zahlen zusammen."),
        _v("getrennt", "separately", "Wir möchten getrennt zahlen."),
        _v("schmecken", "to taste", "Es schmeckt sehr gut."),
        _v("empfehlen", "to recommend", "Was empfehlen Sie?"),
    ],
}

LESSON_06 = {
    "title": "Uhrzeiten und Wochentage",
    "level": "A1",
    "scenario": "free",
    "topic": "Zeit und Wochenplanung",
    "learning_objectives": [
        "Die Uhrzeit formell und informell angeben",
        "Wochentage und Tageszeiten benennen",
        "Termine und Pläne vereinbaren",
    ],
    "estimated_minutes": 13,
    "cultural_note": (
        "Germans are punctual — being 5 minutes early is on time, being on time "
        "is late. For business and official appointments, the 24-hour clock is "
        "standard ('14:30' = vierzehn Uhr dreißig). Informally, people say "
        "'halb drei' (half to three = 14:30)."
    ),
    "dialogue": [
        _t("native", "Was machst du am Samstag?",
           "What are you doing on Saturday?"),
        _t("learner", "Am Samstag habe ich nichts vor. Warum?",
           "I have nothing planned on Saturday. Why?"),
        _t("native", "Wir gehen ins Kino. Hast du Lust mitzukommen?",
           "We're going to the cinema. Do you feel like coming along?"),
        _t("learner", "Gerne! Um wie viel Uhr beginnt der Film?",
           "Gladly! At what time does the film start?"),
        _t("native", "Der Film fängt um halb acht an. Wir treffen uns um Viertel vor acht vor dem Kino.",
           "The film starts at half past seven. We'll meet at quarter to eight in front of the cinema."),
        _t("learner", "Perfekt. Ich bin pünktlich da. Bis Samstag!",
           "Perfect. I'll be there on time. See you Saturday!"),
    ],
    "grammar_focus": {
        "rule_name": "Uhrzeit angeben",
        "explanation": (
            "Informell: 'halb' bezieht sich auf die nächste Stunde — 'halb drei' "
            "bedeutet 14:30. 'Viertel nach' (XX:15), 'Viertel vor' (XX:45). "
            "Formell mit 24-Stunden-System: 'vierzehn Uhr dreißig'."
        ),
        "formula": "Es ist + (Viertel vor/nach | halb) + Stundenzahl",
        "examples": [
            _gex("Es ist halb drei.", "It's 2:30."),
            _gex("Es ist Viertel nach sieben.", "It's 7:15."),
            _gex("Es ist Viertel vor neun.", "It's 8:45."),
        ],
        "common_mistakes": [
            "Falsch: 'halb drei' = 3:30. Richtig: 'halb drei' = 2:30 (halfway TO three).",
            "Falsch: 'um die fünf Uhr'. Richtig: 'um fünf Uhr'.",
        ],
    },
    "exercises": [
        _ex_fib("Der Film beginnt ___ acht Uhr.",
                ["um", "an", "in", "zu"], 0,
                "Bei festen Uhrzeiten benutzt man 'um'."),
        _ex_mc("Wie spät ist 14:30 informell?",
               ["halb drei", "halb vier", "halb zwei", "Viertel drei"], 0,
               "'halb' geht zur nächsten Stunde."),
        _ex_arr(["ich", "Am", "spiele", "Sonntag", "Fußball"],
                "Am Sonntag spiele ich Fußball.",
                "Zeitangabe vorne → Verb an Position 2."),
        _ex_tr("What time does the train leave?",
               "Um wie viel Uhr fährt der Zug ab?"),
        _ex_sp("Beschreibe deinen typischen Wochenplan: Was machst du an welchem Tag?",
               "weekly schedule", 40),
    ],
    "vocabulary_list": [
        _v("die Uhrzeit", "the time", "Wie viel Uhr ist es?"),
        _v("der Termin", "the appointment", "Ich habe einen Termin."),
        _v("pünktlich", "punctual", "Sei bitte pünktlich!"),
        _v("der Montag", "Monday", "Am Montag arbeite ich."),
        _v("der Dienstag", "Tuesday", "Am Dienstag habe ich Deutschkurs."),
        _v("der Mittwoch", "Wednesday", "Am Mittwoch ist Markttag."),
        _v("der Donnerstag", "Thursday", "Am Donnerstag treffe ich Freunde."),
        _v("der Freitag", "Friday", "Am Freitag gehe ich aus."),
        _v("der Samstag", "Saturday", "Am Samstag schlafe ich lange."),
        _v("der Sonntag", "Sunday", "Am Sonntag besuche ich Familie."),
        _v("die Woche", "the week", "Die Woche war anstrengend."),
        _v("treffen", "to meet", "Wir treffen uns um acht."),
    ],
}

LESSON_07 = {
    "title": "Den Weg beschreiben",
    "level": "A1",
    "scenario": "train_station",
    "topic": "Wegbeschreibung in der Stadt",
    "learning_objectives": [
        "Nach dem Weg fragen",
        "Wegbeschreibungen verstehen und geben",
        "Lokale Präpositionen sicher anwenden",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "German addresses put the street name BEFORE the number: "
        "'Berliner Straße 42' (not '42 Berliner Straße'). The postcode comes "
        "before the city: '10115 Berlin'. When asking for directions, "
        "Germans appreciate a polite 'Entschuldigen Sie, bitte...'."
    ),
    "dialogue": [
        _t("native", "Entschuldigen Sie, wie komme ich zum Hauptbahnhof?",
           "Excuse me, how do I get to the central train station?"),
        _t("learner", "Sie gehen hier geradeaus, dann an der Ampel links.",
           "You go straight ahead here, then left at the traffic light."),
        _t("native", "Ist der Hauptbahnhof weit von hier?",
           "Is the central station far from here?"),
        _t("learner", "Nein, ungefähr zehn Minuten zu Fuß. Er liegt gegenüber dem Rathaus.",
           "No, about ten minutes on foot. It's across from the town hall."),
        _t("native", "Vielen Dank! Gibt es eine Apotheke in der Nähe?",
           "Thank you very much! Is there a pharmacy nearby?"),
        _t("learner", "Ja, neben der Bäckerei, gleich rechts an der Ecke.",
           "Yes, next to the bakery, right at the corner."),
    ],
    "grammar_focus": {
        "rule_name": "Lokale Präpositionen mit Dativ",
        "explanation": (
            "Lokale Präpositionen wie 'neben', 'gegenüber', 'an', 'in' verlangen "
            "den Dativ, wenn sie einen Ort (wo?) angeben."
        ),
        "formula": "Präposition + Dativ (dem/der/dem)",
        "examples": [
            _gex("Die Apotheke ist neben der Bäckerei.", "The pharmacy is next to the bakery."),
            _gex("Der Bahnhof liegt gegenüber dem Rathaus.", "The station is across from the town hall."),
            _gex("Der Bus hält an der Ecke.", "The bus stops at the corner."),
        ],
        "common_mistakes": [
            "Falsch: 'neben die Bäckerei' (wenn man WO meint). Richtig: 'neben der Bäckerei'.",
            "Falsch: 'gegenüber dem Rathaus von'. 'Gegenüber' steht alleine.",
        ],
    },
    "exercises": [
        _ex_fib("Gehen Sie ___ Ampel links.",
                ["an der", "an die", "auf der", "in die"], 0,
                "Ortsangabe → Dativ (an der)."),
        _ex_mc("Was bedeutet 'geradeaus'?",
               ["straight ahead", "to the left", "to the right", "around the corner"], 0,
               "Klassische Wegbeschreibung."),
        _ex_arr(["zum", "ich", "Wie", "Bahnhof?", "komme"],
                "Wie komme ich zum Bahnhof?",
                "Standardfrage nach dem Weg."),
        _ex_tr("The pharmacy is next to the bakery.",
               "Die Apotheke ist neben der Bäckerei."),
        _ex_sp("Beschreibe den Weg von deinem Zuhause zum nächsten Supermarkt.",
               "giving directions", 40),
    ],
    "vocabulary_list": [
        _v("der Weg", "the way", "Wo ist der Weg zum Bahnhof?"),
        _v("links", "left", "Gehen Sie nach links."),
        _v("rechts", "right", "Biegen Sie rechts ab."),
        _v("geradeaus", "straight ahead", "Gehen Sie geradeaus."),
        _v("die Ampel", "the traffic light", "An der Ampel rechts."),
        _v("die Kreuzung", "the intersection", "An der Kreuzung links."),
        _v("die Ecke", "the corner", "An der Ecke ist eine Bank."),
        _v("neben", "next to", "Die Bank ist neben der Post."),
        _v("gegenüber", "opposite", "Das Café ist gegenüber dem Park."),
        _v("die Apotheke", "the pharmacy", "Wo ist die Apotheke?"),
        _v("der Bahnhof", "the train station", "Der Bahnhof ist groß."),
        _v("zu Fuß", "on foot", "Ich gehe zu Fuß."),
    ],
}

LESSON_08 = {
    "title": "Beim Arzt — Einfache Beschwerden",
    "level": "A1",
    "scenario": "doctor",
    "topic": "Krankheit und Symptome",
    "learning_objectives": [
        "Körperteile auf Deutsch benennen",
        "Symptome beschreiben können",
        "Bei einer Erkältung den Arzt aufsuchen können",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "In Germany you can call in sick (krankmelden) for up to 3 days without "
        "a doctor's note. From day 4 onwards you need a 'Krankschreibung' "
        "(certificate from a doctor). Antibiotics are prescription-only and "
        "doctors are conservative about prescribing them."
    ),
    "dialogue": [
        _t("native", "Guten Tag, was kann ich für Sie tun?",
           "Good day, what can I do for you?"),
        _t("learner", "Guten Tag, Frau Doktor. Mir ist seit gestern schlecht und ich habe Halsschmerzen.",
           "Good day, doctor. I've felt unwell since yesterday and I have a sore throat."),
        _t("native", "Haben Sie auch Fieber?",
           "Do you also have a fever?"),
        _t("learner", "Ja, ich habe 38 Grad Fieber und Kopfschmerzen.",
           "Yes, I have a fever of 38 degrees and a headache."),
        _t("native", "Das klingt nach einer Erkältung. Ich verschreibe Ihnen Hustensaft und Halstabletten.",
           "That sounds like a cold. I'll prescribe you cough syrup and throat lozenges."),
        _t("learner", "Vielen Dank. Brauche ich eine Krankschreibung für meinen Arbeitgeber?",
           "Thank you very much. Do I need a sick note for my employer?"),
    ],
    "grammar_focus": {
        "rule_name": "Beschwerden mit 'haben' und 'mir ist...'",
        "explanation": (
            "Symptome werden mit 'Ich habe...' (Akkusativ) ausgedrückt. "
            "Subjektive Befindlichkeit mit 'Mir ist...' + Adjektiv (Dativ)."
        ),
        "formula": "Ich habe + Akkusativ-Symptom / Mir ist + Adjektiv",
        "examples": [
            _gex("Ich habe Kopfschmerzen.", "I have a headache."),
            _gex("Ich habe Fieber.", "I have a fever."),
            _gex("Mir ist schlecht.", "I feel sick."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich bin Kopfschmerzen'. Richtig: 'Ich habe Kopfschmerzen'.",
            "Falsch: 'Ich bin schlecht'. Richtig: 'Mir ist schlecht'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ Halsschmerzen.",
                ["habe", "bin", "ist", "hat"], 0,
                "Symptome → 'haben'."),
        _ex_mc("Wie sagt man 'I feel sick'?",
               ["Mir ist schlecht.", "Ich bin schlecht.",
                "Ich habe schlecht.", "Mich ist schlecht."], 0,
               "Dativkonstruktion mit unpersönlichem 'es ist'."),
        _ex_arr(["habe", "Ich", "Fieber", "und", "Kopfschmerzen"],
                "Ich habe Fieber und Kopfschmerzen.",
                "Symptome auflisten."),
        _ex_tr("I have had a headache since yesterday.",
               "Ich habe seit gestern Kopfschmerzen."),
        _ex_sp("Du bist beim Arzt. Beschreibe deine Symptome (mindestens drei).",
               "describing symptoms", 35),
    ],
    "vocabulary_list": [
        _v("der Arzt", "the doctor", "Ich gehe zum Arzt."),
        _v("die Ärztin", "the (female) doctor", "Meine Ärztin ist sehr nett."),
        _v("krank", "sick", "Ich bin krank."),
        _v("die Erkältung", "the cold", "Ich habe eine Erkältung."),
        _v("das Fieber", "the fever", "Ich habe Fieber."),
        _v("die Kopfschmerzen", "the headache", "Sie hat Kopfschmerzen."),
        _v("die Halsschmerzen", "the sore throat", "Ich habe Halsschmerzen."),
        _v("der Husten", "the cough", "Mein Husten ist schlimm."),
        _v("das Medikament", "the medicine", "Nehmen Sie dieses Medikament."),
        _v("die Krankschreibung", "the sick note", "Ich brauche eine Krankschreibung."),
        _v("verschreiben", "to prescribe", "Der Arzt verschreibt Tabletten."),
        _v("sich besser fühlen", "to feel better", "Ich fühle mich besser."),
    ],
}


# =====================================================================
# A2 — 8 lessons
# =====================================================================

LESSON_09 = {
    "title": "Im Supermarkt einkaufen",
    "level": "A2",
    "scenario": "supermarket",
    "topic": "Einkaufen und Akkusativ",
    "learning_objectives": [
        "Eine Einkaufsliste verstehen und verwenden",
        "Mengenangaben benutzen",
        "Den Akkusativ sicher anwenden",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "Most German supermarkets do not provide bags — bring your own or buy "
        "one at the checkout. You bag your own groceries quickly because the "
        "Kassiererin scans fast. 'Pfand' is a deposit on bottles you get back "
        "by returning them to a Pfandautomat."
    ),
    "dialogue": [
        _t("native", "Entschuldigung, wo finde ich den Joghurt?",
           "Excuse me, where do I find the yogurt?"),
        _t("learner", "Den Joghurt finden Sie im Kühlregal hinten links.",
           "You'll find the yogurt in the cold section at the back left."),
        _t("native", "Vielen Dank. Und haben Sie heute frisches Brot?",
           "Thank you. And do you have fresh bread today?"),
        _t("learner", "Ja, das frische Brot ist neben der Käsetheke.",
           "Yes, the fresh bread is next to the cheese counter."),
        _t("native", "Wunderbar. Ich nehme einen Liter Milch, ein Kilo Äpfel und ein Brot.",
           "Wonderful. I'll take a liter of milk, a kilo of apples, and a bread."),
        _t("learner", "Gerne. Brauchen Sie auch eine Tüte?",
           "Of course. Do you also need a bag?"),
    ],
    "grammar_focus": {
        "rule_name": "Akkusativ — direktes Objekt",
        "explanation": (
            "Der Akkusativ markiert das direkte Objekt ('wen oder was?'). "
            "Maskulin: der → den, ein → einen. Feminin und neutrum bleiben "
            "wie im Nominativ."
        ),
        "formula": "Subjekt + Verb + Akkusativobjekt",
        "examples": [
            _gex("Ich kaufe einen Apfel.", "I buy an apple.", "mask. → einen"),
            _gex("Ich kaufe eine Banane.", "I buy a banana.", "fem. → eine"),
            _gex("Ich kaufe ein Brot.", "I buy a bread.", "neut. → ein"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich kaufe ein Apfel'. Richtig: 'Ich kaufe einen Apfel'.",
            "Falsch: 'Ich brauche der Käse'. Richtig: 'Ich brauche den Käse'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich kaufe ___ Apfel.",
                ["einen", "ein", "eine", "der"], 0,
                "Apfel ist maskulin → Akkusativ einen."),
        _ex_mc("Welche Form ist Akkusativ Singular maskulin?",
               ["den/einen", "der/ein", "dem/einem", "des/eines"], 0,
               "Maskulin Akkusativ: der → den, ein → einen."),
        _ex_arr(["Liter", "Ich", "Milch", "möchte", "einen"],
                "Ich möchte einen Liter Milch.",
                "Mengenangabe + Substantiv."),
        _ex_tr("I need bread, butter, and cheese.",
               "Ich brauche Brot, Butter und Käse."),
        _ex_sp("Du gehst einkaufen. Lies deine Einkaufsliste laut vor und erkläre, wofür du jedes Produkt brauchst.",
               "shopping list", 40),
    ],
    "vocabulary_list": [
        _v("der Supermarkt", "the supermarket", "Ich gehe in den Supermarkt."),
        _v("die Einkaufsliste", "the shopping list", "Ich habe eine Einkaufsliste."),
        _v("das Brot", "the bread", "Ich kaufe ein Brot."),
        _v("die Milch", "the milk", "Wir brauchen Milch."),
        _v("der Käse", "the cheese", "Der Käse schmeckt gut."),
        _v("die Butter", "the butter", "Bitte gib mir die Butter."),
        _v("der Apfel", "the apple", "Ich esse einen Apfel."),
        _v("die Tüte", "the bag", "Brauchen Sie eine Tüte?"),
        _v("die Kasse", "the checkout", "Bitte zur Kasse."),
        _v("das Pfand", "the deposit", "Die Flasche hat Pfand."),
        _v("frisch", "fresh", "Das Brot ist frisch."),
        _v("billig", "cheap", "Das ist sehr billig."),
    ],
}

LESSON_10 = {
    "title": "Mit öffentlichen Verkehrsmitteln fahren",
    "level": "A2",
    "scenario": "train_station",
    "topic": "Öffentliche Verkehrsmittel und Modalverben",
    "learning_objectives": [
        "Eine Fahrkarte kaufen können",
        "Modalverben sicher verwenden",
        "Verspätungen und Anschlüsse verstehen",
    ],
    "estimated_minutes": 15,
    "cultural_note": (
        "Deutsche Bahn delays (Verspätung) are notorious. The Deutschlandticket "
        "(€49/month, 2024 prices) covers all regional trains, buses, and trams "
        "nationwide — but NOT ICE/IC long-distance trains. Always validate "
        "older paper tickets in the yellow Entwerter."
    ),
    "dialogue": [
        _t("native", "Guten Tag, ich möchte eine Fahrkarte nach Berlin kaufen.",
           "Good day, I'd like to buy a ticket to Berlin."),
        _t("learner", "Einfach oder hin und zurück?",
           "One way or round trip?"),
        _t("native", "Hin und zurück, bitte. Wann fährt der nächste Zug?",
           "Round trip, please. When does the next train leave?"),
        _t("learner", "Der nächste ICE fährt um 14:23 Uhr von Gleis 7. Sie müssen umsteigen in Hannover.",
           "The next ICE leaves at 14:23 from platform 7. You have to change in Hanover."),
        _t("native", "Wie viel kostet das Ticket?",
           "How much does the ticket cost?"),
        _t("learner", "Mit BahnCard 25 kostet es 89 Euro. Sie können auch online buchen.",
           "With BahnCard 25 it costs 89 euros. You can also book online."),
    ],
    "grammar_focus": {
        "rule_name": "Modalverben im Präsens",
        "explanation": (
            "Modalverben (können, müssen, dürfen, wollen, sollen, mögen) "
            "verändern die Bedeutung anderer Verben. Das Modalverb steht an "
            "Position 2, der Infinitiv geht ans Satzende."
        ),
        "formula": "Subjekt + Modalverb + ... + Infinitiv",
        "examples": [
            _gex("Sie müssen in Hannover umsteigen.", "You have to change in Hanover."),
            _gex("Ich kann gut Deutsch sprechen.", "I can speak German well."),
            _gex("Wir wollen nach Berlin fahren.", "We want to go to Berlin."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich kann sprechen Deutsch'. Richtig: Infinitiv ans Ende.",
            "Falsch: 'Du musst gehen zu'. Richtig: 'Du musst zu ... gehen.'",
        ],
    },
    "exercises": [
        _ex_fib("Sie ___ in Hannover umsteigen.",
                ["müssen", "können", "wollen", "dürfen"], 0,
                "Notwendigkeit ausdrücken."),
        _ex_mc("Wo steht der Infinitiv mit Modalverb?",
               ["Am Satzende", "An Position 1", "An Position 2", "Vor dem Subjekt"], 0,
               "Klassische Klammer im Hauptsatz."),
        _ex_arr(["nach", "Ich", "fahren", "Berlin", "möchte"],
                "Ich möchte nach Berlin fahren.",
                "Modalverb + Infinitiv-Klammer."),
        _ex_tr("The train is delayed by ten minutes.",
               "Der Zug hat zehn Minuten Verspätung."),
        _ex_sp("Du stehst am Schalter und kaufst eine Zugfahrkarte. Frage nach Preis, Gleis und Umstieg.",
               "buying a train ticket", 40),
    ],
    "vocabulary_list": [
        _v("die Fahrkarte", "the ticket", "Ich kaufe eine Fahrkarte."),
        _v("der Zug", "the train", "Der Zug fährt ab."),
        _v("das Gleis", "the platform", "Gleis 7 ist hier."),
        _v("umsteigen", "to change (transport)", "Wir müssen umsteigen."),
        _v("die Verspätung", "the delay", "Der Zug hat Verspätung."),
        _v("einfach", "one way", "Eine einfache Fahrt, bitte."),
        _v("hin und zurück", "round trip", "Eine Fahrkarte hin und zurück."),
        _v("der Schaffner", "the conductor", "Der Schaffner kontrolliert."),
        _v("die Haltestelle", "the stop", "An der nächsten Haltestelle."),
        _v("der Anschluss", "the connection", "Ich habe Anschluss in Köln."),
        _v("ankommen", "to arrive", "Der Zug kommt um 18 Uhr an."),
        _v("abfahren", "to depart", "Der Zug fährt pünktlich ab."),
    ],
}

LESSON_11 = {
    "title": "Über das Wetter sprechen",
    "level": "A2",
    "scenario": "free",
    "topic": "Wetter und Futur I",
    "learning_objectives": [
        "Das Wetter beschreiben",
        "Futur I mit 'werden' bilden",
        "Eine Wettervorhersage verstehen",
    ],
    "estimated_minutes": 12,
    "cultural_note": (
        "Talking about the weather is the universal small-talk topic in Germany "
        "too. Germans love their 'Wetterbericht' on the news. The phrase "
        "'Es gibt kein schlechtes Wetter, nur falsche Kleidung' (there's no bad "
        "weather, only the wrong clothing) is a national motto."
    ),
    "dialogue": [
        _t("native", "Wie wird das Wetter morgen?",
           "What will the weather be like tomorrow?"),
        _t("learner", "Es wird wahrscheinlich regnen. Die Temperaturen liegen bei 12 Grad.",
           "It will probably rain. Temperatures will be around 12 degrees."),
        _t("native", "Schade, wir wollten ein Picknick machen.",
           "Too bad, we wanted to have a picnic."),
        _t("learner", "Vielleicht klart es am Nachmittag auf. Die Sonne soll später scheinen.",
           "Maybe it'll clear up in the afternoon. The sun is supposed to shine later."),
        _t("native", "Hoffentlich. Im Sommer ist das Wetter hier schöner.",
           "Hopefully. In summer the weather here is nicer."),
        _t("learner", "Ja, im Juli und August wird es richtig warm und sonnig.",
           "Yes, in July and August it gets really warm and sunny."),
    ],
    "grammar_focus": {
        "rule_name": "Futur I mit 'werden'",
        "explanation": (
            "Futur I drückt Zukunft, Vermutung oder Absicht aus. Es wird mit "
            "der konjugierten Form von 'werden' + Infinitiv am Satzende gebildet."
        ),
        "formula": "Subjekt + werden + ... + Infinitiv",
        "examples": [
            _gex("Es wird morgen regnen.", "It will rain tomorrow."),
            _gex("Wir werden ins Kino gehen.", "We will go to the cinema."),
            _gex("Sie wird wohl müde sein.", "She is probably tired."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich werde gehen ins Kino'. Richtig: Infinitiv ans Ende.",
            "Falsch: 'Ich bin gehen morgen'. Futur mit 'werden', nicht 'sein'.",
        ],
    },
    "exercises": [
        _ex_fib("Morgen ___ es regnen.",
                ["wird", "werde", "werden", "wirst"], 0,
                "3. Person Singular von werden."),
        _ex_mc("Wie bildet man Futur I?",
               ["werden + Infinitiv", "haben + Partizip II",
                "sein + Partizip II", "Präsens"], 0,
               "Standardformel für Zukunft im Deutschen."),
        _ex_arr(["wird", "Es", "schneien", "morgen"],
                "Es wird morgen schneien.",
                "Futur I."),
        _ex_tr("Tomorrow it will be sunny and warm.",
               "Morgen wird es sonnig und warm sein."),
        _ex_sp("Beschreibe das Wetter heute und mache eine Vorhersage für morgen.",
               "weather description", 35),
    ],
    "vocabulary_list": [
        _v("das Wetter", "the weather", "Wie ist das Wetter heute?"),
        _v("die Sonne", "the sun", "Die Sonne scheint."),
        _v("der Regen", "the rain", "Der Regen ist stark."),
        _v("der Schnee", "the snow", "Der Schnee ist weiß."),
        _v("der Wind", "the wind", "Der Wind ist kalt."),
        _v("die Wolke", "the cloud", "Die Wolken sind grau."),
        _v("das Gewitter", "the thunderstorm", "Heute gibt es ein Gewitter."),
        _v("warm", "warm", "Heute ist es warm."),
        _v("kalt", "cold", "Es ist kalt draußen."),
        _v("die Vorhersage", "the forecast", "Die Wettervorhersage ist gut."),
        _v("die Temperatur", "the temperature", "Die Temperatur ist hoch."),
        _v("der Grad", "the degree", "Es sind 20 Grad."),
    ],
}

LESSON_12 = {
    "title": "Meinen Tagesablauf beschreiben",
    "level": "A2",
    "scenario": "free",
    "topic": "Alltag und reflexive Verben",
    "learning_objectives": [
        "Den eigenen Tagesablauf beschreiben",
        "Reflexive Verben korrekt verwenden",
        "Zeitliche Abfolgen ausdrücken",
    ],
    "estimated_minutes": 13,
    "cultural_note": (
        "Many Germans start work early — 7:30 or 8:00 is normal. The "
        "'Mittagspause' is sacred, often exactly 30 or 60 minutes, and people "
        "actually leave their desks. 'Feierabend' (end of the workday) is a "
        "real cultural concept and you should respect it."
    ),
    "dialogue": [
        _t("native", "Wie sieht dein typischer Morgen aus?",
           "What does your typical morning look like?"),
        _t("learner", "Ich stehe um halb sieben auf, dusche mich und ziehe mich an. Dann frühstücke ich.",
           "I get up at half past six, take a shower and get dressed. Then I have breakfast."),
        _t("native", "Und wann gehst du zur Arbeit?",
           "And when do you go to work?"),
        _t("learner", "Um Viertel nach acht fahre ich mit dem Bus ins Büro. Ich beeile mich immer.",
           "At quarter past eight I take the bus to the office. I always hurry."),
        _t("native", "Was machst du am Abend?",
           "What do you do in the evening?"),
        _t("learner", "Nach der Arbeit treffe ich mich oft mit Freunden. Am Wochenende entspanne ich mich.",
           "After work I often meet with friends. On weekends I relax."),
    ],
    "grammar_focus": {
        "rule_name": "Reflexive Verben",
        "explanation": (
            "Reflexive Verben verlangen ein Reflexivpronomen, das dasselbe "
            "Subjekt bezeichnet. Im Akkusativ: mich, dich, sich, uns, euch, sich."
        ),
        "formula": "Subjekt + Verb + Reflexivpronomen + ...",
        "examples": [
            _gex("Ich wasche mich.", "I wash myself."),
            _gex("Er freut sich über das Geschenk.", "He is happy about the gift."),
            _gex("Wir beeilen uns.", "We hurry."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich wasche'. Richtig: 'Ich wasche mich' (reflexiv).",
            "Falsch: 'Er freut'. Richtig: 'Er freut sich'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ziehe ___ schnell an.",
                ["mich", "mir", "sich", "dich"], 0,
                "Reflexivpronomen 1. Person Akkusativ."),
        _ex_mc("Welches Verb ist reflexiv?",
               ["sich freuen", "gehen", "essen", "sehen"], 0,
               "Klassisches Beispiel für ein reflexives Verb."),
        _ex_arr(["um", "Ich", "sieben", "auf", "stehe"],
                "Ich stehe um sieben auf.",
                "Trennbares Verb + Zeitangabe."),
        _ex_tr("I wake up at seven o'clock.",
               "Ich wache um sieben Uhr auf."),
        _ex_sp("Beschreibe deinen Tagesablauf von morgens bis abends mit mindestens fünf Aktivitäten.",
               "daily routine", 50),
    ],
    "vocabulary_list": [
        _v("aufstehen", "to get up", "Ich stehe um sieben auf."),
        _v("sich duschen", "to shower", "Ich dusche mich morgens."),
        _v("sich anziehen", "to get dressed", "Ich ziehe mich schnell an."),
        _v("frühstücken", "to have breakfast", "Wir frühstücken zusammen."),
        _v("zur Arbeit fahren", "to go to work", "Ich fahre mit dem Bus zur Arbeit."),
        _v("die Mittagspause", "the lunch break", "Die Mittagspause ist um 12."),
        _v("der Feierabend", "end of workday", "Schönen Feierabend!"),
        _v("sich treffen", "to meet", "Wir treffen uns abends."),
        _v("sich entspannen", "to relax", "Am Sonntag entspanne ich mich."),
        _v("ins Bett gehen", "to go to bed", "Ich gehe um elf ins Bett."),
        _v("sich beeilen", "to hurry", "Beeil dich!"),
        _v("der Tagesablauf", "the daily routine", "Mein Tagesablauf ist normal."),
    ],
}

LESSON_13 = {
    "title": "Im Restaurant reklamieren",
    "level": "A2",
    "scenario": "restaurant",
    "topic": "Höfliche Beschwerde",
    "learning_objectives": [
        "Höflich reklamieren mit Konjunktiv II",
        "Bestellfehler ansprechen",
        "Eine Lösung erbitten",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "Germans value direct but polite communication. When something is "
        "wrong, you should say so clearly — but using Konjunktiv II "
        "('Könnten Sie...?', 'Würden Sie...?') keeps the tone respectful. "
        "Servers will usually apologize sincerely and fix the problem quickly."
    ),
    "dialogue": [
        _t("native", "Hier ist Ihre Pizza Margherita.",
           "Here is your pizza Margherita."),
        _t("learner", "Entschuldigung, aber ich habe eine Pizza Funghi bestellt.",
           "Excuse me, but I ordered a pizza Funghi."),
        _t("native", "Oh, das tut mir leid! Ich bringe Ihnen sofort die richtige Pizza.",
           "Oh, I'm sorry! I'll bring you the correct pizza right away."),
        _t("learner", "Vielen Dank. Und könnten Sie auch noch Wasser bringen, bitte? Mein Glas ist leer.",
           "Thank you. And could you also bring water, please? My glass is empty."),
        _t("native", "Selbstverständlich. Möchten Sie etwas anderes statt der Pizza?",
           "Of course. Would you like something else instead of the pizza?"),
        _t("learner", "Nein danke, die Funghi ist in Ordnung. Würden Sie mir die Wartezeit vom Preis abziehen?",
           "No thanks, the Funghi is fine. Would you deduct the waiting time from the price?"),
    ],
    "grammar_focus": {
        "rule_name": "Höfliche Bitten mit Konjunktiv II",
        "explanation": (
            "Für höfliche Bitten verwendet man Konjunktiv II: 'Könnten Sie...?', "
            "'Würden Sie bitte...?', 'Hätten Sie...?'. Diese Formen klingen "
            "respektvoll und sind im Service-Bereich Standard."
        ),
        "formula": "Könnten/Würden/Hätten Sie + ... + Infinitiv?",
        "examples": [
            _gex("Könnten Sie mir bitte helfen?", "Could you please help me?"),
            _gex("Würden Sie das bitte wiederholen?", "Would you please repeat that?"),
            _gex("Hätten Sie einen Moment Zeit?", "Would you have a moment?"),
        ],
        "common_mistakes": [
            "Falsch: 'Können Sie...?' für höchste Höflichkeit. Besser: 'Könnten Sie...?'.",
            "Falsch: 'Wollen Sie...?' (zu direkt). Besser: 'Würden Sie...?'.",
        ],
    },
    "exercises": [
        _ex_fib("___ Sie mir bitte helfen?",
                ["Könnten", "Können", "Konnten", "Kennt"], 0,
                "Konjunktiv II für höfliche Bitten."),
        _ex_mc("Welche Form ist am höflichsten?",
               ["Würden Sie bitte...", "Wollen Sie", "Mach mal", "Du musst"], 0,
               "Konjunktiv II + 'bitte' = höflich."),
        _ex_arr(["Sie", "Würden", "die", "bringen?", "Rechnung"],
                "Würden Sie die Rechnung bringen?",
                "Höfliche Frage mit würden."),
        _ex_tr("This dish is cold. Could you reheat it?",
               "Dieses Gericht ist kalt. Könnten Sie es aufwärmen?"),
        _ex_sp("Im Restaurant ist etwas falsch. Reklamiere höflich mit Konjunktiv II.",
               "complaining politely", 40),
    ],
    "vocabulary_list": [
        _v("reklamieren", "to complain", "Ich möchte reklamieren."),
        _v("falsch", "wrong", "Das ist falsch."),
        _v("kalt", "cold", "Die Suppe ist kalt."),
        _v("die Bestellung", "the order", "Meine Bestellung ist falsch."),
        _v("der Fehler", "the mistake", "Es gibt einen Fehler."),
        _v("entschuldigen", "to excuse", "Entschuldigen Sie bitte."),
        _v("austauschen", "to exchange", "Können Sie das austauschen?"),
        _v("die Wartezeit", "the waiting time", "Die Wartezeit ist lang."),
        _v("das Glas", "the glass", "Mein Glas ist leer."),
        _v("leer", "empty", "Die Flasche ist leer."),
        _v("voll", "full", "Das Glas ist voll."),
        _v("zufrieden", "satisfied", "Ich bin zufrieden."),
    ],
}

LESSON_14 = {
    "title": "Eine Wohnung besichtigen",
    "level": "A2",
    "scenario": "landlord",
    "topic": "Wohnung und Dativ",
    "learning_objectives": [
        "Räume und Möbel benennen",
        "Lokalangaben mit Dativ machen",
        "Eine Wohnung beschreiben",
    ],
    "estimated_minutes": 15,
    "cultural_note": (
        "The German rental market is competitive. To rent an apartment you "
        "usually need a SCHUFA credit check, proof of income, and a 3-month "
        "deposit (Kaution). 'Nebenkosten' (utilities) are charged separately on "
        "top of the cold rent (Kaltmiete) — always ask for the warm rent (Warmmiete)."
    ),
    "dialogue": [
        _t("native", "Hier ist das Wohnzimmer. Wie gefällt es Ihnen?",
           "Here is the living room. How do you like it?"),
        _t("learner", "Sehr schön! Das Sofa steht im Wohnzimmer und der Fernseher hängt an der Wand.",
           "Very nice! The sofa is in the living room and the TV hangs on the wall."),
        _t("native", "Genau. Die Küche ist neben dem Bad. Sie ist komplett ausgestattet.",
           "Exactly. The kitchen is next to the bathroom. It is fully equipped."),
        _t("learner", "Wie hoch ist die Miete und sind die Nebenkosten inklusive?",
           "How high is the rent and are the utilities included?"),
        _t("native", "Die Kaltmiete beträgt 850 Euro, plus 200 Euro Nebenkosten. Insgesamt also 1050 Euro warm.",
           "The cold rent is 850 euros, plus 200 euros utilities. Altogether 1050 euros warm."),
        _t("learner", "In Ordnung. Brauche ich eine SCHUFA-Auskunft und wie hoch ist die Kaution?",
           "Alright. Do I need a SCHUFA report and how high is the deposit?"),
    ],
    "grammar_focus": {
        "rule_name": "Dativ bei Ortsangaben (wo?)",
        "explanation": (
            "Wechselpräpositionen (in, an, auf, unter, über, vor, hinter, "
            "neben, zwischen) verlangen den Dativ, wenn sie einen Ort "
            "bezeichnen (wo?). Im Dativ: dem/der/dem, einem/einer/einem."
        ),
        "formula": "Wechselpräposition + Dativ → wo?",
        "examples": [
            _gex("Das Sofa steht im Wohnzimmer.", "The sofa is in the living room.", "in dem → im"),
            _gex("Die Lampe hängt an der Wand.", "The lamp hangs on the wall.", "an der"),
            _gex("Die Katze schläft auf dem Bett.", "The cat sleeps on the bed.", "auf dem"),
        ],
        "common_mistakes": [
            "Falsch: 'in das Wohnzimmer steht'. Richtig: 'im Wohnzimmer steht' (Ort = Dativ).",
            "Falsch: 'auf dem Tisch legen'. Richtig: 'auf den Tisch legen' (Bewegung = Akk.).",
        ],
    },
    "exercises": [
        _ex_fib("Das Buch liegt ___ Tisch.",
                ["auf dem", "auf den", "in dem", "an dem"], 0,
                "Liegen + wo? → Dativ."),
        _ex_mc("Welche Form ist Dativ Singular feminin?",
               ["der", "die", "den", "dem"], 0,
               "Feminin Dativ: die → der."),
        _ex_arr(["dem", "Die", "neben", "ist", "Bad", "Küche"],
                "Die Küche ist neben dem Bad.",
                "Lokalangabe mit Dativ."),
        _ex_tr("The lamp is on the table.",
               "Die Lampe steht auf dem Tisch."),
        _ex_sp("Beschreibe deine Wohnung: Welche Räume gibt es und was steht wo?",
               "describing an apartment", 45),
    ],
    "vocabulary_list": [
        _v("die Wohnung", "the apartment", "Die Wohnung ist groß."),
        _v("das Wohnzimmer", "the living room", "Das Wohnzimmer ist hell."),
        _v("die Küche", "the kitchen", "Die Küche ist modern."),
        _v("das Schlafzimmer", "the bedroom", "Das Schlafzimmer ist klein."),
        _v("das Bad", "the bathroom", "Das Bad ist neu."),
        _v("der Balkon", "the balcony", "Der Balkon ist schön."),
        _v("die Miete", "the rent", "Die Miete ist hoch."),
        _v("die Nebenkosten", "the utilities", "Die Nebenkosten sind inklusive."),
        _v("die Kaution", "the deposit", "Die Kaution beträgt drei Monatsmieten."),
        _v("möbliert", "furnished", "Die Wohnung ist möbliert."),
        _v("besichtigen", "to view", "Ich möchte die Wohnung besichtigen."),
        _v("der Vermieter", "the landlord", "Mein Vermieter ist freundlich."),
    ],
}

LESSON_15 = {
    "title": "Telefonieren auf Deutsch",
    "level": "A2",
    "scenario": "free",
    "topic": "Telefonieren und indirekte Fragen",
    "learning_objectives": [
        "Sich am Telefon vorstellen",
        "Indirekte Fragen formulieren",
        "Eine Nachricht hinterlassen",
    ],
    "estimated_minutes": 13,
    "cultural_note": (
        "When you answer the phone in Germany, you say your last name — not "
        "'Hello'. 'Müller, guten Tag.' is standard. When calling, you say "
        "'Guten Tag, hier spricht [Name]'. Voicemail is widely used; speak "
        "clearly and leave your number twice."
    ),
    "dialogue": [
        _t("native", "Schmidt, guten Tag.",
           "Schmidt, good day."),
        _t("learner", "Guten Tag, Frau Schmidt. Hier spricht Hans Sharma. Könnten Sie mir sagen, wann Herr Bauer im Büro ist?",
           "Good day, Mrs. Schmidt. This is Hans Sharma speaking. Could you tell me when Mr. Bauer is in the office?"),
        _t("native", "Herr Bauer ist heute leider nicht im Hause. Er ist morgen wieder da.",
           "Mr. Bauer is unfortunately not in the house today. He'll be back tomorrow."),
        _t("learner", "Ich würde gerne wissen, ob ich einen Termin vereinbaren kann.",
           "I would like to know if I can schedule an appointment."),
        _t("native", "Selbstverständlich. Wann passt es Ihnen?",
           "Of course. When suits you?"),
        _t("learner", "Am Donnerstag um zehn Uhr wäre perfekt. Vielen Dank für Ihre Hilfe.",
           "Thursday at ten o'clock would be perfect. Thank you for your help."),
    ],
    "grammar_focus": {
        "rule_name": "Indirekte Fragen",
        "explanation": (
            "Indirekte Fragen sind Nebensätze, die mit einem Fragewort oder 'ob' "
            "beginnen. Das konjugierte Verb steht am Ende. Sie klingen "
            "höflicher als direkte Fragen."
        ),
        "formula": "Hauptsatz + (Fragewort/ob) + Subjekt + ... + Verb",
        "examples": [
            _gex("Können Sie mir sagen, wann der Zug kommt?",
                 "Can you tell me when the train is coming?"),
            _gex("Ich würde gerne wissen, ob er da ist.",
                 "I would like to know if he is there."),
            _gex("Wissen Sie, wo das Rathaus ist?",
                 "Do you know where the town hall is?"),
        ],
        "common_mistakes": [
            "Falsch: 'Wissen Sie wo ist das Rathaus?'. Richtig: 'Wissen Sie, wo das Rathaus ist?'.",
            "Falsch: 'Ob er kommt?'. Richtig: 'Ich weiß nicht, ob er kommt.'",
        ],
    },
    "exercises": [
        _ex_fib("Können Sie mir sagen, wann der Bus ___?",
                ["kommt", "kommen", "kommst", "komme"], 0,
                "Verb am Nebensatzende, 3. Person Singular."),
        _ex_mc("Wo steht das Verb im Nebensatz?",
               ["am Ende", "an Position 1", "an Position 2", "vor dem Subjekt"], 0,
               "Klassische Nebensatz-Wortstellung."),
        _ex_arr(["wissen,", "Ich", "ob", "möchte", "kommt", "er"],
                "Ich möchte wissen, ob er kommt.",
                "Hauptsatz + Komma + ob-Satz."),
        _ex_tr("Could you tell me when she'll be back?",
               "Könnten Sie mir sagen, wann sie zurück ist?"),
        _ex_sp("Ruf in einem Büro an. Frage nach einem Termin und hinterlasse eine kurze Nachricht.",
               "phone call", 40),
    ],
    "vocabulary_list": [
        _v("anrufen", "to call (phone)", "Ich rufe dich später an."),
        _v("das Telefon", "the telephone", "Das Telefon klingelt."),
        _v("die Nachricht", "the message", "Ich hinterlasse eine Nachricht."),
        _v("der Anrufbeantworter", "the answering machine",
           "Der Anrufbeantworter ist an."),
        _v("hinterlassen", "to leave (a message)",
           "Bitte hinterlassen Sie eine Nachricht."),
        _v("verbinden", "to connect (call)", "Ich verbinde Sie weiter."),
        _v("zurückrufen", "to call back", "Ich rufe Sie zurück."),
        _v("besetzt", "busy (line)", "Die Leitung ist besetzt."),
        _v("die Vorwahl", "the area code", "Die Vorwahl ist 030."),
        _v("die Durchwahl", "the extension", "Meine Durchwahl ist 142."),
        _v("buchstabieren", "to spell", "Können Sie das buchstabieren?"),
        _v("auf Wiederhören", "goodbye (phone)", "Auf Wiederhören!"),
    ],
}

LESSON_16 = {
    "title": "Arzttermin vereinbaren",
    "level": "A2",
    "scenario": "doctor",
    "topic": "Termine und trennbare Verben",
    "learning_objectives": [
        "Einen Termin vereinbaren, verschieben und absagen",
        "Trennbare Verben sicher verwenden",
        "Höflich am Telefon sprechen",
    ],
    "estimated_minutes": 14,
    "cultural_note": (
        "German doctors' offices have strict appointment systems. To get a "
        "specialist appointment quickly, mention if you're a 'Privatpatient' or "
        "in 'gesetzliche Krankenkasse'. The 116 117 hotline helps you find "
        "appointments. Most practices close on Wednesday afternoons."
    ),
    "dialogue": [
        _t("native", "Praxis Dr. Weber, Schmidt am Apparat.",
           "Dr. Weber's practice, Schmidt speaking."),
        _t("learner", "Guten Tag, ich möchte einen Termin vereinbaren.",
           "Good day, I'd like to schedule an appointment."),
        _t("native", "Worum geht es denn?",
           "What is it regarding?"),
        _t("learner", "Ich habe seit einer Woche Rückenschmerzen. Wann hätten Sie etwas frei?",
           "I've had back pain for a week. When would you have something free?"),
        _t("native", "Nächste Woche Dienstag um 9:30 Uhr ist noch ein Termin frei.",
           "Next Tuesday at 9:30 there's still an appointment free."),
        _t("learner", "Leider kann ich den Termin nicht wahrnehmen. Kann ich ihn auf Donnerstag verschieben?",
           "Unfortunately I can't take that appointment. Can I move it to Thursday?"),
    ],
    "grammar_focus": {
        "rule_name": "Trennbare Verben",
        "explanation": (
            "Bei trennbaren Verben (anrufen, vereinbaren, absagen, verschieben, "
            "aufschreiben) wird das Präfix im Hauptsatz vom Stamm getrennt und "
            "ans Satzende gestellt."
        ),
        "formula": "Subjekt + Verb-Stamm + ... + Präfix",
        "examples": [
            _gex("Ich rufe morgen an.", "I'm calling tomorrow.", "anrufen → rufe ... an"),
            _gex("Sie sagt den Termin ab.", "She cancels the appointment.", "absagen → sagt ... ab"),
            _gex("Wir verschieben das Treffen.", "We're postponing the meeting.", "verschieben (untrennbar)"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich anrufe dich'. Richtig: 'Ich rufe dich an'.",
            "Falsch: 'Ich aufstehe um sieben'. Richtig: 'Ich stehe um sieben auf'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ den Termin morgen ___.",
                ["sage ... ab", "absage", "abe ... sag", "sagen ... ab"], 0,
                "Trennbares Verb im Präsens."),
        _ex_mc("Welches Verb ist trennbar?",
               ["anrufen", "verstehen", "bekommen", "erlauben"], 0,
               "Präfix 'an-' wird getrennt."),
        _ex_arr(["sieben", "Ich", "auf", "stehe", "um"],
                "Ich stehe um sieben auf.",
                "Trennbares Verb mit Zeitangabe."),
        _ex_tr("I'll call you back tomorrow.",
               "Ich rufe Sie morgen zurück."),
        _ex_sp("Ruf eine Arztpraxis an, vereinbare einen Termin und verschiebe ihn dann auf einen anderen Tag.",
               "scheduling an appointment", 45),
    ],
    "vocabulary_list": [
        _v("die Praxis", "the practice", "Die Praxis ist offen."),
        _v("vereinbaren", "to arrange", "Ich vereinbare einen Termin."),
        _v("absagen", "to cancel", "Ich muss den Termin absagen."),
        _v("verschieben", "to postpone", "Können wir verschieben?"),
        _v("aufschreiben", "to write down", "Ich schreibe das auf."),
        _v("die Sprechstunde", "the consultation hours", "Die Sprechstunde ist morgens."),
        _v("dringend", "urgent", "Es ist dringend."),
        _v("frei haben", "to be free", "Wann haben Sie frei?"),
        _v("die Versichertenkarte", "the insurance card", "Bitte Ihre Versichertenkarte."),
        _v("die Überweisung", "the referral", "Ich brauche eine Überweisung."),
        _v("der Facharzt", "the specialist", "Der Facharzt hat Zeit."),
        _v("warten", "to wait", "Bitte warten Sie."),
    ],
}


# =====================================================================
# B1 — 8 lessons
# =====================================================================

LESSON_17 = {
    "title": "Das Vorstellungsgespräch",
    "level": "B1",
    "scenario": "job_interview",
    "topic": "Bewerbung und Perfekt",
    "learning_objectives": [
        "Ein Vorstellungsgespräch souverän führen",
        "Perfekt vs. Präteritum richtig wählen",
        "Beruflichen Werdegang darstellen",
    ],
    "estimated_minutes": 18,
    "cultural_note": (
        "A German CV ('tabellarischer Lebenslauf') traditionally includes a "
        "professional photo, date and place of birth, and marital status — "
        "things that would be unusual in the US/UK. Be precise about dates "
        "and use reverse-chronological order. Always sign and date your CV."
    ),
    "dialogue": [
        _t("native", "Erzählen Sie mir bitte etwas über Ihren beruflichen Werdegang.",
           "Please tell me something about your professional career."),
        _t("learner", "Gerne. Ich habe in Mumbai Informatik studiert und 2018 mein Studium abgeschlossen. Danach habe ich drei Jahre bei einer IT-Firma gearbeitet.",
           "Gladly. I studied computer science in Mumbai and completed my degree in 2018. After that I worked for an IT company for three years."),
        _t("native", "Warum haben Sie sich bei uns beworben?",
           "Why did you apply with us?"),
        _t("learner", "Ihre Firma ist führend im Bereich Künstliche Intelligenz. Ich möchte meine Kenntnisse erweitern und an spannenden Projekten mitarbeiten.",
           "Your company is a leader in artificial intelligence. I want to expand my knowledge and work on exciting projects."),
        _t("native", "Welche Stärken bringen Sie für die Position mit?",
           "What strengths do you bring to the position?"),
        _t("learner", "Ich bin teamfähig, arbeite strukturiert und habe Erfahrung mit Python und maschinellem Lernen.",
           "I am a team player, work in a structured way, and have experience with Python and machine learning."),
    ],
    "grammar_focus": {
        "rule_name": "Perfekt vs. Präteritum",
        "explanation": (
            "Perfekt (haben/sein + Partizip II) verwendet man in der "
            "gesprochenen Sprache. Präteritum benutzt man in der Schriftsprache "
            "und bei sein, haben sowie Modalverben auch beim Sprechen."
        ),
        "formula": "Sprechen → Perfekt; Schreiben/sein/haben/Modal → Präteritum",
        "examples": [
            _gex("Ich habe Informatik studiert.", "I studied computer science.", "Perfekt - speech"),
            _gex("Ich war in Berlin.", "I was in Berlin.", "Präteritum - sein"),
            _gex("Sie schrieb einen Roman.", "She wrote a novel.", "Präteritum - writing"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich war essen.' Besser: 'Ich habe gegessen.'",
            "Falsch: 'Ich habe gesein'. Sein hat KEIN Perfekt mit 'haben'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ Informatik studiert.",
                ["habe", "bin", "war", "wurde"], 0,
                "Perfekt mit haben."),
        _ex_mc("Welche Form ist Präteritum von 'sein'?",
               ["war", "habe gewesen", "bin", "wäre"], 0,
               "Sein + Präteritum = war/warst/war/waren/wart/waren."),
        _ex_arr(["mich", "Ich", "beworben", "habe", "beworben"],
                "Ich habe mich beworben.",
                "Reflexives Verb im Perfekt."),
        _ex_tr("I worked at Google for two years.",
               "Ich habe zwei Jahre bei Google gearbeitet."),
        _ex_sp("Stell dich in einem Vorstellungsgespräch vor: Erzähle von deiner Ausbildung, Berufserfahrung und Stärken.",
               "job interview", 60),
    ],
    "vocabulary_list": [
        _v("das Vorstellungsgespräch", "the job interview",
           "Das Vorstellungsgespräch war gut."),
        _v("die Bewerbung", "the application", "Meine Bewerbung ist fertig."),
        _v("der Lebenslauf", "the CV", "Hier ist mein Lebenslauf."),
        _v("die Stärke", "the strength", "Meine Stärke ist Teamarbeit."),
        _v("die Schwäche", "the weakness", "Meine Schwäche ist Ungeduld."),
        _v("die Erfahrung", "the experience", "Ich habe viel Erfahrung."),
        _v("die Kenntnisse", "the knowledge", "Ich habe gute Kenntnisse."),
        _v("die Stelle", "the position", "Die Stelle interessiert mich."),
        _v("das Gehalt", "the salary", "Das Gehalt ist verhandelbar."),
        _v("teamfähig", "team player", "Ich bin sehr teamfähig."),
        _v("zuverlässig", "reliable", "Sie ist zuverlässig."),
        _v("der Werdegang", "the career path", "Mein Werdegang ist vielfältig."),
    ],
}

LESSON_18 = {
    "title": "Meinungen ausdrücken und diskutieren",
    "level": "B1",
    "scenario": "free",
    "topic": "Meinungen und Argumente",
    "learning_objectives": [
        "Eine eigene Meinung formulieren",
        "Zustimmen oder widersprechen",
        "Argumente strukturiert vortragen",
    ],
    "estimated_minutes": 16,
    "cultural_note": (
        "Germans value direct, well-structured opinions in discussions. It is "
        "perfectly acceptable to disagree openly — it's seen as respect, not "
        "rudeness. 'Einerseits... andererseits...' (on one hand... on the other...) "
        "shows nuanced thinking."
    ),
    "dialogue": [
        _t("native", "Was hältst du davon, dass Homeoffice immer beliebter wird?",
           "What do you think of the fact that home office is becoming more popular?"),
        _t("learner", "Meiner Meinung nach hat Homeoffice viele Vorteile, aber auch Nachteile.",
           "In my opinion, home office has many advantages, but also disadvantages."),
        _t("native", "Welche Vorteile siehst du?",
           "What advantages do you see?"),
        _t("learner", "Einerseits spart man Zeit und Geld für den Arbeitsweg. Andererseits fehlt der persönliche Kontakt zu Kollegen.",
           "On one hand, you save time and money on commuting. On the other hand, the personal contact with colleagues is missing."),
        _t("native", "Da stimme ich dir zu. Trotzdem finde ich, dass Homeoffice die Zukunft ist.",
           "I agree with you there. Nevertheless, I think home office is the future."),
        _t("learner", "Ich bin der Ansicht, dass eine Mischung am besten funktioniert.",
           "I'm of the view that a mixture works best."),
    ],
    "grammar_focus": {
        "rule_name": "Meinungsformeln",
        "explanation": (
            "Meinungen werden mit festen Wendungen eingeleitet: "
            "'Meiner Meinung nach...', 'Ich bin der Ansicht, dass...', "
            "'Ich finde, dass...'. Mit 'einerseits... andererseits...' "
            "werden Argumente kontrastiert."
        ),
        "formula": "Meinungsformel + Hauptsatz / Nebensatz mit dass",
        "examples": [
            _gex("Meiner Meinung nach ist das richtig.", "In my opinion, that's correct."),
            _gex("Ich bin der Ansicht, dass wir mehr lernen müssen.",
                 "I am of the view that we need to learn more."),
            _gex("Einerseits ist es teuer, andererseits ist es praktisch.",
                 "On one hand it's expensive, on the other it's practical."),
        ],
        "common_mistakes": [
            "Falsch: 'Meine Meinung ist...'. Besser: 'Meiner Meinung nach...'.",
            "Falsch: 'Ich bin agree'. Richtig: 'Ich stimme zu.'",
        ],
    },
    "exercises": [
        _ex_fib("Meiner ___ nach ist das eine gute Idee.",
                ["Meinung", "Meinen", "Meine", "Meinungs"], 0,
                "Festwendung mit Genitiv."),
        _ex_mc("Wie drückt man Zustimmung aus?",
               ["Da stimme ich zu.", "Da bin ich nicht.",
                "Ich gehe nicht.", "Das ist falsch."], 0,
               "'Zustimmen' = to agree."),
        _ex_arr(["andererseits", "Einerseits", "nett,", "ist", "er", "streng", "ist", "er"],
                "Einerseits ist er nett, andererseits ist er streng.",
                "Kontrastive Argumentation."),
        _ex_tr("In my opinion this is the wrong decision.",
               "Meiner Meinung nach ist das die falsche Entscheidung."),
        _ex_sp("Diskutiere die Vor- und Nachteile von sozialen Medien. Gib deine eigene Meinung mit Argumenten.",
               "expressing opinions", 70),
    ],
    "vocabulary_list": [
        _v("die Meinung", "the opinion", "Meine Meinung ist klar."),
        _v("zustimmen", "to agree", "Ich stimme dir zu."),
        _v("widersprechen", "to disagree", "Ich muss widersprechen."),
        _v("der Vorteil", "the advantage", "Das ist ein großer Vorteil."),
        _v("der Nachteil", "the disadvantage", "Es hat auch Nachteile."),
        _v("das Argument", "the argument", "Dein Argument ist stark."),
        _v("die Diskussion", "the discussion", "Die Diskussion war spannend."),
        _v("einerseits", "on one hand", "Einerseits ist es teuer."),
        _v("andererseits", "on the other hand",
           "Andererseits ist es praktisch."),
        _v("das Beispiel", "the example", "Ein Beispiel dafür ist..."),
        _v("die Ansicht", "the view", "Meine Ansicht ist anders."),
        _v("die Tatsache", "the fact", "Das ist eine Tatsache."),
    ],
}

LESSON_19 = {
    "title": "Erlebnisse im Perfekt erzählen",
    "level": "B1",
    "scenario": "free",
    "topic": "Vergangenheit erzählen",
    "learning_objectives": [
        "Vergangene Ereignisse im Perfekt erzählen",
        "Die Wahl zwischen 'haben' und 'sein' verstehen",
        "Unregelmäßige Partizipien benutzen",
    ],
    "estimated_minutes": 16,
    "cultural_note": (
        "Germans love a good story — but tell it concisely. When sharing "
        "weekend or vacation experiences ('Erlebnisse'), structure your narrative "
        "with time markers (zuerst, dann, danach, schließlich) so listeners "
        "can follow."
    ),
    "dialogue": [
        _t("native", "Wie war dein Wochenende?",
           "How was your weekend?"),
        _t("learner", "Es war fantastisch! Am Samstag bin ich in die Berge gefahren und habe eine lange Wanderung gemacht.",
           "It was fantastic! On Saturday I went to the mountains and did a long hike."),
        _t("native", "Klingt anstrengend. Wo genau warst du?",
           "Sounds exhausting. Where exactly were you?"),
        _t("learner", "Ich bin in den Alpen gewesen, in der Nähe von Garmisch. Ich habe drei Berghütten besucht.",
           "I was in the Alps, near Garmisch. I visited three mountain huts."),
        _t("native", "Hast du auch Fotos gemacht?",
           "Did you also take photos?"),
        _t("learner", "Natürlich! Ich habe über hundert Fotos geschossen und am Abend habe ich sie meiner Familie geschickt.",
           "Of course! I took over a hundred photos and in the evening I sent them to my family."),
    ],
    "grammar_focus": {
        "rule_name": "Perfekt mit haben oder sein",
        "explanation": (
            "Die meisten Verben bilden das Perfekt mit 'haben'. Verben der "
            "Bewegung (gehen, fahren, fliegen, kommen) und der Zustandsänderung "
            "(aufstehen, einschlafen) sowie sein/bleiben/werden brauchen 'sein'."
        ),
        "formula": "haben/sein + Partizip II",
        "examples": [
            _gex("Ich habe ein Buch gelesen.", "I read a book.", "Aktivität → haben"),
            _gex("Ich bin nach Berlin gefahren.", "I drove to Berlin.", "Bewegung → sein"),
            _gex("Sie ist eingeschlafen.", "She fell asleep.", "Zustandswechsel → sein"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich habe nach Berlin gefahren'. Richtig: 'Ich bin nach Berlin gefahren'.",
            "Falsch: 'Ich bin ein Buch gelesen'. Richtig: 'Ich habe ein Buch gelesen'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ nach Berlin gefahren.",
                ["bin", "habe", "war", "wurde"], 0,
                "Bewegung → sein."),
        _ex_mc("Welches Partizip II ist richtig für 'gehen'?",
               ["gegangen", "gegehnt", "geht", "gehte"], 0,
               "Unregelmäßiges Partizip II."),
        _ex_arr(["habe", "Ich", "geschrieben", "Brief", "einen"],
                "Ich habe einen Brief geschrieben.",
                "Perfekt im Hauptsatz."),
        _ex_tr("Yesterday I flew to Hamburg.",
               "Gestern bin ich nach Hamburg geflogen."),
        _ex_sp("Erzähle von deinem letzten Urlaub: Wo warst du, was hast du gesehen, was hast du gemacht?",
               "past experiences", 70),
    ],
    "vocabulary_list": [
        _v("erzählen", "to tell", "Ich erzähle dir eine Geschichte."),
        _v("das Erlebnis", "the experience", "Es war ein tolles Erlebnis."),
        _v("die Wanderung", "the hike", "Die Wanderung war lang."),
        _v("die Berge", "the mountains", "Wir sind in die Berge gefahren."),
        _v("besuchen", "to visit", "Ich habe meinen Onkel besucht."),
        _v("schicken", "to send", "Ich schicke dir eine Nachricht."),
        _v("zuerst", "first", "Zuerst gehen wir essen."),
        _v("dann", "then", "Dann fahren wir nach Hause."),
        _v("danach", "afterwards", "Danach trinken wir Kaffee."),
        _v("schließlich", "finally", "Schließlich sind wir angekommen."),
        _v("die Reise", "the trip", "Die Reise war schön."),
        _v("anstrengend", "exhausting", "Der Tag war anstrengend."),
    ],
}

LESSON_20 = {
    "title": "Urlaub planen und buchen",
    "level": "B1",
    "scenario": "train_station",
    "topic": "Reiseplanung",
    "learning_objectives": [
        "Eine Reise planen und buchen",
        "Futur I für Pläne verwenden",
        "Über Urlaubsziele sprechen",
    ],
    "estimated_minutes": 16,
    "cultural_note": (
        "Germans get an average of 28–30 vacation days per year and use them. "
        "Summer vacation (Sommerferien) can be 3 weeks long. Popular destinations "
        "include the North Sea coast, Bavaria, Italy, and Spain. Last-minute "
        "Pauschalreisen (package deals) are very common."
    ),
    "dialogue": [
        _t("native", "Hast du schon Urlaubspläne für den Sommer?",
           "Do you already have vacation plans for the summer?"),
        _t("learner", "Ja, ich werde im Juli zwei Wochen nach Italien fahren. Wir haben eine Pauschalreise gebucht.",
           "Yes, in July I'll go to Italy for two weeks. We've booked a package deal."),
        _t("native", "Wohin genau in Italien?",
           "Where exactly in Italy?"),
        _t("learner", "An die Amalfiküste. Wir werden in Sorrent wohnen und Tagesausflüge machen.",
           "To the Amalfi Coast. We'll stay in Sorrento and do day trips."),
        _t("native", "Das klingt traumhaft. Wie reist ihr dorthin?",
           "That sounds dreamy. How are you traveling there?"),
        _t("learner", "Wir fliegen von Frankfurt nach Neapel und nehmen dann den Zug. Ich freue mich schon riesig.",
           "We're flying from Frankfurt to Naples and then taking the train. I'm really looking forward to it."),
    ],
    "grammar_focus": {
        "rule_name": "Futur I vs. Präsens für Zukunftspläne",
        "explanation": (
            "Im Deutschen benutzt man oft Präsens mit Zeitangabe für Zukunftspläne "
            "('Ich fahre nächste Woche nach Berlin'). Futur I betont die Absicht "
            "oder Vermutung."
        ),
        "formula": "Präsens + Zeitangabe ODER werden + Infinitiv",
        "examples": [
            _gex("Ich fahre morgen nach Berlin.", "I'm driving to Berlin tomorrow."),
            _gex("Ich werde im Sommer Urlaub machen.",
                 "I will take vacation in the summer."),
            _gex("Er wird wohl müde sein.", "He's probably tired."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich werde gehen morgen'. Richtig: 'Ich gehe morgen' (Präsens reicht).",
            "Falsch: 'Ich werde haben Urlaub'. Richtig: 'Ich werde Urlaub haben'.",
        ],
    },
    "exercises": [
        _ex_fib("Wir ___ nächsten Monat nach Spanien.",
                ["fliegen", "flogen", "geflogen", "fliegt"], 0,
                "Präsens für Zukunftsplan."),
        _ex_mc("Wann verwendet man Futur I am besten?",
               ["bei Vermutungen", "bei Befehlen",
                "bei Vergangenheit", "bei Bitten"], 0,
               "Vermutung oder Absicht."),
        _ex_arr(["werden", "Wir", "Urlaub", "im", "Sommer", "machen"],
                "Wir werden im Sommer Urlaub machen.",
                "Futur I mit Zeitangabe."),
        _ex_tr("Next year we will travel to Japan.",
               "Nächstes Jahr werden wir nach Japan reisen."),
        _ex_sp("Plane einen Traumurlaub: Wohin fährst du, wie lange, was machst du dort?",
               "vacation planning", 60),
    ],
    "vocabulary_list": [
        _v("der Urlaub", "the vacation", "Ich habe Urlaub."),
        _v("buchen", "to book", "Ich buche ein Hotel."),
        _v("die Reise", "the trip", "Die Reise war wunderbar."),
        _v("das Reiseziel", "the destination", "Mein Reiseziel ist Italien."),
        _v("die Pauschalreise", "the package tour",
           "Wir nehmen eine Pauschalreise."),
        _v("das Hotel", "the hotel", "Das Hotel ist im Zentrum."),
        _v("der Flug", "the flight", "Der Flug ist günstig."),
        _v("der Strand", "the beach", "Der Strand ist sauber."),
        _v("der Reiseführer", "the guidebook",
           "Ich lese einen Reiseführer."),
        _v("besichtigen", "to sightsee", "Wir besichtigen das Schloss."),
        _v("der Ausflug", "the day trip", "Wir machen einen Ausflug."),
        _v("sich freuen auf", "to look forward to",
           "Ich freue mich auf den Urlaub."),
    ],
}

LESSON_21 = {
    "title": "Beim Arzt — Chronische Beschwerden",
    "level": "B1",
    "scenario": "doctor",
    "topic": "Chronische Krankheiten",
    "learning_objectives": [
        "Längerfristige Symptome detailliert beschreiben",
        "Mit 'seit' + Präsens arbeiten",
        "Über Behandlungen sprechen",
    ],
    "estimated_minutes": 17,
    "cultural_note": (
        "German health insurance is mandatory: GKV (gesetzliche Krankenkasse, "
        "public, ~14.6%) or PKV (private). Most prescriptions have a Zuzahlung "
        "(co-payment) of 5–10€. Chronically ill patients can apply for "
        "Befreiung (exemption) from co-payments."
    ),
    "dialogue": [
        _t("native", "Was führt Sie heute zu mir?",
           "What brings you to me today?"),
        _t("learner", "Ich habe seit drei Wochen starke Rückenschmerzen, besonders morgens.",
           "I've had strong back pain for three weeks, especially in the mornings."),
        _t("native", "Strahlen die Schmerzen in die Beine aus?",
           "Does the pain radiate into your legs?"),
        _t("learner", "Manchmal bis ins linke Bein. Ich nehme seit einer Woche Schmerzmittel, aber sie helfen kaum.",
           "Sometimes down to my left leg. I've been taking painkillers for a week, but they barely help."),
        _t("native", "Ich überweise Sie zum Orthopäden. Wir sollten ein MRT machen lassen.",
           "I'll refer you to an orthopedist. We should have an MRI done."),
        _t("learner", "Vielen Dank. Übernimmt das die gesetzliche Krankenkasse?",
           "Thank you. Does the public health insurance cover that?"),
    ],
    "grammar_focus": {
        "rule_name": "Seit + Präsens für andauernde Zustände",
        "explanation": (
            "Im Deutschen verwendet man 'seit' + Präsens für eine Handlung, "
            "die in der Vergangenheit begonnen hat und bis jetzt andauert. "
            "Im Englischen wäre das das Present Perfect Continuous."
        ),
        "formula": "Subjekt + Verb (Präsens) + seit + Zeitangabe",
        "examples": [
            _gex("Ich habe seit drei Wochen Rückenschmerzen.",
                 "I've had back pain for three weeks."),
            _gex("Sie wohnt seit 2010 in Berlin.",
                 "She has been living in Berlin since 2010."),
            _gex("Wir lernen seit zwei Jahren Deutsch.",
                 "We've been learning German for two years."),
        ],
        "common_mistakes": [
            "Falsch: 'Ich hatte Schmerzen seit drei Wochen'. Richtig: Präsens.",
            "Falsch: 'für drei Wochen' (englisch). Richtig: 'seit drei Wochen'.",
        ],
    },
    "exercises": [
        _ex_fib("Ich ___ seit zwei Wochen Kopfschmerzen.",
                ["habe", "hatte", "haben", "hattest"], 0,
                "Andauernder Zustand → Präsens."),
        _ex_mc("Wie übersetzt man 'I have been waiting for an hour'?",
               ["Ich warte seit einer Stunde.",
                "Ich wartete für eine Stunde.",
                "Ich habe eine Stunde gewartet.",
                "Ich werde eine Stunde warten."], 0,
               "Andauernde Handlung → seit + Präsens."),
        _ex_arr(["seit", "Ich", "Berlin", "wohne", "in", "2020"],
                "Ich wohne seit 2020 in Berlin.",
                "Andauernder Zustand."),
        _ex_tr("I have been taking this medicine for a month.",
               "Ich nehme dieses Medikament seit einem Monat."),
        _ex_sp("Beschreibe deinem Arzt eine chronische Beschwerde: seit wann, wie stark, was hast du dagegen unternommen?",
               "chronic complaint", 60),
    ],
    "vocabulary_list": [
        _v("chronisch", "chronic", "Ich habe chronische Schmerzen."),
        _v("die Beschwerden", "the complaints", "Welche Beschwerden haben Sie?"),
        _v("die Schmerzen", "the pain", "Die Schmerzen sind stark."),
        _v("ausstrahlen", "to radiate", "Der Schmerz strahlt aus."),
        _v("das Schmerzmittel", "the painkiller",
           "Ich nehme ein Schmerzmittel."),
        _v("überweisen", "to refer", "Der Arzt überweist mich."),
        _v("der Facharzt", "the specialist", "Ich gehe zum Facharzt."),
        _v("das MRT", "the MRI", "Das MRT zeigt nichts."),
        _v("die Krankenkasse", "the health insurance",
           "Meine Krankenkasse übernimmt das."),
        _v("die Zuzahlung", "the co-payment", "Die Zuzahlung beträgt 10 Euro."),
        _v("die Behandlung", "the treatment", "Die Behandlung dauert lange."),
        _v("die Diagnose", "the diagnosis", "Die Diagnose ist klar."),
    ],
}

LESSON_22 = {
    "title": "Eine Wohnung mieten",
    "level": "B1",
    "scenario": "landlord",
    "topic": "Mietvertrag und Genitiv",
    "learning_objectives": [
        "Einen Mietvertrag verstehen",
        "Den Genitiv sicher anwenden",
        "Vertragsdetails erfragen",
    ],
    "estimated_minutes": 18,
    "cultural_note": (
        "A standard German rental contract includes Kaltmiete (cold rent), "
        "Nebenkosten (utilities), Kaution (deposit, max 3 months), and "
        "Kündigungsfrist (notice period, usually 3 months). 'Staffelmiete' is "
        "rent that increases yearly by a fixed amount; 'Indexmiete' rises with inflation."
    ),
    "dialogue": [
        _t("native", "Hier ist der Mietvertrag. Bitte lesen Sie ihn sorgfältig durch.",
           "Here is the rental contract. Please read it through carefully."),
        _t("learner", "Wie hoch ist die Kaution und wann muss ich sie überweisen?",
           "How high is the deposit and when do I need to transfer it?"),
        _t("native", "Die Kaution beträgt zwei Monatsmieten und ist bis zum Einzug fällig.",
           "The deposit is two months' rent and is due by move-in."),
        _t("learner", "Wie ist die Regelung der Nebenkosten?",
           "How are the utilities regulated?"),
        _t("native", "Die Nebenkosten umfassen Heizung, Wasser und Müll. Sie zahlen monatlich eine Pauschale, am Jahresende gibt es eine Abrechnung.",
           "The utilities include heating, water, and waste. You pay a monthly flat rate, at the end of the year there's a settlement."),
        _t("learner", "Verstanden. Wie lang ist die Kündigungsfrist des Vertrags?",
           "Understood. How long is the notice period of the contract?"),
    ],
    "grammar_focus": {
        "rule_name": "Genitiv",
        "explanation": (
            "Der Genitiv zeigt Besitz oder Zugehörigkeit ('wessen?'). Artikel: "
            "des/der/des bestimmt, eines/einer/eines unbestimmt. Maskulin und "
            "Neutrum bekommen meist die Endung -s oder -es."
        ),
        "formula": "Substantiv + des/der/des + Substantiv(-s/-es)",
        "examples": [
            _gex("die Höhe der Miete", "the amount of the rent"),
            _gex("der Anfang des Monats", "the beginning of the month"),
            _gex("das Ende der Woche", "the end of the week"),
        ],
        "common_mistakes": [
            "Falsch: 'die Höhe von der Miete' (umgangssprachlich). Schriftlich: Genitiv.",
            "Falsch: 'der Vater von Hans Auto'. Richtig: 'das Auto von Hans' oder 'Hans' Auto'.",
        ],
    },
    "exercises": [
        _ex_fib("Die Höhe ___ Miete ist 850 Euro.",
                ["der", "die", "den", "des"], 0,
                "Genitiv feminin: die → der."),
        _ex_mc("Welche Form ist Genitiv maskulin?",
               ["des", "der", "dem", "den"], 0,
               "Maskulin Genitiv: der → des."),
        _ex_arr(["des", "ist", "Anfang", "Der", "Monats", "schwierig"],
                "Der Anfang des Monats ist schwierig.",
                "Genitivattribut nach Substantiv."),
        _ex_tr("The end of the contract is in December.",
               "Das Ende des Vertrags ist im Dezember."),
        _ex_sp("Erkläre einem Freund die wichtigsten Punkte deines Mietvertrags.",
               "rental contract", 70),
    ],
    "vocabulary_list": [
        _v("der Mietvertrag", "the rental contract",
           "Der Mietvertrag ist lang."),
        _v("die Kaution", "the deposit", "Die Kaution ist hoch."),
        _v("die Kaltmiete", "the cold rent", "Die Kaltmiete beträgt 800 Euro."),
        _v("die Warmmiete", "the warm rent", "Die Warmmiete ist 1000 Euro."),
        _v("die Nebenkosten", "the utilities", "Die Nebenkosten sind extra."),
        _v("die Abrechnung", "the settlement", "Die Abrechnung kommt jährlich."),
        _v("die Heizung", "the heating", "Die Heizung funktioniert nicht."),
        _v("die Kündigungsfrist", "the notice period",
           "Die Kündigungsfrist ist drei Monate."),
        _v("der Einzug", "the move-in", "Der Einzug ist am Ersten."),
        _v("der Auszug", "the move-out", "Der Auszug ist nächste Woche."),
        _v("unterschreiben", "to sign", "Bitte unterschreiben Sie hier."),
        _v("die Übergabe", "the handover", "Die Übergabe ist morgen."),
    ],
}

LESSON_23 = {
    "title": "Bei der Bank",
    "level": "B1",
    "scenario": "free",
    "topic": "Bank und Passiv",
    "learning_objectives": [
        "Bankgeschäfte erledigen",
        "Das Passiv im Präsens bilden",
        "Über Konten und Karten sprechen",
    ],
    "estimated_minutes": 16,
    "cultural_note": (
        "Germans still use cash much more than other Western countries. Many "
        "small shops, bakeries, and Imbisse don't accept cards. Online banking "
        "is widespread but uses TAN-Verfahren (transaction authentication numbers) "
        "for security. Don't expect a US-style 'check' — they're nearly extinct."
    ),
    "dialogue": [
        _t("native", "Guten Tag, wie kann ich Ihnen helfen?",
           "Good day, how can I help you?"),
        _t("learner", "Ich möchte ein Girokonto eröffnen.",
           "I'd like to open a checking account."),
        _t("native", "Sehr gerne. Welche Unterlagen haben Sie dabei?",
           "Of course. What documents do you have with you?"),
        _t("learner", "Meinen Reisepass und eine Meldebescheinigung. Wie wird das Konto eröffnet?",
           "My passport and a registration certificate. How is the account opened?"),
        _t("native", "Das Konto wird sofort eröffnet, die Karte wird Ihnen in einer Woche zugeschickt.",
           "The account is opened immediately, the card will be sent to you in a week."),
        _t("learner", "Wunderbar. Und wenn die Karte verloren geht, wie wird sie gesperrt?",
           "Wonderful. And if the card is lost, how is it blocked?"),
    ],
    "grammar_focus": {
        "rule_name": "Passiv Präsens",
        "explanation": (
            "Das Passiv betont die Handlung statt den Handelnden. Bildung: "
            "'werden' + Partizip II. Im Hauptsatz steht 'werden' an Position 2, "
            "Partizip am Ende."
        ),
        "formula": "Subjekt + werden + ... + Partizip II",
        "examples": [
            _gex("Das Geld wird überwiesen.", "The money is being transferred."),
            _gex("Das Konto wird eröffnet.", "The account is being opened."),
            _gex("Die Karte wird gesperrt.", "The card is being blocked."),
        ],
        "common_mistakes": [
            "Falsch: 'Das wird sein gemacht'. Richtig: 'Das wird gemacht'.",
            "Falsch: 'Die Karte ist gesperrt' (Zustand). Vorgangspassiv: 'Die Karte wird gesperrt'.",
        ],
    },
    "exercises": [
        _ex_fib("Das Konto ___ heute eröffnet.",
                ["wird", "ist", "war", "hat"], 0,
                "Vorgangspassiv mit werden."),
        _ex_mc("Wie bildet man das Vorgangspassiv?",
               ["werden + Partizip II", "sein + Partizip II",
                "haben + Partizip II", "wird + Infinitiv"], 0,
               "Vorgang vs. Zustand."),
        _ex_arr(["wird", "Karte", "Die", "gesperrt"],
                "Die Karte wird gesperrt.",
                "Passivsatz."),
        _ex_tr("The money is transferred immediately.",
               "Das Geld wird sofort überwiesen."),
        _ex_sp("Erkläre, wie ein Konto bei der Bank eröffnet wird (im Passiv).",
               "banking processes", 60),
    ],
    "vocabulary_list": [
        _v("die Bank", "the bank", "Die Bank ist offen."),
        _v("das Konto", "the account", "Mein Konto ist leer."),
        _v("das Girokonto", "the checking account", "Ich habe ein Girokonto."),
        _v("eröffnen", "to open", "Ich eröffne ein Konto."),
        _v("schließen", "to close", "Ich schließe das Konto."),
        _v("überweisen", "to transfer", "Ich überweise das Geld."),
        _v("die Überweisung", "the transfer", "Die Überweisung dauert einen Tag."),
        _v("abheben", "to withdraw", "Ich hebe Geld ab."),
        _v("einzahlen", "to deposit", "Ich zahle Geld ein."),
        _v("die EC-Karte", "the debit card", "Meine EC-Karte ist neu."),
        _v("sperren", "to block", "Bitte sperren Sie die Karte."),
        _v("der Kontoauszug", "the bank statement",
           "Ich drucke den Kontoauszug."),
    ],
}

LESSON_24 = {
    "title": "Aktuelle Ereignisse besprechen",
    "level": "B1",
    "scenario": "free",
    "topic": "Nachrichten und indirekte Rede",
    "learning_objectives": [
        "Über Nachrichten sprechen",
        "Indirekte Rede mit Konjunktiv I bilden",
        "Quellen zitieren",
    ],
    "estimated_minutes": 17,
    "cultural_note": (
        "German news media has a strong tradition of public broadcasting "
        "(ARD, ZDF) funded by the Rundfunkbeitrag (€18.36/month per household). "
        "The Tagesschau at 20:00 is a national institution. Newspapers like "
        "Süddeutsche Zeitung and FAZ are still widely read in print."
    ),
    "dialogue": [
        _t("native", "Hast du die Nachrichten heute Morgen gesehen?",
           "Did you see the news this morning?"),
        _t("learner", "Ja, in der Tagesschau wurde berichtet, dass die Inflation gesunken sei.",
           "Yes, on the Tagesschau they reported that inflation has fallen."),
        _t("native", "Das ist eine gute Nachricht. Was sagt die Regierung dazu?",
           "That's good news. What does the government say about it?"),
        _t("learner", "Der Wirtschaftsminister erklärte, die Maßnahmen würden Wirkung zeigen.",
           "The economics minister stated that the measures are showing effect."),
        _t("native", "Glaubst du das?",
           "Do you believe that?"),
        _t("learner", "Ich bin skeptisch. Die Opposition behauptet, dass die Lage noch immer schwierig sei.",
           "I'm skeptical. The opposition claims that the situation is still difficult."),
    ],
    "grammar_focus": {
        "rule_name": "Konjunktiv I für indirekte Rede",
        "explanation": (
            "Konjunktiv I wird in der schriftlichen Nachrichtensprache benutzt, "
            "um indirekte Rede zu zeigen. Bildung meist: Verbstamm + e/est/e/en/et/en. "
            "Wenn Konjunktiv I = Indikativ, weicht man auf Konjunktiv II aus."
        ),
        "formula": "Hauptsatz + Komma + dass/wie + Konjunktiv I",
        "examples": [
            _gex("Er sagt, er sei krank.", "He says he is sick."),
            _gex("Sie behauptet, sie habe das nicht gesagt.",
                 "She claims she didn't say that."),
            _gex("Der Minister erklärt, die Maßnahmen seien wirksam.",
                 "The minister states the measures are effective."),
        ],
        "common_mistakes": [
            "Falsch: 'Er sagt, er ist krank' (Indikativ in Nachrichten).",
            "Falsch: 'Er sagt, dass er sei krank'. Mit 'dass': normaler Indikativ oder Konjunktiv.",
        ],
    },
    "exercises": [
        _ex_fib("Er sagt, er ___ krank.",
                ["sei", "ist", "war", "wäre"], 0,
                "Konjunktiv I 3. Person Singular von sein."),
        _ex_mc("Wann benutzt man Konjunktiv I?",
               ["indirekte Rede in Nachrichten", "höfliche Bitten",
                "Wünsche", "Vergangenheit"], 0,
               "Typisch für Pressesprache."),
        _ex_arr(["sei", "Sie", "müde,", "sagt,", "sie"],
                "Sie sagt, sie sei müde.",
                "Indirekte Rede."),
        _ex_tr("The president said he would resign.",
               "Der Präsident sagte, er werde zurücktreten."),
        _ex_sp("Berichte über eine aktuelle Nachricht in indirekter Rede.",
               "reporting news", 70),
    ],
    "vocabulary_list": [
        _v("die Nachrichten", "the news", "Ich sehe die Nachrichten."),
        _v("die Regierung", "the government", "Die Regierung ist neu."),
        _v("die Opposition", "the opposition",
           "Die Opposition kritisiert das."),
        _v("die Inflation", "the inflation", "Die Inflation steigt."),
        _v("die Maßnahme", "the measure", "Die Maßnahme ist hart."),
        _v("berichten", "to report", "Die Zeitung berichtet darüber."),
        _v("erklären", "to explain/declare", "Er erklärt seine Position."),
        _v("behaupten", "to claim", "Sie behauptet das Gegenteil."),
        _v("die Meinung", "the opinion", "Meine Meinung ist anders."),
        _v("kritisieren", "to criticize",
           "Die Presse kritisiert die Politik."),
        _v("die Quelle", "the source", "Die Quelle ist verlässlich."),
        _v("wirksam", "effective", "Die Maßnahme ist wirksam."),
    ],
}


# =====================================================================
# B2 — 6 lessons
# =====================================================================

LESSON_25 = {
    "title": "Formelle E-Mails und Briefe schreiben",
    "level": "B2",
    "scenario": "job_interview",
    "topic": "Formelle Korrespondenz",
    "learning_objectives": [
        "Eine formelle E-Mail strukturieren",
        "Nominalisierung von Verben anwenden",
        "Höfliche Schlussformeln benutzen",
    ],
    "estimated_minutes": 20,
    "cultural_note": (
        "A German formal letter follows a strict structure: Absender (sender, "
        "top left), Empfänger (recipient, below), Datum (date, right-aligned), "
        "Betreff (subject), Anrede ('Sehr geehrte Damen und Herren,'), body, "
        "Schlussformel ('Mit freundlichen Grüßen'), signature, attachments noted."
    ),
    "dialogue": [
        _t("native", "Wie beginnt man eine formelle E-Mail im Deutschen am besten?",
           "What's the best way to start a formal email in German?"),
        _t("learner", "Mit der Anrede 'Sehr geehrte Frau Müller,' wenn man den Namen kennt.",
           "With 'Sehr geehrte Frau Müller,' if you know the name."),
        _t("native", "Und wenn man den Empfänger nicht kennt?",
           "And if you don't know the recipient?"),
        _t("learner", "Dann schreibt man 'Sehr geehrte Damen und Herren,'. Das ist die unpersönliche Standardform.",
           "Then you write 'Sehr geehrte Damen und Herren,'. That's the impersonal standard form."),
        _t("native", "Und welche Schlussformel ist angebracht?",
           "And which closing formula is appropriate?"),
        _t("learner", "'Mit freundlichen Grüßen' ist neutral und professionell. Bei sehr formellem Anlass geht auch 'Hochachtungsvoll'.",
           "'Mit freundlichen Grüßen' is neutral and professional. For very formal occasions, 'Hochachtungsvoll' also works."),
    ],
    "grammar_focus": {
        "rule_name": "Nominalisierung von Verben",
        "explanation": (
            "In formeller Schriftsprache werden Verben oft als Substantive "
            "verwendet (Nominalisierung). Das macht den Text dichter und "
            "objektiver. 'bitten' → 'die Bitte', 'anfragen' → 'die Anfrage'."
        ),
        "formula": "Verb → Substantiv (-ung, -e, oder Stammform)",
        "examples": [
            _gex("die Bitte um Antwort", "the request for an answer", "← bitten"),
            _gex("die Anfrage zum Termin", "the inquiry about the appointment", "← anfragen"),
            _gex("die Zusendung der Unterlagen", "the sending of the documents", "← zusenden"),
        ],
        "common_mistakes": [
            "Falsch: 'Ich bitte um die zu schicken'. Richtig: 'Ich bitte um die Zusendung'.",
            "Falsch: 'die anfrage' (klein). Richtig: Substantive immer großschreiben.",
        ],
    },
    "exercises": [
        _ex_fib("Mit freundlichen ___",
                ["Grüßen", "Grüße", "Gruß", "Grüßung"], 0,
                "Standard-Schlussformel im Dativ Plural."),
        _ex_mc("Welche Anrede ist formell richtig?",
               ["Sehr geehrte Frau Müller,", "Hi Frau Müller,",
                "Hallo Frau Müller!", "Liebe Frau Müller."], 0,
               "Geschäftlicher Standard."),
        _ex_arr(["um", "Ich", "bitte", "Antwort", "Ihre", "baldige"],
                "Ich bitte um Ihre baldige Antwort.",
                "Höfliche Bitte mit Adjektivattribut."),
        _ex_tr("I am writing in reference to your advertisement.",
               "Ich schreibe in Bezug auf Ihre Anzeige."),
        _ex_sp("Diktiere eine formelle E-Mail an eine Firma, in der du dich nach einer Stelle erkundigst.",
               "formal email", 80),
    ],
    "vocabulary_list": [
        _v("die Anrede", "the salutation", "Die Anrede ist wichtig."),
        _v("die Schlussformel", "the closing formula",
           "Die Schlussformel ist 'Mit freundlichen Grüßen'."),
        _v("der Betreff", "the subject", "Im Betreff steht 'Bewerbung'."),
        _v("der Empfänger", "the recipient",
           "Der Empfänger ist die Personalabteilung."),
        _v("der Absender", "the sender", "Der Absender steht oben links."),
        _v("die Anfrage", "the inquiry", "Ich habe eine Anfrage."),
        _v("die Bitte", "the request", "Ich habe eine Bitte."),
        _v("der Anhang", "the attachment", "Im Anhang finden Sie..."),
        _v("die Unterlagen", "the documents",
           "Die Unterlagen sind beigefügt."),
        _v("die Rückmeldung", "the feedback",
           "Ich erwarte Ihre Rückmeldung."),
        _v("hochachtungsvoll", "respectfully",
           "Hochachtungsvoll, Hans Sharma."),
        _v("baldmöglichst", "as soon as possible",
           "Bitte antworten Sie baldmöglichst."),
    ],
}

LESSON_26 = {
    "title": "Argumentieren und debattieren",
    "level": "B2",
    "scenario": "free",
    "topic": "Argumentation und Konzessivsätze",
    "learning_objectives": [
        "Strukturiert argumentieren",
        "Konzessivsätze mit 'obwohl' und 'trotzdem' bilden",
        "Gegenargumente anerkennen",
    ],
    "estimated_minutes": 18,
    "cultural_note": (
        "German debate culture values logical structure: Behauptung "
        "(claim), Begründung (justification), Beispiel (example), "
        "Schlussfolgerung (conclusion). Acknowledging counter-arguments is "
        "seen as intellectual honesty, not weakness."
    ),
    "dialogue": [
        _t("native", "Findest du, dass Elektroautos die Lösung für den Klimawandel sind?",
           "Do you think electric cars are the solution for climate change?"),
        _t("learner", "Obwohl sie keine Abgase produzieren, ist die Herstellung der Batterien sehr umweltschädlich.",
           "Although they produce no exhaust, the production of the batteries is very environmentally harmful."),
        _t("native", "Das stimmt. Trotzdem sind sie langfristig besser als Verbrenner.",
           "That's true. Nevertheless, they're better than combustion engines in the long term."),
        _t("learner", "Wenngleich ich dir grundsätzlich zustimme, müssen wir auch die Stromquelle bedenken.",
           "Although I basically agree with you, we also need to consider the power source."),
        _t("native", "Ein gutes Argument. Erneuerbare Energien sind der Schlüssel.",
           "A good argument. Renewable energies are the key."),
        _t("learner", "Genau. Dennoch reicht das allein nicht — wir brauchen auch Verhaltensänderungen.",
           "Exactly. Nevertheless, that alone isn't enough — we also need behavior changes."),
    ],
    "grammar_focus": {
        "rule_name": "Konzessivsätze",
        "explanation": (
            "Konzessivsätze drücken einen Gegensatz aus. 'Obwohl' leitet einen "
            "Nebensatz ein (Verb am Ende). 'Trotzdem', 'dennoch', 'wenngleich' "
            "stehen im Hauptsatz und schieben das konjugierte Verb auf Position 2."
        ),
        "formula": "obwohl + Nebensatz / Hauptsatz + trotzdem + Hauptsatz",
        "examples": [
            _gex("Obwohl es regnet, gehe ich spazieren.",
                 "Although it's raining, I'm going for a walk."),
            _gex("Es regnet, trotzdem gehe ich spazieren.",
                 "It's raining; nevertheless I'm going for a walk."),
            _gex("Wenngleich es schwer ist, schaffe ich es.",
                 "Although it's hard, I'll manage it."),
        ],
        "common_mistakes": [
            "Falsch: 'Obwohl ich bin müde'. Richtig: 'Obwohl ich müde bin'.",
            "Falsch: 'Trotzdem ich gehe'. Richtig: 'Trotzdem gehe ich'.",
        ],
    },
    "exercises": [
        _ex_fib("___ es kalt ist, schwimmen wir im See.",
                ["Obwohl", "Trotzdem", "Weil", "Wenn"], 0,
                "Konzessive Konjunktion mit Nebensatz."),
        _ex_mc("Wie ist die Wortstellung nach 'trotzdem'?",
               ["Verb an Position 2", "Verb am Ende",
                "Verb an Position 1", "Verb nach dem Subjekt"], 0,
               "Trotzdem ist Adverb, kein Konjunktor."),
        _ex_arr(["regnet", "es,", "Obwohl", "wir", "spazieren", "gehen"],
                "Obwohl es regnet, gehen wir spazieren.",
                "Konzessivsatz mit obwohl."),
        _ex_tr("Although he is tired, he keeps working.",
               "Obwohl er müde ist, arbeitet er weiter."),
        _ex_sp("Argumentiere für oder gegen die These: 'Soziale Medien sind schlecht für Jugendliche.' Verwende mindestens zwei Konzessivsätze.",
               "argumentation", 90),
    ],
    "vocabulary_list": [
        _v("argumentieren", "to argue", "Sie argumentiert klar."),
        _v("debattieren", "to debate", "Wir debattieren das Thema."),
        _v("die Behauptung", "the claim",
           "Deine Behauptung ist nicht belegt."),
        _v("die Begründung", "the justification",
           "Die Begründung ist logisch."),
        _v("das Gegenargument", "the counter-argument",
           "Mein Gegenargument lautet..."),
        _v("die Schlussfolgerung", "the conclusion",
           "Die Schlussfolgerung ist klar."),
        _v("obwohl", "although", "Obwohl es regnet, gehe ich raus."),
        _v("trotzdem", "nevertheless", "Es regnet, trotzdem gehe ich raus."),
        _v("dennoch", "yet/still", "Es ist schwer, dennoch versuche ich es."),
        _v("anerkennen", "to acknowledge",
           "Ich erkenne dein Argument an."),
        _v("widerlegen", "to refute", "Diese These ist leicht zu widerlegen."),
        _v("der Standpunkt", "the standpoint", "Mein Standpunkt ist klar."),
    ],
}

LESSON_27 = {
    "title": "Konjunktiv II — Hypothesen und Wünsche",
    "level": "B2",
    "scenario": "free",
    "topic": "Hypothesen und irreale Wünsche",
    "learning_objectives": [
        "Konjunktiv II in synthetischer Form bilden",
        "Würde + Infinitiv korrekt einsetzen",
        "Irreale Wünsche und Bedingungssätze formulieren",
    ],
    "estimated_minutes": 19,
    "cultural_note": (
        "Konjunktiv II is the German learner's nightmare and the German "
        "speaker's daily tool. In speech, 'würde + Infinitiv' has largely "
        "replaced synthetic forms — except for a core set: wäre, hätte, "
        "könnte, müsste, dürfte, sollte, wollte, wüsste, gäbe, fände."
    ),
    "dialogue": [
        _t("native", "Wenn du im Lotto gewinnen würdest, was würdest du tun?",
           "If you won the lottery, what would you do?"),
        _t("learner", "Ich würde sofort ein Haus am Meer kaufen und meinen Eltern eine Reise schenken.",
           "I would immediately buy a house by the sea and give my parents a trip."),
        _t("native", "Würdest du dann auch nicht mehr arbeiten?",
           "Would you then also not work anymore?"),
        _t("learner", "Doch, ich würde weiterarbeiten. Aber ich könnte mehr Pausen machen.",
           "Yes, I would keep working. But I could take more breaks."),
        _t("native", "An deiner Stelle würde ich eine Weltreise machen.",
           "In your place, I would take a trip around the world."),
        _t("learner", "Wenn ich mehr Zeit hätte, wäre das auch mein Traum.",
           "If I had more time, that would also be my dream."),
    ],
    "grammar_focus": {
        "rule_name": "Konjunktiv II — synthetisch vs. analytisch",
        "explanation": (
            "Synthetische Formen (wäre, hätte, könnte, müsste, dürfte, wüsste) "
            "sind im Sprachgebrauch üblich. Für andere Verben benutzt man "
            "'würde + Infinitiv'. In Bedingungssätzen kann man wechseln."
        ),
        "formula": "wäre/hätte/... ODER würde + Infinitiv",
        "examples": [
            _gex("Ich hätte gerne mehr Zeit.", "I would like to have more time."),
            _gex("An deiner Stelle würde ich gehen.", "In your place I would go."),
            _gex("Wenn ich reich wäre, könnte ich reisen.",
                 "If I were rich, I could travel."),
        ],
        "common_mistakes": [
            "Falsch: 'Wenn ich würde gewinnen'. Richtig: 'Wenn ich gewinnen würde' oder 'Wenn ich gewänne'.",
            "Falsch: 'Ich würde haben gerne'. Richtig: 'Ich hätte gerne'.",
        ],
    },
    "exercises": [
        _ex_fib("Wenn ich Zeit ___, würde ich kommen.",
                ["hätte", "habe", "haben", "hatte"], 0,
                "Konjunktiv II von haben in der Bedingung."),
        _ex_mc("Welche Form ist Konjunktiv II von 'sein'?",
               ["wäre", "war", "ist", "sein"], 0,
               "Synthetische Form."),
        _ex_arr(["dich", "An", "Stelle", "deiner", "ich", "würde", "fragen"],
                "An deiner Stelle würde ich dich fragen.",
                "Höflicher Ratschlag."),
        _ex_tr("If I knew the answer, I would tell you.",
               "Wenn ich die Antwort wüsste, würde ich es dir sagen."),
        _ex_sp("Beschreibe, was du machen würdest, wenn du eine Million Euro gewinnen würdest. Verwende mindestens drei Konjunktiv-II-Formen.",
               "hypothetical scenario", 80),
    ],
    "vocabulary_list": [
        _v("die Hypothese", "the hypothesis", "Das ist nur eine Hypothese."),
        _v("der Wunsch", "the wish", "Mein Wunsch ist Frieden."),
        _v("der Traum", "the dream", "Mein Traum ist eine Weltreise."),
        _v("gewinnen", "to win", "Ich möchte im Lotto gewinnen."),
        _v("schenken", "to give as a gift", "Ich schenke dir ein Buch."),
        _v("die Bedingung", "the condition",
           "Die Bedingung ist akzeptabel."),
        _v("möglich", "possible", "Das ist nicht möglich."),
        _v("unmöglich", "impossible", "Das ist unmöglich."),
        _v("wahrscheinlich", "probable", "Das ist wahrscheinlich."),
        _v("sich vorstellen", "to imagine",
           "Ich kann mir das vorstellen."),
        _v("verzichten auf", "to do without",
           "Ich verzichte auf Süßigkeiten."),
        _v("die Weltreise", "the trip around the world",
           "Sie macht eine Weltreise."),
    ],
}

LESSON_28 = {
    "title": "Akademische und abstrakte Sprache",
    "level": "B2",
    "scenario": "free",
    "topic": "Wissenschaftssprache",
    "learning_objectives": [
        "Akademische Texte verstehen",
        "Erweiterte Partizipialattribute erkennen",
        "Komplexe Substantivphrasen bilden",
    ],
    "estimated_minutes": 20,
    "cultural_note": (
        "German academic prose loves long sentences with embedded participle "
        "clauses ('erweiterte Partizipialattribute'). They condense information "
        "but make texts hard to read. Newspapers like FAZ and Die Zeit use them "
        "frequently. In speech they sound stilted."
    ),
    "dialogue": [
        _t("native", "Hast du den Artikel über die in Berlin lebenden Wissenschaftler gelesen?",
           "Did you read the article about the scientists living in Berlin?"),
        _t("learner", "Ja, der von Frau Dr. Weber verfasste Beitrag war sehr informativ.",
           "Yes, the article written by Dr. Weber was very informative."),
        _t("native", "Welche Erkenntnisse hat sie präsentiert?",
           "What findings did she present?"),
        _t("learner", "Sie analysiert das vor drei Jahren gegründete Forschungsinstitut und seine Ergebnisse.",
           "She analyzes the research institute founded three years ago and its results."),
        _t("native", "Sind diese Ergebnisse für die internationale Forschung relevant?",
           "Are these results relevant for international research?"),
        _t("learner", "Absolut. Die in dieser Studie untersuchten Methoden gelten als bahnbrechend.",
           "Absolutely. The methods examined in this study are considered groundbreaking."),
    ],
    "grammar_focus": {
        "rule_name": "Erweitertes Partizipialattribut",
        "explanation": (
            "Ein erweitertes Partizipialattribut ist ein komplexes Adjektiv, "
            "das aus einem Partizip I oder II + Ergänzungen besteht. Es steht "
            "zwischen Artikel und Substantiv und ersetzt einen Relativsatz."
        ),
        "formula": "Artikel + [Ergänzungen + Partizip] + Substantiv",
        "examples": [
            _gex("der in Berlin lebende Wissenschaftler",
                 "the scientist living in Berlin",
                 "= der Wissenschaftler, der in Berlin lebt"),
            _gex("das vor drei Jahren gegründete Unternehmen",
                 "the company founded three years ago",
                 "= das Unternehmen, das vor drei Jahren gegründet wurde"),
            _gex("die von der Regierung beschlossenen Maßnahmen",
                 "the measures decided by the government"),
        ],
        "common_mistakes": [
            "Falsch: 'der lebende in Berlin Wissenschaftler'. Richtig: Ergänzungen vor Partizip.",
            "Falsch: Vergessen der Adjektivendung. Beispiel: 'der lebend' → 'der lebende'.",
        ],
    },
    "exercises": [
        _ex_fib("Der ___ Artikel war interessant.",
                ["gestern erschienene", "erscheinende gestern",
                 "gestern erscheinen", "erschienen gestern"], 0,
                "Partizip II + Ergänzung vorne."),
        _ex_mc("Was ersetzt ein Partizipialattribut?",
               ["einen Relativsatz", "einen Hauptsatz",
                "einen Konditionalsatz", "einen Fragesatz"], 0,
               "Komprimierung eines Relativsatzes."),
        _ex_arr(["gegründete", "Das", "Jahren", "vor", "Unternehmen", "drei", "wächst"],
                "Das vor drei Jahren gegründete Unternehmen wächst.",
                "Komplexes Partizipialattribut."),
        _ex_tr("The book recently published in Berlin is excellent.",
               "Das kürzlich in Berlin veröffentlichte Buch ist hervorragend."),
        _ex_sp("Beschreibe ein bedeutendes wissenschaftliches Projekt mit erweiterten Partizipialattributen.",
               "academic description", 80),
    ],
    "vocabulary_list": [
        _v("die Wissenschaft", "the science", "Die Wissenschaft entwickelt sich."),
        _v("der Wissenschaftler", "the scientist",
           "Der Wissenschaftler forscht."),
        _v("die Forschung", "the research",
           "Die Forschung ist wichtig."),
        _v("untersuchen", "to examine", "Wir untersuchen das Problem."),
        _v("die Studie", "the study",
           "Die Studie zeigt klare Ergebnisse."),
        _v("das Ergebnis", "the result",
           "Die Ergebnisse sind eindeutig."),
        _v("die Erkenntnis", "the finding/insight",
           "Eine wichtige Erkenntnis."),
        _v("der Beitrag", "the contribution/article",
           "Sein Beitrag ist wertvoll."),
        _v("verfassen", "to compose/write",
           "Er verfasst einen Aufsatz."),
        _v("analysieren", "to analyze",
           "Wir analysieren die Daten."),
        _v("bahnbrechend", "groundbreaking",
           "Eine bahnbrechende Entdeckung."),
        _v("die Methode", "the method", "Die Methode ist neu."),
    ],
}

LESSON_29 = {
    "title": "Offizielle Beschwerden einreichen",
    "level": "B2",
    "scenario": "free",
    "topic": "Beschwerdeschreiben und Modalpartikeln",
    "learning_objectives": [
        "Eine offizielle Beschwerde formulieren",
        "Modalpartikeln richtig einsetzen",
        "Forderungen klar äußern",
    ],
    "estimated_minutes": 19,
    "cultural_note": (
        "German consumer protection is strong. For complaints about goods, "
        "you have a 14-day Widerrufsrecht for online purchases and a 2-year "
        "Gewährleistung (warranty) by law. Complaints to companies should be "
        "in writing — Germans take written records seriously."
    ),
    "dialogue": [
        _t("native", "Du bist ja ganz schön aufgeregt — was ist denn passiert?",
           "You're quite upset — what happened?"),
        _t("learner", "Das Internet funktioniert seit drei Tagen nicht. Ich habe die Hotline doch schon zweimal angerufen!",
           "The internet hasn't worked for three days. I've already called the hotline twice!"),
        _t("native", "Hast du eigentlich eine schriftliche Beschwerde eingereicht?",
           "Have you actually filed a written complaint?"),
        _t("learner", "Nein, noch nicht. Ich werde aber heute Abend mal ein Beschwerdeschreiben aufsetzen.",
           "No, not yet. But I'll draft a complaint letter tonight."),
        _t("native", "Mach das. Schreib auch gleich, dass du eine Entschädigung verlangst.",
           "Do that. Also write right away that you demand compensation."),
        _t("learner", "Ja, das ist halt der einzige Weg, eine Reaktion zu bekommen.",
           "Yes, that's just the only way to get a reaction."),
    ],
    "grammar_focus": {
        "rule_name": "Modalpartikeln",
        "explanation": (
            "Modalpartikeln (doch, eben, halt, ja, schon, mal, denn) drücken "
            "Einstellung des Sprechers aus. Sie sind in der gesprochenen "
            "Sprache sehr häufig und werden oft schwer wörtlich übersetzt."
        ),
        "formula": "Im Mittelfeld nach dem konjugierten Verb",
        "examples": [
            _gex("Das ist doch klar.", "That's obvious, isn't it.",
                 "doch → Erinnerung, Widerspruch"),
            _gex("Komm mal her.", "Come here, will you.",
                 "mal → freundliche Aufforderung"),
            _gex("Was ist denn los?", "What's going on?",
                 "denn → freundliche Frage"),
        ],
        "common_mistakes": [
            "Falsch: 'Das ist doch nicht klar' (ironisch). Achte auf Kontext.",
            "Falsch: Modalpartikeln am Satzanfang. Sie stehen IMMER im Mittelfeld.",
        ],
    },
    "exercises": [
        _ex_fib("Komm ___ her!",
                ["mal", "ja", "denn", "doch"], 0,
                "Freundliche Aufforderung."),
        _ex_mc("Welche Modalpartikel signalisiert eine freundliche Frage?",
               ["denn", "doch", "halt", "ja"], 0,
               "Typisch in Fragen."),
        _ex_arr(["doch", "Das", "klar", "ist"],
                "Das ist doch klar.",
                "Modalpartikel im Mittelfeld."),
        _ex_tr("I demand a refund.",
               "Ich verlange eine Rückerstattung."),
        _ex_sp("Schreibe (laut) ein Beschwerdeschreiben an deinen Internetanbieter wegen schlechter Verbindung.",
               "complaint letter", 80),
    ],
    "vocabulary_list": [
        _v("die Beschwerde", "the complaint",
           "Ich habe eine Beschwerde."),
        _v("einreichen", "to submit",
           "Ich reiche die Beschwerde ein."),
        _v("die Entschädigung", "the compensation",
           "Ich verlange Entschädigung."),
        _v("die Rückerstattung", "the refund",
           "Bitte um Rückerstattung."),
        _v("verlangen", "to demand", "Ich verlange eine Antwort."),
        _v("der Vertrag", "the contract",
           "Mein Vertrag ist gültig."),
        _v("kündigen", "to cancel/terminate",
           "Ich kündige den Vertrag."),
        _v("die Frist", "the deadline", "Die Frist läuft ab."),
        _v("schriftlich", "in writing",
           "Bitte schriftlich antworten."),
        _v("die Hotline", "the hotline",
           "Ich rufe die Hotline an."),
        _v("die Verbindung", "the connection",
           "Die Verbindung ist schlecht."),
        _v("der Anbieter", "the provider",
           "Mein Anbieter ist teuer."),
    ],
}

LESSON_30 = {
    "title": "Gehaltsverhandlung und Karriere",
    "level": "B2",
    "scenario": "job_interview",
    "topic": "Gehaltsverhandlung",
    "learning_objectives": [
        "Selbstbewusst über Gehalt verhandeln",
        "Indirekte Rede mit Konjunktiv I Perfekt bilden",
        "Argumente für eine Gehaltserhöhung formulieren",
    ],
    "estimated_minutes": 20,
    "cultural_note": (
        "Salary negotiations in Germany are increasingly common but still "
        "more reserved than in the US. Bring concrete numbers (Gehaltswunsch), "
        "comparable salaries (e.g. via stepstone.de or glassdoor.de), and "
        "a list of accomplishments. Bonuses are less common; base salary matters."
    ),
    "dialogue": [
        _t("native", "Sie haben um dieses Gespräch gebeten. Worum geht es genau?",
           "You requested this meeting. What exactly is it about?"),
        _t("learner", "Ich möchte über mein Gehalt sprechen. In den letzten zwei Jahren habe ich zusätzliche Verantwortung übernommen.",
           "I'd like to talk about my salary. In the last two years I've taken on additional responsibility."),
        _t("native", "Was haben Sie konkret geleistet?",
           "What have you concretely accomplished?"),
        _t("learner", "Ich habe drei wichtige Projekte erfolgreich abgeschlossen. Mein Vorgesetzter hat mehrfach gesagt, ich habe das Team entlastet.",
           "I have successfully completed three important projects. My supervisor has said several times that I have relieved the team."),
        _t("native", "Welche Gehaltsvorstellung haben Sie?",
           "What salary expectation do you have?"),
        _t("learner", "Eine Erhöhung um zehn Prozent würde meine Leistung angemessen widerspiegeln.",
           "A ten-percent increase would adequately reflect my performance."),
    ],
    "grammar_focus": {
        "rule_name": "Indirekte Rede in der Vergangenheit (Konjunktiv I Perfekt)",
        "explanation": (
            "Wenn die ursprüngliche Aussage in der Vergangenheit stand, benutzt "
            "man im Konjunktiv I die Perfekt-Form: 'habe/sei + Partizip II'. "
            "Das markiert klar, dass es um Vergangenheit geht."
        ),
        "formula": "habe/sei + Partizip II",
        "examples": [
            _gex("Er sagte, er habe gearbeitet.", "He said he had worked."),
            _gex("Sie behauptete, sie sei pünktlich gewesen.",
                 "She claimed she had been on time."),
            _gex("Der Chef erklärte, das Projekt sei erfolgreich gewesen.",
                 "The boss stated the project had been successful."),
        ],
        "common_mistakes": [
            "Falsch: 'Er sagte, er hat gearbeitet' (Indikativ in Berichten).",
            "Falsch: 'Sie sagte, sie war müde' → besser 'sie sei müde gewesen'.",
        ],
    },
    "exercises": [
        _ex_fib("Er sagte, er ___ das Projekt abgeschlossen.",
                ["habe", "hat", "ist", "wäre"], 0,
                "Konjunktiv I Perfekt mit haben."),
        _ex_mc("Wie bildet man Konjunktiv I Perfekt?",
               ["habe/sei + Partizip II", "wäre + Infinitiv",
                "haben + Konjunktiv II", "Präteritum"], 0,
               "Indirekte Rede der Vergangenheit."),
        _ex_arr(["sei", "Sie", "gewesen,", "krank", "sagte,", "sie"],
                "Sie sagte, sie sei krank gewesen.",
                "Konjunktiv I Perfekt von sein."),
        _ex_tr("She said she had finished the project.",
               "Sie sagte, sie habe das Projekt beendet."),
        _ex_sp("Bereite eine Gehaltsverhandlung vor: Argumentiere für eine Erhöhung mit konkreten Leistungen aus der Vergangenheit.",
               "salary negotiation", 90),
    ],
    "vocabulary_list": [
        _v("das Gehalt", "the salary", "Mein Gehalt ist gut."),
        _v("die Gehaltserhöhung", "the salary increase",
           "Ich bekomme eine Gehaltserhöhung."),
        _v("verhandeln", "to negotiate",
           "Wir verhandeln über das Gehalt."),
        _v("die Leistung", "the performance/achievement",
           "Meine Leistung ist hoch."),
        _v("die Verantwortung", "the responsibility",
           "Ich übernehme Verantwortung."),
        _v("der Vorgesetzte", "the supervisor",
           "Mein Vorgesetzter ist fair."),
        _v("die Beförderung", "the promotion",
           "Ich erwarte eine Beförderung."),
        _v("die Karriere", "the career",
           "Meine Karriere läuft gut."),
        _v("erfolgreich", "successful",
           "Das Projekt war erfolgreich."),
        _v("abschließen", "to complete",
           "Ich schließe das Projekt ab."),
        _v("die Gehaltsvorstellung", "the salary expectation",
           "Meine Gehaltsvorstellung ist klar."),
        _v("widerspiegeln", "to reflect",
           "Das Gehalt widerspiegelt die Leistung."),
    ],
}


# =====================================================================
# Master list (used by curriculum_service.seed_all_lessons & main.py)
# =====================================================================

LESSONS: List[dict] = [
    LESSON_01, LESSON_02, LESSON_03, LESSON_04, LESSON_05, LESSON_06, LESSON_07, LESSON_08,
    LESSON_09, LESSON_10, LESSON_11, LESSON_12, LESSON_13, LESSON_14, LESSON_15, LESSON_16,
    LESSON_17, LESSON_18, LESSON_19, LESSON_20, LESSON_21, LESSON_22, LESSON_23, LESSON_24,
    LESSON_25, LESSON_26, LESSON_27, LESSON_28, LESSON_29, LESSON_30,
]


async def seed_default_lessons(session: AsyncSession) -> int:
    """Insert any LESSONS not yet present in the database. Returns count added."""
    from models.orm_models import Lesson  # local to avoid import cycles

    existing_titles = {
        row[0]
        for row in (await session.execute(select(Lesson.title))).all()
    }

    added = 0
    for index, lesson in enumerate(LESSONS):
        if lesson["title"] in existing_titles:
            continue
        session.add(
            Lesson(
                title=lesson["title"],
                level=lesson["level"],
                scenario=lesson["scenario"],
                topic=lesson["topic"],
                content_json=lesson,
                order_index=index,
            )
        )
        added += 1

    if added:
        await session.commit()
    return added

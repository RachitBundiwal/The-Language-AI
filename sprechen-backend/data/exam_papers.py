"""Authentic Goethe-Institut style exam papers for A1, A2, B1, B2.

All German content is hand-written and level-appropriate. Each multiple-choice
answer is derivable from the provided text/script. Question numbering inside a
section is FLAT (global question_id), so the grader can map answers without
ambiguity.
"""
from __future__ import annotations

# =====================================================================
# A1 — Lesen
# =====================================================================
A1_LESEN = {
    "level": "A1",
    "section": "Lesen",
    "time_limit_minutes": 45,
    "max_score": 45,
    "instructions": (
        "Lies die Texte und beantworte die Fragen. "
        "Kreuze für jede Aufgabe die richtige Antwort an."
    ),
    "parts": [
        {
            "part_number": 1,
            "instruction": (
                "Lies die fünf Anzeigen. Sind die Aussagen 1–5 'Richtig' oder "
                "'Falsch'? Wenn die Information nicht im Text steht, wähle "
                "'Nicht im Text'."
            ),
            "max_points": 15,
            "texts": [
                {
                    "title": "Anzeige 1 — Wohnung",
                    "text": (
                        "Zu vermieten: 2-Zimmer-Wohnung, 65 m², 850 € kalt + "
                        "Nebenkosten, Stadtmitte Berlin. Balkon, Aufzug, "
                        "ab sofort frei. Tel: 030-445521"
                    ),
                },
                {
                    "title": "Anzeige 2 — Nachhilfe",
                    "text": (
                        "Suche Nachhilfelehrer für Mathematik, Klasse 8. "
                        "15 €/Stunde, einmal pro Woche, in München-Nord. "
                        "Bitte melden bei: eltern@mail.de"
                    ),
                },
                {
                    "title": "Anzeige 3 — Fahrrad",
                    "text": (
                        "Verkaufe Fahrrad, blau, 28 Zoll, neuwertig, 150 €. "
                        "Mit Licht und Schloss. Abzuholen in Hamburg-Eimsbüttel. "
                        "Bei Interesse SMS an 0176-1234567."
                    ),
                },
                {
                    "title": "Anzeige 4 — Deutschkurs",
                    "text": (
                        "Deutschkurs für Anfänger (A1): Mo/Mi 18–20 Uhr. "
                        "VHS München, Raum 12. Kurs beginnt am 5. Oktober. "
                        "Anmeldung bis 30. September online."
                    ),
                },
                {
                    "title": "Anzeige 5 — Stadtfest",
                    "text": (
                        "Stadtfest Köln am 15. August von 12 bis 22 Uhr. "
                        "Eintritt frei! Live-Musik, Essen und Getränke aus "
                        "aller Welt. Familien willkommen."
                    ),
                },
            ],
            "questions": [
                {
                    "question": "Die Wohnung in Berlin kostet 850 € warm.",
                    "options": ["Richtig", "Falsch", "Nicht im Text"],
                    "correct_index": 1,
                    "question_type": "true_false_notmentioned",
                },
                {
                    "question": "Der Nachhilfelehrer soll Mathematik unterrichten.",
                    "options": ["Richtig", "Falsch", "Nicht im Text"],
                    "correct_index": 0,
                    "question_type": "true_false_notmentioned",
                },
                {
                    "question": "Das Fahrrad ist neu und kostet 200 €.",
                    "options": ["Richtig", "Falsch", "Nicht im Text"],
                    "correct_index": 1,
                    "question_type": "true_false_notmentioned",
                },
                {
                    "question": "Der Deutschkurs findet am Wochenende statt.",
                    "options": ["Richtig", "Falsch", "Nicht im Text"],
                    "correct_index": 1,
                    "question_type": "true_false_notmentioned",
                },
                {
                    "question": "Beim Stadtfest in Köln muss man Eintritt zahlen.",
                    "options": ["Richtig", "Falsch", "Nicht im Text"],
                    "correct_index": 1,
                    "question_type": "true_false_notmentioned",
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": (
                "Lies die E-Mail von Lena. Wähle für jede Frage die richtige Antwort."
            ),
            "max_points": 20,
            "texts": [
                {
                    "title": "E-Mail von Lena",
                    "text": (
                        "Hallo Anna,\n\n"
                        "wie geht es dir? Mir geht es sehr gut! Ich habe endlich "
                        "meine neue Wohnung in Hamburg gefunden. Ich bin letzte "
                        "Woche aus München umgezogen und bin sehr glücklich hier.\n\n"
                        "Die Wohnung hat drei Zimmer, eine kleine Küche und einen "
                        "großen Balkon. Sie liegt im vierten Stock, aber es gibt "
                        "einen Aufzug. Die Miete ist 950 € warm. Das ist "
                        "ein bisschen teuer, aber das Viertel ist sehr ruhig.\n\n"
                        "In meiner Straße gibt es einen Bäcker, einen Supermarkt "
                        "und ein kleines Café. Der Bahnhof ist nur zehn Minuten "
                        "zu Fuß entfernt. Das ist perfekt für mich, denn ich fange "
                        "am Montag meine neue Arbeit als Krankenschwester im "
                        "Krankenhaus an.\n\n"
                        "Kommst du mich bald besuchen? Ich freue mich auf dich!\n\n"
                        "Liebe Grüße,\nLena"
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Woher ist Lena umgezogen?",
                    "options": ["Aus Berlin", "Aus München", "Aus Köln", "Aus Wien"],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie viele Zimmer hat Lenas neue Wohnung?",
                    "options": ["Zwei", "Drei", "Vier", "Fünf"],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was findet Lena an der Wohnung nicht ideal?",
                    "options": [
                        "Die Lage",
                        "Die Größe",
                        "Den Preis",
                        "Den Aufzug",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie weit ist es zum Bahnhof?",
                    "options": [
                        "Fünf Minuten zu Fuß",
                        "Zehn Minuten zu Fuß",
                        "Zwanzig Minuten zu Fuß",
                        "Eine halbe Stunde mit dem Bus",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was wird Lena am Montag machen?",
                    "options": [
                        "Sie besucht Anna.",
                        "Sie zieht um.",
                        "Sie beginnt eine neue Arbeit.",
                        "Sie sucht eine Wohnung.",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
            ],
        },
        {
            "part_number": 3,
            "instruction": (
                "Welches Wort passt? Wähle das richtige Wort für jeden Satz "
                "aus dem Wortbank: am, um, im, auf, in, nach, mit, zum."
            ),
            "max_points": 10,
            "texts": [
                {
                    "title": "Wortbank",
                    "text": "am · um · im · auf · in · nach · mit · zum",
                }
            ],
            "questions": [
                {
                    "question": "Ich stehe ___ sieben Uhr auf.",
                    "options": ["am", "um", "im", "auf"],
                    "correct_index": 1,
                    "question_type": "gap_fill",
                },
                {
                    "question": "Er fährt ___ Fahrrad zur Arbeit.",
                    "options": ["mit", "auf", "in", "nach"],
                    "correct_index": 0,
                    "question_type": "gap_fill",
                },
                {
                    "question": "Wir gehen ___ Kino.",
                    "options": ["am", "im", "ins", "zum"],
                    "correct_index": 3,
                    "question_type": "gap_fill",
                },
                {
                    "question": "Das Buch liegt ___ dem Tisch.",
                    "options": ["in", "auf", "mit", "nach"],
                    "correct_index": 1,
                    "question_type": "gap_fill",
                },
                {
                    "question": "Im Sommer fliegen wir ___ Italien.",
                    "options": ["nach", "in", "zum", "am"],
                    "correct_index": 0,
                    "question_type": "gap_fill",
                },
            ],
        },
    ],
}


# =====================================================================
# A1 — Hören
# =====================================================================
A1_HOEREN = {
    "level": "A1",
    "section": "Hören",
    "time_limit_minutes": 30,
    "max_score": 45,
    "instructions": (
        "Du hörst kurze Dialoge und Ansagen. Wähle für jede Frage die "
        "richtige Antwort."
    ),
    "parts": [
        {
            "part_number": 1,
            "instruction": (
                "Du hörst fünf kurze Gespräche. Wähle für jedes Gespräch die "
                "richtige Antwort."
            ),
            "max_points": 25,
            "scripts": [
                {
                    "title": "Dialog 1 — Verabredung",
                    "speaker_context": "Zwei Freunde verabreden sich am Telefon.",
                    "script": (
                        "Mark: Hallo Lisa, sollen wir uns heute treffen?\n"
                        "Lisa: Gerne! Wo und wann?\n"
                        "Mark: Wie wäre es am Bahnhof um halb drei?\n"
                        "Lisa: Halb drei am Bahnhof, das passt mir gut. "
                        "Bis später!"
                    ),
                },
                {
                    "title": "Dialog 2 — Im Supermarkt",
                    "speaker_context": "Eine Kundin fragt im Supermarkt nach Mehl.",
                    "script": (
                        "Kundin: Entschuldigung, wo finde ich das Mehl?\n"
                        "Mitarbeiter: Das Mehl ist im Gang vier, "
                        "ganz hinten beim Zucker.\n"
                        "Kundin: Vielen Dank!\n"
                        "Mitarbeiter: Gerne."
                    ),
                },
                {
                    "title": "Dialog 3 — Beim Zahnarzt",
                    "speaker_context": "Ein Mann ruft die Zahnarztpraxis an.",
                    "script": (
                        "Mann: Guten Tag, hier ist Herr Schmidt. Ich habe "
                        "morgen einen Termin um zehn Uhr, aber ich muss "
                        "leider absagen. Ich bin krank.\n"
                        "Sprechstundenhilfe: Kein Problem, Herr Schmidt. "
                        "Möchten Sie einen neuen Termin?\n"
                        "Mann: Ja, bitte nächste Woche."
                    ),
                },
                {
                    "title": "Dialog 4 — Samstagabend",
                    "speaker_context": "Ein Paar plant den Samstagabend.",
                    "script": (
                        "Frau: Was machen wir am Samstagabend? Kino oder Restaurant?\n"
                        "Mann: Ich habe keinen Hunger. Lass uns lieber ins Kino gehen.\n"
                        "Frau: Gut, dann gehen wir ins Kino. Welcher Film?\n"
                        "Mann: Der neue Film mit Tom Hanks."
                    ),
                },
                {
                    "title": "Dialog 5 — Auf der Straße",
                    "speaker_context": "Ein Tourist fragt nach dem Weg.",
                    "script": (
                        "Tourist: Entschuldigung, wie komme ich zum Hauptbahnhof?\n"
                        "Passant: Gehen Sie immer geradeaus, dann an der "
                        "Ampel links. Nach hundert Metern sehen Sie den Bahnhof "
                        "auf der rechten Seite.\n"
                        "Tourist: Vielen Dank!"
                    ),
                },
            ],
            "questions": [
                {
                    "question": "Wo und wann treffen sich Mark und Lisa?",
                    "options": [
                        "Im Café um drei Uhr",
                        "Am Bahnhof um halb drei",
                        "Am Bahnhof um drei Uhr",
                        "Im Park um halb zwei",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wo ist das Mehl im Supermarkt?",
                    "options": [
                        "Gang zwei, beim Brot",
                        "Gang vier, beim Zucker",
                        "Gang sechs, beim Mehl",
                        "Im Lager",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Warum ruft Herr Schmidt an?",
                    "options": [
                        "Er möchte einen Termin machen.",
                        "Er muss seinen Termin absagen.",
                        "Er möchte Schmerzmittel bestellen.",
                        "Er fragt nach den Öffnungszeiten.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Was machen die beiden am Samstagabend?",
                    "options": [
                        "Sie gehen ins Restaurant.",
                        "Sie bleiben zu Hause.",
                        "Sie gehen ins Kino.",
                        "Sie gehen tanzen.",
                    ],
                    "correct_index": 2,
                },
                {
                    "question": "Wie kommt der Tourist zum Hauptbahnhof?",
                    "options": [
                        "Immer geradeaus, dann rechts",
                        "Erst links, dann geradeaus",
                        "Geradeaus und an der Ampel links",
                        "Mit dem Bus Linie 5",
                    ],
                    "correct_index": 2,
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": (
                "Du hörst eine Radioansage über ein neues Schwimmbad. "
                "Beantworte die Fragen."
            ),
            "max_points": 20,
            "scripts": [
                {
                    "title": "Radio-Ansage — Neues Schwimmbad",
                    "speaker_context": "Eine freundliche Radiomoderatorin liest "
                    "die Ansage langsam und deutlich vor.",
                    "script": (
                        "Liebe Hörerinnen und Hörer, gute Nachrichten für alle "
                        "Wasserratten! Am kommenden Samstag, dem 12. April, "
                        "öffnet das neue Schwimmbad 'Aquapark Süd' in "
                        "Frankfurt. Das Schwimmbad hat ein großes "
                        "Sportbecken, ein Kinderbecken und eine Sauna. "
                        "Die Öffnungszeiten sind von Montag bis Freitag "
                        "von sechs Uhr morgens bis zweiundzwanzig Uhr abends. "
                        "Am Wochenende öffnen wir um acht Uhr. "
                        "Der Eintritt für Erwachsene kostet sechs Euro, "
                        "für Kinder unter zwölf Jahren nur drei Euro. "
                        "Das Schwimmbad liegt in der Hauptstraße zwölf, "
                        "direkt neben dem Stadtpark. Mit der U-Bahn-Linie U2 "
                        "erreichen Sie uns in zehn Minuten vom Hauptbahnhof. "
                        "Wir freuen uns auf Ihren Besuch!"
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wann öffnet das neue Schwimmbad?",
                    "options": [
                        "Am 12. März",
                        "Am 12. April",
                        "Am 22. April",
                        "Am 6. Mai",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wann hat das Schwimmbad am Wochenende geöffnet?",
                    "options": [
                        "Ab 6 Uhr",
                        "Ab 8 Uhr",
                        "Ab 10 Uhr",
                        "Ab 12 Uhr",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie viel kostet der Eintritt für ein 10-jähriges Kind?",
                    "options": ["3 Euro", "6 Euro", "12 Euro", "Frei"],
                    "correct_index": 0,
                },
                {
                    "question": "Wo liegt das Schwimmbad?",
                    "options": [
                        "Am Hauptbahnhof",
                        "In der Hauptstraße 12",
                        "Im Stadtpark",
                        "Am Aquapark Nord",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    ],
}


# =====================================================================
# A1 — Schreiben
# =====================================================================
A1_SCHREIBEN = {
    "level": "A1",
    "section": "Schreiben",
    "time_limit_minutes": 60,
    "max_score": 30,
    "instructions": "Schreibe die zwei Aufgaben.",
    "parts": [
        {
            "task_number": 1,
            "instruction": (
                "Du füllst für deinen Freund Thomas Müller ein "
                "Hotel-Anmeldeformular aus."
            ),
            "prompt": (
                "Thomas Müller wohnt in Wien, Mariahilfer Straße 88, 1060. "
                "Er ist am 14. März 1990 geboren, ist Lehrer und kommt mit "
                "seiner Frau für drei Nächte ins Hotel Berlin. Er möchte ein "
                "Doppelzimmer mit Frühstück. Seine Telefonnummer ist "
                "+43 660 123 4567. Schreibe alle Informationen in das Formular."
            ),
            "min_words": 15,
            "max_words": 40,
            "format_hint": (
                "Felder: Name | Adresse | Geburtsdatum | Beruf | Zimmertyp | "
                "Anzahl Nächte | Telefon | Frühstück (ja/nein)"
            ),
            "model_answer": (
                "Name: Thomas Müller\n"
                "Adresse: Mariahilfer Straße 88, 1060 Wien\n"
                "Geburtsdatum: 14.03.1990\n"
                "Beruf: Lehrer\n"
                "Zimmertyp: Doppelzimmer\n"
                "Anzahl Nächte: 3\n"
                "Telefon: +43 660 123 4567\n"
                "Frühstück: ja"
            ),
            "max_points": 10,
        },
        {
            "task_number": 2,
            "instruction": (
                "Schreibe eine kurze Nachricht an deine Freundin Anna. "
                "Erzähle ihr von deinem neuen Job in Berlin und lade sie ein."
            ),
            "prompt": (
                "Du fängst nächsten Montag eine neue Arbeit in Berlin an. "
                "Schreibe an Anna:\n"
                "• Was für eine Arbeit du machst\n"
                "• Wann du anfängst\n"
                "• Lade Anna ein, dich zu besuchen"
            ),
            "min_words": 40,
            "max_words": 50,
            "format_hint": "Anrede, Hauptteil mit allen Punkten, Gruß",
            "model_answer": (
                "Liebe Anna,\n\n"
                "ich habe tolle Nachrichten! Ich beginne nächsten Montag eine "
                "neue Arbeit als Programmiererin in Berlin. Die Firma ist sehr "
                "modern und das Büro liegt im Zentrum. Ich freue mich sehr! "
                "Möchtest du mich bald besuchen? Berlin ist eine tolle Stadt.\n\n"
                "Liebe Grüße,\nDein/e Freund/in"
            ),
            "max_points": 20,
        },
    ],
}


# =====================================================================
# A1 — Sprechen
# =====================================================================
A1_SPRECHEN = {
    "level": "A1",
    "section": "Sprechen",
    "time_limit_minutes": 15,
    "max_score": 30,
    "instructions": (
        "Drei kurze Sprechaufgaben: Sich vorstellen, ein Bild beschreiben, "
        "und ein Rollenspiel."
    ),
    "parts": [
        {
            "card_number": 1,
            "task_type": "Sich vorstellen",
            "prompt": (
                "Stell dich vor. Sprich über deinen Namen, woher du kommst, "
                "deinen Beruf, wo du wohnst und welche Sprachen du sprichst."
            ),
            "supporting_questions": [
                "Wie heißt du?",
                "Woher kommst du?",
                "Was bist du von Beruf?",
                "Wo wohnst du?",
                "Welche Sprachen sprichst du?",
            ],
            "time_allowed_seconds": 90,
        },
        {
            "card_number": 2,
            "task_type": "Bild beschreiben",
            "prompt": (
                "Beschreibe ein Bild: Eine Familie sitzt zusammen am "
                "Esstisch und isst Abendbrot. Was siehst du? "
                "Wer ist auf dem Bild? Was machen die Personen?"
            ),
            "supporting_questions": [
                "Wie viele Personen siehst du?",
                "Was essen sie?",
                "Wo sind sie?",
                "Wie sehen die Personen aus?",
            ],
            "time_allowed_seconds": 90,
        },
        {
            "card_number": 3,
            "task_type": "Rollenspiel",
            "prompt": (
                "Du bist am Bahnhof und möchtest eine Fahrkarte nach München "
                "kaufen. Sprich mit dem Verkäufer: Frage nach der Fahrkarte, "
                "sag ob du einfach oder hin und zurück möchtest, wann du "
                "fahren willst, und in welcher Klasse."
            ),
            "supporting_questions": [
                "Einfach oder hin und zurück?",
                "Wann möchtest du fahren?",
                "Erste oder zweite Klasse?",
                "Was kostet die Fahrkarte?",
            ],
            "time_allowed_seconds": 120,
        },
    ],
}


# =====================================================================
# A2 — Lesen
# =====================================================================
A2_LESEN = {
    "level": "A2",
    "section": "Lesen",
    "time_limit_minutes": 50,
    "max_score": 45,
    "instructions": "Lies die Texte und beantworte die Fragen.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Lies den Zeitungsartikel und beantworte die Fragen.",
            "max_points": 25,
            "texts": [
                {
                    "title": "Neue Straßenbahnlinie in Leipzig",
                    "text": (
                        "Leipzig bekommt eine neue Straßenbahnlinie. Ab dem "
                        "1. Juni fährt die Linie 17 zwischen dem Hauptbahnhof "
                        "und dem Stadtteil Grünau. Die Fahrt dauert nur "
                        "zwanzig Minuten, mit dem Auto braucht man oft "
                        "vierzig Minuten oder mehr.\n\n"
                        "Die neue Linie hat zwölf Haltestellen. An jeder "
                        "Haltestelle gibt es ein Dach, Sitzbänke und eine "
                        "elektronische Anzeige mit den Abfahrtszeiten. Die "
                        "Bahnen fahren montags bis freitags alle zehn "
                        "Minuten, am Wochenende alle fünfzehn Minuten.\n\n"
                        "Die Stadt hat 80 Millionen Euro in das Projekt "
                        "investiert. Bürgermeister Klaus Werner sagte: "
                        "'Mit dieser neuen Linie machen wir das Leben in "
                        "Leipzig grüner und einfacher. Wir hoffen, dass "
                        "viele Menschen das Auto stehen lassen.' Eine "
                        "Einzelfahrkarte kostet 2,80 Euro, mit der "
                        "Monatskarte fährt man unbegrenzt für 65 Euro."
                    ),
                    "source_note": "Leipziger Volkszeitung, fiktiv",
                }
            ],
            "questions": [
                {
                    "question": "Wann beginnt die neue Linie 17 zu fahren?",
                    "options": ["Am 1. Mai", "Am 1. Juni", "Am 1. Juli", "Am 17. Juni"],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie lange dauert die Fahrt mit der Straßenbahn?",
                    "options": [
                        "10 Minuten",
                        "20 Minuten",
                        "30 Minuten",
                        "40 Minuten",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie oft fahren die Bahnen am Wochenende?",
                    "options": [
                        "Alle 5 Minuten",
                        "Alle 10 Minuten",
                        "Alle 15 Minuten",
                        "Alle 20 Minuten",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was hofft der Bürgermeister?",
                    "options": [
                        "Dass die Fahrkarten billiger werden.",
                        "Dass mehr Menschen das Auto stehen lassen.",
                        "Dass mehr Touristen kommen.",
                        "Dass es mehr Haltestellen gibt.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie viel kostet eine Einzelfahrkarte?",
                    "options": ["2,80 €", "6,50 €", "65 €", "80 €"],
                    "correct_index": 0,
                    "question_type": "multiple_choice",
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Lies die fünf Kurzanzeigen und entscheide jeweils, ob die Aussage richtig oder falsch ist.",
            "max_points": 20,
            "texts": [
                {
                    "title": "Kurzanzeigen",
                    "text": (
                        "A) Yoga-Kurs für Anfänger im Sportzentrum Mitte. "
                        "Jeden Dienstag und Donnerstag von 19 bis 20:30 Uhr. "
                        "Erste Stunde gratis.\n\n"
                        "B) Verkaufe Ledersofa, drei Sitze, fast neu, "
                        "200 Euro. Selbstabholung in Stuttgart-West.\n\n"
                        "C) Suche Mitfahrer von Köln nach Berlin am Freitag, "
                        "16 Uhr. Kosten 25 Euro pro Person.\n\n"
                        "D) Restaurant 'Bella Italia' sucht Kellner für "
                        "Wochenenden. Erfahrung erwünscht. Bewerbung per "
                        "E-Mail an info@bella.de.\n\n"
                        "E) Sprachcafé Deutsch–Spanisch jeden Samstag um "
                        "15 Uhr im Café Lichtblick. Kostenlos, bitte vorher "
                        "anmelden."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Der Yoga-Kurs (A) findet einmal pro Woche statt.",
                    "options": ["Richtig", "Falsch"],
                    "correct_index": 1,
                    "question_type": "true_false",
                },
                {
                    "question": "Das Sofa (B) ist gebraucht, aber in gutem Zustand.",
                    "options": ["Richtig", "Falsch"],
                    "correct_index": 0,
                    "question_type": "true_false",
                },
                {
                    "question": "Die Mitfahrt (C) ist kostenlos.",
                    "options": ["Richtig", "Falsch"],
                    "correct_index": 1,
                    "question_type": "true_false",
                },
                {
                    "question": "Das Restaurant (D) sucht Köche.",
                    "options": ["Richtig", "Falsch"],
                    "correct_index": 1,
                    "question_type": "true_false",
                },
            ],
        },
    ],
}


# =====================================================================
# A2 — Hören
# =====================================================================
A2_HOEREN = {
    "level": "A2",
    "section": "Hören",
    "time_limit_minutes": 30,
    "max_score": 45,
    "instructions": "Du hörst Dialoge und Ansagen. Wähle die richtige Antwort.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Du hörst vier kurze Dialoge.",
            "max_points": 25,
            "scripts": [
                {
                    "title": "Dialog 1 — Im Reisebüro",
                    "speaker_context": "Eine Kundin im Reisebüro plant einen Urlaub.",
                    "script": (
                        "Kundin: Guten Tag, ich möchte einen Urlaub für "
                        "August buchen, eine Woche am Meer.\n"
                        "Mitarbeiter: Wir haben ein gutes Angebot für Mallorca: "
                        "Hotel mit Halbpension, Flug inklusive, 750 Euro pro Person.\n"
                        "Kundin: Das klingt gut. Aber gibt es auch etwas mit Vollpension?\n"
                        "Mitarbeiter: Ja, mit Vollpension kostet es 890 Euro pro Person."
                    ),
                },
                {
                    "title": "Dialog 2 — Beim Arzt",
                    "speaker_context": "Ein Patient beim Hausarzt.",
                    "script": (
                        "Arzt: Guten Tag, was kann ich für Sie tun?\n"
                        "Patient: Seit drei Tagen habe ich starke Kopfschmerzen "
                        "und ich kann nicht gut schlafen.\n"
                        "Arzt: Haben Sie Fieber?\n"
                        "Patient: Nein, kein Fieber.\n"
                        "Arzt: Ich verschreibe Ihnen Tabletten. Nehmen Sie "
                        "morgens und abends eine. Trinken Sie viel Wasser "
                        "und ruhen Sie sich aus."
                    ),
                },
                {
                    "title": "Dialog 3 — Am Telefon",
                    "speaker_context": "Eine Frau ruft im Büro ihres Mannes an.",
                    "script": (
                        "Sekretärin: Firma Schneider, guten Tag.\n"
                        "Frau: Guten Tag, hier spricht Eva Bauer. Ist mein Mann da?\n"
                        "Sekretärin: Herr Bauer ist gerade in einer Besprechung. "
                        "Kann ich etwas ausrichten?\n"
                        "Frau: Ja bitte. Sagen Sie ihm, dass das Abendessen "
                        "heute um halb sieben ist, nicht um sieben."
                    ),
                },
                {
                    "title": "Dialog 4 — Im Hotel",
                    "speaker_context": "Ein Gast checkt im Hotel ein.",
                    "script": (
                        "Gast: Guten Abend, ich habe ein Zimmer reserviert. "
                        "Mein Name ist Klein.\n"
                        "Rezeption: Willkommen, Herr Klein. Sie haben ein "
                        "Doppelzimmer für drei Nächte, richtig?\n"
                        "Gast: Ja, genau. Wann gibt es Frühstück?\n"
                        "Rezeption: Das Frühstück gibt es von sieben bis "
                        "zehn Uhr im Restaurant im Erdgeschoss."
                    ),
                },
            ],
            "questions": [
                {
                    "question": "Wie viel kostet das Mallorca-Angebot mit Halbpension pro Person?",
                    "options": ["650 €", "750 €", "890 €", "1000 €"],
                    "correct_index": 1,
                },
                {
                    "question": "Wie lange hat der Patient schon Kopfschmerzen?",
                    "options": ["Einen Tag", "Zwei Tage", "Drei Tage", "Eine Woche"],
                    "correct_index": 2,
                },
                {
                    "question": "Was soll die Sekretärin Herrn Bauer ausrichten?",
                    "options": [
                        "Das Abendessen ist um sieben Uhr.",
                        "Das Abendessen ist um halb sieben.",
                        "Das Abendessen fällt aus.",
                        "Er soll seine Frau anrufen.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wann gibt es Frühstück im Hotel?",
                    "options": [
                        "Von 6 bis 9 Uhr",
                        "Von 7 bis 10 Uhr",
                        "Von 8 bis 11 Uhr",
                        "Den ganzen Tag",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wo ist das Hotelrestaurant?",
                    "options": [
                        "Im Erdgeschoss",
                        "Im ersten Stock",
                        "Im Keller",
                        "Im dritten Stock",
                    ],
                    "correct_index": 0,
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Du hörst eine Bahnhofsdurchsage.",
            "max_points": 20,
            "scripts": [
                {
                    "title": "Bahnhofsdurchsage",
                    "speaker_context": "Eine Lautsprecherdurchsage am Bahnhof Frankfurt.",
                    "script": (
                        "Achtung an Gleis sieben. Der ICE fünfundzwanzig "
                        "nach Hamburg über Hannover fährt heute mit etwa "
                        "fünfzehn Minuten Verspätung ein. Voraussichtliche "
                        "Abfahrt vierzehn Uhr fünfunddreißig statt vierzehn "
                        "Uhr zwanzig. Wir bitten um Ihr Verständnis. "
                        "Reisende nach Bremen steigen bitte in Hannover um. "
                        "Der Anschlusszug nach Bremen wartet am Gleis drei. "
                        "Die Bordrestaurant ist heute geöffnet. Wir wünschen "
                        "Ihnen eine gute Reise."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Welcher Zug hat Verspätung?",
                    "options": [
                        "Der IC nach Bremen",
                        "Der ICE 25 nach Hamburg",
                        "Der RE nach Frankfurt",
                        "Der ICE 7 nach Berlin",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie viel Verspätung hat der Zug?",
                    "options": [
                        "5 Minuten",
                        "15 Minuten",
                        "25 Minuten",
                        "35 Minuten",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wo müssen Reisende nach Bremen umsteigen?",
                    "options": [
                        "In Frankfurt",
                        "In Hamburg",
                        "In Hannover",
                        "Sie müssen nicht umsteigen.",
                    ],
                    "correct_index": 2,
                },
                {
                    "question": "Auf welchem Gleis fährt der Zug nach Bremen?",
                    "options": ["Gleis 3", "Gleis 5", "Gleis 7", "Gleis 25"],
                    "correct_index": 0,
                },
            ],
        },
    ],
}


# =====================================================================
# A2 — Schreiben
# =====================================================================
A2_SCHREIBEN = {
    "level": "A2",
    "section": "Schreiben",
    "time_limit_minutes": 30,
    "max_score": 30,
    "instructions": "Schreibe zwei kurze Texte.",
    "parts": [
        {
            "task_number": 1,
            "instruction": (
                "Schreibe eine formelle E-Mail. Du wurdest zu einer "
                "Geburtstagsfeier eingeladen, kannst aber nicht kommen."
            ),
            "prompt": (
                "Eine Kollegin, Frau Schmidt, hat dich zu ihrer Geburtstagsfeier "
                "am Samstag eingeladen. Du kannst leider nicht kommen, weil deine "
                "Eltern dich besuchen. Schreibe eine höfliche E-Mail:\n"
                "• Bedanke dich für die Einladung\n"
                "• Erkläre, warum du nicht kommen kannst\n"
                "• Wünsche ihr alles Gute zum Geburtstag\n"
                "• Schlage einen anderen Termin vor"
            ),
            "min_words": 50,
            "max_words": 70,
            "format_hint": "Formelle Anrede (Sehr geehrte ...), Hauptteil, formelle Schlussformel (Mit freundlichen Grüßen)",
            "model_answer": (
                "Sehr geehrte Frau Schmidt,\n\n"
                "vielen Dank für Ihre nette Einladung zu Ihrer Geburtstagsfeier "
                "am Samstag. Leider kann ich nicht kommen, weil meine Eltern "
                "an diesem Wochenende zu Besuch sind. Das tut mir wirklich leid.\n\n"
                "Ich wünsche Ihnen schon jetzt alles Gute zum Geburtstag und "
                "viel Freude mit Ihren Gästen. Vielleicht können wir uns "
                "nächste Woche zum Mittagessen treffen?\n\n"
                "Mit freundlichen Grüßen,\n"
                "Anna Müller"
            ),
            "max_points": 15,
        },
        {
            "task_number": 2,
            "instruction": (
                "Schreibe eine kurze Nachricht in einem Online-Forum über "
                "deine Lieblingsstadt."
            ),
            "prompt": (
                "Im Forum 'Reisetipps' fragt jemand nach einer schönen Stadt für "
                "ein Wochenende. Antworte und schreibe über deine Lieblingsstadt:\n"
                "• Wo ist die Stadt?\n"
                "• Was kann man dort machen?\n"
                "• Was solltest du auf jeden Fall sehen?\n"
                "• Wann ist die beste Reisezeit?"
            ),
            "min_words": 60,
            "max_words": 80,
            "format_hint": "Informeller Stil, klare Struktur, Anrede an die Forum-Community",
            "model_answer": (
                "Hallo zusammen,\n\n"
                "ich kann München sehr empfehlen! Die Stadt liegt im Süden "
                "Deutschlands und ist perfekt für ein Wochenende. Man kann "
                "im Englischen Garten spazieren gehen, das Deutsche Museum "
                "besuchen oder ein Bier im berühmten Hofbräuhaus trinken. "
                "Auf jeden Fall solltest du den Marienplatz und das "
                "Schloss Nymphenburg sehen. Die beste Reisezeit ist Mai "
                "bis September, weil das Wetter dann meistens schön ist.\n\n"
                "Viel Spaß!"
            ),
            "max_points": 15,
        },
    ],
}


# =====================================================================
# A2 — Sprechen
# =====================================================================
A2_SPRECHEN = {
    "level": "A2",
    "section": "Sprechen",
    "time_limit_minutes": 15,
    "max_score": 30,
    "instructions": "Drei Aufgaben: Fragen stellen, Bild beschreiben, gemeinsam planen.",
    "parts": [
        {
            "card_number": 1,
            "task_type": "Fragen zu einem Thema",
            "prompt": (
                "Thema: 'Sport'. Stelle vier Fragen an dein Gegenüber zum "
                "Thema Sport (z. B. welche Sportart, wie oft, mit wem) und "
                "antworte selbst auf diese Fragen."
            ),
            "supporting_questions": [
                "Welche Sportart machst du gerne?",
                "Wie oft pro Woche treibst du Sport?",
                "Mit wem machst du Sport?",
                "Warum ist Sport für dich wichtig?",
            ],
            "time_allowed_seconds": 120,
        },
        {
            "card_number": 2,
            "task_type": "Über sich erzählen",
            "prompt": (
                "Erzähle über deinen letzten Urlaub: Wohin bist du gefahren? "
                "Mit wem? Wie lange? Was hast du dort gemacht? Was hat dir "
                "besonders gut gefallen?"
            ),
            "supporting_questions": [
                "Wohin bist du gefahren?",
                "Wie lange warst du dort?",
                "Was hast du gemacht?",
                "Was war dein Lieblingsmoment?",
            ],
            "time_allowed_seconds": 120,
        },
        {
            "card_number": 3,
            "task_type": "Etwas planen",
            "prompt": (
                "Du und ein Freund möchten am Samstag etwas zusammen "
                "unternehmen. Sprich mit ihm/ihr und einigt euch: "
                "Was wollt ihr machen? Wo trefft ihr euch? Um wie viel Uhr? "
                "Wer bringt was mit?"
            ),
            "supporting_questions": [
                "Was möchten wir machen?",
                "Wo treffen wir uns?",
                "Wann treffen wir uns?",
                "Wer organisiert was?",
            ],
            "time_allowed_seconds": 150,
        },
    ],
}


# =====================================================================
# B1 — Lesen
# =====================================================================
B1_LESEN = {
    "level": "B1",
    "section": "Lesen",
    "time_limit_minutes": 65,
    "max_score": 60,
    "instructions": "Lies die drei Texte und beantworte die Fragen.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Zeitungsartikel — beantworte die Fragen.",
            "max_points": 20,
            "texts": [
                {
                    "title": "Mehr junge Menschen lernen Handwerksberufe",
                    "text": (
                        "Berlin — Eine neue Studie der Handwerkskammer zeigt, dass in "
                        "Deutschland wieder mehr junge Menschen einen Handwerksberuf "
                        "lernen wollen. Im letzten Jahr haben rund 145.000 junge "
                        "Frauen und Männer eine Ausbildung im Handwerk begonnen, das "
                        "sind acht Prozent mehr als im Vorjahr.\n\n"
                        "Die beliebtesten Berufe sind Elektroniker, "
                        "Kraftfahrzeugmechatroniker und Bäcker. Besonders bei jungen "
                        "Frauen wird der Beruf der Tischlerin immer beliebter. "
                        "Experten erklären den Trend mit der Wirtschaftslage: "
                        "Während Akademiker in vielen Branchen mit harter Konkurrenz "
                        "rechnen müssen, finden Handwerker nach der Ausbildung "
                        "schnell eine gut bezahlte Stelle.\n\n"
                        "Der Präsident der Handwerkskammer, Hans Peter König, sagte: "
                        "'Das Handwerk ist modern und vielseitig. Wer heute eine "
                        "Ausbildung beginnt, kann morgen einen eigenen Betrieb "
                        "leiten.' Die Kammer rechnet damit, dass in den nächsten "
                        "fünf Jahren rund 200.000 Handwerksbetriebe neue Inhaber "
                        "suchen werden, weil viele Meister in den Ruhestand gehen."
                    ),
                    "source_note": "Frei nach deutschen Wirtschaftsnachrichten",
                }
            ],
            "questions": [
                {
                    "question": "Wie viel Prozent mehr junge Menschen haben eine Handwerksausbildung begonnen?",
                    "options": ["3 %", "5 %", "8 %", "12 %"],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Welchen Beruf wählen besonders viele junge Frauen jetzt?",
                    "options": [
                        "Elektronikerin",
                        "Bäckerin",
                        "Tischlerin",
                        "Kraftfahrzeugmechatronikerin",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Warum wählen Jugendliche laut Experten das Handwerk?",
                    "options": [
                        "Weil das Studium zu teuer ist.",
                        "Weil Handwerker schnell eine gut bezahlte Stelle finden.",
                        "Weil ihre Eltern es wünschen.",
                        "Weil es weniger Stress ist.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was passiert in den nächsten fünf Jahren laut der Kammer?",
                    "options": [
                        "Viele Betriebe schließen.",
                        "Viele Meister gehen in Rente und suchen Nachfolger.",
                        "Die Löhne steigen stark.",
                        "Es gibt weniger Ausbildungsplätze.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Interview — beantworte die Fragen.",
            "max_points": 20,
            "texts": [
                {
                    "title": "Interview mit der Klimaforscherin Dr. Marlene Hofer",
                    "text": (
                        "Frage: Frau Dr. Hofer, was ist heute die größte Herausforderung "
                        "für Klimaforscher?\n"
                        "Antwort: Die größte Herausforderung ist nicht, das Problem zu "
                        "verstehen — das Problem kennen wir gut. Die Herausforderung ist, "
                        "die Politik und die Bürger davon zu überzeugen, schnell zu "
                        "handeln. Wir reden seit Jahrzehnten über den Klimawandel, aber "
                        "die wirklichen Veränderungen kommen sehr langsam.\n\n"
                        "Frage: Was kann jeder Einzelne tun?\n"
                        "Antwort: Sehr viel. Weniger Fleisch essen, öfter mit dem Fahrrad "
                        "oder dem Zug fahren, weniger fliegen und Strom sparen. Diese "
                        "kleinen Schritte sind wichtig, aber sie ersetzen keine politische "
                        "Lösung. Wir brauchen beides: persönliches Handeln und gute Gesetze.\n\n"
                        "Frage: Sind Sie optimistisch?\n"
                        "Antwort: Ich bin vorsichtig optimistisch. Die jungen Menschen heute "
                        "verstehen das Problem viel besser als meine Generation. Wenn die "
                        "Politik jetzt mutig handelt, können wir noch viel erreichen. "
                        "Aber wir haben keine Zeit mehr für lange Diskussionen."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Was ist laut Dr. Hofer die größte Herausforderung?",
                    "options": [
                        "Das Klimaproblem zu verstehen.",
                        "Politik und Bürger zum schnellen Handeln zu bewegen.",
                        "Genug Forschungsgelder zu bekommen.",
                        "Junge Menschen zu erreichen.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was empfiehlt sie für den Alltag?",
                    "options": [
                        "Komplett auf Auto verzichten.",
                        "Nur noch mit dem Zug reisen.",
                        "Weniger Fleisch, weniger fliegen, Strom sparen.",
                        "Nichts — nur Politik kann helfen.",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie ist ihre Haltung insgesamt?",
                    "options": [
                        "Sehr pessimistisch",
                        "Vorsichtig optimistisch",
                        "Gleichgültig",
                        "Wütend",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was sagt sie über junge Menschen?",
                    "options": [
                        "Sie sind nicht interessiert.",
                        "Sie verstehen das Problem besser als ihre Generation.",
                        "Sie protestieren zu viel.",
                        "Sie sollten mehr lernen.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
            ],
        },
        {
            "part_number": 3,
            "instruction": "Meinungsartikel — beantworte die Fragen.",
            "max_points": 20,
            "texts": [
                {
                    "title": "Homeoffice für immer? Eine Bilanz nach drei Jahren",
                    "text": (
                        "Drei Jahre nach dem großen Homeoffice-Experiment ist es Zeit, "
                        "Bilanz zu ziehen. Viele Unternehmen feiern das Modell als "
                        "Erfolg: Die Mitarbeiter sparen Pendelzeit, sind flexibler und "
                        "oft produktiver. Studien zeigen, dass die meisten Beschäftigten "
                        "lieber zu Hause arbeiten würden, zumindest an einigen Tagen "
                        "der Woche.\n\n"
                        "Doch das Homeoffice hat auch Schattenseiten. Wer den ganzen "
                        "Tag allein im Wohnzimmer sitzt, fühlt sich oft isoliert. "
                        "Die Grenze zwischen Arbeit und Freizeit verschwimmt, und "
                        "manche arbeiten am Ende mehr als im Büro. Junge Mitarbeiter "
                        "klagen, dass sie ohne den persönlichen Kontakt zu Kolleginnen "
                        "und Kollegen weniger lernen.\n\n"
                        "Die meisten Experten sind sich heute einig: Eine Mischung aus "
                        "Büro und Homeoffice ist der beste Weg. Drei Tage zu Hause, "
                        "zwei Tage im Büro — so können Mitarbeiter sowohl die Vorteile "
                        "der Flexibilität genießen als auch den sozialen Kontakt im "
                        "Team behalten. Die Frage ist nur, ob jedes Unternehmen den "
                        "Mut hat, seinen Beschäftigten dieses Vertrauen zu schenken."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Welche Vorteile des Homeoffice nennt der Text?",
                    "options": [
                        "Mehr Geld und mehr Urlaub",
                        "Weniger Pendeln, mehr Flexibilität, oft höhere Produktivität",
                        "Bessere Beziehungen zu Kollegen",
                        "Weniger Arbeit",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was ist ein Nachteil des Homeoffice?",
                    "options": [
                        "Die Technik funktioniert oft nicht.",
                        "Junge Mitarbeiter lernen weniger.",
                        "Die Miete steigt.",
                        "Man muss früher aufstehen.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was empfehlen die meisten Experten?",
                    "options": [
                        "Komplett zurück ins Büro",
                        "Komplett ins Homeoffice",
                        "Eine Mischung aus Büro und Homeoffice",
                        "Vier Tage Büro, ein Tag Homeoffice",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was ist laut Autor die offene Frage?",
                    "options": [
                        "Ob Homeoffice billiger ist.",
                        "Ob Unternehmen ihren Mitarbeitern das nötige Vertrauen schenken.",
                        "Ob der Computer schnell genug ist.",
                        "Ob das Wetter mitspielt.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
            ],
        },
    ],
}


# =====================================================================
# B1 — Hören
# =====================================================================
B1_HOEREN = {
    "level": "B1",
    "section": "Hören",
    "time_limit_minutes": 40,
    "max_score": 60,
    "instructions": "Hörverstehen B1 mit längeren Texten.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Du hörst ein Telefongespräch.",
            "max_points": 20,
            "scripts": [
                {
                    "title": "Telefongespräch — Versicherung",
                    "speaker_context": "Eine Kundin ruft bei ihrer Krankenversicherung an.",
                    "script": (
                        "Mitarbeiter: Krankenversicherung Müller, mein Name ist Becker, "
                        "guten Tag. Wie kann ich Ihnen helfen?\n"
                        "Kundin: Guten Tag, hier spricht Frau Wagner. Ich rufe an, "
                        "weil ich vor zwei Wochen beim Zahnarzt war und jetzt eine "
                        "Rechnung über vierhundertzwanzig Euro bekommen habe.\n"
                        "Mitarbeiter: Verstanden. Wofür war die Behandlung genau?\n"
                        "Kundin: Es war eine professionelle Zahnreinigung und eine "
                        "neue Krone. Ich wollte fragen, wie viel die Versicherung "
                        "bezahlt.\n"
                        "Mitarbeiter: Die Zahnreinigung wird leider nicht erstattet, "
                        "das müssen Sie selbst zahlen, also etwa achtzig Euro. "
                        "Für die Krone übernehmen wir je nach Tarif siebzig bis "
                        "achtzig Prozent. In Ihrem Fall wären das ungefähr zweihundert "
                        "vierzig Euro.\n"
                        "Kundin: Was muss ich tun, damit ich das Geld zurückbekomme?\n"
                        "Mitarbeiter: Schicken Sie uns die Rechnung per Post oder "
                        "über unser Online-Portal. Das Geld ist normalerweise nach "
                        "zehn Werktagen auf Ihrem Konto."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Warum ruft Frau Wagner an?",
                    "options": [
                        "Sie möchte einen Termin vereinbaren.",
                        "Sie hat eine Zahnarztrechnung und fragt nach der Erstattung.",
                        "Sie möchte den Tarif ändern.",
                        "Sie hat Schmerzen.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie viel zahlt die Versicherung für die Zahnreinigung?",
                    "options": [
                        "Alles",
                        "Die Hälfte",
                        "Etwa 80 Euro",
                        "Nichts",
                    ],
                    "correct_index": 3,
                },
                {
                    "question": "Wie viel bekommt sie für die Krone zurück?",
                    "options": [
                        "Etwa 80 Euro",
                        "Etwa 240 Euro",
                        "Etwa 420 Euro",
                        "Gar nichts",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie kann sie die Rechnung einreichen?",
                    "options": [
                        "Nur persönlich vor Ort",
                        "Per Post oder Online-Portal",
                        "Nur per Fax",
                        "Per E-Mail",
                    ],
                    "correct_index": 1,
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Du hörst einen Vortrag.",
            "max_points": 20,
            "scripts": [
                {
                    "title": "Vortrag — Schlafgesundheit",
                    "speaker_context": "Eine Schlafforscherin hält einen Vortrag in der Volkshochschule.",
                    "script": (
                        "Guten Abend, meine Damen und Herren. Heute spreche ich "
                        "über ein Thema, das jeden von uns betrifft: den Schlaf. "
                        "Erwachsene brauchen im Durchschnitt sieben bis acht "
                        "Stunden Schlaf pro Nacht. Das wissen viele, aber nur "
                        "wenige halten sich daran. Studien zeigen, dass etwa "
                        "ein Drittel der Deutschen regelmäßig zu wenig schläft.\n\n"
                        "Die Folgen sind ernst: Schlafmangel macht uns unkonzentriert, "
                        "gereizt und langfristig auch krank. Menschen, die dauerhaft "
                        "weniger als sechs Stunden schlafen, haben ein höheres Risiko "
                        "für Diabetes, Herzkrankheiten und Depressionen.\n\n"
                        "Was können Sie tun? Drei einfache Tipps: Erstens, gehen Sie "
                        "möglichst jeden Tag zur gleichen Zeit ins Bett. Zweitens, "
                        "vermeiden Sie Bildschirme — also Handy, Computer und "
                        "Fernseher — mindestens eine Stunde vor dem Schlafen. "
                        "Drittens, trinken Sie nach achtzehn Uhr keinen Kaffee mehr. "
                        "Diese drei Regeln helfen mehr, als die meisten "
                        "Schlafmedikamente."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wie viele Stunden Schlaf brauchen Erwachsene laut der Vortragenden?",
                    "options": ["5–6 Stunden", "6–7 Stunden", "7–8 Stunden", "9–10 Stunden"],
                    "correct_index": 2,
                },
                {
                    "question": "Wie viele Deutsche schlafen regelmäßig zu wenig?",
                    "options": [
                        "Etwa die Hälfte",
                        "Etwa ein Drittel",
                        "Etwa zwei Drittel",
                        "Fast alle",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Welches Risiko nennt sie NICHT?",
                    "options": [
                        "Diabetes",
                        "Herzkrankheiten",
                        "Krebs",
                        "Depressionen",
                    ],
                    "correct_index": 2,
                },
                {
                    "question": "Welcher Tipp wird gegeben?",
                    "options": [
                        "Vor dem Schlafen viel essen",
                        "Mindestens eine Stunde vor dem Schlafen keine Bildschirme",
                        "Immer Schlafmedikamente nehmen",
                        "Nach dem Aufstehen Kaffee trinken",
                    ],
                    "correct_index": 1,
                },
            ],
        },
        {
            "part_number": 3,
            "instruction": "Du hörst eine Diskussion im Radio.",
            "max_points": 20,
            "scripts": [
                {
                    "title": "Radiodiskussion — Tempolimit auf der Autobahn",
                    "speaker_context": "Zwei Gäste diskutieren im Radio über das Tempolimit.",
                    "script": (
                        "Moderator: Frau Dr. Klein, Sie sind für ein Tempolimit von "
                        "hundertdreißig auf den deutschen Autobahnen. Warum?\n"
                        "Dr. Klein: Aus drei Gründen. Erstens spart ein Tempolimit "
                        "Treibstoff und damit CO2. Zweitens passieren weniger "
                        "schwere Unfälle. Und drittens fließt der Verkehr ruhiger.\n"
                        "Moderator: Herr Schmidt, Sie sind dagegen.\n"
                        "Schmidt: Natürlich. Die deutsche Autobahn ist Teil unserer "
                        "Freiheit. Wer schneller fährt, kommt früher an. Außerdem "
                        "sind die meisten Unfälle nicht auf zu hohem Tempo, sondern "
                        "auf Müdigkeit und Alkohol zurückzuführen.\n"
                        "Dr. Klein: Das stimmt nicht ganz. Die Statistik zeigt klar, "
                        "dass auf Strecken mit Tempolimit deutlich weniger tödliche "
                        "Unfälle passieren.\n"
                        "Schmidt: Aber denken Sie an die Wirtschaft! Schnelle "
                        "Autobahnen sind ein Standortvorteil für Deutschland.\n"
                        "Moderator: Was sagen Sie zur CO2-Frage, Herr Schmidt?\n"
                        "Schmidt: Der Effekt ist sehr klein. Eine echte Klimapolitik "
                        "muss bei der Industrie ansetzen, nicht bei den Autofahrern."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wie viele Argumente nennt Dr. Klein für ein Tempolimit?",
                    "options": ["Eins", "Zwei", "Drei", "Vier"],
                    "correct_index": 2,
                },
                {
                    "question": "Was ist Herrn Schmidts Hauptargument gegen das Tempolimit?",
                    "options": [
                        "Es ist nicht modern.",
                        "Es schränkt die persönliche Freiheit ein und schadet der Wirtschaft.",
                        "Es ist zu teuer.",
                        "Niemand würde sich daran halten.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Was sagt Herr Schmidt über Unfallursachen?",
                    "options": [
                        "Die meisten Unfälle entstehen durch Müdigkeit und Alkohol.",
                        "Die meisten Unfälle entstehen durch zu hohes Tempo.",
                        "Die meisten Unfälle sind nicht zu vermeiden.",
                        "Die Statistik ist gefälscht.",
                    ],
                    "correct_index": 0,
                },
                {
                    "question": "Wie reagiert Dr. Klein auf Schmidts Aussage zu Unfällen?",
                    "options": [
                        "Sie stimmt ihm zu.",
                        "Sie widerspricht und verweist auf Statistiken.",
                        "Sie wechselt das Thema.",
                        "Sie wird wütend.",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    ],
}


# =====================================================================
# B1 — Schreiben
# =====================================================================
B1_SCHREIBEN = {
    "level": "B1",
    "section": "Schreiben",
    "time_limit_minutes": 60,
    "max_score": 100,
    "instructions": "Zwei Schreibaufgaben.",
    "parts": [
        {
            "task_number": 1,
            "instruction": (
                "Schreibe eine formelle E-Mail an deinen Vermieter."
            ),
            "prompt": (
                "Seit einer Woche funktioniert die Heizung in deiner Wohnung nicht. "
                "Schreibe eine formelle E-Mail an deinen Vermieter, Herrn Hoffmann:\n"
                "• Beschreibe das Problem genau\n"
                "• Erkläre, warum es dringend ist\n"
                "• Bitte um eine schnelle Lösung\n"
                "• Schlage einen Termin für eine Reparatur vor"
            ),
            "min_words": 80,
            "max_words": 100,
            "format_hint": "Formell: Sehr geehrter Herr Hoffmann, ... Mit freundlichen Grüßen",
            "model_answer": (
                "Sehr geehrter Herr Hoffmann,\n\n"
                "ich wende mich an Sie mit einem dringenden Problem. Seit einer "
                "Woche funktioniert die Heizung in meiner Wohnung in der "
                "Goethestraße 12 nicht mehr. Auch nach mehreren Versuchen, sie "
                "neu zu starten, bleibt sie kalt.\n\n"
                "Da die Außentemperaturen derzeit unter null Grad liegen, ist "
                "die Situation für mich und meine Familie nicht zumutbar. Wir "
                "müssen abends zusätzliche Pullover tragen und meine Tochter "
                "ist bereits erkältet.\n\n"
                "Ich bitte Sie höflich, so schnell wie möglich einen Handwerker "
                "zu schicken. Ich bin am Donnerstag und Freitag den ganzen Tag "
                "zu Hause und kann den Termin gerne ermöglichen.\n\n"
                "Vielen Dank im Voraus für Ihre Hilfe.\n\n"
                "Mit freundlichen Grüßen,\n"
                "Maria Schneider"
            ),
            "max_points": 50,
        },
        {
            "task_number": 2,
            "instruction": (
                "Schreibe einen Forenbeitrag über ein persönliches Erlebnis."
            ),
            "prompt": (
                "Im Forum 'Mein erster Eindruck' geht es um den ersten Tag in "
                "einem neuen Land. Schreibe über dein eigenes Erlebnis "
                "(oder ein Erlebnis, das du dir vorstellst):\n"
                "• Wann und wohin bist du gereist?\n"
                "• Was war dein erster Eindruck?\n"
                "• Welche Schwierigkeiten hattest du?\n"
                "• Was würdest du anderen empfehlen?"
            ),
            "min_words": 100,
            "max_words": 150,
            "format_hint": "Informeller Stil, persönliche Erzählung mit Details und Gefühlen",
            "model_answer": (
                "Hallo zusammen,\n\n"
                "vor zwei Jahren bin ich für ein Auslandssemester nach Deutschland "
                "gekommen. Mein erster Tag in München werde ich nie vergessen. Als "
                "ich am Hauptbahnhof aus dem Zug stieg, war ich total überfordert. "
                "Alles war auf Deutsch, die Menschen liefen schnell und das Wetter "
                "war kalt und grau.\n\n"
                "Mein erster Eindruck war, dass die Deutschen sehr ernst und "
                "zurückhaltend sind. Aber das hat sich schnell geändert: Schon am "
                "ersten Tag hat mir eine ältere Dame geholfen, den richtigen Bus zu "
                "finden. Schwierig war für mich vor allem die Bürokratie — die "
                "Anmeldung im Rathaus hat fast einen ganzen Vormittag gedauert!\n\n"
                "Mein Tipp: Lernt vor der Reise wenigstens ein paar Sätze Deutsch "
                "und bringt Geduld mit. Deutschland ist am Anfang nicht einfach, "
                "aber nach ein paar Wochen fühlt man sich wirklich willkommen."
            ),
            "max_points": 50,
        },
    ],
}


# =====================================================================
# B1 — Sprechen
# =====================================================================
B1_SPRECHEN = {
    "level": "B1",
    "section": "Sprechen",
    "time_limit_minutes": 15,
    "max_score": 100,
    "instructions": "Drei Teile: Vorstellung, Vortrag aus Karte, Rollenspiel.",
    "parts": [
        {
            "card_number": 1,
            "task_type": "Gemeinsam etwas planen",
            "prompt": (
                "Du und ein Freund/eine Freundin möchten eine Überraschungsparty "
                "für eure beste Freundin Sarah organisieren, die nächste Woche "
                "dreißig Jahre alt wird. Plant gemeinsam: Wo soll die Party sein? "
                "Wen ladet ihr ein? Was soll es zu essen und trinken geben? "
                "Wer organisiert was? Was ist das Geschenk?"
            ),
            "supporting_questions": [
                "Wo machen wir die Party?",
                "Wen laden wir ein?",
                "Wer kümmert sich um Essen und Getränke?",
                "Was schenken wir Sarah?",
            ],
            "time_allowed_seconds": 180,
        },
        {
            "card_number": 2,
            "task_type": "Vortrag aus Karte",
            "prompt": (
                "Halte einen kurzen Vortrag (3-4 Minuten) zum Thema "
                "'Soziale Medien — Fluch oder Segen?'. Strukturiere deinen "
                "Vortrag: Einleitung, deine persönliche Erfahrung, Vor- und "
                "Nachteile, dein Fazit."
            ),
            "supporting_questions": [
                "Welche sozialen Medien benutzt du?",
                "Was sind die Vorteile?",
                "Was sind die Nachteile?",
                "Wie ist deine persönliche Meinung?",
            ],
            "time_allowed_seconds": 240,
        },
        {
            "card_number": 3,
            "task_type": "Rollenspiel — Beschwerde",
            "prompt": (
                "Du hast vor drei Tagen ein Handy online gekauft, aber das "
                "Gerät funktioniert nicht richtig. Der Akku entlädt sich "
                "innerhalb weniger Stunden. Rufe den Kundenservice an und "
                "beschwere dich. Erkläre das Problem genau, frage nach einer "
                "Lösung und sei höflich, aber bestimmt."
            ),
            "supporting_questions": [
                "Was ist genau das Problem?",
                "Wann hast du es bemerkt?",
                "Was möchtest du als Lösung?",
                "Hast du schon etwas versucht?",
            ],
            "time_allowed_seconds": 180,
        },
    ],
}


# =====================================================================
# B2 — Lesen
# =====================================================================
B2_LESEN = {
    "level": "B2",
    "section": "Lesen",
    "time_limit_minutes": 80,
    "max_score": 80,
    "instructions": "Lies die Texte und beantworte die Fragen.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Meinungsartikel zum Thema Bildung.",
            "max_points": 40,
            "texts": [
                {
                    "title": "Die Universität als Geschäftsmodell",
                    "text": (
                        "Vor dreißig Jahren waren die deutschen Universitäten Orte "
                        "der freien Forschung und Bildung. Wer studieren wollte, "
                        "tat dies aus Interesse am Wissen, nicht aus dem Wunsch "
                        "nach einem hohen Gehalt. Heute hat sich diese Sicht "
                        "grundlegend gewandelt. Die Universität ist zu einem "
                        "Dienstleistungsbetrieb geworden, der seine 'Kunden' — also "
                        "die Studierenden — möglichst effizient durch ein "
                        "vorgegebenes Programm schleust.\n\n"
                        "Die Folgen dieser Entwicklung sind weitreichend. "
                        "Studierende denken zunehmend ökonomisch: Welcher Studiengang "
                        "garantiert das höchste Einstiegsgehalt? Welches Praktikum "
                        "macht sich am besten im Lebenslauf? Eine echte "
                        "intellektuelle Auseinandersetzung mit den Inhalten findet "
                        "kaum noch statt. Wer sich für Philosophie oder klassische "
                        "Sprachen interessiert, gilt als naiv oder unrealistisch.\n\n"
                        "Auch die Lehrenden leiden unter diesem Wandel. Statt zu "
                        "forschen, müssen sie immer mehr Verwaltungsaufgaben "
                        "übernehmen, Anträge schreiben und ihre Erfolge in "
                        "messbaren Kennzahlen darstellen. Wissenschaftliche "
                        "Neugierde und langfristiges Denken haben es schwer in "
                        "einem System, das nur kurzfristige Resultate belohnt.\n\n"
                        "Es wäre falsch, in nostalgischer Verklärung zur 'guten "
                        "alten Universität' zurückkehren zu wollen. Aber wir "
                        "sollten uns ernsthaft fragen, ob die radikale "
                        "Ökonomisierung der Hochschulen nicht mehr zerstört, als "
                        "sie nützt. Eine Gesellschaft, die nur noch nach "
                        "Effizienz fragt, verliert am Ende ihre Fähigkeit zur "
                        "kritischen Selbstreflexion. Und genau diese Fähigkeit "
                        "war es, die unsere Universitäten einmal so wertvoll "
                        "gemacht hat."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wie wird die Universität laut Autor heute betrachtet?",
                    "options": [
                        "Als Ort freier Forschung",
                        "Als Dienstleistungsbetrieb mit Studierenden als 'Kunden'",
                        "Als gesellschaftliches Zentrum",
                        "Als reine Forschungseinrichtung",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Wie wirkt sich der Wandel auf die Studierenden aus?",
                    "options": [
                        "Sie studieren mehr aus Interesse.",
                        "Sie denken ökonomischer und vermeiden 'unrealistische' Fächer.",
                        "Sie sind politisch engagierter.",
                        "Sie wählen häufiger Geisteswissenschaften.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Worunter leiden die Lehrenden?",
                    "options": [
                        "Schlechter Bezahlung",
                        "Wachsendem Verwaltungsaufwand und Druck zu kurzfristigen Ergebnissen",
                        "Mangel an Studierenden",
                        "Veralteter Technik",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Welche Position vertritt der Autor am Ende?",
                    "options": [
                        "Zurück zur alten Universität ohne Veränderungen",
                        "Komplette Marktorientierung der Universitäten",
                        "Eine kritische Auseinandersetzung mit der Ökonomisierung",
                        "Schließung der Universitäten",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was riskiert eine reine 'Effizienzgesellschaft' laut Text?",
                    "options": [
                        "Wirtschaftlichen Erfolg",
                        "Die Fähigkeit zur kritischen Selbstreflexion",
                        "Den Zugang zur Universität für alle",
                        "Den internationalen Ruf",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Sachartikel über Künstliche Intelligenz.",
            "max_points": 40,
            "texts": [
                {
                    "title": "KI im Arbeitsalltag — Bedrohung oder Chance?",
                    "text": (
                        "Kaum ein Thema wird derzeit so kontrovers diskutiert wie "
                        "die Künstliche Intelligenz. Während die einen vor dem "
                        "Verlust von Millionen Arbeitsplätzen warnen, sehen andere "
                        "in der KI die größte Chance seit der industriellen Revolution. "
                        "Wie so oft liegt die Wahrheit irgendwo dazwischen.\n\n"
                        "Fest steht: KI wird viele Tätigkeiten verändern. "
                        "Routinetätigkeiten in der Verwaltung, einfache Übersetzungen "
                        "oder die Auswertung großer Datenmengen können Maschinen "
                        "bereits heute schneller und oft auch besser erledigen als "
                        "Menschen. Das bedeutet nicht zwangsläufig, dass die "
                        "betroffenen Berufe verschwinden — aber sie werden sich "
                        "wandeln. Wer heute als Sachbearbeiter arbeitet, wird "
                        "morgen vielleicht eher KI-Systeme überwachen und "
                        "korrigieren.\n\n"
                        "Bemerkenswert ist, dass auch hochqualifizierte Berufe "
                        "betroffen sind. Anwälte, Ärzte und sogar Programmierer "
                        "müssen sich darauf einstellen, dass Routinearbeiten von "
                        "Maschinen übernommen werden. Was bleibt, ist die "
                        "anspruchsvolle, kreative und zwischenmenschliche Arbeit. "
                        "Empathie, ethisches Urteilsvermögen und originelles "
                        "Denken — das sind Fähigkeiten, die selbst die beste KI "
                        "nicht ersetzen kann.\n\n"
                        "Die wichtigste Frage ist daher nicht, ob KI uns die "
                        "Arbeit wegnimmt, sondern wie wir uns darauf vorbereiten. "
                        "Lebenslanges Lernen, Flexibilität und die Bereitschaft, "
                        "neue Fähigkeiten zu erwerben, werden entscheidender "
                        "denn je. Bildungssysteme und Politik müssen jetzt "
                        "handeln — wer heute zögert, wird morgen die Folgen "
                        "spüren."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wie steht der Autor zur KI?",
                    "options": [
                        "Reine Begeisterung",
                        "Reine Ablehnung",
                        "Differenzierte Sicht: Wahrheit liegt zwischen Extrempositionen",
                        "Gleichgültigkeit",
                    ],
                    "correct_index": 2,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was wird laut Text mit Routineberufen passieren?",
                    "options": [
                        "Sie verschwinden komplett.",
                        "Sie verändern sich, viele werden zur Überwachung von KI-Systemen.",
                        "Sie bleiben unverändert.",
                        "Sie werden besser bezahlt.",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Welche Berufe sind laut Text NICHT von KI bedroht?",
                    "options": [
                        "Sachbearbeiter",
                        "Anwälte",
                        "Programmierer",
                        "Keine — auch hochqualifizierte Berufe sind betroffen.",
                    ],
                    "correct_index": 3,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Welche Fähigkeiten bleiben laut Text wertvoll?",
                    "options": [
                        "Schnelles Tippen",
                        "Empathie, ethisches Urteilen, kreatives Denken",
                        "Mathematik",
                        "Fremdsprachen",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
                {
                    "question": "Was fordert der Autor am Schluss?",
                    "options": [
                        "Verbot von KI",
                        "Lebenslanges Lernen und schnelles Handeln in Bildung und Politik",
                        "Mehr Forschung in KI",
                        "Höhere Steuern für KI-Firmen",
                    ],
                    "correct_index": 1,
                    "question_type": "multiple_choice",
                },
            ],
        },
    ],
}


# =====================================================================
# B2 — Hören
# =====================================================================
B2_HOEREN = {
    "level": "B2",
    "section": "Hören",
    "time_limit_minutes": 35,
    "max_score": 80,
    "instructions": "Hörverstehen B2 mit komplexeren Texten.",
    "parts": [
        {
            "part_number": 1,
            "instruction": "Vortrag eines Wirtschaftsexperten.",
            "max_points": 40,
            "scripts": [
                {
                    "title": "Vortrag — Die Zukunft der deutschen Wirtschaft",
                    "speaker_context": "Ein Wirtschaftsexperte hält einen Vortrag bei der IHK.",
                    "script": (
                        "Sehr geehrte Damen und Herren, ich möchte heute über drei "
                        "Herausforderungen sprechen, vor denen die deutsche Wirtschaft "
                        "in den kommenden Jahren steht.\n\n"
                        "Die erste Herausforderung ist der Fachkräftemangel. In den "
                        "nächsten fünfzehn Jahren werden etwa zwölf Millionen "
                        "Arbeitnehmer in den Ruhestand gehen, gleichzeitig kommen "
                        "aber nur etwa neun Millionen junge Menschen nach. Das ist "
                        "eine Lücke von drei Millionen, die wir nur durch zwei Wege "
                        "schließen können: mehr Zuwanderung und höhere Beschäftigungs"
                        "quoten von Frauen und älteren Menschen.\n\n"
                        "Die zweite Herausforderung ist die Digitalisierung. "
                        "Während andere Länder wie Estland oder Südkorea ihre "
                        "Verwaltung weitgehend digitalisiert haben, hinkt "
                        "Deutschland noch deutlich hinterher. Das macht uns nicht "
                        "nur weniger effizient, sondern auch weniger attraktiv für "
                        "internationale Unternehmen, die schnelle und unbürokratische "
                        "Prozesse erwarten.\n\n"
                        "Die dritte und vielleicht wichtigste Herausforderung ist "
                        "die Energiewende. Deutschland hat ehrgeizige Klimaziele "
                        "gesetzt, aber die Umsetzung ist teuer und kompliziert. "
                        "Die Industrie braucht zuverlässige und bezahlbare Energie. "
                        "Wenn die Strompreise zu hoch werden, verlieren wir "
                        "Standortvorteile, und energieintensive Unternehmen "
                        "verlagern ihre Produktion ins Ausland.\n\n"
                        "Mein Fazit: Die deutsche Wirtschaft hat die Substanz, "
                        "auch in Zukunft erfolgreich zu sein. Aber wir dürfen "
                        "keine Zeit mehr verlieren. Bildung, Infrastruktur und "
                        "verlässliche politische Rahmenbedingungen sind jetzt "
                        "wichtiger denn je."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Wie groß ist die erwartete Lücke an Arbeitskräften in 15 Jahren?",
                    "options": [
                        "1 Million",
                        "3 Millionen",
                        "9 Millionen",
                        "12 Millionen",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Welche zwei Lösungen nennt der Experte für den Fachkräftemangel?",
                    "options": [
                        "Mehr Roboter und KI",
                        "Mehr Zuwanderung und höhere Beschäftigung von Frauen/älteren Menschen",
                        "Längere Arbeitszeiten und weniger Urlaub",
                        "Outsourcing nach Asien",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Welche Länder werden als Vorbild für Digitalisierung genannt?",
                    "options": [
                        "USA und Japan",
                        "Estland und Südkorea",
                        "Frankreich und Italien",
                        "Schweiz und Österreich",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Was ist laut Experten das größte Risiko der Energiewende?",
                    "options": [
                        "Stromausfälle",
                        "Hohe Strompreise und Abwanderung der Industrie",
                        "Mangel an Fachkräften",
                        "Politische Proteste",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie ist sein Gesamtfazit?",
                    "options": [
                        "Pessimistisch — Deutschland verliert.",
                        "Optimistisch, aber mit dringender Handlungsaufforderung.",
                        "Gleichgültig",
                        "Sehr optimistisch ohne Bedingungen",
                    ],
                    "correct_index": 1,
                },
            ],
        },
        {
            "part_number": 2,
            "instruction": "Diskussion zwischen zwei Pädagogen.",
            "max_points": 40,
            "scripts": [
                {
                    "title": "Diskussion — Smartphones in der Schule",
                    "speaker_context": "Zwei Lehrkräfte diskutieren über Handys im Unterricht.",
                    "script": (
                        "Frau Bauer: Ich bin der festen Überzeugung, dass Smartphones "
                        "in der Schule grundsätzlich verboten werden sollten. Sie "
                        "lenken die Schüler ab, fördern Mobbing und schaden der "
                        "Konzentrationsfähigkeit. In meinen Klassen sehe ich täglich, "
                        "wie die Aufmerksamkeit darunter leidet.\n\n"
                        "Herr Klein: Ich verstehe Ihre Sorgen, aber ein Verbot löst "
                        "das Problem nicht. Smartphones gehören zur Lebensrealität "
                        "unserer Schüler. Statt sie zu verbieten, sollten wir den "
                        "verantwortungsvollen Umgang lehren. Außerdem können Handys "
                        "im Unterricht durchaus sinnvoll eingesetzt werden — für "
                        "Recherchen, interaktive Aufgaben oder Übersetzungen.\n\n"
                        "Frau Bauer: Das mag in der Theorie funktionieren, aber in "
                        "der Praxis sehen die Schüler das Handy nicht als Lernwerkzeug, "
                        "sondern als Spielzeug. Studien zeigen klar: Schulen, die "
                        "Smartphones verbannt haben, verzeichnen bessere Lernergebnisse "
                        "und weniger Mobbing-Fälle.\n\n"
                        "Herr Klein: Welche Studien meinen Sie? Es gibt auch Studien, "
                        "die das Gegenteil zeigen. Wir dürfen die Realität nicht "
                        "ignorieren. Wenn wir den Schülern jetzt das Handy wegnehmen, "
                        "lernen sie nie, damit umzugehen. Nach der Schule stehen sie "
                        "dann hilflos da.\n\n"
                        "Frau Bauer: Den verantwortungsvollen Umgang können sie auch "
                        "zu Hause oder in speziellen Medienkursen lernen. In der "
                        "Schule sollten wir uns auf Bildung konzentrieren, nicht "
                        "auf Smartphone-Erziehung.\n\n"
                        "Herr Klein: Vielleicht ist ein Mittelweg die Lösung: Handys "
                        "während der Unterrichtsstunden in einer Box, aber gezielt "
                        "in bestimmten Lernsituationen erlaubt. So kombinieren wir "
                        "beides — Konzentration und digitale Bildung."
                    ),
                }
            ],
            "questions": [
                {
                    "question": "Was ist Frau Bauers Position?",
                    "options": [
                        "Smartphones sollten unbeschränkt erlaubt sein.",
                        "Smartphones sollten in der Schule grundsätzlich verboten werden.",
                        "Smartphones sind ihr egal.",
                        "Smartphones nur für Lehrkräfte erlauben.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Was ist Herr Kleins Hauptargument?",
                    "options": [
                        "Smartphones sind Teil der Lebensrealität, ein Verbot löst nichts.",
                        "Schüler können nicht ohne Smartphone lernen.",
                        "Lehrer brauchen Smartphones.",
                        "Eltern wollen kein Verbot.",
                    ],
                    "correct_index": 0,
                },
                {
                    "question": "Welche Beweise nennt Frau Bauer?",
                    "options": [
                        "Eigene Erfahrungen",
                        "Studien über bessere Lernergebnisse in Schulen mit Verbot",
                        "Aussagen von Eltern",
                        "Internationale Vergleichstests",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Wie reagiert Herr Klein auf die Studien?",
                    "options": [
                        "Er stimmt zu.",
                        "Er bezweifelt sie und verweist auf gegenteilige Studien.",
                        "Er ignoriert sie.",
                        "Er wird wütend.",
                    ],
                    "correct_index": 1,
                },
                {
                    "question": "Welchen Kompromiss schlägt Herr Klein am Ende vor?",
                    "options": [
                        "Komplettes Verbot",
                        "Komplette Erlaubnis",
                        "Handys in einer Box, aber gezielter Einsatz in Lernsituationen",
                        "Eltern entscheiden lassen",
                    ],
                    "correct_index": 2,
                },
            ],
        },
    ],
}


# =====================================================================
# B2 — Schreiben
# =====================================================================
B2_SCHREIBEN = {
    "level": "B2",
    "section": "Schreiben",
    "time_limit_minutes": 75,
    "max_score": 100,
    "instructions": "Zwei anspruchsvolle Schreibaufgaben.",
    "parts": [
        {
            "task_number": 1,
            "instruction": "Formelle Beschwerde an ein Unternehmen.",
            "prompt": (
                "Du hast vor einem Monat einen Laptop bei einem Online-Shop "
                "gekauft. Das Gerät ist seit zwei Wochen defekt: Es startet "
                "nicht mehr und der Akku überhitzt. Du hast den Kundenservice "
                "bereits zweimal kontaktiert, aber keine zufriedenstellende "
                "Antwort erhalten. Schreibe einen formellen Beschwerdebrief:\n"
                "• Beschreibe den Vorfall und das Problem genau\n"
                "• Erkläre, was du bereits unternommen hast\n"
                "• Verweise auf deine Rechte als Verbraucher\n"
                "• Fordere eine konkrete Lösung mit Frist\n"
                "• Drohe an, rechtliche Schritte einzuleiten, falls keine Reaktion erfolgt"
            ),
            "min_words": 150,
            "max_words": 200,
            "format_hint": "Streng formell. Briefkopf, Betreff, Anrede, gegliederter Hauptteil, formelle Schlussformel.",
            "model_answer": (
                "Sehr geehrte Damen und Herren,\n\n"
                "mit großem Bedauern wende ich mich an Sie, um mich offiziell über "
                "ein gravierendes Problem mit einem bei Ihnen erworbenen Produkt "
                "zu beschweren.\n\n"
                "Am 15. März kaufte ich in Ihrem Online-Shop einen Laptop der "
                "Marke TechPro (Bestellnummer: 4587-2023) für 1.199 Euro. Bereits "
                "nach zwei Wochen traten erste Probleme auf: Das Gerät startet "
                "seitdem nicht mehr zuverlässig und der Akku überhitzt während "
                "des Betriebs gefährlich.\n\n"
                "Ich habe Ihren Kundenservice bereits am 10. und 18. April "
                "telefonisch kontaktiert. Beide Male wurde mir eine Rückmeldung "
                "innerhalb von 48 Stunden zugesichert, die jedoch bis heute "
                "ausgeblieben ist. Diese Vorgehensweise empfinde ich als äußerst "
                "unprofessionell.\n\n"
                "Gemäß den geltenden Verbraucherrechten habe ich Anspruch auf "
                "eine kostenlose Reparatur, einen Austausch oder die vollständige "
                "Rückerstattung des Kaufpreises. Ich fordere Sie daher auf, bis "
                "zum 5. Mai eine konkrete Lösung anzubieten. Sollte bis zu diesem "
                "Datum keine angemessene Reaktion erfolgen, werde ich rechtliche "
                "Schritte einleiten und mich an die Verbraucherzentrale wenden.\n\n"
                "Ich erwarte Ihre umgehende Antwort.\n\n"
                "Mit freundlichen Grüßen,\n"
                "Daniel Weber"
            ),
            "max_points": 50,
        },
        {
            "task_number": 2,
            "instruction": "Argumentativer Aufsatz zu einem aktuellen Thema.",
            "prompt": (
                "Schreibe einen argumentativen Aufsatz zur Frage: 'Sollte das "
                "Studium an deutschen Universitäten weiterhin kostenlos bleiben?'\n"
                "Strukturiere deinen Text klar:\n"
                "• Einleitung mit These\n"
                "• Mindestens zwei Argumente FÜR ein kostenloses Studium\n"
                "• Mindestens zwei Argumente DAGEGEN (mit Studiengebühren)\n"
                "• Deine persönliche Meinung mit Begründung\n"
                "• Schluss mit Fazit"
            ),
            "min_words": 180,
            "max_words": 220,
            "format_hint": "Klare Argumentation, Konnektoren (einerseits/andererseits, jedoch, daher), neutraler akademischer Stil",
            "model_answer": (
                "In den letzten Jahren wird in Deutschland immer wieder darüber "
                "diskutiert, ob das Hochschulstudium auch in Zukunft gebührenfrei "
                "bleiben soll. Diese Frage berührt grundlegende Werte unserer "
                "Gesellschaft und verdient eine differenzierte Betrachtung.\n\n"
                "Für ein kostenloses Studium spricht zunächst, dass es allen jungen "
                "Menschen unabhängig von ihrem familiären Hintergrund den Zugang zu "
                "Bildung ermöglicht. Bildung sollte nicht vom Geldbeutel der Eltern "
                "abhängen. Darüber hinaus profitiert auch die Wirtschaft langfristig "
                "von gut ausgebildeten Fachkräften, die ohne hohe Schulden ins "
                "Berufsleben starten können.\n\n"
                "Andererseits gibt es auch gewichtige Argumente für moderate "
                "Studiengebühren. Erstens würden zusätzliche Mittel den oft chronisch "
                "unterfinanzierten Universitäten helfen, ihre Lehre und Forschung zu "
                "verbessern. Zweitens zeigen Erfahrungen aus anderen Ländern, dass "
                "Studierende ihr Studium ernster nehmen, wenn sie selbst dafür zahlen.\n\n"
                "Meiner persönlichen Meinung nach überwiegen jedoch die Argumente "
                "für ein kostenloses Studium. Die Chancengleichheit ist ein zu "
                "wichtiges gesellschaftliches Gut, um es ökonomischen Erwägungen "
                "zu opfern. Statt Gebühren einzuführen, sollte der Staat die "
                "Universitäten besser finanzieren — etwa durch eine gerechtere "
                "Steuerpolitik.\n\n"
                "Zusammenfassend lässt sich sagen, dass die Bildung als öffentliches "
                "Gut behandelt werden muss. Nur so kann Deutschland langfristig "
                "wettbewerbsfähig und sozial gerecht bleiben."
            ),
            "max_points": 50,
        },
    ],
}


# =====================================================================
# B2 — Sprechen
# =====================================================================
B2_SPRECHEN = {
    "level": "B2",
    "section": "Sprechen",
    "time_limit_minutes": 15,
    "max_score": 100,
    "instructions": "Drei anspruchsvolle Sprechaufgaben.",
    "parts": [
        {
            "card_number": 1,
            "task_type": "Vortrag mit Argumentation",
            "prompt": (
                "Halte einen vierminütigen Vortrag zum Thema 'Plastikverbot — "
                "sinnvoll oder übertrieben?'. Strukturiere deinen Vortrag mit "
                "Einleitung, Pro- und Kontra-Argumenten, persönlicher Meinung "
                "und Schlussfolgerung. Nutze verbindende Wörter wie 'einerseits', "
                "'andererseits', 'darüber hinaus', 'zusammenfassend'."
            ),
            "supporting_questions": [
                "Welche Plastikprodukte sollten verboten werden?",
                "Welche Auswirkungen hat Plastik auf die Umwelt?",
                "Was sind realistische Alternativen?",
                "Welche Rolle spielen Verbraucher und Politik?",
            ],
            "time_allowed_seconds": 240,
        },
        {
            "card_number": 2,
            "task_type": "Diskussion mit Gegenargumenten",
            "prompt": (
                "Du diskutierst mit jemandem, der die Meinung vertritt: "
                "'Soziale Medien machen Jugendliche unglücklich und sollten "
                "für unter Sechzehnjährige verboten werden.' Stelle die "
                "Gegenposition dar und entwickle mindestens drei differenzierte "
                "Gegenargumente. Reagiere auf mögliche Einwände."
            ),
            "supporting_questions": [
                "Welche positiven Aspekte haben soziale Medien für Jugendliche?",
                "Wie effektiv wären Verbote tatsächlich?",
                "Was wären Alternativen zu einem Verbot?",
                "Wer trägt die Verantwortung — Eltern, Schule oder Politik?",
            ],
            "time_allowed_seconds": 240,
        },
        {
            "card_number": 3,
            "task_type": "Verhandlung",
            "prompt": (
                "Du arbeitest seit drei Jahren in deinem Unternehmen und führst "
                "ein Gespräch mit deiner Vorgesetzten über eine Gehaltserhöhung. "
                "Bringe überzeugende Argumente: deine Leistungen, zusätzliche "
                "Verantwortung, Marktvergleich. Reagiere professionell auf "
                "mögliche Einwände wie 'Unsere wirtschaftliche Lage ist schwierig'."
            ),
            "supporting_questions": [
                "Welche konkreten Erfolge kannst du vorweisen?",
                "Wie viel Gehaltserhöhung möchtest du?",
                "Welche zusätzlichen Aufgaben hast du übernommen?",
                "Wie reagierst du auf eine Ablehnung?",
            ],
            "time_allowed_seconds": 240,
        },
    ],
}


# =====================================================================
# Master registry
# =====================================================================
EXAM_PAPERS = {
    "A1_Lesen": A1_LESEN,
    "A1_Hören": A1_HOEREN,
    "A1_Schreiben": A1_SCHREIBEN,
    "A1_Sprechen": A1_SPRECHEN,
    "A2_Lesen": A2_LESEN,
    "A2_Hören": A2_HOEREN,
    "A2_Schreiben": A2_SCHREIBEN,
    "A2_Sprechen": A2_SPRECHEN,
    "B1_Lesen": B1_LESEN,
    "B1_Hören": B1_HOEREN,
    "B1_Schreiben": B1_SCHREIBEN,
    "B1_Sprechen": B1_SPRECHEN,
    "B2_Lesen": B2_LESEN,
    "B2_Hören": B2_HOEREN,
    "B2_Schreiben": B2_SCHREIBEN,
    "B2_Sprechen": B2_SPRECHEN,
}

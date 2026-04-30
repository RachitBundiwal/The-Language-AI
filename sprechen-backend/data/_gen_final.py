import builtins, pathlib, re

_real_open = builtins.open
def _utf8_open(file, mode="r", **kw):
    if "b" not in mode and kw.get("encoding") is None:
        kw["encoding"] = "utf-8"
    return _real_open(file, mode, **kw)
builtins.open = _utf8_open

SEEDS = pathlib.Path(__file__).parent / "lesson_seeds.py"
src = SEEDS.read_text(encoding="utf-8")
existing = set(re.findall(r"^(LESSON_\d+)\s*=", src, re.MULTILINE))
print(f"Existing lessons before append: {len(existing)}")

APPEND = '''

LESSON_166 = {
    "title": "Advanced Discourse Markers and Text Cohesion",
    "level": "C1",
    "scenario": "academic_writing",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Use advanced discourse markers to create cohesive, well-organized German texts",
        "Distinguish between causal, adversative, concessive, and additive connectors",
        "Produce complex argumentation with appropriate signposting",
        "Identify cohesion devices in authentic academic and journalistic texts",
    ],
    "cultural_note": "German text cohesion relies heavily on explicit connectors and discourse markers. Unlike English, which often prefers implicit cohesion or juxtaposition, German academic and journalistic prose signals each logical relationship explicitly, creating highly structured, navigable texts.",
    "grammar_focus": _gex(
        "Advanced Discourse Connectors",
        "Discourse connectors signal logical relationships between clauses and paragraphs. They differ from subordinating conjunctions in that they can appear in the Mittelfeld (middle field) or independently, and they affect word order differently.",
        "'Demnach / Folglich / Daher' (therefore) / 'Infolgedessen' (as a result) / 'Gleichwohl / Nichtsdestotrotz' (nevertheless) / 'Wohingegen' (whereas)",
        ["Causal: daher, deshalb, demnach, folglich, infolgedessen, demzufolge", "Adversative: wohingegen, hingegen, demgegenüber", "Concessive: gleichwohl, nichtsdestotrotz, nichtsdestoweniger", "Additive: darüber hinaus, überdies, zudem, des Weiteren"],
        ["Folglich lässt sich schlussfolgern, dass die These bestätigt wird.", "Wohingegen ältere Studien X zeigten, belegen neuere Daten Y.", "Nichtsdestotrotz bleibt die Grundfrage offen."],
    ),
    "dialogue": [
        _t("tutor", "Ihr Text ist inhaltlich gut, aber die Übergänge zwischen den Absätzen sind abrupt.", "Your text is good in content, but the transitions between paragraphs are abrupt."),
        _t("student", "Was meinen Sie konkret?", "What do you mean specifically?"),
        _t("tutor", "Sie wechseln ohne Signalwörter von einem Argument zum nächsten.", "You switch from one argument to the next without signal words."),
        _t("student", "Wie verbinde ich sie besser?", "How do I connect them better?"),
        _t("tutor", "Zum Beispiel: 'Darüber hinaus' für Ergänzungen, 'Wohingegen' für Kontraste.", "For example: 'Furthermore' for additions, 'Whereas' for contrasts."),
        _t("student", "Und für Schlussfolgerungen?", "And for conclusions?"),
        _t("tutor", "'Folglich', 'demnach', oder 'infolgedessen' – je nach Stärke der logischen Verbindung.", "'Therefore', 'accordingly', or 'as a result' – depending on the strength of the logical connection."),
        _t("student", "Und für Einschränkungen?", "And for limitations?"),
    ],
    "vocabulary_list": [
        _v("folglich", "therefore / consequently", "Folglich ist das Ergebnis eindeutig."),
        _v("demnach", "accordingly / therefore", "Demnach lässt sich schlussfolgern..."),
        _v("infolgedessen", "as a result / consequently", "Infolgedessen stiegen die Kosten."),
        _v("wohingegen", "whereas", "Wohingegen A stieg, sank B."),
        _v("gleichwohl", "nevertheless / nonetheless (formal)", "Gleichwohl bleibt die Frage offen."),
        _v("nichtsdestotrotz", "nevertheless / nonetheless", "Nichtsdestotrotz ist es wichtig."),
        _v("darüber hinaus", "furthermore / in addition", "Darüber hinaus ist zu beachten..."),
        _v("demgegenüber", "in contrast / on the other hand", "Demgegenüber stehen andere Befunde."),
        _v("des Weiteren", "furthermore / moreover (formal)", "Des Weiteren gilt es zu bedenken..."),
        _v("überdies", "moreover / besides (formal)", "Überdies ist das Verfahren erprobt."),
    ],
    "exercises": [
        _ex_fib(
            "Choose the correct discourse marker",
            ["A stieg. B sank. ___ lässt sich eine Divergenz feststellen. (causal/resultive)", "Ältere Studien zeigten X. ___ belegen neue Daten Y. (adversative)", "Die Kosten sind hoch. ___ ist die Methode erprobt. (additive)"],
            ["Folglich", "Wohingegen", "Darüber hinaus"],
        ),
        _ex_mc(
            "Classify the discourse function",
            [
                ("'Infolgedessen stiegen die Kosten.' – What logical relation?", ["Adversative", "Concessive", "Causal/resultive", "Additive"], 2),
                ("'Nichtsdestotrotz bleibt die Frage offen.' – What logical relation?", ["Causal", "Additive", "Concessive", "Adversative"], 2),
                ("'Des Weiteren gilt es zu beachten...' – What logical relation?", ["Adversative", "Additive", "Concessive", "Resultive"], 1),
            ],
        ),
        _ex_tr(
            "Translate using discourse markers",
            [
                ("Whereas older studies showed X, newer data demonstrate Y.", "Wohingegen ältere Studien X zeigten, belegen neuere Daten Y."),
                ("As a result, the costs increased significantly.", "Infolgedessen stiegen die Kosten erheblich."),
                ("Furthermore, it is important to note that...", "Darüber hinaus ist zu beachten, dass..."),
            ],
        ),
        _ex_arr(
            "Reconstruct the cohesive text",
            [
                (["Folglich", "lässt", "sich", "schlussfolgern", "dass", "die", "These", "bestätigt", "wird"], "Folglich lässt sich schlussfolgern, dass die These bestätigt wird."),
            ],
        ),
        _ex_sp(
            "Cohesion in practice",
            ["Take a text you have written and add at least five discourse markers to improve cohesion.", "Explain the difference between 'jedoch' and 'wohingegen' to a fellow learner.", "Write a paragraph on any topic using at least one connector from each logical category."],
        ),
    ],
}

LESSON_167 = {
    "title": "Collocations with Prepositions: Advanced Prepositional Phrases",
    "level": "C1",
    "scenario": "vocabulary_precision",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Master fixed prepositional collocations with common German verbs and adjectives",
        "Avoid prepositional errors typical of C1 learners",
        "Use prepositional phrases in academic and professional contexts correctly",
        "Build a systematic knowledge of German prepositional government",
    ],
    "cultural_note": "Prepositional government (Rektion) in German is highly lexicalised – the preposition that follows a verb or adjective must be memorised as part of the lexical item, not derived from rules. This is one of the last major systematic challenges for learners at C1/C2.",
    "grammar_focus": _gex(
        "Prepositional Government (Rektion)",
        "Many German verbs and adjectives require a specific preposition. Unlike English, these cannot be predicted from meaning. They must be learned as collocations: abhängen von, bestehen auf, verzichten auf, ankommen auf, reagieren auf.",
        "'abhängen von' (to depend on) / 'bestehen auf' (to insist on) / 'verzichten auf' (to forgo) / 'ankommen auf' (to depend on / matter) / 'eingehen auf' (to engage with)",
        ["auf + Akkusativ: warten auf, reagieren auf, antworten auf, verzichten auf, ankommen auf", "von + Dativ: abhängen von, profitieren von, überzeugen von, abraten von", "für + Akkusativ: sorgen für, verantwortlich für, bekannt für, geeignet für"],
        ["Es kommt auf die Qualität an.", "Das hängt von mehreren Faktoren ab.", "Er bestand auf einer sofortigen Antwort.", "Sie verzichtete auf das Angebot."],
    ),
    "dialogue": [
        _t("advanced_learner", "Ich kämpfe immer noch mit den Präpositionalergänzungen – 'abhängen von' oder 'abhängen auf'?", "I still struggle with prepositional complements – 'depend from' or 'depend on'?"),
        _t("teacher", "Immer 'abhängen von'. Die Präposition ist Teil des Verbs – sie muss auswendig gelernt werden.", "Always 'abhängen von'. The preposition is part of the verb – it must be memorised."),
        _t("advanced_learner", "Und 'bestehen'? 'Bestehen auf' oder 'bestehen an'?", "And 'bestehen'? 'Bestehen auf' or 'bestehen an'?"),
        _t("teacher", "'Bestehen auf' – er besteht auf seiner Meinung. Aber auch: 'bestehen aus' – der Tisch besteht aus Holz.", "'Bestehen auf' – he insists on his opinion. But also: 'bestehen aus' – the table consists of wood."),
        _t("advanced_learner", "Also hat ein Verb manchmal mehrere Präpositionen – mit verschiedenen Bedeutungen?", "So a verb sometimes has multiple prepositions – with different meanings?"),
        _t("teacher", "Genau. 'Bestehen auf' = insist. 'Bestehen aus' = consist of. 'Bestehen in' = consist in/lie in.", "Exactly. 'Bestehen auf' = insist. 'Bestehen aus' = consist of. 'Bestehen in' = consist in/lie in."),
        _t("advanced_learner", "Das ist am schwierigsten – dieselbe Grundform mit verschiedenen Präpositionen.", "That is hardest – the same base form with different prepositions."),
        _t("teacher", "Lernen Sie die ganzen Phrasen: 'bestehen auf + Dativ' als Einheit.", "Learn the whole phrases: 'bestehen auf + Dativ' as a unit."),
    ],
    "vocabulary_list": [
        _v("abhängen von (+ Dat)", "to depend on", "Das hängt von der Situation ab."),
        _v("bestehen auf (+ Dat)", "to insist on", "Er besteht auf einer Entschuldigung."),
        _v("bestehen aus (+ Dat)", "to consist of", "Das Gericht besteht aus vier Gängen."),
        _v("verzichten auf (+ Akk)", "to forgo / give up", "Sie verzichtet auf Zucker."),
        _v("ankommen auf (+ Akk)", "to depend on / matter", "Es kommt auf die Details an."),
        _v("eingehen auf (+ Akk)", "to address / engage with", "Er ging auf alle Fragen ein."),
        _v("reagieren auf (+ Akk)", "to react to / respond to", "Sie reagierte nicht auf seine Nachricht."),
        _v("profitieren von (+ Dat)", "to benefit from / profit from", "Alle profitieren von der Reform."),
        _v("verantwortlich für (+ Akk)", "responsible for", "Wer ist verantwortlich für den Fehler?"),
        _v("geeignet für (+ Akk)", "suitable for / appropriate for", "Das ist geeignet für Anfänger."),
    ],
    "exercises": [
        _ex_fib(
            "Insert the correct preposition",
            ["Das hängt ___ vielen Faktoren ab.", "Er bestand ___ einer schriftlichen Bestätigung.", "Sie reagierte nicht ___ seine Nachricht."],
            ["von", "auf", "auf"],
        ),
        _ex_mc(
            "Choose the correct prepositional collocation",
            [
                ("'To consist of' in German:", ["bestehen auf", "bestehen aus", "bestehen in", "bestehen über"], 1),
                ("'It depends on the quality.' in German:", ["Es hängt von der Qualität ab.", "Es kommt auf der Qualität an.", "Es kommt auf die Qualität an.", "Es hängt auf die Qualität ab."], 2),
                ("'She gave up the offer.' in German:", ["Sie verzichtete über das Angebot.", "Sie verzichtete auf das Angebot.", "Sie verzichtete von dem Angebot.", "Sie verzichtete das Angebot."], 1),
            ],
        ),
        _ex_tr(
            "Translate using correct prepositional government",
            [
                ("That depends on several factors.", "Das hängt von mehreren Faktoren ab."),
                ("He insisted on an immediate answer.", "Er bestand auf einer sofortigen Antwort."),
                ("Everyone benefits from the reform.", "Alle profitieren von der Reform."),
            ],
        ),
        _ex_arr(
            "Reconstruct the prepositional sentence",
            [
                (["Es", "kommt", "auf", "die", "Qualität", "an", "nicht", "auf", "die", "Geschwindigkeit"], "Es kommt auf die Qualität an, nicht auf die Geschwindigkeit."),
            ],
        ),
        _ex_sp(
            "Prepositions in use",
            ["Describe a decision that depends on several factors – use 'abhängen von' and 'ankommen auf'.", "Discuss a project you worked on using five prepositional collocations from today.", "Quiz your partner: give the base form; they supply the preposition and case."],
        ),
    ],
}

LESSON_168 = {
    "title": "German Word Formation: Advanced Derivation and Composition",
    "level": "C1",
    "scenario": "vocabulary_building",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Form new words using German derivational suffixes and prefixes at an advanced level",
        "Understand the semantic and grammatical effects of common affixes",
        "Decode unfamiliar compound words (Komposita) using word formation knowledge",
        "Build vocabulary actively through systematic word family knowledge",
    ],
    "cultural_note": "German word formation (Wortbildung) is exceptionally productive. New words are coined constantly through compounding (Komposition) and derivation (Derivation). This means a C1 learner who understands the system can decode and produce new vocabulary with high accuracy.",
    "grammar_focus": _gex(
        "Suffixes and Prefixes for Advanced Vocabulary",
        "Key suffixes: -ung (nominalization of verbs), -heit/-keit (abstract from adj), -schaft (collective/relationship), -nis (state/result), -sal. Key prefixes: ver- (transformation, intensity, or negation), zer- (destruction), ent- (removal, beginning), miss- (negation).",
        "'lösen' → 'Lösung' / 'frei' → 'Freiheit' / 'Freundschaft' / 'Ergebnis' / 'verarbeiten' / 'zerreißen' / 'entlassen' / 'missverstehen'",
        ["-ung: (die) Lösung, Verbesserung, Entscheidung, Entwicklung (noun from verb)", "-heit/-keit: Freiheit, Sicherheit, Möglichkeit, Schwierigkeit (abstract from adj)", "ver-: verarbeiten (process), verbessern (improve), verlieren (lose), verbieten (forbid)", "zer-: zerreißen (tear apart), zerstören (destroy), zerbrechen (break apart)"],
        ["Die Verarbeitung (← verarbeiten) der Daten dauert einen Tag.", "Die Unmöglichkeit (un- + Möglichkeit) der Aufgabe ist offensichtlich.", "Er zerbrach das Versprechen (zerbrechen = to break into pieces)."],
    ),
    "dialogue": [
        _t("learner", "Ich bin auf das Wort 'Rücksichtslosigkeit' gestoßen – was bedeutet das?", "I came across the word 'Rücksichtslosigkeit' – what does that mean?"),
        _t("teacher", "Zerlegen wir es: Rücksicht + los + igkeit. 'Rücksicht' = consideration, '-los' = without, '-igkeit' = the quality. Also: 'inconsiderateness'.", "Let us break it down: Rücksicht + los + igkeit. 'Rücksicht' = consideration, '-los' = without, '-igkeit' = the quality. So: 'inconsiderateness'."),
        _t("learner", "Beeindruckend. Und 'Unverantwortlichkeit'?", "Impressive. And 'Unverantwortlichkeit'?"),
        _t("teacher", "Un- (negation) + Verantwortlich (responsible) + -keit (abstract noun) = irresponsibility.", "Un- (negation) + Verantwortlich (responsible) + -keit (abstract noun) = irresponsibility."),
        _t("learner", "Dann kann ich jedes neue Wort einfach zerlegen!", "Then I can simply break down every new word!"),
        _t("teacher", "Meistens. Aber Vorsicht: Manche Morpheme haben mehrere Bedeutungen. 'Ver-' kann Intensivierung oder Negation sein.", "Mostly. But caution: some morphemes have multiple meanings. 'Ver-' can be intensification or negation."),
        _t("learner", "Zum Beispiel?", "For example?"),
        _t("teacher", "'Verbessern' (to improve) vs. 'verbieten' (to forbid) – beide mit 'ver-', aber verschiedene Funktionen.", "'Verbessern' (to improve) vs. 'verbieten' (to forbid) – both with 'ver-', but different functions."),
    ],
    "vocabulary_list": [
        _v("die Wortbildung", "word formation", "Wortbildung ist ein produktiver Prozess."),
        _v("das Kompositum (Komposita)", "compound word", "Das Deutsche liebt Komposita."),
        _v("die Derivation (-en)", "derivation", "Derivation durch Affixe ist produktiv."),
        _v("das Affix (-e)", "affix", "Präfixe und Suffixe sind Affixe."),
        _v("zerlegen", "to break down / decompose", "Zerlegen Sie das Wort in seine Bestandteile."),
        _v("der Bestandteil (-e)", "component / constituent", "Jedes Kompositum hat zwei oder mehr Bestandteile."),
        _v("ableiten", "to derive", "Das Wort lässt sich von 'lösen' ableiten."),
        _v("die Rücksichtslosigkeit", "inconsiderateness", "Rücksichtslosigkeit im Verkehr ist gefährlich."),
        _v("die Unverantwortlichkeit", "irresponsibility", "Das war Unverantwortlichkeit."),
        _v("produktiv (Linguistik)", "productive (linguistics)", "Ein produktives Muster erzeugt viele neue Wörter."),
    ],
    "exercises": [
        _ex_fib(
            "Derive the correct word form",
            ["'frei' + Suffix → die ___ (abstract noun)", "'verarbeiten' + Suffix → die ___ (nominalization)", "'un-' + 'möglicher' + Suffix → die ___ (impossibility)"],
            ["Freiheit", "Verarbeitung", "Unmöglichkeit"],
        ),
        _ex_mc(
            "Analyze the word formation",
            [
                ("What does '-los' add in 'rücksichtslos'?", ["Collective meaning", "'Without' / absence of", "Intensification", "Diminutive"], 1),
                ("What does 'zer-' indicate in 'zerstören'?", ["Beginning of action", "Intensification only", "Destruction / breaking apart", "Negation"], 2),
                ("Which suffix forms an abstract noun from an adjective?", ["-ung", "-schaft", "-heit/-keit", "-nis"], 2),
            ],
        ),
        _ex_tr(
            "Form and translate word families",
            [
                ("From 'verbessern' (to improve), form the noun: (die) ___. Translate.", "die Verbesserung – improvement"),
                ("From 'entwickeln' (to develop), form the noun: (die) ___. Translate.", "die Entwicklung – development"),
                ("From 'schwierig' (difficult), form the abstract noun: (die) ___.", "die Schwierigkeit – difficulty"),
            ],
        ),
        _ex_arr(
            "Decompose the compound",
            [
                (["Rücksichts-", "-los-", "-igkeit"], "Rücksicht (consideration) + -los (without) + -igkeit (quality) = Rücksichtslosigkeit (inconsiderateness)"),
            ],
        ),
        _ex_sp(
            "Word formation in use",
            ["Take five verbs you know and form all the nouns you can from them.", "Explain 'Schadenfreude', 'Weltschmerz', and 'Angst' by breaking down their components.", "What is the longest German compound word you know? Break it down."],
        ),
    ],
}

LESSON_169 = {
    "title": "Advanced Listening: Formal Speeches and Lectures",
    "level": "C1",
    "scenario": "lecture_hall",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand formal German lectures and academic presentations fully",
        "Identify argumentation structure in spoken academic discourse",
        "Take effective notes in German during extended listening tasks",
        "Ask pertinent follow-up questions in academic settings",
    ],
    "cultural_note": "German university lectures (Vorlesungen) are typically formal, fast-paced, and information-dense. Professors rarely pause for comprehension checks. Active note-taking (Mitschreiben) and post-lecture processing are essential study skills in German-speaking universities.",
    "grammar_focus": _gex(
        "Discourse Structure in Spoken Academic German",
        "Academic speeches follow predictable discourse patterns: Themeneinführung (topic introduction), Hauptargumente (main arguments), Beispiele (examples), Einschränkungen (limitations), Fazit (conclusion). Recognising these structures aids comprehension.",
        "'Lassen Sie mich zunächst...' / 'Im Mittelpunkt steht...' / 'Ich möchte exemplarisch zeigen...' / 'Abschließend sei festgehalten...'",
        ["Opening: Im Folgenden werde ich... / Zunächst möchte ich... / Die zentrale Frage lautet...", "Transition: Damit komme ich zum zweiten Punkt... / Ich wende mich nun... / Hieran anschließend...", "Closing: Zusammenfassend lässt sich sagen... / Ich hoffe, deutlich gemacht zu haben... / Abschließend sei festgehalten..."],
        ["Im Folgenden werde ich drei Thesen vorstellen und diskutieren.", "Damit komme ich zum zweiten und zentralen Argument.", "Abschließend sei festgehalten, dass die Befunde eindeutig sind."],
    ),
    "dialogue": [
        _t("professor", "Im Folgenden werde ich drei zentrale Thesen zur Digitalisierung der Arbeitswelt vorstellen.", "In what follows I will present three central theses on the digitalisation of the world of work."),
        _t("student_notes", "[Note: three theses – digitalization – work]", "[Note: three theses – digitalization – work]"),
        _t("professor", "Zunächst: Die Automatisierung betrifft nicht nur Routinetätigkeiten, sondern zunehmend auch Wissensarbeit.", "First: Automation affects not only routine activities, but increasingly also knowledge work."),
        _t("professor", "Damit komme ich zum zweiten Punkt: Die Qualifikationsanforderungen verschieben sich fundamental.", "I now come to the second point: Qualification requirements are shifting fundamentally."),
        _t("professor", "Drittens, und das ist entscheidend: Die sozialen Sicherungssysteme müssen angepasst werden.", "Thirdly, and this is crucial: Social security systems must be adapted."),
        _t("professor", "Abschließend sei festgehalten: Die Herausforderung ist real. Aber sie ist gestaltbar.", "In conclusion, let it be noted: The challenge is real. But it can be shaped."),
        _t("student_a", "Darf ich fragen: Welche Berufsgruppen sind am stärksten betroffen?", "May I ask: Which occupational groups are most affected?"),
        _t("professor", "Gute Frage. Besonders mittlere Qualifikationsebenen sind gefährdet.", "Good question. Particularly middle qualification levels are at risk."),
    ],
    "vocabulary_list": [
        _v("im Folgenden", "in what follows / below", "Im Folgenden werde ich drei Punkte erläutern."),
        _v("zunächst", "first / initially / to begin with", "Zunächst zur historischen Einordnung."),
        _v("abschließend", "in conclusion / finally", "Abschließend sei festgehalten..."),
        _v("festhalten", "to establish / note / hold (formally)", "Es sei festgehalten, dass..."),
        _v("die These (-n)", "thesis", "Ich stelle drei Thesen auf."),
        _v("die Qualifikationsanforderung (-en)", "qualification requirement", "Qualifikationsanforderungen steigen."),
        _v("gestaltbar", "shapeable / manageable", "Die Zukunft ist gestaltbar."),
        _v("entscheidend", "crucial / decisive", "Das ist der entscheidende Punkt."),
        _v("betreffen", "to affect / concern", "Die Reform betrifft alle Berufsgruppen."),
        _v("die Vorlesung (-en)", "lecture (university)", "Die Vorlesung beginnt um 10 Uhr."),
    ],
    "exercises": [
        _ex_mc(
            "Comprehension: What did the professor argue?",
            [
                ("What is the first thesis?", ["Only routine work is automated", "Automation affects knowledge work too", "Social systems are fine", "Digitalization is only in IT"], 1),
                ("What does the professor say about the challenge?", ["It is unsolvable", "It is not real", "It is real but can be managed", "Only governments can fix it"], 2),
                ("What qualification level is most at risk?", ["Low qualification", "High qualification", "Middle qualification", "All equally"], 2),
            ],
        ),
        _ex_fib(
            "Complete the lecture discourse markers",
            ["___ werde ich drei Thesen vorstellen. (in what follows)", "Damit ___ ich zum zweiten Punkt.", "___ sei festgehalten, dass die Befunde eindeutig sind."],
            ["Im Folgenden", "komme", "Abschließend"],
        ),
        _ex_tr(
            "Translate lecture discourse markers",
            [
                ("In what follows, I will present three central theses.", "Im Folgenden werde ich drei zentrale Thesen vorstellen."),
                ("In conclusion, let it be noted that the findings are clear.", "Abschließend sei festgehalten, dass die Befunde eindeutig sind."),
                ("I now come to the second and central argument.", "Damit komme ich zum zweiten und zentralen Argument."),
            ],
        ),
        _ex_arr(
            "Order the lecture structure",
            [
                (["Drittens und entscheidend", "Zunächst: These 1", "Damit komme ich zum zweiten Punkt", "Abschließend sei festgehalten"], "Zunächst: These 1 → Damit komme ich zum zweiten Punkt → Drittens und entscheidend → Abschließend sei festgehalten"),
            ],
        ),
        _ex_sp(
            "Give a mini-lecture",
            ["Prepare a 3-minute lecture on any topic using the discourse structure from today.", "Ask two follow-up questions to your partner's lecture using academic register.", "What strategies help you follow fast academic German speech?"],
        ),
    ],
}

LESSON_170 = {
    "title": "C1 Final Review: Language in Society and the World",
    "level": "C1",
    "scenario": "capstone_review",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Synthesize all C1-level language skills in an integrated, communicative task",
        "Demonstrate ability to engage with complex social, cultural, and academic topics",
        "Reflect on language learning as a social and cognitive process",
        "Prepare confidently for C1 certification examinations",
    ],
    "cultural_note": "C1 proficiency (Goethe-Zertifikat C1, Telc C1, DSH) opens doors to German universities, high-level professional positions, and full participation in German-speaking society. C1 speakers navigate authentic German texts, media, and conversation with ease – only very rare or highly technical content presents difficulty.",
    "grammar_focus": _gex(
        "C1 Synthesis: Full Grammar Integration",
        "At C1 level, all grammar structures are available. The task is integration: using Konjunktiv I in reported contexts, Konjunktiv II for politeness and counterfactuals, Partizipialkonstruktionen in writing, and complex subordination fluently and accurately.",
        "Er berichtete, die Lage sei, wenngleich angespannt, noch unter Kontrolle – was, wie viele Beobachter anmerkten, möglicherweise zu optimistisch eingeschätzt worden sein dürfte.",
        ["Full passive inventory: wird + PP / wurde + PP / ist/war + PP / wird + PP + werden", "Complex NP: extended participial + relative + appositional", "All subordinators in sequence"],
        ["Das seit Langem diskutierte, immer drängendere Problem wurde nun endlich von der Kommission, die eigens dafür eingesetzt worden war, angegangen.", "Er sagte, er habe alles versucht, was jedoch, wie sich später herausstellte, nicht stimmte."],
    ),
    "dialogue": [
        _t("examiner", "Zum Abschluss des C1-Kurses: Was bedeutet Sprache für Sie persönlich?", "To close the C1 course: What does language mean to you personally?"),
        _t("learner", "Sprache ist mehr als Kommunikation. Sie formt, wie ich denke und wie ich die Welt wahrnehme.", "Language is more than communication. It shapes how I think and how I perceive the world."),
        _t("examiner", "Inwiefern hat Deutsch Ihre Weltsicht verändert?", "In what ways has German changed your worldview?"),
        _t("learner", "Deutsche hat mir Konzepte gegeben, die ich in meiner Muttersprache nicht hatte: Weltschmerz, Schadenfreude, Gemütlichkeit.", "German has given me concepts I didn't have in my native language: Weltschmerz, Schadenfreude, Gemütlichkeit."),
        _t("examiner", "Das ist die tiefste Form des Sprachenlernens.", "That is the deepest form of language learning."),
        _t("learner", "Und der Weg zu C2 – den möchte ich weitergehen.", "And the path to C2 – I want to continue on it."),
        _t("examiner", "Dann bin ich gespannt, was Sie entdecken werden.", "Then I am curious what you will discover."),
        _t("learner", "Ich auch.", "Me too."),
    ],
    "vocabulary_list": [
        _v("wahrnehmen", "to perceive", "Wie nehmen wir die Welt wahr?"),
        _v("die Weltsicht (-en)", "worldview", "Sprache beeinflusst die Weltsicht."),
        _v("inwiefern", "in what way / to what extent", "Inwiefern hat das Ihre Meinung geändert?"),
        _v("die Muttersprache (-n)", "native language / mother tongue", "Meine Muttersprache ist Englisch."),
        _v("gespannt sein auf", "to be curious about / look forward to", "Ich bin gespannt auf das Ergebnis."),
        _v("entdecken", "to discover", "Es gibt immer Neues zu entdecken."),
        _v("eigenständig", "independent / autonomous", "Eigenständiges Lernen ist wichtig.", ),
        _v("drängend", "pressing / urgent", "Das ist ein drängendes Problem."),
        _v("anmerken", "to note / remark", "Er merkte an, dass..."),
        _v("tiefgreifend", "profound / deep-reaching", "Eine tiefgreifende Veränderung der Weltsicht."),
    ],
    "exercises": [
        _ex_fib(
            "C1 synthesis fill-in",
            ["Er berichtete, die Lage ___ noch unter Kontrolle. (Konjunktiv I: sein)", "Das Problem ___ nun endlich ___ (angehen – Passiv Präteritum).", "Sie sagte, sie ___ alles versucht, was sich später als falsch herausstellte. (Konjunktiv I: haben)"],
            ["sei", "wurde / angegangen", "habe"],
        ),
        _ex_mc(
            "C1 final review: spot the error",
            [
                ("Which sentence has a grammar error?", ["Er sagte, er sei krank.", "Er sagte, er wäre krank. (when KI would be ambiguous)", "Er sagte, er ist krank.", "Er sagte, er habe es gewusst."], 2),
                ("Which uses an extended participial phrase correctly?", ["Das Buch, was er geschrieben hat", "Das von ihm geschriebene Buch", "Das Buch das geschrieben von ihm ist", "Das von geschriebene Buch ihm"], 1),
                ("Which is the correct passive in the Perfekt?", ["Das Problem hat gelöst geworden.", "Das Problem ist gelöst worden.", "Das Problem wurde gelöst worden.", "Das Problem ist gelöst gewesen."], 1),
            ],
        ),
        _ex_tr(
            "C1 synthesis translation",
            [
                ("He reported that the situation, although tense, was still under control.", "Er berichtete, die Lage sei, wenngleich angespannt, noch unter Kontrolle."),
                ("The long-discussed, increasingly pressing problem was finally addressed.", "Das seit Langem diskutierte, immer drängendere Problem wurde nun endlich angegangen."),
                ("Language shapes how we think and how we perceive the world.", "Sprache formt, wie wir denken und wie wir die Welt wahrnehmen."),
            ],
        ),
        _ex_arr(
            "Final C1 complex sentence",
            [
                (["Das", "Problem", "wurde", "von", "der", "Kommission", "die", "eigens", "dafür", "eingesetzt", "worden", "war", "angegangen"], "Das Problem wurde von der Kommission, die eigens dafür eingesetzt worden war, angegangen."),
            ],
        ),
        _ex_sp(
            "C1 final speaking exam practice",
            ["Give a 3-minute presentation on a complex topic integrating all C1 grammar features.", "Discuss the role of language in shaping thought – use concrete examples.", "Reflect on your German learning journey: what has changed since you began?"],
        ),
    ],
}

LESSON_171 = {
    "title": "German Poetry: Language at Its Limits",
    "level": "C2",
    "scenario": "poetry_seminar",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Read and analyse German poetry at native level",
        "Understand how poetry challenges and extends language",
        "Engage with Celan, Rilke, and contemporary German poets",
        "Write short German poems experimenting with form and language",
    ],
    "cultural_note": "German poetry has a long and rich tradition from the Baroque through Goethe, Hölderlin, Rilke, and Brecht to Celan and contemporary poets like Nora Gomringer and Jan Wagner. Paul Celan's poetry, written after the Holocaust, represents language pushed to its limits – fractured, neologistic, and deeply resistant to simple translation.",
    "grammar_focus": _gex(
        "Poetic License and Grammatical Deviation",
        "Poetry exploits all grammatical resources and also deviates from norms for effect: omitting articles, inverting syntax, using archaic or invented forms, and creating new compounds. Understanding these deviations requires secure knowledge of the norms.",
        "Celan: 'Niemand knetet uns wieder aus Erde und Lehm' / Rilke: 'Wer, wenn ich schriee, hörte mich denn aus der Engel Ordnungen?'",
        ["Article omission: 'Schwarze Milch der Frühe' (no article → generalisation/abstraction)", "Inversion for rhythm: 'Hörte mich denn aus der Engel Ordnungen wer?' (KJV-style)", "Neologism: Celan coins compound words not found in dictionaries"],
        ["Celan: 'Schwarze Milch der Frühe trinken wir abends' (Todesfuge)", "Rilke: 'Wer, wenn ich schriee, hörte mich denn aus der Engel Ordnungen?' (Duineser Elegien)", "Brecht: 'Erst kommt das Fressen, dann kommt die Moral.'"],
    ),
    "dialogue": [
        _t("seminar_leader", "Wir lesen heute Celans 'Todesfuge'. Was fällt sofort auf?", "Today we read Celan's 'Death Fugue'. What strikes you immediately?"),
        _t("student_a", "Die Wiederholung – 'Schwarze Milch der Frühe' taucht immer wieder auf.", "The repetition – 'Black milk of dawn' keeps recurring."),
        _t("student_b", "Und die Grammatik ist seltsam. 'Trinken wir' am Ende statt am Anfang.", "And the grammar is strange. 'We drink' at the end instead of the beginning."),
        _t("seminar_leader", "Ja – die Inversionen erzeugen einen Sog, eine Zwanghaftigkeit.", "Yes – the inversions create a vortex, a compulsion."),
        _t("student_a", "Die 'schwarze Milch' – ist das eine Metapher für den Tod?", "The 'black milk' – is that a metaphor for death?"),
        _t("seminar_leader", "Es widersetzt sich einer einzelnen Interpretation. Das ist Celans Stärke.", "It resists a single interpretation. That is Celan's strength."),
        _t("student_b", "Das Gedicht ist fast unübersetzbar.", "The poem is almost untranslatable."),
        _t("seminar_leader", "Genau. Und das ist kein Fehler – das ist sein Zweck.", "Exactly. And that is not a flaw – that is its purpose."),
    ],
    "vocabulary_list": [
        _v("die Todesfuge", "Death Fugue (Celan poem)", "Die Todesfuge ist Celans bekanntestes Gedicht."),
        _v("die Fugue / die Fuge (-n)", "fugue (music)", "Die Todesfuge verbindet Musik und Sprache."),
        _v("die Wiederholung (-en)", "repetition", "Wiederholung ist ein poetisches Mittel."),
        _v("die Inversion (-en)", "inversion (syntax)", "Inversionen verändern Rhythmus und Fokus."),
        _v("der Sog", "vortex / pull", "Das Gedicht zieht uns in seinen Sog."),
        _v("die Zwanghaftigkeit", "compulsion / obsessiveness", "Die Wiederholung erzeugt Zwanghaftigkeit."),
        _v("sich widersetzen (+ Dat)", "to resist / defy", "Das Gedicht widersetzt sich Interpretation."),
        _v("die Neologie / der Neologismus", "neologism", "Celan erfindet neue Wörter."),
        _v("die Instanz (-en)", "instance / authority", "Die Engel Ordnungen – eine höhere Instanz?"),
        _v("der Zweck (-e)", "purpose / aim", "Welchen Zweck hat die Dunkelheit?"),
    ],
    "exercises": [
        _ex_mc(
            "Poetry analysis: choose the correct answer",
            [
                ("What poetic technique does 'Schwarze Milch der Frühe' exemplify?", ["Simile", "Onomatopoeia", "Oxymoron/surreal metaphor", "Alliteration only"], 2),
                ("Why does Celan's poem resist single interpretations?", ["It is grammatically wrong", "It deliberately uses ambiguity and fractured language", "It is unfinished", "It is not a serious poem"], 1),
                ("What effect do Celan's inversions create?", ["They simplify the text", "They create vortex-like compulsion and rhythm", "They are errors", "They translate easily into English"], 1),
            ],
        ),
        _ex_fib(
            "Complete with poetic vocabulary",
            ["Celans Gedicht ___ sich jeder einfachen Deutung.", "Die ___ erzeugt einen hypnotischen Rhythmus.", "Das Poem ist fast ___ – und das ist sein Zweck."],
            ["widersetzt", "Wiederholung", "unübersetzbar"],
        ),
        _ex_tr(
            "Translate poetic German (with commentary)",
            [
                ("'Schwarze Milch der Frühe trinken wir abends' – translate and comment on 'schwarze Milch'.", "'Black milk of dawn we drink in the evenings' – 'black milk' is an oxymoron evoking death and nourishment simultaneously."),
                ("'Wer, wenn ich schriee, hörte mich denn aus der Engel Ordnungen?' (Rilke)", "'Who, if I cried out, would hear me among the orders of angels?' – rhetorical question, subjunctive II 'schriee'"),
            ],
        ),
        _ex_arr(
            "Identify the poetic inversion",
            [
                (["Normal order:", "Wir trinken schwarze Milch abends.", "Inverted (Celan):", "Schwarze Milch der Frühe trinken wir abends."], "Celan places the object first ('Schwarze Milch') for rhythm and emphasis."),
            ],
        ),
        _ex_sp(
            "Poetry seminar discussion",
            ["Write a short poem (4-6 lines) in German using at least one oxymoron or surreal image.", "Read a Rilke poem aloud – what effect does the sound have beyond the meaning?", "Why might poetry be the highest challenge for a language learner?"],
        ),
    ],
}

LESSON_172 = {
    "title": "German in Global Contexts: International German",
    "level": "C2",
    "scenario": "international_german",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand German as a global language spoken in many countries and contexts",
        "Compare German in Germany, Austria, Switzerland, and diaspora communities",
        "Use German effectively in international professional and academic settings",
        "Discuss the role of German in the world and its future",
    ],
    "cultural_note": "German is spoken as a first language by approximately 100 million people in Germany, Austria, Switzerland, Luxembourg, Liechtenstein, and South Tyrol (Italy). German-speaking diaspora communities exist globally. In academia, German remains important in philosophy, science, and history.",
    "grammar_focus": _gex(
        "Austrian and Swiss German: Key Differences",
        "Austrian German (Österreichisches Deutsch) and Swiss German (Schweizerdeutsch) differ from Standard German in vocabulary, some grammar features, and pronunciation. At C2 level, awareness of these differences is expected.",
        "Austrian: 'Jänner' (Januar), 'heuer' (dieses Jahr), 'Erdapfel' (Kartoffel), 'Matura' (Abitur) / Swiss: 'Grüezi' (Guten Tag), 'Velo' (Fahrrad), 'das Tram' (die Straßenbahn), no ß (→ ss)",
        ["Austrian vocabulary: das Sackerl (Tüte), der Sessel (Stuhl), der Topfen (Quark), das Handy (das Mobiltelefon)", "Swiss conventions: ss instead of ß always, different article for some words", "Formal/written Swiss German is close to Standard German; spoken Swiss is a dialect"],
        ["In der Schweiz schreibt man 'Strasse' statt 'Straße'.", "In Österreich heißt das Abitur 'Matura'.", "Die Matura ist in Österreich das Pendant zum deutschen Abitur."],
    ),
    "dialogue": [
        _t("german", "Ich habe bemerkt, dass in der Schweiz 'ß' nicht verwendet wird.", "I noticed that in Switzerland 'ß' is not used."),
        _t("swiss", "Stimmt – wir schreiben immer 'ss', also 'Strasse' und 'gruss'.", "That's right – we always write 'ss', so 'Strasse' and 'gruss'."),
        _t("austrian", "Und in Österreich sagen wir 'Jänner' statt 'Januar' und 'heuer' für 'dieses Jahr'.", "And in Austria we say 'Jänner' instead of 'Januar' and 'heuer' for 'this year'."),
        _t("german", "Interessant. Sind das offizielle Varianten oder Dialekte?", "Interesting. Are these official variants or dialects?"),
        _t("swiss", "Offizielle Varianten – das österreichische und schweizerische Deutsch sind anerkannte Standardvarietäten.", "Official variants – Austrian and Swiss German are recognised standard varieties."),
        _t("austrian", "Genau. Der Duden listet österreichische und schweizerische Wörter eigens.", "Exactly. The Duden lists Austrian and Swiss words separately."),
        _t("german", "Also kein Hochdeutsch als einziger Standard?", "So Standard German is not the only standard?"),
        _t("swiss", "Das plurizentrische Modell: mehrere gleichwertige nationale Standardvarietäten.", "The pluricentric model: several equally valid national standard varieties."),
    ],
    "vocabulary_list": [
        _v("plurizentrisch", "pluricentric", "Das Deutsche ist eine plurizentrische Sprache."),
        _v("die Standardvarietät (-en)", "standard variety", "Österreichisches Deutsch ist eine Standardvarietät."),
        _v("die Matura", "school leaving exam (Austria/Switzerland)", "Die Matura entspricht dem Abitur."),
        _v("heuer (Austrian)", "this year (Austrian German)", "Heuer findet das Fest nicht statt."),
        _v("der Jänner (Austrian)", "January (Austrian German)", "Im Jänner beginnt das neue Semester."),
        _v("das Velo (Swiss)", "bicycle (Swiss German)", "Ich fahre mit dem Velo zur Arbeit."),
        _v("das Tram (Swiss/Austrian)", "tram / streetcar", "Das Tram fährt alle fünf Minuten."),
        _v("der Duden", "Duden (the standard German dictionary)", "Der Duden ist die maßgebliche Referenz."),
        _v("die Diaspora (-s)", "diaspora", "Die deutschsprachige Diaspora ist weltweit verteilt."),
        _v("anerkannt", "recognised / acknowledged", "Österreichisches Deutsch ist anerkannt."),
    ],
    "exercises": [
        _ex_mc(
            "German varieties: choose the correct answer",
            [
                ("In Swiss German writing, 'ß' is replaced by:", ["st", "sz", "ss", "z"], 2),
                ("'Jänner' is the Austrian German word for:", ["June", "January", "Year", "Winter"], 1),
                ("What does 'plurizentrisch' mean for the German language?", ["Only one standard", "Several equal national standard varieties", "Only dialects", "English loanwords"], 1),
            ],
        ),
        _ex_fib(
            "Match German variety to feature",
            ["In der Schweiz schreibt man '___ ' statt 'Straße'.", "In Österreich heißt das Abitur '___'.", "Das ___ Modell erkennt mehrere nationale Standards an."],
            ["Strasse", "Matura", "plurizentrische"],
        ),
        _ex_tr(
            "Translate and note variety differences",
            [
                ("I cycle to work. (Swiss German noun)", "Ich fahre mit dem Velo zur Arbeit."),
                ("This year the festival is not taking place. (Austrian)", "Heuer findet das Fest nicht statt."),
                ("In January the new semester begins. (Austrian)", "Im Jänner beginnt das neue Semester."),
            ],
        ),
        _ex_arr(
            "Order the description of German varieties",
            [
                (["Österreichisch", "Schweizerisch", "und", "Deutsch", "sind", "gleichwertige", "Standardvarietäten"], "Österreichisch, Schweizerisch und Deutsch sind gleichwertige Standardvarietäten."),
            ],
        ),
        _ex_sp(
            "German in the world",
            ["Discuss the advantages of German being a pluricentric language.", "What role does German play globally in science, philosophy, and international organisations?", "Have you encountered Austrian or Swiss German? What surprised you?"],
        ),
    ],
}

LESSON_173 = {
    "title": "Spontaneous Speech: Fillers, Hesitation, and Fluency",
    "level": "C2",
    "scenario": "fluency_training",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Use German hesitation markers and fillers naturally and appropriately",
        "Maintain fluent speech under pressure without reverting to L1 strategies",
        "Deploy repair strategies (Reparaturen) naturally in German",
        "Achieve prosodic naturalness in spontaneous German speech",
    ],
    "cultural_note": "All native speakers use fillers, hesitation markers, and self-repairs. Using German-specific fillers ('äh', 'ähm', 'also', 'na ja', 'ich meine', 'sozusagen') rather than English ones signals linguistic integration. C2 speakers manage these naturally without conscious effort.",
    "grammar_focus": _gex(
        "Spoken Fluency Devices in German",
        "German has specific fillers and repair strategies: 'äh/ähm' (hesitation), 'also' (so / well), 'na ja' (well), 'sozusagen' (so to speak), 'ich meine' (I mean), 'quasi' (sort of), 'wie soll ich sagen' (how shall I put it). These are different from written German.",
        "'Äh, also das ist, wie soll ich sagen, sozusagen ein kompliziertes Thema, na ja.'",
        ["Hesitation: äh, ähm (like 'er/um' in English)", "Fillers: also (so/well), na ja (well/I guess), nämlich (you see), sozusagen (so to speak)", "Repair: also nochmal / ich meine... / oder vielmehr... / beziehungsweise...", "Thinking: Moment mal... / Lass mich kurz nachdenken..."],
        ["'Ich finde das, also, sehr, äh, komplex, sozusagen.' (natural hesitation)", "'Also nochmal von vorne: ich meine damit...' (self-repair)", "'Wie soll ich das sagen... es ist so eine Art Paradox.' (search for word)"],
    ),
    "dialogue": [
        _t("interviewer", "Können Sie Ihren Beruf kurz beschreiben?", "Can you briefly describe your job?"),
        _t("candidate", "Also, äh, ich bin, wie soll ich sagen, eine Art Brücke zwischen Technik und Kommunikation.", "Well, er, I am, how shall I put it, a kind of bridge between technology and communication."),
        _t("interviewer", "Interessant. Was genau macht das aus?", "Interesting. What exactly does that consist of?"),
        _t("candidate", "Na ja, ich übersetze sozusagen technische Konzepte in verständliche Sprache. Also nochmal: ich erkläre komplizierte Dinge für ein breites Publikum.", "Well, I sort of translate technical concepts into understandable language. So to rephrase: I explain complex things to a broad audience."),
        _t("interviewer", "Und welche Fähigkeiten braucht man dafür?", "And what skills does one need for that?"),
        _t("candidate", "Ähm, Empathie natürlich – oder vielmehr, das Gespür dafür, was der andere schon weiß.", "Hm, empathy of course – or rather, the sense of what the other person already knows."),
        _t("interviewer", "Das klingt nach einer seltenen Fähigkeit.", "That sounds like a rare skill."),
        _t("candidate", "Naja, man lernt es. Mit der Zeit.", "Well, you learn it. Over time."),
    ],
    "vocabulary_list": [
        _v("sozusagen", "so to speak / as it were", "Es ist sozusagen ein Paradox."),
        _v("nämlich", "you see / namely / that is", "Das ist nämlich das Problem."),
        _v("oder vielmehr", "or rather / more precisely", "Ich meine das, oder vielmehr..."),
        _v("beziehungsweise (bzw.)", "respectively / or rather", "Er kam montags, bzw. dienstags."),
        _v("wie soll ich sagen", "how shall I put it", "Es ist, wie soll ich sagen, komplex."),
        _v("na ja", "well / I guess / kind of", "Na ja, es hat nicht perfekt geklappt."),
        _v("also", "so / well / anyway (discourse)", "Also, was sollen wir machen?"),
        _v("quasi", "sort of / as it were / quasi", "Er ist quasi mein Chef."),
        _v("das Gespür", "sense / feel / intuition", "Sie hat ein Gespür für Sprache."),
        _v("die Reparatur (-en)", "repair (linguistics)", "Selbstreparaturen sind in der Spontansprache normal."),
    ],
    "exercises": [
        _ex_fib(
            "Choose the natural German filler",
            ["___, äh, das ist schwierig zu erklären. (well)", "Es ist ___ ein Paradox. (so to speak)", "Oder ___, was ich meine ist... (or rather)"],
            ["Also", "sozusagen", "vielmehr"],
        ),
        _ex_mc(
            "Identify the fluency device",
            [
                ("'Also nochmal von vorne' – What type of spoken device is this?", ["Filler only", "Self-repair / restart", "Hesitation marker", "Discourse particle"], 1),
                ("'Wie soll ich das sagen' – What does this signal?", ["Certainty", "Disagreement", "Searching for the right word", "Changing the topic"], 2),
                ("'Na ja' in German is equivalent to:", ["Oh no", "Well / I guess", "Definitely", "Excuse me"], 1),
            ],
        ),
        _ex_tr(
            "Incorporate fluency devices",
            [
                ("'It's sort of a paradox.' (using sozusagen)", "Es ist sozusagen ein Paradox."),
                ("'Well, how shall I put it...' (using na ja + wie soll ich sagen)", "Na ja, wie soll ich das sagen..."),
                ("'Or rather, what I mean is...' (using oder vielmehr)", "Oder vielmehr, was ich meine ist..."),
            ],
        ),
        _ex_arr(
            "Order the natural response",
            [
                (["Also", "äh", "das", "ist", "sozusagen", "eine", "Art", "von", "Paradox", "wie", "soll", "ich", "sagen"], "Also, äh, das ist sozusagen eine Art von Paradox – wie soll ich sagen..."),
            ],
        ),
        _ex_sp(
            "Fluency in practice",
            ["Describe your job or studies for 2 minutes without preparation – use German fillers naturally.", "Practise self-repair: start a sentence, then correct yourself mid-way using 'oder vielmehr'.", "Record yourself speaking German for 3 minutes. How many English fillers did you use?"],
        ),
    ],
}

LESSON_174 = {
    "title": "Advanced German: Style, Voice, and Authenticity",
    "level": "C2",
    "scenario": "style_workshop",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Develop a distinctive personal style in written German",
        "Identify and emulate stylistic features of admired German writers",
        "Revise and improve written German texts for style, not just accuracy",
        "Understand what 'voice' means in writing and how to cultivate it",
    ],
    "cultural_note": "At C2 level, the goal shifts from correctness to style. German has a rich tradition of stylistic reflection – from Schiller's essays on style to contemporary writing guides. The question is no longer 'Is this correct?' but 'Is this good? Does it say what I want, in the way I want?'",
    "grammar_focus": _gex(
        "Stylistic Choices at C2",
        "Style is the sum of choices at every level: word choice (Wortwahl), sentence length and rhythm, the decision between nominalization and verb, active and passive, embedded and coordinate clauses. The same content can be expressed in an infinite number of ways.",
        "'Das Problem ist groß.' (flat) / 'Das Problem hat einen Umfang, der alle bisherigen Schätzungen übersteigt.' (elaborate) / 'Das Problem überwältigt uns.' (vivid)",
        ["Nominalization creates distance and formality; verbs create immediacy", "Short sentences create punch; long sentences create complexity", "Active creates agency; passive creates objectivity", "Abstract nouns vs concrete images: 'Freiheit' vs 'offene Tür'"],
        ["Flat: 'Die Situation war schwierig.' / Vivid: 'Die Situation fraß uns auf.'", "Formal: 'Eine Lösung wurde gefunden.' / Personal: 'Wir fanden eine Lösung.'", "Dense: 'Das von allen gefürchtete Scheitern' / Clear: 'Alle fürchteten, dass es scheitern würde.'"],
    ),
    "dialogue": [
        _t("writing_mentor", "Ich habe Ihren Text gelesen. Er ist korrekt – aber er hat keine Seele.", "I have read your text. It is correct – but it has no soul."),
        _t("writer", "Was fehlt ihm?", "What does it lack?"),
        _t("writing_mentor", "Stimme. Ich weiß nicht, wer dieser Text geschrieben hat.", "Voice. I don't know who wrote this text."),
        _t("writer", "Wie bekommt man eine Stimme?", "How does one develop a voice?"),
        _t("writing_mentor", "Durch Entscheidungen. Jedes Wort, das Sie wählen, ist ein Bekenntnis.", "Through choices. Every word you choose is a commitment."),
        _t("writer", "Also nicht einfach korrekt schreiben?", "So not simply write correctly?"),
        _t("writing_mentor", "Korrektheit ist Voraussetzung, nicht Ziel. Das Ziel ist: Wirkung.", "Correctness is a prerequisite, not a goal. The goal is: impact."),
        _t("writer", "Welche Wirkung will ich erzielen? Das muss ich zuerst wissen.", "What impact do I want to achieve? I need to know that first."),
    ],
    "vocabulary_list": [
        _v("die Stimme (stilistisch)", "voice (literary/stylistic)", "Jeder gute Autor hat eine unverwechselbare Stimme."),
        _v("die Wortwahl", "word choice / diction", "Wortwahl bestimmt den Ton."),
        _v("das Bekenntnis (-se)", "commitment / declaration", "Jede Stilentscheidung ist ein Bekenntnis."),
        _v("die Wirkung (-en)", "effect / impact", "Was ist die Wirkung dieses Satzes?"),
        _v("unverwechselbar", "unmistakable / distinctive", "Kafkas Stil ist unverwechselbar."),
        _v("die Seele (-n)", "soul", "Ein Text ohne Stimme hat keine Seele."),
        _v("die Voraussetzung (-en)", "prerequisite", "Korrektheit ist Voraussetzung."),
        _v("erzielen", "to achieve / attain", "Welche Wirkung wollen Sie erzielen?"),
        _v("übersteigen", "to exceed / surpass", "Das übersteigt alle Erwartungen."),
        _v("auffressen (colloquial figurative)", "to eat up / overwhelm (fig.)", "Die Angst frisst uns auf."),
    ],
    "exercises": [
        _ex_mc(
            "Style: choose the most vivid/effective version",
            [
                ("Which sentence is most vivid?", ["Das Problem ist groß.", "Das Problem hat eine erhebliche Größe.", "Das Problem frisst uns auf.", "Es gibt ein großes Problem."], 2),
                ("Which creates most immediacy?", ["Eine Entscheidung wurde getroffen.", "Es kam zu einer Entscheidung.", "Wir entschieden.", "Die Entscheidung erfolgte."], 2),
                ("Which is most formal/distant?", ["Wir haben das Problem gelöst.", "Das Problem wurde gelöst.", "Ich löste das Problem.", "Das Problem löste sich."], 1),
            ],
        ),
        _ex_fib(
            "Rewrite for style",
            ["Flat: 'Die Situation war schlecht.' → Vivid: 'Die Situation ___ uns auf.'", "Abstract: 'Es herrschte Freiheit.' → Concrete: 'Die Tür stand ___ offen.'", "Long: 'Das, von allen gefürchtete Scheitern' → Simple: 'Alle ___, dass es scheitern würde.'"],
            ["fraß", "weit", "fürchteten"],
        ),
        _ex_tr(
            "Translate and improve style",
            [
                ("The situation was very difficult. (Make it more vivid)", "Die Situation fraß uns auf. / Die Situation lastete wie Blei auf uns."),
                ("We found a solution. (Make it more formal/distant)", "Eine Lösung wurde gefunden. / Es gelang, eine Lösung zu erarbeiten."),
            ],
        ),
        _ex_arr(
            "Order from least to most stylistic impact",
            [
                (["Das Problem frisst uns auf.", "Das Problem ist schwierig.", "Es gibt ein Problem."], "Es gibt ein Problem. → Das Problem ist schwierig. → Das Problem frisst uns auf."),
            ],
        ),
        _ex_sp(
            "Style workshop",
            ["Take a paragraph you have written. Identify three choices that could be more vivid.", "Write the same idea in three different styles: journalistic, academic, literary.", "Read a paragraph from a German author you admire. What makes their style distinctive?"],
        ),
    ],
}

LESSON_175 = {
    "title": "German Language History and the Future of German",
    "level": "C2",
    "scenario": "language_history",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand the major stages of German language history",
        "Explain how modern German emerged from Old and Middle High German",
        "Discuss current changes and future directions of the German language",
        "Engage with the politics and sociology of the German language",
    ],
    "cultural_note": "German has a rich documented history from Old High German (8th–11th century) through Middle High German (11th–14th century) to Early New High German (Luther's Bible, 1534) and Modern German. The language continues to change: anglicisms, gender-neutral forms (Gendern), and digital registers all shape contemporary German.",
    "grammar_focus": _gex(
        "Historical Comparison: Old to Modern German",
        "Reading historical German reveals how dramatically the language has changed. The High German consonant shift (Lautverschiebung) is visible in contrasts with English: English 'water' vs. German 'Wasser', 'make' vs. 'machen'.",
        "OHG: 'ih queme' → MHG: 'ich kome' → NHG: 'ich komme' / Luther: 'Ein feste Burg ist unser Gott' (1524)",
        ["Consonant shift: p→ff/pf: English 'ship' → German 'Schiff'; t→ss/z: English 'eat' → German 'essen'", "Gender change: many nouns changed grammatical gender over centuries", "Luther's Bible: standardized spelling and vocabulary for much of the German-speaking world"],
        ["'Wasser' (German) ↔ 'water' (English) – same Proto-Germanic root, different consonant development", "Die Lautverschiebung trennt Oberdeutsch von Niederdeutsch und Englisch.", "Luther: 'dem Volk aufs Maul schauen' – write as people speak"],
    ),
    "dialogue": [
        _t("historian", "Die Sprache, die wir heute sprechen, würden die Menschen im Mittelalter kaum verstehen.", "The language we speak today would be barely understandable to medieval people."),
        _t("student", "Wann wurde Deutsch, wie wir es kennen, zur Standardsprache?", "When did German, as we know it, become the standard language?"),
        _t("historian", "Luthers Bibelübersetzung 1534 war entscheidend. Er wollte, wie er schrieb, 'dem Volk aufs Maul schauen'.", "Luther's Bible translation in 1534 was decisive. He wanted, as he wrote, to 'look at how ordinary people speak'."),
        _t("student", "Das ist erstaunlich – eine Bibelübersetzung als Grundlage des modernen Deutsch.", "That is astonishing – a Bible translation as the foundation of modern German."),
        _t("historian", "Ja. Und Goethe, Schiller und die Klassiker haben den Standard weiter geprägt.", "Yes. And Goethe, Schiller and the Classicists further shaped the standard."),
        _t("student", "Und die Zukunft? Was verändert Deutsch gerade am stärksten?", "And the future? What is changing German most right now?"),
        _t("historian", "Anglizismen, Gendern, und die Sprache des Internets – drei starke Kräfte.", "Anglicisms, gender-neutral forms, and internet language – three strong forces."),
        _t("student", "Wie reagiert die Gesellschaft darauf?", "How is society reacting to this?"),
    ],
    "vocabulary_list": [
        _v("die Lautverschiebung", "consonant shift (historical linguistics)", "Die hochdeutsche Lautverschiebung trennte Dialekte."),
        _v("das Althochdeutsch", "Old High German", "Althochdeutsch ist die älteste Form des Deutschen."),
        _v("das Mittelhochdeutsch", "Middle High German", "Mittelhochdeutsche Texte sind kaum verständlich."),
        _v("das Frühneuhochdeutsch", "Early New High German", "Luthers Bibel ist auf Frühneuhochdeutsch."),
        _v("prägen", "to shape / characterise", "Luther prägte die deutsche Schriftsprache."),
        _v("das Gendern", "gender-inclusive language", "Das Gendern ist politisch umstritten."),
        _v("die Anglisierung", "anglicisation", "Die Anglisierung des Deutschen schreitet voran."),
        _v("der Sprachpurismus", "linguistic purism", "Sprachpurismus lehnt Fremdwörter ab."),
        _v("die Bibelübersetzung (-en)", "Bible translation", "Luthers Bibelübersetzung ist ein Meilenstein."),
        _v("standardisieren", "to standardise", "Luther half, die Schriftsprache zu standardisieren."),
    ],
    "exercises": [
        _ex_mc(
            "Language history: choose the correct answer",
            [
                ("Luther's Bible (1534) was important because:", ["It created spoken German", "It standardised written German vocabulary and spelling", "It was the first German text", "It replaced all dialects"], 1),
                ("The High German consonant shift explains why:", ["German and English have no common roots", "German 'Wasser' and English 'water' share a root but differ in consonants", "German has more vowels than English", "German developed from Latin"], 1),
                ("'Gendern' refers to:", ["Grammatical gender in German", "Gender-neutral or inclusive language forms", "The German word for 'gender'", "Feminine word endings only"], 1),
            ],
        ),
        _ex_fib(
            "Language history: fill in",
            ["Luthers ___ von 1534 war grundlegend für die Standardisierung des Deutschen.", "Die hochdeutsche ___ erklärt den Unterschied zwischen 'Wasser' und 'water'.", "Englisch und Deutsch haben dieselben ___ Wurzeln."],
            ["Bibelübersetzung", "Lautverschiebung", "germanischen"],
        ),
        _ex_tr(
            "Translate historical and future language statements",
            [
                ("Luther wanted to write as ordinary people speak.", "Luther wollte 'dem Volk aufs Maul schauen'."),
                ("The High German consonant shift separates Upper German from Low German and English.", "Die hochdeutsche Lautverschiebung trennt das Oberdeutsche vom Niederdeutschen und Englischen."),
                ("Anglicisms, gender-neutral forms, and internet language are the three strongest current forces.", "Anglizismen, Gendern und Internetsprache sind die drei stärksten Kräfte der Gegenwart."),
            ],
        ),
        _ex_arr(
            "Order German language history chronologically",
            [
                (["Frühneuhochdeutsch (Luther, 1534)", "Althochdeutsch (8.-11. Jh.)", "Modernes Deutsch (ab 18. Jh.)", "Mittelhochdeutsch (11.-14. Jh.)"], "Althochdeutsch → Mittelhochdeutsch → Frühneuhochdeutsch → Modernes Deutsch"),
            ],
        ),
        _ex_sp(
            "Language history discussion",
            ["Why was Luther's Bible so important for German standardisation? Could one text do the same today?", "Do you think anglicisms enrich or threaten German? Give arguments for both sides.", "What changes to German in the last 20 years have you noticed as a learner?"],
        ),
    ],
}

LESSON_176 = {
    "title": "German Across Text Types: Genre Mastery",
    "level": "C2",
    "scenario": "genre_mastery",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Produce excellent German across all major text genres: academic, journalistic, literary, official, conversational",
        "Recognize genre conventions and apply them in writing and speech",
        "Adapt the same message to different genres and purposes",
        "Demonstrate complete communicative competence across German text types",
    ],
    "cultural_note": "Genre literacy – the ability to navigate multiple text types – is the defining feature of a fully educated speaker. In German, each genre (Wissenschaftstext, Feuilleton, Behördentext, literarischer Text, Alltagsgespräch) has its own vocabulary, syntax, and pragmatic conventions.",
    "grammar_focus": _gex(
        "Genre-Specific Grammar Choices",
        "Each genre uses grammar differently: Academic = nominalization + passive + hedging; Journalistic = active + clear structure + quotation; Official = fixed formulas + passive + modal; Literary = flexibility + deviation; Conversational = ellipsis + fillers + discourse particles.",
        "Same content in 5 genres: 'The meeting was cancelled / Die Sitzung fiel aus / Hiermit wird mitgeteilt, dass die Sitzung abgesagt wurde / Die Sitzung? Fällt aus.'",
        ["Academic: 'Im Rahmen der Untersuchung wurde festgestellt...'", "Official: 'Hiermit wird mitgeteilt, dass...'", "Literary: 'Die Sitzung, die niemand wollte, fiel endlich aus.'", "Conversational: 'Die Sitzung fällt aus, hab ich grad gehört.'"],
        ["Genre shifts require: vocabulary, syntax, register, and pragmatic adjustments", "The same writer must master all genres to be fully C2 literate"],
    ),
    "dialogue": [
        _t("editor", "Können Sie denselben Sachverhalt in vier verschiedenen Stilen schreiben?", "Can you write the same content in four different styles?"),
        _t("writer", "Als Aufgabe – natürlich. Welches Thema?", "As a task – of course. What topic?"),
        _t("editor", "Stau auf der Autobahn.", "Traffic jam on the motorway."),
        _t("writer", "Akademisch: 'Die Analyse der Verkehrsdaten zeigt signifikante Staubildung auf der BAB 3.'", "Academic: 'The analysis of traffic data shows significant congestion forming on the A3.'"),
        _t("editor", "Gut. Journalistisch?", "Good. Journalistic?"),
        _t("writer", "'Chaos auf der A3: 40 Kilometer Stau – Pendler stehen seit Stunden.'", "'Chaos on the A3: 40 kilometres of traffic – commuters stuck for hours.'"),
        _t("editor", "Sehr gut. Amtlich?", "Very good. Official?"),
        _t("writer", "'Hiermit wird bekanntgegeben, dass auf der BAB 3 aufgrund eines Unfalls mit einer Verzögerung von ca. 120 Minuten zu rechnen ist.'", "'It is hereby announced that a delay of approx. 120 minutes is to be expected on the A3 due to an accident.'"),
    ],
    "vocabulary_list": [
        _v("das Genre (-s)", "genre", "Jedes Genre hat seine eigenen Regeln."),
        _v("die Genrekompetenz", "genre literacy / competence", "Genrekompetenz ist ein C2-Merkmal."),
        _v("der Sachverhalt (Sachverhalte)", "matter / subject matter / state of affairs", "Beschreiben Sie den Sachverhalt korrekt."),
        _v("die Staubildung", "congestion formation / traffic jam forming", "Die Staubildung begann um 7 Uhr."),
        _v("bekanntgeben", "to announce / make known", "Es wird bekanntgegeben, dass..."),
        _v("signifikant", "significant", "Signifikante Unterschiede wurden festgestellt."),
        _v("adaptieren", "to adapt", "Den Stil adaptieren ist eine Kompetenz."),
        _v("der Pendler / die Pendlerin", "commuter", "Tausende Pendler sind betroffen."),
        _v("die Ellipse (-n)", "ellipsis / elliptical structure", "In der Alltagssprache sind Ellipsen normal."),
        _v("der Lesefluss", "readability / flow of reading", "Ein guter Stil fördert den Lesefluss."),
    ],
    "exercises": [
        _ex_fib(
            "Identify the genre of each sentence",
            ["'Hiermit wird mitgeteilt, dass die Sitzung abgesagt wurde.' → ___ Genre", "'Die Sitzung? Fällt aus.' → ___ Genre", "'Im Rahmen der Studie wurde festgestellt, dass...' → ___ Genre"],
            ["Official/bureaucratic", "Conversational (ellipsis)", "Academic"],
        ),
        _ex_mc(
            "Choose the genre-appropriate sentence",
            [
                ("You are writing a news headline. Which is most appropriate?", ["Im Rahmen der Sitzung wurden Beschlüsse gefasst.", "Sitzung: Wichtige Beschlüsse – was ändert sich jetzt?", "Hiermit wird bekanntgegeben, dass Beschlüsse gefasst wurden.", "Sitzung war, Beschlüsse wurden gemacht."], 1),
                ("You are writing an official notice. Which opening is correct?", ["Hey!", "Hiermit wird mitgeteilt, dass...", "Also, wir wollten mal sagen...", "Stellen Sie sich vor..."], 1),
                ("Literary style for a traffic jam:", ["40 km Stau auf A3.", "Die Autobahn schluckte uns, stundenlang.", "Hiermit wird ein Stau bekanntgegeben.", "Traffic jam analysis completed."], 1),
            ],
        ),
        _ex_tr(
            "Translate and adapt to the specified genre",
            [
                ("There is a traffic jam on the motorway. (Academic)", "Auf der Bundesautobahn konnte eine signifikante Staubildung festgestellt werden."),
                ("There is a traffic jam on the motorway. (Conversational)", "Auf der Autobahn ist totaler Stau – steh da seit einer Stunde."),
                ("There is a traffic jam on the motorway. (Official)", "Hiermit wird bekanntgegeben, dass auf der BAB mit erheblichen Verzögerungen zu rechnen ist."),
            ],
        ),
        _ex_arr(
            "Match sentence to genre",
            [
                (["'Die Daten belegen eine Zunahme.'", "'Die Zahlen gehen hoch!'", "'Hiermit wird eine Zunahme bekanntgegeben.'", "'Die Zahlen? Deutlich gestiegen.'"], ["Academic", "Journalistic", "Official", "Conversational"]),
            ],
        ),
        _ex_sp(
            "Genre mastery practice",
            ["Take one event and write it in academic, journalistic, official, and literary styles.", "Explain to a partner the grammar and vocabulary differences between two genres.", "Discuss: Which German genre do you find most challenging? Why?"],
        ),
    ],
}

LESSON_177 = {
    "title": "Intercultural Communication: German and the World",
    "level": "C2",
    "scenario": "intercultural_competence",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Navigate intercultural communication situations in German with full competence",
        "Understand and manage cultural mismatches in German professional contexts",
        "Reflect critically on cultural assumptions embedded in language",
        "Act as a cultural mediator between German-speaking and other cultures",
    ],
    "cultural_note": "Intercultural competence at C2 means more than knowing German culture – it means being able to reflect on cultural difference, navigate misunderstandings, and serve as a bridge between cultures. This meta-cultural awareness is the final frontier of language mastery.",
    "grammar_focus": _gex(
        "Hedged Cultural Generalizations",
        "Discussing culture requires careful hedging to avoid stereotyping. German grammar provides the tools: Konjunktiv II for tentativeness, modal adverbs (tendenziell, neigt dazu), impersonal constructions (es wird angenommen), and explicit attribution (laut Umfragen / nach allgemeiner Wahrnehmung).",
        "'Deutsche neigen tendenziell dazu, direkt zu kommunizieren.' vs. 'Deutsche sind direkt.' (overgeneralization)",
        ["Hedging: Deutsche neigen dazu... / Es wird oft wahrgenommen, dass... / Laut Studien...", "Attribution: Nach allgemeiner Einschätzung... / Einer verbreiteten Ansicht zufolge...", "Qualification: Dies trifft nicht auf alle zu... / Es gibt natürlich Ausnahmen..."],
        ["Deutsche Kommunikation wird oft als direkter wahrgenommen als die in vielen anderen Kulturen.", "Es lässt sich beobachten, dass Pünktlichkeit in Deutschland einen hohen Stellenwert hat.", "Diese Beobachtungen sind natürlich verallgemeinert und treffen nicht auf alle zu."],
    ),
    "dialogue": [
        _t("mediator", "In unserem Team arbeiten Deutsche, Japaner und Brasilianer. Es gibt Kommunikationsprobleme.", "In our team we have Germans, Japanese and Brazilians. There are communication problems."),
        _t("consultant", "Was beobachten Sie genau?", "What specifically do you observe?"),
        _t("mediator", "Die deutschen Kollegen sagen direkt, wenn etwas nicht funktioniert. Das wird manchmal als unhöflich empfunden.", "The German colleagues say directly when something is not working. This is sometimes perceived as impolite."),
        _t("consultant", "Ja, direkte Kommunikation wird in Deutschland tendenziell als Respekt gewertet.", "Yes, direct communication tends to be valued as respect in Germany."),
        _t("mediator", "Wie kann ich das dem Team erklären?", "How can I explain that to the team?"),
        _t("consultant", "Zeigen Sie, dass Direktheit kein Angriff ist, sondern Effizienz und Respekt vor der Zeit anderer.", "Show that directness is not an attack, but efficiency and respect for others' time."),
        _t("mediator", "Das hilft. Und umgekehrt – wie erkläre ich den deutschen Kollegen indirekte Kommunikation?", "That helps. And vice versa – how do I explain indirect communication to the German colleagues?"),
        _t("consultant", "Als ein System, das Harmonie und Beziehungspflege priorisiert – nicht als Umgehung der Wahrheit.", "As a system that prioritises harmony and relationship maintenance – not as avoidance of truth."),
    ],
    "vocabulary_list": [
        _v("die interkulturelle Kompetenz", "intercultural competence", "Interkulturelle Kompetenz ist heute unerlässlich."),
        _v("die Direktheit", "directness", "Direktheit wird in Deutschland geschätzt."),
        _v("die Beziehungspflege", "relationship maintenance", "Beziehungspflege hat in manchen Kulturen hohe Priorität."),
        _v("tendenziell", "tendentially / as a tendency", "Deutsche kommunizieren tendenziell direkter."),
        _v("wahrnehmen", "to perceive", "Das wird oft als unhöflich wahrgenommen."),
        _v("der Kulturmittler / die Kulturmittlerin", "cultural mediator / broker", "Sie arbeitet als Kulturmittlerin."),
        _v("die Verallgemeinerung (-en)", "generalization", "Verallgemeinerungen sind mit Vorsicht zu behandeln."),
        _v("priorisieren", "to prioritize", "Manche Kulturen priorisieren Harmonie."),
        _v("die Umgehung (-en)", "avoidance / bypass", "Indirektheit ist keine Umgehung der Wahrheit."),
        _v("unerlässlich", "indispensable / essential", "Empathie ist unerlässlich für interkulturelle Arbeit."),
    ],
    "exercises": [
        _ex_fib(
            "Hedge the cultural generalization",
            ["'Deutsche sind direkt.' → Deutsche ___ dazu, direkt zu kommunizieren.", "'In Japan ist man höflich.' → In Japan ___ Höflichkeit einen hohen ___ haben.", "Das ___ nicht auf alle zu – es gibt natürlich Ausnahmen."],
            ["neigen", "scheint / Stellenwert", "trifft"],
        ),
        _ex_mc(
            "Intercultural communication: choose the correct response",
            [
                ("A German colleague gives very direct criticism. The best interpretation is:", ["They are being rude", "They are showing respect and efficiency", "They dislike you", "They are stressed"], 1),
                ("How should you hedge cultural generalizations?", ["State them as absolute facts", "Use 'tendenziell', 'neigen dazu', 'laut Studien'", "Avoid them entirely", "Use only stereotypes"], 1),
                ("'Beziehungspflege' in cultural context means:", ["Maintaining equipment", "Relationship maintenance", "Formal negotiations", "HR management"], 1),
            ],
        ),
        _ex_tr(
            "Translate with appropriate hedging",
            [
                ("German communication tends to be perceived as more direct than in many other cultures.", "Deutsche Kommunikation wird tendenziell als direkter wahrgenommen als in vielen anderen Kulturen."),
                ("These observations are generalized and do not apply to everyone.", "Diese Beobachtungen sind natürlich verallgemeinert und treffen nicht auf alle zu."),
            ],
        ),
        _ex_arr(
            "Reconstruct the hedged generalization",
            [
                (["Deutsche", "neigen", "tendenziell", "dazu", "direkt", "zu", "kommunizieren"], "Deutsche neigen tendenziell dazu, direkt zu kommunizieren."),
            ],
        ),
        _ex_sp(
            "Intercultural mediation practice",
            ["Explain a cultural misunderstanding you have experienced or observed.", "Role-play: mediate a conflict between two colleagues from different cultural backgrounds.", "Discuss: Is there a risk of over-explaining cultural difference? Where is the line?"],
        ),
    ],
}

LESSON_178 = {
    "title": "Advanced Speaking: Debates, Panels, and Public Discourse",
    "level": "C2",
    "scenario": "public_discourse",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Participate fluently and effectively in formal German debates and panel discussions",
        "Use turn-taking strategies, interruptions, and floor-holding at native level",
        "Respond to unexpected questions spontaneously in formal German",
        "Chair a discussion or moderate a debate in German",
    ],
    "cultural_note": "German public discourse – in TV talk shows (Talkshows like Anne Will or Hart aber Fair), academic panels (Podiumsdiskussionen), and parliamentary debates – follows specific conventions for turn-taking, interruption, and rhetorical practice. Mastering these marks full integration into German public life.",
    "grammar_focus": _gex(
        "Turn-Taking and Floor Management in German",
        "German floor management uses specific phrases to take the floor, hold it, interrupt, and yield. These are different from English and must be learned as chunks.",
        "'Wenn ich da kurz einhaken darf...' (If I may interject...) / 'Das führt mich zu einem weiteren Punkt...' (That leads me to another point...) / 'Dazu möchte ich noch ergänzen...' (I would like to add to that...)",
        ["Taking the floor: Ich möchte nur kurz... / Dazu hätte ich eine Frage. / Wenn ich da einhaken darf...", "Holding the floor: Lassen Sie mich ausführen... / Ich bin gleich fertig. / Einen Moment noch...", "Yielding: Das Wort hat... / Ich gebe gerne ab. / Was meinen Sie dazu?"],
        ["Wenn ich da kurz einhaken darf – das sehe ich etwas anders.", "Lassen Sie mich das kurz ausführen, dann gebe ich gerne das Wort weiter.", "Ich stimme im Grundsatz zu, möchte aber einen Aspekt ergänzen."],
    ),
    "dialogue": [
        _t("moderator", "Ich eröffne die Diskussion. Herr Klein, bitte.", "I open the discussion. Herr Klein, please."),
        _t("panelist_a", "Danke. Ich möchte zunächst betonen, dass wirtschaftliches Wachstum und Nachhaltigkeit kein Widerspruch sind.", "Thank you. I would first like to emphasize that economic growth and sustainability are not a contradiction."),
        _t("panelist_b", "Wenn ich da kurz einhaken darf – die empirischen Daten widersprechen dieser These.", "If I may interject briefly – the empirical data contradicts this thesis."),
        _t("panelist_a", "Lassen Sie mich ausführen, dann stehe ich für Fragen gerne zur Verfügung.", "Let me elaborate, then I am happy to take questions."),
        _t("moderator", "Bitte, Herr Klein.", "Please, Herr Klein."),
        _t("panelist_a", "Die Entkopplung von BIP und CO2-Emissionen zeigt: Wachstum kann grün sein.", "The decoupling of GDP and CO2 emissions shows: growth can be green."),
        _t("panelist_b", "Ich stimme im Grundsatz zu, möchte aber einen kritischen Aspekt ergänzen.", "I agree in principle, but would like to add a critical aspect."),
        _t("moderator", "Frau Schmidt – bitte.", "Frau Schmidt – please."),
    ],
    "vocabulary_list": [
        _v("einhaken (in eine Debatte)", "to interject / hook in", "Wenn ich kurz einhaken darf..."),
        _v("ausführen", "to elaborate / develop (a point)", "Lassen Sie mich das kurz ausführen."),
        _v("ergänzen", "to add / supplement", "Ich möchte einen Aspekt ergänzen."),
        _v("im Grundsatz", "in principle", "Im Grundsatz stimme ich zu."),
        _v("zur Verfügung stehen", "to be available", "Ich stehe für Fragen zur Verfügung."),
        _v("das BIP (Bruttoinlandsprodukt)", "GDP (gross domestic product)", "Das BIP wächst."),
        _v("die Entkopplung (-en)", "decoupling", "Die Entkopplung von Wachstum und Emissionen."),
        _v("eröffnen", "to open / launch", "Der Moderator eröffnet die Diskussion."),
        _v("der Widerspruch (Widersprüche)", "contradiction / conflict", "Das ist kein Widerspruch."),
        _v("betonen", "to emphasize", "Ich möchte betonen, dass..."),
    ],
    "exercises": [
        _ex_fib(
            "Complete the floor-management phrases",
            ["Wenn ich da kurz ___ darf – ich sehe das etwas anders.", "Lassen Sie mich das kurz ___, dann gebe ich das Wort weiter.", "Ich stimme im ___ zu, möchte aber einen Aspekt ___."],
            ["einhaken", "ausführen", "Grundsatz / ergänzen"],
        ),
        _ex_mc(
            "Turn-taking: choose the correct phrase",
            [
                ("To politely interrupt a speaker, you say:", ["Halt! Falsch!", "Wenn ich da kurz einhaken darf...", "Das ist falsch!", "Sie irren sich."], 1),
                ("To hold the floor and ask for time to finish, you say:", ["Ich bin gleich fertig, einen Moment noch.", "Nein, hören Sie auf.", "Das interessiert mich nicht.", "Ich weiß nicht."], 0),
                ("To hand the floor to another speaker, you say:", ["Weiter!", "Ich gebe gerne das Wort weiter.", "Hören Sie auf!", "Bitte nicht!"], 1),
            ],
        ),
        _ex_tr(
            "Translate floor-management phrases",
            [
                ("If I may interject briefly – I see that slightly differently.", "Wenn ich da kurz einhaken darf – ich sehe das etwas anders."),
                ("I agree in principle, but would like to add a critical point.", "Ich stimme im Grundsatz zu, möchte aber einen kritischen Punkt ergänzen."),
                ("Let me elaborate, then I am happy to take questions.", "Lassen Sie mich das ausführen, dann stehe ich für Fragen gerne zur Verfügung."),
            ],
        ),
        _ex_arr(
            "Order the debate exchange",
            [
                (["Wenn ich kurz einhaken darf", "Lassen Sie mich ausführen", "Im Grundsatz stimme ich zu aber", "Das Wort hat Frau Schmidt"], "Wenn ich kurz einhaken darf → Lassen Sie mich ausführen → Im Grundsatz stimme ich zu aber → Das Wort hat Frau Schmidt"),
            ],
        ),
        _ex_sp(
            "Panel discussion practice",
            ["Stage a 10-minute panel discussion on any controversial topic using all floor-management phrases.", "Practise interrupting politely three times in a debate.", "Chair a discussion: ensure all participants can speak and manage time."],
        ),
    ],
}

LESSON_179 = {
    "title": "The German Mind: Philosophy of Language and Thought",
    "level": "C2",
    "scenario": "philosophy_of_language",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Engage with philosophical questions about the relationship between language and thought",
        "Understand Humboldt's theory of language as world-view (Weltansicht)",
        "Discuss Wittgenstein's language philosophy in German",
        "Reflect on how learning German has changed your thinking",
    ],
    "cultural_note": "Wilhelm von Humboldt (1767–1835) argued that each language embodies a unique worldview (Weltansicht) and that learning a new language means acquiring a new perspective on reality. This idea, radical in his time, resonates deeply with the experience of advanced language learners.",
    "grammar_focus": _gex(
        "Philosophical Language: Gerunds, Abstract Nouns, Infinitival Clauses",
        "Philosophical German uses infinitival clauses ('Zu denken bedeutet...), gerundial nouns (Das Denken, Das Sprechen, Das Verstehen), and abstract noun chains to express complex conceptual relationships.",
        "'Sprechen und Denken sind untrennbar.' / 'Das Denken vollzieht sich in der Sprache.' / 'Zu verstehen heißt, in der Sprache zu Hause zu sein.'",
        ["Infinitival nouns: Das Sprechen, Das Schweigen, Das Verstehen, Das Bedeuten", "Infinitival clauses: 'Zu denken bedeutet...' / 'Sprachlos zu sein heißt...'", "Abstract relationships: Sprache als... / Denken durch... / Welt im Licht der Sprache"],
        ["Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt. (Wittgenstein)", "Die Sprache ist das Haus des Seins. (Heidegger)", "Eine neue Sprache zu lernen bedeutet, eine neue Seele zu bekommen. (Tschechisches Sprichwort)"],
    ),
    "dialogue": [
        _t("philosopher", "Humboldt sagte: Jede Sprache ist eine eigene Weltansicht.", "Humboldt said: Every language is its own worldview."),
        _t("student", "Das habe ich tatsächlich erfahren – als ich anfing, auf Deutsch zu träumen.", "I have actually experienced that – when I began dreaming in German."),
        _t("philosopher", "Das ist ein Zeichen der tiefen Verankerung. Aber es geht noch tiefer.", "That is a sign of deep anchoring. But it goes even deeper."),
        _t("student", "Inwiefern?", "In what way?"),
        _t("philosopher", "Wittgenstein schrieb: 'Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt.'", "Wittgenstein wrote: 'The limits of my language mean the limits of my world.'"),
        _t("student", "Also erweitert jede neue Sprache die eigene Welt.", "So every new language expands one's own world."),
        _t("philosopher", "Genau. Und das ist nicht Metapher – das ist Kognitionswissenschaft.", "Exactly. And that is not a metaphor – that is cognitive science."),
        _t("student", "Dann ist Deutschlernen auch Selbsterweiterung.", "Then learning German is also self-expansion."),
    ],
    "vocabulary_list": [
        _v("die Weltansicht (-en)", "worldview (Humboldt)", "Jede Sprache trägt eine eigene Weltansicht."),
        _v("die Verankerung (-en)", "anchoring / rootedness", "Tiefe Verankerung zeigt sich im Träumen."),
        _v("das Schweigen", "silence (as noun)", "Das Schweigen sagt oft mehr als Worte."),
        _v("die Kognitionswissenschaft", "cognitive science", "Kognitionswissenschaft bestätigt Humboldts Intuition."),
        _v("untrennbar", "inseparable", "Denken und Sprache sind untrennbar."),
        _v("die Selbsterweiterung", "self-expansion", "Sprachenlernen ist Selbsterweiterung."),
        _v("vollziehen (sich)", "to take place / be enacted", "Denken vollzieht sich in der Sprache."),
        _v("das Haus des Seins", "the house of being (Heidegger)", "Heidegger nennt Sprache das Haus des Seins."),
        _v("die Grenze (-n)", "limit / boundary", "Die Grenzen meiner Sprache."),
        _v("träumen (auf Deutsch)", "to dream (in German)", "Auf Deutsch träumen ist ein Zeichen tiefer Kompetenz."),
    ],
    "exercises": [
        _ex_mc(
            "Philosophy of language: match to philosopher",
            [
                ("'Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt.' – Who said this?", ["Humboldt", "Heidegger", "Wittgenstein", "Kant"], 2),
                ("'Die Sprache ist das Haus des Seins.' – Who said this?", ["Wittgenstein", "Humboldt", "Nietzsche", "Heidegger"], 3),
                ("Humboldt's concept of Weltansicht means:", ["One standard global language", "Each language embodies a unique worldview", "Grammar is universal", "Words have no meaning"], 1),
            ],
        ),
        _ex_fib(
            "Complete philosophical sentences",
            ["Die ___ meiner Sprache bedeuten die Grenzen meiner Welt.", "Das Denken ___ sich in der Sprache.", "Sprache ist nicht nur Kommunikation – sie ist ___."],
            ["Grenzen", "vollzieht", "Weltansicht"],
        ),
        _ex_tr(
            "Translate philosophical statements",
            [
                ("The limits of my language mean the limits of my world.", "Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt."),
                ("Thinking takes place in language.", "Das Denken vollzieht sich in der Sprache."),
                ("Learning a new language means acquiring a new soul.", "Eine neue Sprache zu lernen bedeutet, eine neue Seele zu bekommen."),
            ],
        ),
        _ex_arr(
            "Reconstruct Wittgenstein's quote",
            [
                (["Die", "Grenzen", "meiner", "Sprache", "bedeuten", "die", "Grenzen", "meiner", "Welt"], "Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt."),
            ],
        ),
        _ex_sp(
            "Philosophy of language discussion",
            ["Has learning German changed the way you think? Give a specific example.", "Do you agree with Wittgenstein that language limits thought? Or can we think beyond words?", "What concept exists in German that cannot be fully expressed in your native language?"],
        ),
    ],
}

LESSON_180 = {
    "title": "C2 Grand Finale: Language as Life",
    "level": "C2",
    "scenario": "grand_finale",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Demonstrate complete mastery of German language at the C2 level",
        "Integrate all skills – reading, writing, speaking, listening – in a capstone task",
        "Reflect on the journey from learner to near-native speaker",
        "Celebrate and commit to a lifelong relationship with the German language",
    ],
    "cultural_note": "Reaching C2 in German is one of the most demanding language achievements in the world. German's complexity – its grammar, its philosophical depth, its rich literary tradition, its dialect variety, its ongoing change – make it a language that rewards a lifetime of engagement. The end of this course is not the end of the journey: it is the beginning of living in German.",
    "grammar_focus": _gex(
        "C2: The Full Toolkit",
        "At C2 level you command every grammatical structure of German: all tenses, moods, aspects, passive forms, complex syntax, all registers, pragmatic precision, and stylistic mastery. This lesson reviews the most sophisticated constructions.",
        "Das von Fachleuten lange als unlösbar geltende, nun jedoch endlich angegangene Problem zeigt: Wer hartnäckig bleibt, dem öffnen sich auch die schwersten Türen.",
        ["Stacked participials: 'das von X lange als Y geltende, nun als Z anerkannte Problem'", "Nested counterfactuals: 'Hätte man früher gehandelt, wäre das Problem kleiner geblieben, als es nun ist.'", "Full rhetorical toolkit: anaphora, antithesis, climax, rhetorical question, metaphor, irony"],
        ["Die Sprache ist nicht unser Werkzeug. Wir sind ihr Werkzeug.", "Wer eine Sprache wirklich beherrscht, hat nicht eine Sprache gelernt. Er hat eine Welt gewonnen.", "Ende und Anfang: Das Wichtigste kommt noch."],
    ),
    "dialogue": [
        _t("mentor", "Sie haben alle 180 Stunden absolviert. Was sagen Sie dazu?", "You have completed all 180 hours. What do you say to that?"),
        _t("graduate", "Ich denke an den Anfang – 'Hallo, ich heiße...' – und jetzt führe ich dieses Gespräch.", "I think of the beginning – 'Hello, my name is...' – and now I am having this conversation."),
        _t("mentor", "Was hat sich am stärksten verändert?", "What has changed most strongly?"),
        _t("graduate", "Ich denke anders. Auf Deutsch zu denken hat neue Räume in mir geöffnet.", "I think differently. Thinking in German has opened new spaces within me."),
        _t("mentor", "Das ist die tiefste Form des Spracherwerbs. Was kommt als nächstes?", "That is the deepest form of language acquisition. What comes next?"),
        _t("graduate", "Lesen, schreiben, sprechen – täglich. Die Sprache lebendig halten.", "Reading, writing, speaking – daily. Keeping the language alive."),
        _t("mentor", "Und wenn Sie in zwanzig Jahren zurückblicken?", "And when you look back in twenty years?"),
        _t("graduate", "Ich werde sagen: Deutsch lernen war eine der besten Entscheidungen meines Lebens.", "I will say: Learning German was one of the best decisions of my life."),
    ],
    "vocabulary_list": [
        _v("absolvieren", "to complete / finish", "Er hat den Kurs erfolgreich absolviert."),
        _v("der Spracherwerb", "language acquisition", "Tiefer Spracherwerb verändert das Denken."),
        _v("lebendig halten", "to keep alive", "Eine Sprache lebendig halten erfordert tägliche Übung."),
        _v("zurückblicken", "to look back", "Wenn ich zurückblicke, sehe ich den Fortschritt."),
        _v("hartnäckig", "persistent / tenacious", "Wer hartnäckig bleibt, erreicht das Ziel."),
        _v("der Raum (Räume)", "space / room", "Neue Räume im Denken öffnen sich.", ),
        _v("gewinnen", "to gain / win", "Eine neue Sprache: eine neue Welt gewinnen."),
        _v("das Werkzeug (-e)", "tool", "Die Sprache ist nicht unser Werkzeug."),
        _v("beherrschen", "to master / command", "Eine Sprache wirklich beherrschen."),
        _v("der Spracherwerb", "language acquisition", "Tiefgreifender Spracherwerb ist transformativ."),
    ],
    "exercises": [
        _ex_fib(
            "Grand finale fill-in",
            ["Das von Experten lange als unlösbar ___ Problem wurde nun endlich angegangen. (gelten als / Partizip I)", "Hätte man früher gehandelt, ___ das Problem kleiner ___ (bleiben – Konjunktiv II Plusquamperfekt).", "Wer eine Sprache wirklich ___, hat eine Welt ___."],
            ["geltende", "wäre / geblieben", "beherrscht / gewonnen"],
        ),
        _ex_mc(
            "C2 grand final review",
            [
                ("'Die Sprache ist nicht unser Werkzeug. Wir sind ihr Werkzeug.' – What rhetorical device?", ["Anaphora", "Antithesis / Paradox", "Tricolon", "Hyperbole"], 1),
                ("Which is the most grammatically complex sentence?", ["Das ist ein Problem.", "Das Problem ist schwer.", "Das von Experten lange als unlösbar geltende Problem dürfte sich lösen lassen.", "Es gibt ein schweres Problem."], 2),
                ("'Hätte man früher gehandelt, wäre das Problem kleiner geblieben.' – What is this?", ["Simple past", "Konjunktiv II counterfactual in the past", "Konjunktiv I reported speech", "Future conditional"], 1),
            ],
        ),
        _ex_tr(
            "C2 synthesis: final translation challenge",
            [
                ("Whoever masters a language has not learned a language. They have gained a world.", "Wer eine Sprache wirklich beherrscht, hat nicht eine Sprache gelernt. Er hat eine Welt gewonnen."),
                ("The problem, long considered unsolvable by experts, is now finally being addressed.", "Das von Experten lange als unlösbar geltende Problem wird nun endlich angegangen."),
                ("Learning German was one of the best decisions of my life.", "Deutsch zu lernen war eine der besten Entscheidungen meines Lebens."),
            ],
        ),
        _ex_arr(
            "Final C2 sentence",
            [
                (["Wer", "hartnäckig", "bleibt", "dem", "öffnen", "sich", "auch", "die", "schwersten", "Türen"], "Wer hartnäckig bleibt, dem öffnen sich auch die schwersten Türen."),
            ],
        ),
        _ex_sp(
            "Grand finale speaking tasks",
            ["Give a 5-minute speech on what German means to you – use all registers and rhetorical devices.", "Write a 200-word Feuilleton on the experience of learning German to C2 level.", "Share: What German word, phrase, or text will you carry with you forever?"],
        ),
    ],
}
'''

for num in list(range(166, 171)) + list(range(171, 181)):
    tag = f"LESSON_{num}"
    if tag in existing:
        print(f"SKIP {tag} already exists")
        APPEND = re.sub(rf"\nLESSON_{num}\s*=.*?(?=\nLESSON_|\Z)", "", APPEND, flags=re.DOTALL)

SEEDS.write_text(src + APPEND, encoding="utf-8")

verify = SEEDS.read_text(encoding="utf-8")
found = sorted(set(re.findall(r"^(LESSON_\d+)\s*=", verify, re.MULTILINE)),
               key=lambda x: int(x.split("_")[1]))
print(f"Total lessons: {len(found)}, range: {found[0]}-{found[-1]}")

# Count by level
content = verify
levels = {}
for m in re.finditer(r'^LESSON_\d+\s*=\s*\{[^}]*?"level":\s*"([^"]+)"', content, re.MULTILINE | re.DOTALL):
    lvl = m.group(1)
    levels[lvl] = levels.get(lvl, 0) + 1
print("Lessons by level:", levels)

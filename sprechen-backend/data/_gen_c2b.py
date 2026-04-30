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

LESSON_156 = {
    "title": "German Collocations and Lexical Chunks",
    "level": "C2",
    "scenario": "vocabulary_mastery",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Master high-frequency German collocations (verb + noun, adjective + noun)",
        "Use prepositional collocations accurately without translation interference",
        "Identify and correct collocational errors typical of advanced learners",
        "Build a mental lexicon of chunks rather than isolated words",
    ],
    "cultural_note": "Native German speakers store language in chunks (lexical units) rather than as individual words combined by rules. Learning collocations – the natural word partnerships in German – is what separates advanced learners from native-like speakers.",
    "grammar_focus": _gex(
        "Common German Collocations",
        "Collocations are fixed word partnerships. Getting them wrong is the most common sign of a non-native speaker even at C1/C2 level. Examples: eine Entscheidung treffen (NOT machen), einen Fehler begehen (NOT machen in formal contexts), Verständnis aufbringen.",
        "'eine Entscheidung treffen' (to make a decision) / 'eine Rolle spielen' (to play a role) / 'Interesse wecken' (to arouse interest)",
        ["Verb + Noun: Rücksicht nehmen, Abstand halten, Einfluss nehmen, Verantwortung übernehmen", "Adjective + Noun: weitreichende Konsequenzen, tiefgreifende Veränderungen, nachhaltige Wirkung", "Preposition: im Hinblick auf, im Rahmen von, in Bezug auf, angesichts + Genitiv"],
        ["Das spielt eine entscheidende Rolle.", "Wir müssen Rücksicht auf die Umwelt nehmen.", "Die Reform hat weitreichende Konsequenzen."],
    ),
    "dialogue": [
        _t("native", "Du hast geschrieben: 'eine Entscheidung machen'. Das sagen wir nicht.", "You wrote: 'make a decision'. We don't say that."),
        _t("learner", "Was sagt man dann?", "What do you say instead?"),
        _t("native", "'Eine Entscheidung treffen'. 'Treffen' ist die richtige Kollokation.", "'Make a decision'. 'Treffen' is the correct collocation."),
        _t("learner", "Und 'einen Fehler machen'?", "And 'make a mistake'?"),
        _t("native", "Das geht – aber formeller ist 'einen Fehler begehen' oder 'einen Fehler unterlaufen lassen'.", "That works – but more formal is 'commit a mistake' or 'let a mistake occur'."),
        _t("learner", "Und Einfluss – 'Einfluss haben' oder 'Einfluss nehmen'?", "And influence – 'have influence' or 'take influence'?"),
        _t("native", "Beides, aber mit Nuance: 'Einfluss haben' = passiv. 'Einfluss nehmen' = aktiv/intentional.", "Both, but with nuance: 'have influence' = passive. 'Take influence' = active/intentional."),
        _t("learner", "Das sind die Feinheiten, die man nur durch viel Lesen lernt.", "Those are the subtleties you only learn through a lot of reading."),
    ],
    "vocabulary_list": [
        _v("eine Entscheidung treffen", "to make a decision", "Sie traf eine schwierige Entscheidung."),
        _v("Rücksicht nehmen auf", "to show consideration for / to be mindful of", "Bitte nimm Rücksicht auf deine Mitmenschen."),
        _v("Einfluss nehmen auf", "to exert influence on", "Er nahm Einfluss auf die Entscheidung."),
        _v("Verantwortung übernehmen", "to take responsibility", "Er übernahm die Verantwortung für den Fehler."),
        _v("weitreichend", "far-reaching", "Die Entscheidung hat weitreichende Folgen."),
        _v("tiefgreifend", "profound / deep-reaching", "Eine tiefgreifende Veränderung ist nötig."),
        _v("nachhaltig", "sustainable / lasting", "Eine nachhaltige Wirkung erzielen."),
        _v("angesichts (+ Genitiv)", "in view of / given", "Angesichts der Lage müssen wir handeln."),
        _v("im Hinblick auf", "with regard to / in view of", "Im Hinblick auf die Zukunft planen."),
        _v("begehen", "to commit (error, crime)", "Einen Fehler / eine Straftat begehen."),
    ],
    "exercises": [
        _ex_fib(
            "Complete with the correct collocation verb",
            ["Er ___ eine wichtige Entscheidung. (treffen)", "Wir müssen Rücksicht auf andere ___. (nehmen)", "Die Reform hat weitreichende Konsequenzen ___ (haben → zeigt / hat / bringt)."],
            ["traf", "nehmen", "gehabt"],
        ),
        _ex_mc(
            "Choose the correct collocation",
            [
                ("'To play a role' in German:", ["eine Rolle haben", "eine Rolle spielen", "eine Rolle tun", "eine Rolle nehmen"], 1),
                ("'To arouse interest' in German:", ["Interesse machen", "Interesse haben", "Interesse wecken", "Interesse nehmen"], 2),
                ("'Far-reaching consequences' in German:", ["weite Konsequenzen", "weitreichende Konsequenzen", "große Konsequenzen", "hohe Konsequenzen"], 1),
            ],
        ),
        _ex_tr(
            "Translate using correct collocations",
            [
                ("She took responsibility for the mistake.", "Sie übernahm die Verantwortung für den Fehler."),
                ("The reform has far-reaching consequences.", "Die Reform hat weitreichende Konsequenzen."),
                ("We must show consideration for the environment.", "Wir müssen Rücksicht auf die Umwelt nehmen."),
            ],
        ),
        _ex_arr(
            "Reconstruct the collocation sentence",
            [
                (["Sie", "traf", "eine", "weitreichende", "und", "tiefgreifende", "Entscheidung"], "Sie traf eine weitreichende und tiefgreifende Entscheidung."),
            ],
        ),
        _ex_sp(
            "Collocations in context",
            ["Use five collocations from today in a paragraph about a difficult decision you faced.", "Find three 'false friend' collocations where the German differs from English (e.g. make a decision).", "Quiz your partner: give an English collocation, they produce the German equivalent."],
        ),
    ],
}

LESSON_157 = {
    "title": "German in the Digital Age: Online Language and New Media",
    "level": "C2",
    "scenario": "digital_communication",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand German internet slang, memes, and digital communication",
        "Use digital registers appropriately (WhatsApp, Twitter, formal email)",
        "Recognise anglicisms and their status in contemporary German",
        "Critically discuss language change and digital German",
    ],
    "cultural_note": "German internet language borrows heavily from English but adapts it phonologically and grammatically. 'Liken', 'posten', 'updaten', 'googeln' are standard verbs. The Rat für deutsche Rechtschreibung monitors language change, and the debate about anglicisms is lively in German public discourse.",
    "grammar_focus": _gex(
        "Anglicisms and Neologisms in German",
        "Anglicisms in German follow German grammar rules: they receive case endings, take German verb conjugation, and form compounds with German words. Compound formation (Kompositum) is how German absorbs foreign vocabulary most productively.",
        "'googeln' (to google) / 'liken' (to like) / 'das Selfie' / 'das Update' / 'downloaden' / 'der Hype'",
        ["Anglicisms as verbs: liken, posten, updaten, streamen, boomen, chatten, googeln", "Compounds: das Smartphone-Zeitalter, der Social-Media-Auftritt, der Online-Handel", "German internet slang: krass (extreme), geil (cool/awesome in youth language), Digga (dude), lit"],
        ["Hast du das Video schon geliked?", "Ich muss noch kurz meine E-Mails checken.", "Der Post ist total abgegangen. (The post really blew up.)"],
    ),
    "dialogue": [
        _t("young_person", "Hast du seinen neuen Post gesehen? Der ist total abgegangen!", "Did you see his new post? It really blew up!"),
        _t("other", "Ja, ich hab's geliked. Aber der Hype darum ist schon etwas übertrieben.", "Yes, I liked it. But the hype around it is a bit exaggerated."),
        _t("young_person", "Ich finde, er hat das super gecheckt, wie man viral geht.", "I think he totally figured out how to go viral."),
        _t("other", "Stimmt. Aber sein Inhalt ist doch ziemlich oberflächlich, oder?", "True. But his content is pretty shallow, isn't it?"),
        _t("young_person", "Krass. Du klingst wie mein Deutschlehrer.", "Wow. You sound like my German teacher."),
        _t("other", "Naja, ich finde die Sprache interessant – wie das Englische ins Deutsche eingebaut wird.", "Well, I find the language interesting – how English is built into German."),
        _t("young_person", "Googeln, liken, posten – das ist halt einfach normal jetzt.", "Googling, liking, posting – that's just normal now."),
        _t("other", "Ja, aber 'gecheckt' als Partizip II von 'checken' – das ist schon kreativ.", "Yes, but 'gecheckt' as the past participle of 'checken' – that is creative."),
    ],
    "vocabulary_list": [
        _v("der Anglizismus (Anglizismen)", "anglicism", "Anglizismen prägen die Gegenwartssprache."),
        _v("abgehen (umgangssprachlich)", "to go off / blow up (colloquial)", "Der Post ist abgegangen."),
        _v("viral gehen", "to go viral", "Das Video ist viral gegangen."),
        _v("gecheckt haben", "to have figured out (colloquial)", "Er hat das total gecheckt."),
        _v("der Hype (-s)", "hype", "Der Hype ist schnell vorbei."),
        _v("posten", "to post (online)", "Sie postet täglich auf Instagram."),
        _v("liken", "to like (social media)", "Hast du das Foto geliked?"),
        _v("krass (Jugendsprache)", "extreme / wow / crazy (youth slang)", "Das ist voll krass."),
        _v("oberflächlich", "superficial / shallow", "Der Inhalt ist zu oberflächlich."),
        _v("der Neologismus (Neologismen)", "neologism", "Neologismen entstehen ständig neu."),
    ],
    "exercises": [
        _ex_fib(
            "Form the correct German past tense/past participle of anglicisms",
            ["liken → er hat ___ (Partizip II)", "posten → sie hat ___ (Partizip II)", "googeln → ich habe ___ (Partizip II)"],
            ["geliked", "gepostet", "gegoogelt"],
        ),
        _ex_mc(
            "Digital German: choose the correct form",
            [
                ("'Das Video ist ___.' (went viral)", ["viral gegangen", "viral geht", "viral ging", "viral geworden"], 0),
                ("'Der Post ist total ___.' (blew up / went viral)", ["abgegangen", "abgegeben", "abgesetzt", "abgeflogen"], 0),
                ("Which is a correct German compound with an anglicism?", ["Smartphone-Zeitalter", "Zeit-Smartphone", "Zeitalter Smartphone", "Smartphone Zeitalter"], 0),
            ],
        ),
        _ex_tr(
            "Translate digital language",
            [
                ("Did you like his post yet?", "Hast du seinen Post schon geliked?"),
                ("The video went viral overnight.", "Das Video ist über Nacht viral gegangen."),
                ("I need to check my emails quickly.", "Ich muss kurz meine E-Mails checken."),
            ],
        ),
        _ex_arr(
            "Order the digital conversation",
            [
                (["Hast", "du", "seinen", "neuen", "Post", "schon", "geliked"], "Hast du seinen neuen Post schon geliked?"),
            ],
        ),
        _ex_sp(
            "Discuss digital German",
            ["Discuss: Should anglicisms in German be encouraged, tolerated, or resisted?", "List five German internet terms and explain them to a non-digital-native speaker.", "Compare your native language's digital slang to German – what patterns do you notice?"],
        ),
    ],
}

LESSON_158 = {
    "title": "The German Essay Tradition (Essayistik)",
    "level": "C2",
    "scenario": "essay_writing",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Write a German essay in the tradition of the 'Essayistik'",
        "Balance subjective reflection with intellectual argument",
        "Use the German essay's characteristic mixture of genres and registers",
        "Analyse and emulate essays by Adorno, Benjamin, and contemporary writers",
    ],
    "cultural_note": "The German essay tradition (from Montaigne through Lessing to Walter Benjamin and Theodor W. Adorno) prizes intellectual rigour combined with stylistic elegance. Adorno's 'Der Essay als Form' argues that the essay resists system-building and embraces the fragmentary – a very different ideal from the five-paragraph Anglo-American essay.",
    "grammar_focus": _gex(
        "The Essay Voice: First Person + Generalization",
        "The German essay balances personal reflection ('ich') with generalizing statements ('man', 'wir', 'es'). This creates intimacy and authority simultaneously. Sentence rhythm, allusion, and conceptual density are key stylistic features.",
        "'Ich weiß nicht, was Wahrheit ist. Aber ich weiß, wie es sich anfühlt, wenn man nah daran ist.'",
        ["Personal: Ich erinnere mich... / Mir scheint... / Was mich beschäftigt...", "General: Man könnte... / Es lässt sich... / Wir alle kennen...", "Conceptual tension: Das Paradoxon / Der Widerspruch / Die Spannung zwischen X und Y"],
        ["Was uns am Schreiben fasziniert, ist vielleicht genau das, was am schwersten zu sagen ist.", "Der Essay weigert sich, ein System zu sein – und darin liegt seine Wahrheit.", "Adorno schreibt: 'Der Essay... denkt in Brüchen.'"],
    ),
    "dialogue": [
        _t("writer", "Ich finde es schwierig, den richtigen Ton für meinen Essay zu finden.", "I find it difficult to find the right tone for my essay."),
        _t("mentor", "Was ist das Thema?", "What is the topic?"),
        _t("writer", "Stille. Ich will über Stille schreiben – aber auch über das Gegenteil davon.", "Silence. I want to write about silence – but also about its opposite."),
        _t("mentor", "Ein klassisches Essaythema. Beginnen Sie persönlich: eine Szene, ein Moment.", "A classic essay topic. Begin personally: a scene, a moment."),
        _t("writer", "Und dann?", "And then?"),
        _t("mentor", "Öffnen Sie das Persönliche zum Allgemeinen. Bauen Sie Spannung auf.", "Open the personal to the general. Build tension."),
        _t("writer", "Wie Benjamin – der beginnt immer mit einem kleinen, konkreten Bild.", "Like Benjamin – he always begins with a small, concrete image."),
        _t("mentor", "Genau. Das Konkrete führt zum Abstrakten. Das ist die Essaybewegung.", "Exactly. The concrete leads to the abstract. That is the essay movement."),
    ],
    "vocabulary_list": [
        _v("die Essayistik", "essay writing / the essay tradition", "Die Essayistik hat in Deutschland lange Tradition."),
        _v("das Fragment (-e)", "fragment", "Adorno schätzt das Fragmentarische."),
        _v("das Paradoxon (Paradoxa)", "paradox", "Das Paradoxon ist ein essayistisches Mittel."),
        _v("die Reflexion (-en)", "reflection", "Persönliche Reflexion ist typisch für Essays."),
        _v("die Spannung", "tension / suspense", "Die Spannung zwischen Ich und Welt."),
        _v("konkret", "concrete", "Beginnen Sie mit einem konkreten Bild."),
        _v("abstrakt", "abstract", "Das Konkrete führt zum Abstrakten."),
        _v("der Bruch (Brüche)", "break / fracture / rupture", "Der Essay denkt in Brüchen."),
        _v("verweigern / sich weigern", "to refuse", "Der Essay weigert sich, ein System zu sein."),
        _v("die Allgemeinheit", "generality / the general", "Vom Konkreten zur Allgemeinheit."),
    ],
    "exercises": [
        _ex_mc(
            "The essay tradition: choose the correct statement",
            [
                ("Adorno's view of the essay is that it:", ["Should follow a strict five-paragraph structure", "Resists system-building and embraces the fragmentary", "Must be purely objective", "Should avoid personal voice"], 1),
                ("What is the typical essay movement described in the lesson?", ["Abstract to concrete", "Concrete to abstract", "Argument to conclusion", "Question to answer"], 1),
                ("What does 'Der Essay denkt in Brüchen' mean?", ["The essay is broken and incomplete", "The essay thinks through ruptures and contradictions", "The essay uses bullet points", "The essay is fragmentary only"], 1),
            ],
        ),
        _ex_fib(
            "Complete the essay-style sentences",
            ["Was uns am Schreiben fasziniert, ist ___, was am schwersten zu sagen ist.", "Der Essay ___ sich, ein System zu sein – und darin liegt seine ___.", "Ich ___ mich nicht, was Wahrheit ist. Aber ich ___, wie es sich anfühlt."],
            ["vielleicht genau das", "weigert / Wahrheit", "weiß / weiß"],
        ),
        _ex_tr(
            "Translate in essay style",
            [
                ("What fascinates us about writing is perhaps precisely what is hardest to say.", "Was uns am Schreiben fasziniert, ist vielleicht genau das, was am schwersten zu sagen ist."),
                ("The essay refuses to be a system – and therein lies its truth.", "Der Essay weigert sich, ein System zu sein – und darin liegt seine Wahrheit."),
            ],
        ),
        _ex_arr(
            "Order the essay sentence",
            [
                (["Der", "Essay", "weigert", "sich", "ein", "System", "zu", "sein", "und", "darin", "liegt", "seine", "Wahrheit"], "Der Essay weigert sich, ein System zu sein – und darin liegt seine Wahrheit."),
            ],
        ),
        _ex_sp(
            "Write your essay",
            ["Write the opening paragraph of an essay on a topic of your choice. Begin concretely.", "Read Benjamin's 'Berliner Kindheit' opening – what makes it an essay and not a memoir?", "Discuss: What is the purpose of the essay form? Why not just write an article?"],
        ),
    ],
}

LESSON_159 = {
    "title": "German Science Writing and Academic Prose",
    "level": "C2",
    "scenario": "academic_writing",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Write in the conventions of German academic prose (Wissenschaftssprache)",
        "Use hedging, distancing, and objectivizing constructions at the highest level",
        "Understand the structure of a German academic paper (Hausarbeit/Seminararbeit)",
        "Produce a German abstract (Zusammenfassung) and introduction (Einleitung)",
    ],
    "cultural_note": "German Wissenschaftssprache (academic prose) is characterised by: impersonal constructions, heavy nominalization, passive voice, extensive citation apparatus (Fußnoten), and a formal structure (Einleitung, Hauptteil, Schluss). The Hausarbeit is the main written assessment form in German universities.",
    "grammar_focus": _gex(
        "Distancing and Objectivizing in Academic German",
        "Academic German removes personal agency through impersonal constructions, nominalization, and third-person reference. The goal is to present findings as objective and independent of the author.",
        "'Ich habe untersucht' → 'Im Rahmen dieser Arbeit wurde untersucht...' / 'Ich meine' → 'Es lässt sich argumentieren, dass...'",
        ["Impersonal: Im Rahmen dieser Untersuchung / In der vorliegenden Arbeit / Es zeigt sich", "Nominalisation: die Untersuchung (← untersuchen), die Analyse (← analysieren)", "Distancing: Es wird angenommen / Es gilt als erwiesen / Den Ergebnissen zufolge"],
        ["Im Rahmen dieser Arbeit wurde der Einfluss von X auf Y untersucht.", "Den vorliegenden Daten zufolge lässt sich folgendes feststellen.", "Es konnte gezeigt werden, dass die Hypothese bestätigt wird."],
    ),
    "dialogue": [
        _t("supervisor", "Ihre Einleitung beginnt mit 'Ich will in dieser Arbeit zeigen...' Das müssen Sie ändern.", "Your introduction begins with 'I want to show in this paper...' You need to change that."),
        _t("student", "Was ist falsch daran?", "What is wrong with that?"),
        _t("supervisor", "In der deutschen Wissenschaftssprache schreibt man nicht 'ich'. Schreiben Sie: 'Ziel dieser Arbeit ist es...'", "In German academic prose one does not write 'I'. Write: 'The aim of this paper is...'"),
        _t("student", "Also unpersönlich – aber wie verweise ich dann auf meine eigene Analyse?", "So impersonal – but how do I then refer to my own analysis?"),
        _t("supervisor", "'In der vorliegenden Arbeit wird argumentiert...' oder 'Die Analyse zeigt...'", "'In the present paper it is argued...' or 'The analysis shows...'"),
        _t("student", "Und für die Schlussfolgerung?", "And for the conclusion?"),
        _t("supervisor", "'Zusammenfassend lässt sich festhalten...' oder 'Die Ergebnisse belegen...'", "'In summary it can be held...' or 'The results demonstrate...'"),
        _t("student", "Das klingt sehr formell, aber ich verstehe die Logik.", "That sounds very formal, but I understand the logic."),
    ],
    "vocabulary_list": [
        _v("im Rahmen dieser Arbeit", "within the scope of this paper", "Im Rahmen dieser Arbeit wird X untersucht."),
        _v("vorliegend", "present / current", "Die vorliegende Studie analysiert..."),
        _v("festhalten", "to establish / hold / note", "Zusammenfassend lässt sich festhalten..."),
        _v("belegen", "to demonstrate / substantiate", "Die Daten belegen die Hypothese."),
        _v("zufolge (+ Dativ)", "according to", "Den Ergebnissen zufolge..."),
        _v("die Schlussfolgerung (-en)", "conclusion", "Die Schlussfolgerung lautet: ..."),
        _v("die Einleitung (-en)", "introduction", "Die Einleitung skizziert das Thema."),
        _v("argumentieren", "to argue", "In der Arbeit wird argumentiert, dass..."),
        _v("die Zusammenfassung (-en)", "summary / abstract", "Die Zusammenfassung fasst die Ergebnisse zusammen."),
        _v("die Hypothese (-n)", "hypothesis", "Die Hypothese wird im Hauptteil geprüft."),
    ],
    "exercises": [
        _ex_fib(
            "Rewrite in academic German",
            ["'Ich untersuche X.' → 'Im Rahmen dieser Arbeit ___ X ___.' (Passiv: untersuchen)", "'Ich denke, dass Y stimmt.' → 'Es ___ sich ___, dass Y zutrifft.' (lassen / argumentieren)", "'Die Ergebnisse zeigen, dass...' → 'Den Ergebnissen ___ lässt sich ___, dass...' (zufolge / feststellen)"],
            ["wird / untersucht", "lässt / argumentieren", "zufolge / feststellen"],
        ),
        _ex_mc(
            "Academic register: choose the correct form",
            [
                ("Which is the correct academic opening for a paper?", ["Ich will hier zeigen dass...", "Ziel der vorliegenden Arbeit ist es, zu zeigen, dass...", "Hier geht es um...", "Wir wollen untersuchen ob..."], 1),
                ("How do you refer to your own findings impersonally?", ["Ich fand heraus...", "Es wurde festgestellt...", "Wir sahen...", "Man sieht..."], 1),
                ("Which closing formula is academic?", ["Alles in allem...", "Zusammenfassend lässt sich festhalten, dass...", "Ich denke also...", "Zum Schluss sage ich..."], 1),
            ],
        ),
        _ex_tr(
            "Translate into academic German",
            [
                ("The aim of this paper is to investigate the influence of X on Y.", "Ziel der vorliegenden Arbeit ist es, den Einfluss von X auf Y zu untersuchen."),
                ("According to the results, the hypothesis is confirmed.", "Den Ergebnissen zufolge wird die Hypothese bestätigt."),
                ("In summary, it can be established that...", "Zusammenfassend lässt sich festhalten, dass..."),
            ],
        ),
        _ex_arr(
            "Reconstruct the academic sentence",
            [
                (["Im", "Rahmen", "dieser", "Arbeit", "wurde", "der", "Einfluss", "von", "X", "auf", "Y", "untersucht"], "Im Rahmen dieser Arbeit wurde der Einfluss von X auf Y untersucht."),
            ],
        ),
        _ex_sp(
            "Academic writing practice",
            ["Write a 150-word introduction for a paper on a topic of your choice using academic register.", "Rewrite a personal paragraph about your research in fully impersonal academic German.", "What are the key differences between Anglo-American and German academic writing conventions?"],
        ),
    ],
}

LESSON_160 = {
    "title": "German Dialects: Recognition and Appreciation",
    "level": "C2",
    "scenario": "dialectology",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Recognize major German dialect groups and their key features",
        "Understand the social and cultural significance of dialects in Germany",
        "Decode basic dialect features in Bavarian, Saxon, Swabian, and Low German",
        "Discuss language variation and standardisation in German-speaking countries",
    ],
    "cultural_note": "Germany has an extremely rich dialect landscape. While Standard German (Hochdeutsch) is the prestige variety, dialects carry deep cultural identity. Bavarian, Saxon (Sächsisch), Swabian (Schwäbisch), Berlin dialect (Berlinerisch), Cologne (Kölsch), and Low German (Niederdeutsch/Plattdeutsch) are major groups.",
    "grammar_focus": _gex(
        "Key Dialect Features",
        "Dialects differ from Standard German in phonology, grammar, and vocabulary. Key features to recognize: vowel shifts, consonant changes (High German consonant shift not fully applied in Low German), different articles, and unique vocabulary.",
        "Bavarian: 'Mia san mia' (= Wir sind wir) / Saxon: 'Ich hab ä Buch gekoofd' (= ein Buch gekauft) / Low German: 'Ik bün' (= Ich bin)",
        ["Bavarian: ch → k, Diphthong shift: 'ei' → 'oa', 'ie' → 'ia'", "Saxon: 'g' → 'ch', rounding of vowels, unique prosody", "Low German: no High German consonant shift: maken (machen), Water (Wasser), Tid (Zeit)"],
        ["Bavarian: 'Servus!' / 'Grüß Gott!' / 'Pfiat di!' (Tschüss)", "Swabian: 'Ge?' (= oder?) / 'Schaffe' (= arbeiten)", "Berlinerisch: 'ick' (ich), 'det' (das), 'keen' (kein)"],
    ),
    "dialogue": [
        _t("traveller", "Ich war gerade in Bayern – ich habe kein Wort verstanden!", "I was just in Bavaria – I didn't understand a word!"),
        _t("linguist", "Das geht vielen so. Bayerisch ist ein Oberdeutscher Dialekt mit starker Eigenheit.", "That happens to many. Bavarian is an Upper German dialect with strong distinctive features."),
        _t("traveller", "Besonders die Aussprache – 'Mia san mia' statt 'Wir sind wir'.", "Especially the pronunciation – 'Mia san mia' instead of 'Wir sind wir'."),
        _t("linguist", "Genau. Und 'Servus' als Gruß – das kommt aus dem Lateinischen 'servus' (Diener).", "Exactly. And 'Servus' as a greeting – that comes from the Latin 'servus' (servant)."),
        _t("traveller", "Und Sächsisch – das klingt ganz anders.", "And Saxon – that sounds completely different."),
        _t("linguist", "Sächsisch hat eine charakteristische Intonation und ein 'g' das zum 'ch' wird.", "Saxon has a characteristic intonation and a 'g' that becomes 'ch'."),
        _t("traveller", "Und Niederdeutsch – ist das überhaupt noch Deutsch?", "And Low German – is that even still German?"),
        _t("linguist", "Es ist eine eigene Sprache, näher am Englischen als am Hochdeutschen. 'Water' = Wasser, 'Tid' = Zeit.", "It is a separate language, closer to English than to Standard German. 'Water' = Wasser, 'Tid' = Zeit."),
    ],
    "vocabulary_list": [
        _v("der Dialekt (-e)", "dialect", "Deutschland hat viele lebendige Dialekte."),
        _v("das Hochdeutsch", "Standard German / High German", "Hochdeutsch ist die überregionale Standardsprache."),
        _v("die Mundart (-en)", "dialect (more traditional term)", "Mundarten sind regionale Sprachformen."),
        _v("oberdeutsch", "Upper German", "Bayerisch und Schwäbisch sind oberdeutsche Dialekte."),
        _v("niederdeutsch / Plattdeutsch", "Low German", "Plattdeutsch wird in Norddeutschland gesprochen."),
        _v("der Lautwandel", "sound change", "Der hochdeutsche Lautwandel ist historisch bedeutsam."),
        _v("die Intonation (-en)", "intonation", "Dialekte unterscheiden sich in der Intonation."),
        _v("die Eigenheit (-en)", "distinctive feature / peculiarity", "Bayerisch hat starke Eigenheiten."),
        _v("die Standardisierung", "standardisation", "Die Standardisierung begann im 16. Jahrhundert."),
        _v("der Prestigedialekt", "prestige dialect", "Hochdeutsch ist der überregionale Prestigedialekt."),
    ],
    "exercises": [
        _ex_mc(
            "Dialects: match to region",
            [
                ("'Mia san mia' is from which dialect?", ["Berlinerisch", "Sächsisch", "Bayerisch", "Schwäbisch"], 2),
                ("Low German (Niederdeutsch) is most closely related to:", ["Standard German", "Dutch and English", "Bavarian", "Yiddish"], 1),
                ("'Ick' instead of 'ich' is characteristic of:", ["Bayerisch", "Sächsisch", "Berlinerisch", "Schwäbisch"], 2),
            ],
        ),
        _ex_fib(
            "Translate from dialect to Standard German",
            ["Bavarian: 'Mia san mia.' → '___ sind ___.'", "Berlinerisch: 'Ick hab det jetan.' → 'Ich habe ___ ___.'", "Low German: 'Water' → '___'"],
            ["Wir / wir", "das / getan", "Wasser"],
        ),
        _ex_tr(
            "Translate and discuss dialect features",
            [
                ("'Schaffe' in Swabian dialect means 'to work'.", "'Schaffe' im Schwäbischen bedeutet 'arbeiten'."),
                ("Low German 'maken' corresponds to Standard German 'machen'.", "Niederdeutsch 'maken' entspricht dem Hochdeutschen 'machen'."),
            ],
        ),
        _ex_arr(
            "Order the dialect description",
            [
                (["Bayerisch", "ist", "ein", "oberdeutscher", "Dialekt", "mit", "starken", "Eigenheiten"], "Bayerisch ist ein oberdeutscher Dialekt mit starken Eigenheiten."),
            ],
        ),
        _ex_sp(
            "Dialect appreciation",
            ["Which German dialect do you find most interesting and why?", "Why might dialects be important for cultural identity even as Standard German dominates?", "Compare dialect preservation in Germany with the situation in your own country."],
        ),
    ],
}

LESSON_161 = {
    "title": "German Legal and Official Language",
    "level": "C2",
    "scenario": "legal_language",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Read and understand German legal and official documents",
        "Recognize characteristic features of German Amtssprache (bureaucratic language)",
        "Use legal German vocabulary and fixed formulas correctly",
        "Write a formal complaint or petition in German bureaucratic style",
    ],
    "cultural_note": "Amtssprache (official/bureaucratic language) is famously complex in German-speaking countries. The Plain Language movement (Leichte Sprache, Einfache Sprache) pushes back against it, but mastering official German is essential for life in Germany – from Behördengänge (administrative visits) to Widersprüche (appeals against decisions).",
    "grammar_focus": _gex(
        "Bureaucratic Nominalization and Fixed Formulas",
        "Official German maximises nominalization, removes human agency, and uses fixed formulas. Every official act has a standard phrasing that signals legitimacy.",
        "'Ich beantrage...' / 'Hiermit wird mitgeteilt, dass...' / 'Dem Antrag wird stattgegeben.' / 'Der Widerspruch wird zurückgewiesen.'",
        ["Opening formulas: Sehr geehrte Damen und Herren, / Hiermit teile ich Ihnen mit, dass...", "Nominalization: die Beantragung, die Bewilligung, die Ablehnung, die Zustellung", "Legal passive: wird stattgegeben / wird zurückgewiesen / wurde erlassen"],
        ["Hiermit beantrage ich die Ausstellung eines Reisepasses.", "Gegen den Bescheid vom 12. März lege ich hiermit Widerspruch ein.", "Der Antrag auf Kindergeld wird mit Wirkung vom 1. Januar bewilligt."],
    ),
    "dialogue": [
        _t("citizen", "Ich habe einen Ablehnungsbescheid bekommen. Was kann ich tun?", "I received a rejection notice. What can I do?"),
        _t("advisor", "Sie können Widerspruch einlegen. Die Frist beträgt in der Regel vier Wochen.", "You can file an appeal. The deadline is generally four weeks."),
        _t("citizen", "Wie formuliere ich das?", "How do I formulate that?"),
        _t("advisor", "Beginnen Sie mit: 'Gegen den Bescheid vom [Datum] lege ich hiermit Widerspruch ein.'", "Begin with: 'I hereby appeal against the notice dated [date].'"),
        _t("citizen", "Und dann begründe ich es?", "And then I give reasons?"),
        _t("advisor", "Ja. Formulieren Sie sachlich und präzise. Vermeiden Sie Emotionen.", "Yes. Write factually and precisely. Avoid emotions."),
        _t("citizen", "Und wie schließe ich ab?", "And how do I close?"),
        _t("advisor", "Mit 'Ich bitte um Abhilfe' oder 'Ich beantrage die Aufhebung des Bescheides'.", "With 'I request a remedy' or 'I request the revocation of the notice'."),
    ],
    "vocabulary_list": [
        _v("der Bescheid (-e)", "official notice / decision", "Sie erhielt einen Ablehnungsbescheid."),
        _v("der Widerspruch (Widersprüche)", "appeal / objection", "Ich lege Widerspruch ein."),
        _v("die Frist (-en)", "deadline / period", "Die Widerspruchsfrist beträgt vier Wochen."),
        _v("die Aufhebung (-en)", "revocation / annulment", "Die Aufhebung des Bescheides wird beantragt."),
        _v("beantragen", "to apply for / to request", "Ich beantrage die Ausstellung eines Ausweises."),
        _v("stattgeben (+ Dativ)", "to grant / uphold", "Dem Antrag wird stattgegeben."),
        _v("zurückweisen", "to reject / dismiss", "Der Widerspruch wird zurückgewiesen."),
        _v("hiermit", "hereby", "Hiermit teile ich Ihnen mit..."),
        _v("die Abhilfe", "remedy / redress", "Ich bitte um Abhilfe."),
        _v("sachlich", "factual / objective / unemotional", "Bleiben Sie sachlich in Ihrer Formulierung."),
    ],
    "exercises": [
        _ex_fib(
            "Complete the official German formulas",
            ["Gegen den Bescheid vom 5. März ___ ich hiermit Widerspruch ___.", "Hiermit ___ ich die Ausstellung eines neuen Reisepasses.", "___ dem Antrag wird stattgegeben."],
            ["lege / ein", "beantrage", "Dem"],
        ),
        _ex_mc(
            "Legal German vocabulary",
            [
                ("What is 'einen Widerspruch einlegen'?", ["To submit a form", "To file an appeal", "To pay a fine", "To request information"], 1),
                ("What does 'Dem Antrag wird stattgegeben' mean?", ["The application is rejected", "The application is granted", "The application is pending", "The application must be resubmitted"], 1),
                ("What is the correct translation of 'Bescheid'?", ["Advice", "Question", "Official notice / decision", "Letter"], 2),
            ],
        ),
        _ex_tr(
            "Translate into German official language",
            [
                ("I hereby file an appeal against the notice dated 10 April.", "Gegen den Bescheid vom 10. April lege ich hiermit Widerspruch ein."),
                ("I request the issuance of a passport.", "Ich beantrage die Ausstellung eines Reisepasses."),
                ("I request a remedy.", "Ich bitte um Abhilfe."),
            ],
        ),
        _ex_arr(
            "Reconstruct the formal appeal opening",
            [
                (["Gegen", "den", "Bescheid", "vom", "12. März", "lege", "ich", "hiermit", "Widerspruch", "ein"], "Gegen den Bescheid vom 12. März lege ich hiermit Widerspruch ein."),
            ],
        ),
        _ex_sp(
            "Official language in practice",
            ["Write a formal appeal against an imaginary official decision in German.", "Role-play: you visit the Bürgeramt – what vocabulary and register do you use?", "Discuss: Why is Amtssprache so complex? What would Leichte Sprache look like here?"],
        ),
    ],
}

LESSON_162 = {
    "title": "Cultural Competence: Stereotypes, Identity, and Belonging",
    "level": "C2",
    "scenario": "cultural_reflection",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Discuss German cultural identity, stereotypes, and their origins with nuance",
        "Engage with concepts of Leitkultur, Heimat, Identität in German public discourse",
        "Use vocabulary for discussing diversity, inclusion, and belonging in German",
        "Critically reflect on cultural assumptions in language learning itself",
    ],
    "cultural_note": "Germany has grappled publicly with questions of identity since reunification and intensifying since the refugee crisis of 2015. Concepts like Leitkultur (leading/core culture), Heimat (homeland/belonging), and Willkommenskultur (welcome culture) have become politically charged. These discussions are essential for understanding contemporary German society.",
    "grammar_focus": _gex(
        "Discussing Abstract Social Concepts",
        "Discussions of identity and culture require abstract vocabulary and careful use of hedging (lässt sich argumentieren), modal verbs (sollte, dürfte), and concessive structures. These prevent oversimplification of complex social questions.",
        "'Heimat ist keine geografische, sondern eine emotionale Kategorie.' / 'Es lässt sich kaum bestreiten, dass Identität ein vielschichtiges Konzept ist.'",
        ["Hedged claims: Es lässt sich argumentieren, dass... / Es wäre vereinfachend zu sagen...", "Abstract nouns: die Zugehörigkeit, das Zugehörigkeitsgefühl, die Verwurzelung, die Entwurzelung", "Discourse: einerseits... andererseits / auf der einen Seite... auf der anderen Seite"],
        ["Heimat ist das, wo man sich verstanden fühlt.", "Die Frage der Leitkultur ist in der deutschen Politik umstritten.", "Vielfalt ist eine Realität, aber auch eine Gestaltungsaufgabe."],
    ),
    "dialogue": [
        _t("journalist", "Was bedeutet 'Heimat' für Sie – als jemand, der mit zwei Kulturen aufgewachsen ist?", "What does 'Heimat' mean to you – as someone who grew up between two cultures?"),
        _t("interviewee", "Das ist eine sehr persönliche Frage. Heimat ist für mich nicht ein Ort, sondern ein Gefühl von Verstehtsein.", "That is a very personal question. Heimat for me is not a place, but a feeling of being understood."),
        _t("journalist", "Fühlen Sie sich in Deutschland zu Hause?", "Do you feel at home in Germany?"),
        _t("interviewee", "Ja – und auch nicht. Ich gehöre dazu, aber ich werde manchmal trotzdem als Außenseiter behandelt.", "Yes – and also not. I belong, but I am sometimes still treated as an outsider."),
        _t("journalist", "Wie sollte die Gesellschaft damit umgehen?", "How should society deal with that?"),
        _t("interviewee", "Es braucht mehr als Toleranz – echte Zugehörigkeit erfordert aktive Anerkennung.", "It needs more than tolerance – genuine belonging requires active recognition."),
        _t("journalist", "Das klingt nach dem Unterschied zwischen Duldung und Willkommen.", "That sounds like the difference between tolerance and welcome."),
        _t("interviewee", "Genau. Das ist der entscheidende Unterschied.", "Exactly. That is the decisive difference."),
    ],
    "vocabulary_list": [
        _v("die Zugehörigkeit", "belonging / membership", "Das Gefühl der Zugehörigkeit ist grundlegend."),
        _v("die Heimat", "home / homeland / belonging (complex concept)", "Heimat ist mehr als ein geografischer Begriff."),
        _v("die Leitkultur", "leading / core culture (politically contested)", "Der Begriff Leitkultur ist umstritten."),
        _v("die Vielfalt", "diversity", "Kulturelle Vielfalt ist eine Stärke."),
        _v("die Anerkennung (-en)", "recognition / acknowledgement", "Echte Anerkennung geht über Toleranz hinaus."),
        _v("die Entwurzelung", "uprooting / displacement", "Migration kann Entwurzelung bedeuten."),
        _v("die Verwurzelung", "rootedness / sense of belonging", "Kulturelle Verwurzelung gibt Stabilität."),
        _v("umstritten", "contested / controversial", "Das Konzept der Leitkultur ist umstritten."),
        _v("die Willkommenskultur", "welcome culture", "Die Willkommenskultur wurde viel diskutiert."),
        _v("die Duldung", "tolerance (mere acceptance, not embrace)", "Duldung ist nicht dasselbe wie Anerkennung."),
    ],
    "exercises": [
        _ex_mc(
            "Cultural concepts: choose the correct answer",
            [
                ("'Heimat' in German most closely refers to:", ["A specific city", "A feeling of home and belonging", "The German state", "One's birthplace only"], 1),
                ("What is the difference between 'Duldung' and 'Anerkennung'?", ["No difference", "Duldung is active, Anerkennung is passive", "Duldung is mere tolerance, Anerkennung is active recognition", "They mean the same in context"], 2),
                ("'Leitkultur' is best described as:", ["An uncontested legal concept", "A politically contested concept of a dominant national culture", "The German constitution", "Standard German language only"], 1),
            ],
        ),
        _ex_fib(
            "Complete with vocabulary of belonging",
            ["Echte ___ erfordert aktive Anerkennung, nicht nur Toleranz.", "Heimat ist für mich ein Gefühl von ___, nicht ein Ort.", "Die Frage der Leitkultur ist in der deutschen Politik ___."],
            ["Zugehörigkeit", "Verstehtsein", "umstritten"],
        ),
        _ex_tr(
            "Translate cultural discussion sentences",
            [
                ("Genuine belonging requires active recognition, not mere tolerance.", "Echte Zugehörigkeit erfordert aktive Anerkennung, nicht nur Duldung."),
                ("Cultural diversity is a strength but also a challenge.", "Kulturelle Vielfalt ist eine Stärke, aber auch eine Gestaltungsaufgabe."),
                ("The concept of Leitkultur is politically contested.", "Der Begriff der Leitkultur ist politisch umstritten."),
            ],
        ),
        _ex_arr(
            "Order the discussion sentence",
            [
                (["Heimat", "ist", "das", "wo", "man", "sich", "verstanden", "fühlt"], "Heimat ist das, wo man sich verstanden fühlt."),
            ],
        ),
        _ex_sp(
            "Identity and belonging discussion",
            ["What does Heimat mean to you personally? Answer in German.", "Is cultural diversity a strength or a challenge for German society – or both?", "Critically reflect: What cultural assumptions are built into German language learning materials?"],
        ),
    ],
}

LESSON_163 = {
    "title": "Advanced Translation: German and English",
    "level": "C2",
    "scenario": "translation_workshop",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Translate complex German texts into English with high fidelity",
        "Translate challenging English texts into natural, idiomatic German",
        "Handle untranslatable German concepts in translation",
        "Understand translation theory: equivalence, domestication, foreignization",
    ],
    "cultural_note": "Translation theory distinguishes between foreignization (keeping the foreignness of the source) and domestication (making it sound natural in the target language). The German Übersetzung debate is rich: Walter Benjamin's 'The Task of the Translator' argues for foreignization, revealing the foreignness of the original.",
    "grammar_focus": _gex(
        "Structural Differences in German-English Translation",
        "Key translation challenges: German compounds needing English phrases, German verb-final word order, German case system needing prepositions in English, modal particle meaning, and register differences.",
        "'Schadenfreude' → 'pleasure at others' misfortune' (no English equivalent) / 'Weltschmerz' → 'world-weariness' / 'Gemütlichkeit' → 'cosiness + warmth + friendliness'",
        ["Compound translation: Donaudampfschifffahrtsgesellschaft → Danube steamship company", "Modal particles: 'Das ist ja interessant.' → 'That's actually interesting.' / 'Well, that's interesting.'", "Register shift: German formal passive → English active voice often sounds more natural"],
        ["'Er hat sich doch nicht verrechnet?' → 'Surely he didn't miscalculate?' (doch = expectation of answer)", "Die Weltanschauung → worldview (but loses philosophical weight)", "Angst → anxiety/dread (but German Angst has existential depth English lacks)"],
    ),
    "dialogue": [
        _t("translator", "Wie übersetzt man 'Weltschmerz'? Es gibt kein englisches Äquivalent.", "How does one translate 'Weltschmerz'? There is no English equivalent."),
        _t("theorist", "Das ist das Faszinierende an Übersetzung. Manchmal muss man paraphrasieren.", "That is what is fascinating about translation. Sometimes one must paraphrase."),
        _t("translator", "Also 'a deep sadness about the state of the world'?", "So 'a deep sadness about the state of the world'?"),
        _t("theorist", "Das trifft es, verliert aber die Verdichtung. Benjamin würde sagen: behalte das Fremdwort.", "That captures it, but loses the compression. Benjamin would say: keep the foreign word."),
        _t("translator", "Aber dann verstehen englische Leser es nicht sofort.", "But then English readers don't understand it immediately."),
        _t("theorist", "Genau das ist Verfremdung – der Leser muss sich anstrengen. Das ist gewollt.", "That is precisely defamiliarisation – the reader must make an effort. That is intentional."),
        _t("translator", "Also ist jede Übersetzung eine Interpretation.", "So every translation is an interpretation."),
        _t("theorist", "Exakt. Traduttore, traditore – der Übersetzer ist immer auch Verräter.", "Exactly. Traduttore, traditore – the translator is always also a traitor."),
    ],
    "vocabulary_list": [
        _v("die Übersetzung (-en)", "translation", "Eine gute Übersetzung ist eine Kunst."),
        _v("die Verfremdung", "defamiliarisation / foreignization", "Verfremdung hält die Fremdheit des Originals."),
        _v("die Eindeutschung (-en)", "domestication / naturalization", "Eindeutschung macht den Text flüssiger."),
        _v("das Äquivalent (-e)", "equivalent", "Es gibt kein direktes Äquivalent."),
        _v("paraphrasieren", "to paraphrase", "Manchmal muss man paraphrasieren."),
        _v("die Verdichtung (-en)", "compression / condensation", "Komposita erlauben maximale Verdichtung."),
        _v("der Übersetzer / die Übersetzerin", "translator", "Ein guter Übersetzer ist zweisprachig und bikulturell."),
        _v("unübersetzbar", "untranslatable", "Manche Konzepte sind unübersetzbar."),
        _v("der Verrat", "betrayal / treason", "Traduttore, traditore – Übersetzen ist Verrat."),
        _v("die Interpretation (-en)", "interpretation", "Jede Übersetzung ist eine Interpretation."),
    ],
    "exercises": [
        _ex_mc(
            "Translation theory: choose the correct answer",
            [
                ("'Foreignization' in translation means:", ["Making the text sound natural in the target language", "Keeping the foreignness of the source text", "Translating word for word", "Avoiding difficult words"], 1),
                ("'Domestication' in translation means:", ["Keeping foreign words", "Making the text sound natural in the target language", "Using literal translation", "Foreignizing the text"], 1),
                ("'Traduttore, traditore' means:", ["The translator is always correct", "The translator is always also a traitor", "Translation is perfect", "Translators are artists"], 1),
            ],
        ),
        _ex_fib(
            "Translation challenges: fill in",
            ["'Weltschmerz' hat kein direktes englisches ___.", "Benjamin plädiert für Verfremdung: die ___ des Originals bewahren.", "'Gemütlichkeit' lässt sich nur ___ – es gibt kein einzelnes englisches Wort."],
            ["Äquivalent", "Fremdheit", "paraphrasieren"],
        ),
        _ex_tr(
            "Translate and discuss",
            [
                ("'Das ist doch klar.' – Translate, preserving the 'doch' nuance.", "That's obvious, isn't it. / Surely that's clear. (doch = expecting agreement)"),
                ("'Weltschmerz' – give both a foreignizing and domesticating translation.", "Foreignizing: Weltschmerz / Domesticating: world-weariness / deep sadness about the state of the world"),
            ],
        ),
        _ex_arr(
            "Order the translation discussion",
            [
                (["Jede", "Übersetzung", "ist", "auch", "eine", "Interpretation", "des", "Originals"], "Jede Übersetzung ist auch eine Interpretation des Originals."),
            ],
        ),
        _ex_sp(
            "Translation workshop",
            ["Translate a paragraph from a German newspaper into natural English. Note what was lost.", "Translate a complex English sentence into German. Where did you face structural challenges?", "Discuss: Is there a German word you wish existed in English? Explain its meaning."],
        ),
    ],
}

LESSON_164 = {
    "title": "Argumentation and Persuasion: Advanced Rhetoric",
    "level": "C2",
    "scenario": "public_speaking",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Deliver a persuasive speech using classical and modern rhetorical strategies",
        "Use Logos, Ethos, and Pathos in German argument",
        "Master the German Topos-tradition: loci communes in argumentation",
        "Engage audiences with narrative, data, and emotional appeals in German",
    ],
    "cultural_note": "German rhetorical tradition draws on classical antiquity (Cicero, Quintilian) through the Reformation (Luther's powerful German) to contemporary political speech. German political oratory values structure (Aufbau), evidence (Beleg), and logical progression. Emotional appeals are used but balanced by rational argument.",
    "grammar_focus": _gex(
        "Rhetorical Structures in German",
        "Effective German rhetoric uses: anaphora (repetition for emphasis), antithesis (contrast), climax (Steigerung), rhetorical questions (rhetorische Fragen), and tricolon (sets of three).",
        "Luther's 'Hier stehe ich, ich kann nicht anders' – anaphoric structure, personal stance, moral necessity.",
        ["Anaphora: 'Wir kämpfen für... Wir kämpfen gegen... Wir kämpfen, weil...'", "Antithesis: 'Nicht X, sondern Y.' / 'Einerseits... andererseits...'", "Tricolon: 'Freiheit, Gleichheit, Brüderlichkeit' / 'Klar, präzise, überzeugend'"],
        ["Wir haben die Wahl. Wir haben die Verantwortung. Wir haben die Zukunft in unseren Händen.", "Nicht Angst, sondern Mut soll uns leiten.", "Wer, wenn nicht wir? Wann, wenn nicht jetzt?"],
    ),
    "dialogue": [
        _t("speech_coach", "Ihre Rede ist gut strukturiert, aber sie fehlt an rhetorischer Kraft.", "Your speech is well structured, but it lacks rhetorical force."),
        _t("speaker", "Was meine ich falsch?", "What am I doing wrong?"),
        _t("speech_coach", "Sie argumentieren nur logisch – Logos. Sie brauchen auch Ethos und Pathos.", "You argue only logically – Logos. You also need Ethos and Pathos."),
        _t("speaker", "Ethos – das ist meine Glaubwürdigkeit als Sprecher?", "Ethos – that is my credibility as a speaker?"),
        _t("speech_coach", "Genau. Zeigen Sie, warum man Ihnen vertrauen kann. Persönliche Erfahrung ist stark.", "Exactly. Show why you can be trusted. Personal experience is powerful."),
        _t("speaker", "Und Pathos – Emotionen?", "And Pathos – emotions?"),
        _t("speech_coach", "Ja, aber dosiert. Ein konkretes Beispiel, eine menschliche Geschichte – das bewegt.", "Yes, but in measured doses. A concrete example, a human story – that moves people."),
        _t("speaker", "Und strukturell? Wie ende ich stark?", "And structurally? How do I end strongly?"),
    ],
    "vocabulary_list": [
        _v("das Ethos", "ethos (speaker credibility)", "Ethos entsteht durch Glaubwürdigkeit und Expertise."),
        _v("der Logos", "logos (logical argument)", "Logos überzeugt durch Fakten und Logik."),
        _v("das Pathos", "pathos (emotional appeal)", "Pathos bewegt durch Gefühle und Geschichten."),
        _v("die Anaphora (-phern)", "anaphora (repetition at start of clauses)", "Anaphora erzeugt Rhythmus und Nachdruck."),
        _v("die Antithese (-n)", "antithesis", "Antithesen klären durch Kontrast."),
        _v("die Steigerung (-en)", "climax / escalation", "Eine rhetorische Steigerung steigert Spannung."),
        _v("die rhetorische Frage (-n)", "rhetorical question", "Rhetorische Fragen laden zum Nachdenken ein."),
        _v("das Trikolon (-s/-kola)", "tricolon (set of three)", "Trikola sind einprägsam."),
        _v("dosiert", "measured / dosed", "Pathos sollte dosiert eingesetzt werden."),
        _v("überzeugen", "to convince / persuade", "Eine gute Rede überzeugt durch alle drei Dimensionen."),
    ],
    "exercises": [
        _ex_mc(
            "Rhetorical devices: identify",
            [
                ("'Wir kämpfen. Wir siegen. Wir bleiben.' – What device?", ["Antithesis", "Anaphora", "Tricolon", "Rhetorical question"], 2),
                ("'Nicht Angst, sondern Mut soll uns leiten.' – What device?", ["Anaphora", "Antithesis", "Climax", "Irony"], 1),
                ("'Wer, wenn nicht wir? Wann, wenn nicht jetzt?' – What device?", ["Anaphora", "Antithesis", "Rhetorical question", "Tricolon"], 2),
            ],
        ),
        _ex_fib(
            "Complete the rhetorical sentences",
            ["Wir haben die Wahl. Wir haben die ___. Wir haben die Zukunft in unseren ___.", "Nicht ___, sondern Mut soll uns leiten.", "Freiheit, ___, Brüderlichkeit – das klassische Trikolon."],
            ["Verantwortung / Händen", "Angst", "Gleichheit"],
        ),
        _ex_tr(
            "Translate using rhetorical devices",
            [
                ("We have the choice. We have the responsibility. We have the future in our hands.", "Wir haben die Wahl. Wir haben die Verantwortung. Wir haben die Zukunft in unseren Händen."),
                ("Not fear, but courage should guide us.", "Nicht Angst, sondern Mut soll uns leiten."),
            ],
        ),
        _ex_arr(
            "Build the anaphoric sequence",
            [
                (["Wir", "kämpfen", "für", "Gerechtigkeit", "Wir", "kämpfen", "gegen", "Unrecht", "Wir", "kämpfen", "weil", "wir", "müssen"], "Wir kämpfen für Gerechtigkeit. Wir kämpfen gegen Unrecht. Wir kämpfen, weil wir müssen."),
            ],
        ),
        _ex_sp(
            "Deliver a rhetorical speech",
            ["Prepare a 2-minute persuasive speech on any topic. Use anaphora, antithesis, and a rhetorical question.", "Peer feedback: identify which rhetorical devices your partner used.", "Discuss: When is emotional appeal appropriate in German public discourse?"],
        ),
    ],
}

LESSON_165 = {
    "title": "C2 Advanced Synthesis: Mastery and Beyond",
    "level": "C2",
    "scenario": "mastery_review",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Demonstrate mastery of all C2 grammar, style, and register features",
        "Produce extended German discourse indistinguishable from a near-native speaker",
        "Reflect on the journey from beginner to C2 and identify a personal learning legacy",
        "Explore what comes after C2: maintaining, deepening, and enjoying German mastery",
    ],
    "cultural_note": "C2 represents the highest recognised level of language proficiency. At this point, German is not a foreign language you use – it is a language you live in. The DELF/TELC/Goethe C2 exams test this. But C2 is not the end: native-like mastery deepens for life through reading, friendship, and immersion.",
    "grammar_focus": _gex(
        "C2 Grammar: Complete Synthesis",
        "Every grammatical resource of German is available to a C2 speaker: all tenses, moods, voice alternations, complex syntax, and pragmatic structures. The goal is not accuracy alone but stylistic precision – choosing the right form for the right effect.",
        "Das von Fachleuten jahrelang diskutierte, aber erst jetzt öffentlich anerkannte Problem wird nun endlich angegangen – was, wenngleich spät, zu begrüßen ist.",
        ["Complete form inventory: all passive tenses, Konjunktiv I+II, all participial patterns", "Stylistic choices: active vs. passive, Konjunktiv I vs. II, extended NP vs. relative clause", "Discourse: cohesion devices, text organisation, genre conventions"],
        ["Wenngleich spät, ist der Schritt zu begrüßen.", "Das lässt sich, trotz aller Einschränkungen, kaum bestreiten.", "Es wäre verfehlt anzunehmen, die Reise sei hier zu Ende."],
    ),
    "dialogue": [
        _t("examiner", "Sie haben den Kurs abgeschlossen. Was hat Sie am meisten überrascht?", "You have completed the course. What surprised you most?"),
        _t("learner", "Dass Sprache nie aufhört, mich zu überraschen. Immer gibt es eine Nuance, die ich noch nicht kannte.", "That language never stops surprising me. There is always a nuance I didn't yet know."),
        _t("examiner", "Was werden Sie mitnehmen?", "What will you take with you?"),
        _t("learner", "Die Überzeugung, dass Sprache Denken ist. Auf Deutsch zu denken verändert, was ich denke.", "The conviction that language is thought. Thinking in German changes what I think."),
        _t("examiner", "Das ist eine tiefe Erkenntnis. Was kommt als nächstes?", "That is a profound insight. What comes next?"),
        _t("learner", "Lesen. Freundschaften auf Deutsch. Leben auf Deutsch.", "Reading. Friendships in German. Living in German."),
        _t("examiner", "Das ist der Weg zu wirklicher Meisterschaft.", "That is the path to true mastery."),
        _t("learner", "Dann fange ich jetzt an.", "Then I begin now."),
    ],
    "vocabulary_list": [
        _v("die Meisterschaft", "mastery", "Sprachliche Meisterschaft ist ein lebenslanger Weg."),
        _v("die Erkenntnis (-se)", "insight / realisation", "Das war eine tiefe Erkenntnis."),
        _v("die Überzeugung (-en)", "conviction / belief", "Ich bin der Überzeugung, dass..."),
        _v("wirklich", "true / real / truly", "Wirkliche Meisterschaft zeigt sich im Alltag."),
        _v("vertiefen", "to deepen", "Man kann eine Sprache immer weiter vertiefen."),
        _v("das Denken", "thought / thinking (as noun)", "Sprache formt das Denken."),
        _v("die Nuance (-n)", "nuance", "Es gibt immer neue Nuancen zu entdecken."),
        _v("wenngleich", "even though / although (formal)", "Wenngleich schwierig, ist es machbar."),
        _v("bestreiten", "to deny / dispute", "Das lässt sich kaum bestreiten."),
        _v("der Weg (Wege)", "path / way", "Das ist der Weg zur Meisterschaft."),
    ],
    "exercises": [
        _ex_fib(
            "C2 final fill-in synthesis",
            ["Das von Experten ___ Problem wird nun endlich angegangen. (Partizip II: diskutieren)", "Wenngleich spät, ___ der Schritt zu begrüßen.", "Es ___ verfehlt anzunehmen, die Reise ___ hier zu Ende. (sein x2)"],
            ["diskutierte", "ist", "wäre / sei"],
        ),
        _ex_mc(
            "C2 mastery check: all levels",
            [
                ("Which is correct Konjunktiv I of 'haben' (3. Person Plural) for reported speech?", ["hätten", "haben", "hatten", "habe"], 0),
                ("'Das lässt sich kaum bestreiten.' – What construction is this?", ["Passive", "Modal + infinitive", "Sich-lassen passive equivalent", "Reflexive"], 2),
                ("Which demonstrates highest register precision?", ["Ich hab keine Ahnung.", "Ich weiß es nicht.", "Mir liegen dazu keine Informationen vor.", "Keine Ahnung."], 2),
            ],
        ),
        _ex_tr(
            "C2 synthesis translation",
            [
                ("The long-discussed problem is now finally being addressed – which, although late, is to be welcomed.", "Das lange diskutierte Problem wird nun endlich angegangen – was, wenngleich spät, zu begrüßen ist."),
                ("It would be mistaken to assume the journey ends here.", "Es wäre verfehlt anzunehmen, die Reise sei hier zu Ende."),
                ("Language is thought. Thinking in German changes what you think.", "Sprache ist Denken. Auf Deutsch zu denken verändert, was man denkt."),
            ],
        ),
        _ex_arr(
            "Final C2 complex sentence",
            [
                (["Es", "wäre", "verfehlt", "anzunehmen", "die", "Reise", "sei", "hier", "zu", "Ende"], "Es wäre verfehlt anzunehmen, die Reise sei hier zu Ende."),
            ],
        ),
        _ex_sp(
            "C2 final tasks",
            ["Give a 3-minute reflective speech on your German learning journey. Use all C2 resources.", "Write a Feuilleton of 200 words on the experience of learning a language.", "Discuss: What does it mean to truly master a language – and is it ever finished?"],
        ),
    ],
}
'''

for num in range(156, 166):
    tag = f"LESSON_{num}"
    if tag in existing:
        print(f"SKIP {tag} already exists")
        APPEND = re.sub(rf"\nLESSON_{num}\s*=.*?(?=\nLESSON_|\Z)", "", APPEND, flags=re.DOTALL)

SEEDS.write_text(src + APPEND, encoding="utf-8")

verify = SEEDS.read_text(encoding="utf-8")
found = sorted(set(re.findall(r"^(LESSON_\d+)\s*=", verify, re.MULTILINE)),
               key=lambda x: int(x.split("_")[1]))
print(f"Total lessons: {len(found)}, range: {found[0]}-{found[-1]}")

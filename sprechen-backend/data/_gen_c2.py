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

LESSON_146 = {
    "title": "Mastery of German Idioms and Fixed Expressions",
    "level": "C2",
    "scenario": "language_mastery",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Recognize and use advanced German idioms in appropriate contexts",
        "Understand the etymology and cultural background of key idioms",
        "Avoid false cognates and deceptive idioms at C2 level",
        "Produce idiomatic German that sounds fully native",
    ],
    "cultural_note": "German has a rich stock of idiomatic expressions rooted in agriculture, crafts, and history. Many idioms differ completely from English equivalents. Mastering them is the hallmark of a C2 speaker and signals deep cultural integration.",
    "grammar_focus": _gex(
        "Idiom Structure and Register",
        "Idioms are fixed expressions whose meaning cannot be deduced from individual words. They exist in all registers: formal (auf dem Prüfstand stehen), neutral (auf den Punkt kommen), and colloquial (jemandem auf den Wecker gehen).",
        "'das Handtuch werfen' (to throw in the towel) / 'auf Herz und Nieren prüfen' (to put to the test thoroughly)",
        ["Verb + Noun idioms: Klartext reden / Brücken bauen / Öl ins Feuer gießen", "Fixed prepositional phrases: auf den ersten Blick / im Großen und Ganzen / nach wie vor", "Comparative idioms: klar wie Kloßbrühe / blind wie ein Maulwurf"],
        ["Im Großen und Ganzen war die Veranstaltung ein Erfolg.", "Er redet immer um den heißen Brei herum.", "Lass uns Nägel mit Köpfen machen!"],
    ),
    "dialogue": [
        _t("native_speaker", "Na, wie läuft das Projekt? Ihr seid doch schon ewig dran.", "So, how is the project going? You've been at it for ages."),
        _t("learner", "Im Großen und Ganzen gut. Aber wir drehen uns manchmal im Kreis.", "By and large good. But sometimes we go round in circles."),
        _t("native_speaker", "Das kenne ich. Manchmal muss man einfach Nägel mit Köpfen machen.", "I know that. Sometimes you just have to get things done properly."),
        _t("learner", "Genau. Unser Chef redet immer um den heißen Brei herum.", "Exactly. Our boss always beats around the bush."),
        _t("native_speaker", "Das nervt. Hat er das Handtuch schon geworfen?", "That's annoying. Has he thrown in the towel yet?"),
        _t("learner", "Nein, aber er gießt manchmal Öl ins Feuer.", "No, but he sometimes pours oil on the fire."),
        _t("native_speaker", "Da musst du Klartext reden.", "You need to speak plainly."),
        _t("learner", "Leichter gesagt als getan!", "Easier said than done!"),
    ],
    "vocabulary_list": [
        _v("Nägel mit Köpfen machen", "to do things properly / get things done", "Lass uns endlich Nägel mit Köpfen machen."),
        _v("um den heißen Brei herumreden", "to beat around the bush", "Hör auf, um den heißen Brei herumzureden."),
        _v("Klartext reden", "to speak plainly / straight", "Ich rede jetzt Klartext."),
        _v("Öl ins Feuer gießen", "to add fuel to the fire", "Dein Kommentar hat nur Öl ins Feuer gegossen."),
        _v("das Handtuch werfen", "to throw in the towel", "Er warf nach drei Runden das Handtuch."),
        _v("im Großen und Ganzen", "by and large / on the whole", "Im Großen und Ganzen bin ich zufrieden."),
        _v("sich im Kreis drehen", "to go round in circles", "Die Diskussion dreht sich im Kreis."),
        _v("nach wie vor", "as ever / still", "Das Problem besteht nach wie vor."),
        _v("auf den ersten Blick", "at first glance", "Auf den ersten Blick sieht es einfach aus."),
        _v("auf Herz und Nieren prüfen", "to put through the wringer / examine thoroughly", "Der Kandidat wurde auf Herz und Nieren geprüft."),
    ],
    "exercises": [
        _ex_mc(
            "Match the idiom to its meaning",
            [
                ("'Um den heißen Brei herumreden' means:", ["To speak directly", "To beat around the bush", "To pour oil on the fire", "To throw in the towel"], 1),
                ("'Nägel mit Köpfen machen' means:", ["To do things half-heartedly", "To hammer nails", "To do things properly", "To make mistakes"], 2),
                ("'Das Handtuch werfen' means:", ["To clean up", "To give up / throw in the towel", "To start a fight", "To celebrate"], 1),
            ],
        ),
        _ex_fib(
            "Complete the idioms",
            ["Er redet immer um den heißen ___ herum.", "Lass uns ___ mit Köpfen machen.", "Dein Verhalten gießt nur ___ ins Feuer."],
            ["Brei", "Nägel", "Öl"],
        ),
        _ex_tr(
            "Translate using German idioms",
            [
                ("By and large, the conference was a success.", "Im Großen und Ganzen war die Konferenz ein Erfolg."),
                ("Stop beating around the bush and speak plainly.", "Hör auf, um den heißen Brei herumzureden, und rede Klartext."),
                ("The problem still exists today.", "Das Problem besteht nach wie vor."),
            ],
        ),
        _ex_arr(
            "Reconstruct the idiomatic sentence",
            [
                (["Er", "redet", "immer", "um", "den", "heißen", "Brei", "herum"], "Er redet immer um den heißen Brei herum."),
                (["Im", "Großen", "und", "Ganzen", "war", "es", "ein", "Erfolg"], "Im Großen und Ganzen war es ein Erfolg."),
            ],
        ),
        _ex_sp(
            "Use idioms in context",
            ["Use three of today's idioms in a short story about a difficult project.", "Explain the meaning of 'Öl ins Feuer gießen' to a beginner in your own words.", "What English idioms have German equivalents? Compare them."],
        ),
    ],
}

LESSON_147 = {
    "title": "Mastering Register: From Colloquial to Formal",
    "level": "C2",
    "scenario": "register_mastery",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Consciously shift between colloquial, neutral, and formal German registers",
        "Rewrite the same content in multiple registers accurately",
        "Understand register-specific vocabulary, syntax, and pragmatics",
        "Identify and correct register mismatches in written and spoken German",
    ],
    "cultural_note": "Register mastery is the clearest marker of a C2 speaker. Germans are highly sensitive to register mismatches – using overly formal language in casual contexts sounds stiff, while informal language in professional contexts seems unprofessional or rude.",
    "grammar_focus": _gex(
        "Register Markers in German",
        "Each register has characteristic features: colloquial uses shortened forms, slang, and loose syntax; formal uses passive, nominalisation, and complex subordination; academic adds hedging, impersonal constructions, and technical lexis.",
        "Colloquial: 'Ich hab keine Ahnung.' / Neutral: 'Ich weiß es nicht.' / Formal: 'Darüber liegen mir keine Informationen vor.'",
        ["Colloquial: pronoun drop, contracted verbs, modal particles (ja, halt, eben, doch)", "Formal: nominalization, passive, extended noun phrases, bureaucratic set phrases", "Academic: hedging (dürfte, scheint), impersonal (es wird angenommen), Latin-derived vocabulary"],
        ["Colloquial: 'Das klappt nie.' / Formal: 'Eine Realisierung erscheint unter den gegebenen Umständen nicht zielführend.'", "Colloquial: 'Ich ruf dich an.' / Formal: 'Ich werde Sie telefonisch kontaktieren.'"],
    ),
    "dialogue": [
        _t("trainer", "Heute üben wir Registerwechsel. Ich gebe Ihnen einen Satz – Sie reformulieren ihn in einem anderen Register.", "Today we practise register shifts. I give you a sentence – you reformulate it in a different register."),
        _t("candidate", "Gut. Bitte fangen Sie an.", "Good. Please begin."),
        _t("trainer", "Colloquial: 'Ich hab total keine Lust auf die Sitzung.' – Bitte formal.", "Colloquial: 'I really don't feel like the meeting.' – Please formal."),
        _t("candidate", "Formal: 'Ich sehe mich derzeit außerstande, an der Sitzung teilzunehmen.'", "Formal: 'I currently find myself unable to attend the meeting.'"),
        _t("trainer", "Sehr gut. Jetzt andersherum. Formal: 'Die Unterlagen wurden fristgerecht eingereicht.' – Colloquial.", "Very good. Now the other way round. Formal: 'The documents were submitted on time.' – Colloquial."),
        _t("candidate", "Colloquial: 'Ich hab die Sachen pünktlich abgegeben.'", "Colloquial: 'I handed the stuff in on time.'"),
        _t("trainer", "Gut. 'Sachen' ist sehr colloquial – 'Unterlagen' wäre neutral.", "Good. 'Sachen' is very colloquial – 'Unterlagen' would be neutral."),
        _t("candidate", "Verstanden. Die Grenze zwischen neutral und colloquial ist fließend.", "Understood. The boundary between neutral and colloquial is fluid."),
    ],
    "vocabulary_list": [
        _v("das Register (-)", "register (linguistic)", "Jedes Register hat seine eigenen Regeln."),
        _v("fließend", "fluid / fluent", "Der Übergang ist fließend."),
        _v("der Registerwechsel (-)", "register shift", "Registerwechsel erfordert Bewusstsein."),
        _v("außerstande sein", "to be unable to", "Ich sehe mich außerstande, zu helfen."),
        _v("fristgerecht", "on time / within the deadline", "Die Unterlagen wurden fristgerecht eingereicht."),
        _v("die Nominaliserung (-en)", "nominalization", "Nominalisierungen sind typisch für formelles Deutsch."),
        _v("die Reformulierung (-en)", "reformulation", "Reformulierung zeigt Sprachkompetenz."),
        _v("pragmatisch", "pragmatic", "Pragmatisches Wissen ist für Register nötig."),
        _v("der Registermissklang", "register mismatch", "Ein Registermissklang wirkt unprofessionell."),
        _v("zielführend", "productive / leading to the goal (formal)", "Diese Maßnahme ist nicht zielführend."),
    ],
    "exercises": [
        _ex_fib(
            "Rewrite in the requested register",
            ["Colloquial: 'Ich hab keine Ahnung.' → Formal: 'Darüber ___ mir keine ___ vor.'", "Formal: 'Die Realisierung erscheint nicht zielführend.' → Colloquial: 'Das ___ nie.'", "Neutral: 'Ich weiß nicht.' → Academic: 'Darüber ___ keine gesicherten Erkenntnisse vor.'"],
            ["liegen / Informationen", "klappt", "liegen"],
        ),
        _ex_mc(
            "Identify the register",
            [
                ("'Ich ruf dich dann mal an.' – What register?", ["Formal", "Academic", "Colloquial", "Bureaucratic"], 2),
                ("'In Anbetracht der vorliegenden Sachlage erscheint ein Aufschub nicht vertretbar.' – What register?", ["Colloquial", "Neutral", "Formal/Bureaucratic", "Academic"], 2),
                ("'Es wird angenommen, dass...' – What register?", ["Colloquial", "Academic/Formal", "Neutral", "Informal"], 1),
            ],
        ),
        _ex_tr(
            "Translate into the specified German register",
            [
                ("I can't make it to the meeting today. (Formal)", "Ich sehe mich heute außerstande, an der Sitzung teilzunehmen."),
                ("The documents have been submitted. (Colloquial)", "Ich hab die Unterlagen abgegeben."),
                ("Further research is required. (Academic)", "Weiterer Forschungsbedarf besteht in diesem Bereich."),
            ],
        ),
        _ex_arr(
            "Order from most colloquial to most formal",
            [
                (["'Das klappt nie.'", "'Eine Realisierung erscheint nicht zielführend.'", "'Das funktioniert nicht.'"], "'Das klappt nie.' → 'Das funktioniert nicht.' → 'Eine Realisierung erscheint nicht zielführend.'"),
            ],
        ),
        _ex_sp(
            "Register shifting practice",
            ["Describe your commute to work in three different registers: colloquial, neutral, formal.", "Your boss sends you a very formal email – rewrite it in neutral register.", "In conversation, practise shifting register mid-dialogue deliberately."],
        ),
    ],
}

LESSON_148 = {
    "title": "Advanced Syntax: Inversion, Cleft Sentences, and Focus",
    "level": "C2",
    "scenario": "advanced_grammar",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Use syntactic inversion for emphasis and information structuring",
        "Produce cleft sentences (Spaltungssätze) for focus and contrast",
        "Understand topic-comment structure and given-new information ordering",
        "Recognise and produce marked word orders for stylistic effect",
    ],
    "cultural_note": "German word order flexibility is a key resource for information structuring. Unlike English, German can front almost any element for emphasis without sounding ungrammatical. Mastering this is crucial for sounding natural and expressive in German.",
    "grammar_focus": _gex(
        "Inversion and Focus in German",
        "German allows fronting of adverbials, objects, and predicates by placing them in the Vorfeld (pre-verb position). This creates emphasis and signals topic-comment structure. Cleft sentences ('Es ist X, der/die/das...') isolate and focus one element.",
        "Gestern habe ich ihn gesehen. / Es war Peter, der das gesagt hat. (cleft) / Das Buch hat er gelesen, nicht den Artikel.",
        ["Vorfeld inversion: Gestern / Deshalb / Den Brief / Gelesen hat er...", "Cleft: Es ist/war [X], der/die/das...", "Contrastive focus: Das Buch hat er gelesen, nicht den Artikel."],
        ["Erst jetzt verstehe ich, was gemeint war.", "Es war die falsche Entscheidung, die alles verändert hat.", "Gelobt wurde sie für ihre Arbeit, kritisiert für ihren Stil."],
    ),
    "dialogue": [
        _t("author", "In diesem Kapitel wollte ich die Spannung bewusst aufbauen.", "In this chapter I wanted to deliberately build tension."),
        _t("editor", "Das merkt man. Besonders der erste Satz – da steckt die ganze Energie.", "You can tell. Especially the first sentence – all the energy is in it."),
        _t("author", "Ich habe ihn mehrfach umgestellt. Erst war es: 'Er öffnete die Tür langsam.'", "I restructured it several times. First it was: 'He opened the door slowly.'"),
        _t("editor", "Und jetzt: 'Langsam öffnete er die Tür.' Viel besser – das Adverb vorne erzeugt Spannung.", "And now: 'Slowly he opened the door.' Much better – the adverb at the front creates tension."),
        _t("author", "Genau. Und im Schlusskapitel habe ich Spaltungssätze verwendet.", "Exactly. And in the final chapter I used cleft sentences."),
        _t("editor", "Zum Beispiel?", "For example?"),
        _t("author", "'Es war ihre Stimme, die ihn verriet, nicht ihr Gesicht.'", "'It was her voice that gave her away, not her face.'"),
        _t("editor", "Stark. Das setzt den Kontrast scharf.", "Powerful. That sets the contrast sharply."),
    ],
    "vocabulary_list": [
        _v("die Inversion (-en)", "inversion", "Inversion verändert den Satzschwerpunkt."),
        _v("das Vorfeld", "pre-verbal position (syntax)", "Im Vorfeld steht das Thema oder der Fokus."),
        _v("der Spaltungssatz (Spaltungssätze)", "cleft sentence", "Spaltungssätze dienen der Fokussierung."),
        _v("der Kontrast (-e)", "contrast", "Kontraste machen Texte lebendiger."),
        _v("die Spannung (-en)", "tension / suspense", "Der Autor baut Spannung durch Syntax auf."),
        _v("der Schwerpunkt (Schwerpunkte)", "focal point / emphasis", "Der Satzschwerpunkt liegt auf dem Vorfeld-Element."),
        _v("umstellen", "to restructure / rearrange", "Er stellte den Satz mehrfach um."),
        _v("verraten", "to betray / reveal", "Ihre Stimme verriet sie.", ),
        _v("markiert (Syntax)", "marked (word order)", "Eine markierte Wortstellung erzeugt Fokus."),
        _v("das Thema-Rhema-Prinzip", "topic-comment principle", "Das Thema-Rhema-Prinzip ordnet Information."),
    ],
    "exercises": [
        _ex_fib(
            "Rewrite with inversion for emphasis",
            ["'Er öffnete die Tür langsam.' → '___ öffnete er die Tür.'", "'Ich habe ihn gestern gesehen.' → '___ habe ich ihn gesehen.'", "'Sie hat den Preis wegen ihrer Arbeit gewonnen.' → '___ hat sie den Preis gewonnen.'"],
            ["Langsam", "Gestern", "Wegen ihrer Arbeit"],
        ),
        _ex_mc(
            "Identify the syntactic effect",
            [
                ("'Gelobt wurde sie für ihre Arbeit, kritisiert für ihren Stil.' – What structure is this?", ["Simple statement", "Cleft sentence", "Parallel contrastive inversion", "Passive only"], 2),
                ("'Es war Peter, der das gesagt hat.' – What does this do?", ["States a fact neutrally", "Focuses on Peter as the one who said it", "Denies Peter said it", "Uses indirect speech"], 1),
                ("What is in the 'Vorfeld' in 'Gestern habe ich ihn gesehen'?", ["ich", "ihn", "Gestern", "gesehen"], 2),
            ],
        ),
        _ex_tr(
            "Translate using inversion or cleft sentences",
            [
                ("It was her voice that gave her away, not her face.", "Es war ihre Stimme, die sie verriet, nicht ihr Gesicht."),
                ("Only now do I understand what was meant.", "Erst jetzt verstehe ich, was gemeint war."),
                ("Praised for her work, criticised for her style.", "Gelobt wurde sie für ihre Arbeit, kritisiert für ihren Stil."),
            ],
        ),
        _ex_arr(
            "Reorder for maximum emphasis",
            [
                (["Erst", "jetzt", "verstehe", "ich", "was", "gemeint", "war"], "Erst jetzt verstehe ich, was gemeint war."),
            ],
        ),
        _ex_sp(
            "Experiment with word order",
            ["Take a paragraph you've written and restructure three sentences for emphasis using inversion.", "Write two cleft sentences contrasting two things in your field or area of interest.", "Explain to a partner why you chose a specific word order in a sentence."],
        ),
    ],
}

LESSON_149 = {
    "title": "German Philosophical and Abstract Language",
    "level": "C2",
    "scenario": "philosophy_seminar",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Read and produce abstract philosophical argument in German",
        "Use German abstract nouns and nominalization to the highest degree",
        "Understand key philosophical concepts in their German formulation",
        "Engage with Kant, Hegel, and Nietzsche terminology in German",
    ],
    "cultural_note": "German philosophy is untranslatable at its deepest level – concepts like Dasein, Weltanschauung, Zeitgeist, Angst, Aufhebung, and Bildung carry nuances that resist English equivalents. Reading philosophy in German opens unique intellectual territory.",
    "grammar_focus": _gex(
        "Philosophical Nominalization and Abstract Language",
        "German philosophical writing maximizes nominalization: turning verbs and adjectives into abstract nouns. This compresses complex relationships into noun phrases that can then be modified and related to one another.",
        "Das Sein (being) / das Werden (becoming) / die Aufhebung (sublation/cancellation-and-preservation) / die Erscheinung (appearance/phenomenon)",
        ["Infinitive as noun: das Denken, das Sein, das Werden, das Wollen", "Derivation: die Freiheit, die Wahrheit, die Wirklichkeit, die Notwendigkeit", "Compound abstracts: die Weltanschauung, das Selbstbewusstsein, das Zeitbewusstsein"],
        ["Das Sein des Seienden ist das grundlegende Problem der Metaphysik.", "Die Aufhebung vereint Negation und Bewahrung in einer dialektischen Bewegung.", "Das Subjekt konstituiert sich durch das Andere seiner selbst."],
    ),
    "dialogue": [
        _t("philosopher", "Hegel unterscheidet zwischen dem An-sich-Sein, dem Für-sich-Sein und dem An-und-für-sich-Sein.", "Hegel distinguishes between being-in-itself, being-for-itself, and being-in-and-for-itself."),
        _t("student", "Das klingt zunächst abstrakt. Können Sie das anhand eines Beispiels erläutern?", "That sounds abstract at first. Can you explain it with an example?"),
        _t("philosopher", "Das Bewusstsein beginnt als An-sich – unreflektiert. Im Für-sich erkennt es sich selbst.", "Consciousness begins as in-itself – unreflected. In being-for-itself it recognises itself."),
        _t("student", "Also Selbstbewusstsein als Für-sich-Sein?", "So self-consciousness as being-for-itself?"),
        _t("philosopher", "Genau. Und die Aufhebung – Hegels Schlüsselbegriff – bewahrt und negiert zugleich.", "Exactly. And Aufhebung – Hegel's key concept – preserves and negates simultaneously."),
        _t("student", "Das erinnert mich an den Begriff der Freiheit bei Kant – Freiheit als Selbstgesetzgebung.", "That reminds me of Kant's concept of freedom – freedom as self-legislation."),
        _t("philosopher", "Sehr guter Zusammenhang. Beide Denker setzen das Subjekt ins Zentrum.", "Very good connection. Both thinkers place the subject at the centre."),
        _t("student", "Und Nietzsche kritisiert genau das als Ideologie des Subjekts.", "And Nietzsche critiques precisely that as the ideology of the subject."),
    ],
    "vocabulary_list": [
        _v("das Dasein", "existence / being-there (Heidegger)", "Heidegger analysiert das Dasein des Menschen."),
        _v("die Aufhebung", "sublation (Hegel: negate, preserve, lift to higher level)", "Die Aufhebung ist ein zentraler Hegelscher Begriff."),
        _v("das Selbstbewusstsein", "self-consciousness / self-awareness", "Hegel entwickelt eine Theorie des Selbstbewusstseins."),
        _v("die Weltanschauung", "worldview", "Jede Kultur hat ihre eigene Weltanschauung."),
        _v("die Selbstgesetzgebung", "self-legislation / autonomy (Kant)", "Freiheit bedeutet für Kant Selbstgesetzgebung."),
        _v("das Werden", "becoming / process of becoming", "Nietzsche betont das Werden gegenüber dem Sein."),
        _v("die Erscheinung (-en)", "appearance / phenomenon", "Kant unterscheidet Erscheinung und Ding an sich."),
        _v("konstituieren", "to constitute / make up", "Das Subjekt konstituiert die Wirklichkeit."),
        _v("die Negation (-en)", "negation", "Die dialektische Negation ist produktiv."),
        _v("zugleich", "simultaneously / at the same time", "Die Aufhebung negiert und bewahrt zugleich."),
    ],
    "exercises": [
        _ex_mc(
            "Match concept to philosopher",
            [
                ("'Aufhebung' (sublation) is associated with:", ["Kant", "Nietzsche", "Hegel", "Schopenhauer"], 2),
                ("'Selbstgesetzgebung' (autonomy) is Kant's definition of:", ["Knowledge", "Freedom", "Reason", "Duty"], 1),
                ("'Dasein' as a philosophical concept is central to:", ["Hegel", "Kant", "Nietzsche", "Heidegger"], 3),
            ],
        ),
        _ex_fib(
            "Fill in the philosophical terms",
            ["Das ___ vereint Negation und Bewahrung. (Hegel's key concept)", "Kant unterscheidet ___ und Ding an sich.", "Das Subjekt ___ sich durch die Begegnung mit dem Anderen."],
            ["Aufhebung", "Erscheinung", "konstituiert"],
        ),
        _ex_tr(
            "Translate philosophical sentences",
            [
                ("The subject constitutes itself through the encounter with the other.", "Das Subjekt konstituiert sich durch die Begegnung mit dem Anderen."),
                ("Freedom, for Kant, means self-legislation.", "Freiheit bedeutet für Kant Selbstgesetzgebung."),
                ("Hegel's Aufhebung simultaneously negates and preserves.", "Hegels Aufhebung negiert und bewahrt zugleich."),
            ],
        ),
        _ex_arr(
            "Order the philosophical sentence",
            [
                (["Die", "Aufhebung", "vereint", "Negation", "und", "Bewahrung", "in", "einer", "dialektischen", "Bewegung"], "Die Aufhebung vereint Negation und Bewahrung in einer dialektischen Bewegung."),
            ],
        ),
        _ex_sp(
            "Philosophical discussion",
            ["Explain Hegel's concept of Aufhebung in your own words in German.", "How does Nietzsche's critique of the subject differ from Kant's view of freedom?", "Choose a philosophical concept from today's lesson and explain why it is difficult to translate."],
        ),
    ],
}

LESSON_150 = {
    "title": "Advanced Writing: Feuilleton and Literary Journalism",
    "level": "C2",
    "scenario": "literary_journalism",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Write in the German Feuilleton style – essayistic, literary, opinionated",
        "Blend argumentation with literary technique in non-fiction prose",
        "Use metaphor, allusion, and cultural reference in journalistic writing",
        "Understand the tradition of German literary journalism",
    ],
    "cultural_note": "The Feuilleton is a distinctly German and Austrian journalistic tradition: a short, essayistic piece that mixes opinion, cultural commentary, and literary technique. It appears in the arts section of major newspapers (FAZ, Süddeutsche) and demands the highest level of language mastery.",
    "grammar_focus": _gex(
        "Essayistic Prose Style",
        "Feuilleton prose uses varied sentence length (long and short in alternation), literary devices (metaphor, allusion, parenthesis), direct address to the reader, and a personal, reflective first person. It avoids both news-register flatness and academic impersonality.",
        "Man könnte meinen, die Welt sei eine einzige Bühne. Und vielleicht stimmt das sogar. (Short following long, personal reflection)",
        ["Varied rhythm: long complex sentence → short sentence punch", "Direct address: 'Stellen Sie sich vor...' / 'Man denke nur an...'", "Literary allusion: 'Um mit Goethe zu sprechen...' / 'Das erinnert an Kafkas Verwandlung'"],
        ["Das Paradoxe an der Freiheit ist, dass sie uns am schwersten fällt, wenn wir sie haben.", "Man muss kein Pessimist sein, um zu erkennen: Die einfachen Antworten sind meist falsch.", "Es gibt Momente – selten, aber unvergesslich –, in denen sich alles verschiebt."],
    ),
    "dialogue": [
        _t("editor", "Ihr Text hat Substanz, aber er liest sich noch zu akademisch für den Feuilleton.", "Your text has substance, but it still reads too academically for the Feuilleton."),
        _t("writer", "Was fehlt ihm?", "What does it lack?"),
        _t("editor", "Rhythmus. Wechseln Sie zwischen langen, verschlungenen Sätzen und kurzen Schlägen.", "Rhythm. Alternate between long, winding sentences and short punches."),
        _t("writer", "Und inhaltlich?", "And content-wise?"),
        _t("editor", "Bringen Sie sich selbst ein. Ein guter Feuilleton spricht aus einer persönlichen Perspektive.", "Bring yourself in. A good Feuilleton speaks from a personal perspective."),
        _t("writer", "Also mehr 'Ich'?", "So more 'I'?"),
        _t("editor", "Ja, aber nicht nabelschauend. Persönlich, aber mit Anspruch auf Allgemeingültigkeit.", "Yes, but not navel-gazing. Personal, but with a claim to universal relevance."),
        _t("writer", "Das ist der schmalste Grat, den ich kenne.", "That is the narrowest line I know."),
    ],
    "vocabulary_list": [
        _v("das Feuilleton (-s)", "Feuilleton (literary-journalistic essay)", "Das Feuilleton erscheint im Kulturteil der Zeitung."),
        _v("essayistisch", "essayistic", "Der Stil ist essayistisch und reflektiv."),
        _v("der Anspruch (Ansprüche)", "claim / demand / aspiration", "Sein Feuilleton hat Anspruch auf Allgemeingültigkeit."),
        _v("die Allgemeingültigkeit", "universal validity / general relevance", "Persönliche Erfahrung kann Allgemeingültigkeit beanspruchen."),
        _v("nabelschauend", "navel-gazing / self-absorbed", "Nabelschauende Texte interessieren wenige."),
        _v("der Rhythmus (Rhythmen)", "rhythm", "Prosarhythmus ist ein Kunstmittel."),
        _v("die Parenthese (-n)", "parenthesis / parenthetical remark", "Parenthesen bremsen und vertiefen den Lesefluss."),
        _v("der Grat (Grate)", "ridge / narrow line", "Das ist ein schmaler Grat."),
        _v("reflektiv", "reflective", "Feuilletons sind reflektive Texte."),
        _v("die Allusion (-en)", "allusion", "Literarische Allusionen bereichern den Text."),
    ],
    "exercises": [
        _ex_mc(
            "Feuilleton style: what fits?",
            [
                ("Which sentence best fits a Feuilleton opening?", ["On 5 March 2024, the conference took place.", "Man könnte meinen, die Zeit stehe still. Sie tut es nicht.", "The conference addressed several issues.", "Es wird untersucht, ob..."], 1),
                ("What is characteristic of Feuilleton prose?", ["Long academic sentences only", "Short news-style sentences only", "Alternation of long and short sentences with personal voice", "Passive constructions throughout"], 2),
                ("What does 'nabelschauend' mean?", ["Universal in scope", "Self-absorbed / navel-gazing", "Literary and allusive", "Direct and argumentative"], 1),
            ],
        ),
        _ex_fib(
            "Complete the Feuilleton-style sentences",
            ["Das Paradoxe an der Freiheit ist, dass sie uns am ___ fällt, wenn wir sie ___ (haben / schwersten).", "Es gibt Momente – selten, aber ___ –, in denen sich alles verschiebt.", "Man muss kein Pessimist sein, um zu ___: Die einfachen Antworten sind meist ___."],
            ["schwersten / haben", "unvergesslich", "erkennen / falsch"],
        ),
        _ex_tr(
            "Translate in Feuilleton style",
            [
                ("The strangest thing about freedom is that it is hardest when we have it.", "Das Paradoxe an der Freiheit ist, dass sie uns am schwersten fällt, wenn wir sie haben."),
                ("There are moments – rare but unforgettable – when everything shifts.", "Es gibt Momente – selten, aber unvergesslich –, in denen sich alles verschiebt."),
            ],
        ),
        _ex_arr(
            "Order the Feuilleton sentences by stylistic effect",
            [
                (["Alles war ruhig. Die Stadt schlief. Nur er nicht.", "Er konnte nicht schlafen, weil ihn die Gedanken, die sich wie Wellen um eine Frage drehten, die er seit Jahren nicht zu beantworten vermochte, nicht losließen."], "Long sentence first → short punches OR short → long for build-up"),
            ],
        ),
        _ex_sp(
            "Write your own Feuilleton",
            ["Write a 200-word Feuilleton on any topic. Include: personal voice, one metaphor, alternating sentence length.", "Read your piece aloud. Where does the rhythm work well? Where does it feel flat?", "Discuss: What is the difference between a Feuilleton and an opinion column in your country?"],
        ),
    ],
}

LESSON_151 = {
    "title": "Advanced Grammar: Genitive Absolute and Rare Constructions",
    "level": "C2",
    "scenario": "advanced_grammar",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Recognize and use archaic and literary genitive constructions",
        "Understand double infinitive constructions and perception verbs",
        "Use 'lassen' in its full range of causative and passive-equivalent uses",
        "Master rare but important constructions in literary and formal German",
    ],
    "cultural_note": "C2 German includes awareness of archaic, literary, and regional constructions that appear in high-quality prose but are rarely taught. Recognising these separates a very advanced learner from a native-like speaker.",
    "grammar_focus": _gex(
        "Lassen: Causative and Passive Equivalent",
        "'Lassen' + infinitive has several uses: causative (to have something done), permissive (to let something happen), and a passive-equivalent construction (sich lassen + infinitive = can be done). All these are common in sophisticated German.",
        "Er lässt das Auto reparieren. (He is having the car repaired.) / Das lässt sich nicht ändern. (That cannot be changed.) / Sie ließ ihn nicht reden. (She didn't let him speak.)",
        ["Causative: etw. machen lassen – have sth done", "Permissive: jdn etw. tun lassen – let sb do sth", "Passive equivalent: sich + lassen + Infinitiv – can be done (Das lässt sich lösen.)"],
        ["Das Problem lässt sich auf verschiedene Arten lösen.", "Ich lasse mir die Haare schneiden.", "Der Chef ließ die Mitarbeiter früher gehen.", "Das lässt tief blicken. (That is revealing.)"],
    ),
    "dialogue": [
        _t("author", "In diesem Absatz verwende ich 'lassen' auf drei verschiedene Arten.", "In this paragraph I use 'lassen' in three different ways."),
        _t("reader", "Interessant. Zeigen Sie mal.", "Interesting. Show me."),
        _t("author", "Erstens: 'Er ließ das Manuskript prüfen' – er hat jemanden beauftragt.", "First: 'He had the manuscript checked' – he commissioned someone."),
        _t("reader", "Kausativ. Was noch?", "Causative. What else?"),
        _t("author", "Zweitens: 'Er ließ sie reden' – er hat sie nicht unterbrochen.", "Second: 'He let her speak' – he didn't interrupt her."),
        _t("reader", "Permissiv. Und drittens?", "Permissive. And third?"),
        _t("author", "'Das lässt sich nicht leugnen' – es ist nicht zu leugnen.", "'That cannot be denied' – it is not to be denied."),
        _t("reader", "Passivequivalent. Sehr elegant.", "Passive equivalent. Very elegant."),
    ],
    "vocabulary_list": [
        _v("kausativ", "causative", "Eine kausative Konstruktion lässt jemanden etwas tun."),
        _v("permissiv", "permissive", "Permissives 'lassen' erlaubt etwas."),
        _v("leugnen", "to deny", "Das lässt sich nicht leugnen."),
        _v("beauftragen", "to commission / instruct", "Er beauftragte einen Anwalt."),
        _v("tief blicken lassen", "to be revealing (lit: to allow a deep look)", "Das lässt tief blicken."),
        _v("das Doppelinfintiv", "double infinitive construction", "Nach 'lassen' steht Doppelinfintiv im Perfekt."),
        _v("unterbrechen", "to interrupt", "Er ließ sie sprechen, ohne sie zu unterbrechen."),
        _v("das Manuskript (-e)", "manuscript", "Das Manuskript wurde lektoriert."),
        _v("der Absatz (Absätze)", "paragraph / section", "Dieser Absatz ist besonders dicht."),
        _v("elegant", "elegant", "Eine elegante Konstruktion klingt natürlich."),
    ],
    "exercises": [
        _ex_fib(
            "Identify the type of 'lassen' construction",
            ["'Er lässt das Auto reparieren.' → ___ lassen (causative/permissive/passive-equiv)", "'Sie ließ ihn nicht reden.' → ___ lassen", "'Das lässt sich nicht ändern.' → ___ lassen"],
            ["causative", "permissive", "passive-equivalent"],
        ),
        _ex_mc(
            "Choose the correct 'lassen' construction",
            [
                ("'The problem can be solved.' → Which German sentence is correct?", ["Das Problem wird gelöst.", "Das Problem lässt sich lösen.", "Das Problem ist lösbar.", "Das Problem kann lösen."], 1),
                ("'She had her photo taken.' → Correct form?", ["Sie ließ ihr Foto nehmen.", "Sie ließ sich fotografieren.", "Sie wurde fotografiert lassen.", "Sie ließ sich fotografieren lassen."], 1),
                ("'He let her finish speaking.' → Correct?", ["Er ließ sie reden fertig.", "Er ließ sie ausreden.", "Er ließ sie sprechen fertig.", "Er ließ ausreden sie."], 1),
            ],
        ),
        _ex_tr(
            "Translate using 'lassen' constructions",
            [
                ("That cannot be denied.", "Das lässt sich nicht leugnen."),
                ("She had the documents checked.", "Sie ließ die Dokumente prüfen."),
                ("He let his colleague finish speaking.", "Er ließ seinen Kollegen ausreden."),
            ],
        ),
        _ex_arr(
            "Reconstruct lassen sentences",
            [
                (["Das", "lässt", "sich", "auf", "verschiedene", "Weisen", "interpretieren"], "Das lässt sich auf verschiedene Weisen interpretieren."),
            ],
        ),
        _ex_sp(
            "Use 'lassen' in extended sentences",
            ["Describe three things you had done recently using causative 'lassen'.", "Give two examples of 'sich lassen' constructions from your field of work or study.", "Explain the difference between 'Das kann gelöst werden' and 'Das lässt sich lösen'."],
        ),
    ],
}

LESSON_152 = {
    "title": "Spoken German at Native Speed: Reduction and Liaison",
    "level": "C2",
    "scenario": "phonetics_and_fluency",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand and produce connected speech reductions in German",
        "Recognize elision, assimilation, and liaison in native speech",
        "Achieve near-native rhythm and prosody in German",
        "Understand dialect and regional variation at the phonological level",
    ],
    "cultural_note": "Native German speech is radically different from written German. Syllables are dropped, words merge, and forms contract in ways not taught in standard courses. A C2 speaker understands these reductions and can produce them naturally without sounding artificial.",
    "grammar_focus": _gex(
        "Connected Speech Phenomena in German",
        "In natural spoken German: unstressed 'e' drops in prefixes and endings, auxiliary 'haben/sein' contract, articles reduce, and consonant clusters simplify. These are not errors but natural phonological processes.",
        "'Ich habe es gemacht' → 'Ich hab's gemacht' / 'Hast du das?' → 'Hasste das?' / 'in dem' → 'im' / 'zu dem' → 'zum'",
        ["Auxiliary reduction: hab, hat, hast (no final -e)", "Pronoun cliticization: hab's, macht's, gibst du → gibste", "Article contraction: im, am, zum, zur, beim, vom, ans, ins", "Verb-pronoun fusion: gehste (= gehst du), weißte (= weißt du), machste (= machst du)"],
        ["'Ich hab keine Ahnung, was er hat.' (fast speech)", "'Weißte was? Das ist mir egal.' (very colloquial)", "'Kommste heute noch?' (dialectal / colloquial)"],
    ),
    "dialogue": [
        _t("friend_a", "Weißte schon, dass Lena heiratet?", "Did you know that Lena is getting married?"),
        _t("friend_b", "Nee, hab ich nichts davon gehört. Wann denn?", "No, I haven't heard anything about that. When?"),
        _t("friend_a", "Im Sommer, glaub ich. Irgendwo im Süden.", "In summer, I think. Somewhere in the south."),
        _t("friend_b", "Cool. Und wer ist der Glückliche?", "Cool. And who is the lucky one?"),
        _t("friend_a", "Dieser Typ aus der Schweiz. Kennste den?", "That guy from Switzerland. Do you know him?"),
        _t("friend_b", "Hab ihn mal kurz getroffen. Netter Kerl.", "I met him briefly once. Nice guy."),
        _t("friend_a", "Werden wir eingeladen, meinste?", "Will we be invited, do you think?"),
        _t("friend_b", "Hoffentlich! Ich fahr auf jeden Fall hin.", "Hopefully! I'll definitely go."),
    ],
    "vocabulary_list": [
        _v("die Reduktion (-en)", "reduction (phonetics)", "Reduktionen sind typisch für schnelles Sprechen."),
        _v("die Assimilation (Phonetik)", "assimilation (phonetics)", "Assimilation verändert benachbarte Laute."),
        _v("der Schwa-Laut", "schwa sound (the 'uh' in unstressed syllables)", "Unstressed 'e' often becomes schwa or drops."),
        _v("kliticisieren", "to cliticize / attach as a clitic", "Pronomen kliticisieren sich an Verben."),
        _v("der Kerl (-e)", "guy / fellow (colloquial)", "Er ist ein netter Kerl."),
        _v("auf jeden Fall", "in any case / definitely", "Ich komme auf jeden Fall."),
        _v("die Prosodie", "prosody (rhythm and intonation)", "Prosody marks native fluency."),
        _v("die Elision (-en)", "elision (dropping sounds)", "Elision von 'e' ist häufig."),
        _v("der Glückliche / die Glückliche", "the lucky one", "Wer ist der Glückliche?"),
        _v("hoffentlich", "hopefully", "Hoffentlich wird es schön."),
    ],
    "exercises": [
        _ex_fib(
            "Write the reduced spoken form",
            ["'Weißt du das?' → '___te das?'", "'Hast du das gemacht?' → '___te das gemacht?'", "'Ich habe keine Zeit.' → 'Ich ___ keine Zeit.'"],
            ["Weiß", "Has", "hab"],
        ),
        _ex_mc(
            "Identify the spoken reduction",
            [
                ("'Geh ich mal kurz raus.' is a reduction of:", ["Gehe ich mal kurz heraus.", "Ich gehe mal kurz hinaus.", "Ich gehe mal kurz raus.", "Ich gehe kurz raus."], 2),
                ("'Weißte' is a fusion of:", ["weiß ich", "weißt du", "weiß er", "wisst ihr"], 1),
                ("'Hab's gemacht.' is a contraction of:", ["Ich habe es gemacht.", "Ich hab das gemacht.", "Habe ich es gemacht.", "Hat er es gemacht."], 0),
            ],
        ),
        _ex_tr(
            "Expand the spoken forms to standard written German",
            [
                ("Kommste heute noch vorbei?", "Kommst du heute noch vorbei?"),
                ("Hab keine Lust.", "Ich habe keine Lust."),
                ("Machen wir's so.", "Machen wir es so."),
            ],
        ),
        _ex_arr(
            "Match spoken form to written form",
            [
                (["Weißte?", "Machste das?", "Hab nix.", "Is mir egal."], ["Weißt du?", "Machst du das?", "Ich habe nichts.", "Das ist mir egal."]),
            ],
        ),
        _ex_sp(
            "Practice native-speed German",
            ["Listen to a German podcast at full speed and transcribe 30 seconds. Note all reductions.", "Read the dialogue above aloud at natural speed – record yourself.", "Have a conversation using colloquial reductions intentionally."],
        ),
    ],
}

LESSON_153 = {
    "title": "Advanced Pragmatics: Politeness, Face, and Indirectness",
    "level": "C2",
    "scenario": "social_pragmatics",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand face-threatening acts and how German mitigates them",
        "Use indirect speech acts and implicature in German",
        "Navigate German directness vs. politeness strategies",
        "Produce appropriate requests, refusals, and complaints at C2 level",
    ],
    "cultural_note": "Germans are often perceived as direct, but German actually has sophisticated politeness strategies. The difference from English is not less politeness but different conventions: Germans use politeness structurally (via Konjunktiv II, modal verbs) rather than formulaically (saying 'please' and 'sorry' frequently).",
    "grammar_focus": _gex(
        "Konjunktiv II for Politeness and Indirectness",
        "The most important politeness device in German is Konjunktiv II: softening requests (Könnten Sie...? / Würden Sie...? / Ich hätte gerne...), expressing wishes (Ich würde gerne...), and hedging disagreement (Das wäre eine Möglichkeit, aber...).",
        "'Machen Sie das bitte.' → 'Könnten Sie das eventuell machen?' / 'Würden Sie mir helfen?' / 'Ich hätte da eine Frage.'",
        ["Request softening: Könnten Sie / Würden Sie / Hätten Sie / Wäre es möglich", "Disagreement hedging: Das wäre denkbar, aber... / Ich bin mir nicht sicher, ob...", "Refusal: Das ist leider nicht so einfach. / Ich würde lieber nicht. / Das passt mir leider nicht."],
        ["Wäre es möglich, den Termin zu verschieben?", "Ich hätte da eine vielleicht etwas ungewöhnliche Bitte.", "Das ist sicher richtig; ich würde jedoch bedenken, dass..."],
    ),
    "dialogue": [
        _t("employee", "Darf ich Sie kurz stören?", "May I disturb you briefly?"),
        _t("manager", "Natürlich. Was gibt es?", "Of course. What is it?"),
        _t("employee", "Ich hätte da eine Bitte bezüglich des Projekttermins.", "I have a request regarding the project deadline."),
        _t("manager", "Ja?", "Yes?"),
        _t("employee", "Wäre es möglich, die Abgabe um eine Woche zu verschieben? Der Umfang ist größer als erwartet.", "Would it be possible to postpone the deadline by a week? The scope is larger than expected."),
        _t("manager", "Das ist grundsätzlich verständlich. Ich müsste aber mit dem Kunden sprechen.", "That is understandable in principle. I would need to speak with the client, though."),
        _t("employee", "Natürlich. Ich würde mich über eine Rückmeldung bis morgen sehr freuen.", "Of course. I would very much appreciate feedback by tomorrow."),
        _t("manager", "Das sollte sich einrichten lassen.", "That should be arrangeable."),
    ],
    "vocabulary_list": [
        _v("das Gesicht wahren", "to save face", "Er will sein Gesicht wahren."),
        _v("die Gesichtsbedrohung", "face-threatening act (pragmatics)", "Eine Absage kann eine Gesichtsbedrohung sein."),
        _v("die Implikatur (-en)", "implicature", "Implikaturen sind unausgesprochene Bedeutungen."),
        _v("der Sprechakt (-e)", "speech act", "Eine Bitte ist ein direktiver Sprechakt."),
        _v("indirekt", "indirect", "Indirekte Sprechakte sind höflicher."),
        _v("die Absage (-n)", "rejection / cancellation", "Eine höfliche Absage ist besser als keine Antwort."),
        _v("verschieben", "to postpone / move", "Können wir den Termin verschieben?"),
        _v("die Rückmeldung (-en)", "feedback / response", "Ich bitte um eine Rückmeldung."),
        _v("grundsätzlich", "in principle / fundamentally", "Das ist grundsätzlich möglich."),
        _v("sich einrichten lassen", "to be arrangeable", "Das lässt sich einrichten."),
    ],
    "exercises": [
        _ex_fib(
            "Soften these requests using Konjunktiv II",
            ["'Helfen Sie mir.' → '___ Sie mir helfen?' (polite request)", "'Ich will einen Termin.' → 'Ich ___ gerne einen Termin.'", "'Ist das möglich?' → '___ es möglich?'"],
            ["Könnten", "hätte", "Wäre"],
        ),
        _ex_mc(
            "Pragmatic interpretation",
            [
                ("'Das ist sicher richtig.' followed by 'aber...' – What does this signal?", ["Full agreement", "A polite disagreement is coming", "A change of subject", "A compliment"], 1),
                ("'Das lässt sich einrichten.' – What does this mean pragmatically?", ["Definite yes", "Definite no", "Polite yes / probably possible", "I don't know"], 2),
                ("'Ich hätte da eine Bitte.' – What is the pragmatic function of 'hätte'?", ["Past tense", "Politeness marker / face-saving", "Uncertainty", "Future intention"], 1),
            ],
        ),
        _ex_tr(
            "Translate politely using Konjunktiv II",
            [
                ("Would it be possible to postpone the meeting?", "Wäre es möglich, die Besprechung zu verschieben?"),
                ("I would very much appreciate a response by Friday.", "Ich würde mich über eine Antwort bis Freitag sehr freuen."),
                ("Could you perhaps take a look at this?", "Könnten Sie sich das vielleicht einmal ansehen?"),
            ],
        ),
        _ex_arr(
            "Order the polite request",
            [
                (["Wäre", "es", "möglich", "den", "Termin", "um", "eine", "Woche", "zu", "verschieben"], "Wäre es möglich, den Termin um eine Woche zu verschieben?"),
            ],
        ),
        _ex_sp(
            "Pragmatics in action",
            ["Make a difficult request to a colleague using maximum politeness.", "Refuse an invitation politely without giving offence.", "Compare German and English politeness strategies: where are they similar, where different?"],
        ),
    ],
}

LESSON_154 = {
    "title": "Advanced Reading: German Prose of the 20th Century",
    "level": "C2",
    "scenario": "advanced_literature",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Read and analyse difficult 20th-century German prose at native level",
        "Understand stream of consciousness and other modernist techniques in German",
        "Engage with texts by Musil, Bachmann, Bernhard, and Celan",
        "Write an advanced literary critique in German",
    ],
    "cultural_note": "20th-century German literature is among the most challenging and rewarding in world literature. Thomas Mann's long sentences, Kafka's logical absurdity, Paul Celan's fractured poetry, Ingeborg Bachmann's lyrical prose, and Thomas Bernhard's spiralling monologues all represent unique linguistic achievements.",
    "grammar_focus": _gex(
        "Long-Sentence Prose and Bernhard's Spiral Syntax",
        "Thomas Bernhard is famous for extremely long sentences with repeated qualifications, self-corrections, and layered embedding. Understanding and producing this style is a C2 challenge.",
        "'Es ist, wie ich jetzt denke, obwohl ich früher anders gedacht haben mag und möglicherweise auch in Zukunft wieder anders denken werde, das größte Problem, das ich kenne.' (Bernhard-style)",
        ["Self-correction embedding: '..., wie ich jetzt denke...' / '..., wenn ich ehrlich bin...'", "Repetition and intensification: 'immer mehr', 'immer größer', 'alles, alles, alles'", "Qualification chains: '..., obwohl... / ..., was jedoch... / ..., was ich allerdings...'"],
        ["'Es ist das Schrecklichste, was ich je erlebt habe, wenngleich ich, wenn ich ehrlich bin, Ähnliches schon früher erfahren hatte, ohne es damals so zu nennen.'"],
    ),
    "dialogue": [
        _t("student", "Ich verstehe Bernhards Sätze beim ersten Lesen nie.", "I never understand Bernhard's sentences on first reading."),
        _t("professor", "Das ergeht allen so. Bernhard schreibt Gedankenspiralen, keine linearen Sätze.", "That happens to everyone. Bernhard writes thought spirals, not linear sentences."),
        _t("student", "Wie soll man das analysieren?", "How should one analyse that?"),
        _t("professor", "Suchen Sie den Hauptsatz – er steht oft am Ende oder ist eingebettet.", "Find the main clause – it is often at the end or embedded."),
        _t("student", "Und die endlosen Einschübe?", "And the endless insertions?"),
        _t("professor", "Die sind Qualifikationen, Korrekturen, Selbstzweifel. Bernhard denkt laut auf dem Papier.", "Those are qualifications, corrections, self-doubt. Bernhard thinks aloud on paper."),
        _t("student", "Das ist eigentlich sehr ehrlich.", "That is actually very honest."),
        _t("professor", "Genau. Und deswegen zieht es uns in den Sog.", "Exactly. And that is why we are drawn into the vortex."),
    ],
    "vocabulary_list": [
        _v("der Einschub (Einschübe)", "insertion / parenthetical element", "Bernhards Einschübe sind charakteristisch."),
        _v("der Gedankenstrom", "stream of consciousness", "Der Gedankenstrom ist eine modernistische Technik."),
        _v("die Qualifikation (-en)", "qualification / restriction", "Qualifikationen machen Aussagen präziser."),
        _v("der Sog", "vortex / pull / current", "Der Text zieht uns in den Sog."),
        _v("die Selbstkorrektur (-en)", "self-correction", "Bernhard verwendet häufig Selbstkorrekturen."),
        _v("eingebettet", "embedded", "Der Hauptsatz ist eingebettet."),
        _v("linear", "linear", "Bernhards Syntax ist nicht linear."),
        _v("laut denken", "to think aloud", "Er denkt auf dem Papier laut."),
        _v("die Spirale (-n)", "spiral", "Bernhards Satzspirale ist einzigartig."),
        _v("der Zweifel (-)", "doubt", "Selbstzweifel durchziehen seinen Stil."),
    ],
    "exercises": [
        _ex_mc(
            "20th-century German literature: match author to style",
            [
                ("Extremely long, spiralling sentences with self-corrections:", ["Kafka", "Bernhard", "Celan", "Musil"], 1),
                ("Logical, bureaucratic language in surreal situations:", ["Bernhard", "Bachmann", "Kafka", "Mann"], 2),
                ("Fractured, post-Holocaust poetry that tests language's limits:", ["Böll", "Grass", "Celan", "Bachmann"], 2),
            ],
        ),
        _ex_fib(
            "Complete the Bernhard-style sentence",
            ["Es ist das Schlimmste, ___ ich je erlebt habe, obwohl ich, ___ ich ehrlich bin, Ähnliches kannte.", "Der Text zieht uns, wie alle großen Bücher es tun, ___ in seinen Sog.", "Bernhard denkt, was ich nach langem Lesen ___, laut auf dem Papier."],
            ["was", "wenn", "unweigerlich", "glaube"],
        ),
        _ex_tr(
            "Translate in Bernhard's style (with qualifications)",
            [
                ("It is the worst thing I know, although I have perhaps known worse, or so I think now.", "Es ist das Schlimmste, das ich kenne, obwohl ich vielleicht Schlimmeres gekannt habe, oder so denke ich jetzt."),
            ],
        ),
        _ex_arr(
            "Find the main clause in this Bernhard-style sentence",
            [
                (["Es ist", "[obwohl ich früher anders gedacht hatte]", "[wenn ich ehrlich bin]", "das größte Problem"], "Main clause: 'Es ist das größte Problem.' Insertions are qualifications."),
            ],
        ),
        _ex_sp(
            "Literary analysis at C2 level",
            ["Analyse a Bernhard sentence: identify main clause, all insertions, and their function.", "What effect does Bernhard's spiral syntax create in the reader?", "Write a short paragraph imitating Bernhard's style on any topic."],
        ),
    ],
}

LESSON_155 = {
    "title": "C2 Mid-Level Review and Consolidation",
    "level": "C2",
    "scenario": "review_session",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Review all major C2 grammar and style features covered so far",
        "Demonstrate native-like fluency across all registers and text types",
        "Identify remaining gaps and targets for full C2 mastery",
        "Produce extended, polished German text in multiple genres",
    ],
    "cultural_note": "At this stage you command German at a near-native level. The final stretch is refinement: eliminating residual errors, mastering the last idioms and collocations, and developing a personal style that feels natural in German rather than translated.",
    "grammar_focus": _gex(
        "C2 Grammar Synthesis",
        "C2 mastery synthesizes: all tenses and aspects, all passive forms, Konjunktiv I and II in all uses, complex syntax (clefts, inversion, extended NPs, participial phrases), register control, and pragmatic precision.",
        "Das von seiner Lehrerin seit Jahren als unverkennbar talentiert beschriebene Kind, das jedoch, wie alle wissen, nie einfach war, ließ sich – trotz allem – nicht entmutigen.",
        ["All register levels: colloquial → formal → academic → literary", "Complex NP: extended participial + relative + appositional structures", "Discourse markers: moreover, however, furthermore, consequently, in spite of"],
        ["Es wäre verfehlt anzunehmen, die Sprache sei lediglich ein Werkzeug.", "Das lässt sich, wenngleich mit Einschränkungen, so formulieren.", "Zugegeben, es gibt Ausnahmen; dennoch bleibt die Regel bestehen."],
    ),
    "dialogue": [
        _t("examiner", "Wir sind kurz vor dem Abschluss Ihres C2-Kurses. Was war die größte Veränderung für Sie?", "We are near the end of your C2 course. What was the biggest change for you?"),
        _t("learner", "Ich denke nicht mehr auf Englisch, bevor ich spreche. Ich denke auf Deutsch.", "I no longer think in English before speaking. I think in German."),
        _t("examiner", "Das ist das entscheidende Zeichen. Was müssen Sie noch verbessern?", "That is the decisive sign. What still needs improvement?"),
        _t("learner", "Idiome und Kollokationen – die automatisch richtigen Wortkombinationen.", "Idioms and collocations – the automatically correct word combinations."),
        _t("examiner", "Sehr ehrlich. Das ist tatsächlich das Letzte, was sich festigt.", "Very honest. That is indeed the last thing to consolidate."),
        _t("learner", "Und manchmal fehlt mir noch der Mut, in Diskussionen den Ton zu halten.", "And sometimes I still lack the courage to hold my register in discussions."),
        _t("examiner", "Das kommt mit Übung und Selbstvertrauen.", "That comes with practice and self-confidence."),
        _t("learner", "Ich freue mich auf den Weg dorthin.", "I look forward to the journey there."),
    ],
    "vocabulary_list": [
        _v("die Kollokation (-en)", "collocation", "Kollokationen sind schwer zu lernen."),
        _v("entscheidend", "decisive / crucial", "Das ist das entscheidende Kriterium."),
        _v("festigen", "to consolidate / strengthen", "Mit der Zeit festigen sich Strukturen."),
        _v("der Mut", "courage", "Mut zum Sprechen ist entscheidend."),
        _v("das Selbstvertrauen", "self-confidence", "Sprachliches Selbstvertrauen wächst mit Übung."),
        _v("residual", "residual", "Restfehler (residuale Fehler) sind schwer zu eliminieren."),
        _v("polieren", "to polish / refine", "C2 bedeutet, Sprache zu polieren.", ),
        _v("der Ton (Töne)", "tone / register", "Den richtigen Ton zu treffen ist eine Kunst."),
        _v("verfehlt", "misguided / mistaken", "Es wäre verfehlt, das anzunehmen."),
        _v("wenngleich", "even though / although (formal)", "Wenngleich schwierig, ist es möglich."),
    ],
    "exercises": [
        _ex_fib(
            "C2 comprehensive fill-in",
            ["Das ___ sich, wenngleich mit Einschränkungen, so ___ (lassen / formulieren).", "Es ___ verfehlt anzunehmen, die Sprache sei lediglich ein Werkzeug.", "Zugegeben, es gibt Ausnahmen; ___ bleibt die Regel bestehen."],
            ["lässt / formulieren", "wäre", "dennoch"],
        ),
        _ex_mc(
            "C2 review: identify the stylistic feature",
            [
                ("'Es war ihre Stimme, die sie verriet.' – What is this?", ["Passive sentence", "Cleft sentence for focus", "Inversion", "Relative clause only"], 1),
                ("'Das von Experten entwickelte Verfahren' – What construction is this?", ["Relative clause", "Extended participial noun phrase", "Passive sentence", "Apposition"], 1),
                ("'Könnten Sie mir vielleicht behilflich sein?' – What is the pragmatic function?", ["Order", "Polite request via Konjunktiv II", "Question about ability", "Rhetorical question"], 1),
            ],
        ),
        _ex_tr(
            "C2 synthesis translation",
            [
                ("The method developed by experts, though not without limitations, can be applied universally.", "Das von Experten entwickelte Verfahren lässt sich, wenngleich nicht ohne Einschränkungen, universell anwenden."),
                ("It would be misguided to assume that language is merely a tool.", "Es wäre verfehlt anzunehmen, die Sprache sei lediglich ein Werkzeug."),
                ("Granted, there are exceptions; nevertheless, the rule holds.", "Zugegeben, es gibt Ausnahmen; dennoch bleibt die Regel bestehen."),
            ],
        ),
        _ex_arr(
            "Reconstruct the C2-level sentence",
            [
                (["Es", "wäre", "verfehlt", "anzunehmen", "die", "Sprache", "sei", "lediglich", "ein", "Werkzeug"], "Es wäre verfehlt anzunehmen, die Sprache sei lediglich ein Werkzeug."),
            ],
        ),
        _ex_sp(
            "C2 final speaking tasks",
            ["Give a 3-minute presentation on German literature, using all C2 vocabulary and grammar features.", "Have a debate using concessive structures, cleft sentences, and epistemic modals.", "Reflect: What does it mean to truly master a language?"],
        ),
    ],
}
'''

for num in range(146, 156):
    tag = f"LESSON_{num}"
    if tag in existing:
        print(f"SKIP {tag} already exists")
        APPEND = re.sub(rf"\nLESSON_{num}\s*=.*?(?=\nLESSON_|\Z)", "", APPEND, flags=re.DOTALL)

SEEDS.write_text(src + APPEND, encoding="utf-8")

verify = SEEDS.read_text(encoding="utf-8")
found = sorted(set(re.findall(r"^(LESSON_\d+)\s*=", verify, re.MULTILINE)),
               key=lambda x: int(x.split("_")[1]))
print(f"Total lessons: {len(found)}, range: {found[0]}-{found[-1]}")

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

LESSON_136 = {
    "title": "Advanced Grammar: Subjunctive I (Konjunktiv I)",
    "level": "C1",
    "scenario": "grammar_workshop",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Use Konjunktiv I to report speech indirectly in formal contexts",
        "Distinguish Konjunktiv I from Konjunktiv II in reported speech",
        "Recognize Konjunktiv I in newspaper and academic writing",
        "Produce correct Konjunktiv I forms for common verbs",
    ],
    "cultural_note": "Konjunktiv I is essential in German journalism and formal writing for attributing statements without endorsing them. German newspapers routinely use it to report on politicians, court proceedings, and scientific claims.",
    "grammar_focus": _gex(
        "Konjunktiv I for Indirect Speech",
        "Konjunktiv I is formed from the infinitive stem + subjunctive endings. It signals reported speech without the speaker claiming truth.",
        "Er sagt, er sei krank. (He says he is sick.) vs. Er sagte, er wäre krank. (Konjunktiv II as fallback when KI = indicative)",
        ["sein: sei, sei(e)st, sei, seien, seiet, seien", "haben: habe, habest, habe, haben, habet, haben", "werden: werde, werdest, werde, werden, werdet, werden"],
        ["Der Minister erklärte, die Lage sei unter Kontrolle.", "Die Wissenschaftler berichteten, das Experiment habe erfolgreich funktioniert.", "Er behauptete, er habe nichts gewusst.", "Die Zeitung schreibt, die Preise seien gestiegen."],
    ),
    "dialogue": [
        _t("journalist", "Ich zitiere den Sprecher: Die Regierung werde alle notwendigen Maßnahmen ergreifen.", "I quote the spokesman: The government will take all necessary measures."),
        _t("editor", "Gut. Schreib das im Konjunktiv I – das ist Zeitungsstandard.", "Good. Write that in Konjunktiv I – that is the newspaper standard."),
        _t("journalist", "Also: Die Regierung werde alle notwendigen Maßnahmen ergreifen.", "So: The government would take all necessary measures."),
        _t("editor", "Genau. Und wenn Konjunktiv I identisch mit dem Indikativ ist, nimmst du Konjunktiv II.", "Exactly. And when Konjunktiv I is identical to the indicative, you use Konjunktiv II."),
        _t("journalist", "Zum Beispiel bei 'haben' in der dritten Person Plural?", "For example with 'haben' in the third person plural?"),
        _t("editor", "Richtig. 'Sie haben' ist Indikativ und Konjunktiv I. Also schreibst du 'sie hätten'.", "Correct. 'Sie haben' is indicative and Konjunktiv I. So you write 'sie hätten'."),
        _t("journalist", "Das macht Sinn. Und bei 'sein'?", "That makes sense. And with 'sein'?"),
        _t("editor", "Sein hat eindeutige Konjunktiv-I-Formen, deshalb immer Konjunktiv I verwenden.", "Sein has unambiguous Konjunktiv I forms, so always use Konjunktiv I."),
    ],
    "vocabulary_list": [
        _v("die indirekte Rede", "indirect speech", "In der indirekten Rede benutzt man Konjunktiv I."),
        _v("berichten", "to report", "Die Zeitung berichtet über den Vorfall."),
        _v("behaupten", "to claim / assert", "Er behauptet, unschuldig zu sein."),
        _v("zitieren", "to quote", "Der Anwalt zitierte das Gesetz."),
        _v("der Sprecher / die Sprecherin", "spokesman / spokeswoman", "Der Sprecher der Partei gab eine Erklärung ab."),
        _v("eindeutig", "unambiguous / clear", "Die Konjunktiv-I-Formen von 'sein' sind eindeutig."),
        _v("die Maßnahme (-n)", "measure / step", "Die Regierung ergreift geeignete Maßnahmen."),
        _v("zufolge (+ Dativ)", "according to", "Dem Bericht zufolge stieg die Inflation."),
        _v("angeblich", "allegedly / supposedly", "Er hat angeblich das Dokument unterschrieben."),
        _v("der Vorwurf (Vorwürfe)", "accusation / charge", "Die Vorwürfe gegen den Minister sind schwerwiegend."),
    ],
    "exercises": [
        _ex_fib(
            "Convert to Konjunktiv I reported speech",
            ["Er sagt: 'Ich bin müde.' → Er sagt, er ___ müde.", "Sie sagt: 'Wir haben keine Zeit.' → Sie sagt, sie ___ keine Zeit.", "Der Arzt sagt: 'Das Medikament wirkt.' → Der Arzt sagt, das Medikament ___."],
            ["sei", "hätten", "wirke"],
        ),
        _ex_mc(
            "Choose the correct reported speech form",
            [
                ("Der Politiker erklärte, die Wirtschaft ___ wachsen.", ["wächst", "wachse", "wachsen würde", "wachste"], 1),
                ("Die Forscherin berichtete, sie ___ neue Daten gefunden.", ["hat", "hatte", "habe", "hätte"], 2),
                ("Er behauptete, er ___ die Wahrheit.", ["sagt", "sage", "sagte", "würde sagen"], 1),
            ],
        ),
        _ex_arr(
            "Order the words to form correct Konjunktiv I sentences",
            [
                (["der", "Bericht", "die", "Lage", "angespannt", "zufolge", "sei"], "Dem Bericht zufolge sei die Lage angespannt."),
                (["behauptete", "er", "habe", "er", "alles", "gewusst"], "Er behauptete, er habe alles gewusst."),
            ],
        ),
        _ex_tr(
            "Translate into German using Konjunktiv I",
            [
                ("The minister said the situation was under control.", "Der Minister sagte, die Lage sei unter Kontrolle."),
                ("The newspaper reports that prices have risen.", "Die Zeitung berichtet, die Preise seien gestiegen."),
                ("He claims he did not know anything.", "Er behauptet, er habe nichts gewusst."),
            ],
        ),
        _ex_sp(
            "Report what your partner said using Konjunktiv I",
            ["Your partner says: 'I am learning German.' Report it formally.", "Your partner says: 'We have finished the project.' Report it in writing.", "Your partner says: 'The results are promising.' Report it as a journalist."],
        ),
    ],
}

LESSON_137 = {
    "title": "Complex Sentence Architecture",
    "level": "C1",
    "scenario": "academic_writing",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Construct multi-clause sentences with multiple subordinate clauses",
        "Use participial phrases (Partizipialkonstruktionen) to compress information",
        "Employ extended noun phrases (erweiterte Nominalphrasen) in academic prose",
        "Recognize and produce the German periodic sentence style",
    ],
    "cultural_note": "German academic writing traditionally favors long, complex sentences that pack maximum information into a single syntactic unit. This style, rooted in 18th-century philosophical prose, contrasts sharply with Anglo-American preferences for shorter sentences.",
    "grammar_focus": _gex(
        "Participial Phrases and Extended Noun Phrases",
        "Partizipialkonstruktionen replace relative clauses: 'das veröffentlichte Buch' instead of 'das Buch, das veröffentlicht wurde'. Extended noun phrases place multiple modifiers before the noun.",
        "das von der Universität geförderte, international beachtete Forschungsprojekt (the university-funded, internationally acclaimed research project)",
        ["Present participle: das wachsende Problem (the growing problem)", "Past participle: die gelöste Aufgabe (the solved task)", "Extended: das von Experten entwickelte, weltweit eingesetzte Verfahren"],
        ["Die von der Regierung eingesetzte, mit internationalen Experten besetzte Kommission legte ihren Bericht vor.", "Das bereits seit Jahren diskutierte, aber noch immer nicht gelöste Problem der Altersarmut erfordert dringendes Handeln."],
    ),
    "dialogue": [
        _t("professor", "Ihr Aufsatz liest sich noch sehr einfach. Versuchen Sie, Partizipialkonstruktionen zu verwenden.", "Your essay still reads very simply. Try using participial constructions."),
        _t("student", "Wie meine ich: 'die Studie, die von Müller durchgeführt wurde'?", "Do you mean: 'the study that was conducted by Müller'?"),
        _t("professor", "Genau. Das wird zu: 'die von Müller durchgeführte Studie'.", "Exactly. That becomes: 'the study conducted by Müller'."),
        _t("student", "Und ich kann noch mehr Attribute hinzufügen?", "And I can add even more attributes?"),
        _t("professor", "Ja, solange es grammatisch korrekt bleibt. Zum Beispiel: 'die von Müller 2023 in Berlin durchgeführte, international beachtete Studie'.", "Yes, as long as it remains grammatically correct. For example: 'the internationally acclaimed study conducted by Müller in Berlin in 2023'."),
        _t("student", "Das klingt sehr akademisch.", "That sounds very academic."),
        _t("professor", "Genau das wollen wir in wissenschaftlichen Texten.", "That is exactly what we want in academic texts."),
        _t("student", "Ich werde es in der nächsten Version versuchen.", "I will try it in the next version."),
    ],
    "vocabulary_list": [
        _v("die Partizipialkonstruktion (-en)", "participial construction", "Partizipialkonstruktionen verdichten Informationen."),
        _v("die Nominalphrase (-n)", "noun phrase", "Erweiterte Nominalphrasen sind typisch für Wissenschaftssprache."),
        _v("verdichten", "to compress / condense", "Man kann Information durch Nominalisierung verdichten."),
        _v("das Attribut (-e)", "attribute / modifier", "Das Adjektiv ist ein Attribut zum Nomen."),
        _v("einsetzen", "to deploy / use / establish", "Die Kommission wurde vom Ministerium eingesetzt."),
        _v("darlegen", "to present / set out", "Er legte seine These ausführlich dar."),
        _v("erfordern", "to require / demand", "Das Problem erfordert eine grundlegende Lösung."),
        _v("dringlich / dringend", "urgent", "Es besteht dringender Handlungsbedarf."),
        _v("die Voraussetzung (-en)", "prerequisite / condition", "Gute Sprachkenntnisse sind Voraussetzung für das Studium."),
        _v("ausführlich", "detailed / thorough / at length", "Er erklärte die Methode ausführlich."),
    ],
    "exercises": [
        _ex_fib(
            "Convert relative clauses to participial phrases",
            ["Das Experiment, das gestern durchgeführt wurde → Das gestern ___ Experiment", "Die Methode, die weltweit angewendet wird → Die weltweit ___ Methode", "Der Bericht, der von Experten erstellt wurde → Der von Experten ___ Bericht"],
            ["durchgeführte", "angewendete", "erstellte"],
        ),
        _ex_mc(
            "Choose the grammatically correct extended noun phrase",
            [
                ("___ liegt dem Ausschuss vor.", ["Der von der Kommission verfasste, mit Statistiken belegte Bericht", "Den von der Kommission verfassten Bericht", "Das von der Kommission verfassender Bericht", "Die von der Kommission verfassten Berichte lag"], 0),
                ("Wir diskutierten ___.", ["das schon lange bekannte Problem", "die schon lange bekannten Problems", "dem schon lange bekanntem Problem", "den schon lange bekannten Problem"], 0),
            ],
        ),
        _ex_tr(
            "Translate using participial constructions",
            [
                ("The recently published study challenges previous assumptions.", "Die kürzlich veröffentlichte Studie stellt frühere Annahmen in Frage."),
                ("The internationally funded, widely discussed project will be concluded next year.", "Das international geförderte, breit diskutierte Projekt wird nächstes Jahr abgeschlossen."),
            ],
        ),
        _ex_arr(
            "Reconstruct the sentence from components",
            [
                (["Die", "von", "Fachleuten", "entwickelte", "weltweit", "eingesetzte", "Methode", "hat", "sich", "bewährt"], "Die von Fachleuten entwickelte, weltweit eingesetzte Methode hat sich bewährt."),
            ],
        ),
        _ex_sp(
            "Rewrite these sentences using extended noun phrases",
            ["The car that was built in Germany and sold worldwide is very popular.", "The problem that has been discussed for years and still has not been solved requires action.", "The report that was written by experts and submitted to the committee is comprehensive."],
        ),
    ],
}

LESSON_138 = {
    "title": "German in Professional Contexts: Business Communication",
    "level": "C1",
    "scenario": "business_meeting",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Write professional German emails and formal correspondence",
        "Use appropriate register in business negotiations and meetings",
        "Understand and use German business idioms and set phrases",
        "Navigate intercultural differences in German professional communication",
    ],
    "cultural_note": "German business communication tends to be more formal, direct, and detail-oriented than in many other cultures. The use of titles (Herr Doktor, Frau Professorin) is important, and Siezen (formal 'Sie') is standard until explicitly invited to switch to 'du'.",
    "grammar_focus": _gex(
        "Formal Written Register in Business German",
        "Business German uses specific formulaic openings, closings, and set phrases. Passive constructions and nominalisations are common.",
        "Anbei übersende ich Ihnen... / Beigefügt finden Sie... / Mit freundlichen Grüßen",
        ["Opening: Sehr geehrte Damen und Herren / Sehr geehrte Frau [Name] / Sehr geehrter Herr [Name]", "Referencing: Bezugnehmend auf Ihr Schreiben vom... / In Bezug auf unsere Unterhaltung...", "Closing: Mit freundlichen Grüßen / Hochachtungsvoll (very formal)"],
        ["Anbei übersende ich Ihnen den unterzeichneten Vertrag.", "Bezugnehmend auf unser Gespräch vom 15. März möchte ich Folgendes mitteilen.", "Wir erlauben uns, Ihnen unser neues Produktportfolio vorzustellen."],
    ),
    "dialogue": [
        _t("colleague", "Haben Sie die E-Mail an den Kunden schon geschrieben?", "Have you already written the email to the client?"),
        _t("you", "Fast. Ich bin mir bei der Anrede nicht sicher – er hat einen Doktortitel.", "Almost. I'm not sure about the salutation – he has a doctorate."),
        _t("colleague", "Dann schreib 'Sehr geehrter Herr Dr. Schneider'. Den Titel immer verwenden.", "Then write 'Dear Dr. Schneider'. Always use the title."),
        _t("you", "Und zum Abschluss? 'Mit freundlichen Grüßen' oder 'Hochachtungsvoll'?", "And for the closing? 'Kind regards' or 'Yours faithfully'?"),
        _t("colleague", "'Mit freundlichen Grüßen' ist standard. 'Hochachtungsvoll' klingt heute zu steif.", "'Mit freundlichen Grüßen' is standard. 'Hochachtungsvoll' sounds too stiff today."),
        _t("you", "Was ist mit dem Anhang? Wie weise ich darauf hin?", "What about the attachment? How do I refer to it?"),
        _t("colleague", "Schreib 'Anbei übersende ich Ihnen...' oder 'Im Anhang finden Sie...'.", "Write 'Please find attached...' or 'In the attachment you will find...'."),
        _t("you", "Perfekt. Und das Angebot soll ich bis wann einreichen?", "Perfect. And by when should I submit the offer?"),
    ],
    "vocabulary_list": [
        _v("anbei", "enclosed / attached (formal)", "Anbei sende ich Ihnen die Unterlagen."),
        _v("beigefügt", "attached / enclosed", "Beigefügt finden Sie unseren Kostenvoranschlag."),
        _v("bezugnehmend auf", "with reference to / referring to", "Bezugnehmend auf Ihr Angebot vom 3. Mai..."),
        _v("der Kostenvoranschlag (Kostenvoranschläge)", "cost estimate / quote", "Wir bitten um einen Kostenvoranschlag."),
        _v("die Anrede (-n)", "salutation / form of address", "Die korrekte Anrede ist wichtig."),
        _v("das Schreiben (-)", "letter / correspondence (formal)", "Ihr Schreiben vom 12. April ist eingegangen."),
        _v("in Bezug auf", "regarding / with respect to", "In Bezug auf Ihre Anfrage..."),
        _v("die Rücksprache", "consultation / checking back", "Ich werde nach Rücksprache mit meiner Abteilung antworten."),
        _v("der Sachverhalt (Sachverhalte)", "matter / state of affairs", "Ich möchte den Sachverhalt kurz erläutern."),
        _v("verbindlich", "binding / reliable / obliging", "Wir bitten um eine verbindliche Zusage."),
    ],
    "exercises": [
        _ex_fib(
            "Complete the formal email phrases",
            ["___ Damen und Herren,", "Bezugnehmend auf unser Gespräch ___ ich Folgendes mitteilen.", "Im Anhang ___ Sie unseren Bericht."],
            ["Sehr geehrte", "möchte", "finden"],
        ),
        _ex_mc(
            "Choose the appropriate business register",
            [
                ("You are writing to a client for the first time. Which opening is correct?", ["Hey!", "Liebe Frau Müller,", "Sehr geehrte Frau Müller,", "Hallo Frau Müller,"], 2),
                ("Which closing is standard in German business emails today?", ["Tschüss!", "Hochachtungsvoll", "Mit freundlichen Grüßen", "Alles Gute"], 2),
                ("How do you refer to an attachment formally?", ["Hier ist die Datei", "Anbei übersende ich Ihnen die Unterlagen.", "Ich hab was angehängt.", "Schau mal in den Anhang."], 1),
            ],
        ),
        _ex_tr(
            "Translate into formal business German",
            [
                ("With reference to your letter of 5 May, we would like to inform you that...", "Bezugnehmend auf Ihr Schreiben vom 5. Mai möchten wir Ihnen mitteilen, dass..."),
                ("Please find enclosed our revised offer.", "Anbei übersenden wir Ihnen unser überarbeitetes Angebot."),
                ("We look forward to hearing from you.", "Wir freuen uns auf Ihre Rückmeldung."),
            ],
        ),
        _ex_arr(
            "Put the email components in the correct order",
            [
                (["Mit freundlichen Grüßen", "Sehr geehrte Frau Schmidt,", "Anbei finden Sie den Bericht.", "Bezugnehmend auf unser Gespräch", "Thomas Braun"], "Sehr geehrte Frau Schmidt, / Bezugnehmend auf unser Gespräch / Anbei finden Sie den Bericht. / Mit freundlichen Grüßen / Thomas Braun"),
            ],
        ),
        _ex_sp(
            "Role-play business communication scenarios",
            ["Write a formal email requesting a meeting with a new client.", "You are in a business meeting: politely disagree with a colleague's proposal.", "Call a company to follow up on your job application – use appropriate formal register."],
        ),
    ],
}

LESSON_139 = {
    "title": "Advanced Listening: Radio and Podcasts",
    "level": "C1",
    "scenario": "media_consumption",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Understand fast-paced authentic German radio speech",
        "Identify main ideas and supporting details in podcasts",
        "Recognise ellipsis and informal structures in spoken German",
        "Take notes in German while listening to extended passages",
    ],
    "cultural_note": "German public radio (ARD, ZDF, Deutschlandradio) maintains high linguistic standards and is excellent for C1 learners. Podcasts like 'Slow German' (for learners) or 'Fest & Flauschig' (authentic) offer different registers.",
    "grammar_focus": _gex(
        "Spoken vs. Written German: Key Differences",
        "Spoken German drops pronouns, uses more modal particles, contracts words, and has freer word order than written German.",
        "'Kommst du mit?' → 'Kommste mit?' / 'Das ist schon in Ordnung' → 'Is schon in Ordnung'",
        ["Pronoun drop: 'Hab keine Zeit' (= Ich habe keine Zeit)", "Contraction: 'in dem' → 'im', 'an dem' → 'am', 'gehste' = gehst du", "Particle use: 'Na ja, is halt so.' (Well, that's just how it is.)"],
        ["Komm, wir gehen jetzt. (Come on, let's go now.)", "Is doch klar, oder? (That's obvious, isn't it?)", "Hab ich schon gemacht. (Already done that.)"],
    ),
    "dialogue": [
        _t("host", "Willkommen zurück bei unserem Podcast. Heute sprechen wir über die Zukunft der Arbeit.", "Welcome back to our podcast. Today we're talking about the future of work."),
        _t("guest", "Ja, das Thema bewegt gerade wirklich viele Menschen.", "Yes, this topic is really moving a lot of people right now."),
        _t("host", "Stimmmt. Homeoffice, KI, Automatisierung – alles auf einmal.", "True. Home office, AI, automation – all at once."),
        _t("guest", "Wobei ich sagen würde: Die Veränderungen kommen nicht über Nacht.", "Though I would say: The changes don't come overnight."),
        _t("host", "Aber die Beschleunigung ist schon spürbar, oder?", "But the acceleration is already noticeable, isn't it?"),
        _t("guest", "Absolut. Besonders in der Wissensarbeit – da tut sich gerade irrsinnig viel.", "Absolutely. Especially in knowledge work – an incredible amount is happening there right now."),
        _t("host", "Was raten Sie Menschen, die sich Sorgen um ihren Job machen?", "What do you advise people who are worried about their jobs?"),
        _t("guest", "Lebenslang lernen. Klingt wie ein Klischee, ist aber die ehrlichste Antwort.", "Lifelong learning. Sounds like a cliché, but it's the most honest answer."),
    ],
    "vocabulary_list": [
        _v("die Automatisierung", "automation", "Die Automatisierung verändert die Arbeitswelt."),
        _v("die Wissensarbeit", "knowledge work", "Wissensarbeit ist besonders von KI betroffen."),
        _v("die Beschleunigung", "acceleration", "Die technologische Beschleunigung ist spürbar."),
        _v("spürbar", "noticeable / perceptible", "Die Veränderungen sind deutlich spürbar."),
        _v("irrsinnig (colloquial)", "incredibly / insanely", "Da tut sich irrsinnig viel."),
        _v("lebenslang", "lifelong", "Lebenslanges Lernen ist wichtig."),
        _v("sich Sorgen machen", "to worry", "Viele Menschen machen sich Sorgen um die Zukunft."),
        _v("raten (+ Dativ)", "to advise", "Was raten Sie mir?"),
        _v("wobei", "though / whereas / while", "Wobei ich das anders sehe."),
        _v("auf einmal", "all at once / suddenly", "Alles passiert auf einmal."),
    ],
    "exercises": [
        _ex_mc(
            "Comprehension: What is said in the dialogue?",
            [
                ("What is the main topic of the podcast?", ["The history of work", "The future of work", "Remote work only", "AI dangers"], 1),
                ("What does the guest say about the speed of change?", ["Changes happen overnight", "Changes are slow", "Acceleration is noticeable", "There is no change"], 2),
                ("What is the guest's advice?", ["Find a new job", "Learn to code", "Lifelong learning", "Avoid technology"], 2),
            ],
        ),
        _ex_fib(
            "Fill in the colloquial spoken forms",
            ["'Ich habe keine Zeit.' → '___  keine Zeit.' (pronoun drop)", "'Das ist doch klar.' → '___ doch klar.' (contracted)", "'Hast du das schon gemacht?' → '___te das schon gemacht?'"],
            ["Hab", "Is", "Has"],
        ),
        _ex_tr(
            "Translate the informal spoken German to standard written German",
            [
                ("Is halt so.", "Das ist eben so."),
                ("Hab ich schon erledigt.", "Ich habe das schon erledigt."),
                ("Kommste morgen mit?", "Kommst du morgen mit?"),
            ],
        ),
        _ex_arr(
            "Match spoken features to their written equivalents",
            [
                (["Hab keine Ahnung.", "Is doch egal.", "Machste das?", "Gehts dir gut?"], ["Ich habe keine Ahnung.", "Das ist doch egal.", "Machst du das?", "Geht es dir gut?"]),
            ],
        ),
        _ex_sp(
            "Discuss media consumption in German",
            ["What German podcasts or radio programs do you listen to? Describe their content.", "What is most difficult about understanding fast spoken German?", "Compare spoken and written German – what differences have you noticed?"],
        ),
    ],
}

LESSON_140 = {
    "title": "Nuanced Argumentation and Rhetoric",
    "level": "C1",
    "scenario": "debate",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Structure a complex argument using German rhetorical devices",
        "Concede points while maintaining your position (konzessive Strukturen)",
        "Use hedging language to express degrees of certainty",
        "Employ anaphora, antithesis, and rhetorical questions effectively",
    ],
    "cultural_note": "German rhetorical tradition values structured, logical argumentation (Erörterung). School and university debates follow a thesis-antithesis-synthesis structure influenced by Hegelian dialectics. Being able to argue both sides is considered a mark of intellectual maturity.",
    "grammar_focus": _gex(
        "Concessive Structures and Hedging",
        "Concessive structures acknowledge opposing points: obwohl, obgleich, wenngleich, auch wenn, zwar...aber, dennoch, gleichwohl. Hedging expresses tentativeness: es scheint, als ob; es lässt sich argumentieren; man könnte einwenden.",
        "Zwar hat die Technologie viele Vorteile, dennoch birgt sie erhebliche Risiken.",
        ["Obwohl / Obgleich / Wenngleich + Verb-last clause", "Zwar... aber / jedoch / dennoch / gleichwohl", "Einräumend: Zugegeben, ... / Es stimmt zwar, dass... / Man muss zugeben, dass..."],
        ["Wenngleich dieses Argument nachvollziehbar ist, überzeugt es mich nicht vollständig.", "Zugegeben, die Kosten sind hoch; dennoch überwiegen die langfristigen Vorteile.", "Es lässt sich kaum bestreiten, dass... / Es wäre verfehlt anzunehmen, dass..."],
    ),
    "dialogue": [
        _t("debater_a", "Ich vertrete die These, dass soziale Medien mehr schaden als nützen.", "I am arguing the thesis that social media does more harm than good."),
        _t("debater_b", "Das ist eine weitverbreitete Ansicht. Zugegeben, es gibt Risiken – Fehlinformation, Sucht, Polarisierung.", "That is a widespread view. Granted, there are risks – misinformation, addiction, polarisation."),
        _t("debater_a", "Eben. Diese Risiken überwiegen die Vorteile bei weitem.", "Exactly. These risks far outweigh the benefits."),
        _t("debater_b", "Wenngleich das bei bestimmten Gruppen zutreffen mag, lässt sich nicht pauschal sagen, dass soziale Medien schaden.", "While that may apply to certain groups, one cannot say categorically that social media is harmful."),
        _t("debater_a", "Aber die empirischen Daten zur psychischen Gesundheit sprechen eine klare Sprache.", "But the empirical data on mental health speaks a clear language."),
        _t("debater_b", "Korrelation ist nicht Kausalität. Zwar besteht ein Zusammenhang, dennoch fehlt der Beweis für direkte Kausalität.", "Correlation is not causation. While there is a correlation, proof of direct causality is lacking."),
        _t("debater_a", "Ich gebe zu, dass das methodisch korrekt ist. Dennoch halte ich meine Position aufrecht.", "I admit that is methodologically correct. Nevertheless, I maintain my position."),
        _t("moderator", "Vielen Dank für diese differenzierte Debatte.", "Thank you for this nuanced debate."),
    ],
    "vocabulary_list": [
        _v("die These (-n)", "thesis / proposition", "Er stellt eine klare These auf."),
        _v("wenngleich", "even though / although", "Wenngleich es schwierig ist, lohnt es sich."),
        _v("dennoch / gleichwohl", "nevertheless / nonetheless", "Es ist schwierig; dennoch versuche ich es."),
        _v("überwiegen", "to outweigh / predominate", "Die Nachteile überwiegen die Vorteile."),
        _v("pauschal", "sweeping / blanket / categorical", "Pauschalurteile sind selten fair."),
        _v("die Kausalität", "causality", "Kausalität ist schwer zu beweisen."),
        _v("die Korrelation", "correlation", "Korrelation ist nicht Kausalität."),
        _v("aufrechterhalten / aufrecht halten", "to maintain / uphold", "Ich halte meinen Standpunkt aufrecht."),
        _v("einräumen", "to concede / admit", "Er räumte ein, dass er einen Fehler gemacht hatte."),
        _v("differenziert", "nuanced / differentiated", "Eine differenzierte Betrachtung ist nötig."),
    ],
    "exercises": [
        _ex_fib(
            "Complete the concessive structures",
            ["___ dieses Argument nachvollziehbar ist, überzeugt es mich nicht.", "___ stimmt es, dass Technologie Risiken birgt; ___ überwiegen die Vorteile.", "Ich ___ ein, dass die Kosten hoch sind."],
            ["Wenngleich", "Zwar / dennoch", "räume"],
        ),
        _ex_mc(
            "Identify the rhetorical device",
            [
                ("'Wir kämpfen. Wir siegen. Wir bleiben.' – What device is this?", ["Antithesis", "Anaphora", "Rhetorical question", "Irony"], 1),
                ("'Entweder wir handeln jetzt, oder wir bereuen es später.' – What is this?", ["Anaphora", "Hedging", "Antithesis", "Concession"], 2),
                ("'Man könnte argumentieren, dass...' – What function does this serve?", ["Assertion", "Hedging", "Concession", "Refutation"], 1),
            ],
        ),
        _ex_tr(
            "Translate using concessive structures",
            [
                ("Although the costs are high, the long-term benefits outweigh them.", "Obwohl die Kosten hoch sind, überwiegen die langfristigen Vorteile."),
                ("Granted, there are risks; nevertheless, we must act.", "Zugegeben, es gibt Risiken; dennoch müssen wir handeln."),
                ("While this argument is understandable, it is not fully convincing.", "Wenngleich dieses Argument nachvollziehbar ist, überzeugt es mich nicht vollständig."),
            ],
        ),
        _ex_arr(
            "Reconstruct the argument",
            [
                (["Zugegeben", "die", "Technik", "hat", "Risiken", "dennoch", "überwiegen", "die", "Vorteile"], "Zugegeben, die Technik hat Risiken; dennoch überwiegen die Vorteile."),
            ],
        ),
        _ex_sp(
            "Debate practice: argue both sides",
            ["Argue FOR and AGAINST: 'Social media does more harm than good.'", "Use at least two concessive structures in your argument.", "Challenge your partner's point using hedging language."],
        ),
    ],
}

LESSON_141 = {
    "title": "German Literature: Reading and Analysing Texts",
    "level": "C1",
    "scenario": "literature_seminar",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Analyse a literary text using German critical vocabulary",
        "Identify narrative perspective (Erzählperspektive) and its effect",
        "Discuss themes, motifs, and symbolism in German literary texts",
        "Write a short literary analysis (Textanalyse) in German",
    ],
    "cultural_note": "German literature has a rich tradition from Goethe and Schiller through Kafka and Brecht to contemporary authors like Herta Müller, Daniel Kehlmann, and Jenny Erpenbeck. Literary analysis (Textinterpretation) is a core skill in German schools and universities.",
    "grammar_focus": _gex(
        "Present Tense for Literary Analysis (Historisches Präsens)",
        "In German literary analysis, events in texts are described in the present tense (historisches Präsens), not the past tense. This is standard academic practice.",
        "Faust schließt einen Pakt mit Mephisto. (Faust makes a pact with Mephistopheles.) – not 'schloss'",
        ["Der Erzähler schildert... / Die Protagonistin erkennt... / Der Text thematisiert...", "In der Exposition wird... eingeführt. / Im Höhepunkt entscheidet sich...", "Dies symbolisiert / repräsentiert / verdeutlicht / spiegelt wider..."],
        ["Der Erzähler schildert die Situation aus einer auktorialen Perspektive.", "Die Metapher des Spiegels symbolisiert die Selbstreflexion der Protagonistin.", "Im zweiten Akt entscheidet sich der Held, den Widerstand aufzugeben."],
    ),
    "dialogue": [
        _t("seminar_leader", "Wir lesen heute einen Ausschnitt aus Kafkas 'Die Verwandlung'. Was fällt Ihnen sofort auf?", "Today we're reading an excerpt from Kafka's 'The Metamorphosis'. What strikes you immediately?"),
        _t("student_a", "Die Situation ist sofort absurd: Gregor wacht als Ungeziefer auf, und sein erster Gedanke gilt dem Beruf.", "The situation is immediately absurd: Gregor wakes up as a vermin, and his first thought is about his job."),
        _t("student_b", "Das ist wohl eine Gesellschaftskritik – die Entfremdung des modernen Menschen.", "That is probably social criticism – the alienation of modern man."),
        _t("seminar_leader", "Sehr gut. Und wie ist die Erzählperspektive?", "Very good. And what is the narrative perspective?"),
        _t("student_a", "Personal, aus Gregors Sicht – wir erleben alles durch seine Wahrnehmung.", "Personal, from Gregor's perspective – we experience everything through his perception."),
        _t("seminar_leader", "Richtig. Das nennen wir personales Erzählen. Was bewirkt das beim Leser?", "Correct. We call that personal narration. What effect does it have on the reader?"),
        _t("student_b", "Man empfindet Mitgefühl mit Gregor, auch wenn die Situation absurd ist.", "You feel empathy for Gregor, even though the situation is absurd."),
        _t("seminar_leader", "Exzellent. Schreiben Sie für nächste Woche eine kurze Textanalyse.", "Excellent. Write a short text analysis for next week."),
    ],
    "vocabulary_list": [
        _v("die Erzählperspektive (-n)", "narrative perspective", "Die Erzählperspektive beeinflusst den Leser stark."),
        _v("auktorial", "omniscient (narration)", "Ein auktorialer Erzähler weiß alles."),
        _v("personal", "personal / limited third person (narration)", "Personales Erzählen zeigt nur eine Perspektive."),
        _v("die Entfremdung", "alienation", "Kafkas Werk thematisiert die Entfremdung."),
        _v("das Motiv (-e)", "motif", "Das Motiv des Spiegels zieht sich durch den Text."),
        _v("die Metapher (-n)", "metaphor", "Die Verwandlung ist eine einzige große Metapher."),
        _v("schildern", "to depict / describe", "Der Erzähler schildert die Szene detailliert."),
        _v("das Mitgefühl", "empathy / compassion", "Der Text weckt Mitgefühl beim Leser."),
        _v("thematisieren", "to address / deal with (a theme)", "Das Werk thematisiert Isolation und Entfremdung."),
        _v("widerspiegeln", "to reflect / mirror", "Das Symbol spiegelt die innere Zerrissenheit wider."),
    ],
    "exercises": [
        _ex_fib(
            "Complete the literary analysis sentences",
            ["Der Erzähler ___ die Verwandlung aus Gregors Perspektive.", "Die Verwandlung ___ die Entfremdung des modernen Menschen.", "Das Motiv des Ungeziefers ___ Gregors gesellschaftliche Ausgrenzung wider."],
            ["schildert", "thematisiert", "spiegelt"],
        ),
        _ex_mc(
            "Literary terms: choose the correct definition",
            [
                ("What is 'auktoriales Erzählen'?", ["Narration from one character's view", "Omniscient narration knowing all characters' thoughts", "First-person narration", "Stream of consciousness"], 1),
                ("What does 'thematisieren' mean in literary analysis?", ["To avoid a topic", "To address or deal with a theme", "To describe visually", "To quote directly"], 1),
                ("What is the 'Erzählperspektive'?", ["The plot of the story", "The narrative perspective", "The author's biography", "The text's genre"], 1),
            ],
        ),
        _ex_tr(
            "Translate literary analysis sentences",
            [
                ("The narrator depicts the scene from an omniscient perspective.", "Der Erzähler schildert die Szene aus einer auktorialen Perspektive."),
                ("The metamorphosis symbolises the alienation of modern man.", "Die Verwandlung symbolisiert die Entfremdung des modernen Menschen."),
                ("The text addresses themes of isolation and identity.", "Der Text thematisiert Isolation und Identität."),
            ],
        ),
        _ex_arr(
            "Order the elements of a text analysis",
            [
                (["Thema und Deutung", "Einleitung mit Titel und Autor", "Analyse der Sprache und Stilmittel", "Beschreibung der Erzählperspektive", "Fazit"], "Einleitung mit Titel und Autor / Beschreibung der Erzählperspektive / Thema und Deutung / Analyse der Sprache und Stilmittel / Fazit"),
            ],
        ),
        _ex_sp(
            "Literary seminar discussion",
            ["Describe the narrative perspective in a book you have read in German.", "What themes does Kafka's 'Die Verwandlung' address? Use literary vocabulary.", "Write 3-4 sentences analysing a short German text excerpt using the present tense."],
        ),
    ],
}

LESSON_142 = {
    "title": "German Society and Politics: Discourse and Debate",
    "level": "C1",
    "scenario": "political_discussion",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Discuss German political institutions and current affairs with precision",
        "Use political and social science vocabulary accurately",
        "Understand and respond to opinion pieces (Kommentare) and editorials",
        "Express and defend political opinions with appropriate register",
    ],
    "cultural_note": "Germany is a federal parliamentary republic. The Bundestag (parliament), Bundesrat (states' chamber), and Bundesverfassungsgericht (Federal Constitutional Court) are key institutions. Political discourse values consensus-building (Konsensdemokratie) and tends to be more technocratic than adversarial compared to other systems.",
    "grammar_focus": _gex(
        "Passive and Impersonal Constructions in Political Language",
        "Political language uses passive voice and impersonal constructions to de-emphasize agents and create authority: 'Es wird erwartet, dass...' / 'Maßnahmen wurden ergriffen.'",
        "Es muss gehandelt werden. (Action must be taken.) / Die Reform wird umgesetzt. (The reform is being implemented.)",
        ["Vorgangspassiv: wird / werden + Partizip II", "Zustandspassiv: ist / sind + Partizip II (result state)", "Impersonal: Es wird diskutiert. / Es besteht die Erwartung, dass..."],
        ["Die Koalitionsverhandlungen wurden erfolgreich abgeschlossen.", "Es wird erwartet, dass die Inflation sinkt.", "Der Gesetzentwurf ist bereits verabschiedet worden."],
    ),
    "dialogue": [
        _t("commentator", "Die Koalitionsverhandlungen ziehen sich hin. Was bedeutet das für die Stabilität der Regierung?", "The coalition negotiations are dragging on. What does that mean for the stability of the government?"),
        _t("analyst", "Das ist typisch für das deutsche Konsenssystem. Verhandlungen dauern länger, dafür sind die Ergebnisse tragfähiger.", "That is typical of the German consensus system. Negotiations take longer, but the results are more sustainable."),
        _t("commentator", "Kritiker sagen, das System ist zu träge für die heutigen Herausforderungen.", "Critics say the system is too sluggish for today's challenges."),
        _t("analyst", "Das mag sein. Aber schnelle Entscheidungen ohne Konsens führen oft zu gesellschaftlicher Spaltung.", "That may be. But quick decisions without consensus often lead to social division."),
        _t("commentator", "Welche Reformen werden gerade diskutiert?", "What reforms are currently being discussed?"),
        _t("analyst", "Vor allem in der Renten- und Klimapolitik besteht dringender Handlungsbedarf.", "Above all in pension and climate policy there is an urgent need for action."),
        _t("commentator", "Wird das Verfassungsgericht dabei eine Rolle spielen?", "Will the Constitutional Court play a role in this?"),
        _t("analyst", "Sehr wahrscheinlich. Das Bundesverfassungsgericht ist ein wichtiges Korrektiv.", "Very likely. The Federal Constitutional Court is an important corrective."),
    ],
    "vocabulary_list": [
        _v("die Koalitionsverhandlungen (Pl.)", "coalition negotiations", "Die Koalitionsverhandlungen dauern Wochen."),
        _v("die Tragfähigkeit", "sustainability / viability", "Der Kompromiss muss tragfähig sein."),
        _v("der Konsens", "consensus", "Das deutsche System basiert auf Konsens."),
        _v("träge", "sluggish / inert", "Manche kritisieren das System als zu träge."),
        _v("die Spaltung", "division / split", "Politische Spaltung ist eine große Gefahr."),
        _v("das Korrektiv (-e)", "corrective", "Das Gericht dient als Korrektiv."),
        _v("der Handlungsbedarf", "need for action", "Es besteht dringender Handlungsbedarf."),
        _v("verabschieden", "to pass (a law) / to adopt", "Das Gesetz wurde verabschiedet."),
        _v("der Gesetzentwurf (Gesetzentwürfe)", "bill / draft law", "Der Gesetzentwurf wird im Bundestag diskutiert."),
        _v("das Bundesverfassungsgericht", "Federal Constitutional Court", "Das Bundesverfassungsgericht prüft die Verfassungskonformität."),
    ],
    "exercises": [
        _ex_fib(
            "Complete with the correct passive construction",
            ["Die Reform ___ bereits ___ (abschließen – Perfekt Passiv).", "Es ___ erwartet, dass die Wirtschaft wächst.", "Die Koalitionsverhandlungen ___ erfolgreich ___ (abschließen – Präteritum Passiv)."],
            ["ist / abgeschlossen worden", "wird", "wurden / abgeschlossen"],
        ),
        _ex_mc(
            "Political vocabulary: choose the correct answer",
            [
                ("What is the 'Bundesrat'?", ["The federal parliament", "The chamber representing Germany's states", "The Federal Constitutional Court", "The federal government"], 1),
                ("What does 'Konsenssystem' mean in German politics?", ["A system based on majority rule", "A system based on consensus and coalition-building", "A one-party system", "A presidential system"], 1),
                ("What is 'Handlungsbedarf'?", ["A completed action", "Need for action / urgency to act", "Government budget", "Political party"], 1),
            ],
        ),
        _ex_tr(
            "Translate political sentences",
            [
                ("The coalition negotiations were successfully concluded.", "Die Koalitionsverhandlungen wurden erfolgreich abgeschlossen."),
                ("There is an urgent need for action in climate policy.", "In der Klimapolitik besteht dringender Handlungsbedarf."),
                ("The bill is being discussed in the Bundestag.", "Der Gesetzentwurf wird im Bundestag diskutiert."),
            ],
        ),
        _ex_arr(
            "Order the words to form political sentences",
            [
                (["Die", "Reform", "ist", "bereits", "verabschiedet", "worden"], "Die Reform ist bereits verabschiedet worden."),
                (["Es", "wird", "erwartet", "dass", "die", "Inflation", "sinkt"], "Es wird erwartet, dass die Inflation sinkt."),
            ],
        ),
        _ex_sp(
            "Discuss German politics",
            ["Describe how the German political system works to someone unfamiliar with it.", "What do you think are the advantages of a consensus democracy?", "Discuss a current political issue in Germany using passive constructions."],
        ),
    ],
}

LESSON_143 = {
    "title": "Expressing Doubt, Scepticism, and Epistemic Modality",
    "level": "C1",
    "scenario": "academic_discussion",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Express degrees of certainty and doubt using modal verbs and adverbs",
        "Use epistemic modality (dürfte, müsste, könnte, sollte) precisely",
        "Distinguish between deontic and epistemic uses of modal verbs",
        "Respond to claims with appropriate hedging and qualification",
    ],
    "cultural_note": "German academic and intellectual culture prizes precision in expressing certainty. Using 'dürfte' (is probably) instead of 'ist' (is) signals awareness of epistemic limits and is considered intellectually rigorous, not evasive.",
    "grammar_focus": _gex(
        "Epistemic Modal Verbs",
        "Modal verbs in Konjunktiv II express epistemic modality – degrees of probability rather than permission/obligation (deontic). 'Müsste' = should logically be / ought to be; 'dürfte' = is likely/probably; 'könnte' = could possibly; 'sollte' = is said to be.",
        "Das dürfte schwierig sein. (That is probably difficult.) / Das müsste stimmen. (That should be correct.) / Er könnte recht haben. (He might be right.)",
        ["dürfte: high probability (≈ 'probably is')", "müsste: logical expectation (≈ 'should logically be')", "könnte: possibility (≈ 'might be / could be')", "sollte: reported (≈ 'is said to be / reportedly')"],
        ["Das dürfte die Ursache sein. (That is probably the cause.)", "Er müsste schon angekommen sein. (He should have arrived by now.)", "Die Lösung könnte einfacher sein als gedacht. (The solution could be simpler than thought.)"],
    ),
    "dialogue": [
        _t("researcher_a", "Ich glaube, wir haben den Fehler in der Datenanalyse gefunden.", "I think we've found the error in the data analysis."),
        _t("researcher_b", "Das dürfte tatsächlich das Problem sein. Aber ich bin noch nicht hundertprozentig sicher.", "That is probably indeed the problem. But I'm not yet a hundred percent certain."),
        _t("researcher_a", "Die Ergebnisse müssten dann anders aussehen, wenn wir den Datensatz korrigieren.", "The results should then look different if we correct the dataset."),
        _t("researcher_b", "Stimmt. Es könnte aber auch sein, dass der Fehler woanders liegt.", "True. But it's also possible that the error lies elsewhere."),
        _t("researcher_a", "Was sollte das dann sein?", "What should that be then?"),
        _t("researcher_b", "Vielleicht in der Methodik. Das sollte Ihrer Aussage nach eigentlich kontrolliert worden sein.", "Perhaps in the methodology. According to your statement, that should have been controlled."),
        _t("researcher_a", "Stimmt, das hätte kontrolliert werden müssen. Ein Versehen.", "True, that should have been controlled. An oversight."),
        _t("researcher_b", "Kein Problem – das dürfte leicht zu korrigieren sein.", "No problem – that should be easy to correct."),
    ],
    "vocabulary_list": [
        _v("die Epistemik / epistemisch", "epistemics / epistemic", "Epistemische Modalität drückt Wahrscheinlichkeit aus."),
        _v("die Gewissheit", "certainty", "Mit Gewissheit lässt sich das noch nicht sagen."),
        _v("der Vorbehalt (Vorbehalte)", "reservation / caveat", "Ich habe einige Vorbehalte gegenüber dieser Methode."),
        _v("das Versehen (-)", "oversight / mistake", "Das war ein Versehen meinerseits."),
        _v("anzweifeln", "to doubt / question", "Ich zweifle diese These an."),
        _v("spekulativ", "speculative", "Das ist noch sehr spekulativ."),
        _v("nachvollziehbar", "comprehensible / plausible", "Das Argument ist nachvollziehbar."),
        _v("belegen", "to demonstrate / substantiate", "Diese These lässt sich empirisch belegen."),
        _v("widerlegen", "to refute / disprove", "Das Experiment widerlegt die Hypothese."),
        _v("einschränken", "to qualify / limit", "Diese Aussage muss ich einschränken."),
    ],
    "exercises": [
        _ex_fib(
            "Fill in the correct epistemic modal",
            ["Das ___ das Problem sein. (probably is = high probability)", "Er ___ schon wissen, was zu tun ist. (should logically know)", "Die Lösung ___ einfacher sein. (might / could be)"],
            ["dürfte", "müsste", "könnte"],
        ),
        _ex_mc(
            "Deontic or epistemic? Identify the use",
            [
                ("'Du musst das Formular ausfüllen.' – Is this deontic or epistemic?", ["Epistemic (probability)", "Deontic (obligation)", "Both", "Neither"], 1),
                ("'Er muss krank sein.' – Is this deontic or epistemic?", ["Deontic (obligation)", "Epistemic (deduction)", "Request", "Permission"], 1),
                ("'Das dürfte stimmen.' – What does this express?", ["Permission", "Obligation", "Probability", "Doubt"], 2),
            ],
        ),
        _ex_tr(
            "Translate using epistemic modals",
            [
                ("That is probably the correct answer.", "Das dürfte die richtige Antwort sein."),
                ("He should have arrived by now.", "Er müsste inzwischen angekommen sein."),
                ("The solution might be simpler than expected.", "Die Lösung könnte einfacher sein als erwartet."),
            ],
        ),
        _ex_arr(
            "Order to form epistemic sentences",
            [
                (["Das", "dürfte", "die", "Ursache", "des", "Problems", "sein"], "Das dürfte die Ursache des Problems sein."),
                (["Er", "könnte", "recht", "haben", "mit", "seiner", "These"], "Er könnte recht haben mit seiner These."),
            ],
        ),
        _ex_sp(
            "Express degrees of certainty",
            ["State a claim, then express doubt about it using 'dürfte', 'könnte', and 'müsste'.", "Respond to: 'The economy will grow next year.' – agree with hedging, then disagree with hedging.", "Discuss a scientific claim you are uncertain about using epistemic modals."],
        ),
    ],
}

LESSON_144 = {
    "title": "Humour, Irony, and Sarcasm in German",
    "level": "C1",
    "scenario": "social_interaction",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Recognise and produce verbal irony and sarcasm in German",
        "Understand the role of intonation and context in detecting irony",
        "Use understatement (Untertreibung) and hyperbole (Übertreibung) appropriately",
        "Navigate cultural differences in German humour",
    ],
    "cultural_note": "German humour is often dry, ironic, and based on wordplay (Wortspiele) and absurdism. German comedic tradition includes Kabarett (political satire), Loriot's absurdist sketches, and regional humour (Berliner Schnauze, Bavarian). The stereotype that Germans lack humour is largely a misunderstanding rooted in cultural differences.",
    "grammar_focus": _gex(
        "Verbal Irony: Structure and Signals",
        "Irony in German often involves saying the opposite of what is meant, signalled by context, exaggeration, or specific particles like 'ja', 'wohl', 'doch', 'bloß'. The meaning is the opposite of the literal content.",
        "'Na, das war ja eine tolle Idee!' (Well, that was a great idea!) – said when something went wrong",
        ["Irony markers: übertriebenes Lob (excessive praise for failure)", "Understatement: 'Das könnte besser sein.' (That could be better.) for something terrible", "Hyperbole: 'Ich habe tausend Mal gesagt...' / 'Das dauert eine Ewigkeit'"],
        ["Das hat ja super geklappt. (That worked out great.) – when it didn't", "'Kein großes Problem' für eine Katastrophe", "Loriot: 'Ein Klavier! Ein Klavier!' – absurdist deadpan"],
    ),
    "dialogue": [
        _t("anna", "Wie war dein erster Tag im neuen Job?", "How was your first day at the new job?"),
        _t("felix", "Traumhaft. Der Drucker hat zweimal nicht funktioniert, ich habe mich dreimal verlaufen, und in der Mittagspause hat mir jemand mein Essen geklaut.", "Dreamlike. The printer didn't work twice, I got lost three times, and during lunch break someone stole my food."),
        _t("anna", "Na, das klingt nach einem absoluten Erfolg.", "Well, that sounds like an absolute success."),
        _t("felix", "Ja, ich glaube, ich habe einen Traumstart hingelegt.", "Yes, I think I've had a dream start."),
        _t("anna", "Im Ernst – wird es besser?", "Seriously though – will it get better?"),
        _t("felix", "Das kann eigentlich nur besser werden. Tiefer geht's kaum.", "It can only get better. You can't sink much lower."),
        _t("anna", "Das ist der Geist! Oder soll ich sagen: das Bodensatz-Prinzip?", "That's the spirit! Or should I say: the rock-bottom principle?"),
        _t("felix", "Genau. Von hier an geht's nur noch aufwärts. Theoretisch.", "Exactly. From here on it only goes up. Theoretically."),
    ],
    "vocabulary_list": [
        _v("die Ironie", "irony", "Das meinte er natürlich mit Ironie."),
        _v("der Sarkasmus", "sarcasm", "Ihr Sarkasmus war unübersehbar."),
        _v("die Untertreibung (-en)", "understatement", "Das ist eine massive Untertreibung."),
        _v("die Übertreibung (-en)", "exaggeration / hyperbole", "Hundert Mal gesagt – eine typische Übertreibung."),
        _v("das Wortspiel (-e)", "wordplay / pun", "Deutsche Witze basieren oft auf Wortspielen."),
        _v("das Kabarett", "political cabaret / satirical comedy", "Kabarett ist eine wichtige Form der Gesellschaftskritik."),
        _v("der Traumstart", "dream start", "Das war kein Traumstart."),
        _v("aufwärts", "upward / up", "Es geht aufwärts!"),
        _v("trocken (Humor)", "dry (humour)", "Sein trockener Humor ist typisch norddeutsch."),
        _v("im Ernst", "seriously / in earnest", "Im Ernst: Wie geht es dir wirklich?"),
    ],
    "exercises": [
        _ex_mc(
            "Recognise the irony",
            [
                ("'Na, das hat ja super geklappt.' – said when something went badly. What is this?", ["Literal statement", "Verbal irony", "Understatement", "Hyperbole"], 1),
                ("'Ich habe dir das tausend Mal erklärt.' – What is this?", ["Irony", "Literal count", "Hyperbole", "Sarcasm"], 2),
                ("'Das könnte besser sein.' – said about a complete disaster. What is this?", ["Hyperbole", "Understatement", "Irony", "Sarcasm"], 1),
            ],
        ),
        _ex_fib(
            "Complete the ironic responses",
            ["Das erste Date lief nicht gut. 'Na, das war ja ein ___!' (absoluter Erfolg / Traumstart)", "Das Essen schmeckt schrecklich. '___!' (Köstlich!)", "Es regnet in Strömen. '___ für einen Ausflug!' (Tolles Wetter)"],
            ["absoluter Erfolg / Traumstart", "Köstlich!", "Tolles Wetter"],
        ),
        _ex_tr(
            "Translate the ironic statements",
            [
                ("Well, that worked out brilliantly! (when it didn't)", "Na, das hat ja wunderbar geklappt!"),
                ("What a great idea! (when it's terrible)", "Was für eine tolle Idee!"),
                ("That's not a problem at all. (when it's a disaster)", "Das ist überhaupt kein Problem."),
            ],
        ),
        _ex_arr(
            "Reconstruct the ironic exchange",
            [
                (["Na", "das", "war", "ja", "ein", "absoluter", "Erfolg", "oder"], "Na, das war ja ein absoluter Erfolg, oder?"),
            ],
        ),
        _ex_sp(
            "Humour in conversation",
            ["Tell a short ironic story about something that went wrong today.", "Use at least one understatement and one hyperbole.", "Explain a German joke or Kabarett clip to your partner."],
        ),
    ],
}

LESSON_145 = {
    "title": "C1 Comprehensive Review and Consolidation",
    "level": "C1",
    "scenario": "review_session",
    "estimated_minutes": 120,
    "learning_objectives": [
        "Consolidate all major C1 grammar and vocabulary areas",
        "Demonstrate fluency across formal, academic, and professional registers",
        "Identify remaining gaps and plan further C2-oriented study",
        "Produce extended, coherent discourse across multiple genres",
    ],
    "cultural_note": "Reaching C1 means you can use German flexibly and effectively for social, academic, and professional purposes. You can express yourself fluently and spontaneously and produce clear, well-structured text on complex subjects. The step to C2 is about refinement, native-like accuracy, and complete command of idiom and nuance.",
    "grammar_focus": _gex(
        "C1 Grammar Overview",
        "C1 grammar mastery includes: Konjunktiv I (reported speech), Konjunktiv II (counter-factuals, politeness, epistemic modality), Partizipialkonstruktionen, extended noun phrases, passive in all tenses, complex subordinate clause patterns, and advanced modal verb use.",
        "Das von Experten lange diskutierte, aber noch immer nicht gelöste Problem dürfte komplexer sein, als man zunächst angenommen hatte.",
        ["Review: Konjunktiv I vs II distinction", "Review: Partizipialkonstruktionen vs relative clauses", "Review: Epistemic vs deontic modal use", "Review: Passive tenses (Präsens, Perfekt, Plusquamperfekt, Futur)"],
        ["Er sagte, die Lage sei unter Kontrolle. (KI reported speech)", "Wäre ich früher gegangen, hätte ich den Zug nicht verpasst. (KII counter-factual)", "Das dürfte die Lösung sein. (Epistemic)"],
    ),
    "dialogue": [
        _t("tutor", "Wir sind am Ende des C1-Niveaus. Was waren die schwierigsten Themen für Sie?", "We are at the end of the C1 level. What were the most difficult topics for you?"),
        _t("learner", "Konjunktiv I hat mich am meisten verwirrt – vor allem, wann ich Konjunktiv II verwenden soll.", "Konjunktiv I confused me the most – especially when I should use Konjunktiv II instead."),
        _t("tutor", "Das ist sehr häufig. Die Regel: Konjunktiv II, wenn Konjunktiv I identisch mit dem Indikativ wäre.", "That is very common. The rule: Konjunktiv II when Konjunktiv I would be identical to the indicative."),
        _t("learner", "Und die langen Nominalphrasen mit Partizipien – die schreibe ich noch nicht automatisch.", "And the long noun phrases with participles – I don't write those automatically yet."),
        _t("tutor", "Das kommt mit der Leseerfahrung. Lesen Sie viel akademische Prosa.", "That comes with reading experience. Read a lot of academic prose."),
        _t("learner", "Was brauche ich noch für C2?", "What else do I need for C2?"),
        _t("tutor", "C2 ist Verfeinerung: idiomatische Perfektion, stilistische Flexibilität, muttersprachliche Nuanzen.", "C2 is refinement: idiomatic perfection, stylistic flexibility, native-speaker nuances."),
        _t("learner", "Das klingt wie lebenslanges Lernen.", "That sounds like lifelong learning."),
    ],
    "vocabulary_list": [
        _v("die Verfeinerung", "refinement", "C2 erfordert stilistische Verfeinerung."),
        _v("die Nuance (-n)", "nuance", "Native speakers master subtle nuances."),
        _v("idiomatisch", "idiomatic", "Idiomatische Sprache klingt natürlich."),
        _v("die Perfektion", "perfection", "Sprachliche Perfektion ist ein lebenslanger Prozess."),
        _v("automatisch", "automatic / automatically", "Mit Übung kommt automatisches Sprechen."),
        _v("die Leseerfahrung", "reading experience", "Leseerfahrung verbessert den Stil."),
        _v("stilistisch", "stylistic", "Stilistische Vielfalt ist ein C2-Merkmal."),
        _v("konsolidieren", "to consolidate", "Diese Stunde dient der Konsolidierung."),
        _v("identifizieren", "to identify", "Identifizieren Sie Ihre Schwachstellen.", ),
        _v("die Schwachstelle (-n)", "weak point / gap", "Jeder Lernende hat individuelle Schwachstellen."),
    ],
    "exercises": [
        _ex_fib(
            "C1 comprehensive fill-in",
            ["Er berichtete, die Situation ___ unter Kontrolle. (KI)", "Das von Experten ___ Problem dürfte komplex sein. (Partizip II of: diskutieren)", "Die Kosten ___ bereits ___ (abdecken – Zustandspassiv Präsens)."],
            ["sei", "diskutierte", "sind / abgedeckt"],
        ),
        _ex_mc(
            "C1 review: choose the correct form",
            [
                ("Which is Konjunktiv I of 'sein' (3rd person singular)?", ["wäre", "ist", "sei", "war"], 2),
                ("Which sentence uses epistemic modality?", ["Du musst jetzt gehen.", "Das dürfte stimmen.", "Er darf nicht rauchen.", "Kannst du mir helfen?"], 1),
                ("Which contains a Partizipialkonstruktion?", ["Das Buch, das er schrieb", "Das von ihm geschriebene Buch", "Er schrieb das Buch", "Das Buch wurde geschrieben"], 1),
            ],
        ),
        _ex_tr(
            "C1 synthesis translation",
            [
                ("He reportedly said the situation was under control.", "Er sagte, die Lage sei unter Kontrolle."),
                ("The long-discussed, internationally recognised problem requires urgent action.", "Das lange diskutierte, international anerkannte Problem erfordert dringendes Handeln."),
                ("If I had left earlier, I would not have missed the train.", "Wäre ich früher gegangen, hätte ich den Zug nicht verpasst."),
            ],
        ),
        _ex_arr(
            "Order to form a complex C1 sentence",
            [
                (["Das", "von", "Experten", "lange", "diskutierte", "Problem", "dürfte", "komplexer", "sein", "als", "erwartet"], "Das von Experten lange diskutierte Problem dürfte komplexer sein als erwartet."),
            ],
        ),
        _ex_sp(
            "C1 final speaking tasks",
            ["Give a 2-minute presentation on a complex topic of your choice using C1 grammar and vocabulary.", "Debate a political or social issue using concessive structures and epistemic modals.", "Reflect: What has been your greatest achievement in learning German to C1 level?"],
        ),
    ],
}
'''

for num in range(136, 146):
    tag = f"LESSON_{num}"
    if tag in existing:
        print(f"SKIP {tag} already exists")
        APPEND = re.sub(rf"\nLESSON_{num}\s*=.*?(?=\nLESSON_|\Z)", "", APPEND, flags=re.DOTALL)

SEEDS.write_text(src + APPEND, encoding="utf-8")

verify = SEEDS.read_text(encoding="utf-8")
found = sorted(set(re.findall(r"^(LESSON_\d+)\s*=", verify, re.MULTILINE)),
               key=lambda x: int(x.split("_")[1]))
print(f"Total lessons: {len(found)}, range: {found[0]}-{found[-1]}")

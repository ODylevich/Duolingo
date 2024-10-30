import re
from classes import Noun, OtherWord, Verb, PartOfSpeech, PresentConjugation
from typing import Optional, Union


noun_or_word_patterns = [
    # Specific case for "Noun: der Himmel | Plural: die Himmel Translation: sky, heaven Example Usages: Der Himmel ist heute sehr blau. (The sky is very blue today.)"
    r"""
    Noun:\s*                          # Matches 'Noun:' followed by optional whitespace.
    (?P<Sing_Article>[dD]er|[dD]ie|[dD]as)?    # Matches an optional article (Der, Die, Das) in group 1.
    \s*(?P<Main_Noun>\w+(?:\s\w+)*)   # Captures the main noun (single word or phrase) in group 2.
    \s*\|                             # Matches the literal '|' character, indicating the start of the plural.
    \s*Plural:\s*                     # Matches 'Plural:' followed by optional whitespace.
    (?P<Plural_Article>[dD]er|[dD]ie|[dD]as)?  # Matches an optional article for the plural (group 3).
    \s*(?P<Plural>\w+(?:\s\w+)*)      # Captures the plural noun (single word or phrase) in group 4.
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (?P<Translation>.+?)(?=Present|Example|$)                           # Captures the translation text until 'Example' or end of string in group 5.
    """,

    # Specific case for Noun: das HeftPlural: die HefteTranslation: notebook, exercise bookExample Usages:Ich schreibe meine Notizen in ein Heft. (I write my notes in a notebook.)Die Schüler haben ihre Hefte für die Klasse mitgebracht. (The students brought their notebooks for class.)
    r"""
    Noun:\s*                          # Matches 'Noun:' followed by optional whitespace.
    (?P<Sing_Article>[dD]er|[dD]ie|[dD]as)?                    # Matches an optional article (Der, Die, Das) in group 1.
    \s*(?P<Main_Noun>\w+(?:\s\w+)*)             # Captures the main noun (single word or phrase) in group 2.
    Plural:\s*                        # Matches 'Plural:' directly after the noun, with no space.
    (?P<Plural_Article>[dD]er|[dD]ie|[dD]as)?                 # Matches an optional article for the plural (group 3).
    \s*(?P<Plural>\w+(?:\s\w+)*)               # Captures the plural noun (single word or phrase) in group 4.
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (?P<Translation>.+?)(?=Present|Example|$)                           # Captures the translation text until 'Example' or end of string in group 5.
    """,

    # Specific case for Word: Die Reise /Die Reisen Translation: Trip, journey
    r"""
    Word:\s*                        # Matches 'Word:' followed by optional whitespace.
    (?P<Sing_Article>[dD]er|[dD]ie|[dD]as)?      # Matches the singular article (Die) in group 1.
    \s*(?P<Main_Noun>\w+)          # Captures the main word (Reise) in group 2.
    \s*/\s*                        # Matches the '/' character surrounded by optional whitespace.
    (?P<Plural_Article>[dD]er|[dD]ie|[dD]as)?      # Matches the plural article (Die) in group 3.
    \s*(?P<Plural>\w+)              # Captures the plural word (Reisen) in group 4.
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (?P<Translation>.+?)(?=Present|Example|$)                           # Captures the translation text until 'Example' or end of string in group 5.
    """,

    # Specific case for Noun: Wiese | Singular: die Wiese | Plural: die WiesenTranslation: meadow, fieldExample Usages:Die Kinder spielen auf der Wiese. (The children are playing on the meadow.)Die Blumen wachsen auf der Wiese. (The flowers grow in the field.)
    r"""
    Noun:\s*(?P<Main_Noun>\w+)                      # Captures the main noun (e.g., 'Wiese')
    \s*\|\s*                                        # Matches the '|' separator with optional whitespace
    Singular:\s*(?P<Sing_Article>[dD]ie|[dD]er|[dD]as)\s+(?P<Singular_Noun>\w+)   # Captures singular article and noun
    \s*\|\s*                                        # Matches the next '|' separator
    Plural:\s*(?P<Plural_Article>[dD]ie|[dD]er|[dD]as)\s+(?P<Plural>\w+)
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (?P<Translation>.+?)(?=Present|Example|$)                           # Captures the translation text until 'Example' or end of string in group 5.
    """,

    # General case
    r"""
    (?:Noun|Word):?                  # Matches 'Noun' or 'Word', optionally followed by a colon.
    \s*(?P<Sing_Article>[dD]er|[dD]ie|[dD]as)?                 # Matches an optional article (Der, Die, Das) in group 1.
    \s*(?P<Main_Noun>\w+(?:\s\w+)*)                # Captures the main noun/word in group 2 (single word or phrase).
    (?:\s*[\|/]\s*(\w+(?:\s\w+)*))?   # Matches an optional second word, prefixed by '|' or '/' (group 3).
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (?P<Translation>.+?)(?=Present|Example|$)                           # Captures the translation text until 'Example' or end of string in group 5.
    """
]

adjective_or_adverb_patterns = [
    r"""
    (?P<Speech_part>Adjective|Adverb):?\s*            # Matches "Adjective" or "Adverb" as Speech_part
    (?P<Main_Word>\w+(?:\s\w+)?)\s*                   # Main word or phrase (supports one space between words)
    Translation:\s*(?P<Translation>.+?)               # Matches Translation after "Translation:" label
    (?=\s*Example|\s*$)                               # Looks ahead for "Example" or end of line
    """
]

verb_patterns = [
     r"""
    Verb:\s*(?P<Main_Verb>\w+(?:\s\w+)*)
    \s*\|\s*Perfekt:\s*(?P<Perfekt>\w+(?:\s\w+)*)
    \s*Translation:\s*(?P<Translation>.+?)
    \s*Present:\s*
    Ich\s*(?P<first_singular>\w+(?:\s\w+)*)      # 1st person singular (ich)
    \s*\|\s*Wir\s*(?P<first_plural>\w+(?:\s\w+)*) # 1st person plural (wir)
    \s*Du\s*(?P<second_singular>\w+(?:\s\w+)*)   # 2nd person singular (du)
    \s*\|\s*Ihr\s*(?P<second_plural>\w+(?:\s\w+)*) # 2nd person plural (ihr)
    \s*Er/sie/es\s*(?P<third_singular>\w+(?:\s\w+)*) # 3rd person singular (er/sie/es)
    \s*\|\s*Sie\s*(?P<third_plural>\w+(?:\s\w+)*)\s*(?=Example)  # 3rd person plural (sie), up to "Example"
    """,

    r"""
    Verb:?\s*
    (?P<Main_Verb>\w+(?:\s\w+)*)
    \s*(?:\|\s*Perfekt:\s*(?P<Perfekt>\w+(?:\s\w+)*))?\s*
    Translation:\s*
    (?P<Translation>.*?)(?=\s*(?:Present|Example|$))
    """
]

test_cases = [
    'Word: Das Gespräch Translation: Conversation / talk ',
    'Word: das Frühstück Translation: Breakfast ',
    'Word Bis dann Translation: See you then / Until then',
    'Word: Der Spiegel |Die Spiegel Translation: Mirror ',
    'Word: Teuer Translation: Expensive ',
    'Word: Die Reise /Die Reisen Translation: Trip, journey ',
    'Noun: das HeftPlural: die HefteTranslation: notebook, exercise bookExample Usages:Ich schreibe meine Notizen in ein Heft. (I write my notes in a notebook.)Die Schüler haben ihre Hefte für die Klasse mitgebracht. (The students brought their notebooks for class.) ',
    'Noun: der Himmel | Plural: die HimmelTranslation: sky, heavenExample Usages:Der Himmel ist heute sehr blau. (The sky is very blue today.)Sie glaubt an den Himmel nach dem Tod. (She believes in heaven after death.)Am Abend war der Himmel voller Sterne. (In the evening, the sky was full of stars.) ',
    'Noun: Wiese | Singular: die Wiese | Plural: die WiesenTranslation: meadow, fieldExample Usages:Die Kinder spielen auf der Wiese. (The children are playing on the meadow.)Die Blumen wachsen auf der Wiese. (The flowers grow in the field.) ',
    'Adjective: mächtigTranslation: powerfulExample Usages:Der König war ein mächtiger Herrscher. (The king was a powerful ruler.)Die Armee des Feindes war mächtig und gut ausgerüstet. (The enemy"s army was powerful and well-equipped.)Sie hat eine mächtige Rede gehalten. (She gave a powerful speech.) ',
    'Verb: Sagen Translation: To say Present: Ich Du Er/sie/es wir Ihr Sie sage sagst sagt sagen sagt sagen ',
    'Verb: Einsteigen Translation: To enter a transport Present: Ich Du Er/sie/es wir Ihr Sie steige ein steigst ein steigt ein steigen ein steigt ein steigen ein ',
    'Verb: Schauen Translation: To look, watch Present: Ich Du Er/sie/es wir Ihr Sie schaue schaust schaut schauen schaut schauen Geschaut ',
    'Verb: Aussehen Translation: To look, to appear Present: Ich Du Er/sie/es wir Ihr Sie sehe aus siehst aus sieht aus sehen aus seht aus sehen aus ausgesehen Example SentencesPresent Tense:Ich sehe heute müde aus. (I look tired today.)Wie sieht das Kleid aus? (How does the dress look?)Perfekt Tense:Er hat gestern sehr glücklich ausgesehen. (He looked very happy yesterday.)Wir haben schon besser ausgesehen. (We have looked better before.) ',
    'Verb: Dürfen | Perfekt: GedurftTranslation: To be allowed to, mayPresent:Ich darf | Wir dürfenDu darfst | Ihr dürftEr/sie/es darf | Sie dürfenExample SentencesPresent Tense:Darf ich hier sitzen? (May I sit here?)Wir dürfen heute länger bleiben. (We are allowed to stay longer today.)Perfekt Tense:Er hat nicht ins Kino gehen dürfen. (He was not allowed to go to the cinema.)Ich habe das nicht machen dürfen. (I was not allowed to do that.) ',
    'Verb: Anziehen | Perfekt: AngezogenTranslation: To put on (clothes), to dressPresent:Ich ziehe an | Wir ziehen anDu ziehst an | Ihr zieht anEr/sie/es zieht an | Sie ziehen anExample SentencesPresent Tense:Ich ziehe mir eine Jacke an. (I am putting on a jacket.)Ziehst du heute dein neues Kleid an? (Are you wearing your new dress today?)Perfekt Tense:Er hat sich schnell angezogen. (He dressed quickly.)Wir haben uns für die Party schön angezogen. (We dressed nicely for the party.) '
]


def create_word(case: str) -> Optional[Union[Noun, OtherWord, Verb]]:
    """
    Identifies and creates the appropriate word object (Noun, OtherWord, or Verb) based on regex patterns.

    Args:
        case (str): The string containing the word details.

    Returns:
        Union[Noun, OtherWord, Verb, None]: Returns the word object if matched; otherwise, None.
    """

    verb = match_verb(case)
    if verb:
        print(verb)
        return verb

    adjective_or_adverb = match_adjective_or_adverb(case)
    if adjective_or_adverb:
        print(adjective_or_adverb)
        return adjective_or_adverb

    noun_or_word = match_noun_or_word(case)
    if noun_or_word:
        print(noun_or_word)
        return noun_or_word

    print("No match found.")
    return None


def match_noun_or_word(case: str) -> Optional[Union[Noun, OtherWord]]:
    """Attempts to match and return either a Noun or OtherWord object."""
    for pattern in noun_or_word_patterns:
        match = re.search(pattern, case, re.VERBOSE)
        if match:
            match_dict = match.groupdict()
            if match_dict.get("Sing_Article"):
                return Noun(
                    noun=match_dict.get("Main_Noun", ""),
                    gender_article=match_dict.get("Sing_Article", ""),
                    plural_form=match_dict.get("Plural", ""),
                    translation=match_dict.get("Translation", "")
                )
            else:
                return OtherWord(
                    word=match_dict.get("Main_Noun", ""),
                    translation=match_dict.get("Translation", "")
                )
    return None


def match_verb(case: str) -> Optional[Verb]:
    """Attempts to match and return a Verb object."""
    for pattern in verb_patterns:
        match = re.search(pattern, case, re.VERBOSE)
        if match:
            match_dict = match.groupdict()
            conjugation = PresentConjugation(
                singular_1st=match_dict.get("first_singular", "").strip(),
                singular_2nd=match_dict.get("second_singular", "").strip(),
                singular_3rd=match_dict.get("third_singular", "").strip(),
                plural_1st=match_dict.get("first_plural", "").strip(),
                plural_2nd=match_dict.get("second_plural", "").strip(),
                plural_3rd=match_dict.get("third_plural", "").strip()
            )
            return Verb(main_verb=match_dict.get("Main_Verb", ""),
                        perfekt=match_dict.get("Perfekt", ""),
                        translation=match_dict.get("Translation", ""),
                        present_conjugation=conjugation)
    return None


def match_adjective_or_adverb(case: str) -> Optional[OtherWord]:
    """Attempts to match and return an adjective or adverb as an OtherWord object."""
    for pattern in adjective_or_adverb_patterns:
        match = re.search(pattern, case, re.VERBOSE)
        if match:
            match_dict = match.groupdict()
            part_of_speech = (
                PartOfSpeech[match_dict.get("Speech_part", "").strip().upper()]
                if match_dict.get("Speech_part", "").strip().upper() in PartOfSpeech.__members__
                else PartOfSpeech.OTHER
            )
            return OtherWord(
                word=match_dict.get("Main_Word", ""),
                translation=match_dict.get("Translation", ""),
                part_of_speech=part_of_speech
            )

    return None


for case in test_cases:
    create_word(case)

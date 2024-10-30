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
    (.+?)                             # Captures the translation text until 'Example' or end of string in group 5.
    (?=Example|$)                     # Positive lookahead to ensure 'Example' or end of string follows.
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
    (.+?)                             # Captures the translation text until 'Example' or end of string in group 5.
    (?=Example|$)                     # Positive lookahead to ensure 'Example' or end of string follows.
    """,

    # Specific case for Word: Die Reise /Die Reisen Translation: Trip, journey
    r"""
    Word:\s*                        # Matches 'Word:' followed by optional whitespace.
    (?P<Sing_Article>[dD]er|[dD]ie|[dD]as)?      # Matches the singular article (Die) in group 1.
    \s*(?P<Main_Noun>\w+)          # Captures the main word (Reise) in group 2.
    \s*/\s*                        # Matches the '/' character surrounded by optional whitespace.
    (?P<Plural_Article>[dD]er|[dD]ie|[dD]as)?      # Matches the plural article (Die) in group 3.
    \s*(?P<Plural>\w+)              # Captures the plural word (Reisen) in group 4.
    \s*Translation:\s*              # Matches 'Translation:' followed by optional whitespace.
    (.+?)                           # Captures the translation text (Trip, journey) until end of string.
    """,

    # Specific case for Noun: Wiese | Singular: die Wiese | Plural: die WiesenTranslation: meadow, fieldExample Usages:Die Kinder spielen auf der Wiese. (The children are playing on the meadow.)Die Blumen wachsen auf der Wiese. (The flowers grow in the field.)
    r"""
    Noun:\s*(?P<Main_Noun>\w+)                      # Captures the main noun (e.g., 'Wiese')
    \s*\|\s*                                        # Matches the '|' separator with optional whitespace
    Singular:\s*(?P<Sing_Article>[dD]ie|[dD]er|[dD]as)\s+(?P<Singular_Noun>\w+)   # Captures singular article and noun
    \s*\|\s*                                        # Matches the next '|' separator
    Plural:\s*(?P<Plural_Article>[dD]ie|[dD]er|[dD]as)\s+(?P<Plural>\w+)(?=\s*Translation|$)   # Captures plural article and noun, stops before 'Translation' or end of line
    """,

    # General case
    r"""
    (?:Noun|Word):?                  # Matches 'Noun' or 'Word', optionally followed by a colon.
    \s*([dD]er|[dD]ie|[dD]as)?                 # Matches an optional article (Der, Die, Das) in group 1.
    \s*(\w+(?:\s\w+)*)                # Captures the main noun/word in group 2 (single word or phrase).
    (?:\s*[\|/]\s*(\w+(?:\s\w+)*))?   # Matches an optional second word, prefixed by '|' or '/' (group 3).
    \s*Translation:\s*                # Matches 'Translation:' followed by optional whitespace.
    (.+?)                             # Captures the translation text in group 4 until 'Example' or end of string.
    (?=Example|$)                     # Positive lookahead for 'Example' or end of string.
    """
]


verb_patterns = r"Verb:?\s*(\w+|\w+\s\w+)"
adjective_or_adverb_patterns = r"(?:Adjective|Adverb):?\s*(\w+|\w+\s\w+)\s*Translation:\s*(.+?)(?=Example|$)"
translation_patterns = r"Translation:\s*(.+?)(?=Present|Example|$)"
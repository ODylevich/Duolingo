from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
from enum import Enum, auto


class PartOfSpeech(Enum):
    """
    Enumeration of parts of speech to standardize allowed values.
    """
    ADVERB = "adverb"
    ADJECTIVE = "adjective"
    PHRASE = "phrase"
    OTHER = "other"


PresentConjugation = namedtuple('Conjugation', ['singular_1st', 'plural_1st', 'singular_2nd', 'plural_2nd', 'singular_3rd', 'plural_3rd'])


@dataclass
class Noun:
    """
    Represents a noun with its grammatical and usage details in German.
    """
    noun: str
    gender_article: str
    plural_form: str
    translation: str
    examples: List[Tuple[str, str]] = field(default_factory=list)

    def __post_init__(self):
        self.gender_article = self.gender_article.lower()

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the Noun instance.
        """
        examples_text = "\n".join(f"{s} - {t}" for s, t in self.examples)
        return (
            f"Singular: {self.gender_article} {self.noun}\n"
            f"Plural: {self.plural_form}\n"
            f"Translation: {self.translation}\n"
            f"Examples:\n{examples_text}"
        )

    def add_example(self, sentence: str, translation: str) -> None:
        """
        Adds an example sentence with its English translation to the list of examples.
        """
        self.examples.append((sentence, translation))

    def display_examples(self) -> None:
        """
        Prints each example sentence along with its English translation, formatted for readability.
        """
        for sentence, translation in self.examples:
            print(f"{sentence} - {translation}")


@dataclass
class Verb:
    """
    Represents a verb with its grammatical details in German.

    Attributes:
        main_verb (str): The base form of the verb (e.g., "Erleben").
        perfekt (str): The perfect tense form of the verb (e.g., "Erlebt").
        translation (str): The English translation of the verb (e.g., "To experience").
        present_conjugation (PresentConjugation): The present tense conjugation of the verb.
        examples (List[Tuple[str, str]]): A list of example sentences with their translations,
            where each item is a tuple containing the sentence in German and its English translation.
    """
    main_verb: str
    perfekt: str
    translation: str
    present_conjugation: PresentConjugation
    examples: List[Tuple[str, str]] = field(default_factory=list)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the Verb instance.
        """
        conjugation_str = (
            f"Ich {self.present_conjugation.singular_1st} | Wir {self.present_conjugation.plural_1st}\n"
            f"Du {self.present_conjugation.singular_2nd} | Ihr {self.present_conjugation.plural_2nd}\n"
            f"Er/sie/es {self.present_conjugation.singular_3rd} | Sie {self.present_conjugation.plural_3rd}\n"
        )

        return (f"Verb: {self.main_verb}\n"
                f"Perfekt: {self.perfekt}\n"
                f"Translation: {self.translation}\n"
                f"{conjugation_str}"
                f"Examples:\n" +
                "\n".join(f"  - {sentence} (Translation: {translation})" for sentence, translation in self.examples))

    def add_example(self, sentence: str, translation: str) -> None:
        """
        Adds an example sentence with its English translation to the list of examples.

        Args:
            sentence (str): The example sentence in German.
            translation (str): The English translation of the sentence.
        """
        self.examples.append((sentence, translation))

    def display_examples(self) -> None:
        """
        Prints each example sentence along with its English translation, formatted for readability.
        """
        for sentence, translation in self.examples:
            print(f"{sentence} - {translation}")


conjugation = PresentConjugation(
    singular_1st="erlebe",
    singular_2nd="erlebst",
    singular_3rd="erlebt",
    plural_1st="erleben",
    plural_2nd="erlebt",
    plural_3rd="erleben"
)

verb = Verb(
    main_verb="Erleben",
    perfekt="Erlebt",
    translation="To experience",
    present_conjugation=conjugation
)


@dataclass
class OtherWord:
    """
    Represents words other than nouns and verbs, such as adverbs, adjectives, and expressions,
    with their translations and usage examples.

    Attributes:
        word (str): The primary word or expression (e.g., "schnell").
        translation (str): English translation of the word (e.g., "fast").
        part_of_speech (Optional[str]): The grammatical category, like adverb, adjective, or phrase (e.g., "adverb").
        examples (List[Tuple[str, str]]): A list of example sentences with translations,
            where each tuple contains the sentence in German and its English translation.
    """
    word: str
    translation: str
    part_of_speech: PartOfSpeech = PartOfSpeech.OTHER
    examples: List[Tuple[str, str]] = field(default_factory=list)

    def add_example(self, sentence: str, translation: str) -> None:
        """
        Adds an example sentence with its English translation to the list of examples.

        Args:
            sentence (str): The example sentence in German.
            translation (str): The English translation of the sentence.
        """
        self.examples.append((sentence, translation))

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the OtherWord instance.
        """
        example_str = "\n".join([f"{sent} ({trans})" for sent, trans in self.examples])
        return (f"Word: {self.word} ({self.part_of_speech.value})\n"
                f"Translation: {self.translation}\n"
                f"Examples:\n{example_str}")


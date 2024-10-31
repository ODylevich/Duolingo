from bs4 import BeautifulSoup
import re
from classes import Noun, OtherWord, Verb, PartOfSpeech, PresentConjugation
from typing import Optional, Union
from regex_patterns import noun_or_word_patterns, verb_patterns, adjective_or_adverb_patterns


def make_plain_text(text: str) -> str:
    """
    This function uses BeautifulSoup to parse the input HTML
    and extract the plain text content.

    :param text: str - The HTML formatted text to be converted.
    :return: str - The plain text extracted from the HTML input.
    """
    raw_content = text
    soup = BeautifulSoup(raw_content, 'html.parser')
    return soup.get_text()


eligible_frame_titles = {
    "Copy of Noun",
    "Copy of Word",
    "Copy of Verb conjugation"}


def is_title_match(item_title: str) -> bool:
    """
    Checks if the given title is in the predefined set of titles to match.
    """
    return item_title in eligible_frame_titles


def gather_plain_text_from_frame(client, board_id: str, frame_id: str) -> str:
    """
    Collects and concatenates all plain text within a frame.
    """
    frame_items = client.get_all_items_within_frame(board_id=board_id, parent_item_id=frame_id)
    full_plain_text = " ".join(make_plain_text(item.data.actual_instance.content) for item in frame_items)
    return full_plain_text


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
                PartOfSpeech[str(match_dict.get("Speech_part", "").strip().upper())]
                if match_dict.get("Speech_part", "").strip().upper() in PartOfSpeech.__members__
                else PartOfSpeech.OTHER
            )
            return OtherWord(
                word=match_dict.get("Main_Word", ""),
                translation=match_dict.get("Translation", ""),
                part_of_speech=part_of_speech
            )

    return None


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
import miro_api
import re
from utils import is_title_match, gather_plain_text_from_frame
from regex_patterns import noun_or_word_patterns, verb_patterns, adjective_or_adverb_patterns, translation_patterns
from config import MIRO_ACCESS_TOKEN, BOARD_ID

client = miro_api.MiroApi(MIRO_ACCESS_TOKEN)

items = client.get_all_items(board_id=BOARD_ID, type='frame')


def parse_text(full_plain_text):
    # Initialize dictionary to store parsed information
    return_dict = {"Word_type": "", "Word": "", "Gender": "", "Plural_form": "", "Translation": ""}

    for index, pattern in enumerate(noun_or_word_patterns, start=1):
        noun_or_word_match = re.search(pattern, full_plain_text, re.VERBOSE)
        if noun_or_word_match:
            if index == 1:
                return_dict["Word"] = noun_or_word_match.group("Main_Noun")
                return_dict["Gender"] = noun_or_word_match.group("Sing_Article")
                return_dict["Plural_form"] = noun_or_word_match.group("Plural")
                return_dict["Word_type"] = 'Noun'
                return_dict["Recognized_pattern"] = index

            elif index == 2:
                return_dict["Word"] = noun_or_word_match.group(2)
                return_dict["Gender"] = noun_or_word_match.group(1) or ""
                return_dict["Plural_form"] = noun_or_word_match.group(4) or ""
                return_dict["Word_type"] = 'Noun'
                return_dict["Recognized_pattern"] = index

            elif index == 3:
                return_dict["Word"] = noun_or_word_match.group("Main_Noun")
                return_dict["Gender"] = noun_or_word_match.group("Sing_Article")
                return_dict["Plural_form"] = noun_or_word_match.group("Plural")
                return_dict["Word_type"] = 'Noun'
                return_dict["Recognized_pattern"] = index

            elif index == 4:
                return_dict["Word"] = noun_or_word_match.group("Main_Noun")
                return_dict["Gender"] = noun_or_word_match.group("Sing_Article")
                return_dict["Plural_form"] = noun_or_word_match.group("Plural")
                return_dict["Word_type"] = 'Noun'
                return_dict["Recognized_pattern"] = index

            elif index == 5:
                return_dict["Word"] = noun_or_word_match.group(2)
                return_dict["Gender"] = noun_or_word_match.group(1) or ""
                return_dict["Word_type"] = "Noun" if noun_or_word_match.group(1) else "Unknown"
                return_dict["Recognized_pattern"] = index
    # Check if the text is a verb
    verb_match = re.search(verb_patterns, full_plain_text)
    if verb_match:
        return_dict["Word_type"] = "Verb"
        return_dict["Word"] = verb_match.group(1)

    # Check if the text is an adjective
    adj_match = re.search(adjective_or_adverb_patterns, full_plain_text)
    if adj_match:
        return_dict["Word_type"] = "Adjective"
        return_dict["Word"] = adj_match.group(1)

    # Extract the translation if available
    translation_match = re.search(translation_patterns, full_plain_text)
    if translation_match:
        return_dict["Translation"] = translation_match.group(1).strip()

    return return_dict


for item in items:
        item_title = item.data.actual_instance.title
        if is_title_match(item_title):
            full_plain_text = gather_plain_text_from_frame(client, BOARD_ID, item.id)
            print(f'Full plain text: {full_plain_text}')

            main_info = parse_text(full_plain_text)

            if main_info["Word"]:
                print(f'    Parsed information: {main_info}')
            else:
                print('    Parsed information: None')



from utils.utils import is_title_match, gather_plain_text_from_frame, create_word
from config.config import  BOARD_ID
from utils.loader import App

duolingo = App()

items = duolingo.miro_client.get_all_items(board_id=BOARD_ID, type='frame')

all_words = []

for item in items:
        item_title = item.data.actual_instance.title
        if is_title_match(item_title):
            full_plain_text = gather_plain_text_from_frame(duolingo.miro_client, BOARD_ID, item.id)
            print(f'Full plain text: {full_plain_text}')
            created_word = create_word(full_plain_text)
            if created_word:
                all_words.append(created_word)

print(f'Created {len(all_words)} words')




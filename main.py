import random


class Card:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.picked_side = ""
        self.unpicked_side = ""

    def pick_card(self):
        self.picked_side, self.unpicked_side = random.sample([self.word, self.translation], 2)
        return self.picked_side

    def check_user(self, user_answer):
        return user_answer == self.unpicked_side


cards = []

new_words = {
    'Hola': 'Привет',
    'Adios': "Пока",
    'Gracias': 'Спасибо',
    'Palabras': 'Слова'
}

for key, value in new_words.items():
    cards.append(Card(word=key, translation=value))


def get_card():
    random_index = random.randint(0, len(cards) - 1)
    return cards[random_index].pick_card(), cards[random_index].unpicked_side



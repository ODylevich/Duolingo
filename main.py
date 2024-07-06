import random


class Card:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.picked_side = ""

    def pick_card(self):
        self.picked_side = random.choice([self.word, self.translation])
        return self.picked_side


cards = []

new_words = {
    'Hola': 'Привет',
    'Adios': "Пока",
    'Gracias': 'Спасибо'
}

for key, value in new_words.items():
    cards.append(Card(word=key, translation=value))

print(f'Picked card function: {cards[0].pick_card()}')
print(f'Picked side : {cards[0].picked_side}')
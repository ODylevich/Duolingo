import random


class Card:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.picked_side = ""

    def pick_card(self):
        self.picked_side = random.choice([self.word, self.translation])
        print(self.picked_side)

    def check_word(self):
        user_answer = input("Write the word")
        if (user_answer == self.word or user_answer == self.translation):
            print("Well done ")
        else:
            print("Not well done")









cards = []

new_words = {
    'Hola': 'Приветтт',
    'Adios': "Пока",
    'Gracias': 'Спасибо',
    'Palabras': 'Слова'
}

for key, value in new_words.items():
    cards.append(Card(word=key, translation=value))


random_index = random.randint(0,len(cards)-1)
cards[random_index].pick_card()
cards[random_index].check_word()
import spacy
import requests
from googletrans import Translator

translator = Translator()
nlp = spacy.load("de_core_news_sm")

doc = nlp("machen")
for token in doc:
    print(f'Word: {token.text}, translation: {translator.translate(token.text, src="de", dest="en").text}')
    print(token.text, token.pos_, token.morph.get('Gender'), token.lemma_)


def get_verb_forms(verb):
    # Process the verb using spaCy
    doc = nlp(verb)

    for token in doc:
        if token.pos_ == "VERB":
            # Present tense conjugation (for 'ich')
            present_tense = f"ich {token.lemma_}e"  # Basic conjugation
            if token.lemma_ == "sein":
                present_tense = "ich bin"
            elif token.lemma_ == "haben":
                present_tense = "ich habe"
            else:
                # Handle regular verbs for 'ich' conjugation
                present_tense = f"ich {token.lemma_[:-1]}e" if token.lemma_[-1] == 'n' else f"ich {token.lemma_}e"

            # Perfekt form
            if token.lemma_ == "sein":
                perfekt_form = "sein gewesen"
            elif token.lemma_ == "haben":
                perfekt_form = "haben gehabt"
            else:
                # Create the past participle for regular verbs
                if token.lemma_[-2:] == "en":
                    past_participle = token.lemma_[:-2] + "t"
                else:
                    past_participle = token.lemma_ + "t"  # Simplified for demonstration
                perfekt_form = f"haben {past_participle}"

            return {
                "Present Tense": present_tense,
                "Perfekt Form": perfekt_form
            }

# Example usage
verb = "lernen"  # The infinitive form
verb_forms = get_verb_forms(verb)
print(verb_forms)

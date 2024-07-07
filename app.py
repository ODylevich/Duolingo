from flask import Flask, render_template, request, jsonify, session
from main import get_card
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    word, translation = get_card()
    session['word'] = word
    session['real_translation'] = translation
    print('In home')
    return render_template('index.html', word=word)


@app.route('/check', methods=['POST'])
def card_check():
    user_translation = request.form.get('user_translation')
    real_translation = session.get('real_translation')
    word = session.get('word')
    if user_translation != real_translation:
        return render_template('index.html', word=word, real_translation=real_translation,
                               is_correct=False)
    else:
        word, translation = get_card()
        session['word'] = word
        session['real_translation'] = translation
        return render_template('index.html', word=word, real_translation=real_translation,
                               is_correct=True)


if __name__ == '__main__':
    app.run(debug=True)

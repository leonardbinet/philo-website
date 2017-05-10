#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import logging
import logging.config
import setpath
from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

app = Flask(__name__)

app.secret_key = "yodela"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/new-game', methods=['POST'])
def new_game():
    session['score'] = 0
    session['article'] = request.form["page"]
    return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    page = session['article']
    title, items = getPage(page)
    score = session['score']
    if title == "Philosophie" and score == 0:
        flash('Tricheur! (tu sors!)')
        return render_template('index.html')
    elif title == "Philosophie":
        flash('Gagné! (score: %s)' % score)
        return render_template('index.html')
    elif title is None:
        flash('Aucun article trouvé!')
        return render_template('index.html')

    return render_template('game.html', title=title, items=items)


@app.route('/move', methods=['POST'])
def move():
    session['score'] += 1
    session['article'] = request.form["page"]
    return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)

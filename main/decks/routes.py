from flask import Blueprint
from main import db
from flask import render_template, url_for, redirect, abort
from main.decks.forms import CreateDeckForm, CreateCardForm
from main.models import User, Deck, Card
from flask_login import current_user, login_required
import random

decks = Blueprint('decks', __name__)


@decks.route('/decks', methods=['GET', 'POST'])
@login_required
def all_decks():
    form = CreateDeckForm()
    if form.validate_on_submit():
        deck = Deck(title=form.title.data, owner_id=current_user.id)
        db.session.add(deck)
        db.session.commit()
        return redirect(url_for('decks.all_decks'))
    return render_template('decks.html', title="Decks", form=form, Card=Card)


@decks.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    # TODO: Deck should exist!

    # Shouldn't want users to access decks they dont own!
    if deck.owner_id != current_user.id:
        abort(403)
    form = CreateCardForm()
    if form.validate_on_submit():
        card = Card(front=form.front.data,
                    back=form.back.data, deck_id=deck_id)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('decks.deck', deck_id=deck_id))
    return render_template('deck.html', title="Deck", deck=deck, form=form)


@decks.route('/study/<int:deck_id>')
@login_required
def study_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    # Can't study from a deck you don't own
    if deck.owner_id != current_user.id:
        abort(403)
    # Get all cards associated with deck -- shuffle them
    cards = Card.query.filter_by(deck_id=deck_id).all()
    random.shuffle(cards)
    return render_template('study.html', cards=cards)


@decks.route('/delete_deck/<int:deck_id>')
@login_required
def delete_deck(deck_id):
    # Shouldn't be able to delete deck if don't own it!
    deck = Deck.query.get_or_404(deck_id)
    if deck.owner_id != current_user.id:
        abort(403)

    # Delete all associated cards
    for card in Card.query.filter_by(deck_id=deck_id):
        db.session.delete(card)
    db.session.delete(deck)
    db.session.commit()
    # redirect to decks page
    return redirect(url_for('decks.all_decks'))

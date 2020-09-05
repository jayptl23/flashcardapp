from flask import Blueprint
from main import db
from flask import render_template, url_for, redirect, flash, abort
from main.cards.forms import EditCardForm
from main.models import Deck, Card
from flask_login import current_user, login_required

cards = Blueprint('cards', __name__)


@cards.route('/edit_card/<int:deck_id>/<int:card_id>', methods=['GET', 'POST'])
@login_required
def edit_card(deck_id, card_id):
    # Check if decks exists
    deck = Deck.query.get_or_404(deck_id)

    # If user doesn't own deck abort
    if deck.owner_id != current_user.id:
        abort(403)

    curr_card = Card.query.get_or_404(card_id)

    # Check if card belongs to deck
    if curr_card.deck_id != deck_id:
        abort(403)
    form = EditCardForm()
    if form.validate_on_submit():
        curr_card.front = form.front.data
        curr_card.back = form.back.data
        db.session.commit()
        flash("Card Updated!", "success")
        return redirect(url_for('cards.edit_card', deck_id=deck_id, card_id=card_id))
    form.front.data = curr_card.front
    form.back.data = curr_card.back
    return render_template('edit.html', title="Edit Card", deck_id=deck_id, card=curr_card, form=form)


@cards.route('/delete_card/<int:deck_id>/<int:card_id>')
@login_required
def delete_card(deck_id, card_id):
    # Check if decks exists
    deck = Deck.query.get_or_404(deck_id)

    # If user doesn't own deck abort
    if deck.owner_id != current_user.id:
        abort(403)

    # If card not found or doesn't belong to deck throw 404
    card = Card.query.get_or_404(card_id)
    if card.deck_id != deck_id:
        abort(404)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('decks.deck', deck_id=deck_id))

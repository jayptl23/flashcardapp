from main import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    decks = db.relationship('Deck', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.decks}')"


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card', backref="deck", lazy=True)

    def __repr__(self):
        return f"Deck('{self.id}', '{self.title}', '{self.owner_id}')"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(500), nullable=False)
    back = db.Column(db.String(500), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return f"Card('{self.id}', '{self.front}', '{self.back}', '{self.deck_id}')"

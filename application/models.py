"""Data models."""
from . import db


class Result(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'dice-results'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    modifier = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    result = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<DiceResult {} - {}>'.format(self.name, self.id)


class Dice(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'dice-dices'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    resultId = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    diceType = db.Column(
        db.String(8),
        index=False,
        unique=False,
        nullable=False
    )
    value = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<Dice {}>'.format(self.name)

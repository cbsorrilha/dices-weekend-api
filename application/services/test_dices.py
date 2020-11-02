from flask_sqlalchemy import SQLAlchemy
from application.tests.fixtures import app, db  # noqa
from datetime import datetime as dt
from application.models import Result, Dice
from application.services.dices import DiceService


def test_get_all(db: SQLAlchemy):  # noqa
    yin = Result(
        name='Tester',
        modifier=0,
        created=dt.now(),
        result=10,
    )
    yang = Result(
        name='Tester',
        modifier=0,
        created=dt.now(),
        result=10,
    )

    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()

    yin_dice = Dice(
        resultId=yin.id,
        diceType=6,
        value=11,
    )

    yang_dice = Dice(
        resultId=yang.id,
        diceType=6,
        value=10,
    )

    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()

    results = DiceService.list(4)

    assert len(results) == 2
    assert yin in results and yang in results


def test_create(db: SQLAlchemy):  # noqa
    dice = {diceType: 6}
    DiceService.create(
        name='teste',
        modifier=10,
        mode='sum',
        dices=[dice])

    results = DiceService.list(4)

    assert len(results) == 1

    for k in yin.keys():
        assert getattr(results[0], k) == yin[k]

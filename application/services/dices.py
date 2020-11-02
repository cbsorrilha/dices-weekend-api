from functools import reduce
from random import randint
from operator import add
from datetime import datetime as dt
from ..models import db, Result, Dice
from ..schemas import ResultSchema, DiceSchema


def get_value(dice):
    return dice['value']


def generate_result(dices, mode, modifier):
    valueList = list(map(get_value, dices))
    if mode == 'sum':
        result = reduce(
            add,
            valueList,
            0
        )
        return max(result + modifier, 1)
    return max(max(valueList) + modifier, 1)


def generate_individual_results(dices):
    with_results = list()

    for dice in dices:
        with_results.append(
            {'diceType': dice['diceType'], 'value': randint(1, dice['diceType'])})

    return with_results


class DiceService:
    def list(limit):
        results = Result.query.order_by(
            Result.created.desc()).limit(limit).all()
        complete_results = list()

        for result in results:
            dices = Dice.query.filter_by(resultId=result.id).all()
            result.dices = dices
            complete_results.append(result)

        return complete_results

    def create(name, modifier, mode, dices):
        if name == False or name == None:
            raise TypeError('name is required')
        if dices == False or dices == None or not isinstance(dices, list) or len(dices) == 0:
            raise TypeError('dices is required and must an array')
        if mode != 'sum' and mode != 'minmax' and mode != None:
            raise TypeError('mode must be sum or minmax or null')

        individual_results = generate_individual_results(dices)
        new_result = Result(
            name=name,
            modifier=modifier,
            created=dt.now(),
            result=generate_result(individual_results, mode, modifier),
        )

        # Adds new User record to database
        db.session.add(new_result)

        db.session.commit()  # Commits all changes

        for dice in individual_results:
            new_dice = Dice(
                resultId=new_result.id,
                diceType=dice['diceType'],
                value=dice['value'],
            )
            db.session.add(new_dice)

        db.session.commit()

        return new_result, individual_results

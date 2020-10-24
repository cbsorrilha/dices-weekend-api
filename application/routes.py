from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Result, Dice
from functools import reduce
from random import randint
from operator import add
from marshmallow import Schema, fields


class DiceSchema(Schema):
    diceType = fields.Integer()
    value = fields.Integer()


class ResultSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    mode = fields.Str()
    modifier = fields.Integer()
    created = fields.Date()
    result = fields.Integer()
    dices = fields.List(fields.Nested(DiceSchema))


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in db.inspect(obj).mapper.column_attrs}


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


@app.route('/create', methods=['POST'])
def create_dices():
    """Create a dice result post."""
    request.get_json(force=True)
    name = request.json.get('name')
    modifier = request.json.get('modifier')
    mode = request.json.get('mode')
    dices = request.json.get('dices')

    if name and dices and len(dices) > 0 and (mode == 'sum' or mode == 'minmax'):
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

        return {'result': object_as_dict(new_result), 'dices': individual_results}


@app.route('/list', methods=['GET'])
def list_dices():
    """List dices results."""
    limit = 4
    argLimit = request.args.get('limit')
    if (argLimit):
        limit = argLimit

    results = Result.query.order_by(Result.created.desc()).limit(limit).all()
    schema = ResultSchema(many=True)

    complete_results = list()
    for result in results:
        dices = Dice.query.filter_by(resultId=result.id).all()
        result.dices = dices
        complete_results.append(result)
    return {'results': schema.dump(complete_results)}
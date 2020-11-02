from pytest import fixture
from .models import Result, Dice


@fixture
def result() -> Result:
    return Result(
        name='test', modifier='sum', result=10, created='2020-11-02T09:58:25'
    )


def test_Result_create(result: Result):
    assert result


@fixture
def dice() -> Dice:
    return Dice(
        resultId=1,
        diceType=6,
        value=10
    )


def test_Dice_create(dice: Dice):
    assert dice

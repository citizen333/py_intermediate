import pytest
from scripts.base_classes import A, B, C

data = [x/11 for x in range(1, 11)]
result = [0, 1] * 5

@pytest.mark.parametrize(
    "cls, data, result, score",
    [(A, data, result, 0.6),
     (B, data, result, 0.6),
     (C, data, result, 0.6)]
)
def test_get_score(cls, data, result, score):
    obj = cls(data, result)
    assert obj.get_score() == score

@pytest.mark.parametrize(
    "cls, data, result, loss",
    [(A, data, result, 2.7272727272727275),
     (B, data, result, 7.47249743682016),
     (C, data, result, 4.545454545454545)]
)
def test_get_loss(cls, data, result, loss):
    obj = cls(data, result)
    assert obj.get_loss() == loss
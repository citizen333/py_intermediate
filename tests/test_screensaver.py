import pytest
from screensaver import screen
from screensaver import screen_old

@pytest.mark.parametrize("vec_1, vec_2", [([2, 5], [1, 2])])
def test_vec2d_add(vec_1, vec_2):
    vec2d_1 = screen.Vec2d(vec_1[0], vec_1[1])
    vec2d_2 = screen.Vec2d(vec_2[0], vec_2[1])
    assert vec2d_1 + vec2d_2 == screen_old.add(vec_1, vec_2)
    
@pytest.mark.parametrize("vec_1, vec_2", [([2, 5], [1, 2])])
def test_vec2d_sub(vec_1, vec_2):
    vec2d_1 = screen.Vec2d(vec_1[0], vec_1[1])
    vec2d_2 = screen.Vec2d(vec_2[0], vec_2[1])
    assert vec2d_1 - vec2d_2 == screen_old.sub(vec_1, vec_2)

@pytest.mark.parametrize("vec, coef", [([2, 5], 4)])
def test_vec2d_mul(vec, coef):
    vec2d = screen.Vec2d(vec[0], vec[1])
    assert vec2d * coef == screen_old.mul(vec, coef)
    
@pytest.mark.parametrize("vec", [([2, 5])])
def test_vec2d_repr(vec):
    vec2d = screen.Vec2d(vec[0], vec[1])
    assert vec2d.int_pair() == screen_old.vec([0, 0], vec)
    
@pytest.mark.parametrize("vec", [([2, 5])])
def test_vec2d_len(vec):
    vec2d = screen.Vec2d(vec[0], vec[1])
    assert len(vec2d) == int(screen_old.length(vec))
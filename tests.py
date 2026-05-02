import pytest
from copy import deepcopy
from main import legal_move, make_move, unmake_move, evaluate, victory_conditions, negamax

##===========Fixures===========

@pytest.fixture
def empty_board():
    board = [[[None, None] for _ in range(8)] for _ in range(8)]
    return board

@pytest.fixture
def initial_state():
    board = empty_board()
    board[6][3][1] = ("red", "dark")
    board[1][4][1] = ("blue", "light")
    return {
        "board": board,
        "current": 0,
        "color": None
    }

##===========Tests unitaires===========

def test_is_legal_move_empty():
    state = {
        "board": empty_board(),
        "current": 0,
        "color": None
    }
    moves = legal_move(state)
    assert moves == []

def test_is_legal_move_not_empty():
    state = initial_state()
    moves = legal_move(state)
    assert len(moves) > 0

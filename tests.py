import pytest
from copy import deepcopy
from main import legal_move, make_move, unmake_move, evaluate, victory_conditions, negamax

##===========Fixures===========

@pytest.fixture
def empty_board():
    board = [[[None, None] for _ in range(8)] for _ in range(8)]
    return board

@pytest.fixture
def initial_state(empty_board):
    state = {
        "board": deepcopy(empty_board),
        "current": 0,        
        "color": None
    }
    return state
##===========Tests unitaires===========

def test_is_legal_move_empty(initial_state):
    moves = legal_move(initial_state)
    assert moves == []
    

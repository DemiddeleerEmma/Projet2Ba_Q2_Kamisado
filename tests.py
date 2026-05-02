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
class Test_legal_move_0: 
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

class Test_make_move():
    def test_make_move():
        state = initial_state()
        move = [[6,3], [5,3]]
        make_move(state, move)
        assert state["board"][6][3][1] is None
        assert state["board"][5][3][1] is not None

class Test_unmake_move():
    def test_unmake_move():
        state = initial_state()
        original = deepcopy(state)
        move = [[6,3], [5,3]]
        piece, captured, old_color, old_current = make_move(state, move)
        unmake_move(state, move, piece, captured, old_color, old_current)
        assert state == original

class Test_victory_conditions():
    def test_victory_conditions_dark():
        board = empty_board()
        board[0][0][1] = ("red", "dark")
        state = {
            "board": board,
            "current": 0,
            "color": None
        }
        assert victory_conditions(state)
    
    def test_victory_conditions_light():
        board = empty_board()
        board[7][0][1] = ("blue", "light")
        state = {
            "board": board,
            "current": 0,
            "color": None
        }
        assert victory_conditions(state)
    
    def test_no_victory_conditions():
        assert not victory_conditions(initial_state())

class Test_evaluate():
    def test_evaluate_return():
        score = evaluate(initial_state())
        assert isinstance(score, int)
    
    def test_evaluate_win_score():
        board = empty_board()
        board[0][0][1] = ("red", "dark")
        state = {
            "board": board,
            "current": 0,
            "color": None
        }
        score = evaluate(state)
        assert abs(score) >= 100000

class Test_negamax():
    def test_negamax_return():
        state = initial_state()
        value, move = negamax(state, depth=2)
        assert move is not None
        assert len(move) == 2
        assert isinstance(move, list)
    
    def test_negamax_terminal_position():
        board = empty_board()
        board[0][0][1] = ("red", "dark")
        state = {
            "board": board,
            "current": 0,
            "color": None
        }
        value, move = negamax(state, depth=2)
        assert move is None


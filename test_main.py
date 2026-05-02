import pytest
from stratégie import legal_move, make_move, unmake_move, evaluate, victory_conditions, negamax

class Test_legal_move:

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]


    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }

    def test_dark_piece_moves(self):
        state = self.make_empty_state(0)
        state["board"][3][3][1] = ("red", "dark")

        moves = legal_move(state)

        assert [[3, 3], [2, 3]] in moves
        assert [[3, 3], [1, 3]] in moves
        assert [[3, 3], [0, 3]] in moves
        assert [[3, 3], [2, 2]] in moves
        assert [[3, 3], [2, 4]] in moves


    def test_light_piece_moves(self):
        state = self.make_empty_state(1)
        state["board"][4][4][1] = ("red", "light")

        moves = legal_move(state)

        assert [[4, 4], [5, 4]] in moves
        assert [[4, 4], [6, 4]] in moves
        assert [[4, 4], [7, 4]] in moves
        assert [[4, 4], [5, 5]] in moves
        assert [[4, 4], [5, 3]] in moves

    def test_piece_bloquee(self):
        state = self.make_empty_state(0)
        state["board"][3][3][1] = ("red", "dark")
        state["board"][2][2][1] = ("red", "light")
        state["board"][2][3][1] = ("blue", "light")
        state["board"][2][4][1] = ("purple", "light")
        
        moves = legal_move(state)
        assert [[3, 3], [3, 3]] in moves

    def test_obstacle_cut(self):
        state = self.make_empty_state(0)
        state["board"][5][3][1] = ("red", "dark")
        state["board"][3][3][1] = ("blue", "light")
        moves = legal_move(state)
        assert [[5, 3], [4, 3]] in moves
        assert [[5, 3], [3, 3]] not in moves
        assert [[5, 3], [2, 3]] not in moves

    def test_stay_in_board(self):
        state = self.make_empty_state(0)
        state["board"][1][0][1] = ("red", "dark") 
        moves = legal_move(state)
        assert [[1, 0], [0, 0]] in moves
        assert [[1, 0], [0, -1]] not in moves

    def test_forced_color(self):
        state = self.make_empty_state(0,"red")
        state["board"][3][3][1] = ("red", "dark") 
        state["board"][5][5][1] = ("blue", "dark")
        moves = legal_move(state)
        sources = [mov[0] for mov in moves]
        assert [3, 3] in sources
        assert [5, 5] not in sources

    def test_opponent_ignored(self):
        state = self.make_empty_state(0)
        state["board"][3][3][1] = ("red", "dark") 
        state["board"][5][5][1] = ("blue", "light")
        moves = legal_move(state)
        sources = [mov[0] for mov in moves]
        assert [3, 3] in sources
        assert [5, 5] not in sources

class Test_make_move:

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]


    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }

    def test_change_state(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        make_move(state, [[4, 4], [2, 4]])
        assert state["board"][2][4][1] == ("red", "dark")
        assert state["board"][4][4][1] is None

    def test_change_current(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        make_move(state, [[4, 4], [2, 4]])
        assert state["current"] == 1

    def test_change_color(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        destination_tile_color = state["board"][2][4][0]
        make_move(state, [[4, 4], [2, 4]])
        assert state["color"] == destination_tile_color

class Test_unmake_move:
        

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]

    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }
    
    def test_tile_come_back(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        piece, captured, old_color, old_current = make_move(state, [[4, 4], [2, 4]])
        unmake_move(state, [[4, 4], [2, 4]], piece, captured, old_color, old_current)
        assert state["board"][4][4][1] == ("red", "dark")

    def test_destination_none(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        piece, captured, old_color, old_current = make_move(state, [[4, 4], [2, 4]])
        unmake_move(state, [[4, 4], [2, 4]], piece, captured, old_color, old_current)
        assert state["board"][2][4][1] is None

    def test_current(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        piece, captured, old_color, old_current = make_move(state, [[4, 4], [2, 4]])
        unmake_move(state, [[4, 4], [2, 4]], piece, captured, old_color, old_current)
        assert state["current"] == 0

    def test_color_(self):
        state = self.make_empty_state(current=0, forced_color="pink")
        state["board"][4][4][1] = ("red", "dark")
        piece, captured, old_color, old_current = make_move(state, [[4, 4], [2, 4]])
        unmake_move(state, [[4, 4], [2, 4]], piece, captured, old_color, old_current)
        assert state["color"] == "pink"


    
class Test_victory_conditions:

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]

    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }

    def test_no_tile_no_win(self):
        state = self.make_empty_state()
        state["board"][4][4][1] = ("red", "dark")
        state["board"][3][3][1] = ("blue", "light")
        assert victory_conditions(state) is False

    def test_light_win(self):
        for col in range(8):
            state = self.make_empty_state()
            state["board"][7][col][1] = ("red", "light")
            assert victory_conditions(state) is True
 
    def test_dark_win(self):
        for col in range(8):
            state = self.make_empty_state()
            state["board"][0][col][1] = ("red", "dark")
            assert victory_conditions(state) is True

    def test_dark_no_win(self):
        for col in range(8):
            state = self.make_empty_state()
            state["board"][7][col][1] = ("red", "dark")
            assert victory_conditions(state) is False

 
    def test_light_no_win(self):
        for col in range(8):
            state = self.make_empty_state()
            state["board"][0][col][1] = ("yellow", "light")
            assert victory_conditions(state) is False
 
    def test_victory_make_move(self):
        state = self.make_empty_state(0)
        state["board"][1][3][1] = ("red", "dark")
        make_move(state, [[1, 3], [0, 3]])
        assert victory_conditions(state) is True

class Test_evaluate:

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]

    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }
    #=================VICTOIRE=================#

    def test_light_row_7_light(self):
        state = self.make_empty_state(1)
        state["board"][7][3][1] = ("red", "light")
        score = evaluate(state)
        assert score == 100000
 
    def test_light_row_7_dark(self):
        state = self.make_empty_state(0)
        state["board"][7][3][1] = ("red", "light")
        score = evaluate(state)
        assert score == -100000

    def test_dark_row_0_dark(self):
        state = self.make_empty_state(0)
        state["board"][0][3][1] = ("red", "dark")
        score = evaluate(state)
        assert score == 100000
 
    def test_dark_row_0_light(self):
        state = self.make_empty_state(1)
        state["board"][0][3][1] = ("red", "dark")
        score = evaluate(state)
        assert score == -100000
    
    #=================Mobility=================#
    def test_score_mobility(self):
        state1 = self.make_empty_state(0)
        state1["board"][4][4][1] = ("red", "dark")
 
        state2 = self.make_empty_state(0)
        state2["board"][4][4][1] = ("red", "dark")
        state2["board"][3][4][1] = ("blue", "light")
        state2["board"][3][3][1] = ("pink", "light")
        state2["board"][3][5][1] = ("green", "light")
 
        assert evaluate(state1) > evaluate(state2)

    #=================symetrie=================#
    def test_opposite_current(self):
        state0 = self.make_empty_state(0)
        state0["board"][4][4][1] = ("red", "dark")
 
        state1 = self.make_empty_state(1)
        state1["board"][4][4][1] = ("red", "dark")
 
        score0 = evaluate(state0)
        score1 = evaluate(state1)
        assert score0 == -score1

    #=================Position_bonus=================#
    def test_dark_advanced(self):
        state1 = self.make_empty_state(0)
        state1["board"][1][4][1] = ("red", "dark")
 
        state2 = self.make_empty_state(0)
        state2["board"][6][4][1] = ("red", "dark")
 
        assert evaluate(state1) > evaluate(state2)

    def test_light_advanced(self):
        state1 = self.make_empty_state(1)
        state1["board"][6][4][1] = ("red", "dark")

        state2 = self.make_empty_state(1)
        state2["board"][1][4][1] = ("red", "dark")

        assert evaluate(state1) > evaluate(state2)

    def test_central_col_dark(self):
        state_centre = self.make_empty_state(0)
        state_centre["board"][4][3][1] = ("red", "dark")
        state_bord = self.make_empty_state(0)
        state_bord["board"][4][0][1] = ("red", "dark") 
 
        assert evaluate(state_centre) > evaluate(state_bord)

    def test_central_col_light(self):
        state_centre = self.make_empty_state(1)
        state_centre["board"][4][3][1] = ("red", "light")
        state_bord = self.make_empty_state(1)
        state_bord["board"][4][0][1] = ("red", "light") 
 
        assert evaluate(state_centre) > evaluate(state_bord)

    #=================General consistency=================#
    def test_score_integer(self):
        state = self.make_empty_state(current=0)
        state["board"][4][4][1] = ("red", "dark")
        assert isinstance(evaluate(state), int)

class Test_negamax:

    BOARD = [
        ["orange", "blue", "purple", "pink", "yellow", "red", "green", "brown"],
        ["red", "orange", "pink", "green", "blue", "yellow", "brown", "purple"],
        ["green", "pink", "orange", "red", "purple", "brown", "yellow", "blue"],
        ["pink", "purple", "blue", "orange", "brown", "green", "red", "yellow"],
        ["yellow", "red", "green", "brown", "orange", "blue", "purple", "pink"],
        ["blue", "yellow", "brown", "purple", "red", "orange", "pink", "green"],
        ["purple", "brown", "yellow", "blue", "green", "pink", "orange", "red"],
        ["brown", "green", "red", "yellow", "pink", "purple", "blue", "orange"],
    ]

    def make_empty_state(self, current=0, forced_color=None):
        return {
            "board": [[[color, None] for color in row] for row in self.BOARD],
            "current": current,
            "color": forced_color
        }

    def test_depth_0(self):
        state = self.make_empty_state(0)
        state["board"][4][4][1] = ("red", "dark")
        _, move = negamax(state, depth=0)
        assert move is None

    def test_victory_stop_search(self):
        state = self.make_empty_state(current=0)
        state["board"][0][3][1] = ("red", "dark")
        score, move = negamax(state, depth=3)
        assert score == 100000
        assert move is None

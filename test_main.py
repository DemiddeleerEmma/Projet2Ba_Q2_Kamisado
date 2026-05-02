import pytest
from main import legal_move, make_move, unmake_move, evaluate, victory_conditions, negamax


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
        state = self.make_empty_state(current=0)
        state["board"][3][3][1] = ("red", "dark")

        moves = legal_move(state)

        assert [[3, 3], [2, 3]] in moves
        assert [[3, 3], [1, 3]] in moves
        assert [[3, 3], [0, 3]] in moves
        assert [[3, 3], [2, 2]] in moves
        assert [[3, 3], [2, 4]] in moves


    def test_light_piece_moves(self):
        state = self.make_empty_state(current=1)
        state["board"][4][4][1] = ("red", "light")

        moves = legal_move(state)

        assert [[4, 4], [5, 4]] in moves
        assert [[4, 4], [6, 4]] in moves
        assert [[4, 4], [7, 4]] in moves
        assert [[4, 4], [5, 5]] in moves
        assert [[4, 4], [5, 3]] in moves

    def test_piece_bloquee(self):
        state = self.make_empty_state(current=0)
        state["board"][3][3][1] = ("red", "dark")
        state["board"][2][2][1] = ("red", "light")
        state["board"][2][3][1] = ("blue", "light")
        state["board"][2][4][1] = ("purple", "light")
        
        moves = legal_move(state)
        assert [[3, 3], [3, 3]] in moves

    def test_obstacle_cut(self):
        state = self.make_empty_state(current=0)
        state["board"][5][3][1] = ("red", "dark")
        state["board"][3][3][1] = ("blue", "light")
        moves = legal_move(state)
        assert [[5, 3], [4, 3]] in moves
        assert [[5, 3], [3, 3]] not in moves
        assert [[5, 3], [2, 3]] not in moves

    def test_stay_in_board(self):
        state = self.make_empty_state(current=0)
        state["board"][1][0][1] = ("red", "dark") 
        moves = legal_move(state)
        assert [[1, 0], [0, 0]] in moves
        assert [[1, 0], [0, -1]] not in moves

    def test_forced_color(self):
        state = self.make_empty_state(current=0, forced_color="red")
        state["board"][3][3][1] = ("red", "dark") 
        state["board"][5][5][1] = ("blue", "dark")
        moves = legal_move(state)
        sources = [mov[0] for mov in moves]
        assert [3, 3] in sources
        assert [5, 5] not in sources

    def test_opponent_ignored(self):
        state = self.make_empty_state(current=0)
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
        state = self.make_empty_state(current=0)
        state["board"][4][4][1] = ("red", "dark")
        make_move(state, [[4, 4], [2, 4]])
        assert state["board"][2][4][1] == ("red", "dark")
        assert state["board"][4][4][1] is None

    def test_change_current(self):
        state = self.make_empty_state(current=0)
        state["board"][4][4][1] = ("red", "dark")
        make_move(state, [[4, 4], [2, 4]])
        assert state["current"] == 1

    def test_change_color(self):
        state = self.make_empty_state(current=0)
        state["board"][4][4][1] = ("red", "dark")
        destination_tile_color = state["board"][2][4][0]
        make_move(state, [[4, 4], [2, 4]])
        assert state["color"] == destination_tile_color

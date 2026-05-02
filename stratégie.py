import random
import time as _time
##===========Variables===========

Dark_bonus = [80, 50, 30, 18, 10, 5, 2, 0]
Light_bonus = [0, 2, 5, 10, 18, 30, 50, 80]


##===========Messages marrants===========

messages = [
    "Prépare-toi à perdre !",
    "C est déjà terminé, tu ne le sais juste pas encore.",
    "Je prends juste le contrôle, rien de personnel.",
    "Tu viens vraiment de jouer ça ?",
    "Erreur de calcul détectée… chez toi.",
    "Je vais accélérer la fin de cette partie",

    "Tu ne t y attendais pas, hein ?",
    "Ce coup était déjà prévu depuis longtemps.",
    "Je joue sur le plateau… et dans ta tête",
    "Réfléchis bien à ton prochain regret.",
    "Tu hésites ? Mauvais signe.",
    "Tout est sous contrôle… du mien.",

    "Analyse terminée. Résultat: favorable pour moi.",
    "Probabilité de victoire en hausse",
    "Optimisation en cours… et réussie.",
    "Je ne ressens pas de stress. Toi si ?",
    "Je calcule plus vite que ton intuition.",

    "Coup de maître incoming (ou pas)",
    "J espère que tu as bien réfléchi… moi oui.",
    "Je joue et je juge en même temps ",
    "Ce coup est sponsorisé par la logique.",
    "Je ne fais jamais d erreurs… enfin presque.",
    "Bonne chance pour défendre ça",
    "Oops… trop tard pour réagir."
]

##===========Générer tous les moves legaux===========

def legal_move(state):
    board = state["board"]
    current = state["current"]
    forced_color = state["color"]
    legal_moves = []

    for r in range(8):
        for c in range(8):
            tile = board[r][c][1]
            if tile is None:
                continue

            color, kind = tile

            if kind != ["dark","light"][current]:
                continue

            if forced_color is not None and color != forced_color:
                continue

            if kind == "light":
                directions = [(1,0),(1,1),(1,-1)]
            else:
                directions = [(-1,0),(-1,-1),(-1,1)]
                
            piece_moves = []

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                while 0 <= nr < 8 and 0 <= nc < 8:

                    if board[nr][nc][1] is not None:
                        break

                    piece_moves.append([[r, c], [nr, nc]])

                    nr += dr
                    nc += dc
            if piece_moves:
                legal_moves.extend(piece_moves)

            else:
                legal_moves.append([[r, c], [r, c]])
        
    return legal_moves

##======================Stratégie======================
##===========Make/unmake_moves===========

def make_move(state, move):
    board = state["board"]
    (r1, c1), (r2, c2) = move

    old_color = state["color"]
    old_current = state["current"]

    piece = board[r1][c1][1]
    captured = board[r2][c2][1]

    board[r1][c1][1] = None
    board[r2][c2][1] = piece

    state["current"] = 1 - state["current"]
    state["color"] = board[r2][c2][0]

    return piece, captured, old_color, old_current

def unmake_move(state, move, piece, captured, old_color, old_current):
    board = state["board"]
    (r1, c1), (r2, c2) = move

    board[r1][c1][1] = piece
    board[r2][c2][1] = captured

    state["current"] = old_current
    state["color"] = old_color

    
##===========Evaluate + Negamax===========

def victory_conditions(state):
    board = state["board"]

    for c in range(8):
        tile = board[7][c][1]
        if tile is not None and tile[1] == "light":
            return True

    for c in range(8):
        tile = board[0][c][1]
        if tile is not None and tile[1] == "dark":
            return True

    return False

def evaluate(state):

    board = state["board"]
    current = state["current"]

    for c in range(8):
        tile = board[7][c][1]
        if tile is not None and tile[1] == "light":
            return -100000 if current == 0 else 100000
        
    for c in range(8):
        tile = board[0][c][1]
        if tile is not None and tile[1] == "dark":
            return 100000 if current == 0 else -100000

    score = 0

    for r in range(8):
        for c in range(8):
            cell = board[r][c]
            tile = cell[1]
            if tile is None:
                continue

            _, kind = tile

            if kind == "dark":

                base = Dark_bonus[r]
                if 2 <= c <= 5:
                    base += 15

                free = 0
                for nr in range(r - 1, -1, -1):
                    if board[nr][c][1] is not None:
                        break
                    free += 1
                score += base + free * 2

            else:

                base = Light_bonus[r]
                if 2<= c <= 5:
                    base += 15

                free = 0               
                for nr in range(r + 1, 8):
                    if board[nr][c][1] is not None:
                        break
                    free += 1
                score -= base + free * 2

    dark_moves  = len(legal_move({**state, "current": 0}))
    light_moves = len(legal_move({**state, "current": 1}))

    score += (dark_moves - light_moves) * 2

    return score if current == 0 else -score

def move_score_for_ordering(move, board, kind):
    (r1, c1), (r2, c2) = move
    score = 0
    if kind == "dark":
        score += (r1 - r2) * 10   
    else:
        score += (r2 - r1) * 10   
    if 2 <= c2 <= 5:
        score += 3
    return score

_deadline = None

class _TimeoutException(Exception):
    pass


def negamax(state, depth, alpha=float('-inf'), beta=float('inf')):
    global _deadline

    if _deadline is not None and _time.time() > _deadline:
        raise _TimeoutException()
    
    if depth == 0 or victory_conditions(state):
        return evaluate(state), None

    best_value = -float("inf")
    best_move = None
    
    moves = legal_move(state)

    board = state["board"]
    current_kind = "light" if state["current"] == 1 else "dark"
    moves.sort(key=lambda m: move_score_for_ordering(m, board, current_kind), reverse=True)

    for move in moves:

        piece, captured, old_color, old_current = make_move(state, move)

        value, _ = negamax(state, depth - 1, -beta, -alpha)
        value = -value

        unmake_move(state, move, piece, captured, old_color, old_current)

        if value > best_value:
            best_value = value
            best_move = move

        alpha = max(alpha, best_value)

        if alpha >= beta:
            break

    return best_value, best_move

def negamax_timeout(state, max_depth=9, time_limit=2.8):
    global _deadline
    _deadline = _time.time() + time_limit

    best_move = None
    best_value = -float("inf")

    for depth in range(1, max_depth + 1):
        try:
            value, move = negamax(state,depth)
            if move is not None:
                best_move = move
                best_value = value
                print(f"  depth={depth} score={value} move={move}")

        except _TimeoutException:
                print(f"  Timeout à depth={depth}")
                break
    
    _deadline = None
    return best_value, best_move
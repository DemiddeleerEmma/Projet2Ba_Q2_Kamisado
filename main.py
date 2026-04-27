import socket
import threading
import sys
import struct
import json
import random
from copy import deepcopy

##===========configuration===========
PORT = 8888
NAME = "Les Infernales"
MATRICULES = ["24164","24374"]

##===========Générer tous les moves legaux===========

def legal_move(state):
    board = state["board"]
    current = state["current"]
    forced_color = state["color"]
    legal_moves = []

    if forced_color is None:
        legal_moves.append([[7, 4], [4, 4]])        

    else:

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
                


                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    while 0 <= nr < 8 and 0 <= nc < 8:

                        if board[nr][nc][1] is not None:
                            break

                        legal_moves.append([[r, c], [nr, nc]])

                        nr += dr
                        nc += dc
                
                if legal_moves == []:
                    legal_moves = ([[r, c], [r, c]])

        
    return legal_moves

##===========Stratégie===========

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


def count_moves_fake(state, player):
    fake_state = {
        "board": state["board"],
        "current": player,
        "color": state["color"]
    }
    return len(legal_move(fake_state))

def evaluate(state):
    board = state["board"]

    if victory_conditions(state):
        for c in range(8):
            tile = board[0][c][1]
            if tile is not None and tile[1] == "dark":
                return 100000
        return -100000

    score = 0
    center_cols = {2, 3, 4, 5}

    for r in range(8):
        for c in range(8):
            tile = board[r][c][1]
            if tile is None:
                continue

            _, kind = tile

            if kind == "dark":
                score += (7 - r) * 5
                if c in center_cols:
                    score += 3
            else:
                score -= r * 5
                if c in center_cols:
                    score -= 3

    moves_current = len(legal_move(state))

    moves_opponent = count_moves_fake(state, 1 - state["current"])

    score += (moves_current - moves_opponent) * 2

    return score



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

    state["color"] = old_color
    state["current"] = old_current

def negamax(state, depth, alpha=float('-inf'), beta=float('inf')):

    if depth == 0 or victory_conditions(state):
        return evaluate(state), None

    best_value = -float("inf")
    best_move = None

    for move in legal_move(state):

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
    





##===========Serveur TCP===========
def start_serveur():
    def handle_client(client, adresse):

        print("Connexion reçue")

        with client:
            def recv_exact(client, n):
                data = b""
                while len(data) < n:
                    packet = client.recv(n - len(data))
                    if not packet:
                        return None
                    data += packet
                return data

            raw_length = recv_exact(client, 4)
            if raw_length is None:
                return

            length = struct.unpack('I', raw_length)[0]

            data = recv_exact(client, length)
            if data is None:
                return

            data = data.decode().strip()
            req = json.loads(data)

            if req["request"] == "ping":
                try:
                    res = {"response": "pong"}
                    msg = json.dumps(res).encode()
                    client.sendall(struct.pack('I', len(msg)))
                    client.sendall(msg)
                    print("pong envoyé")
                except Exception as e:
                    print("Connexion fermée après ping:", e)
                    return


            elif req["request"] == "play":
                try:
                    print("demande de jeu")

                    state = req["state"]
                    moves = legal_move(state)

                    if not moves:
                        move = [[0, 0], [0, 0]]
                    else:
                        _, move = negamax(state, depth=3)

                    res = {
                        "response": "move",
                        "move": move
                    }

                    print(move)

                    msg = json.dumps(res).encode()
                    client.sendall(struct.pack('I', len(msg)))
                    client.sendall(msg)

                except Exception as e:
                    print("Erreur play:", e)
                    return

    
    def loop():
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", PORT))
        s.listen()
        
        while True:
            client, adresse = s.accept()
            #threading.Thread(target=handle_client, args=(client, adresse), daemon=True).start()
            handle_client(client, adresse)

    threading.Thread(target=loop, daemon=True).start()
        
####===========Inscrire l'IA au tournoi##===========

def register(host, port):
    s = socket.socket()
    s.connect((host, port))

    message = {
        "request": "subscribe",
        "port": PORT,
        "name": NAME,
        "matricules": MATRICULES
    }
    msg = json.dumps(message).encode()
    s.sendall(struct.pack('I', len(msg)))
    s.sendall(msg)

    raw_length = s.recv(4)

    if len(raw_length) != 4:
        print("Serveur n'a pas répondu")
        return

    length = struct.unpack('I', raw_length)[0]
    response = s.recv(length).decode()
    s.close()

##===========LANCER LE JEU===========
def main():

    if len(sys.argv) < 3:
        print("Usage: python main.py <host> <port>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    


    start_serveur() 
    register(host, port)

    while True:
        try:
            pass
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
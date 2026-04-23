import socket
import threading
import sys
import struct
import json

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
    for r in range(8):
        for c in range(8):
            tile = board[r][c][tile]
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

                while 0 <= nr < 8 and 0 <= nc < 8:
                    # case occupée → stop
                    if board[nr][nc][TILE] is not None:
                        break

                    legal_moves.append([[r, c], [nr, nc]])

                    nr += dr
                    nc += dc

    return legal_moves

#si pas de move possible, rester sur place


##===========Serveur TCP===========
#Repondre aux requêtes PING et PLAY
def start_serveur():
    def handle_client(client,adresse):
        with client:
            raw_length = client.recv(4)
            length = struct.unpack('I', raw_length)[0]
            data = client.recv(length).decode().strip()

            if not data:
                return
            
            req = json.loads(data)

            if req["request"] == "ping":
                res = {"response": "pong"}
                msg = json.dumps(res).encode()
                client.sendall(struct.pack('I', len(msg)))
                client.sendall(msg)

            elif req["request"] == "play":
               ##REPONSE SELON NOS FONCTIONS
               pass
    
    def loop():
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", PORT))
        s.listen()
        
        while True:
            client, adresse = s.accept()
            threading.Thread(target=handle_client, args=(client, adresse), daemon=True).start()

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
    length = struct.unpack('I', raw_length)[0]
    response = s.recv(length).decode()
    s.close()

##===========LANCER LE JEU===========
def main():

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
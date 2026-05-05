import socket
import threading
import struct
import json
import random

from stratégie import legal_move, negamax_timeout, messages

##===========Serveur TCP===========
def recv_exact(conn, n):
    data = b""
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def start_serveur(port):

    def handle_client(client, adresse):

        print("Connexion reçue")
        client.settimeout(10)

        try:

           with client:

                raw_length = recv_exact(client, 4)
                if raw_length is None:
                    return

                length = struct.unpack('I', raw_length)[0]

                data = recv_exact(client, length)
                if data is None:
                    return

                data = data.decode().strip()
                req = json.loads(data)

            #############################

                if req["request"] == "ping":

                    res = {"response": "pong"}
                    msg = json.dumps(res).encode()
                    client.sendall(struct.pack('I', len(msg)))
                    client.sendall(msg)
                    print("pong envoyé")


                elif req["request"] == "play":
                    print("demande de jeu")
                    state = req["state"]
                    moves = legal_move(state)

                    if not moves:
                        move = [[0, 0], [0, 0]]
                    else:
                        _, move = negamax_timeout(state, 25 , 2.9 )
                    message = random.choice(messages)

                    print(move)

                    res = {
                        "response": "move",
                        "move": move,
                        "message": message
                    }

                    msg = json.dumps(res).encode()
                    client.sendall(struct.pack('I', len(msg)))
                    client.sendall(msg)
                  
        except Exception as e:
                
            print("Connexion fermée après ping:", e)
        except Exception as e:
                print("Erreur play:", e)

    
    def loop():
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen()
        
        while True:
            client, adresse = s.accept()
            threading.Thread(target=handle_client, args=(client, adresse), daemon=True).start()
            #handle_client(client, adresse)

    threading.Thread(target=loop, daemon=True).start()
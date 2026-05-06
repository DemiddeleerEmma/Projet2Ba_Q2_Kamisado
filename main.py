import socket
import struct
import json
import sys
import time
from serveur import start_serveur, recv_exact

##===========configuration===========

PORT = 8888
NAME = "Les Infernales"
MATRICULES = ["24164","24374"]

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
    s.sendall(struct.pack('I', len(msg)) + msg)
    raw_length = recv_exact(s, 4)

    if raw_length is None:
        print("Pas de réponse du serveur")
        s.close()
        return

    if len(raw_length) != 4:
        print("Serveur n'a pas répondu")
        return
    
    length = struct.unpack('I', raw_length)[0]

    response_data = recv_exact(s, length)

    if response_data is None:
        print("Réponse incomplète")
        s.close()
        return

    response = response_data.decode()
    s.shutdown(socket.SHUT_RDWR)
    s.close()

##===========LANCER LE JEU===========

def main():

    if len(sys.argv) < 3:
        print("Usage: python main.py <host> <port>")
        return
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    start_serveur(PORT) 
    register(host, port)

    while True:

        try:
            time.sleep(1)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
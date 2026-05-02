import socket
import struct
import json
import sys
import time

from serveur import start_serveur

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
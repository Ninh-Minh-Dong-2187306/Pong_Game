import socket
import pickle
from _thread import start_new_thread
from src.player import Player

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("waiting for connection...")

players = [
    Player(0, 200, 20, 100, (0, 255, 0)),
    Player(680, 200, 20, 100, (0, 0, 255))
]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            if not data:
                print("disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("recieved:", data)
                print("sending:", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("connected to", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

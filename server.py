import socket
import pickle
import src.game as g
from _thread import start_new_thread
from src.player import Player
from src.ball import Ball

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
ball = Ball(350 - 7, 250 - 7, 7)


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[player] = data
            if not data:
                print("disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                ball.move()
                g.handle_collision(ball, players[0], players[1])
                # print("recieved:", data)
                # print("sending:", reply)

            # conn.sendall(pickle.dumps((reply, (ball.x, ball.y))))
            conn.sendall(pickle.dumps((reply, ball)))
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

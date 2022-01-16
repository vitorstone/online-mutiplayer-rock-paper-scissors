import socket
import _thread
import pickle
import typing
from game import Game

server = socket.gethostbyname(socket.gethostname())
port: int = 5555

print(f"Server's ip: {server}, Server's port: {port}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection... Server Started!")

connected = set()
games: typing.Dict[int, Game] = {}
idCount = 0


def threaded_client(conn: socket.socket, p: int, gameId: int):
    global idCount
    conn.send(str.encode(str(p)))

    while True:

        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game: Game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))

            else:
                break

        except:
            break

    print("Lost Connection.")

    try:
        del games[gameId]
        print("Closing Game ", gameId)
    except:
        pass

    idCount -= 1
    conn.close()


while True:

    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print(f"Creating new game with ID: {gameId}")
    else:
        games[gameId].ready = True
        p = 1

    _thread.start_new_thread(threaded_client, (conn, p, gameId))

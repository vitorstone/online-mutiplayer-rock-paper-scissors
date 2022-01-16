import socket
import pickle
import typing
from game import Game


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server: str = "XXX.X.X.X"
        self.port: int = 5555
        self.addr: typing.Tuple[str, int] = (self.server, self.port)
        self.playerNumber: str = self.connect()

    def getPlayerNumber(self) -> int:
        return int(self.playerNumber)

    def connect(self) -> str:
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("Could not connect to game.")

    def send(self, data: str) -> Game:
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))

        except socket.error as e:
            print(e)

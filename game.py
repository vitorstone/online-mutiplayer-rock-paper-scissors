import typing


class Game:
    def __init__(self, id):
        self.p1Went: bool = False
        self.p2Went: bool = False
        self.ready: bool = False
        self.id = id
        self.moves: typing.Tuple[typing.Optional[str], typing.Optional[str]] = [
            None,
            None,
        ]
        self.wins: typing.Tuple[int, int] = [0, 0]
        self.ties: int = 0

    def get_player_move(self, p) -> typing.Optional[str]:
        return self.moves[p]

    def play(self, player: int, move: str) -> None:

        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def isConnected(self) -> bool:
        return self.ready

    def bothWent(self) -> bool:
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1

        if p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self) -> None:
        self.p1Went = False
        self.p2Went = False

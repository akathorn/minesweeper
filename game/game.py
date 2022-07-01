import random
import itertools
from pprint import pprint
import re

class Game:
    def __init__(self, rows: int = 16, cols: int = 16, n_mines: int = 40) -> None:
        self.rows = rows
        self.cols = cols
        self._coordinates = list(itertools.product(range(rows), range(cols)))

        self.mines: list[list[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
        for r, c in random.sample(self._coordinates, n_mines):
            self.mines[r][c] = 1

        self.board: list[list[str]] = [["#" for _ in range(cols)] for _ in range(rows)]

        self.numbers = [
            [len(self.adjacent_mines((r, c))) for c in range(cols)] for r in range(rows)
        ]
    
    
    def reveal_all(self):
        for pos in self._coordinates:
            self.reveal(pos)

    def reveal(self, pos: tuple[int, int]) -> bool:
        r, c = pos
        if self.mines[r][c]:
            self.board[r][c] = "X"
            return False

        n = self.numbers[r][c]
        if n:
            self.board[r][c] = str(n)
        else:
            self.board[r][c] = " "
            for r1, c1 in self.neighbours(pos):
                if self.board[r1][c1] != " ":
                    self.reveal((r1, c1))
        return True


    def adjacent_mines(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for r, c in self.neighbours(pos):
            if (r, c) != pos and self.mines[r][c]:
                result.append((r, c))
        return result

    def neighbours(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = pos
        result: list[tuple[int, int]] = []
        for i in -1, 0, 1:
            for j in -1, 0, 1:
                x1 = x + i
                y1 = y + j
                if 0 <= x1 < self.rows and 0 <= y1 < self.cols:
                    result.append((x1, y1))

        return result
        
    def pprint(self):
        for row in self.board:
            for c in row:
                print(c, end="")
            print()


if __name__ == "__main__":
    game = Game(5, 5, 3)
    # game.reveal_all()
    game.pprint()

    while True:
        pos = tuple(map(int, input("> ").split()))
        res = game.reveal(pos)
        if not res:
            print("Boom!")
        game.pprint()
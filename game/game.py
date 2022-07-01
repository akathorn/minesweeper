import random
import itertools

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
            [len(self.adjacent_mines(r, c)) for c in range(cols)] for r in range(rows)
        ]
    
    
    def reveal_all(self):
        for r, c in self._coordinates:
            self.reveal(r, c)

    def reveal(self, r: int, c: int) -> bool:
        if self.mines[r][c]:
            self.board[r][c] = "X"
            return False

        n = self.numbers[r][c]
        if n:
            self.board[r][c] = str(n)
        else:
            self.board[r][c] = " "
            for r1, c1 in self.neighbours(r, c):
                if self.board[r1][c1] != " ":
                    self.reveal(r1, c1)
        return True


    def adjacent_mines(self, r: int, c: int) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for r1, c1 in self.neighbours(r, c):
            if (r1, c1) != (r, c) and self.mines[r1][c1]:
                result.append((r1, c1))
        return result

    def neighbours(self, r: int, c: int) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for i in -1, 0, 1:
            for j in -1, 0, 1:
                r1 = r + i
                c1 = c + j
                if 0 <= r1 < self.rows and 0 <= c1 < self.cols:
                    result.append((r1, c1))

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
        r, c = tuple(map(int, input("> ").split()))
        res = game.reveal(r, c)
        if not res:
            print("Boom!")
        game.pprint()
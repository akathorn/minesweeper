import random
import itertools
from typing import NamedTuple
import numpy as np

Position = tuple[int, int]


class Game:
    def __init__(
        self,
        rows: int = 16,
        cols: int = 16,
        n_mines: int = 40,
        mines: list[list[int]] | None = None,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self._coordinates = list(itertools.product(range(rows), range(cols)))

        self.n_mines = n_mines
        self.mines: list[list[int]] = mines or [
            [0 for _ in range(cols)] for _ in range(rows)
        ]
        if not mines:
            for r, c in random.sample(self._coordinates, n_mines):
                self.mines[r][c] = 1

        self.board: list[list[str]] = [["#" for _ in range(cols)] for _ in range(rows)]

        self.numbers = [
            [len(self.adjacent_mines(r, c)) for c in range(cols)] for r in range(rows)
        ]

        self.won = False
        self.lost = False
        self.n_revealed = 0

    def reveal_all(self):
        for r, c in self._coordinates:
            self.reveal(r, c)

    def reveal(self, r: int, c: int) -> bool:
        if self.mines[r][c]:
            self.board[r][c] = "X"
            self.lost = True
            return False

        if not self.is_revealed(r, c):
            self.n_revealed += 1

        if self.rows * self.cols - self.n_mines == self.n_revealed:
            self.won = True

        n = self.numbers[r][c]
        if n:
            self.board[r][c] = str(n)
        else:
            self.board[r][c] = " "
            for r1, c1 in self.neighbours(r, c):
                if not self.is_revealed(r1, c1):
                    self.reveal(r1, c1)
        return True

    def is_revealed(self, r: int, c: int) -> bool:
        return self.board[r][c] not in {"#", "?", "!"}

    def adjacent_mines(self, r: int, c: int) -> list[Position]:
        result: list[Position] = []
        for r1, c1 in self.neighbours(r, c):
            if (r1, c1) != (r, c) and self.mines[r1][c1]:
                result.append((r1, c1))
        return result

    def neighbours(self, r: int, c: int) -> list[Position]:
        result: list[Position] = []
        for i in -1, 0, 1:
            for j in -1, 0, 1:
                r1 = r + i
                c1 = c + j
                if 0 <= r1 < self.rows and 0 <= c1 < self.cols:
                    result.append((r1, c1))

        return result

    def mark(self, r: int, c: int):
        switch = {"#": "!", "!": "?", "?": "#"}
        t = self.board[r][c]
        if t in switch:
            self.board[r][c] = switch[t]

    def pprint(self, print_=True):
        r = ""
        for row in self.board:
            for c in row:
                r += c
            r += "\n"
        if print_:
            print(r)
        return r


class Solver:
    def __init__(self, game: Game) -> None:
        self.game = game

    def solve_all(self) -> bool:
        while not self.game.won:
            if not self.solve_step():
                return False
        return True

    def solve_step(self) -> bool:
        move = self.next_move()
        if not move:
            print("Can't do anything")
            return False

        r, c = move
        assert self.game.board[r][c] in {"#", "?", "!"}
        self.game.reveal(r, c)
        return True

    def next_move(self) -> Position | None:
        vars, eqs = self._generate_equations()

        vars_list = list(vars)

        variables = np.zeros(len(vars_list) + 1, dtype=np.int32)
        equations = np.zeros((len(eqs), 8), dtype=np.int32)
        total_sum = np.zeros(len(eqs), dtype=np.int32)

        for i, eq in enumerate(eqs):
            positions, total_sum[i] = eq
            for j, pos in enumerate(positions):
                equations[i, j] = vars_list.index(pos) + 1

        result = self._solve_rec(variables, equations, total_sum)

        assert len(result) == 1

        for index, value in enumerate(result[0][1:]):
            if value == 0:
                return vars_list[index]

        return None

    def _solve_rec(self, variables, equations, total_sum, i=0):
        if i == len(variables):
            if (variables[equations].sum(axis=1) == total_sum).all():
                return [variables.copy()]
            else:
                return []

        result = self._solve_rec(variables, equations, total_sum, i + 1)

        variables[i] = 1
        if (variables[equations].sum(axis=1) <= total_sum).all():
            result.extend(self._solve_rec(variables, equations, total_sum, i + 1))
        variables[i] = 0

        return result

    def _generate_equations(self):
        variables = set[Position]()
        equations = list[tuple[list[Position], int]]()
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                tile = self.game.board[r][c]
                if not tile.isdigit():
                    continue
                equation = ([], int(tile))
                for n in self.game.neighbours(r, c):
                    if not self.game.is_revealed(*n):
                        variables.add(n)
                        equation[0].append(n)
                equations.append(equation)

        return variables, equations


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

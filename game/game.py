import random
import itertools
from typing import NamedTuple


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


Equation = NamedTuple(
    "Equation",
    [
        ("variables", tuple[Position, ...]),
        ("sum", int),
    ],
)


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
        variables, equations = self._generate_equations()

        results = self._solve_rec({}, [], set(equations))

        assert len(results) == 1

        for pos, val in results[0].items():
            if not val:
                return pos

        return None

    def _solve_rec(
        self,
        assignment: dict[Position, int],
        next_equations: list[Equation],
        unsatisfied_equations: set[Equation],
    ) -> list[dict[Position, int]]:
        if next_equations:
            eq = next_equations[0]
        elif unsatisfied_equations:
            eq = unsatisfied_equations.pop()
            unsatisfied_equations.add(eq)
        else:
            # Base case
            return [assignment.copy()]

        unassigned = set(eq.variables) - assignment.keys()
        assigned = set(eq.variables) & assignment.keys()

        diff = eq.sum - sum(assignment[var] for var in assigned)
        if not (0 <= diff <= len(unassigned)):
            # Invalid assignment
            return []

        results = []
        for variables in itertools.combinations(unassigned, diff):
            # Make an assignment
            for var in unassigned:
                assignment[var] = 1 if var in variables else 0

            # Add neighboring equations to queue
            neighbors = [
                e
                for e in (unsatisfied_equations - set(next_equations))
                if set(variables) & set(e.variables) and e != eq
            ]

            assert not set(next_equations) - unsatisfied_equations

            unsatisfied_equations.remove(eq)
            results.extend(
                self._solve_rec(
                    assignment,
                    next_equations[1:] + neighbors,
                    unsatisfied_equations,
                )
            )
            unsatisfied_equations.add(eq)

            for var in unassigned:
                del assignment[var]

        return results

    def _generate_equations(self) -> tuple[set[Position], list[Equation]]:
        variables = set[Position]()
        equations = list[Equation]()
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                tile = self.game.board[r][c]
                if not tile.isdigit():
                    continue

                vars_ = []
                for n in self.game.neighbours(r, c):
                    if not self.game.is_revealed(*n):
                        variables.add(n)
                        vars_.append(n)
                equations.append(Equation(tuple(vars_), int(tile)))

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

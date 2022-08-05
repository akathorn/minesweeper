import random
import itertools
import logging

from typing import Any, Callable, NamedTuple, Sequence


logging.basicConfig(
    format="game.py [%(levelname)s]: %(message)s", level=logging.WARNING
)


Position = tuple[int, int]


class Board:
    def __init__(
        self,
        rows: int = 16,
        cols: int = 16,
        n_mines: int = 40,
        mines: list[list[int]] | None = None,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.coordinates = list(itertools.product(range(rows), range(cols)))

        self.n_mines = n_mines
        self.mines: list[list[int]] = mines or [
            [0 for _ in range(cols)] for _ in range(rows)
        ]
        if not mines:
            for r, c in random.sample(self.coordinates, n_mines):
                self.mines[r][c] = 1

        self.tiles: list[list[str]] = [["#" for _ in range(cols)] for _ in range(rows)]

        self.numbers = [
            [len(self._adjacent_mines(r, c)) for c in range(cols)] for r in range(rows)
        ]

    def is_revealed(self, r: int, c: int) -> bool:
        return self.tiles[r][c] not in {"#", "?", "!", "O"}

    def _adjacent_mines(self, r: int, c: int) -> list[Position]:
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

    def pprint(self, print_=True):
        r = ""
        for row in self.tiles:
            for c in row:
                r += c
            r += "\n"
        if print_:
            print(r)
        return r


class Equation:
    def __init__(self, variables: Sequence[Position], total: int) -> None:
        self.variables = set(variables)
        self.total = total

    def __hash__(self) -> int:
        vars_ = list(self.variables)
        vars_.sort()
        return hash(tuple(vars_) + (self.total,))

    def __eq__(self, other) -> int:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return f"Equation[{self.variables} = {self.total}]"


# TODO: take into account the total number of mines
class Solver:
    def __init__(self, board: Board) -> None:
        self.board = board

        self.ambiguous = set[Position]()
        self.unreachable = set[Position](
            itertools.product(range(board.rows), range(board.cols))
        )

        self.assignment = dict[Position, int]()
        self.equations = list[Equation]()

    @property
    def safe(self):
        safe = set[Position]()
        for pos, val in self.assignment.items():
            if not val and not self.board.is_revealed(*pos):
                safe.add(pos)
        return safe

    @property
    def mines(self):
        mines = set[Position]()
        for pos, val in self.assignment.items():
            if val and not self.board.is_revealed(*pos):
                mines.add(pos)
        return mines

    def next_move(self) -> Position | None:
        self.update_assignments()

        for pos, val in self.assignment.items():
            if val == 0 and not self.board.is_revealed(*pos):
                return pos

        # We couldn't find a safe tile to reveal
        return None

    def reveal(self, pos: Position):
        r, c = pos
        self._assign_variable(pos, self.board.mines[r][c])

        # Update the set
        self.unreachable -= {pos}

        # Add a new equation
        tile = self.board.tiles[r][c]
        if tile.isdigit():
            total = int(tile)
            vars_ = []
            for neigh in self.board.neighbours(*pos):
                self.unreachable -= {neigh}
                if neigh in self.assignment:
                    total -= self.assignment[neigh]
                else:
                    vars_.append(neigh)
            if vars_:
                self.equations.append(Equation(vars_, total))

    def _assign_variable(self, pos: Position, value: int):
        self.assignment[pos] = value

        # Update the existing equations
        for equation in self.equations:
            if pos in equation.variables:
                equation.total -= self.assignment[pos]
                equation.variables.remove(pos)
                if not equation.variables:
                    self.equations.remove(equation)

    def update_assignments(self):
        guesses = self._find_assignments_rec({}, [], set(self.equations))
        # logging.debug(f"Equations: {equations}")
        variables = set(guesses[0].keys()) - set(self.assignment.keys())

        self.ambiguous = set()
        for var in variables:
            values = {guess[var] for guess in guesses}
            if len(values) > 1:
                self.ambiguous.add(var)
            else:
                self._assign_variable(var, 1 if all(values) else 0)

    def _find_assignments_rec(
        self,
        guess: dict[Position, int],
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
            return [guess.copy()]

        # assert not set(next_equations) - unsatisfied_equations

        unassigned = set(eq.variables) - guess.keys()
        assigned = set(eq.variables) & guess.keys()

        diff = eq.total - sum(guess[var] for var in assigned)
        if not (0 <= diff <= len(unassigned)):
            # Invalid assignment
            return []

        results = []
        for variables in itertools.combinations(unassigned, diff):
            # Make an assignment
            for var in unassigned:
                guess[var] = 1 if var in variables else 0

            # Add neighboring equations to queue
            neighbors = [
                e
                for e in (unsatisfied_equations - set(next_equations))
                if set(variables) & set(e.variables) and e != eq
            ]

            unsatisfied_equations.remove(eq)
            results.extend(
                self._find_assignments_rec(
                    guess,
                    next_equations[1:] + neighbors,
                    unsatisfied_equations,
                )
            )
            unsatisfied_equations.add(eq)

            for var in unassigned:
                del guess[var]

        return results


class Game:
    def __init__(
        self,
        rows: int = 16,
        cols: int = 16,
        n_mines: int = 40,
        guarantee_move: bool = False,
        mines: list[list[int]] | None = None,
        end_callback: Callable[[bool], Any] | None = None,
        seed: float = -1,
    ) -> None:
        self.seed = seed if seed >= 0 else random.randint(0, 10000000000)
        random.seed(self.seed)

        self.board = Board(rows, cols, n_mines, mines)
        self.solver = Solver(self.board)

        self.won = False
        self.lost = False
        self.n_revealed = 0
        self.end_callback = end_callback

        self.guarantee_move = guarantee_move
        if guarantee_move:
            self.ensure_move()

    def reveal_all(self):
        for r, c in self.board.coordinates:
            self.reveal(r, c)

    def reveal(
        self, r: int, c: int, update_solver: bool = True, ensure_move: bool = True
    ) -> bool:
        if self.board.mines[r][c]:
            if self.end_callback and not (self.lost or self.won):
                self.end_callback(False)
            self.lost = True
            self.board.tiles[r][c] = "X"
            self.solver.reveal((r, c))
            return False

        if not self.board.is_revealed(r, c):
            self.n_revealed += 1

        if self.board.rows * self.board.cols - self.board.n_mines == self.n_revealed:
            if self.end_callback and not (self.lost or self.won):
                self.end_callback(True)
            self.won = True

        n = self.board.numbers[r][c]
        if n:
            self.board.tiles[r][c] = str(n)
        else:
            self.board.tiles[r][c] = " "
            for r1, c1 in self.board.neighbours(r, c):
                if not self.board.is_revealed(r1, c1):
                    self.reveal(r1, c1, update_solver=False, ensure_move=False)

        self.solver.reveal((r, c))
        if self.guarantee_move and ensure_move:
            self.ensure_move()
        return True

    def mark(self, r: int, c: int):
        switch = {"#": "!", "!": "?", "?": "#"}
        t = self.board.tiles[r][c]
        if t in switch:
            self.board.tiles[r][c] = switch[t]

    def ensure_move(self):
        logging.debug("Ensuring move")
        if self.won or self.lost or self.solver.next_move():
            return

        logging.debug("Looking for an ambiguous tile")
        for r, c in self.solver.ambiguous:
            if not self.board.mines[r][c]:
                logging.debug(f"Revealing {r, c}")
                self.reveal(r, c)
                return

        logging.debug("Looking for an unreachable tile")
        unreachable = list(self.solver.unreachable)
        random.shuffle(unreachable)
        for r, c in unreachable:
            if not self.board.mines[r][c]:
                logging.debug(f"Revealing {r, c}")
                self.reveal(r, c)
                return

        raise Exception("Couldn't ensure move!")

    def solve_all(self) -> bool:
        while not self.won:
            if not self.solve_step():
                return False
        return True

    def solve_step(self) -> Position | None:
        move = self.solver.next_move()
        if not move:
            print("Can't do anything")
        else:
            assert not self.board.is_revealed(*move)
            self.reveal(*move)
        return move

    def hint(self):
        if any("O" in row for row in self.board.tiles):
            return

        tile = self.solver.next_move()
        if tile:
            r, c = tile
            self.board.tiles[r][c] = "O"


if __name__ == "__main__":
    game = Game(5, 5, 3, guarantee_move=True)
    # game.reveal_all()
    print(game.solver.safe)
    game.board.pprint()

    while True:
        r, c = tuple(map(int, input("> ").split()))
        res = game.reveal(r, c)
        if not res:
            print("Boom!")
        print(game.solver.safe)
        game.board.pprint()

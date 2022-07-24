from textwrap import dedent
from game import Game

from pytest_mock import mocker, MockerFixture

from game.game import Solver  # type: ignore


def game_from_mines(mines_ascii: str):
    lines = dedent(mines_ascii.strip()).split()
    rows = len(lines)
    cols = len(lines[0])
    n_mines = mines_ascii.count("X")
    mines = [[1 if c == "X" else 0 for c in line] for line in lines]

    return Game(rows, cols, n_mines, mines)


def reveal_from_ascii(game: Game, tiles: str):
    ascii = dedent(tiles.strip())
    for i, line in enumerate(ascii.split()):
        for j, c in enumerate(line):
            if c == "?":
                game.reveal(i, j)


def create_and_reveal(board_ascii: str):
    game = game_from_mines(board_ascii)
    reveal_from_ascii(game, board_ascii)
    return game


def assert_board(game: Game, board_ascii: str):
    ascii = dedent(board_ascii).strip().replace("-", " ") + "\n"
    assert game.pprint(print_=False) == ascii


def test_1(mocker: MockerFixture):
    game = Game(rows=3, cols=4, n_mines=3)

    assert sum(sum(col) for col in game.mines) == 3
    assert not game.won and not game.lost


def test_lose():
    game = game_from_mines(
        """
    ---
    -X-
    ---
    """
    )

    assert not game.lost
    game.reveal(1, 1)
    assert game.lost and not game.won


def test_win():
    game = game_from_mines(
        """
    -X-
    """
    )

    assert not game.won
    game.reveal(0, 0)
    game.reveal(0, 2)
    assert not game.lost and game.won

    # 2nd
    game = game_from_mines(
        """
    X--
    ---
    ---
    """
    )
    assert_board(
        game,
        """
    ###
    ###
    ###
    """,
    )

    game.reveal(1, 2)

    assert_board(
        game,
        """
    #1-
    11-
    ---
    """,
    )

    assert game.won


def test_solve():
    game = create_and_reveal(
        """
    X-X
    ???
    """
    )

    assert_board(
        game,
        """
    ###
    121
    """,
    )

    solver = Solver(game)
    solver.solve_step()
    assert game.won

    game = create_and_reveal(
        """
    ---
    ?X?
    ???
    """
    )

    solver = Solver(game)
    solver.solve_all()
    assert game.won


def test_two_components():
    game = create_and_reveal(
        """
    -X???X-
    ???????
    """
    )

    solver = Solver(game)
    move = solver.next_move()
    solver.solve_all()
    assert game.won


def test_ambiguous():
    game = create_and_reveal(
        """
    -X
    ??
    """
    )

    solver = Solver(game)
    move = solver.next_move()
    assert move


import copy
import random

SIZE = 9
EMPTY = 0

DIFFICULTY_CLUES = {
    "easy": 45,
    "medium": 35,
    "hard": 25,
}


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)

                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate

                        if fill_board(board):
                            return True

                        board[row][col] = EMPTY

                return False

    return True


def count_solutions(board, limit=2):
    """Count solutions, stopping as soon as ``limit`` is reached."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    return _count_solutions(board, limit)


def _count_solutions(board, limit):
    empty_cell = None
    candidates_for_cell = None

    # Choose the most constrained empty cell to reduce the search tree.
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if value != EMPTY:
                if not 1 <= value <= SIZE:
                    return 0
                continue

            candidates = [
                candidate
                for candidate in range(1, SIZE + 1)
                if is_safe(board, row, col, candidate)
            ]
            if not candidates:
                return 0
            if candidates_for_cell is None or len(candidates) < len(
                candidates_for_cell
            ):
                empty_cell = (row, col)
                candidates_for_cell = candidates

    if empty_cell is None:
        return int(_is_complete_board_valid(board))

    row, col = empty_cell
    count = 0
    for candidate in candidates_for_cell:
        board[row][col] = candidate
        count += _count_solutions(board, limit - count)
        board[row][col] = EMPTY

        if count >= limit:
            return limit

    return count


def _is_complete_board_valid(board):
    """Return whether a completely filled board satisfies Sudoku rules."""
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            board[row][col] = EMPTY
            valid = 1 <= value <= SIZE and is_safe(board, row, col, value)
            board[row][col] = value
            if not valid:
                return False
    return True


def has_unique_solution(board):
    test_board = deep_copy(board)

    return count_solutions(test_board, limit=2) == 1


def remove_cells(board, clues):
    cells = [
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
    ]

    random.shuffle(cells)

    current_clues = SIZE * SIZE

    for row, col in cells:
        if current_clues <= clues:
            break

        original = board[row][col]

        if original == EMPTY:
            continue

        board[row][col] = EMPTY

        if has_unique_solution(board):
            current_clues -= 1
        else:
            board[row][col] = original

    return current_clues


def generate_puzzle(clues=35, difficulty=None):
    """
    Generate a uniquely solvable Sudoku puzzle.

    The function supports either:
    - a specific number of clues
    - a difficulty level: easy, medium, or hard
    """

    if difficulty is not None:
        difficulty = difficulty.lower()

        if difficulty not in DIFFICULTY_CLUES:
            raise ValueError(
                "difficulty must be easy, medium, or hard"
            )

        clues = DIFFICULTY_CLUES[difficulty]

    if clues < 17 or clues > SIZE * SIZE:
        raise ValueError("clues must be between 17 and 81")

    while True:
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)

        if remove_cells(board, clues) == clues:
            return deep_copy(board), solution


def get_locked_cells(puzzle):
    """
    Return the positions of all prefilled cells.

    Each position is returned as a (row, col) tuple.
    """
    locked = set()

    for row in range(SIZE):
        for col in range(SIZE):
            if puzzle[row][col] != EMPTY:
                locked.add((row, col))

    return locked

def is_valid_move(board, row, col, num, solution=None):
    """
    Check whether a move is valid.

    A move is valid when:
    - the number is between 1 and 9
    - the cell is not a locked/prefilled cell
    - the number does not violate Sudoku rules
    - if a solution is provided, the number matches the solution
    """

    if not 1 <= num <= 9:
        return False

    if board[row][col] != EMPTY:
        return False

    if not is_safe(board, row, col, num):
        return False

    if solution is not None and solution[row][col] != num:
        return False

    return True

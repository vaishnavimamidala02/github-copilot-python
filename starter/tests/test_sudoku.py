import pytest

import sudoku_logic


def test_create_empty_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == 9
    assert all(len(row) == 9 for row in board)
    assert all(cell == 0 for row in board for cell in row)


def test_fill_board_creates_valid_complete_board():
    board = sudoku_logic.create_empty_board()

    result = sudoku_logic.fill_board(board)

    assert result is True
    assert all(
        1 <= cell <= 9
        for row in board
        for cell in row
    )


def test_is_safe_rejects_duplicate_in_row():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False


def test_is_safe_rejects_duplicate_in_column():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 1, 0, 5) is False


def test_is_safe_rejects_duplicate_in_box():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 1, 1, 5) is False


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == 9
    assert len(solution) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(len(row) == 9 for row in solution)


def test_solution_is_complete():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert all(
        1 <= cell <= 9
        for row in solution
        for cell in row
    )


def test_puzzle_has_requested_number_of_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    filled_cells = sum(
        cell != sudoku_logic.EMPTY
        for row in puzzle
        for cell in row
    )

    assert filled_cells == 35


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_generated_puzzles_have_unique_solution(difficulty):
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)

    assert sudoku_logic.has_unique_solution(puzzle) is True
    assert sudoku_logic.count_solutions(
        sudoku_logic.deep_copy(puzzle), limit=2
    ) == 1


def test_count_solutions_finds_one_solution_for_generated_puzzle():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    test_board = sudoku_logic.deep_copy(puzzle)

    assert sudoku_logic.count_solutions(test_board, limit=2) == 1


def test_count_solutions_stops_after_two_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board, limit=2) == 2
    assert board == sudoku_logic.create_empty_board()


def test_count_solutions_rejects_invalid_complete_board():
    board = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    assert sudoku_logic.count_solutions(board) == 0


def test_count_solutions_rejects_out_of_range_values():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 10

    assert sudoku_logic.count_solutions(board) == 0


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_generated_solution_is_the_unique_solution(difficulty):
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)

    assert sudoku_logic.count_solutions(
        sudoku_logic.deep_copy(puzzle), limit=2
    ) == 1
    assert all(
        solution[row][col] == puzzle[row][col]
        or puzzle[row][col] == sudoku_logic.EMPTY
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )


def test_easy_difficulty_generates_puzzle():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="easy")

    filled_cells = sum(
        cell != sudoku_logic.EMPTY
        for row in puzzle
        for cell in row
    )

    assert filled_cells == 45


def test_medium_difficulty_generates_puzzle():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="medium")

    filled_cells = sum(
        cell != sudoku_logic.EMPTY
        for row in puzzle
        for cell in row
    )

    assert filled_cells == 35


def test_hard_difficulty_generates_puzzle():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="hard")

    filled_cells = sum(
        cell != sudoku_logic.EMPTY
        for row in puzzle
        for cell in row
    )

    assert filled_cells == 25

def test_get_locked_cells_returns_prefilled_positions():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    locked = sudoku_logic.get_locked_cells(puzzle)

    assert (0, 0) in locked
    assert (0, 1) in locked
    assert (0, 2) not in locked
    assert (8, 8) in locked


def test_locked_cells_match_prefilled_cells():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="medium")

    locked = sudoku_logic.get_locked_cells(puzzle)

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != sudoku_logic.EMPTY:
                assert (row, col) in locked
            else:
                assert (row, col) not in locked


def test_is_valid_move_accepts_correct_solution_value():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="easy")

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == sudoku_logic.EMPTY:
                assert sudoku_logic.is_valid_move(
                    puzzle,
                    row,
                    col,
                    solution[row][col],
                    solution
                ) is True
                return


def test_is_valid_move_rejects_invalid_number():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="easy")

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == sudoku_logic.EMPTY:
                correct = solution[row][col]

                wrong = next(
                    num for num in range(1, 10)
                    if num != correct
                )

                assert sudoku_logic.is_valid_move(
                    puzzle,
                    row,
                    col,
                    wrong,
                    solution
                ) is False
                return


def test_is_valid_move_rejects_prefilled_cell():
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty="easy")

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != sudoku_logic.EMPTY:
                assert sudoku_logic.is_valid_move(
                    puzzle,
                    row,
                    col,
                    puzzle[row][col],
                    solution
                ) is False
                return

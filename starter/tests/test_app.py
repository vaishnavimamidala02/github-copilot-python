import copy

import pytest

import app


@pytest.fixture
def client():
    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None

    with app.app.test_client() as test_client:
        yield test_client

    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None


def test_index_renders_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku Game" in response.data
    assert b"new-game" in response.data
    assert b"check-solution" in response.data


def test_new_game_returns_default_puzzle_and_stores_solution(client):
    response = client.get("/new")

    assert response.status_code == 200
    puzzle = response.get_json()["puzzle"]
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(cell != 0 for row in puzzle for cell in row) == 35
    assert app.CURRENT["puzzle"] == puzzle
    assert app.CURRENT["solution"] is not None


def test_new_game_honors_clues_query_parameter(client):
    response = client.get("/new?clues=40")

    assert response.status_code == 200
    puzzle = response.get_json()["puzzle"]
    assert sum(cell != 0 for row in puzzle for cell in row) == 40


@pytest.mark.parametrize("difficulty, clues", [
    ("easy", 45),
    ("medium", 35),
    ("hard", 25),
])
def test_new_game_honors_difficulty_query_parameter(client, difficulty, clues):
    response = client.get(f"/new?difficulty={difficulty}")

    assert response.status_code == 200
    puzzle = response.get_json()["puzzle"]
    # The legacy generator can retain extra clues when removing one would
    # break uniqueness, but it should never return fewer than requested.
    assert sum(cell != 0 for row in puzzle for cell in row) >= clues


def test_check_requires_game_in_progress(client):
    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}


def test_hint_returns_first_empty_cell_value(client):
    client.get("/new")
    board = copy.deepcopy(app.CURRENT["puzzle"])
    row, col = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if board[row][col] == 0
    )

    response = client.post("/hint", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {
        "row": row,
        "col": col,
        "value": app.CURRENT["solution"][row][col],
    }


def test_check_reports_incorrect_cells(client):
    client.get("/new")
    board = copy.deepcopy(app.CURRENT["solution"])
    board[0][0] = 1 if board[0][0] != 1 else 2

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json()["incorrect"] == [[0, 0]]


def test_check_reports_complete_correct_solution(client):
    client.get("/new")

    response = client.post("/check", json={"board": app.CURRENT["solution"]})

    assert response.status_code == 200
    assert response.get_json() == {"incorrect": []}

// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_KEY = 'sudoku-top-10';
let puzzle = [];
let solution = [];
let difficulty = 'medium';
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerId = null;
let gameCompleted = false;

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainder = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainder}`;
}

function startTimer() {
  window.clearInterval(timerId);
  elapsedSeconds = 0;
  document.getElementById('timer').innerText = formatTime(elapsedSeconds);
  timerId = window.setInterval(() => {
    elapsedSeconds += 1;
    document.getElementById('timer').innerText = formatTime(elapsedSeconds);
  }, 1000);
}

function stopTimer() {
  window.clearInterval(timerId);
  timerId = null;
}

function readLeaderboard() {
  const stored = window.localStorage.getItem(LEADERBOARD_KEY);
  if (!stored) return [];

  let entries;
  try {
    entries = JSON.parse(stored);
  } catch (error) {
    console.error('Unable to read saved Sudoku scores.', error);
    return [];
  }

  if (!Array.isArray(entries)) return [];
  return entries.filter((entry) => (
    entry
    && typeof entry.name === 'string'
    && Number.isFinite(entry.time)
    && typeof entry.difficulty === 'string'
    && Number.isFinite(entry.hints)
  ));
}

function renderLeaderboard() {
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  readLeaderboard().forEach((entry) => {
    const row = document.createElement('tr');
    [entry.name, formatTime(entry.time), entry.difficulty, entry.hints]
      .forEach((value) => {
        const cell = document.createElement('td');
        cell.innerText = value;
        row.appendChild(cell);
      });
    body.appendChild(row);
  });
}

function saveScore() {
  const name = window.prompt('Enter your name for the leaderboard:', 'Player');
  const entry = {
    name: name && name.trim() ? name.trim() : 'Player',
    time: elapsedSeconds,
    difficulty,
    hints: hintsUsed
  };
  const scores = readLeaderboard()
    .concat(entry)
    .sort((first, second) => first.time - second.time)
    .slice(0, 10);
  window.localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(scores));
  renderLeaderboard();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.classList.add(
        `box-${Math.floor(i / 3) * 3 + Math.floor(j / 3)}`
      );
      input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  solution = [];
  renderPuzzle(data.puzzle);
  hintsUsed = 0;
  gameCompleted = false;
  document.getElementById('hint-count').innerText = hintsUsed;
  startTimer();
  const message = document.getElementById('message');
  message.className = '';
  message.innerText = '';
}

async function useHint() {
  const inputs = document.getElementById('sudoku-board')
    .getElementsByTagName('input');
  const board = [];
  for (let index = 0; index < inputs.length; index += 1) {
    const row = Math.floor(index / SIZE);
    const col = index % SIZE;
    if (!board[row]) board[row] = [];
    board[row][col] = inputs[index].value
      ? parseInt(inputs[index].value, 10)
      : 0;
  }

  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) return;
  const index = data.row * SIZE + data.col;
  inputs[index].value = data.value;
  inputs[index].disabled = true;
  inputs[index].classList.add('hinted');
  hintsUsed += 1;
  document.getElementById('hint-count').innerText = hintsUsed;
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.className = 'message-error';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0 && !gameCompleted) {
    gameCompleted = true;
    stopTimer();
    msg.className = 'message-success';
    msg.innerText = 'Congratulations! You solved it!';
    saveScore();
  } else {
    msg.className = 'message-error';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', useHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('difficulty').addEventListener('change', newGame);
  renderLeaderboard();
  // initialize
  newGame();
});
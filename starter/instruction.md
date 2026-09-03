# Project Instructions — Sudoku Flask Application

## 1\. Project Overview

This project is a Flask-based Sudoku web application. The goal is to refactor the existing legacy application into clean, modular, maintainable, and well-tested code while improving the user experience.

The application should allow users to:

* Generate Sudoku puzzles.
* Select Easy, Medium, and Hard difficulty levels.
* Enter numbers into the puzzle.
* Receive immediate feedback for invalid moves.
* Check whether the completed puzzle is correct.
* Request hints.
* Track the solving time.
* Display a congratulatory message when the puzzle is solved.
* Save completed-game scores locally.
* Display the Top 10 scores.
* Switch between light and dark modes.
* Use the application comfortably on desktop and mobile devices.

## 2\. Code Quality

Follow clean coding practices throughout the project.

* Use meaningful variable and function names.
* Keep functions small and focused on one responsibility.
* Avoid unnecessary code duplication.
* Create reusable functions and components when functionality is repeated.
* Use consistent 4-space indentation in Python.
* Add comments where they improve understanding.
* Avoid unnecessary comments that only repeat what the code already says.
* Keep Python, HTML, CSS, and JavaScript organized.
* Use consistent error handling.
* Do not introduce unnecessary dependencies.

## 3\. Python Standards

Use Python best practices.

* Follow PEP 8 style where practical.
* Use descriptive function and variable names.
* Prefer modular functions over large blocks of code.
* Validate inputs where appropriate.
* Handle errors gracefully.
* Avoid global state when possible.
* Keep Sudoku logic separate from Flask route logic.
* Write reusable and testable functions.

## 4\. Flask Standards

Follow Flask best practices.

* Keep route functions focused on handling HTTP requests and responses.
* Separate application logic from presentation logic.
* Use templates for HTML rendering.
* Use static files for CSS and JavaScript.
* Validate data received from the browser.
* Return clear and appropriate responses.
* Avoid placing large amounts of business logic directly inside routes.

## 5\. Sudoku Requirements

The Sudoku game must follow standard Sudoku rules.

* The board must contain a valid Sudoku puzzle.
* Every generated puzzle must have exactly one unique solution.
* Difficulty levels must include Easy, Medium, and Hard.
* Prefilled cells must be locked and cannot be edited by the user.
* User-entered values must be validated.
* Invalid moves should provide clear feedback.
* The Check function should determine whether the completed puzzle is correct.
* The Hint function should provide a valid value for an appropriate empty cell.
* A congratulatory message should appear after successfully completing the puzzle.

## 6\. Timer

The application should provide a visible timer.

* The timer should start when a puzzle begins.
* The timer should continue while the user solves the puzzle.
* The final solving time should be recorded when the puzzle is completed.
* The timer should reset when a new puzzle is started.

## 7\. Top 10 Scores

Completed games should be stored using browser LocalStorage.

Each score should include:

* Player name.
* Solving time.
* Difficulty level.
* Number of hints used.

The application should display the best 10 scores.

## 8\. User Interface

The interface should be clear and easy to use.

* Use readable text and controls.
* Make the Sudoku grid visually clear.
* Clearly distinguish editable cells from prefilled cells.
* Use alternating visual styling for the 3x3 Sudoku blocks.
* Provide clear feedback for invalid and valid actions.
* Provide buttons for important game actions.
* Make the layout responsive on different screen sizes.

## 9\. Dark Mode

Provide both light and dark display modes.

* Text must remain readable in both modes.
* Sudoku cells must remain clearly visible.
* Buttons and controls must remain usable.
* Colors should provide sufficient contrast.

## 10\. Accessibility

Follow accessibility best practices.

* Use meaningful labels for controls.
* Ensure buttons and inputs can be understood by users.
* Maintain readable contrast.
* Provide useful feedback messages.
* Support keyboard interaction where practical.
* Avoid relying only on color to communicate important information.

## 11\. Testing

Use automated tests where appropriate.

Tests should cover important Sudoku functionality, including:

* Sudoku board validity.
* Unique solution generation.
* Difficulty levels.
* User input validation.
* Hint functionality.
* Puzzle checking.
* Important application behavior.

Run the test suite before submitting the project.

## 12\. GitHub Copilot Usage

Use GitHub Copilot as a development assistant, not as a replacement for understanding the code.

When using Copilot:

1. Clearly describe the required functionality.
2. Ask Copilot to explain existing code before making major changes.
3. Review generated code carefully.
4. Test generated code before accepting it.
5. Reject suggestions that do not follow the project requirements.
6. Prefer simple, readable, modular solutions.
7. Avoid accepting unnecessary dependencies or overly complicated implementations.

## 13\. Documentation

Document important parts of the project.

The README should explain:

* Project purpose.
* Main features.
* Technologies used.
* Installation instructions.
* How to run the application.
* How to run tests.
* Sudoku functionality.
* Difficulty levels.
* Hint and Check features.
* Timer.
* Top 10 scores.
* Dark mode.
* How GitHub Copilot was used.

## 14\. Development Workflow

Follow this workflow when making changes:

1. Understand the existing code.
2. Identify the required change.
3. Ask GitHub Copilot for a suitable solution.
4. Review the suggestion.
5. Implement the change.
6. Run tests.
7. Run the Flask application.
8. Test the feature manually.
9. Fix any errors.
10. Update documentation when necessary.

The final project should be clean, functional, maintainable, tested, and easy for another developer to understand.


# Tic-Tac-Toe Game Using Python

## Project Description

This is a simple, console-based Tic-Tac-Toe game developed using Python 3. The game supports two players who take turns placing X and O on a 3×3 board.

The first player to get three marks in a row, column, or diagonal wins. If all cells are filled and neither player wins, the game ends in a draw.

## Requirements

* Python 3.x
* No external libraries required

## How to Run

1. Save the Python source code as `tictactoe.py`.
2. Open a terminal or command prompt in the project folder.
3. Run the following command:

   ```bash
   python tictactoe.py
   ```

## How to Play

1. Player X starts the game.
2. Player O plays after X.
3. Enter a row number between 0 and 2.
4. Enter a column number between 0 and 2.
5. Players cannot select a cell that is already occupied.
6. The game announces the winner when a player completes a row, column, or diagonal.
7. If all nine cells are filled without a winner, the game announces a draw.
8. After each round, enter Y to play again or N to exit.

## Features

* 3×3 game board
* Two-player gameplay
* Automatic turn switching
* Win detection for rows, columns, and diagonals
* Draw detection
* Input validation
* Prevention of moves on occupied cells
* Play-again option

## Concepts Used

* Variables and data types
* Lists
* Functions
* While loops and for loops
* Conditional statements
* User input
* Exception handling

## Project Structure

```text
TicTacToe_Project/
├── tictactoe.py
└── README.md
```

## Author

Python Mini Project Assignment

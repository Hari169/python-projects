def print_board(board):
    print(board[0][0], "|", board[0][1], "|", board[0][2])
    print("---------")
    print(board[1][0], "|", board[1][1], "|", board[1][2])
    print("---------")
    print(board[2][0], "|", board[2][1], "|", board[2][2])


def check_win(board):
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == "X":
            print("X is the winner!")
            return True

        if board[row][0] == board[row][1] == board[row][2] == "O":
            print("O is the winner!")
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == "X":
            print("X is the winner!")
            return True

        if board[0][col] == board[1][col] == board[2][col] == "O":
            print("O is the winner!")
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == "X":
        print("X is the winner!")
        return True

    if board[0][0] == board[1][1] == board[2][2] == "O":
        print("O is the winner!")
        return True

    if board[0][2] == board[1][1] == board[2][0] == "X":
        print("X is the winner!")
        return True

    if board[0][2] == board[1][1] == board[2][0] == "O":
        print("O is the winner!")
        return True

    return False


def check_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False

    return True


# Main game loop
while True:
    # Create a fresh board for each round
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

    print("\nWelcome to Tic-Tac-Toe!")
    print_board(board)

    current_player = "X"

    # Continue until someone wins or the game is a draw
    while True:
        print("\nCurrent player:", current_player)

        # Get and validate row input
        try:
            row = int(input("Enter row (0-2): "))
        except ValueError:
            print("Invalid input! Please enter a number between 0 and 2.")
            continue

        if row < 0 or row > 2:
            print("Invalid row! Please enter a number between 0 and 2.")
            continue

        # Get and validate column input
        try:
            col = int(input("Enter column (0-2): "))
        except ValueError:
            print("Invalid input! Please enter a number between 0 and 2.")
            continue

        if col < 0 or col > 2:
            print("Invalid column! Please enter a number between 0 and 2.")
            continue

        # Check whether the selected cell is empty
        if board[row][col] != " ":
            print("That cell is already occupied! Try again.")
            continue

        # Place the player's mark
        board[row][col] = current_player
        print_board(board)

        # Check whether the current player has won
        if check_win(board):
            break

        # Check whether the game is a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch players
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

    # Ask whether the players want another round
    while True:
        play_again = input("\nDo you want to play again? (Y/N): ").strip().lower()

        if play_again == "y":
            break
        elif play_again == "n":
            print("Thank you for playing!")
            exit()
        else:
            print("Invalid choice! Please enter Y or N.")
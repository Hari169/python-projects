# Print the board
def print_board(board):
    print(board[0][0], "|", board[0][1], "|", board[0][2])
    print("---------")
    print(board[1][0], "|", board[1][1], "|", board[1][2])
    print("---------")
    print(board[2][0], "|", board[2][1], "|", board[2][2])
#defining the conditions of winning
def check_win(board):
    for row in range(3):
        #when a straight row contains either X or O
        if board[row][0] == board[row][1] == board[row][2] == "X":
            print("X is the winner")
            return True

        if board[row][0] == board[row][1] == board[row][2] == "O":
            print("O is the winner")
            return True

    for col in range(3):
        #when a straight column contains X or O
        if board[0][col] == board[1][col] == board[2][col] == "X":
            print("X is the winner")
            return True
        if board[0][col] == board[1][col] == board[2][col] == "O":
            print("O is the winner")
            return True
    #diagonals with X or O
    if board[0][0] == board[1][1] == board[2][2] == "X":
        print("X is the winner")
        return True
    if board[0][0] == board[1][1] == board[2][2] == "O":
        print("O is the winner")
        return True
    if board[0][2] == board[1][1] == board[2][0] == "X":
        print("X is the winner")
        return True
    if board[0][2] == board[1][1] == board[2][0] == "O":
        print("O is the winner")
        return True

    return False

#condition for Draw
def check_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


while True:
    #default board
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    print_board(board)
    current_player = "X"#to update the values to current player
    while True:

        print('Current player: ', current_player)

        try:
            #entering the rows and columns as proper integer values
            row = int(input("Enter row 0-2: "))
        except ValueError:
            print("Enter a valid row 0-2")
            continue
        if row >= 3 or row < 0:
            print("Enter a valid row 0-2")
            continue
        try:
            col = int(input("Enter column 0-2: "))
        except ValueError:
            print("Enter a valid column 0-2")
            continue
        if col >= 3 or col < 0:
            print("Enter a valid column 0-2")
            continue
        if board[row][col] == " ":
            board[row][col] = current_player #switching player after each move
            print_board(board)

            if check_win(board):
                break
            if check_draw(board):
                print("Draw")
                break

            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

        else:
            print("This cell is occupied")#declaration for occupied cell

    play_again = input("Do you want to play again? (Y/N): ")#uses while loop to repeat the game
    if play_again.lower() != "y":
        print("Thank you for playing")
        break
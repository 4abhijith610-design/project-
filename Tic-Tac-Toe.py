"""
Tic-Tac-Toe Game (2-Player)
"""
# Board Setup

def create_board():
    return [str(i) for i in range(1, 10)]


def display_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

# Move Handling & Input Validation

def get_move(board, player_symbol):
    while True:
        choice = input(f"Player ({player_symbol}), enter a cell number (1-9): ").strip()

        # Handle empty input
        if choice == "":
            print("Input cannot be empty. Please try again.\n")
            continue

        # Handle non-numeric input
        if not choice.isdigit():
            print("That's not a valid number. Please enter a number from 1-9.\n")
            continue

        num = int(choice)

        # Handle out-of-range input
        if num < 1 or num > 9:
            print(" Please choose a number between 1 and 9.\n")
            continue

        index = num - 1

        # Handle already-occupied cell
        if board[index] in ("X", "O"):
            print("That cell is already taken. Choose another one.\n")
            continue

        # Valid move
        return index

# Win / Draw Detection

def check_winner(board, symbol):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6)               # diagonals
    ]

    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] == symbol:
            return True
    return False


def is_draw(board):
    return all(cell in ("X", "O") for cell in board)


# Main Game Loop

def play_round():
    board = create_board()
    current_symbol = "X"   # Player 1 starts
    player_names = {"X": "Player 1", "O": "Player 2"}

    display_board(board)

    while True:
        # Get and apply a valid move
        index = get_move(board, current_symbol)
        board[index] = current_symbol

        display_board(board)

        # Check for a win
        if check_winner(board, current_symbol):
            print(f" {player_names[current_symbol]} ({current_symbol}) wins!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw! The board is full.")
            break

        # Switch turns
        current_symbol = "O" if current_symbol == "X" else "X"


def main():
    print("=" * 40)
    print("      WELCOME TO TIC-TAC-TOE!")
    print("=" * 40)
    print("Player 1 = X   |   Player 2 = O")
    print("Enter a number 1-9 to place your mark:")
    print(" 1 | 2 | 3 ")
    print(" 4 | 5 | 6 ")
    print(" 7 | 8 | 9 ")

    while True:
        play_round()

        # Play again option
        again = input("\nPlay again? (y/n): ").strip().lower()
        while again not in ("y", "n", "yes", "no"):
            again = input("Please enter 'y' or 'n': ").strip().lower()

        if again in ("n", "no"):
            print("\nThanks for playing! Goodbye")
            break

if __name__ == "__main__":
    main()

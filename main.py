import random

def calculate_xor_sum(board):
    xor_sum = 0
    for row in board:
        xor_sum ^= row
    return xor_sum

def print_board(board):
    print("Current board state:")
    for i, row in enumerate(board):
        print(f"Row {i+1}: {'█' * row} ({row} squares)")
    print()

def get_optimal_move(board):
    xor_sum = calculate_xor_sum(board)
    if xor_sum == 0:
        return None, None
    for i, row in enumerate(board):
        if row ^ xor_sum < row:
            return i, row - (row ^ xor_sum)
    return None, None

def player_move(board):
    while True:
        try:
            row = (
                int(
                    input(
                        "Enter the row number to remove squares from (1-based index): "
                    )
                )
                - 1
            )
            if row < 0 or row >= len(board):
                raise ValueError("Row number out of range.")
            count = int(
                input(
                    f"Enter the number of squares to remove from row {row + 1} (1-{board[row]}): "
                )
            )
            if count <= 0 or count > board[row]:
                raise ValueError("Invalid number of squares.")
            board[row] -= count
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def optimal_move(board):
    row, count = get_optimal_move(board)
    if row is not None:
        print(f"Optimal move: Remove {count} squares from row {row + 1}.")
        board[row] -= count
    else:
        print("No optimal move available. Making a random move.")
        make_random_move(board)

def make_random_move(board):
    non_empty_rows = [i for i, row in enumerate(board) if row > 0]
    if not non_empty_rows:
        return
    row = random.choice(non_empty_rows)
    count = random.randint(1, board[row])
    print(f"Random move: Remove {count} squares from row {row + 1}.")
    board[row] -= count

def is_game_over(board):
    return all(squares == 0 for squares in board)

def read_board_from_file(file_path):
    while True:
        try:
            with open(file_path, "r") as file:
                board = [int(line.strip()) for line in file.readlines()]
            if any(x <= 0 for x in board):
                raise ValueError("Board values must be positive integers.")
            return board
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}. Please try again.")
            file_path = input("Enter a valid file path: ").strip()

def generate_random_board(n, m):
    return [random.randint(1, m) for _ in range(n)]

def main():
    print("Welcome to the Square Game!")

    while True:
        try:
            choice = input(
                "Enter '1' to read board from file, '2' to generate random board: "
            ).strip()
            if choice == "1":
                file_path = input("Enter the path to the input file: ").strip()
                board = read_board_from_file(file_path)
            elif choice == "2":
                n = int(input("Enter the number of rows (n): ").strip())
                m = int(input("Enter the maximum squares per row (m): ").strip())
                if n <= 0 or m <= 0:
                    raise ValueError("Both n and m must be positive integers.")
                board = generate_random_board(n, m)
            else:
                raise ValueError("Invalid choice.")
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    print_board(board)

    while not is_game_over(board):
        print("Your turn:")
        player_move(board)
        print_board(board)

        if is_game_over(board):
            print("You win!")
            break

        print("Computer's turn:")
        optimal_move(board)
        print_board(board)

        if is_game_over(board):
            print("Computer wins!")
            break

if __name__ == "__main__":
    main()

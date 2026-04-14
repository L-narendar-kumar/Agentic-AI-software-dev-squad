def print_board(board):
    """
    Prints the Sudoku board in a formatted way.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def find_empty(board):
    """
    Finds the next empty cell (represented by 0) on the board.
    Returns (row, col) if an empty cell is found, otherwise None.
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)  # (row, col)
    return None

def is_valid(board, num, pos):
    """
    Checks if placing 'num' at 'pos' (row, col) is valid according to Sudoku rules.
    """
    row, col = pos

    # Check row
    for c in range(9):
        if board[row][c] == num and col != c:
            return False

    # Check column
    for r in range(9):
        if board[r][col] == num and row != r:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3

    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if board[r][c] == num and (r, c) != pos:
                return False

    return True

def solve(board):
    """
    Solves the Sudoku puzzle using a backtracking algorithm.
    Modifies the board in place.
    Returns True if a solution is found, False otherwise.
    """
    find = find_empty(board)
    if not find:
        return True  # No empty cells, puzzle solved

    row, col = find

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0  # Backtrack

    return False

def parse_input(input_string):
    """
    Parses a string of 81 characters into a 9x9 Sudoku board.
    '0' or '.' are treated as empty cells.
    Raises ValueError if input is invalid.
    """
    input_string = input_string.replace('.', '0').strip()
    if len(input_string) != 81:
        raise ValueError("Input must be exactly 81 characters long.")

    board = []
    for i in range(9):
        row = []
        for j in range(9):
            char = input_string[i * 9 + j]
            if not char.isdigit():
                raise ValueError(f"Invalid character '{char}' found. Only digits (0-9) are allowed.")
            num = int(char)
            if not (0 <= num <= 9):
                raise ValueError(f"Invalid digit '{num}' found. Digits must be between 0 and 9.")
            row.append(num)
        board.append(row)
    return board

if __name__ == "__main__":
    print("Sudoku Solver")
    print("Enter your Sudoku puzzle as a single string of 81 digits (0-9).")
    print("Use '0' or '.' for empty cells.")
    print("Example: 530070000600195000098000060800060003400803001700020006060000280000419005000080079")

    user_input = input("Enter puzzle: ")

    try:
        initial_board = parse_input(user_input)
        # Create a deep copy of the board for the solver, as it modifies in place
        # A simple list comprehension for a 2D list of immutable integers is sufficient.
        board_to_solve = [row[:] for row in initial_board]

        print("\nOriginal Puzzle:")
        print_board(initial_board)
        print("\nAttempting to solve...")

        if solve(board_to_solve):
            print("\nSolved Sudoku:")
            print_board(board_to_solve)
        else:
            print("\nNo solution exists for the given puzzle.")
            print("The original puzzle was:")
            print_board(initial_board)

    except ValueError as e:
        print(f"\nError: {e}")
        print("Please ensure your input is a valid 81-character string of digits (0-9).")

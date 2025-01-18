# Dimensions of the connect four board
ROW_COUNT = 6
COLUMN_COUNT = 8

# Function to create a new Connect Four board
def create_board():
    board = []
    for _ in range(ROW_COUNT):
        board.append([0] * COLUMN_COUNT)
    return board

# Function to drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column is valid for dropping a piece
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Function to get the next open row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to print the board
def print_board(board):
    for row in reversed(board):
        row_str = ""
        for cell in row:
            row_str += str(cell) + " "
        print(row_str)
    print("-" * (COLUMN_COUNT * 2 + 1))  # Line separator

# Function to check if a player has won
def winning_move(board, piece):
    # Checking horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Checking vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Checking positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Checking negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

# Heuristic evaluation function
def evaluate_board(board, piece):
    score = 0

    # Checking horizontal score
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Checking vertical score
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            window = [board[r + i][c] for i in range(4)]
            score += evaluate_window(window, piece)

    # Checking positively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Checking negatively sloped diagonal score
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Heuristic function to evaluate a window of 4 cells
def evaluate_window(window, piece):
    score = 0
    opponent_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

# Function to determine the best column for the AI to make a move using minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player, piece):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)

    if depth == 0 or len(valid_locations) == 0 or winning_move(board, 1) or winning_move(board, 2):
        if winning_move(board, 2):
            return (None, 100000000000000)
        elif winning_move(board, 1):
            return (None, -10000000000000)
        else:  # Game is over, no more valid moves
            return (None, evaluate_board(board, piece))
    elif maximizing_player:
        value = -float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, piece)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False, piece)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, 1 if piece == 2 else 2)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True, piece)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Main function to play the game
def main():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    while not game_over:
        # Player 1 input
        if turn == 0:
            valid_input = False
            while not valid_input:
                try:
                    print("Player 1 make your selection (1-", COLUMN_COUNT, "):", end=" ")
                    col = int(input()) - 1
                    if col < 0 or col >= COLUMN_COUNT or not is_valid_location(board, col):
                        print("Invalid column! Please select again.")
                    else:
                        valid_input = True
                except ValueError:
                    print("Invalid input! Please enter a number.")
            
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("Player 1 wins!")
                game_over = True
        # Player 2 / AI input
        else:
            col, _ = minimax(board, 6, -float('inf'), float('inf'), True, 2)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("Player 2 wins!")
                game_over = True

        print_board(board)
        turn += 1
        turn %= 2  # Switch between players 1 and 2 / AI

        empty_cells = 0
        for row in board:
            for cell in row:
                if cell == 0:
                    empty_cells += 1
        if empty_cells == 0:
            print("Game Over - Draw!")
            game_over = True

main()
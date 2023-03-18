import os
import sys
import random

####################################################################
#   Interactive mode test command:                                 #
#   python maxconnect4.py interactive input8.txt human-next 7     #
#                                                                  #
#   One-Move mode test command:                                    #
#   python maxconnect4.py one-move input2.txt output2.txt 7        #
####################################################################

def command_line_inputs() -> list:
    try:
        mode = sys.argv[1]
        
        if mode == "interactive":
            input_file = sys.argv[2]
            next_player = sys.argv[3]
            depth: int = int(sys.argv[4])
            return mode, input_file, next_player, depth
        elif mode == "one-move":
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            depth: int = int(sys.argv[4])
            return mode, input_file, output_file, depth
        else:
            raise Exception("The requested mode does not exist. Options are: [interactive, one-move]")
    except IndexError:
        print('Please pass arguments to specify the desired mode and parameters.')
        sys.exit(1)
        
def read_board_from_file(filename: str = "input2.txt"):
    board = []
    next_player = None
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if len(line) == 7:
                    # print(f"row: {line}")
                    row = []
                    for c in line:
                        row.append(c)
                    board.append(row)
                elif len(line) == 1:
                    # print(f"next turn: {line}")
                    next_player = int(line)
    except FileNotFoundError:
        # Generate empty board
        print("Starting new game...")
        board = [["0" for _ in range(7)] for _ in range(6)]
        next_player = random.choice(["computer-next","human-next"])
                
    return board, next_player

def write_board_to_file(board: list[list[str]], turn: str = "human-next", filename: str = "output.txt"):
    with open(filename, 'w') as f:
        line = ""
        
        for row in board:
            for c in row:
                line += c
            f.write(line + "\n")
            line = ""
            
        if turn == "human-next":
            f.write("1\n")
        else: 
            f.write("2\n")
        
            
def print_board(board: list[list[str]]) -> None:
    print("\n  " + " ".join([str(i+1) for i in range(len(board[0]))]))
    for i, row in enumerate(board):
        print(f"{len(board) - i} ", end="")
        for item in row:
            if item == "0":
                print("⚪️", end="")
            elif item == "1":
                print("🔴", end="")
            elif item == "2":
                print("🟢", end="") 
        print() if i != len(board) - 1 else None
        
def window_has_point(window) -> bool:
    return all([item == window[0] for item in window])
        
def game_is_over(board) -> bool:
    '''
    Return true if game is over
    '''
    # if any value is zero, return False
    for row in board:
        for val in row:
            if val == "0":
                return False
    return True
    
def score_board(board: list[list[str]]):
    '''
    Computes the score each player has. 
    '''
    
    p1_points, p2_points = 0, 0
    
    '''
    HORIZONTAL POINTS
    '''
    
    # Use a sliding window of 4 approach to count horizontal points
    for row in board:
        
        l = 0
        u = 3
        
        while u < len(row):
            window = row[l:u+1]
            # print(window)
            
            if window_has_point(window):
                if window[0] == "1":
                    p1_points += 1
                elif window[0] == "2":
                    p2_points += 1
            
            # Move the window
            l += 1
            u += 1
            
    '''
    VERTICAL POINTS
    '''
    
    transposed_board = list(map(list, zip(*board)))
    
    for row in transposed_board:
        
        l = 0
        u = 3
        
        while u < len(row):
            window = row[l:u+1]
            # print(window)
            
            if window_has_point(window):
                if window[0] == "1":
                    p1_points += 1
                elif window[0] == "2":
                    p2_points += 1
            
            # Move the window
            l += 1
            u += 1
            
    '''
    UPPER DIAGONAL POINTS FOR TOP HALF
    '''
    for i in range(len(board)):
        x_values = [i - j for j in range(i+1)]
        y_values = [j for j in range(i+1)]
            
        diagonal_row = []
        for j in range(len(x_values)):
            diagonal_row.append(board[x_values[j]][y_values[j]])
        
        # Slide window across diagonal row and add points
        if len(diagonal_row) >= 4:
            l = 0
            u = 3
            
            while u < len(diagonal_row):
                window = diagonal_row[l:u+1]
                
                if window_has_point(window):
                    if window[0] == "1":
                        p1_points += 1
                    elif window[0] == "2":
                        p2_points += 1
                
                # Move the window
                l += 1
                u += 1
                
    '''
    UPPER DIAGONAL FOR BOTTOM HALF
    '''
    
    print("\n\n\n")
    # Start at 1st index for columns, last row
    for i in range(1, len(board[0])):
        y_values = list(reversed([j for j in range(len(board))]))
        x_values = list(range(i, len(board[0])))
        
        diagonal_row = []
        for j in range(len(x_values)):
            diagonal_row.append(board[y_values[j]][x_values[j]])
        
        if len(diagonal_row) >= 4:
            l = 0
            u = 3
            
            while u < len(diagonal_row):
                window = diagonal_row[l:u+1]
                
                if window_has_point(window):
                    if window[0] == "1":
                        p1_points += 1
                    elif window[0] == "2":
                        p2_points += 1
                
                # Move the window
                l += 1
                u += 1
    
    '''
    DOWNWARD DIAGONAL BOTTOM CHECK
    '''
    
    for i in range(len(board)): 
        y_values = [j for j in range(i, len(board))]
        x_values = [j for j in range(len(y_values))]
        
        diagonal_row = []
        for j in range(len(x_values)):
            diagonal_row.append(board[y_values[j]][x_values[j]])
        
        if len(diagonal_row) >= 4:
            l = 0
            u = 3
            
            while u < len(diagonal_row):
                window = diagonal_row[l:u+1]
                
                if window_has_point(window):
                    if window[0] == "1":
                        p1_points += 1
                    elif window[0] == "2":
                        p2_points += 1
                
                # Move the window
                l += 1
                u += 1
        
        
    '''
    DOWNWARD DIAGONAL TOP CHECK
    '''
    
    for i in range(1, len(board[0])):
        
        x_values = [j for j in range(i, len(board[0]))]
        y_values = [j for j in range(len(x_values))]
        
        diagonal_row = []
        for j in range(len(x_values)):
            diagonal_row.append(board[y_values[j]][x_values[j]])
        
        if len(diagonal_row) >= 4:
            l = 0
            u = 3
            
            while u < len(diagonal_row):
                window = diagonal_row[l:u+1]
                
                if window_has_point(window):
                    if window[0] == "1":
                        p1_points += 1
                    elif window[0] == "2":
                        p2_points += 1
                
                # Move the window
                l += 1
                u += 1
    
    return p1_points, p2_points

def fix_board(board: list[list[str]]) -> list[list[str]]:
    """
    Moves pieces down 1 spot if possible.
    """

    # Make a copy of the input board
    new_board = [row[:] for row in board]

    # Iterate over the columns of the board
    for col_index in range(len(board[0])):
        # Extract the current column as a list
        column = [board[row_index][col_index] for row_index in range(len(board))]
        
        # Move non-zero pieces down as far as possible
        for row_index in range(len(column) - 1, -1, -1):
            if column[row_index] != '0':
                for shift_index in range(row_index+1, len(column)):
                    if column[shift_index] == '0':
                        # Swap the pieces
                        column[row_index], column[shift_index] = column[shift_index], column[row_index]

        # Update the new board with the modified column
        for row_index in range(len(column)):
            new_board[row_index][col_index] = column[row_index]
    
    # Return the modified copy of the board
    return new_board

def has_empty_cell_below(board) -> bool:
    """
    Check if there is any non-zero cell in the given column that has an empty cell below it.

    Returns:
    True if there is any non-zero cell in the column that has an empty cell below it, False otherwise.
    """
    
    
    # Iterate over the columns
    for i in range(len(board[0])):
        
        # Get column i
        column = [board[j][i] for j in range(len(board))]
        # print(f"column: {column}")
        
        # Find first nonzero number. If zero after that, then return True. Otherwise False
        found_nonzero = False
        for value in column:
            # If we find nonzero value, save its index
            if value != "0" and not found_nonzero:
                found_nonzero = True
                continue
            
            if value == "0" and found_nonzero:
                return True
        
    # If no non-zero cell has an empty cell below it, return False
    return False

def minimax(board, depth):
    '''
    Input: current board state
    Output: optimal next move given the depth limit 
    
    num_valid_moves = num_cols - num_full_cols (check board[0])
    '''
    # TODO: Implement (watch seb lague video)
    pass
    
def play_move(board: list[list[str]], col: int, curr_player: int) -> list[list[str]]:
    '''
    Input: Current board, column to play move, and the current player
    Output: Updated board after playing that move.
    '''
    
    # Account for 1-indexed display function
    col -= 1
    
    # Place piece at top
    if curr_player == "human-next":
        board[0][col] = "1"
    else:
        board[0][col] = "2"
    
    # Fix the board
    while has_empty_cell_below(board):
        board = fix_board(board)
        
    # Return fixed board
    return board

def print_score(p1_score, p2_score, game_over = False) -> None:
    if game_over:
        if p1_score > p2_score: print("Red wins!")
        elif p1_score == p2_score: print("Tie game!")
        else: print("Green wins!")
    else:
        print(f"{p1_score} - {p2_score}")
        
def static_evalulation(board) -> int:
    '''
    Evaluates a board state as single integer. 
    '''
    p1_points, p2_points = score_board(board)
    return p1_points - p2_points

def toggle_turn(curr_player: str) -> str:
    return "computer-next" if curr_player == "human-next" else "human-next"



def interactive(board, next_turn, depth):
    if next_turn == "computer-next":
        # Print current board and score
        print_board(board)
        p1_score, p2_score = score_board(board)
        print_score(p1_score, p2_score)
        
        # If terminal, exit
        if game_is_over(board):
            p1_score, p2_score = score_board(board)
            print_score(p1_score, p2_score, game_over=True)
        else:
            # TODO: use minimax to compute next move
            pass
    else:
        # TODO: Implement human move here
        pass

def main():
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Collect argument data 
    mode, input_file, next_player, depth = command_line_inputs()
    output_file = next_player if mode == "one-move" else ""
    
    # Output argument data
    print(f"\nmode: \t\t{mode}")
    print(f"input_file: \t{input_file}")
    print(f"output_file: \t{output_file}") if mode == "one-move" else print(f"next_player: \t{next_player}")
    print(f"depth: \t\t{depth}\n")
    
    # Read in file
    board, _ = read_board_from_file(input_file)
    
    # Fix board
    while has_empty_cell_below(board):
        board = fix_board(board)
        
    print_board(board)
    
    board = play_move(board, 5, next_player)
    print_board(board)
    
    p1_points, p2_points = score_board(board)
    # print_score(p1_points, p2_points)
    
    # print(static_evalulation(board))
    
    next_player = toggle_turn(next_player)
    
    write_board_to_file(board, next_player, "output_test.txt")
    
    
    
    
    
    # if mode == "interactive":
    #     interactive(board, next_player, depth)
    # elif mode == "one-move":
    #     pass
    

if __name__ == '__main__':
    main()
import os
import sys

####################################################################
#   Interactive mode test command:                                 #
#   python maxconnect4.py interactive input2.txt output2.txt 7     #
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
                
    return board, next_player
            
def print_board(board: list[list[str]]) -> None:
    print("  " + " ".join([str(i+1) for i in range(len(board[0]))]))
    for i, row in enumerate(board):
        print(f"{len(board) - i} ", end="")
        for item in row:
            if item == "0":
                print("⚪️", end="")
            elif item == "1":
                print("🔴", end="")
            elif item == "2":
                print("🟢", end="") 
        print()
        
def window_has_point(window) -> bool:
    return all([item == window[0] for item in window])
        
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
        
    
    
    print(f"\nScore: ({p1_points}-{p2_points})", end="")
    if p1_points > p2_points: print(" :: Red is winning! ")
    elif p1_points == p2_points: print(" :: Tied!")
    else: print(" :: Green is winning! ")

def main():
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    mode, input_file, next_player, depth = command_line_inputs()
    output_file = next_player if mode == "one-move" else ""
    
    print(f"mode: \t\t{mode}")
    print(f"input_file: \t{input_file}")
    print(f"output_file: \t{output_file}") if mode == "one-move" else print(f"next_player: {next_player}")
    print(f"depth: \t\t{depth}\n")
    
    board, next_player = read_board_from_file(input_file)
    
    # print(board)
    # print(next_player, end="\n\n")
    
    print_board(board)
    
    score_board(board)

if __name__ == '__main__':
    main()
import os
import sys

####################################################################
#   Interactive mode test command:                                 #
#   python maxconnect4.py interactive input1.txt output1.txt 7     #
#                                                                  #
#   One-Move mode test command:                                    #
#   python maxconnect4.py one-move input1.txt output1.txt 7        #
####################################################################

def command_line_inputs() -> list:
    try:
        mode = sys.argv[1]
        
        if mode == "interactive":
            input_file = sys.argv[2]
            next_player = sys.argv[3]
            depth = sys.argv[4]
            return mode, input_file, next_player, depth
        elif mode == "one-move":
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            depth = sys.argv[4]
            return mode, input_file, output_file, depth
        else:
            raise Exception("The requested mode does not exist. Options are: [interactive, one-move]")
    except IndexError:
        print('Please pass arguments to specify the desired mode and parameters.')
        sys.exit(1)

def main():
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    mode, input_file, next_player, depth = command_line_inputs()
    output_file = next_player if mode == "one-move" else ""
    
    print(f"mode: {mode}")
    print(f"input_file: {input_file}")
    print(f"output_file: {output_file}") if mode == "one-move" else print(f"next_player: {next_player}")
    print(f"depth: {depth}")

if __name__ == '__main__':
    main()
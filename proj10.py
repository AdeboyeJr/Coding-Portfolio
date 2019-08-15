############################################################
#
#                       Project 10
#-Create a Checkers game
#-Create a way for users to indexify and deindexify 
#coordinates
#-Find all possible moves and captures
#-Apply moves and captures
#-Provide hints of possible moves or captures
#-Create AI that plays against user input
#-Declare a winner
############################################################

import tools
import gameai as ai
from checkers import Piece
from checkers import Board


"""
    Text based Checkers game. Human vs. AI
"""

def indexify(position):
    """
    Takes a string and converts into coordinates
    """
    string_dict ={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,\
               'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,\
               't':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}
    #dictionary for indexing 
    
    #variable calls dictionary in global namespace
    
    coord_string = position[0]
    #saves letter as a variable
    
    row = string_dict.get(coord_string)
    #searches for number associated with string and saves as a value
    
    column_num = int(position[1:]) - 1
    #takes second index of position, converts to an int then subtracts 1
    
    tup = (row,column_num)
    #final coordinate
    
    return tup

def deindexify(row, col):
    """
    Takes coordinates and converts back to strings
    """
    string_dict ={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,\
               'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,\
               't':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}
    #dictionary for indexing 
    
    letter = [ key for key,val in string_dict.items() if val==row ]
    #use list comprehension to search for the string in the string dict 
    #using row
    
    number = col+1 #simply add 1 to the column to get the number
    
    string = ''.join(letter) + str(number) #join letter list into an empty 
    #string. Then concatenate with number string
    
    return string

def initialize(board):
    """
    This function puts white and black pieces according to the checkers
    game positions. The black pieces will be on the top three rows and
    the white pieces will be on the bottom three rows (for an 8x8 board).
    The first row for the black pieces will be placed as a2, a4, a6, ...
    etc. and the next rows will be b1, b3, b5, ... etc. For the white
    rows, the placement patterns will be opposite of those of blacks.
    This must work for any even length board size.
    """
    row = col = board.get_length()
    initrows = (row // 2) - 1
    for r in range(row - 1, row - (initrows + 1), -1):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece('white'))
    for r in range(0, initrows):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece())

def count_pieces(board):
    """
    Count number of black and white pieces currently on the board
    """
    black_piece = 0
    white_piece = 0
    #counters for pieces
    
    board_length = board.get_length()
    #saves length of the board to be used as an iterable
    
    
    for row in range(board_length):
        #iterate through the length of the board row by row
        
        for col in range(board_length):
            #iterate throught the length of the board column by column
            
            piece = board.get(row,col) 
            #get pieces at specific coordinate
            
            if piece == None:
                continue
                
            if Piece.is_white(piece) == True:
                    white_piece += 1
                    #add to white counter if piece is white
                    
            elif Piece.is_black(piece) == True:
                    black_piece += 1
                    #add to black counter if piece is black
                    
    tup = (black_piece,white_piece) 
    return tup       

def get_all_moves(board, color, is_sorted = False):
    """
    Returns list of tuples that store information of first position and possible 
    positions to take from first position.
    """
    
    move_list = []
    
    board_length = board.get_length()
    for row in range(board_length):
            for col in range(board_length):
                
                deindex = deindexify(row,col)
                #convert row and columns into a string; will be used as
                #starting positon
                
                
                piece = board.get(row,col)
                #find piece at given row and column
                
                if piece != None and piece.color() == color:
                    
                    moves = tools.get_moves(board,row,col)
                    #find possible moves for each row as long as there is a 
                    #piece in that position
                    
                    if moves:
                        
                            
                            
                            for element in moves:
                                
                                move_tup = (deindex,element)
                                #create a tuple for the starting postion and
                                #ending position
                                
                                move_list.append(move_tup)
                            
    return sorted(move_list) 

def sort_captures(all_captures,is_sorted=False):
    '''If is_sorted flag is True then the final list will be sorted by the 
    length of each sub-list and the sub-lists with the same length will be
    sorted again with respect to the first item in corresponding the sub-list,
    alphabetically.'''
    
    return sorted(all_captures, key = lambda x: (-len(x), x[0])) if is_sorted \
            else all_captures

def get_all_captures(board, color, is_sorted = False):
    """
    Find all possible captures for each piece on the board
    """
    capture_list = []
    #list to be returned after iterated through length of the board
    
    board_length = board.get_length()
    
    for row in range(board_length):
        for col in range(board_length):
            
            
            piece = board.get(row,col)
            #saves piece as a variable
            
            
            if piece!= None and piece.color() == color:
                captures = tools.get_captures(board,row,col)
                #find all possible captures for a specific place on the board
                #as long as said place has a piece on it
                
                if captures:
                    
                    for element in captures:
                        
                        
                        capture_list.append(element)
                        #takes every element found in the captures list and 
                        #appends it to the empty capture list
                        
    return capture_list

def apply_move(board, move):
    """
    Takes piece from initial postion and moves it to the last position. If 
    movement yields a board position on the kings row, then the piece will turn
    into a king (use the turn_king() function)
    
    Raise this exception below:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.") 
    If,
        a. there is no move from move[0], i.e. use tools.get_moves() function to
            get all the moves from move[0]
        b. the destination position move[1] is not in the moves list found
            from tools.get_moves() function.            
    """
    
    
    board_length = board.get_length()
    #length of the board
    
    if move:
        
               coord= indexify(move[0])
               #takes string in move tuple and converts said string into 
               #coordinates
               
               row = coord[0] #first element in coordinate tuple
               
               col = coord[1] #second element in coordinate tuple
                
               move1 = indexify(move[1])
               row2 = move1[0]
               col2 = move1[1]
               #second pair of coordinates, rows and columns for the ending 
               #position
                   
               moves = tools.get_moves(board,row,col)
               #find possible moves for the piece at said row and column
               
               
                    
               if move[1] in moves:
                   #checks to see if the second move provided is a possible move
                       
                    piece = board.get(row,col)
                    if piece == None:
                        pass    
                    
                    board.remove(row,col)
                    #remove whatever is on the board at given row and column
                    
                    board.place(row2,col2,piece)
                    #place new piece at new row and column
                    
                        
                    if piece.color() == 'white':
                        if row2 == 0:
                            piece.turn_king()
                            #turns white pieces into kings if they happened to 
                            #reach the opposite end of the board
                            
                    if piece.color() == 'black':
                        if row2 == board_length -1:
                            piece.turn_king()
                            #turns black pieces into kings if they happened to
                            #reach the opposite end of the board
                
               else:
                       raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.") 
                       #raise error if given move is not a possible move
                       
            
    else:
       raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.") 
       #raise error if given move is not valid
        
  

def apply_capture(board, capture_path):
    """
    Uses get_all_captures funtion and executes all the possible captures for 
    a given piece via the capture path
    
    Raise this exception below:
        raise RuntimeError("Invalid jump/capture, please type" \
                         + " \'hints\' to get suggestions.") 
    If,
        a. there is no jump found from any position in capture_path, i.e. use 
            tools.get_jumps() function to get all the jumps from a certain
            position in capture_path
        b. the destination position from a jump is not in the jumps list found
            from tools.get_jumps() function.            
    """
  
    track = 0 
    #keeps track of which position to move from in capture path
     
    for capture in capture_path[:len(capture_path)-1]:
        #iterates through capture path list
       
        
           begin_point_pos = indexify(capture)
           #save capture as starting coordinate
           
           row_begin = begin_point_pos[0]
           #staring row
           
           col_begin = begin_point_pos[1]
           #starting column
           
           jumps = tools.get_jumps(board,row_begin,col_begin)
           #save list of possible jumps as avariable
           
           if jumps and capture_path[track +1] in jumps:
               #checks if the next element in the capture path is a possible
               #jump
               
               piece = board.get(row_begin,col_begin)
               #save pieces as a variable
               
               board.remove(row_begin,col_begin)
               #remove piece from starting position
               
               row,col = indexify(capture_path[track +1])
               
               
               if row > row_begin:
                   row_sub = row_begin +1
                   #row the piece jumps over is just 1 row above starting row
                   #if and only if the ending row is greater than the starting 
                   #row
                   
               else:
                   row_sub = row_begin -1
               
               if col > col_begin:
                   col_sub = col_begin +1
                   #column the piece jumps over is just 1 column above starting 
                   #column if and only if the ending row is greater than the 
                   #starting column
                   
               else:
                   col_sub = col_begin -1
              
               board.remove(row_sub,col_sub)
               #remove pieces that have been jumped over 
               
               board.place(row,col,piece)
               #place piece in ending position
               
               track += 1
               #add to track to allow loop to move to next element in list
               
               if piece.color() == 'black' and row == board.get_length() -1: 
                   piece.turn_king()
                   
               if piece.color() == 'white' and row == 0:
                   piece.turn_king()
                   #turns piece into king if it meets criteria
                   
            
            
           else:
                raise RuntimeError("Invalid jump/capture, please type" \
                             + " \'hints\' to get suggestions.") 
               #returns error if jump is not a possible jump
            
def get_hints(board, color, is_sorted = False):
    """
    Gives user all possible moves or jumps they can make 
    """
    capture_list =  get_all_captures(board,color,is_sorted = False)
    #saves capture list as the get all captures funciton
    
    move_list = get_all_moves(board,color,is_sorted = False)
    #saves the move list as teh get all moves function
    
    if capture_list == []:
        hint_tup = (move_list,[])
        #return only the move list if the capture list is enpty
    else:
        hint_tup = ([],capture_list)
        #if capture list is not empty, only return capture list
                       
    return hint_tup
        
def get_winner(board, is_sorted = False):
    """
    Finds current winner
    """
    piece_num = count_pieces(board)
    #save number of pieces as funtion
    
    black = get_hints(board,'black', is_sorted)
    white = get_hints(board,'white', is_sorted)
    #use get hints function for both black and white pieces

    if black[0] != [] or black[1] != []:
        if white[0] == [] and white[1] == []:
            return 'black'
    #black is the winner if black still has moves and jumps while white has
    #no remaining moves or jumps
    
    elif white[0] != [] or white[1] != []:
        if black[0] == [] and black[1] == []:
            return 'white'
    #white is the winner if white still has moves and jumps while black has no
    #remaining moves or jumps
    
    if piece_num[0] == 1 and piece_num[1] == 1:
       
            return 'draw'
    #if the number of white and black pieces both equal one, it's a draw
    
    else:
        return 'black'
        
    

                        
def is_game_finished(board, is_sorted = False):
    """
    Checks to see if game has ended. Returns Boolean
    """

    black = get_hints(board,'black', is_sorted = False)
    white = get_hints(board,'white', is_sorted = False)
    if black[0] == [] and black[1] == []:
        return True
    #game is over when the black pieces don't have any possible moves left
            
    elif white[0] == [] and white[1] == []:
        return True
    #game is over when the white pieces don't have possible moves left
    
    else:
        return False
    #if niether pieces ran out of possible moves, game continues
            
# Some error messages to save lines.
move_error = "Invalid move, please type \'hints\' to get suggestions."
hasjump_error = "You have jumps, please type \'hints\' to get suggestions."
jump_error = "Invalid jump, please type \'hints\' to get suggestions."
hint_error = "Invalid hint number."
cmd_error = "Invalid command."

def game_play_human():
    """
    This is the main mechanism of the human vs. human game play.
    Use this function to write the game_play_ai() function.
    """    
    # UNCOMMENT THESE TWO LINES TO TEST ON MIMIR SUBMISSION
    # Piece.symbols = ['b', 'w']
    # Piece.symbols_king = ['B', 'W']
    
    prompt = "[{:s}'s turn] :> "
    print(tools.banner)
   
    # Choose the color here
    (my_color, opponent_color) = tools.choose_color()
    
    # Take a board of size 8x8
    board = Board(8)
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'black' else opponent_color
    print("Black always plays first.\n")
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            
            # Get the command from user using input
            command = input(prompt.format(turn)).strip().lower()
            
            # Now decide on different commands
            if command == 'pass':
                break
            elif command == 'exit':
                break
            elif command == 'hints':
                (moves, captures) = get_hints(board, turn, True)
                if moves:
                    print("You have moves:")
                    for i, move in enumerate(moves):
                        print("\t{:d}: {:s} --> {:s}"\
                                  .format(i + 1, move[0], move[1]))
                if captures:
                    print("You have captures:")
                    for i, path in enumerate(captures):
                        print("\t{:d}: {:s}".format(i + 1, str(path)))
            else:
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    if command != 'pass':
        winner = get_winner(board)
        if winner != 'draw':
            diff = abs(piece_count[0] - piece_count[1])
            print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
        else:
            print("This game ends in a draw.")
    else:
        winner = opponent_color if turn == my_color else my_color
        print("{:s} gave up! {:s} is the winner!! yay!!!".format(turn, winner))
    # --- end of game play human ---
    
def game_play_ai():
    """
    This is the main mechanism of the human vs. ai game play. You need to
    implement this function by taking helps from the game_play_human() 
    function.
    
    For a given board situation/state, you can call the ai function to get
    the next best move, like this:
        
        move = ai.get_next_move(board, turn)
        
    where the turn variable is a color 'black' or 'white', also you need to 
    import ai module as 'import gameai as ai' at the beginning of the file.
    This function will be very similar to game_play_human().
    """
    prompt = "[{:s}'s turn] :> "
    print(tools.banner)
   
    # Choose the color here
    (my_color, opponent_color) = tools.choose_color()
    
    Piece.symbols = ['b', 'w']
    Piece.symbols_king = ['B', 'W']
    
    
    # Take a board of size 8x8
    board = Board(8)
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'black' else opponent_color
    print("Black always plays first.\n")
    
    game_over = False
    #variable to keep track of game status
    
    # loop until the game is finished
    while not game_over:
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            
            # cpu chooses command
            if turn == my_color:
                command = input(prompt.format(turn)).strip().lower()
                #allows user to select commands if it's their turn
                
            else:
                moves = ai.get_next_move(board,turn)
                
                
                
                if type(moves) == tuple:
                        command = "move {:s} {:s}".format(moves[0], moves[1])
                        #formats moves as a string
                else:
                    command = "jump {:s}".format(" ".join([v for v in moves]))
                    #joins each move in list into an empty string
                command = command.strip().lower()
                
            
                
                
            # Now decide on different commands
            if command == 'pass':
                break
            elif command == 'exit':
                break
            elif command == 'hints':
                (moves, captures) = get_hints(board, turn, True)
                if moves:
                    print("You have moves:")
                    for i, move in enumerate(moves):
                        print("\t{:d}: {:s} --> {:s}"\
                                  .format(i + 1, move[0], move[1]))
                if captures:
                    print("You have captures:")
                    for i, path in enumerate(captures):
                        print("\t{:d}: {:s}".format(i + 1, str(path)))
            else:
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
                
                status = is_game_finished(board)
                #lets program know if game is finished
                if status == False:
                    continue
                elif status == True:
                    game_over = True
                    
                    break
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    if command != 'pass':
        winner = get_winner(board)
        if winner != 'draw':
            diff = abs(piece_count[0] - piece_count[1])
            print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
        else:
            print("This game ends in a draw.")
    else:
        winner = opponent_color if turn == my_color else my_color
        print("{:s} gave up! {:s} is the winner!! yay!!!".format(turn, winner))
    # --- end of game play ai ---

def main():
#    game_play_human()
    game_play_ai()
    
# main function, the program's entry point
if __name__ == "__main__":
    main()


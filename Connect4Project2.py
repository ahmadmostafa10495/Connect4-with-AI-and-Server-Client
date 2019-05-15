import numpy as np
import random
import math
import socket
difficulty = 5
ROWS = 6
COLS = 7
GAME_OVER = False
PLAYER_TURN = 0
AI_TURN = 1
TURN = random.randint(PLAYER_TURN, AI_TURN)
PLAYER = 1
AI = 2
FREE = 0
LINE_SIZE = 4
def save(board,name,difficulty, turn):
    fileToSave = open(name+".txt",'w')
    for r in range(ROWS):
        for c in range(COLS):
            fileToSave.write(str(int(list(board)[r][c]))+ " ")
        fileToSave.write("\n")
    fileToSave.write(str(difficulty))
    fileToSave.write("\n")
    fileToSave.write(str(turn))
    fileToSave.close()
def load (name):
    arr = []
    fileToLoad = open(name+".txt",'r')
    for r in range(ROWS):
        s = fileToLoad.readline()
        arr.append(np.fromstring(s, dtype=int, sep=' '))
    arr2d = np.array(arr)
    difficulty = int(fileToLoad.readline())
    turn = int(fileToLoad.readline())
    fileToLoad.close()
    return arr2d, difficulty, turn
def make_board_with_dim(ROWS, COLS):
    return np.zeros((ROWS,COLS))
def print_board_up_right(board):
    print(np.flip(board))
def make_a_move(col, board, player):
    row = get_first_available_row(board,col)
    board[row,col] = player
    return board
def get_first_available_row(board,col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r
def someone_won(board, player):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
def allowed_here(board, col):
        if board[ROWS-1,col] == 0:
            return True
        return False
def get_score_for_this_position(player, board):
    score = 0
    # Center cols is preferred
    score += get_C_score_for_this_position(player, board)
    # Horizontal
    score += get_H_score_for_this_position(player, board)
    # Vertical
    score += get_V_score_for_this_position(player, board)
    # P slop
    score += get_P_score_for_this_position(player, board)
    # N slop
    score += get_N_score_for_this_position(player, board)
    return score
def get_C_score_for_this_position(player, board):
    score = 0    
    center_col = board[:,COLS//2]
    score +=list(center_col).count(player) * 2
    return score
def get_H_score_for_this_position(player, board):
    score = 0
    for r in range(ROWS):
        row = board[r,:]
        for c in range(COLS-3):
            line = row[c:c+LINE_SIZE]
            score += give_score_to_line(list(line), player)
    return score
def get_V_score_for_this_position(player, board):
    score = 0
    for c in range(COLS):
        col = board[:,c]
        for r in range(ROWS-3):
            line = col[r:r+LINE_SIZE]
            score += give_score_to_line(list(line), player)
    return score
def get_P_score_for_this_position(player, board):
    score = 0
    for c in range(COLS-3):
        for r in range(ROWS-3):
            line = [board[r+i][c+i] for i in range(LINE_SIZE)]
            score += give_score_to_line(list(line), player)
    return score
def get_N_score_for_this_position(player, board):
    score = 0
    for c in range(COLS-3):
        for r in range(ROWS-3):
            line = [board[r+3-i][c+i] for i in range(LINE_SIZE)]
            score += give_score_to_line(list(line), player)
    return score    
def give_score_to_line(line, player):
    score = 0
    if player == PLAYER:
        opp = AI
    else:
        opp = PLAYER
    if line.count(player) == 4:
        score += 150
    elif line.count(player) == 3 and line.count(FREE) == 1:
        score += 7
    elif line.count(player) == 2 and line.count(FREE) == 2:
        score += 3
    elif line.count(opp) == 3 and line.count(FREE) == 1:
        score -= 5
    return score
def all_allowed_positions(board):
    allowed_cols = []
    for c in range(COLS):
        if allowed_here(board, c):
            allowed_cols.append(c)
    return allowed_cols
def minMax (board, alpha, beta, depth, condition):    
    newCondition = not (condition)
    if condition == True:
        player= AI
        value = -math.inf
    else:
        player = PLAYER
        value = math.inf        
    if someone_won(board, AI):
        return (None, 99999999999999)
    elif someone_won(board, PLAYER):
        return (None, -99999999999999)
    elif len(all_allowed_positions(board)) == 0:
        GAME_OVER = True
        return(None,0)        
    elif depth == 0:
        return (None, get_score_for_this_position(AI, board))    
    validLocations = all_allowed_positions(board)   
    retCol = random.choice(validLocations)
    for col in validLocations:
        boardCopy = board.copy()
        boardCopy = make_a_move(col, boardCopy,player) 
        newValue = minMax(boardCopy, alpha , beta , depth-1 , newCondition)[1]  
        if condition == True :
            if newValue > value :
                value = newValue
                retCol = col 
            alpha = max(alpha,value)
        else :
            if newValue < value :
                value = newValue
                retCol = col 
            beta = min (beta,value)
        if alpha >= beta:
            break
    return retCol,value
mode = int(input("Please Choose Game Mode:\n-Player Vs Player (Same Game) Press 1\n-Player Vs Player (Server Based) Press 2\n-Player Vs AI (Same Game) Press 3\n-AI Vs AI (Server Based) Press 4\n"))
if mode == 1 or mode == 3:
    loadFlag= input("Do you want to load a game you already exists y/n: ")
    if loadFlag == 'y':
        fileToLoad= input("Please enter the game name: ")
        board, difficulty, TURN = load (fileToLoad)
        print_board_up_right(board)

    else:
        if mode == 3:
            difficulty = int(input("Please Enter Desired Level Of Difficulty 1-5: "))  
        board = make_board_with_dim(ROWS,COLS)
        print_board_up_right(board)
else:
    if mode == 4:
        difficulty = int(input("Please Enter Desired Level Of Difficulty 1-5: "))  
    board = make_board_with_dim(ROWS,COLS)
    print_board_up_right(board)
    
while(not GAME_OVER) and (mode == 1 or mode == 3):
    if TURN == PLAYER_TURN:
        inp = input("PLEASE ENTER A COL 6-0 TO PLAY OR SAVE TO SAVE: ")
        if inp == "SAVE":
            name = input("Please choose a name for your game: ")
            save(board,name, difficulty, TURN)
            GAME_OVER = True
            break
        else:    
            col = int(inp)
            if allowed_here(board, col):
                board = make_a_move(col, board, PLAYER)
                print_board_up_right(board)
                if someone_won(board, PLAYER):
                    GAME_OVER = True
                    print("Player1 Won")
                TURN += 1
                TURN %= 2
    elif TURN == AI_TURN and not GAME_OVER:
        if mode == 1:
            inp = input("PLEASE ENTER A COL 6-0 TO PLAY OR SAVE TO SAVE: ")
            if inp == "SAVE":
                name = input("Please choose a name for your game: ")
                save(board,name, difficulty, TURN)
                GAME_OVER = True
                break
            else:    
                col = int(inp)
                if allowed_here(board, col):
                    board = make_a_move(col, board, AI)
                    print_board_up_right(board)
                    if someone_won(board, AI):
                        GAME_OVER = True
                        print("Player2 Won")
                    TURN += 1
                    TURN %= 2
        elif mode == 3:
            col, score = minMax (board, -math.inf, math.inf,difficulty, True)
            if allowed_here(board, col):
                board = make_a_move(col, board, AI)
                print_board_up_right(board)
                if someone_won(board, AI):
                    GAME_OVER = True
                    print("AI Won")
                TURN += 1
                TURN %= 2   
if(not GAME_OVER) and (mode == 2 or mode == 4):
    ###########

    file = open("ClientConfig.txt",'r')
    host = file.readline()
    host = host[:len(host)-1]
    #print(host)
    port = int(file.readline())  # initiate port no above 1024
    #print(port)
    file.close()

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = ""  # take input
    turn = int(client_socket.recv(1024).decode())# receive response
    print(turn)
    if turn == 0:
        TURN = AI_TURN
    else:
        TURN = PLAYER_TURN

    x = 0

    while message.lower().strip() != 'bye':
        if TURN == AI_TURN  :
            ## ana hal3b
            #########take move############
            #move = input("put move here")
            if mode == 2:
                col = int(input("PLEASE ENTER A COL 6-0 TO PLAY: "))
                if allowed_here(board, col):
                    board = make_a_move(col, board, AI)
                    print_board_up_right(board)
                    if someone_won(board, AI):
                        GAME_OVER = True
                        print("I Won")
                    TURN += 1
                    TURN %= 2
            elif mode == 4:    
                col, score = minMax (board, -math.inf, math.inf,difficulty, True)
                if allowed_here(board, col):
                    board = make_a_move(col, board, AI)
                    print_board_up_right(board)
                    if someone_won(board, AI):
                        GAME_OVER = True
                        print("I Won")
                    TURN += 1
                    TURN %= 2
            move = str(col)
            client_socket.send(move.encode())
        elif TURN == PLAYER_TURN:
            ## ana hast2bl
            move = client_socket.recv(1024).decode()
            #print('Received from server: ' + move)  # show in terminal
            col = int(move)
            if allowed_here(board, col):
                board = make_a_move(col, board, PLAYER)
                print_board_up_right(board)
                if someone_won(board, PLAYER):
                    GAME_OVER = True
                    print("Opponent Won")
                TURN += 1
                TURN %= 2

        #client_socket.send(message.encode())  # send message
        #move = client_socket.recv(1024).decode()  # receive response

        #print('Received from server: ' + move)  # show in terminal
        if not GAME_OVER:
            message = "not bye"  # again take input
        else:
            message = "bye"  # again take input

    client_socket.close()  # close the connection



    ##############
q = input("Press q to exit")

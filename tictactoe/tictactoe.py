"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def count(board):
    counter={X:0,O:0,EMPTY:0}
    for row in board:
        for cell in row:
            counter[cell] += 1

    return counter



def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    else:
        counter=count(board)
        if counter[X]>counter[O]:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves=set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    dup = copy.deepcopy(board)
    turn = player(board)
    i=action[0]
    j=action[1]
    if dup[i][j] != EMPTY:
        raise Exception("Cell is already filled.")
    else:
        dup[i][j] = turn
        return dup


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if player(board)==X:
        prev_turn = O
    else:
        prev_turn = X

    for i in range(len(board)):
        check1=check2=check3=check4=True
        for j in range(len(board)):
            #Row Check
            if board[i][j] != prev_turn:
                check1=False

            #Column Check
            if board[j][i] != prev_turn:
                check2=False

            #Diagonal Check
            if board[j][j] != prev_turn:
                check3=False

            #Anti-Diagnal Check
            if board[j][len(board)-1-j] != prev_turn:
                check4=False
                
        #If any one condition is satisified, return the winner
        if check1|check2|check3|check4:
            return prev_turn
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #If game is won
    if winner(board) != None:
        return True
    #If board is filled
    elif count(board)[EMPTY] == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board,alpha,beta):
    """
    Returns the maximum utility value of the board
    """
    if terminal(board):
        return utility(board)
    else:
        v = -math.inf
        for action in actions(board):
            v = max(v,min_value(result(board,action),alpha,beta))
            if v >= beta:
                return v
            alpha = max(alpha,v)
        return v


def min_value(board,alpha,beta):
    """
    Returns the minimum utility value of the board
    """
    if terminal(board):
        return utility(board)
    else:
        v = math.inf
        for action in actions(board):
            v = min(v,max_value(result(board,action),alpha,beta))
            if v <= alpha:
                return v
            beta = min(beta,v)
        return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            v = max_value(board,-math.inf,math.inf)
            for action in actions(board):
                if min_value(result(board,action),-math.inf,math.inf) == v:
                    return action

        else:
            v = min_value(board,-math.inf,math.inf)
            for action in actions(board):
                if max_value(result(board,action),-math.inf,math.inf) == v:
                    return action
                    
            
        


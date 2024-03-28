"""
Tic Tac Toe Player
"""
import copy
import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    init = False
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            if board[i][j] == O:
                o += 1
        if EMPTY in board[i]:
            init = True
    if init != True:
        return 'no more moves'
    elif x == o:
        return X
    else:
        return O


def actions(board):
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i, j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    my_board = copy.deepcopy(board)
    if action == (None, None):
        return board
    elif action in actions(board):
        i = action[0]
        j = action[1]
        my_board[i][j] = player(board)
        return my_board


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) == None:
        for row in board:
            if EMPTY in row:
                return False
        else:
            return True
    else:
        return True


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Define the possible winning combinations of three symbols
    win_combos = [
        # Horizontal rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        # Vertical columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    # Check if any of the winning combinations has three Xs
    if [X, X, X] in win_combos:
        # Return X as the winner
        return X
    # Check if any of the winning combinations has three Os
    elif [O, O, O] in win_combos:
        # Return O as the winner
        return O
    # Otherwise, there is no winner
    else:
        return None


def max_value(board):
    if terminal(board):
        return utility(board)

    best = -float("inf")
    for action in actions(board):
        new_board = result(board, action)
        v_max = min_value(new_board)
        best = max(best, v_max)
    return best


def min_value(board):
    if terminal(board):
        return utility(board)

    best = float("inf")
    for action in actions(board):
        new_board = result(board, action)
        v_min = max_value(new_board)
        best = min(best, v_min)
    return best


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get the winner of the game
    win_symbol = winner(board)
    # Return the corresponding utility value
    if win_symbol == X:
        return 1
    elif win_symbol == O:
        return -1
    else:
        return 0

def minimax(board):
    best_X = -float('inf')
    best_O = float('inf')
    if terminal(board) != True:
        if player(board) == X:
            for action in actions(board):
                new_board = result(board,action)
                value = min_value(new_board)
                if value > best_X:
                    best_X = value
                    move = action
            return move
        else:
            for action in actions(board):
                new_board = result(board,action)
                value = max_value(new_board)
                if value < best_O:
                    best_O = value
                    move = action
            return move


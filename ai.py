import random
import itertools
import copy
from checkers import Piece
from checkers import Board
import string

def allowed_moves(board, color):
    b = Board(8)
    initialize(b, board)
    if color == 'b':
        color = 'black'
    else:
        color = 'white'
    hints = get_hints(b, color)
    hints = convert_positions(hints)
    return(hints)

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """
    moves = allowed_moves(board, color)

    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py

    b = Board(8)
    initialize(b, board)
    if color == 'b':
        turn = 'black'
    else:
        turn = 'white'
    choice = get_next_move(b, turn)
    choice = list(choice)
    for i in range(0, len(choice)):
        choice[i] = indexify(choice[i])
    return choice


def convert_positions(l):
    """
    Use ascii tables to convert alphabetic and numeric strings (moves and jumps) into coordinates.
    return list of tuples
    """
    l = list(l)
    l = [x for x in l if x != []]
    l = l[0]

    for i in range(0, len(l)):
        l[i] = list(l[i])
    for i in range(0, len(l)):
        if l[i]:
            for j in range(0, len(l[i])):
                l[i][j] = indexify(l[i][j])
    return l

def get_moves(board, row, col, is_sorted = False):
    """
    This function returns moves for a given single piece at row,col position.
    This function returns a list of valid moves in terms of string positions,
    like 'a1', 'b4' etc. The rules are follows:
        a. All the move(s) must be inside the board.
        b. If the given row, col position has no piece (i.e. empty), this
            function returns an empty list.
        c. If the piece is not a king then it will return a list of at most
            two diagonal positions. For a black piece, the diagonals will be
            bottom-left and bottom-right. For a white, they will be top-left
            and top-right.
        d. If the piece is a king, then it will return a list of at most
            four diagonal positions. Irrespective of color, the diagonals
            will be bottom and top, left and right.
        e. By default, is_sorted flag is set to False, if it's True then
            the final returning list must be sorted. Remember that the list
            is a list of string positions.
    """
    down, up = [(+1, -1), (+1, +1)], [(-1, -1), (-1, +1)]
    length = board.get_length()
    piece = board.get(row, col)
    if piece:
        bottom = [ deindexify(row + x, col + y) for (x, y) in down \
                      if (0 <= (row + x) < length) \
                          and (0 <= (col + y) < length) \
                          and board.is_free(row + x, col + y)]
        top = [ deindexify(row + x, col + y) for (x, y) in up \
                   if (0 <= (row + x) < length) \
                       and (0 <= (col + y) < length) \
                       and board.is_free(row + x, col + y)]
        return (sorted(bottom + top) if piece.is_king() else \
                (sorted(bottom) if piece.is_black() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_black() else top))
    return []

def get_jumps(board, row, col, is_sorted = False):
    """
    This function is very similar to the get_moves() function. This function
    lists all the capture for a single piece on the board located at the row,
    col position. To capture the piece needs to "jump". A checker may move
    more than one space if they can jump one of the opponent's checker pieces
    which is located immediately in their diagonal vicinity and onto a free
    space. This function returns a list of valid captures in terms of string
    positions, like 'a1', 'b4' etc. The rules are follows:
        a. All the captures(s) must be inside the board.
        b. If the given row, col position has no piece (i.e. empty), this
            function returns an empty list.
        c. To make a jump, there must be an opponent piece on the immediate
            diagonal.
        d. If the piece is not a king then it will return a list of at most
            two diagonal positions. For a black piece, the diagonals will be
            bottom-left and bottom-right.
        e. If the piece is a king, then it will return a list of at most
            four diagonal positions. Irrespective of color, the diagonals
            will be bottom and top, left and right.
        f. By default, is_sorted flag is set to False, if it's True then
            the final returning list must be sorted. Remember that the list
            is a list of string positions.
    """
    down, up = [(+1, -1), (+1, +1)], [(-1, -1), (-1, +1)]
    length = board.get_length()
    piece = board.get(row, col)
    if piece:
        bottom = \
            [ deindexify(row + 2 * x, col + 2 * y) for (x, y) in down \
             if (0 <= (row + 2 * x) < length) \
                 and (0 <= (col + 2 * y) < length) \
                 and board.is_free(row + 2 * x, col + 2 * y) \
                 and (not board.is_free(row + x, col + y)) \
                 and (board.get(row + x, col + y).color() != piece.color())]
        top = \
            [ deindexify(row + 2 * x, col + 2 * y) for (x, y) in up \
             if (0 <= (row + 2 * x) < length) \
                 and (0 <= (col + 2 * y) < length) \
                 and board.is_free(row + 2 * x, col + 2 * y) \
                 and (not board.is_free(row + x, col + y)) \
                 and (board.get(row + x, col + y).color() != piece.color())]
        return (sorted(bottom + top) if piece.is_king() else \
                (sorted(bottom) if piece.is_black() else sorted(top))) \
                    if is_sorted else (bottom + top if piece.is_king() else \
                                       (bottom if piece.is_black() else top))
    return []

def search_path(board, row, col, path, paths, is_sorted = False):
    """
    This function recursive builds all capturing paths started at a certain
    row/col position.
    """
    path.append( deindexify(row, col))
    jumps = get_jumps(board, row, col, is_sorted)
    if not jumps:
        paths.append(path)
    else:
        for position in jumps:
            (row_to, col_to) =  indexify(position)
            piece = copy.copy(board.get(row, col))
            board.remove(row, col)
            board.place(row_to, col_to, piece)
            if (piece.color() == 'black' \
                and row_to == board.get_length() - 1) \
                    or (piece.color() == 'white' \
                        and row_to == 0) \
                            and (not piece.is_king()):
                                piece.turn_king()
            row_mid = row + 1 if row_to > row else row - 1
            col_mid = col + 1 if col_to > col else col - 1
            capture = board.get(row_mid, col_mid)
            board.remove(row_mid, col_mid)
            search_path(board, row_to, col_to, copy.copy(path), paths)
            board.place(row_mid, col_mid, capture)
            board.remove(row_to, col_to)
            board.place(row, col, piece)

def get_captures(board, row, col, is_sorted = False):
    """
    This function finds all capturing paths started at a certain row/col
    position on the board. If there is no capture from the given row/col,
    this function will return an empty list [].
    """
    paths = []
    board_ = copy.copy(board)
    search_path(board_, row, col, [], paths, is_sorted)
    if len(paths) == 1 and len(paths[0]) == 1:
        paths = []
    return paths

def indexify(position):
    """
Use ascii tables to convert alphabetic and numeric strings into coordinates.
    use the ord and int
return tuple
    """
    return (ord(position[0])-ord('a'),int(position[1:])-1)

def deindexify(row, col):
    """
Use ascii tables to convert coordinates to strings.
    use the ord and str
return string
    """
    return chr(row+97)+str(col+1)

def initialize(board, b):
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
    for r in range(0, row):
        for c in range(0, col):
            if b[r][c] == 'w':
                board.place(r, c, Piece('white'))
            if b[r][c] == 'b':
                board.place(r, c, Piece('black'))
            if b[r][c] == 'W':
                board.place(r, c, Piece('white', True))
            if b[r][c] == 'B':
                board.place(r, c, Piece('black', True))

def count_pieces(board):
    """
Counts the total number of black and white pieces on the board.
    use two for loop and three if
return tuple of black and white
    """
    row = col = board.get_length()
    black, white = 0, 0
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.is_black():
                    black += 1
                if piece.is_white():
                    white += 1
    return (black, white)

def get_all_moves(board, color, is_sorted = False):
    """
Get all the positions of all the pieces on the board that can be moved.
    use three for loop and three if
return list of all move
    """
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_moves(board, r, c, is_sorted)
                    path_start = deindexify(r, c)
                    for path in path_list:
                        final_list.append((path_start, path))

    if is_sorted == True:
        final_list.sort()
    return final_list

def sort_captures(all_captures,is_sorted=False):
    '''If is_sorted flag is True then the final list will be sorted by
    the length of each sub-list and the sub-lists with the same length
    will be sorted again with respect to the first item in corresponding
    the sub-list, alphabetically.'''

    return sorted(all_captures, key = lambda x: (-len(x), x[0]))\
    if is_sorted else all_captures

def get_all_captures(board, color, is_sorted = False):
    """
Get the probability that all the pieces on the board can jump.
    use three for loop and two if
return sort_captures list
    """
    row = col = board.get_length()
    final_list = []
    for r in range(row):
        for c in range(col):
            piece = board.get(r, c)
            if piece:
                if piece.color() == color:
                    path_list = get_captures(board, r, c, is_sorted)
                    for path in path_list:
                        final_list.append(path)
    return sort_captures(final_list, is_sorted)

def get_hints(board, color, is_sorted = False):
    """
Use movement and jump to get all the possibilities.
    use the get_all_moves and get_all_captures
return tuple of move and jump
    """
    move = get_all_moves(board, color, is_sorted)
    jump = get_all_captures(board, color, is_sorted)
    if jump:
        return ([], jump)
    else:
        return (move, jump)

def apply_move(board, move):
    """
Performs actual operations and moves that move the specified pieces.
    use the if and piece and board class
No return

    Raise this exception below:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.")
    If,
        a. there is no move from move[0], i.e. use get_moves() function
        to get all the moves from move[0]
        b. the destination position move[1] is not in the moves list found
            from get_moves() function.
    """
    row,col = indexify(move[0])
    row_end,col_end = indexify(move[1])
    path_list = get_moves(board, row, col, is_sorted = False)

    if move[1] in path_list:
        piece = board.get(row, col)
        if piece.is_black() and row_end == board.get_length()-1 \
        or piece.is_white() and row_end == 0:
            piece.turn_king()
        board.remove(row, col)
        board.place(row_end, col_end, piece)
    else:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.")

def apply_capture(board, capture_path):
    """
Performs actual operations and jumps to move the specified pieces.
    use one while loop and one if
No return

    Raise this exception below:
        raise RuntimeError("Invalid jump/capture, please type" \
                         + " \'hints\' to get suggestions.")
    If,
        a. there is no jump found from any position in capture_path, i.e. use
            get_jumps() function to get all the jumps from a certain
            position in capture_path
        b. the destination position from a jump is not in the jumps list found
            from get_jumps() function.
    """
    counter = 0
    while counter < len(capture_path)-1:
        path = [capture_path[counter], capture_path[counter + 1]]
        counter += 1
        row,col = indexify(path[0])
        row_end,col_end = indexify(path[1])
        path_list = get_jumps(board, row, col, is_sorted = False)

        if path[1] in path_list:
            piece = board.get(row, col)
            if piece.is_black() and row_end == board.get_length()-1 \
            or piece.is_white() and row_end == 0:
                piece.turn_king()
            board.remove(row, col)
            row_eat, col_eat = max(row, row_end)-1, max(col, col_end)-1
            board.remove(row_eat, col_eat)
            board.place(row_end, col_end, piece)
        else:
            raise RuntimeError("Invalid jump/capture, please type" \
                             + " \'hints\' to get suggestions.")


def heuristics(state):
    """
    This is the heuristics function. This function calculates these metrics:
        a. Normalized utility values from the number of pawn and king pieces
            on the board. [0.32, -0.32]
        b. Normalized utility values from the number of captures could be made
            by kings and pawns. [0.96, -0.96]
        c. Normalized utility values from the distances of pawns to become
            kings. [0.70, -0.70]
        d. Normalized utility values from the number of pieces on the safer
            places on the board. [0.19, -0.19]
    """
    board = state[0]
    turn = state[1]
    length = board.get_length()
    bp, wp = 0, 0
    bk, wk = 0, 0
    bc, wc = 0, 0
    bkd, wkd = 0, 0
    bsd, wsd = 0.0, 0.0
    for row in range(length):
        for col in range(length):
            piece = board.get(row, col)
            if piece:
                r = row if row > (length - (row + 1)) else (length - (row + 1))
                c = col if col > (length - (col + 1)) else (length - (col + 1))
                d = int(((r ** 2.0 + c ** 2.0) ** 0.5) / 2.0)
                if piece.color() == 'black':
                    bc += sum([len(v) for v in \
                               get_captures(board, row, col)])
                    if piece.is_king():
                        bk += 1
                    else:
                        bp += 1
                        bkd += row + 1
                        bsd += d
                else:
                    wc += sum([len(v) for v in \
                               get_captures(board, row, col)])
                    if piece.is_king():
                        wk += 1
                    else:
                        wp += 1
                        wkd += length - (row + 1)
                        wsd += d
    if turn == 'black':
        black_count_heuristics = \
                3.125 * (((bp + bk * 2.0) - (wp + wk * 2.0)) \
                    / 1.0 + ((bp + bk * 2.0) + (wp + wk * 2.0)))
        black_capture_heuristics = 1.0417 * ((bc - wc)/(1.0 + bc + wc))
        black_kingdist_heuristics = 1.429 * ((bkd - wkd)/(1.0 + bkd + wkd))
        black_safe_heuristics = 5.263 * ((bsd - wsd)/(1.0 + bsd + wsd))
        return black_count_heuristics + black_capture_heuristics \
                    + black_kingdist_heuristics + black_safe_heuristics
    else:
        white_count_heuristics = \
                3.125 * (((wp + wk * 2.0) - (bp + bk * 2.0)) \
                    / 1.0 + ((bp + bk * 2.0) + (wp + wk * 2.0)))
        white_capture_heuristics = 1.0416 * ((wc - bc)/(1.0 + bc + wc))
        white_kingdist_heuristics = 1.428 * ((wkd - bkd)/(1.0 + bkd + wkd))
        white_safe_heuristics = 5.263 * ((wsd - bsd)/(1.0 + bsd + wsd))
        return white_count_heuristics + white_capture_heuristics \
                    + white_kingdist_heuristics + white_safe_heuristics

def is_terminal(state, maxdepth = None):
    """
    Determines if a tree node is a terminal or not.
    Returns boolean True/False.
    """
    board = state[0]
    turn = state[1]
    depth = state[2]
    (moves, captures) = get_hints(board, turn)
    if maxdepth is not None:
        return ((not moves) and (not captures)) or depth >= maxdepth
    else:
        return ((not moves) and (not captures))

def utility(state):
    """
    This function computes the utility of a node, if that is
    a terminal node.
    """
    return heuristics(state)

def transition(state, action, ttype):
    """
    This is the transition function. Given a board state and action,
    it transitions to the next board state.
    """
    board = copy.deepcopy(state[0])
    turn = state[1]
    depth = state[2]
    if ttype == "move":
        apply_move(board, action)
    elif ttype == "jump":
        apply_capture(board, action)
    turn = 'white' if state[1] == 'black' else 'black'
    depth += 1
    return (board, turn, depth)

def maxvalue(state, maxdepth, alpha = None, beta = None):
    """
    The maxvalue function for the adversarial tree search.
    """
    board = state[0]
    turn = state[1]
    if is_terminal(state, maxdepth):
        return utility(state)
    else:
        v = float('-inf')
        (moves, captures) = get_hints(board, turn)
        if captures:
            for a in captures:
                v = max(v, minvalue(transition(state, a, "jump"), \
                        maxdepth, alpha, beta))
                if alpha is not None and beta is not None:
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v
        elif moves:
            for a in moves:
                v = max(v, minvalue(transition(state, a, "move"), \
                        maxdepth, alpha, beta))
                if alpha is not None and beta is not None:
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

def minvalue(state, maxdepth, alpha = None, beta = None):
    """
    The minvalue function for the adversarial tree search.
    """
    board = state[0]
    turn = state[1]
    if is_terminal(state, maxdepth):
        return utility(state)
    else:
        v = float('inf')
        (moves, captures) = get_hints(board, turn)
        if captures:
            for a in captures:
                v = min(v, maxvalue(transition(state, a, "jump"), \
                                     maxdepth, alpha, beta))
                if alpha is not None and beta is not None:
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v
        elif moves:
            for a in moves:
                v = min(v, maxvalue(transition(state, a, "move"), \
                                     maxdepth, alpha, beta))
                if alpha is not None and beta is not None:
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

def minimax_search(state, maxdepth = None):
    """
    The depth limited minimax tree search.
    """
    board = state[0]
    turn = state[1]
    (moves, captures) = get_hints(board, turn)
    if captures:
        return max([(a, minvalue(transition(state, a, "jump"), maxdepth)) \
                        for a in captures], key = lambda v: v[1])
    elif moves:
        return max([(a, minvalue(transition(state, a, "move"), maxdepth)) \
                        for a in moves], key = lambda v: v[1])
    else:
        return ("pass", -1)

def alphabeta_search(state, maxdepth = None):
    """
    The depth limited alpha-beta tree search, it's 2-times faster than
    the minimax search.
    """
    board = state[0]
    turn = state[1]
    (moves, captures) = get_hints(board, turn)
    alpha = float('-inf')
    beta = float('inf')
    if captures:
        return max([\
            (a, minvalue(transition(state, a, "jump"), \
                         maxdepth, alpha, beta)) \
                             for a in captures], key = lambda v: v[1])
    elif moves:
        return max([\
            (a, minvalue(transition(state, a, "move"), \
                         maxdepth, alpha, beta)) \
                             for a in moves], key = lambda v: v[1])
    else:
        return ("pass", -1)

def get_next_move(board, turn):
    """
    Use the AI to get the next best move.
    Takes almost 6 seconds to find a move.
    """
    state = (board, turn, 0)
    print("Thinking ...")
    #move = minimax_search(state, 6) # slow
    move = alphabeta_search(state, 6) # fast
    return move[0]

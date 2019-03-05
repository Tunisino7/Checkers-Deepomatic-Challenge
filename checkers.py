class Board(object):
    
    def __init__(self, length = 8):
        """
        The default size of the board is 8x8. It allocates the cells according
        to the given length of the board. i.e. It will create a NxN list of
        lists of None if the provided length is N.
        """
        if length > 1:
            self._length = length  # the length of the board
            # running a loop to build a 2D list into cell
            # (i.e. list of lists)
            self._cell = [[None for c in range(self._length)] \
                                for r in range(self._length)]
        else:
            raise ValueError("The minimum allowed length of a board is 2.")

    def get_length(self):
        """
        Returns the length of the board.
        """
        return self._length

    def get_cells(self):
        """
        Returns the cells in the board.
        """
        return self._cell

    def is_free(self, row, col):
        """
        Resturns True if the given position (i.e. tuple) is free.
        """
        return self._cell[row][col] is None

    def place(self, row, col, piece):
        """
        Places a piece at the position given by the row-column index.
        This does not check any validity condition.
        """
        self._cell[row][col] = piece

    def get(self, row, col):
        """
        Gets the piece located at the position indexed by the row-column value.
        Does not check any validity condition.
        """
        return self._cell[row][col]

    def remove(self, row, col):
        """
        Removes a piece from the position given by the row-column index.
        This does not check any validity condition.
        """
        self._cell[row][col] = None

    def is_empty(self):
        """
        Returns True if the whole board is empty.
        """
        for r in range(self._length):
            for c in range(self._length):
                if not self.is_free(r,c):
                    return False
        return True

    def is_full(self):
        """
        Returns True if the whole board is filled up.
        """
        for r in range(self._length):
            for c in range(self._length):
                if self.is_free(r, c):
                    return False
        return True

    def display(self, count = None):
        """
        Displays the board, if a count of black and white pieces (in a tuple)
        is provided, it will show the counts at the bottom.
        """
        print(self)
        if count is not None:
            print("  Black: {:d}, White: {:d}"\
                  .format(count[0], count[1]))

    def __str__(self):
        """
        The string representation of the board.
        """
        vline = '\n' + (' ' * 2) + ('+---' * self._length) + '+' + '\n'
        numline = ' '.join([(' ' + str(i) + ' ') \
                            for i in range(1, self._length + 1)])
        str_ = (' ' * 3) + numline + vline
        for r in range(0, self._length):
            str_ += chr(97 + r) + ' |'
            for c in range(0, self._length):
                str_ += ' ' + \
                    (str(self._cell[r][c]) \
                         if self._cell[r][c] is not None else ' ') + ' |'
            str_ += vline
        return str_

    def __repr__(self):
        """
        Function for the REPL printing.
        """
        return self.__str__()

class Piece(object):
    """
    This class encapsulates a Piece object. In the Checkers game a piece is
    a small piece which is colored black on once side and white on the other.
    """

    """ The symbols for the pieces: black and white circles. """
    symbols = ['b', 'w']

    # the flag to denote if a piece is a king
    _is_king = False
    symbols_king = ['B', 'W']

    def __init__(self, color = 'black', is_king = False):
        """
        The default color is always black, i.e. 'black'.
        """
        if color.isalpha():
            color = color.lower()
            if color == 'black' or color == 'white':
                self._color = color
                self._is_king  = is_king
            else:
                raise ValueError("A piece must be \'black\' or \'white\'.")
        else:
            raise ValueError("A piece must be \'black\' or \'white\'.")

    def color(self):
        """
        Returns the color of the piece.
        """
        return self._color

    def is_black(self):
        """
        Returns a boolean True if the piece is black.
        """
        return self._color == 'black'

    def is_white(self):
        """
        Returns a boolean True if the piece is white.
        """
        return self._color == 'white'

    def is_king(self):
        """
        Returns a boolean True if the piece is a king.
        """
        return self._is_king


    def turn_king(self):
        """
        Turns this piece into a king from pawn.
        """
        self._is_king = True

    def turn_pawn(self):
        """
        Turns this piece from king to pawn.
        """
        self.is_king = False

    def __str__(self):
        """
        String represetation of a piece.
        """
        if self._is_king:
            return self.symbols_king[0] if self._color == 'black' \
                        else self.symbols_king[1]
        else:
            return self.symbols[0] if self._color == 'black' \
                        else self.symbols[1]

    def __repr__(self):
        """
        The function for the REPL printing.
        """
        return self.__str__()

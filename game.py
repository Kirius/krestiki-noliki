# coding=utf-8
import random
from itertools import chain
import copy


def memo(f):
    cache = {}

    def _f(*args):
        if args in cache:
            return cache[args]
        cache[args] = f(*args)
        return cache[args]

    return _f


class GiveUp(BaseException):
    pass


class Board(object):
    """
    Represents a board for the game.
    """
    empty_mark = ' '

    def __init__(self, size=3, init_board=None):

        self.size = size
        if init_board is None:
            self.board = [[self.empty_mark] * size for _ in range(size)]
        else:
            self.board = init_board

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return '\n' + '\n'.join(str(line) for line in self.board) + '\n'

    def copy(self):
        return Board(self.size, copy.deepcopy(self.board))

    def check_move(self, x, y):
        """
        Returns True if the move is valid
        and False otherwise.
        """
        try:
            if x < 0 or y < 0:
                # accept only positive coordinates
                return False
            return self.board[x][y] == self.empty_mark
        except (TypeError, IndexError):
            return False

    def move(self, x, y, mark):
        """
        Tries to perform move.
        Mutates self and returns it on success.
        Returns False on failure.
        """
        if self.check_move(x, y):
            self.board[x][y] = mark
            return self
        return False

    def get_all_moves(self):
        """
        Returns list of all valid moves (ex. [(1,2), (2,3)])
        """
        size = range(self.size)
        return [(x, y) for x in size for y in size
                if self.board[x][y] == self.empty_mark]

    def won(self):
        """
        Returns True if any player won.
        (filled horizontal, vertical or diagonal lines).
        """
        size = range(self.size)
        # chain horizontal, vertical and diagonal lines in 1 iterable
        lines = chain(self.board,
                      zip(*self.board),
                      [[self.board[i][j] for i in size for j in size if i == j]],
                      [[self.board[i][self.size - j - 1] for i in size for j in size if i == j]])
        # returns True if there is a line which completely filled in by one of the players
        return any(line[0] != self.empty_mark
                   and line.count(line[0]) == self.size for line in lines)

    def finished(self):
        """
        Checks if a game has finished.
        Returns 1 if someone won, 2 if a draw, 0 if game continues
        """
        if self.won():
            return 1
        if any(cell == self.empty_mark for row in self.board for cell in row):
            # empty cell(s) is present
            return 0
        # nobody won and no empty cells left => draw
        return 2


class Player(object):
    """
    Represents a player for the game.
    """
    def __init__(self, id, mark, strategy):
        self.id = id
        self.mark = mark
        self.strategy = strategy


class Game(object):
    """
    Represents a game.
    """
    def __init__(self, strategy1, strategy2, board_size=3):
        self._active = Player(id=1, mark='x', strategy=strategy1)
        self._passive = Player(id=2, mark='o', strategy=strategy2)
        self._board = Board(size=board_size)

    def _switch_turn(self):
        self._active, self._passive = self._passive, self._active

    def play(self):
        """
        Call this method to start a game.
        Returns winner id or 0 if a draw.
        """
        while True:
            print '\n########################################\n'
            print self._board
            print "Player's %s turn" % self._active.id
            try:
                x, y = self._active.strategy(self._board, self._active.mark)
            except GiveUp:
                print '\nPlayer %s gave up :(' % self._active.id
                print 'Player %s won!!!' % self._passive.id
                return self._passive.id
            if not self._board.move(x, y, self._active.mark):
                print "Don't even try to cheat!"
                print 'Player %s won' % self._passive.id
                return self._passive.id
            res = self._board.finished()
            if res == 1:
                print self._board
                print 'Player %s won!!!' % self._active.id
                return self._active.id
            elif res == 2:
                print self._board
                print 'A draw!!!'
                return 0
            else:
                self._switch_turn()


def manual_strategy(board, *args):
    """
    This strategy will ask you to play.
    """
    while True:
        try:
            coord = raw_input("Enter cell coordinates ex. 1,3 (or press Ctrl+C to give up):\n>> ")
            x, y = map(lambda num: int(num) - 1, coord.split(','))
            if board.check_move(x, y):
                return x, y
            else:
                print "Not a valid move!"
        except KeyboardInterrupt:
            raise GiveUp
        except BaseException:
            print "Not a valid coordinates!"


def random_strategy(board, *args):
    """
    This strategy will chose moves randomly.
    """
    return random.choice(board.get_all_moves())


def minimax_strategy(board, mark, *args):
    """
    This strategy will play optimally.
    """
    next_mark = {'x': 'o', 'o': 'x'}

    @memo
    def utility(board, mark, max_player):
        res = board.finished()
        if res == 1:
            return -1 if max_player else 1
        elif res == 2:
            return 0
        else:
            f = max if max_player else min
            return f(utility(board.copy().move(x, y, mark), next_mark[mark], not max_player)
                     for x, y in board.get_all_moves())

    def move_utility(coord):
        return utility(board.copy().move(*coord, mark=mark), next_mark[mark], False)

    return max(board.get_all_moves(), key=move_utility)


def input(input_msg, error_msg, validate):
    """
    Helper function to get user input.
    """
    while True:
        string = raw_input(input_msg)
        if validate(string):
            return string
        print error_msg


def main():
    """
    Setups and plays games.
    """
    strategies = [manual_strategy, random_strategy, minimax_strategy]
    try:
        while True:
            idx1 = input(
                input_msg="Select player 1 (0 - Person, 1 - CPU random donk, 2 - CPU expert):\n>> ",
                error_msg="Incorrect strategy number!",
                validate=lambda s: s in ('0', '1', '2')
            )
            idx2 = input(
                input_msg="Select player 2 (0 - Person, 1 - CPU random donk, 2 - CPU expert):\n>> ",
                error_msg="Incorrect strategy number!",
                validate=lambda s: s in ('0', '1', '2')
            )

            #size = input(
            #    input_msg="Select border size (3 to 7):\n>> ",
            #    error_msg="Incorrect border size!",
            #    validate=lambda s: s in (str(i) for i in range(3, 8))
            #)
            size = 3
            g = Game(strategies[int(idx1)], strategies[int(idx2)], int(size))
            g.play()
            if raw_input("Would you like to play again? (yes/no):\n>> ") == 'no':
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        print "\nThank you for playing this awesome game!"


if __name__ == '__main__':
    main()

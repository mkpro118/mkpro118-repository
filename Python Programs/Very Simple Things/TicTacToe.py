import random
import sys
import time
from itertools import permutations


class TicTacToe:
    '''A simple tic tac toe game, allows the player to play first or second, against the computer'''

    def display(self):
        '''To display the game board. Used recursively to display after every turn.
        This function just improves the readability of the the output, displaying it
        in the traditional 3x3 Tic Tac Toe pattern'''
        x, y = 1, 4
        for i in range(3):
            for j in range(x, y):
                print(self.board[j], "" if y - j == 1 else "|", end="")  # two cases used, one for displaying the boundary
            print('\t', end='')                                      # between two columns
            for i in range(x, y):                                      # and one for the ends
                print(i, "  ", end='')
            x, y = x + 3, y + 3
            print()
        print()

    def win(self, AI):
        '''Partially used for the standard display. The try except
        has been used for the positions where nothing has been
        filled yet. By having the empty positions known, we can
        know when all the spaces are filled which indicates that
        the game is over and then we assign a winner or loser
        based on the criteria of the game.'''
        b = self.board
        try:
            for i in [2, 5, 8]:
                if b[i - 1] == b[i] == b[i + 1] != ' - ':
                    raise Exception
            for i in [4, 5, 6]:
                if b[i - 3] == b[i] == b[i + 3] != ' - ':
                    raise Exception
            if b[1] == b[5] == b[9] != ' - ':
                raise Exception
            if b[3] == b[5] == b[7] != ' - ':
                raise Exception
        except Exception:
            print('{0} Win{1}!'.format('Computer' if AI else 'You', 's' if AI else ''))
            # using the format function I can use just one statement to indicate the winner or loser
            # In some consoles, the console window closes after the program is over, so this timer allows
            # the user to read the result.
            sys.exit()  # used to forcefully exit the game, and not return to the place of function call.
        else:
            ctr = 0
            for i in range(1, 10):
                if self.board[i] == ' - ':
                    ctr += 1
            if ctr == 0:
                print('It\'s a Tie!')
                time.sleep(50)
                sys.exit()

    def mark(self, pos, AI=True):  # used default argument to indicate if the player is AI or human
        self.board[pos] = ' O ' if AI else ' X '
        self.display()  # we first display the board
        self.win(AI)  # then check for winner. We exit the game after a result, and not come back to continue
        self.player() if AI else self.AI()

    def player(self):
        pos = -1  # makes sure that no wrong value can be assigned and removes any prior value
        try:  # used to avoid human errors.
            pos = int(input("Enter position you want to mark as indicated by the layout : "))
            if pos not in list(self.board.keys()):  # to check if the given input is valid
                raise KeyError  # used a special error to identify the type of error
            positions_available = [i for i in range(1, 10) if self.board[i] == ' - ']  # finds and store all possible position which are not already filled
            if pos not in positions_available:  # check if the position to be filled is vacant or not
                raise IndexError
        except KeyError:  # by catching this error, the system knows what the error is and can display the appro
            print('That position doesn\'t exist! Try Again')
            self.player()
        except IndexError:
            print("That spot is already taken! Try Again")
            self.player()
        except ValueError:  # this error is raised by the system itself, and not forcefully raised by the code
            print('Invalid Position! Try Again')
            self.player()
        else:
            self.mark(pos, False)  # the second argument is to indicate it's not the computer playing.

    def AI(self):
        '''A complicated function which basically decides
        where the best position is to play for the computer.
        This function first checks if it's the first time playing.
        If yes, it marks a position randomly.
        Otherwise, it checks in the following order: horizontal, vertical, diagonal
        finding the optimal position to mark in order to win.'''
        print('Opponent\'s Turn')
        print('Thinking', end="")
        for i in range(3):
            time.sleep(0.5)
            print(".", end="")
        print()
        pos = -1
        if self.first_time:
            self.first_time = False
            positions_available = [i for i in range(1, 10) if self.board[i] == ' - ']
            # the first chance is played randomly, as there isn't enough information to calculate the best position
            pos = random.choice(positions_available)
        else:
            # after the first chance, we check if the human has any chance of winning and try to block that. Otherwise we pick randomly
            x, y = 1, 4
            # first, we check if the human is winning along a row
            # if yes, we block it and mark the position
            for i in range(3):
                a = list(permutations(tuple(range(x, y)), 2))
                for j in a:
                    if self.board[j[0]] == self.board[j[1]] != ' - ':
                        for k in range(x, y):
                            if k not in j and self.board[k] == ' - ':
                                pos = k
                                if self.board[j[1]] == " O ":
                                    self.mark(pos)
                x, y = x + 3, y + 3
            x, y = 1, 4

            # second, in case no possibilty of player's victory,
            # we check along the columns and try to block that line
            for i in range(1, 4):
                for j in list(permutations(range(i, 10, 3), 2)):
                    if self.board[j[0]] == self.board[j[1]] != ' - ':
                        for k in range(i, 10, 3):
                            if k not in j and self.board[k] == ' - ':
                                pos = k
                                if self.board[j[1]] == " O ":
                                    self.mark(pos)

            # in case both the above don't seem a threat, we check along diagonals for a possible victory
            # there are 2 diagonals, we check top left to bottom right first
            # and top right to bottom left next, if there is no possibility of victory in the former case
            diag1 = list(permutations((1, 5, 9), 2))
            diag2 = list(permutations((3, 5, 7), 2))
            for i in diag1:
                if self.board[i[0]] == self.board[i[1]] != ' - ':
                    for k in (1, 5, 9):
                        if k not in i and self.board[k] == ' - ':
                            pos = k
                            if self.board[i[1]] == " O ":
                                self.mark(pos)
            for i in diag2:
                if self.board[i[0]] == self.board[i[1]] != ' - ':
                    for k in (3, 5, 7):
                        if k not in i and self.board[k] == ' - ':
                            pos = k
                            if self.board[i[1]] == " O ":
                                self.mark(pos)

        # In case of no possibility of victory, we mark an available position randomly
        if pos == -1:
            positions_available = [i for i in range(1, 10) if self.board[i] == ' - ']
            pos = random.choice(positions_available)
        self.mark(pos)

    def play(self):
        self.player() if self.pfirst else self.AI()  # starts the marking process

    def __init__(self, pfirst):
        '''Initializes the class when called from driver code. It also initializes
        variables which are required throught the code and program like the board '''
        self.pfirst = pfirst
        self.board = {}
        for i in range(1, 10):
            self.board[i] = " - "  # fills the board with blank spaces
        self.first_time = True  # sets default value as true, which is later changed by the AI function
        print('The Layout of the board is :\n')
        self.display()


def main():
    first = input('Would you like to play first or second : ')
    # since we are not primarily checking for typos, this ensures that
    # the player plays first unless the input starts with 's' as in 'second'
    pfirst = False if first.lower().startswith('s') else True
    play = TicTacToe(pfirst)
    play.play()


# Driver Code
if __name__ == '__main__':
    main()

# Team members: Sienna Gaita-Monjaraz, Maximo Mejia, Susanne Santos Erenst
# CAP4630 - Intro to AI
# Project 1 - Tic Tac Toe
# Due: 06/07/2023

import math
import random
import time

#Player class
class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter
    
    # we want all players to get their next move given a name
    def get_move(self, game):
        pass

# Human Player
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

# Computer Player: Easy difficulty
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

# Computer Player: Medium difficulty
class MediumComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # Make a random move in the first turn
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # AI player
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            # If the other player has won, assign a high score if the other player is the max player,
            # or assign a low score if the other player is not the max player
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            # If there are no empty squares, it's a tie, so assign a score of 0
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

        
# Computer Player: Hard difficulty
class HardComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # Make a random move in the first turn
        else:
            square = self.alpha_beta(game, self.letter)['position']
        return square

    def alpha_beta(self, state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter  # AI player
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            # If the other player has won, assign a high score if the other player is the max player,
            # or assign a low score if the other player is not the max player
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            # If there are no empty squares, it's a tie, so assign a score of 0
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
            for possible_move in state.available_moves():
                state.make_move(possible_move, player)
                sim_score = self.alpha_beta(state, other_player, alpha, beta)

                # Undo move
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move

                if sim_score['score'] > best['score']:
                    best = sim_score

                alpha = max(alpha, best['score'])
                if alpha >= beta:
                    # If alpha is greater than or equal to beta, we can prune the remaining branches
                    break
        else:
            best = {'position': None, 'score': math.inf}
            for possible_move in state.available_moves():
                state.make_move(possible_move, player)
                sim_score = self.alpha_beta(state, other_player, alpha, beta)

                # Undo move
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move

                if sim_score['score'] < best['score']:
                    best = sim_score

                beta = min(beta, best['score'])
                if alpha >= beta:
                    # If alpha is greater than or equal to beta, we can prune the remaining branches
                    break

        return best
# Tic-Tac-Toe game: sets up board, register player moves, and checks game status
class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

#Play the game
def play(game, x_player, o_player, print_game=True):

    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player

        time.sleep(.8)

    if print_game:
        print('It\'s a tie!')


# Main function
if __name__ == '__main__':
    # Welcome message
    print("\nWelcome to Tic Tac Toe!") 
    print("You are 'X', and the computer is 'O'.")
    print("Your goal is to get three of your marks in a row before the computer does.\n")

    print("Select the computer difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    mode = input("Enter the mode number (1,2, or 3): ")
    
    # Variable to check if user wants to play again
    gameChoice = 'y'
    
    # Game loop
    while gameChoice != 'n':
        x_player = HumanPlayer('X')

        if mode == '1':
            o_player = RandomComputerPlayer('O')  # Easy mode
        elif mode == '2':
            o_player = MediumComputerPlayer('O') # Medium mode
        elif mode == '3':
            o_player = HardComputerPlayer('O')  # Hard mode
        else:
            print("Invalid mode. Defaulting to Easy.")
            o_player = RandomComputerPlayer('O')  # Default to Easy mode
        
        t = TicTacToe()
        play(t, x_player, o_player, print_game=True)
        gameChoice = input('Play again? (y/n): ')
        if gameChoice == 'y': 
            print("Select the computer difficulty level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            mode = input("Enter the mode number (1,2, or 3): ")

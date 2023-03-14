import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
        # Create the game board
        self.board = [[None for _ in range(3)] for _ in range(3)]

        # Initialize the game variables
        self.current_player = random.randint(0, 1)
        self.player_wins = [0, 0]
        self.num_moves = 0

    def check_win(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return True

        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return True

        # No winner yet
        return False

    def is_game_over(self):
        if self.check_win() or self.num_moves == 9:
            return True
        else:
            return False

    def make_move(self, clicked_row, clicked_col):
        # Check if the button has already been clicked
        if self.board[clicked_row][clicked_col] is not None:
            return

        # Update the game board and the button text
        self.board[clicked_row][clicked_col] = self.current_player

        # Increment the move counter
        self.num_moves += 1

        # Check for a winner
        if self.check_win():
            self.player_wins[self.current_player] += 1
            self.reset_game()
            return

        # Switch to the other player
        self.current_player = 1 - self.current_player

    def reset_game(self):
        # Reset the game board
        for i in range(3):
            for j in range(3):
                self.board[i][j] = None

        # Reset game variables
        self.current_player = random.randint(0, 1)
        self.num_moves = 0

    def get_board(self):
        return self.board

    def get_next_player(self):
        return self.current_player

    def get_winner(self):
        if self.player_wins[0] > self.player_wins[1]:
            return 0
        elif self.player_wins[1] > self.player_wins[0]:
            return 1
        else:
            return None
            
    def calculate_winning_probabilities(game):
        # Initialize a 3x3 matrix to hold the probabilities
        probabilities = [[0 for _ in range(3)] for _ in range(3)]

        # Check each position on the board
        for i in range(3):
            for j in range(3):
                # If the position is not empty, skip it
                if game.board[i][j] is not None:
                    continue

                # Create a copy of the game with the hypothetical move
                hypothetical_game = TicTacToe()
                hypothetical_game.board = [[game.board[row][col] for col in range(3)] for row in range(3)]
                hypothetical_game.current_player = game.current_player
                hypothetical_game.player_wins = [x for x in game.player_wins]
                hypothetical_game.num_moves = game.num_moves
                hypothetical_game.make_move(i, j)

                # Count the number of wins for the current player in 1000 hypothetical games
                wins = 0
                for _ in range(1000):
                    hypothetical_game_copy = TicTacToe()
                    hypothetical_game_copy.board = [[hypothetical_game.board[row][col] for col in range(3)] for row in range(3)]
                    hypothetical_game_copy.current_player = hypothetical_game.current_player
                    hypothetical_game_copy.player_wins = [x for x in hypothetical_game.player_wins]
                    hypothetical_game_copy.num_moves = hypothetical_game.num_moves

                    while not hypothetical_game_copy.is_game_over():
                        hypothetical_game_copy.make_move(*random.choice([(i, j) for i in range(3) for j in range(3) if hypothetical_game_copy.board[i][j] is None]))

                    if hypothetical_game_copy.get_winner() == game.current_player:
                        wins += 1

                # Calculate the probability of winning from this position
                probabilities[i][j] = wins / 1000

        return probabilities            




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
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'

    if print_game:
        print('It\'s a tie!')


class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def make_move(self, board):
        while True:
            try:
                move = int(input(f"{self.name}, enter a number between 1-9 to place your '{self.symbol}': "))
                if move < 1 or move > 9:
                    print("Invalid input. Enter a number between 1-9.")
                elif board[move-1] != ' ':
                    print("That spot is already taken. Choose another.")
                else:
                    return move-1
            except ValueError:
                print("Invalid input. Enter a number between 1-9.")
            

class TicTacToeUI:
    def __init__(self, player1: Player, player2: Player):
        self.game = TicTacToe(player1, player2)
        self.board = self.game.board
        self.players = [player1, player2]
        self.current_player = self.players[0]

    def print_board(self):
        print(self.board)

    def switch_player(self):
        self.current_player = self.players[(self.players.index(self.current_player) + 1) % 2]

    def play(self):
        while True:
            print(f"It's {self.current_player}'s turn.")
            self.print_board()
            try:
                move = self.current_player.get_move(self.game)
                self.game.make_move(move)
            except ValueError as e:
                print(e)
                continue

            if self.game.check_win():
                self.print_board()
                print(f"{self.current_player} wins!")
                return

            if self.game.check_tie():
                self.print_board()
                print("It's a tie!")
                return

            self.switch_player()

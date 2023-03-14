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

class TicTacToeUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        # Create buttons for the game board
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 24), width=3, height=1, command=lambda row=i, col=j: self.handle_click(row, col))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        # Create a label to display the current player
        self.current_player_label = tk.Label(self.root, text="Current player: " + self.get_player_text(self.game.current_player))
        self.current_player_label.grid(row=3, column=0, columnspan=3)

        # Create a button to reset the game
        self.reset_button = tk.Button(self.root, text="New Game", font=("Arial", 16), command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=3)

        # Initialize the UI
        self.update_board()

    def get_player_text(self, player):
        return "X" if player == 0 else "O"

    def update_board(self):
        board = self.game.board
        for i in range(3):
            for j in range(3):
                text = self.get_player_text(board[i][j]) if board[i][j] is not None else ""
                self.buttons[i][j].config(text=text, state="disabled" if self.game.is_game_over() else "normal")
        self.current_player_label.config(text="Current player: " + self.get_player_text(self.game.current_player))

    def handle_click(self, row, col):
        self.game.make_move(row, col)
        self.update_board()

    def reset_game(self):
        self.game.reset_game()
        self.update_board()

    def run(self):
        self.root.mainloop()

            
def play_game():
    game = TicTacToe()
    ui = TicTacToeUI(game)
    ui.run()

play_game()


# Create the main window
root = tk.Tk()

# Create the TicTacToeUI object and start the game
tictactoe = TicTacToeUI(root)

# Run the main event loop
root.mainloop()        

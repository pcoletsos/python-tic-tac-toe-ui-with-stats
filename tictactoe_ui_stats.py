import tkinter as tk
import random

class TicTacToeUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        # Create the game board
        self.board = [[None for _ in range(3)] for _ in range(3)]

        # Create the player labels and winning percentage labels
        self.player_labels = [tk.Label(master, text="Player 1"), tk.Label(master, text="Player 2")]
        self.win_percent_labels = [tk.Label(master, text="Wins: 0 / 0"), tk.Label(master, text="Wins: 0 / 0")]

        # Create the buttons for the game board
        self.buttons = [[tk.Button(master, width=5, height=2, command=lambda row=i, col=j: self.make_move(row, col)) for j in range(3)] for i in range(3)]

        # Place the player labels and winning percentage labels
        for i in range(2):
            self.player_labels[i].grid(row=i, column=3, padx=10, pady=10)
            self.win_percent_labels[i].grid(row=i+1, column=3, padx=10, pady=10)

        # Place the buttons for the game board
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].grid(row=i, column=j)

        # Initialize the game variables
        self.current_player = 0
        self.num_moves = 0
        self.player_wins = [0, 0]

        # Initialize the winning percentages
        self.win_percentages = [0.0, 0.0]

    def make_move(self, row, col):
        self.num_moves += 1
        # Check if the button has already been clicked
        if self.buttons[row][col]["text"] != "":
            return

        # Update the game board and the button text
        self.board[row][col] = self.current_player
        self.buttons[row][col]["text"] = "X" if self.current_player == 0 else "O"

        # Check if the current player has won
        if self.check_win():
            self.player_wins[self.current_player] += 1
            self.win_percentages[self.current_player] = float(self.player_wins[self.current_player]) / self.num_moves
            self.win_percent_labels[self.current_player]["text"] = "Wins: {} / {} ({:.1f}%)".format(self.player_wins[self.current_player], self.num_moves, self.win_percentages[self.current_player] * 100)
            self.reset_game()
            return

        # Check if the game is a tie
        if self.num_moves == 8:
            self.win_percentages[0] = float(self.player_wins[0]) / self.num_moves
            self.win_percentages[1] = float(self.player_wins[1]) / self.num_moves
            self.win_percent_labels[0]["text"] = "Wins: {} / {} ({:.1f}%)".format(self.player_wins[0], self.num_moves, self.win_percentages[0] * 100)
            self.win_percent_labels[1]["text"] = "Wins: {} / {} ({:.1f}%)".format(self.player_wins[1], self.num_moves, self.win_percentages[1] * 100)
            self.reset_game()
            return

        # Switch to the other player
        self.current_player = 1 if self.current_player == 0 else 0

        
    def reset_game(self):
        # Reset the game board and button text
        self.board = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""

        # Reset the game variables
        self.current_player = 0
        self.num_moves = 0

    def check_win(self):
        # Check rows
        for row in self.board:
            if row.count(self.current_player) == 3:
                return True

        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] == self.current_player:
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
            return True

        # No winner yet
        return False


# Create the main window
root = tk.Tk()

# Create the TicTacToeUI object and start the game
tictactoe = TicTacToeUI(root)

# Run the main event loop
root.mainloop()
        

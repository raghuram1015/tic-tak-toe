import tkinter as tk
from tkinter import messagebox

# Initialize variables
current_player = 'X'
board = ["", "", "", "", "", "", "", "", ""]
game_active = True

# Function to check for a winner


def check_winner():
    global game_active
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            messagebox.showinfo("Game Over", f"{board[a]} Wins!")
            reset_game()
            return

    if "" not in board:
        messagebox.showinfo("Game Over", "It's a Draw!")
        reset_game()

# Function to handle cell clicks


def cell_click(index):
    global current_player, game_active
    if board[index] == "" and game_active:
        board[index] = current_player
        buttons[index].config(text=current_player)
        check_winner()
        current_player = 'O' if current_player == 'X' else 'X'

# Function to reset the game


def reset_game():
    global board, game_active, current_player
    board = ["", "", "", "", "", "", "", "", ""]
    game_active = True
    current_player = 'X'
    for button in buttons:
        button.config(text="")


# Create the GUI
root = tk.Tk()
root.title("Tic Tac Toe")

buttons = []
for i in range(9):
    button = tk.Button(root, text="", font=("Arial", 24), height=2, width=5,
                       command=lambda i=i: cell_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

reset_button = tk.Button(root, text="Play Again",
                         font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

root.mainloop()

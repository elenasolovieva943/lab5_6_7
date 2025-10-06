import tkinter as tk
from tkinter import messagebox

PLAYER = "X"
BOT = "O"


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.configure(bg='white')
        self.root.resizable(False, False)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.create_status()
        self.create_buttons()

        self.player_turn = True
        self.winning_line = []

    def create_status(self):
        self.status_label = tk.Label(self.root, text="Ваш ход (X)",
                                     font=("Arial", 14), bg='white')
        self.status_label.pack(pady=10)

    def create_buttons(self):
        game_frame = tk.Frame(self.root, bg='white')
        game_frame.pack(pady=10)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(game_frame, text="", font=("Arial", 32),
                                width=3, height=1, bg='#f0f0f0',
                                command=lambda x=i, y=j: self.player_move(x, y))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn

    def player_move(self, x, y):
        if not self.player_turn:
            return
        if self.board[x][y] == "":
            self.buttons[x][y].config(text=PLAYER, fg='blue', disabledforeground='blue')
            self.buttons[x][y].config(state="disabled")
            self.board[x][y] = PLAYER

            if self.check_winner(self.board, PLAYER):
                self.highlight_winning_line()
                messagebox.showinfo("Игра окончена", "Вы выиграли!")
                self.reset()
                return
            elif self.is_draw(self.board):
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return
            else:
                self.player_turn = False
                self.status_label.config(text="Ход бота...")
                self.root.after(500, self.bot_move)

    def bot_move(self):
        move = self.find_best_move(self.board)
        if move:
            x, y = move
            self.buttons[x][y].config(text=BOT, fg='red', disabledforeground='red')
            self.buttons[x][y].config(state="disabled")
            self.board[x][y] = BOT

            if self.check_winner(self.board, BOT):
                self.highlight_winning_line()
                messagebox.showinfo("Игра окончена", "Бот выиграл!")
                self.reset()
                return
            elif self.is_draw(self.board):
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return

        self.player_turn = True
        self.status_label.config(text="Ваш ход (X)")

    def check_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                self.winning_line = [(i, j) for j in range(3)]
                return True
            if all(board[j][i] == player for j in range(3)):
                self.winning_line = [(j, i) for j in range(3)]
                return True
        if all(board[i][i] == player for i in range(3)):
            self.winning_line = [(i, i) for i in range(3)]
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            self.winning_line = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def highlight_winning_line(self):
        for i, j in self.winning_line:
            self.buttons[i][j].config(bg='lightgreen')

    def is_draw(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def find_best_move(self, board):
        best_val = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = BOT
                    move_val = self.minimax(board, 0, False)
                    board[i][j] = ""
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_max):
        if self.check_winner(board, BOT):
            return 10 - depth
        if self.check_winner(board, PLAYER):
            return depth - 10
        if self.is_draw(board):
            return 0

        if is_max:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = BOT
                        val = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best = max(best, val)
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = PLAYER
                        val = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best = min(best, val)
            return best

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg='#f0f0f0')
        self.player_turn = True
        self.status_label.config(text="Ваш ход (X)")
        self.winning_line = []


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
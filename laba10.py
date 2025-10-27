import tkinter as tk
from tkinter import messagebox

Player = "X"
Bot = "O"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.resizable(False, False)
        self.root.configure(bg="#e0f7fa")

        self.status_label = tk.Label(
            self.root,
            text="Ваш ход (X)",
            font=("Arial", 18, "bold"),
            bg="#e0f7fa",
            fg="#01579b",
        )
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.create_buttons()
        self.player_turn = True

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 40, "bold"),
                    width=5,
                    height=2,
                    bg="#ffffff",
                    activebackground="#b3e5fc",
                    relief="raised",
                    command=lambda x=i, y=j: self.player_move(x, y),
                )
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#bbdefb"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff"))
                self.buttons[i][j] = btn

    def player_move(self, x, y):
        if not self.player_turn or self.board[x][y] != "":
            return
        self.make_move(x, y, Player, color="#1976d2")
        if self.check_winner(Player):
            self.status_label.config(text="Вы выиграли!", fg="#2e7d32")
            messagebox.showinfo("Игра окончена", "Поздравляем, вы выиграли!")
            self.root.after(1000, self.reset)
            return
        elif self.is_draw():
            self.status_label.config(text="Ничья!", fg="#616161")
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.root.after(1000, self.reset)
            return

        self.player_turn = False
        self.status_label.config(text="Ход бота (O)", fg="#b71c1c")
        self.root.after(400, self.bot_move)

    def bot_move(self):
        best_score = -float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = Bot
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            x, y = best_move
            self.make_move(x, y, Bot, color="#d32f2f")
            if self.check_winner(Bot):
                self.status_label.config(text="Бот выиграл!", fg="#c62828")
                messagebox.showinfo("Игра окончена", "Бот выиграл!")
                self.root.after(1000, self.reset)
                return
            elif self.is_draw():
                self.status_label.config(text="Ничья!", fg="#616161")
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.root.after(1000, self.reset)
                return

        self.player_turn = True
        self.status_label.config(text="Ваш ход (X)", fg="#01579b")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_board(board, Bot):
            return 10 - depth
        if self.check_winner_board(board, Player):
            return depth - 10
        if self.is_draw_board(board):
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = Bot
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = Player
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner_board(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def make_move(self, x, y, player, color):
        self.board[x][y] = player
        self.buttons[x][y].config(
            text=player,
            state="disabled",
            disabledforeground=color,
            relief="sunken",
            bg="#e3f2fd",
        )

    def check_winner(self, player):
        return self.check_winner_board(self.board, player)

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def is_draw_board(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg="#ffffff", relief="raised")
        self.player_turn = True
        self.status_label.config(text="Ваш ход (X)", fg="#01579b")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

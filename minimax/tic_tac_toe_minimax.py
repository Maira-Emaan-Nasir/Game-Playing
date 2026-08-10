import tkinter as tk
import math

PLAYER = "X"
AI_MARK = "O"

# ================= AI =================
class AI:
    def best_move(self, board):
        best_score = -math.inf
        move = None

        for i in range(9):
            if board[i] is None:
                board[i] = AI_MARK
                score = self.minimax(board, False)
                board[i] = None

                if score > best_score:
                    best_score = score
                    move = i

        return move

    def minimax(self, board, is_maximizing):
        winner = check(board)

        if winner == AI_MARK:
            return 1
        elif winner == PLAYER:
            return -1
        elif None not in board:
            return 0

        if is_maximizing:
            best = -math.inf
            for i in range(9):
                if board[i] is None:
                    board[i] = AI_MARK
                    best = max(best, self.minimax(board, False))
                    board[i] = None
            return best

        else:
            best = math.inf
            for i in range(9):
                if board[i] is None:
                    board[i] = PLAYER
                    best = min(best, self.minimax(board, True))
                    board[i] = None
            return best


# ================= UI =================
root = tk.Tk()
root.title("TIC TAC TOE")
root.geometry("360x520")
root.configure(bg="#12001f")

board = [None]*9
game_over = False
ai = AI()

# ================= TITLE =================
title = tk.Label(
    root,
    text="✦ TIC TAC TOE ✦",
    font=("Segoe UI", 24, "bold"),
    fg="#d79aff",
    bg="#12001f"
)
title.pack(pady=15)

# ================= CANVAS =================
canvas = tk.Canvas(root, width=300, height=300, bg="#12001f", highlightthickness=0)
canvas.pack()

cell = 100

def grid():
    for i in range(1,3):
        canvas.create_line(0,i*cell,300,i*cell,fill="#5a2a82",width=3)
        canvas.create_line(i*cell,0,i*cell,300,fill="#5a2a82",width=3)

grid()

# ================= DRAW =================
def draw(i, sym):
    x = (i%3)*cell + 50
    y = (i//3)*cell + 50

    color = "#ff4d6d" if sym=="X" else "#4cc9f0"
    canvas.create_text(x,y,text=sym,font=("Arial",40,"bold"),fill=color)

# ================= CHECK =================
def check(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b1,c in wins:
        if b[a] and b[a]==b[b1]==b[c]:
            return b[a]
    return None


def draw_check():
    return all(v is not None for v in board)

# ================= CLICK =================
def click(event):
    global game_over

    if game_over:
        return

    col = event.x // cell
    row = event.y // cell
    i = row*3 + col

    if i < 0 or i > 8:
        return

    if board[i] is None:

        # PLAYER MOVE
        board[i] = PLAYER
        draw(i, PLAYER)

        if check(board):
            status.config(text="🎉 You Win!")
            game_over = True
            return

        if draw_check():
            status.config(text="🤝 Draw!")
            game_over = True
            return

        # AI MOVE
        move = ai.best_move(board)
        if move is not None:
            board[move] = AI_MARK
            draw(move, AI_MARK)

        if check(board):
            status.config(text="🤖 AI Wins!")
            game_over = True
            return

        if draw_check():
            status.config(text="🤝 Draw!")
            game_over = True
            return

        status.config(text="✨ Your Turn")

canvas.bind("<Button-1>", click)

# ================= STATUS =================
status = tk.Label(
    root,
    text="✨ Your Turn",
    font=("Segoe UI",12),
    fg="#caa6ff",
    bg="#12001f"
)
status.pack(pady=10)

# ================= RESET =================
def reset():
    global board, game_over
    board = [None]*9
    game_over = False
    canvas.delete("all")
    grid()
    status.config(text="✨ Your Turn")

tk.Button(
    root,
    text="Restart ↻",
    bg="#6a0dad",
    fg="white",
    font=("Segoe UI",11,"bold"),
    command=reset
).pack(pady=10)

root.mainloop()

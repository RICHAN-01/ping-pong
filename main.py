import tkinter as tk
import time
import random

root = tk.Tk()
root.title('Ping pong')
root.resizable(0, 0)
root.wm_attributes('-topmost', 1)
canvas = tk.Canvas(root, width=1080, height=720, bd=0, highlightthickness=0)
canvas.pack()
root.update()


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 540, 360)
        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -2
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if self.hit_paddle(pos):
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(540, 300, text=f'GAME OVER   \nTOTAL SCORE: {self.score.score}', font=('Arial', 15),
                               fill='Black')
        if pos[2] >= self.canvas_width:
            self.x = -2

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                self.score.score_update()
                return True
        return False


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 150, 10, fill=color)
        self.canvas.move(self.id, 500, 650)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_right(self, event):
        self.x = 5

    def turn_left(self, event):
        self.x = -5


class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(70, 20, text=f'SCORE: {self.score}', font=('Arial', 15), fill=color)

    def score_update(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=f'SCORE: {self.score}')


score = Score(canvas, 'black')
paddle = Paddle(canvas, 'gray')
ball = Ball(canvas, paddle, score, 'red')
while True:
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
    else:
        break
    root.update_idletasks()
    root.update()
    time.sleep(0.005)
time.sleep(3)

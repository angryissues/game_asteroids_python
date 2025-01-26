# отображение очков и жизней
import tkinter as tk
from settings import *

class HUD:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lives_text = self.canvas.create_text(10, 10, text="Lives: 0", fill="white", anchor="nw", font=("Arial", 14))
        self.score_text = self.canvas.create_text(10, 30, text="Score: 0", fill="white", anchor="nw", font=("Arial", 14))

    def update(self, lives, score):
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {lives}")
        self.canvas.itemconfig(self.score_text, text=f"Score: {score}")

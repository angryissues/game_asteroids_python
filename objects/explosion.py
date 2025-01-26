# класс анимации взрыв
import tkinter as tk
from settings import *
import math

class Explosion:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.frames = [tk.PhotoImage(file=img).subsample(4, 4) for img in EXPLOSION_FRAMES]
        self.current_frame = 0
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.frames[self.current_frame])
        self.frame_delay = 5  # задержка между кадрами
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_delay:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self):
        if not self.finished:
            self.canvas.itemconfig(self.sprite, image=self.frames[self.current_frame])
            self.canvas.coords(self.sprite, self.x, self.y)

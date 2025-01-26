# класс астероидов
import tkinter as tk
from settings import *
import random
from utils import wrap_around

class Asteroid:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-1, 1) # скорость
        self.velocity_y = random.uniform(-1, 1)

        self.image = tk.PhotoImage(file=ASTEROID_IMAGE).subsample(6, 6)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.x, self.y = wrap_around(self.x, self.y, self.canvas)

    def draw(self):
        self.canvas.coords(self.sprite, self.x, self.y)

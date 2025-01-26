# класс ракет
import tkinter as tk
from settings import *
from PIL import Image, ImageTk
import math

class Rocket:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.alive = True

        original_image = Image.open(ROCKET_IMAGE)
        new_size = (original_image.width // 9, original_image.height // 9)
        original_image = original_image.resize(new_size, Image.Resampling.LANCZOS)
        self.original_image = original_image
        self.current_image = ImageTk.PhotoImage(self.original_image)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.current_image)

        self.speed = 10
        self.life = 150  # время жизни ракеты в кадрах

    def update(self):
        radians = math.radians(self.angle)
        self.x += math.cos(radians)*self.speed
        self.y += math.sin(radians)*self.speed
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self):
        rotated = self.original_image.rotate(-self.angle, expand=True)
        self.current_image = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.sprite, image=self.current_image) # обновляет спрайт
        self.canvas.coords(self.sprite, self.x, self.y)

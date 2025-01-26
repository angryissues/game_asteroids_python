# класс корабля
import tkinter as tk
from settings import *
from utils import wrap_around
import math
from PIL import Image, ImageTk


class Ship:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0

        self.accelerating = False # ускорение
        self.rotating_left = False # вращение
        self.rotating_right = False

        original_normal = Image.open(SHIP_IMAGE)
        original_thrust = Image.open(SHIP_THRUST_IMAGE)
        new_size = (original_normal.width // 4, original_normal.height // 4)
        original_normal = original_normal.resize(new_size, Image.Resampling.LANCZOS)
        original_thrust = original_thrust.resize(new_size, Image.Resampling.LANCZOS)

        self.original_normal = original_normal
        self.original_thrust = original_thrust

        self.current_image = ImageTk.PhotoImage(self.original_normal)
        
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.current_image) # идентификатор объекта на холсте

    def update(self):
        if self.rotating_left:
            self.angle -= 5
        if self.rotating_right:
            self.angle += 5

        # Ускорение
        if self.accelerating:
            radians = math.radians(self.angle)
            self.velocity_x += math.cos(radians) * 0.1
            self.velocity_y += math.sin(radians) * 0.1
        else:
            # Трение
            self.velocity_x *= 0.99
            self.velocity_y *= 0.99

        # Обновление позиции
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Торроидальная геометрия 
        self.x, self.y = wrap_around(self.x, self.y, self.canvas)

    def draw(self):
        if self.accelerating:
            base_image = self.original_thrust
        else:
            base_image = self.original_normal

        # Поворачиваем изображение
        rotated = base_image.rotate(-self.angle, expand=True)

        # Обновляем текущую картинку
        self.current_image = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.sprite, image=self.current_image)
        self.canvas.coords(self.sprite, self.x, self.y)

    def shoot(self):
        from objects.rocket import Rocket
        # Смещение носа ракеты относительно центра
        nose_offset = 175  # Расстояние от центра корабля до носа

        # Угол поворота корабля
        radians = math.radians(self.angle)

        # Координаты носа ракеты
        nose_x = self.x + math.cos(radians) * nose_offset
        nose_y = self.y + math.sin(radians) * nose_offset

        # Создаём ракету
        rocket = Rocket(self.canvas, nose_x, nose_y, self.angle)

        # Возвращаем одну ракету
        return rocket

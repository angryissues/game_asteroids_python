# управление фоном
import tkinter as tk
from PIL import Image, ImageTk
from settings import *


class Background:
    def __init__(self, canvas):
        self.canvas = canvas
        
        # Загрузка статичного фона
        self.bg_image = tk.PhotoImage(file=BACKGROUND_IMAGE)
        self.bg_sprite = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Загрузка динамического слоя
        dynamic_image = Image.open(DYNAMIC_BACKGROUND_IMAGE)
        self.dynamic_bg_image = ImageTk.PhotoImage(dynamic_image)

        # Начальная позиция динамического слоя
        self.dynamic_x = 0
        self.dynamic_y = 0
        self.dynamic_speed = -0.5  # скорость движения влево
        self.dynamic_bg_sprite = self.canvas.create_image(self.dynamic_x, self.dynamic_y, image=self.dynamic_bg_image, anchor="nw")

        # Чтобы бесконечно прокручивать фон, создать второй экземпляр того же изображения, 
        # расположенный сразу за первым. Когда первый уйдет далеко влево, можно сдвигать их по кругу.
        self.dynamic_bg_sprite2 = self.canvas.create_image(self.dynamic_x + dynamic_image.width, self.dynamic_y, image=self.dynamic_bg_image, anchor="nw")
        self.dynamic_width = dynamic_image.width

    def update(self):
        # Двигаем влево
        self.dynamic_x += self.dynamic_speed

        # Если первый слой ушел слишком далеко влево, циклически перемещаем его вправо
        if self.dynamic_x <= -self.dynamic_width:
            self.dynamic_x += self.dynamic_width

    def draw(self):
        # Обновляем координаты динамических слоёв
        # Первый слой
        self.canvas.coords(self.dynamic_bg_sprite, self.dynamic_x, self.dynamic_y)
        # Второй слой всегда следует за первым, чтобы создать непрерывную ленту
        self.canvas.coords(self.dynamic_bg_sprite2, self.dynamic_x + self.dynamic_width, self.dynamic_y)

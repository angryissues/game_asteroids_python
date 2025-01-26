# вспомогательные функции (например, обработка коллизий)
from settings import *
import math

def wrap_around(x, y, canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if x < 0:
        x += width
    elif x > width:
        x -= width

    if y < 0:
        y += height
    elif y > height:
        y -= height

    return x, y

def check_collision(obj1, obj2, threshold=50):
    # Простейшая проверка по расстоянию между центрами
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    dist = math.sqrt(dx*dx + dy*dy)
    return dist < threshold

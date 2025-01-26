# основной игровой цикл и управление состояниями игры
import tkinter as tk
from settings import *
from objects.ship import Ship
from objects.rocket import Rocket
from objects.asteroid import Asteroid
from objects.explosion import Explosion
from ui.hud import HUD
from ui.splash_screen import SplashScreen
from background import Background
import random
from utils import check_collision
from tkinter import StringVar
from playsound import playsound
import threading


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asteroids")
        self.root.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self.root, bg=BACKGROUND_COLOR)
        self.canvas.pack(fill = "both", expand = True)

        self.background = Background(self.canvas)
        self.hud = HUD(self.canvas)
        self.splash = SplashScreen(self.canvas, self)

        self.root.bind("<KeyPress>", self.handle_key_press)
        self.root.bind("<KeyRelease>", self.handle_key_release)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))

        self.running = False
        self.ship = None
        self.asteroids = []
        self.rockets = []
        self.explosions = []

        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE

        self.selected_track = StringVar(value=list(TRACKS.keys())[0])
        self.create_track_selection_ui()

        self.track_menu.config(font=("Arial", 14))
        self.track_menu.place(relx=0.5, rely=0.63, anchor="center")
        
        # Показать заставку при старте
        self.splash.show_question()

    def run(self):
        self.root.mainloop()

    def create_track_selection_ui(self):
        self.track_label = tk.Label(self.root, text = 'Выберите саундрек:', bg = 'black', fg = 'white', font = ('Arial', 18))
        self.track_label.place(relx=0.5, rely=0.55, anchor="center")
        self.track_menu = tk.OptionMenu(self.root, self.selected_track, *TRACKS.keys())
    
    def start_game(self):
        self.splash.hide()

        self.track_label.place_forget()
        self.track_menu.place_forget()

        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.ship = Ship(self.canvas, canvas_width // 2, canvas_height // 2)

        # Создание нескольких астероидов
        for _ in range(8):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            self.asteroids.append(Asteroid(self.canvas, x, y))

        self.running = True

        chosen_name = self.selected_track.get()  # Получаем название трека (ключ)
        chosen_path = TRACKS[chosen_name]        # Получаем путь к файлу
        threading.Thread(target=self.loop_music, args=(chosen_path,), daemon=True).start()

        self.game_loop()

    def loop_music(self, track):
        # Бесконечный цикл для зацикливания музыки
        while self.running:  # пока игра идет
            playsound(track)

    def end_game(self):
        self.running = False
        # Можно реализовать логику конца игры, отобразить финальный счет, заставку и т.д.
        self.splash.show_end_message()

    def game_loop(self):
        if not self.running:
            return

        # Обновление состояния
        self.update_objects()

        # Проверка коллизий
        self.check_collisions2()

        # Отрисовка
        self.draw_objects()

        self.hud.update(self.lives, self.score)

        # Следующий кадр
        self.root.after(int(1000/FPS), self.game_loop)

    def update_objects(self):
        self.background.update()
        self.ship.update()

        for a in self.asteroids:
            a.update()

        for r in self.rockets:
            r.update()

        # Удаляем ракеты, вышедшие за срок жизни
        self.rockets = [r for r in self.rockets if r.alive]

        # Обновление взрывов
        for e in self.explosions:
            e.update()

        # Удаляем завершившиеся взрывы
        self.explosions = [e for e in self.explosions if not e.finished]

    def draw_objects(self):
        self.background.draw()
        self.ship.draw()

        for a in self.asteroids:
            a.draw()

        for r in self.rockets:
            r.draw()

        for e in self.explosions:
            e.draw()

    def check_collisions2(self):
    # Столкновения ракеты с астероидом
        for r in self.rockets:
            for a in self.asteroids:
                if check_collision(r, a, threshold=70):
                    # Удаляем астероид и ракету, создаём взрыв, увеличиваем счёт
                    self.explosions.append(Explosion(self.canvas, a.x, a.y))
                    self.asteroids.remove(a)
                    r.alive = False
                    self.score += 1
                    break

        # Если все астероиды уничтожены, победа
        if not self.asteroids:
            self.win_game()

        # Столкновения корабля с астероидом
        for a in self.asteroids:
            if check_collision(self.ship, a):
                self.explosions.append(Explosion(self.canvas, self.ship.x, self.ship.y))
                self.asteroids.remove(a)
                self.lives -= 1
                # Перемещаем корабль в центр
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                self.ship.x = canvas_width // 2
                self.ship.y = canvas_height // 2
                self.ship.velocity_x = 0
                self.ship.velocity_y = 0
                if self.lives <= 0:
                    self.end_game()

    def handle_key_press(self, event):
        if event.keysym == "Left":
            self.ship.rotating_left = True
        elif event.keysym == "Right":
            self.ship.rotating_right = True
        elif event.keysym == "Up":
            self.ship.accelerating = True
        elif event.keysym == "space":
            # Стрельба
            r = self.ship.shoot()
            if r:
                self.rockets.append(r)

    def handle_key_release(self, event):
        if event.keysym == "Left":
            self.ship.rotating_left = False
        elif event.keysym == "Right":
            self.ship.rotating_right = False
        elif event.keysym == "Up":
            self.ship.accelerating = False

    def win_game(self):
        self.running = False
        self.splash.show_victory_message()

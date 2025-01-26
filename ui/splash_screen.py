# заставка игры
import tkinter as tk
from settings import *

class SplashScreen:
    def __init__(self, canvas, game):
        self.canvas = canvas
        self.game = game
        # Изначально скрываем старый текст, он нам не нужен
        self.text = self.canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,
                                            text="", fill="white", font=("Arial", 24), state="hidden")

        # canvas.master возвращает главное окно приложения
        self.question_label = tk.Label(self.canvas.master, text="Ответьте на вопрос:\nЧей Крым?", fg="white", bg="black", font=("Arial", 24))
        self.left_button = tk.Button(self.canvas.master, text="Украинский", command=self.on_left_click)
        self.right_button = tk.Button(self.canvas.master, text="Русский", command=self.on_right_click)
        
        # Сообщение об окончании игры
        self.end_label = tk.Label(self.canvas.master, text="Игра для вас окончена!", fg="red", bg="black", font=("Arial", 24))

    def show_question(self):
        # Показываем вопрос и кнопки
        # Разместим их примерно по центру экрана
        self.question_label.place(relx=0.5, rely=0.4, anchor="center")
        self.left_button.place(relx=0.4, rely=0.5, anchor="center")
        self.right_button.place(relx=0.6, rely=0.5, anchor="center")

    def hide(self):
        # Скрываем все элементы заставки
        self.question_label.place_forget()
        self.left_button.place_forget()
        self.right_button.place_forget()
        self.end_label.place_forget()
        self.canvas.itemconfig(self.text, state="hidden")

    def show_end_message(self):
        # Показываем сообщение о конце игры
        # Скрываем вопрос и кнопки
        self.question_label.place_forget()
        self.left_button.place_forget()
        self.right_button.place_forget()
        self.end_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_left_click(self):
        # Неверный ответ
        # Игра окончена для игрока
        self.game.end_game()

    def on_right_click(self):
        # Верный ответ
        # Начинаем игру
        self.game.start_game()

    def show_victory_message(self):
        # Показываем сообщение о победе
        self.end_label.config(text="Поздравляем! Вы уничтожили все астероиды!")
        self.end_label.place(relx=0.5, rely=0.5, anchor="center")


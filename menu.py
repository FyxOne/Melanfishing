import pygame

"""
    USE GUIDE
    somebutton = Button(X, Y, Width, Height, Text) - Создание кнопки. Параметры не обязательны, но желательно прописать
    somebutton.setPosition(X, Y) - Смена позиции по X и Y
    somebutton.draw() - Отрисовка
    somebutton.getRect() - Возвращает pygame.Rect (self.btn)
"""
class Button:
    # Конструктор
    def __init__(self, x = 0, y = 0, w = 250, h = 250, text = "New button"):
        # Позиция
        self.posx = x
        self.posy = y
        # Ширина и высота
        self.width = w
        self.height = h
        # Фигура
        self.btn = pygame.Rect(self.posx, self.posy, self.width, self.height)

        # Текст и шрифт
        pygame.font.init()
        self.font = pygame.font.Font("resources/EpilepsySans.ttf", 30)
        self.text = self.font.render(text, True, (15, 0, 50))

    # Смена позиции кнопки
    def setPosition(self, x, y):
        # self - это обозначение, что объект принадлежит классу (и переменная тоже)
        self.posx = x
        self.posy = y
        self.btn.topleft = (x, y)

    # Рисуем кнопку (рендер)
    # В аргументах указываем окно (screen) и цвет (color)
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.btn)
        # тут текст ебанный
        text_rect = self.text.get_rect(center=self.btn.center)
        screen.blit(self.text, text_rect)
        
    # Полуение фиругы кнопки. Возвращает pygame.Rect
    # В основном для логики нажатия
    def getRect(self):
        return self.btn
    

# Объект кнопки "играть"
# X, Y, Ширина, Высота, Текст на кнопке
play_button = Button(1280/2 - 250/2, 300, 250, 50, "Play")
quit_button = Button(1280/2 - 250/2, 370, 250, 50, "Quit")

# def menu(screen) по-сути
def menu(screen, color):
    # Рисуем эту кнопку
    play_button.draw(screen, color)
    quit_button.draw(screen, color)

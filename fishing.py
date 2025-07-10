import pygame
import random

class Fishing:
    # Конструктор класса
    def __init__(self, x = 55): 
        # Рыбачит ли сейчас игрок или нет?
        self.isFishing = False
        # Защита от повтороного прожатия через зажатие клавиши
        self.isKeyPressed = False
        # Позиция основной части "шкалы"
        self.posx = x
        # Направление движения шкалы
        self.direction = 0
        # Позиция полосы управлемой игроком
        self.arrow_x = 150

        self.zone = pygame.Rect(self.posx, 55, 35, 40)
        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)

        self.points = 0
        self.fish = 0
        
    # Нажатия на клавиши
    def keybinds(self):
        # Вход в режим рыбалки
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] :
            if self.isKeyPressed == False:
                self.isKeyPressed = True
                
                if(self.isFishing != True):
                    self.isFishing = True
                else:
                    self.isFishing = False
        else:
            self.isKeyPressed = False

        # Управление полосой игрока
        if keys[pygame.K_w]:
            if self.arrow_x <= 295:
                self.arrow_x += 0.3
        else:
            if self.arrow_x >= 55:
                self.arrow_x -= 0.3

        self.arrow.topleft = (self.arrow_x, 50)

    # Генерация рандомного правравления основной шкалы
    def random(self):
        self.direction = random.randint(1, 2)

        if self.posx > 60 and self.posx < 220:
            if self.direction == 1:
                self.posx += 0.5
            if self.direction == 2:
                self.posx -= 0.5
        else:
            self.posx = (60 + (300 - 55)) / 2

        self.zone.topleft = (self.posx, 55)

    def update(self):
        if self.zone.colliderect(self.arrow):
            if self.points <= 240:
                self.points += 0.1
        else:
            if self.points > -0.1:
                self.points -= 0.1
        if self.points > 239:
            self.points = 0
            self.fish += 1
        print(self.fish)

    # Отрисовка объектов
    def draw(self, screen, color):
        pygame.draw.line(screen, color, (50, 50), (300, 50))
        pygame.draw.line(screen, color, (50, 100), (300, 100))
        pygame.draw.line(screen, color, (50, 50), (50, 100))
        pygame.draw.line(screen, color, (300, 50), (300, 100))

        # Шкала 
        pygame.draw.line(screen, color, (50, 200), (300, 200))
        pygame.draw.line(screen, color, (50, 250), (300, 250))
        pygame.draw.line(screen, color, (50, 200), (50, 250))
        pygame.draw.line(screen, color, (300, 200), (300, 250))

        pygame.draw.rect(screen, color, (55, 205, self.points, 40))
        
        # Эти 2 штуки должны быть доступны во всем классе. Сделай также как и модель игрока, там просто
        pygame.draw.rect(screen, color, self.zone)
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)

    # Возврат состояния рыбалки игрока
    def isFishing(self):
        return self.isFishing

fishing_menu = Fishing()

def fishing(screen, color):
    fishing_menu.keybinds()

    if fishing_menu.isFishing:
        fishing_menu.random()
        fishing_menu.draw(screen, color)
        fishing_menu.update()
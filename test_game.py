import pygame

class Player:
    # Конструктор
    def __init__(self, x=0, y=0):
        # Позиция
        self.posx = x
        self.posy = y
        # Фигура
        self.player_model = pygame.Rect(self.posx, self.posy, 50, 50)
        self.player_texture = pygame.image.load('resources/player.png') 

    # управление
    def control(self):
        keys = pygame.key.get_pressed()
        if self.posy > 0:
            if keys[pygame.K_w]:
                self.posy -= 0.5
        if self.posx > 0:
            if keys[pygame.K_a]:
                self.posx -= 0.5
        if self.posy < 670:
            if keys[pygame.K_s]:
                self.posy += 0.5
        if self.posx < 1230:
            if keys[pygame.K_d]:
                self.posx += 0.5
                
        # Обновление
        self.player_model.topleft = (self.posx, self.posy)
    
    # Отрисовка
    def draw(self, screen, color):
        screen.blit(self.player_texture, self.player_model)

# Создание квадрата с кордами (0, 0)
square = Player(0, 0)

def game(screen, color):
    square.control() 
    square.draw(screen, color)

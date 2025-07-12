import pygame
import random
import time
import string

class Fishing:
    # Конструктор класса
    def __init__(self): 
        # Рыбачит ли сейчас игрок или нет?
        self.isFishing = False
        # Защита от повтороного прожатия через зажатие клавиши
        self.isKeyPressed = False
        # Позиция основной части "шкалы"
        self.posx = 55
        # Направление движения шкалы
        self.direction = 0
        # Позиция полосы управлемой игроком
        self.arrow_x = 250

        self.zone = pygame.Rect(self.posx, 55, 30, 40)
        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)

        self.points = 0
        self.fish = 0

        self.clock = pygame.time.Clock()
        self.clockclock = pygame.time.Clock()
        self.clockclockclock = pygame.time.Clock()

        self.arrow_speed = 0.1
        self.zone_speed = 0.05
        
        self.start_time = pygame.time.get_ticks()
        self.startstart_time = pygame.time.get_ticks()
        self.startstartstart_time = pygame.time.get_ticks()

        self.dt = 0

        self.wait_time = 5

        self.pizda = 0
        self.lock = 0
        self.start = 0
        self.reaction = 0
        self.fuck_u = 0

        self.meow = 0

        pygame.font.init()
        self.font = pygame.font.Font("resources/EpilepsySans.ttf", 30)
        self.text = self.font.render("My fishies: " + str(self.fish), True, (255, 255, 100))
        self.text2 = self.font.render("FUCK MY FISH IS HERE!!!!", True, (255, 255, 255))

        pygame.mixer.init()
        self.klujet = pygame.mixer.Sound("resources/klujet.mp3")
        self.katushka = pygame.mixer.Sound("resources/katushka.mp3")
        self.katushka.set_volume(0.1)
        self.rain = pygame.mixer.Sound("resources/rain.mp3")

        self.player_model = pygame.Rect(0, 0, 1280, 720)
        self.player_texture = pygame.image.load('resources/fishing1.png')
        
    def getFishes(self):
        return self.fish
        
    # Нажатия на клавиши
    def keybinds(self):
        pipipi = self.wait_time - (pygame.time.get_ticks() - self.startstart_time) // 1000
        if pipipi <= 0:
            if self.pizda == 0:
                self.start = time.time()
                print("РЫБА НАХУЙ!")
                self.pizda = 1
                self.klujet.play()

            # Вход в режим рыбалки
            if self.lock != 1:
                self.fuck_u = time.time() - self.start
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[2]:
                    self.reaction = time.time() - self.start
                    print(self.reaction)

                    self.arrow_x = 140
                    self.posx = 55
                    self.zone.topleft = (self.posx, 55)
                    self.arrow.topleft = (self.arrow_x, 50)

                    if self.reaction < 1.5:
                        self.katushka.play(-1)
                        self.player_texture = pygame.image.load('resources/fishing2.png')
                        if self.isKeyPressed == False:
                            self.isKeyPressed = True
                            self.lock = 1
                            
                            if(self.isFishing != True):
                                self.isFishing = True
                    else:
                        print("ебать ты окунь")
                        self.pizda = 0
                        self.klujet.stop()
                        self.startstart_time = pygame.time.get_ticks()
                else:
                    self.isKeyPressed = False

    # Генерация рандомного правравления основной шкалы
    def random(self):
        pi_pi = 1 - (pygame.time.get_ticks() - self.start_time) // 1000

        if pi_pi <= 0:
            self.start_time = pygame.time.get_ticks()
            self.direction = random.randint(1, 2)

        #if self.posx > 60 and self.posx < 220:
        if self.direction == 1:
            self.posx += self.zone_speed * self.dt
            if self.posx > 220:
                self.direction = 2
            
        if self.direction == 2:
            self.posx -= self.zone_speed * self.dt
            if self.posx < 60:
                self.direction = 1
        #else:
        #    self.posx = (60 + (300 - 55)) / 2


    def update(self):
        self.dt = self.clock.tick(60)

        if self.zone.colliderect(self.arrow):
            if self.points <= 240:
                self.points += 1
        else:
            if self.points > -0.1:
                self.points -= 1

        if self.points > 239:
            self.points = 0
            self.fish += 1
            self.isFishing = False
            self.player_texture = pygame.image.load('resources/fishing1.png')
            self.startstart_time = pygame.time.get_ticks()
            self.katushka.stop()
            self.klujet.play()
            self.wait_time = random.randint(3, 10)

            self.arrow_x = 140
            self.posx = 55
            self.zone.topleft = (self.posx, 55)
            self.arrow.topleft = (self.arrow_x, 50)

            self.pizda = 0

            self.lock = 0

            self.text = self.font.render("My fishies: " + str(self.fish), True, (255, 255, 100))
        
        if self.points == 227:
            self.player_texture = pygame.image.load('resources/fishing3.png')

        mouse_buttons = pygame.mouse.get_pressed()
        if self.isFishing:
            # Управление полосой игрока
            if mouse_buttons[0]:
                if self.arrow_x <= 290:
                    self.arrow_x += self.arrow_speed * self.dt
            else:
                if self.arrow_x >= 55:
                    self.arrow_x -= self.arrow_speed * self.dt
                
                if self.arrow.x < 40:
                    self.arrow_x = 150

            #self.player_texture = pygame.image.load('resources/fishing2.png')

        self.zone.topleft = (self.posx, 55)
        self.arrow.topleft = (self.arrow_x, 50)
    # Отрисовка объектов
    def draw(self, screen, color):
        pygame.draw.line(screen, color, (50, 50), (300, 50))
        pygame.draw.line(screen, color, (50, 100), (300, 100))
        pygame.draw.line(screen, color, (50, 50), (50, 100))
        pygame.draw.line(screen, color, (300, 50), (300, 100))

        # Шкала 
        pygame.draw.line(screen, color, (50, 150), (300, 150))
        pygame.draw.line(screen, color, (50, 200), (300, 200))
        pygame.draw.line(screen, color, (50, 150), (50, 200))
        pygame.draw.line(screen, color, (300, 150), (300, 200))

        pygame.draw.rect(screen, color, (55, 155, self.points, 40))
        
        # Эти 2 штуки должны быть доступны во всем классе. Сделай также как и модель игрока, там просто
        pygame.draw.rect(screen, color, self.zone)
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)

    def force_draw(self, screen):
        screen.blit(self.text, (1280-200, 50))

        screen.blit(self.player_texture, self.player_model)

        if self.lock == 0 and self.pizda == 1 and self.fuck_u <= 1.5:
            self.text2 = self.font.render(str(self.fuck_u), True, (255, 255, 100))
            screen.blit(self.text2, (500, 100))
        if self.lock == 0 and self.pizda == 1 and self.fuck_u > 1.5:
            self.text2 = self.font.render(str(self.fuck_u), True, (255, 0, 0))
            screen.blit(self.text2, (500, 100))

    # Возврат состояния рыбалки игрока
    def isFishing(self):
        return self.isFishing

fishing_menu = Fishing()

def fishing(screen, color):
    if fishing_menu.meow == 0:
        fishing_menu.rain.set_volume(0.3)
        fishing_menu.rain.play(-1)
        fishing_menu.meow = 1

    fishing_menu.keybinds()
    fishing_menu.force_draw(screen)

    if fishing_menu.isFishing:
        fishing_menu.random()
        fishing_menu.draw(screen, color)
        fishing_menu.update()
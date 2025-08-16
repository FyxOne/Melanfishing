import pygame
import random
import time
import audio
import utils

class Fishing:
    def __init__(self): 
        self.isFishing = False
        self.isKeyPressed = False
        self.posx = 55
        self.direction = 0
        self.arrow_x = 140  # начальная позиция стрелки ближе к центру
        self.zone = pygame.Rect(self.posx, 55, 30, 40)
        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)

        self.points = 0
        self.fish = 0

        self.clock = pygame.time.Clock()
        self.arrow_speed = 0.1
        self.zone_speed = 0.05
        
        self.start_time = pygame.time.get_ticks()
        self.startstart_time = pygame.time.get_ticks()

        self.dt = 0
        self.wait_time = 5

        self.pizda = 0
        self.lock = 0
        self.start = 0
        self.reaction = 0
        self.fuck_u = 0
        self.meow = 0

        pygame.font.init()
        self.font = pygame.font.Font(utils.resource_path("resources/EpilepsySans.ttf"), 30)
        self.text = self.font.render("My fishies: " + str(self.fish), True, (255, 255, 100))

        try:
            self.klujet = pygame.mixer.Sound(utils.resource_path("resources/klujet.mp3"))
            self.katushka = pygame.mixer.Sound(utils.resource_path("resources/katushka.mp3"))
            self.katushka.set_volume(0.1)
            self.rain = pygame.mixer.Sound(utils.resource_path("resources/rain.mp3"))
        except Exception as e:
            print("[fishing] audio load error:", e)
            self.klujet = self.katushka = self.rain = None

        self.player_model = pygame.Rect(0, 0, 1280, 720)
        self.texture_fishing1 = pygame.image.load(utils.resource_path("resources/fishing1.png"))
        self.texture_fishing2 = pygame.image.load(utils.resource_path("resources/fishing2.png"))
        self.texture_fishing3 = pygame.image.load(utils.resource_path("resources/fishing3.png"))
        self.player_texture = self.texture_fishing1
        
    def getFishes(self):
        return self.fish
        
    def keybinds(self, mouse_buttons):
        pipipi = self.wait_time - (pygame.time.get_ticks() - self.startstart_time) // 1000
        if pipipi <= 0:
            if self.pizda == 0:
                self.start = time.time()
                print("РЫБА НАХУЙ!")
                self.pizda = 1
                if self.klujet:
                    audio.channel(audio.FX).play(self.klujet)

            if self.lock != 1:
                self.fuck_u = time.time() - self.start
                if mouse_buttons[2]:
                    self.reaction = time.time() - self.start
                    print(self.reaction)

                    self.arrow_x = 140
                    self.posx = 55
                    self.zone.topleft = (self.posx, 55)
                    self.arrow.topleft = (self.arrow_x, 50)

                    if self.reaction < 1:
                        if self.katushka:
                            audio.channel(audio.ENGINE).play(self.katushka, loops=-1)
                        self.player_texture = self.texture_fishing2
                        if not self.isKeyPressed:
                            self.isKeyPressed = True
                            self.lock = 1
                            if not self.isFishing:
                                self.isFishing = True
                    else:
                        print("ебать ты окунь")
                        self.pizda = 0
                        if self.klujet:
                            audio.channel(audio.FX).stop()
                        self.startstart_time = pygame.time.get_ticks()
                else:
                    self.isKeyPressed = False

    def random(self):
        pi_pi = 1 - (pygame.time.get_ticks() - self.start_time) // 1000
        if pi_pi <= 0:
            self.start_time = pygame.time.get_ticks()
            self.direction = random.randint(1, 2)

        if self.direction == 1:
            self.posx += self.zone_speed * self.dt
            if self.posx > 220:
                self.direction = 2
        if self.direction == 2:
            self.posx -= self.zone_speed * self.dt
            if self.posx < 60:
                self.direction = 1

    def update(self, keys, mouse_buttons):
        self.dt = self.clock.tick(60)

        # защита от глюка стрелки — если слишком далеко, вернуть в дефолт
        if self.arrow_x > 300 or self.arrow_x < 40:
            self.arrow_x = 140

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
            self.player_texture = self.texture_fishing1
            self.startstart_time = pygame.time.get_ticks()
            audio.channel(audio.ENGINE).stop()
            if self.klujet:
                audio.channel(audio.FX).play(self.klujet)
            self.wait_time = random.randint(3, 10)

            self.arrow_x = 140
            self.posx = 55
            self.zone.topleft = (self.posx, 55)
            self.arrow.topleft = (self.arrow_x, 50)
            self.pizda = 0
            self.lock = 0
            self.text = self.font.render("My fishies: " + str(self.fish), True, (255, 255, 100))
        
        if self.points == 227:
            self.player_texture = self.texture_fishing3

        if self.isFishing:
            if mouse_buttons[0]:
                if self.arrow_x <= 290:
                    self.arrow_x += self.arrow_speed * self.dt
            else:
                if self.arrow_x >= 55:
                    self.arrow_x -= self.arrow_speed * self.dt
                if self.arrow.x < 40:
                    self.arrow_x = 150

        self.zone.topleft = (self.posx, 55)
        self.arrow.topleft = (self.arrow_x, 50)

    def draw(self, screen, color):
        pygame.draw.line(screen, color, (50, 50), (300, 50))
        pygame.draw.line(screen, color, (50, 100), (300, 100))
        pygame.draw.line(screen, color, (50, 50), (50, 100))
        pygame.draw.line(screen, color, (300, 50), (300, 100))
        pygame.draw.line(screen, color, (50, 150), (300, 150))
        pygame.draw.line(screen, color, (50, 200), (300, 200))
        pygame.draw.line(screen, color, (50, 150), (50, 200))
        pygame.draw.line(screen, color, (300, 150), (300, 200))
        pygame.draw.rect(screen, color, (55, 155, self.points, 40))
        pygame.draw.rect(screen, color, self.zone)
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)

    def force_draw(self, screen):
        screen.blit(self.text, (1280-200, 50))
        screen.blit(self.player_texture, self.player_model)
        if self.lock == 0 and self.pizda == 1 and self.fuck_u <= 1:
            self.text2 = self.font.render(str(self.fuck_u), True, (255, 255, 100))
            screen.blit(self.text2, (500, 100))
        if self.lock == 0 and self.pizda == 1 and self.fuck_u > 1:
            self.text2 = self.font.render(str(self.fuck_u), True, (255, 0, 0))
            screen.blit(self.text2, (500, 100))
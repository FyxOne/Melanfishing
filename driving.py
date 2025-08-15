
import pygame
import random
import audio

class Driving:
    def __init__(self):
        self.direction = 0
        self.posx = 365

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.car_speed = 0
        self.direction_speed = self.car_speed * 0.3
        self.arrow_x = 985

        self.car_model = pygame.Rect(self.posx, 310, 500, 250)
        self.car_texture = pygame.image.load('resources/car.png')
        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)

        self.dt = 0
        self.points = 0

        self.engine_loaded = False
        self.engine_playing = False
        try:
            self.car_sound = pygame.mixer.Sound("resources/car_sound.mp3")
            self.engine_loaded = True
        except Exception as e:
            print("[driving] audio load error:", e)
            self.car_sound = None

    def _ensure_engine(self):
        if self.engine_loaded and not self.engine_playing:
            ch = audio.channel(audio.ENGINE)
            ch.play(self.car_sound, loops=-1)
            ch.set_volume(0.0)  # start silent
            self.engine_playing = True

    def _update_engine_volume(self):
        if not self.engine_playing:
            return
        ch = audio.channel(audio.ENGINE)
        # Volume proportional to speed
        ch.set_volume(max(0.0, min(1.0, self.car_speed * 0.5)))

    def getPoints(self):
        return self.points

    def random(self):
        pi_pi = 1 - (pygame.time.get_ticks() - self.start_time) // 1000

        if pi_pi <= 0:
            self.start_time = pygame.time.get_ticks()
            self.direction = random.randint(1, 2)

        if self.direction == 1:
            if self.posx <= 780:
               if self.direction_speed > 0:
                self.posx += self.direction_speed * self.dt

        if self.direction == 2:
            if self.posx >= 0:
                if self.direction_speed > 0:
                    self.posx -= self.direction_speed * self.dt

    def update(self, keys, mouse_buttons):
        self.dt = self.clock.tick(60)

        self._ensure_engine()

        keys = keys
        if keys[pygame.K_d]:
            if self.posx <= 780 and self.car_speed >= 0:
                self.posx += self.car_speed * self.dt
        if keys[pygame.K_a]:
            if self.posx >= 0 and self.car_speed >= 0:
                self.posx -= self.car_speed * self.dt
        if keys[pygame.K_w]:
            if self.car_speed <= 1:
                self.car_speed += 0.01
                self.direction_speed = self.car_speed * 0.3
            if self.car_speed > 1:
                self.car_speed = 1
            if self.arrow_x >= 985 and self.arrow_x <= 1220:
                self.arrow_x = self.car_speed * 235 + 985
        if keys[pygame.K_s]:
            if self.car_speed >= 0:
                self.car_speed -= 0.01
                self.direction_speed = self.car_speed * 0.3
            if self.car_speed < 0:
                self.car_speed = 0
            if self.direction_speed < 0:
                self.direction_speed = 0
            if self.arrow_x >= 985 and self.arrow_x <= 1220:
                self.arrow_x = self.car_speed * 235 + 985

        self.car_model.topleft = (self.posx, 365)
        self.arrow.topleft = (self.arrow_x, 50) 

        if self.points <= 241:
            if self.posx >= 280 and self.posx <= 500:
                self.points += self.car_speed * 0.5
            else:
                if self.points >= 0:
                    self.points -= 5

        self._update_engine_volume()

    def draw(self, screen, color):
        pygame.draw.line(screen, color, (480, 0), (320, 720), 2)
        pygame.draw.line(screen, color, (800, 0), (960, 720), 10)
        pygame.draw.line(screen, color, (160, 0), (0, 180), 5)

        pygame.draw.line(screen, color, (980, 50), (1230, 50))
        pygame.draw.line(screen, color, (980, 100), (1230, 100))
        pygame.draw.line(screen, color, (980, 50), (980, 100))
        pygame.draw.line(screen, color, (1230, 50), (1230, 100))

        pygame.draw.rect(screen, color, (985, 55, self.points, 40))
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)

        screen.blit(self.car_texture, self.car_model)

    def stop_audio(self):
        audio.channel(audio.ENGINE).stop()

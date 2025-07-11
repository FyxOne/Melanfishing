import pygame
import random

class Driving:
    def __init__(self):
        self.isDriving = True

        self.direction = 0
        self.posx = 365

        self.clock = pygame.time.Clock()
        self.direction_speed = 0.1
        self.car_speed = 0.1

        self.car = pygame.Rect(self.posx, 360, 550, 250)

        self.dt = 0

    def random(self):
        pi_pi = 1 - (pygame.time.get_ticks() - self.start_time) // 1000

        if pi_pi <= 0:
            self.start_time = pygame.time.get_ticks()
            self.direction = random.randint(1, 2)

        if self.direction == 1:
            self.posx += self.direction_speed * self.dt

        if self.direction == 2:
            self.posx -= self.direction_speed * self.dt

    def update(self):
        self.dt = self.clock.tick(60)

        keys = pygame.key.get_pressed()
        if self.isDriving:
            if keys[pygame.K_d]:
                self.arrow_x += self.arrow_speed * self.dt
            if keys[pygame.K_a]:
                self.arrow_x -= self.arrow_speed * self.dt

        self.car.topleft = (self.posx, 360)

    def draw(self, screen, color):
        # car не отрисовывается
        pygame.draw.rect(screen, color, (365, 360, 550, 250))

        pygame.draw.line(screen, color, (480, 0), (320, 720))
        pygame.draw.line(screen, color, (800, 0), (960, 720))
        pygame.draw.line(screen, color, (160, 0), (0, 180))

# раян гослинг
def driving():
    pass

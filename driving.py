import pygame
import random

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

        self.car_sound = pygame.mixer.Sound("resources/car_sound.mp3")

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

    def update(self):
        self.dt = self.clock.tick(60)

        keys = pygame.key.get_pressed()
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

        if self.points <= 240:
            if self.posx >= 280 and self.posx <= 500:
                self.points += self.car_speed
            else:
                if self.points >= 0:
                    self.points -= 5

        if self.car_speed > 0:
            self.car_sound.set_volume(self.car_speed)
            self.car_sound.play(-1)
        else:
            self.car_sound.stop()

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

driving_menu = Driving()

def driving(screen, color):
    driving_menu.draw(screen, color)
    driving_menu.random()
    driving_menu.update()

import pygame
import random

class Cooking:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.dt = 0

        self.btn_x = random.randint(310, 1180)
        self.btn_y = random.randint(0, 620)

        self.posx = 0
        self.arrow_x = 55
        self.points = 0

        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)
        self.btn = pygame.Rect(self.btn_x, self.btn_y, 100, 100)
        self.stir_btn = pygame.Rect(50, 150, 250, 50)

    def getPoints(self):
        return self.points
        
    def random(self):
        pi_pi = 1 - (pygame.time.get_ticks() - self.start_time) // 1000

        if pi_pi <= 0:
            self.start_time = pygame.time.get_ticks()
            self.btn_x = random.randint(0, 1180)
            self.btn_y = random.randint(0, 620)


    def update(self):
        self.dt = self.clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.btn.collidepoint(mouse_pos) and mouse_buttons[0]:
            if self.points < 240:
                self.points += 5
            self.btn_x = random.randint(310, 1180)
            self.btn_y = random.randint(0, 620)

            self.btn.topleft = (self.btn_x, self.btn_y)

        if self.stir_btn.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.arrow_x = 55

        if self.arrow_x < 290:
            self.arrow_x += 0.25
        if self.arrow_x == 290:
            if self.points > 0:
                self.points -= 0.5

        if self.points > 0:
            self.points -= 0.05

        self.arrow.topleft = (self.arrow_x, 50)


    def draw(self, screen, color):
        pygame.draw.line(screen, color, (50, 50), (300, 50))
        pygame.draw.line(screen, color, (50, 100), (300, 100))
        pygame.draw.line(screen, color, (50, 50), (50, 100))
        pygame.draw.line(screen, color, (300, 50), (300, 100))

        pygame.draw.rect(screen, color, (55, 55, self.points, 40))
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)
        pygame.draw.rect(screen, color, self.stir_btn)

        pygame.draw.rect(screen, color, self.btn)

cooking_menu = Cooking()

def cooking(screen, color):
    cooking_menu.draw(screen, color)
    cooking_menu.random()
    cooking_menu.update()

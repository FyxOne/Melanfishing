import pygame
import random

class Cooking:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.dt = 0

        self.btn_x = random.randint(310, 1180)
        self.btn_y = random.randint(0, 275)

        self.posx = 0
        self.arrow_x = 55
        self.points = 0

        self.arrow = pygame.Rect(self.arrow_x, 50, 5, 50)
        self.btn_model = pygame.Rect(self.btn_x, self.btn_y, 100, 100)
        self.btn_texture = pygame.image.load('resources/add_fire.png')
        self.stir_btn = pygame.Rect(50, 150, 250, 50)

        self.pan1 = pygame.image.load('resources/pan1.png')
        self.pan2 = pygame.image.load('resources/pan2.png')
        self.pan_model = pygame.Rect(0, 0, 1280, 720)
        self.pan_texture = self.pan1

        self.font = pygame.font.Font("resources/EpilepsySans.ttf", 30)
        self.text = self.font.render("Stir", True, (15, 0, 50))

    def getPoints(self):
        return self.points
    


    def update(self):
        self.dt = self.clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.btn_model.collidepoint(mouse_pos) and mouse_buttons[0]:
            if self.points < 240:
                self.points += 5
            self.btn_x = random.randint(310, 1180)
            self.btn_y = random.randint(0, 275)

            self.btn_model.topleft = (self.btn_x, self.btn_y)

        if self.stir_btn.collidepoint(mouse_pos) and mouse_buttons[0]:
            if self.arrow_x > 56:
                if self.pan_texture == self.pan1:
                    self.pan_texture = self.pan2
                else:
                    self.pan_texture = self.pan1
            self.arrow_x = 55

        if self.arrow_x < 290:
            self.arrow_x += 0.5
        if self.arrow_x == 290:
            if self.points > 0:
                self.points -= 0.5

        if self.points > 0:
            self.points -= 0.1

        self.arrow.topleft = (self.arrow_x, 50)


    def draw(self, screen, color):
        pygame.draw.line(screen, color, (50, 50), (300, 50))
        pygame.draw.line(screen, color, (50, 100), (300, 100))
        pygame.draw.line(screen, color, (50, 50), (50, 100))
        pygame.draw.line(screen, color, (300, 50), (300, 100))

        pygame.draw.rect(screen, color, (55, 55, self.points, 40))
        pygame.draw.rect(screen, (255, 0, 0), self.arrow)

        pygame.draw.rect(screen, color, self.stir_btn)
        text_rect = self.text.get_rect(center=self.stir_btn.center)
        screen.blit(self.text, text_rect)

        screen.blit(self.pan_texture, self.pan_model)
        screen.blit(self.btn_texture, self.btn_model)

cooking_menu = Cooking()

def cooking(screen, color):
    cooking_menu.draw(screen, color)
    cooking_menu.update()

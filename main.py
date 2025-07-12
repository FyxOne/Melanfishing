import pygame
import os

import menu
import fishing
import driving

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Melanfishing")
    icon = pygame.image.load("resources/logo.png")
    pygame.display.set_icon(icon)
    isOpen = True

    clock = pygame.time.Clock()
    speed = 15

    DarkPurple  = (15, 0, 50)
    LightYellow = (255, 255, 100)

    x, y = 500, 500

    state = "menu"

    while isOpen: 
        pygame.time.Clock().tick(60)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isOpen = False

            # Если кнопка нажата
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "menu":
                    # Если мышь находится на play_button - тогда условие верно
                    if menu.play_button.btn.collidepoint(mouse_pos):
                        # вот тут логика нажатия
                        print("Button is working")
                        state = "fishing"
                
                    if menu.quit_button.btn.collidepoint(mouse_pos):
                        isOpen = False

        screen.fill(DarkPurple)

        if state == "menu":
            # рендер и вызов меню
            menu.menu(screen, LightYellow)
        if state == "fishing":
            fishing.fishing(screen, LightYellow)
            if fishing.fishing_menu.getFishes() == 5:
                state = "driving"
        if state == "driving":
            driving.driving(screen, LightYellow)
            if driving.driving_menu.getPoints() == 240:
                state = "menu"

        pygame.display.flip()
            

if __name__ == "__main__":
    main()

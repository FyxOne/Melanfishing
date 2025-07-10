import pygame
import menu
import game
import fishing

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Симулятор пня")
    isOpen = True

    #цвета
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    DarkPurple  = (15, 0, 50)
    LightYellow = (255, 255, 100)

    x, y = 500, 500

    state = "menu"

    while isOpen: 
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
                        state = "game"
                
                    if menu.quit_button.btn.collidepoint(mouse_pos):
                        isOpen = False

        screen.fill(DarkPurple)

        if state == "menu":
            # рендер и вызов меню
            menu.menu(screen, LightYellow)
        if state == "game":
            fishing.fishing(screen, LightYellow)

        pygame.display.flip()
            

if __name__ == "__main__":
    main()

import pygame
import os

import menu
import splashes
import audio
import control

import fishing as fishing_mod
import driving as driving_mod
import cooking as cooking_mod
import utils

import sys
# Ensure working directory is next to the .exe (PyInstaller) or project folder (source)
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))
def main():
    pygame.init()
    pygame.mixer.init()
    audio.init()

    screen = pygame.display.set_mode((1280, 720))
    splash = splashes.generate_randrom_spalsh()
    pygame.display.set_caption(f"Melanfishing | {splash}")
    icon = pygame.image.load(utils.resource_path("resources/logo.png"))
    pygame.display.set_icon(icon)
    isOpen = True

    fishing_menu = fishing_mod.Fishing()
    driving_menu = driving_mod.Driving()
    cooking_menu = cooking_mod.Cooking()

    audio.play_music(volume=0.1)
    controls = control.TouchControls(1280, 720)

    clock = pygame.time.Clock()
    DarkPurple  = (15, 0, 50)
    LightYellow = (255, 255, 100)

    state = "menu"
    debug = False

    while isOpen:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isOpen = False
            controls.process_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "menu":
                    if menu.play_button.btn.collidepoint(event.pos):
                        state = "fishing"
                    if menu.quit_button.btn.collidepoint(event.pos):
                        isOpen = False
            if event.type == pygame.KEYDOWN:
                keys_hw = pygame.key.get_pressed()
                if keys_hw[pygame.K_d] and keys_hw[pygame.K_LALT]:
                    debug = not debug
                    if not debug:
                        pygame.display.set_caption(f"Melanfishing | {splash}")

        # combine input
        keys_hw = pygame.key.get_pressed()
        mouse_hw = pygame.mouse.get_pressed()
        keys_touch = controls.get_keys()
        mouse_touch = controls.get_mouse()
        keys = [keys_hw[i] or keys_touch[i] for i in range(len(keys_hw))]
        mouse_buttons = tuple(mouse_hw[i] or mouse_touch[i] for i in range(3))

        screen.fill(DarkPurple)

        if state == "menu":
            menu.menu(screen, LightYellow)
        elif state == "fishing":
            fishing_menu.keybinds(mouse_buttons)
            fishing_menu.force_draw(screen)
            if fishing_menu.isFishing:
                fishing_menu.random()
                fishing_menu.draw(screen, LightYellow)
                fishing_menu.update(keys, mouse_buttons)
            if fishing_menu.getFishes() == 3:
                state = "driving"
        elif state == "driving":
            driving_menu.draw(screen, LightYellow)
            driving_menu.random()
            driving_menu.update(keys, mouse_buttons)
            if driving_menu.getPoints() > 239:
                state = "cooking"
        elif state == "cooking":
            cooking_menu.draw(screen, LightYellow)
            cooking_menu.update(keys, mouse_buttons)
            if cooking_menu.getPoints() > 239:
                cooking_menu.stop_audio()
                state = "menu"

        if debug:
            pygame.display.set_caption(f"Melanfishing | {splash} | DEBUG: {clock.get_fps()}")

        controls.draw(screen)
        pygame.display.flip()

    audio.stop_all()
    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
import os

class TouchControls:
    def __init__(self, screen_width=1280, screen_height=720):
        self.sw = screen_width
        self.sh = screen_height
        size = 80
        margin = 20

        # Позиции крестовины
        self.btn_left = pygame.Rect(margin, self.sh - margin - size*2, size, size)
        self.btn_right = pygame.Rect(margin + size*2, self.sh - margin - size*2, size, size)
        self.btn_up = pygame.Rect(margin + size, self.sh - margin - size*3, size, size)
        self.btn_down = pygame.Rect(margin + size, self.sh - margin - size, size, size)

        # Высота кнопок A/B такая же, как у кнопок влево/вправо
        ab_y = self.sh - margin - size*2
        # Кнопка A — справа
        self.btn_a = pygame.Rect(self.sw - margin - size, ab_y, size, size)
        # Кнопка B — левее A на size + margin
        self.btn_b = pygame.Rect(self.sw - margin - size*2 - margin, ab_y, size, size)

        # Состояния
        self.key_w = False
        self.key_a = False
        self.key_s = False
        self.key_d = False
        self.mouse_left = False
        self.mouse_right = False

        # Загрузка текстур
        try:
            self.tex_arrow = pygame.image.load(os.path.join("resources", "arrow_btn.png")).convert_alpha()
            self.tex_a = pygame.image.load(os.path.join("resources", "a_btn.png")).convert_alpha()
            self.tex_b = pygame.image.load(os.path.join("resources", "b_btn.png")).convert_alpha()
        except Exception as e:
            print("[control] Ошибка загрузки текстур кнопок:", e)
            self.tex_arrow = self.tex_a = self.tex_b = None

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_press(event.pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_press(event.pos, False)

    def _handle_press(self, pos, pressed):
        if self.btn_up.collidepoint(pos):
            self.key_w = pressed
        if self.btn_down.collidepoint(pos):
            self.key_s = pressed
        if self.btn_left.collidepoint(pos):
            self.key_a = pressed
        if self.btn_right.collidepoint(pos):
            self.key_d = pressed
        if self.btn_a.collidepoint(pos):
            self.mouse_left = pressed
        if self.btn_b.collidepoint(pos):
            self.mouse_right = pressed

    def get_keys(self):
        keys = [0] * 512
        if self.key_w: keys[pygame.K_w] = 1
        if self.key_a: keys[pygame.K_a] = 1
        if self.key_s: keys[pygame.K_s] = 1
        if self.key_d: keys[pygame.K_d] = 1
        return keys

    def get_mouse(self):
        return (
            1 if self.mouse_left else 0,
            0,
            1 if self.mouse_right else 0
        )

    def draw(self, screen):
        if self.tex_arrow:
            # Крестовина
            up_img = pygame.transform.scale(self.tex_arrow, self.btn_up.size)
            down_img = pygame.transform.rotate(up_img, 180)
            left_img = pygame.transform.rotate(up_img, 90)
            right_img = pygame.transform.rotate(up_img, -90)

            screen.blit(up_img, self.btn_up.topleft)
            screen.blit(down_img, self.btn_down.topleft)
            screen.blit(left_img, self.btn_left.topleft)
            screen.blit(right_img, self.btn_right.topleft)
        else:
            # Рисуем простые эллипсы, если текстура не загрузилась
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_up)
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_down)
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_left)
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_right)

        # Кнопки A и B
        if self.tex_a:
            a_img = pygame.transform.scale(self.tex_a, self.btn_a.size)
            screen.blit(a_img, self.btn_a.topleft)
        else:
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_a)

        if self.tex_b:
            b_img = pygame.transform.scale(self.tex_b, self.btn_b.size)
            screen.blit(b_img, self.btn_b.topleft)
        else:
            pygame.draw.ellipse(screen, (255,255,255,100), self.btn_b)

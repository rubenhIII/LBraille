import os
import sys
import json
import pygame
from perfil import get_color
from entorno_instalacion import base_path

class GameUI:
    def __init__(self):
        self.user = None
        self.screen = None
        self.font = None

    def ui_tutorial(self, screen, font):
        options = ["Juego", "Tutorial", "Ranking", "Salir"]
        selected = 0
        last_selected = -1
        last_tts_time = 0
        ruta = os.path.join(base_path, "sys", "alfabeto.json")
        with open(ruta, "r") as file:
            alphabet = json.load(file)
        letters = alphabet["BASE"]
        while True:
            for i, option in enumerate(letters):
                color = get_color("CL_TEXTO_RES") if i == selected else get_color("CL_TEXTO")
                self.draw_text(option, font, color, screen, 40, 100 + i * 50)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_BACKSPACE]:
                        selected -= 1 % len(options)
                    elif event.key in [pygame.K_DOWN, pygame.K_SPACE]:
                        selected += 1 % len(options)
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def draw_text(self, text, font, color, surface, x, y):
        obj = font.render(text, True, color)
        rect = obj.get_rect(topleft=(x, y))
        surface.blit(obj, rect)
    
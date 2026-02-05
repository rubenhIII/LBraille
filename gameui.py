import os
import sys
import json
import pygame

from perfil import get_color
from speaker import sp
from entorno_instalacion import base_path

class GameUI:
    def __init__(self):
        self.user = None
        self.screen = None
        self.font = None

    def ui_tutorial(self, screen, font):
        ruta = os.path.join(base_path, "sys", "alfabeto.json")
        with open(ruta, "r") as file:
            alphabet = json.load(file)
        letters = alphabet["BASE"]
        self.draw_menu("Tutorial", letters, screen, font)
        

    def draw_menu(self, title: str, options: dict, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Método para renderizar un menú en base a una lista de opciones
        
        :param options: Diccionario de opciones del menú - Opción: Acción
        :type options: dictionary
        :param screen: Surface de pygame
        :type screen: pygame.Surface
        :param font: Fuente del texto de pygame
        :type font: pygame.font.Font
        """

        action = list(options.values())
        options = list(options.keys())

        scroll = 0
        scroll_steps = 8 # Number of options by screen
        selected = 0
        last_selected = -1
        last_tts_time = pygame.time.get_ticks()

        screen.fill(get_color("CL_FONDO"))
        self.draw_text(title, font, get_color("CL_TEXTO"), screen, 20, 20)
        sp.speak_async(title)

        while True:
            for i, option in enumerate(options[scroll:min((scroll+scroll_steps),len(options))]):
                color = get_color("CL_TEXTO_RES") if (i+scroll) == selected else get_color("CL_TEXTO")
                self.draw_text(option, font, color, screen, 40, 100 + i * 50)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_BACKSPACE]:
                        selected = (selected - 1) % len(options)
                    elif event.key in [pygame.K_DOWN, pygame.K_SPACE]:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        print(action[selected])
                        sp.speak_async(str(action[selected]))


            if (selected != last_selected) and (pygame.time.get_ticks() - last_tts_time >= 200):
                # Circular menu algorithm
                if selected == 0 and selected != scroll:
                    scroll = 0
                    screen.fill(get_color("CL_FONDO"))
                    self.draw_text(title, font, get_color("CL_TEXTO"), screen, 20, 20)
                elif selected == (len(options) - 1) and scroll != (len(options) // scroll_steps * scroll_steps):
                    scroll = len(options) // scroll_steps * scroll_steps
                    screen.fill(get_color("CL_FONDO"))
                    self.draw_text(title, font, get_color("CL_TEXTO"), screen, 20, 20)
                elif selected >= (scroll+scroll_steps):
                    scroll = (scroll + scroll_steps) % (len(options)+scroll_steps-1)
                    screen.fill(get_color("CL_FONDO"))
                    self.draw_text(title, font, get_color("CL_TEXTO"), screen, 20, 20)
                elif selected < scroll:
                    scroll = (scroll - scroll_steps)  % (len(options)+scroll_steps-1)
                    screen.fill(get_color("CL_FONDO"))
                    self.draw_text(title, font, get_color("CL_TEXTO"), screen, 20, 20)

                last_selected = selected
                last_tts_time = pygame.time.get_ticks()
                sp.speak_async(options[selected])

    def draw_text(self, text, font, color, surface, x, y):
        obj = font.render(text, True, color)
        rect = obj.get_rect(topleft=(x, y))
        surface.blit(obj, rect)
    
import pygame
import sys
from speaker import sp
from juego import juego
from tutorial import jugar_tutorial
from configuracion import configuracion_menu
from ranking import mostrar_ranking
from perfil import get_color
import os
from entorno_instalacion import base_path


def reproducir_ding():
    try:
        ding = pygame.mixer.Sound(os.path.join(base_path, "sys", "ding.mp3"))
        ding.play()
    except Exception as e:
        print(f"Error reproduciendo ding: {e}")


def draw_text(text, font, color, surface, x, y):
    obj = font.render(text, True, color)
    rect = obj.get_rect(topleft=(x, y))
    surface.blit(obj, rect)


def menu(usuario, screen, font):
    options = ["Juego", "Tutorial", "Ranking", "Salir"]
    selected = 0
    last_selected = -1
    last_tts_time = 0

    # Reproducir sonido al entrar
    reproducir_ding()
    sp.speak_async("Menú principal")

    #if sp.speak_async(options[selected]) == False:
    #    print("El engine no está disponible")
    #else:
    #    print("El engine SI está disponible")

    while True:
        current_time = pygame.time.get_ticks()
        screen.fill(get_color("CL_FONDO"))
        draw_text("Menú Principal", font, get_color("CL_TEXTO"), screen, 20, 20)

        for i, option in enumerate(options):
            color = get_color("CL_TEXTO_RES") if i == selected else get_color("CL_TEXTO")
            draw_text(option, font, color, screen, 40, 100 + i * 50)

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
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        for games in range(5):
                            juego(usuario, screen, font)
                        sp.speak_async("Juego finalizado")
                    elif selected == 1:
                        configuracion_menu(usuario, screen, font)
                    elif selected == 2:
                        mostrar_ranking(usuario, screen, font)
                    elif selected == 3:
                        pygame.quit()
                        sys.exit()
                    reproducir_ding()
                    sp.speak_async("Menú principal")
                    sp.speak_async(options[selected])

        if selected != last_selected and (current_time - last_tts_time) > 200:
            sp.speak_async(options[selected])
            last_selected = selected
            last_tts_time = current_time

        pygame.time.delay(30)

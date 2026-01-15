import pygame
from perfil import cargar_perfil, guardar_perfil, get_color
from entorno_instalacion import base_path

def configuracion_menu(usuario, screen, font):
    config = cargar_perfil(usuario)
    options = [
        lambda: f"Nivel: {config['nivel']}",
        lambda: f"Máx errores: {config['max_mistakes']}",
        lambda: f"Mayúsculas sensibles: {'Sí' if config['case_sensitive'] else 'No'}",
        lambda: "Volver"
    ]
    selected = 0

    while True:
        screen.fill(get_color("CL_FONDO"))
        draw_text("Configuración", font, get_color("CL_TEXTO"), screen, 20, 20)

        for i, opt in enumerate(options):
            color = get_color("CL_TEXTO_RES") if i == selected else get_color("CL_TEXTO")
            draw_text(opt(), font, color, screen, 40, 100 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        config['nivel'] = (config['nivel'] % 12) + 1
                    elif selected == 1:
                        config['max_mistakes'] = (config['max_mistakes'] % 10) + 1
                    elif selected == 2:
                        config['case_sensitive'] = not config['case_sensitive']
                    elif selected == 3:
                        guardar_perfil(usuario, config)
                        return
                elif event.key == pygame.K_LEFT:
                    if selected == 0:
                        config['nivel'] = ((config['nivel'] - 2) % 12) + 1
                    elif selected == 1:
                        config['max_mistakes'] = ((config['max_mistakes'] - 2) % 10) + 1
                    elif selected == 2:
                        config['case_sensitive'] = not config['case_sensitive']

def draw_text(text, font, color, surface, x, y):
    obj = font.render(text, True, color)
    rect = obj.get_rect(topleft=(x, y))
    surface.blit(obj, rect)

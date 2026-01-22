import os
import json
import pygame
#from tts import speak_async
from speaker import sp
from entorno_instalacion import base_path

folder = {"users": "usr"}


def pedir_texto(pantalla, fuente, mensaje):
    entrada = ""
    reloj = pygame.time.Clock()
    sp.speak_async(mensaje)

    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render(mensaje, True, (255, 255, 255))
        pantalla.blit(texto, (50, 150))

        cuadro = pygame.Rect(50, 250, 400, 50)
        pygame.draw.rect(pantalla, (255, 255, 255), cuadro, 2)
        render_entrada = fuente.render(entrada, True, (255, 255, 255))
        pantalla.blit(render_entrada, (cuadro.x + 10, cuadro.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return entrada.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                else:
                    entrada += evento.unicode
        reloj.tick(30)


def login_o_registrar_usuario(pantalla, fuente):
    sp.speak_async("¿Ya tienes un usuario? Presiona S para sí, N para no")
    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render("¿Ya tienes un usuario? (S/N)", True, (255, 255, 255))
        pantalla.blit(texto, (50, 200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return login(pantalla, fuente)
                elif event.key == pygame.K_n:
                    return registrar(pantalla, fuente)


def login(pantalla, fuente):
    while True:
        nombre = pedir_texto(pantalla, fuente, "Ingresa tu nombre de usuario:")
        #ruta = os.path.join(base_path, folder["users"], f"{nombre}.json")
        ruta = os.path.join(folder["users"], f"{nombre}.json")
        if os.path.exists(ruta):
            sp.speak_async(f"Bienvenido de nuevo, {nombre}")
            return nombre
        else:
            sp.speak_async("Usuario no encontrado. ¿Deseas registrarte con ese nombre? S o N")
            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            return registrar_con_nombre(pantalla, fuente, nombre)
                        elif event.key == pygame.K_n:
                            esperando = False

def registrar(pantalla, fuente):
    while True:
        nombre = pedir_texto(pantalla, fuente, "Escribe tu nuevo nombre de usuario:")
        #ruta = os.path.join(base_path, folder["users"], f"{nombre}.json")
        ruta = os.path.join(folder["users"], f"{nombre}.json")
        if os.path.exists(ruta):
            sp.speak_async("Ese nombre ya está en uso. ¿Deseas iniciar sesión con ese nombre? S o N")
            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            return nombre
                        elif event.key == pygame.K_n:
                            esperando = False
        else:
            sp.speak_async(f"Usuario {nombre} registrado correctamente.")
            from perfil import default_config
            with open(ruta, 'w') as f:
                json.dump(default_config.copy(), f, indent=4)
            return nombre

def registrar_con_nombre(pantalla, fuente, nombre):
    #ruta = os.path.join(base_path, folder["users"], f"{nombre}.json")
    ruta = os.path.join(folder["users"], f"{nombre}.json")
    sp.speak_async(f"Usuario {nombre} registrado correctamente.")
    from perfil import default_config
    with open(ruta, 'w') as f:
        json.dump(default_config.copy(), f, indent=4)
    return nombre
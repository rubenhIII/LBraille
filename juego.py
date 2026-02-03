import os
import random
import pygame
from time import sleep
from perfil import cargar_perfil, guardar_perfil, get_color, get_configuracion
from entorno_instalacion import base_path
from speaker import sp

folder = {"audio": "sounds", "users": "usr"}


def sonido_systema(f, volumen=0.5):
    path = os.path.join(base_path, "sys", f)
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(volumen)
    return sonido


def calcular_puntaje(nivel, tiempoPorCaracter):
    return int((nivel * 10) + (5 / max(tiempoPorCaracter, 0.5)))


def actualizar_puntaje(config, puntos_ganados):
    from datetime import datetime
    hoy = datetime.now().date()
    ultima_actualizacion = config.get("ultima_actualizacion")

    if ultima_actualizacion:
        ultima_fecha = datetime.strptime(ultima_actualizacion, "%Y-%m-%d").date()
        dias_sin_jugar = (hoy - ultima_fecha).days

        if dias_sin_jugar > get_configuracion()["DIAS_PENALIZACION"]:
            penalizacion = (dias_sin_jugar - get_configuracion()["DIAS_PENALIZACION"]) * get_configuracion()["PUNTOS_PENALIZACION_POR_DIA"]
            config["puntos"] = max(0, config["puntos"] - penalizacion)

    if ultima_actualizacion != str(hoy):
        config["puntos_hoy"] = 0

    if config["puntos_hoy"] + puntos_ganados > get_configuracion()["PUNTOS_DIARIOS_MAX"]:
        puntos_ganados = max(0, get_configuracion()["PUNTOS_DIARIOS_MAX"] - config["puntos_hoy"])

    config["puntos"] += puntos_ganados
    config["puntos_hoy"] += puntos_ganados
    config["ultima_actualizacion"] = str(hoy)
    return config


def juego(usuario, screen, font):
    config = cargar_perfil(usuario)

    win_sound = sonido_systema("correct.mp3", volumen=0.5)
    lose_sound = sonido_systema("incorrect.mp3", volumen=0.5)
    beep_sound = sonido_systema("lose_buzzer.mp3", volumen=0.5)
    incorrect_sound = sonido_systema("incorrect_buzz.mp3", volumen=0.5)

    files = [f for f in os.listdir(os.path.join(folder["audio"])) if os.path.isfile(os.path.join(folder["audio"], f))]
    min_length = max(1, int(0.4 * config["nivel"]))
    max_length = config["nivel"]
    filtered_words = [word for word in files if min_length <= len(word) - 4 <= max_length]

    if not filtered_words:
        print("No hay palabras disponibles.")
        return

    f = random.choice(filtered_words)
    word = os.path.splitext(f)[0] if not config["case_sensitive"] else os.path.splitext(f)[0].lower()
    tiempo_limite = config["tiempoPorCaracter"] * len(word) * 1000
    sonado_ultimo_segundo = [False, False, False]

    typed = ""
    mistakes = 0

    pygame.mixer.init()
    audio_path = os.path.join(folder["audio"], f)
    if os.path.exists(audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

    jugando = True
    tiempo_inicio = pygame.time.get_ticks()

    while jugando:
        screen.fill(get_color("CL_FONDO"))
        draw_text(f"Palabra: {word}", font, get_color("CL_TEXTO"), screen, 20, 100)
        draw_text(f"Escrito: {typed}", font, get_color("CL_TEXTO_RES"), screen, 20, 200)
        draw_text(f"Errores: {mistakes}", font, get_color("CL_TEXTO_ADV"), screen, 20, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.TEXTINPUT:
                char = event.text
                correct_char = word[len(typed):len(typed) + 1]
                if char == correct_char or (not config["case_sensitive"] and char.lower() == correct_char):
                    win_sound.play()
                    typed += char
                else:
                    incorrect_sound.play()
                    mistakes += 1

                if typed == word:
                    win_sound.play()
                    puntos = calcular_puntaje(config["nivel"], config["tiempoPorCaracter"])
                    config = actualizar_puntaje(config, puntos)
                    guardar_perfil(usuario, config)
                    mostrar_mensaje(screen, font, "¡Palabra completada!", get_color("CL_TEXTO_RES"))
                    sp.speak_async("¡Correcto!")
                    sleep(2.5)
                    return
                if mistakes >= config["max_mistakes"]:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()  # detener la palabra si sigue sonando

                    if not pygame.mixer.get_busy():
                        lose_sound.play()
                    mostrar_mensaje(screen, font, "¡Demasiados errores!", get_color("CL_TEXTO_ADV"))
                    sp.speak_async("¡Demasiados errores!")
                    sleep(2.5)
                    return

        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = max(0, tiempo_limite - (tiempo_actual - tiempo_inicio))
        if tiempo_restante <= 3005:
            segundos_restantes = tiempo_restante // 1000
            if segundos_restantes in [3, 2, 1] and not sonado_ultimo_segundo[3 - segundos_restantes]:
                beep_sound.play()
                sonado_ultimo_segundo[3 - segundos_restantes] = True

        if tiempo_restante <= 0:
            mostrar_mensaje(screen, font, "¡Tiempo agotado!", get_color("CL_TEXTO_ADV"))
            sp.speak_async("Tiempo Agotado!")
            sleep(2.5)
            return


def draw_text(text, font, color, surface, x, y):
    obj = font.render(text, True, color)
    rect = obj.get_rect(topleft=(x, y))
    surface.blit(obj, rect)


def mostrar_mensaje(screen, font, mensaje, color):
    screen.fill(get_color("CL_FONDO"))
    text = font.render(mensaje, True, color)
    screen.blit(text, (400 - text.get_width() // 2, 300))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.mixer.music.stop()

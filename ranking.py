import os
import json
import pygame
from perfil import get_color
from tts import speak_async
from entorno_instalacion import base_path

folder = {"users": "usr"}


def ranking_usuarios():
    usuarios = []
    for archivo in os.listdir(folder["users"]):
        if archivo.endswith(".json"):
            path = os.path.join(base_path, folder["users"], archivo)
            with open(path, "r") as f:
                datos = json.load(f)
                usuarios.append((archivo[:-5], datos.get("puntos", 0)))
    usuarios.sort(key=lambda x: x[1], reverse=True)
    return usuarios

def mostrar_ranking(nombre_usuario, pantalla, fuente):
    ranking = ranking_usuarios()
    pantalla.fill(get_color("CL_FONDO"))

    # Título
    titulo = fuente.render("Ranking de Usuarios", True, get_color("CL_TEXTO"))
    pantalla.blit(titulo, (400 - titulo.get_width() // 2, 20))

    # Mostrar top 5 en pantalla
    y_offset = 80
    for i, (usuario, puntos) in enumerate(ranking[:5], 1):
        texto = f"{i}. {usuario}: {puntos} puntos"
        if usuario == nombre_usuario:
            texto += " <- Tú"
        linea = fuente.render(texto, True, get_color("CL_TEXTO"))
        pantalla.blit(linea, (50, y_offset))
        y_offset += 30

    # Obtener posición real del usuario y datos
    posicion = next((i + 1 for i, (u, _) in enumerate(ranking) if u == nombre_usuario), None)
    tu_usuario = next((u for u in ranking if u[0] == nombre_usuario), None)

    pygame.display.flip()

    # Preparar mensaje de voz
    if posicion and tu_usuario:
        mensaje = f"Estás en el puesto número {posicion} con {tu_usuario[1]} puntos."
    else:
        mensaje = "No se encontró tu puntaje."

    # Siempre anunciar el top 3 por voz también
    top_voz = " Los mejores son: "
    for i, (usuario, puntos) in enumerate(ranking[:3], 1):
        top_voz += f"Puesto {i}, {usuario} con {puntos} puntos. "

    speak_async(mensaje + top_voz)

    # Esperar tecla para continuar
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                esperando = False

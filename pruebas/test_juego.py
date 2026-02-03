import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from auth import login_o_registrar_usuario
from menu import menu
import pygame
from perfil import cargar_configuracion_global

# Inicializar Pygame y pantalla
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aprender a usar el teclado")

# Fuente global
font = pygame.font.Font(None, 40)

# Obtener usuario desde login o registro
usuario = "Ruben"

# Cargar configuración inicial (para tamaños y colores)
cargar_configuracion_global()

# Iniciar menú
menu(usuario, screen, font)

# Cerrar Pygame al salir
pygame.quit()
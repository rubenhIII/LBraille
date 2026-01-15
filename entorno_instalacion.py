import sys
import os

# Determinar si estamos en un ejecutable
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Ruta temporal de PyInstaller
else:
    base_path = os.path.dirname(__file__)
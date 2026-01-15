import os
import json
from datetime import datetime
from entorno_instalacion import base_path

folder = {"system": "sys", "users": "usr"}

# Valores por omisión para perfiles nuevos
default_config = {
    "nivel": 2,
    "max_mistakes": 5,
    "case_sensitive": False,
    "tiempoPorCaracter": 5,
    "puntos": 0,
    "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d"),
    "puntos_hoy": 0
}

# Configuración global
_configuracion = {}


def cargar_configuracion_global(nombre_archivo="config.json"):
    global _configuracion
    ruta = os.path.join(base_path, folder["system"], nombre_archivo)
    por_defecto = {
        "PUNTOS_DIARIOS_MAX": 200,
        "DIAS_PENALIZACION": 5,
        "PUNTOS_PENALIZACION_POR_DIA": 10,
        "WIDTH": 800,
        "HEIGHT": 600,
        "COLORES": {
            "CL_FONDO": [0, 0, 0],
            "CL_TEXTO": [255, 255, 255],
            "CL_TEXTO_RES": [0, 255, 0],
            "CL_TEXTO_ADV": [255, 0, 0]
        }
    }
    try:
        with open(ruta, "r") as archivo:
            _configuracion = json.load(archivo)
            # Asegurar que todo esté presente
            for key, value in por_defecto.items():
                if key not in _configuracion:
                    _configuracion[key] = value
    except Exception as e:
        print(f"Error cargando config global: {e}")
        _configuracion = por_defecto



def cargar_perfil(usuario):
    ruta = os.path.join(base_path, folder["users"], f"{usuario}.json")
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    else:
        return default_config.copy()


def guardar_perfil(usuario, config):
    ruta = os.path.join(base_path, folder["users"], f"{usuario}.json")
    with open(ruta, "w") as f:
        json.dump(config, f, indent=4)


def get_color(nombre):
    return tuple(get_configuracion()["COLORES"].get(nombre, [255, 255, 255]))


def get_configuracion():
    return _configuracion
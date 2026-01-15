# LBraille - Proyecto Educativo Modularizado

LBraille es una aplicación educativa en Python + Pygame para practicar la escritura de palabras mediante audio y texto, con soporte para perfiles de usuario, puntuación y configuración personalizada.

---

## 🚀 Ejecución del proyecto

### 1. **Requisitos previos**

* Python 3.7+
* Las siguientes bibliotecas deben estar instaladas:

  ```bash
  pip install pygame pyttsx3
  ```

### 2. **Estructura del proyecto**

```
LBraille/
├── main.py                  # Punto de entrada
├── auth.py                  # Inicio de sesión y registro de usuarios
├── perfil.py                # Manejo de perfiles de usuario y configuración
├── juego.py                 # Juego principal
├── menu.py                  # Menú principal de navegación
├── configuracion.py         # Configuración personalizada del usuario
├── ranking.py               # Ranking de puntajes entre usuarios
├── tts.py                   # Manejo de voz asíncrona
├── usr/                     # Carpeta de usuarios con archivos JSON
├── sounds/                  # Carpeta de sonidos de palabras
├── sys/                     # Archivos de sistema como aplausos01.wav y config.json
```

### 3. **¿Cuál archivo ejecuto?**

Ejecuta el archivo `main.py`:

```bash
python main.py
```

Este archivo inicializa pygame, pide login o registro, carga el perfil y abre el menú principal.

---

## 👤 Sistema de usuarios

Al iniciar el programa se pregunta si ya tienes usuario:

* Si presionas **S**, podrás iniciar sesión escribiendo tu nombre.
* Si presionas **N**, podrás registrarte con un nuevo nombre (se crea un archivo `usr/TUNOMBRE.json`).

El sistema evitará duplicados y confirmará tus acciones por voz.

---

## 🧠 Funcionalidades destacadas

* ✅ Síntesis de voz con `pyttsx3`
* ✅ Menú accesible con teclado y audio
* ✅ Palabras aleatorias para practicar
* ✅ Sistema de puntaje y penalizaciones por inactividad
* ✅ Configuración personalizada (nivel, errores, sensibilidad)
* ✅ Ranking global entre usuarios

---

## 📁 Datos necesarios

Asegúrate de tener:

* Archivos `.wav` en la carpeta `sounds/` (cada archivo representa una palabra).
* Archivo `config.json` en `sys/` con la configuración base.
* Sonidos auxiliares en `sys/` como:

  * `aplausos01.wav`
  * `lose01.wav`
  * `ouch02.wav`

---

## 🧪 Sugerencia para probar el proyecto

1. Crea las carpetas `usr`, `sounds`, `sys` si no existen.
2. Agrega archivos `.wav` en `sounds` (por ejemplo: `gato.wav`, `casa.wav`, etc.)
3. Agrega el archivo `config.json` en `sys/` (o deja que se use el predeterminado si no está).
4. Ejecuta `main.py`, registra un usuario y comienza a practicar.

---

¡Listo! LBraille ya está modularizado, funcional y listo para crecer. 🎉

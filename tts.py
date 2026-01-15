import pyttsx3
import threading
import queue

"""
<Voice id=roa/es-419
          name=Spanish (Latin America)
          languages=['es-419']
          gender=Male
          age=None>
"""

def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
       
# Inicializar el motor de voz
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.5)
    change_voice(engine, 'es', "Male")
except Exception as e:
    print(f"Error al inicializar pyttsx3: {e}")
    engine = None

# Cola de mensajes
tts_queue = queue.Queue()
stop_tts = threading.Event()
tts_thread = None


def tts_worker():
    while not stop_tts.is_set():
        try:
            texto = tts_queue.get(timeout=0.1)
            if engine:
                try:
                    engine.stop()
                    engine.say(texto)
                    engine.runAndWait()
                except Exception as e:
                    print(f"Error en TTS: {e}")
            tts_queue.task_done()
        except queue.Empty:
            continue


def speak_async(text):
    if engine is None:
        return

    with tts_queue.mutex:
        tts_queue.queue.clear()

    tts_queue.put(text)

    global tts_thread
    if tts_thread is None or not tts_thread.is_alive():
        stop_tts.clear()
        tts_thread = threading.Thread(target=tts_worker, daemon=True)
        tts_thread.start()

import pyttsx4
import threading
import queue

class Speaker:
    def __init__(self):
        self.engine_thread = None
        self.engine = None
        self.language = None # TODO: Poner un lenguaje default. Si no existe obligar a seleccionar uno
        self.gender = "Female"

        self.msg_queue = queue.Queue()
        self.flag = threading.Event()
        self.mutex = threading.Lock()
        self.speaking = False

        self.create_speaker()

    def __del__(self):
        pass

    def change_voice(self, engine, language, gender='VoiceGenderFemale'):
        for voice in engine.getProperty('voices'):
            if language in voice.languages and gender == voice.gender:
                engine.setProperty('voice', voice.id)
                return True
        raise RuntimeError("Lenguaje '{}' para el género '{}' no fue encontrado".format(language, gender))
       
    # Inicializar el motor de voz
    def _onStart(self, name):
        print('Iniciando', name)
        self.speaking = True
    def _onWord(self, name, location, length):
        print('Palabra', name, location, length)
    def _onEnd(self, name, completed):
        print('Finalizando', name, completed)
        self.speaking = False


    def get_engine(self):
        try:
            self.engine = pyttsx4.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.5)

            #self.change_voice(self.engine, 'es-ES', "Female")
            #self.engine.connect('started-utterance', self._onStart)
            #self.engine.connect('started-word', self._onWord)
            #self.engine.connect('finished-utterance', self._onEnd)

        except Exception as e:
            print(f"Error al inicializar pyttsx: {e}")
            self.engine = None
    
    def engine_worker(self):
        while not self.flag.is_set():
            try:
                texto = self.msg_queue.get(timeout=0.1)
                try:
                    self.engine.stop()
                    self.engine.say(texto, texto)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"Error en TTS: {e}")
                self.msg_queue.task_done()
            except queue.Empty:
                continue

    def create_speaker(self):
        self.get_engine()
        if self.engine_thread is None or not self.engine_thread.is_alive():
            try:
                self.engine_thread = threading.Thread(target=self.engine_worker, daemon=True)
                self.engine_thread.start()
                self.flag.clear()
                return True
            except Exception as e:
                print("Error obteniendo hilo", e)
                self.flag.set()
                return False
    
    def speak_async(self, text):
        self.msg_queue.put(text)
        
sp = Speaker()
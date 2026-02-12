from entorno_instalacion import base_path
import pyttsx4
import threading
import queue
import json
import os

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

        self.__default_voice = None

        self.load_configuration()
        self.create_speaker()

    def load_configuration(self):
        conf_path = os.path.join(base_path, "sys", "speaker_conf.json")
        with open(conf_path, "r") as f:
            sp_conf = json.load(f)
            print(sp_conf)
            self.__default_voice = sp_conf["voice_id"]

    def change_voice(self):
        for voice in self.engine.getProperty('voices'):
            if self.__default_voice == voice.id:
                self.engine.setProperty('voice', voice.id)
                self.engine.say("Motor de voz seleccionado")
                self.engine.runAndWait()      
                #print(f"Lenguaje {voice.name} Voz seleccionada {voice}")
                return True
        raise RuntimeError(f"Lenguaje '{self.__default_voice}' no fue encontrado")
       
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
            self.engine.setProperty('volume', 0.8)

            if self.__default_voice != "": self.change_voice()
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
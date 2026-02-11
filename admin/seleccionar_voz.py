import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pyttsx4

class VoiceSelector:
    def __init__(self):
        self.engine = pyttsx4.init()
        self.available_voices = self.get_available_voices()

    def get_current_voice(self):
        return self.engine.getProperty('voice')

    def print_current_voice(self):
        print("Datos de voz actual del motor texto a voz")
        print(self.get_current_voice())
        print("")

    def get_available_voices(self):
        available_voices = {}
        for i, voice in enumerate(self.engine.getProperty('voices')):
            available_voices[str(i)] = voice
        return available_voices

    def print_available_voices(self):
        print("Voces disponibles en el sistema")
        for i, voice in self.available_voices.items():
            print(i)
            print(voice.id)
            print(voice.name)
            print(voice.age)
            print(voice.gender)
            print(voice.languages)
            print("")

    def set_current_voice(self, voice_id):
        voice_selected = self.available_voices[voice_id]
        print(f"Voz elegida {voice_selected}")
        for voice in self.engine.getProperty('voices'):
            if voice_selected.id == voice.id:
                self.engine.setProperty('voice', voice.id)
                vc.engine.say("Nueva voz seleccionada")
                vc.engine.runAndWait()
                return True
        raise RuntimeError("Lenguaje '{}' para el género '{}' no fue encontrado".format(voice_selected.languages, voice_selected.gender))

if __name__ == "__main__":
    vc = VoiceSelector()
    vc.print_available_voices()

    sel = 'y'
    while True:
        vc.print_current_voice()
        sel = input('Introduce la opcion a seleccionar: ')
        if sel == 'q':
            break
        try:
            vc.set_current_voice(sel)
            print(vc.engine.getProperty('voice'))
        except Exception as e:
            print(f"No pudo cambiarse la voz: {e}")

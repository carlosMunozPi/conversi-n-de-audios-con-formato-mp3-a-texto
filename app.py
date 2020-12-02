# ==============================================================
# @autor CarlosMunozPi
# El siguiente codigo convierte audios con formato .mp3 a texto
# 
# input : file_name (archivo .mp3)
# output:  archivo .txt con el texto del audio
# requirements : SpeechRecognition, pydub
# ===============================================================

import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

#file_name = 'audio.mp3'
class audio_to_text():
    def __init__(self, file_name):
        self.file_name = file_name
        self.reconoce = sr.Recognizer()
        self.linea = ['-#-#-#- AUDIO A TEXTO -#-#-#-\n',]
        self.main()
        self.exporta()

    def divide_audio(self):
        long_audio = AudioSegment.from_mp3(self.file_name)
        audio_div = split_on_silence(
            long_audio,  min_silence_len = 500,
            silence_thresh = long_audio.dBFS-11,
            keep_silence=500,
        )
        return audio_div

    def main(self):
        audios = self.divide_audio()
        nrow = 1
        indice = len(str(len(audios)))
        for audio_chunk in audios:
            audio_chunk.export("temp", format="wav")
            with sr.AudioFile("temp") as source:
                audio = self.reconoce.listen(source)
                try:
                    text = self.reconoce.recognize_google(audio)
                    self.linea.append(f'\n{" "*(indice-len(str(nrow)))}{nrow} : {text}')
                    print(f'{" "*(indice-len(str(nrow)))}{nrow} : {text}')
                except Exception as ex:
                    self.linea.append(f'\n{" "*(indice-len(str(nrow)))}{nrow} : No se reconoce fragmento')
                    print(f'{ex}')
            nrow += 1

        self.linea.append("\n-#-#-#-")

    def exporta(self):
        with open('texto.txt','w') as f:
            for i in self.linea:
                f.write(i)

if __name__ == "__main__":
    audio_to_text("audio.mp3")

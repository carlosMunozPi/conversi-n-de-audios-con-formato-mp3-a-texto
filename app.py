import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

file_name = 'audio.mp3'
reconoce = sr.Recognizer()

def divide_audio(filename):
    long_audio = AudioSegment.from_mp3(filename)
    audio_div = split_on_silence(
        long_audio,  min_silence_len = 500,
        silence_thresh = long_audio.dBFS-11,
        keep_silence=500,
    )
    return audio_div

audios = divide_audio(file_name)

linea = ['-#-#-#- AUDIO A TEXTO -#-#-#-\n',]
nrow = 1
indice = len(str(len(audios)))
for audio_chunk in audios:
    audio_chunk.export("temp", format="wav")
    with sr.AudioFile("temp") as source:
        audio = reconoce.listen(source)
        try:
            text = reconoce.recognize_google(audio)
            linea.append(f'\n{" "*(indice-len(str(nrow)))}{nrow} : {text}')
            print(f'{" "*(indice-len(str(nrow)))}{nrow} : {text}')
        except Exception as ex:
            linea.append(f'\n{" "*(indice-len(str(nrow)))}{nrow} : No se reconoce fragmento')
            print(f'{ex}')
    nrow += 1

linea.append("\n-#-#-#-")

with open('resultado/texto.txt','w') as f:
    for i in linea:
        f.write(i)

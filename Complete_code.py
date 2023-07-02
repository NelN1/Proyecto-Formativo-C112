#Importando las librerías necesarias
import sys, os
import time, random
import wave, argparse, pygame
import math
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

# ¿Mostrar un plot del algoritmo en acción?
gShowPlot=False

#Notas de la escala pentatónica menor
#piano C4-E(b)-F-G-B(b)-C5
pmNotes={'C4':261.626,'Eb':311.127,'F':349.228,'G':391.995,'Bb':466.164}
#Diccionario de relación de teclas y notas
keywords={'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4}
#Diccionario en cual las llaves son las frecuencias de las notas y sus valores son colores para las gráficas
frecolor={ 261.626: 'g', 311.127: 'r', 349.228:'c', 391.995: 'm', 466.164:'y'}
#Diccionario con colores RGB
color={0: (241,196,15), 1: (165,105,189), 2: (69,179,157), 3: (220,118,51) , 4: (93,109,126)}
#Tamaño de la ventana de pygame
size=800, 600
#Inicializa la variable white de tipo Tupla que contiene el color blanco en la escala RGB.
white=255,255,255
#Define la función que escribe el archivo WAV
def writeWAVE(fname,data):
    #Abrir archivo
    file=wave.open(fname,'wb')
    #Parámetros del archivo WAV
    nChannels=1
    sampleWidth=2
    frameRate=44100
    nFrames=44100
    #Configurar los parámetros
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

#Define la función que genera una nota a partir de una frecuencia dada.
def generateNote(freq):
    #freq=220
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    #Iniciañiza el buffer circular.
    buf = deque([random.random() - 0.5 for i in range(N)])
    #Muestra la gráfica si el valor de gShowPlot es verdadero.
    if gShowPlot:
        axline, = plt.plot(buf, frecolor[freq])
        plt.pause(3.0)
    #Inicializa el buffer de muestra.
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft() 
    # plot of flag set 
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()
    # Muestra de 16-bit a string
    # El máximo valor es 32767 para 16-bit
    samples = np.array(samples * 32767, 'int16')
    return samples.tobytes()

#Reproduce un archivo WAV
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        #Diccionario de notas
        self.notes = {}
    #Añade una nota al diccionario self.notes
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    #Tocando una nota
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' no encontrado!')
    def playRandom(self):
        """Toca una nota aleatoria"""
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
        return index

#Definiendo a la función principal
def main():
    #Declarando una variable global
    global gShowPlot
    print("""
       |---------------------------------------------------|
       |Generando sonidos con el aloritmo de Karplus-Strong|
       |---------------------------------------------------| 
    """)

    parser=argparse.ArgumentParser(description="Generando sonidos con el algoritmo de Karplus-Strong")
    #Añade argumentos
    parser.add_argument('--mostrar', action='store_true',required=False, help="Este argumento le dice al programa que genere un gráfico.")
    parser.add_argument('--reproducir', action='store_true',required=False, help="Este argumento le dice al programa que genere una melodía aleatoria")
    parser.add_argument('--pcolor', action='store_true',required=False, help="Este argumento le dice al programa que reproduzca música y al mismo tiempo muestre colores que están relacionados a las notas")
    parser.add_argument('--piano', action='store_true',required=False, help="Este argumento le dice al programa que juegue al modo piano")
    args=parser.parse_args()

    #Mostrar gráfico si se ingrese el argumento --mostrar desde la línea de comandos.
    if args.mostrar:
        gShowPlot = True
        plt.ion()

    #Creando una instancia de la clase NotePlayer
    nplayer = NotePlayer()

    print('Creando notas...')
    for name, freq in list(pmNotes.items()):
        fileName=name+'.wav'
        if not os.path.exists(fileName) or args.mostrar:
            data=generateNote(freq)
            print('Creando '+fileName+'...')
            writeWAVE(fileName,data)
        else:
            moreFile=name+'.wav'
            print(fileName+' ya ha sido creado. Saltando al siguiente archivo...')
            #Añade notas al diccionario de la clase.
            nplayer.add(moreFile)
            #Toca una nota si args.mostrar es True
            if args.mostrar:
                nplayer.play(moreFile)
                time.sleep(0.5)
    
    #Solo reproduce una melodía aleatoria
    if args.reproducir:
        while True:
            try:
                nplayer.playRandom()
                #Descansa - 1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
        
    #Reproduce una melodía aleatorio y muestra colores en la ventana
    if args.pcolor:
        pygame.init()
        screen=pygame.display.set_mode(size)
        pygame.display.set_caption("Play mode")
        font=pygame.font.Font('freesansbold.ttf',26)
        text0=font.render('En la terminal, presiona las teclas CTRL+C para salir.',True, 'black')
        text0Rect=text0.get_rect()
        text0Rect.center=(400,100)
        play=True
        while play:
            try:
                screen.fill(color[nplayer.playRandom()])
                time.sleep(2.0)
                pygame.display.flip()
                #Descansa - 1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
            screen.fill(white)
            screen.blit(text0, text0Rect)
            pygame.display.flip()
            pygame.display.update()
    
    #Modo piano
    if args.piano:
        pygame.init()
        screen=pygame.display.set_mode(size)
        pygame.display.set_caption("Piano mode")
        font=pygame.font.Font('freesansbold.ttf',26)
        text=font.render('Key    Note',True, 'black')
        textRect=text.get_rect()
        textRect.center=(380,100)
        text1=font.render('A      C4',True, 'black')
        text1Rect=text1.get_rect()
        text1Rect.center=(380,130)
        text2=font.render('S      Eb',True, 'black')
        text2Rect=text2.get_rect()
        text2Rect.center=(380,160)
        text3=font.render('D      F',True, 'black')
        text3Rect=text3.get_rect()
        text3Rect.center=(373,190)
        text4=font.render('F      G',True, 'black')
        text4Rect=text4.get_rect()
        text4Rect.center=(373,220)
        text5=font.render('G      Bb',True, 'black')
        text5Rect=text5.get_rect()
        text5Rect.center=(380,250)
        text6=font.render('Haz click en \'X\' para salir',True, 'black')
        text6Rect=text6.get_rect()
        text6Rect.center=(380,60)
        run=True
        while run:
            for event in pygame.event.get():
                if(event.type==pygame.KEYUP):
                    if(event.key==pygame.K_a):
                        fname="C4.wav"
                        print("key pressed")
                        nplayer.play(fname)
                        screen.fill(color[0])
                        pygame.display.flip()
                    elif(event.key==pygame.K_s):
                        fname="Eb.wav"
                        print("key pressed")
                        nplayer.play(fname)
                        screen.fill(color[1])
                        pygame.display.flip()
                    elif(event.key==pygame.K_d):
                        fname="F.wav"
                        print("key pressed")
                        nplayer.play(fname)
                        screen.fill(color[2])
                        pygame.display.flip()
                    elif(event.key==pygame.K_f):
                        fname="G.wav"
                        print("key pressed")
                        nplayer.play(fname)
                        screen.fill(color[3])
                        pygame.display.flip()
                    elif(event.key==pygame.K_g):
                        fname="Bb.wav"
                        print("key pressed")
                        nplayer.play(fname)
                        screen.fill(color[4])
                        pygame.display.flip()
                    time.sleep(0.5)
                elif(event.type==pygame.QUIT): run=False
                screen.fill(white)
                screen.blit(text, textRect)
                screen.blit(text1, text1Rect)
                screen.blit(text2, text2Rect)
                screen.blit(text3, text3Rect)
                screen.blit(text4, text4Rect)
                screen.blit(text5, text5Rect)
                screen.blit(text6, text6Rect)
                pygame.display.flip()
                pygame.display.update()
        pygame.quit()
# call main
if __name__=='__main__':
    main()

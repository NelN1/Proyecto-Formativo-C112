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
pmNotes={'C4':262,'Eb':349,'F':349,'G':391,'Bb':466}
#Diccionario de relación de teclas y notas
keywords={'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4}
#Diccionario con colores RGB
color={0: (241,196,15), 1: (165,105,189), 2: (69,179,157), 3: (220,118,51) , 4: (93,109,126)}
#Tamaño de la ventana de pygame
size=800, 600
#color blanco en RGB
white=255,255,255
# write out WAV file
def writeWAVE(fname,data):
    #open file
    file=wave.open(fname,'wb')
    #WAV file parameters
    nChannels=1
    sampleWidth=2
    frameRate=44100
    nFrames=44100
    # set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

# generate note of given frequency
def generateNote(freq):
    #freq=220
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    llave=list(pmNotes.keys())
    indice=list(pmNotes.values()).index(freq)
    # initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    lineal=np.array(range(len(buf)))*0
    # plot a flag set
    if gShowPlot:
        plt.cla()
        arline, = plt.plot(lineal, 'b')
        axline, = plt.plot(buf, 'g')
        plt.title(llave[indice])
        plt.pause(3.0)
    # Inicializa el buffer de muestra
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
    # samples to 16-bit to string
    # max value is 32767 for 16-bit
    samples = np.array(samples * 32767, 'int16')
    return samples.tobytes()

# play a wav file
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # dictionary of notes
        self.notes = {}
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' not found!')
    def playRandom(self):
        """play a random note"""
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
        return index

#main() function
def main():
    #declare global var
    global gShowPlot
    print("""
       |-----------------------------------------------|
       |Generating sounds with Karplus String Algorithm|
       |-----------------------------------------------| 
    """)

    parser=argparse.ArgumentParser(description="Generating sounds with Karplus String Algorithm")
    # add arguments
    parser.add_argument('--display', action='store_true',required=False, help="this command display a graphic.")
    parser.add_argument('--play', action='store_true',required=False, help="This command oly can play the sound clip.")
    parser.add_argument('--pcolor', action='store_true',required=False, help="This command can play the sound clip and shows the relationship of colors and notes in window.")
    parser.add_argument('--piano', action='store_true',required=False, help="Play piand mode.")
    args=parser.parse_args()

    #show plot ut flag set
    if args.display:
        gShowPlot = True
        plt.ion()

    #create note player
    nplayer = NotePlayer()

    print('creating note...')
    for name, freq in list(pmNotes.items()):
        fileName=name+'.wav'
        if not os.path.exists(fileName) or args.display:
            data=generateNote(freq)
            print('creating '+fileName+'...')
            writeWAVE(fileName,data)
        else:
            print('fileName already created. skipping...')
            #add note to player
            nplayer.add(name+'.wav')

            #play note if display flag set
            if args.display:
                nplayer.play(name+'.wav')
                time.sleep(0.5)
    
    #Solo reproduce una melodía aleatoria
    if args.play:
        while True:
            try:
                nplayer.playRandom()
                #rest - 1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
        
    #Reproduce una melodía aleatorio y muestra colores en la ventana
    if args.pcolor:
        pygame.init()
        screen=pygame.display.set_mode(size)
        pygame.display.set_caption("Play mode")
        play=True
        while play:
            try:
                screen.fill(color[nplayer.playRandom()])
                time.sleep(2.0)
                pygame.display.flip()
                #rest - 1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
            screen.fill(white)
            pygame.display.flip()
    #random piano mode
    
    if args.piano:
        pygame.init()
        screen=pygame.display.set_mode(size)
        pygame.display.set_caption("Piano mode")
        font=pygame.font.Font('freesansbold.ttf',26)
        text=font.render('Press the keys A, S, D, F or G',True, 'black')
        textRect=text.get_rect()
        textRect.center=(400,300)
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
                pygame.display.flip()
                pygame.display.update()
        pygame.quit()
# call main
if __name__=='__main__':
    main()

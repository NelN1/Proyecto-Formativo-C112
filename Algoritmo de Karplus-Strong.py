import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque
#Genera una nota de una frecuencia dada
def generateNote(freq):
    #freq=220
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    #Inicializa un búfer cicular
    buf = deque([random.random() - 0.5 for i in range(N)])
    #Inicializa una muestra del búfer
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft() 
    #Muestra el gráfico si el valor de gShowPlot es True
        if gShowPlot:
            if i % 1000 == 0:
                plt.axline.set_ydata(buf)
                plt.draw()
    #Muestra de 16-bit a string
    #Máximo valor is 32767 para 16-bit
        samples = np.array(samples * 32767, 'int16')
        print(samples.tostring())
    return samples.tostring()
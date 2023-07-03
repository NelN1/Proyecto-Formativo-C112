import random
import numpy as np
from collections import deque
from IPython.display import Audio

# Frecuencias de la escala pentatÃ³nica menor (piano C4-Eb-F-G-Bb-C5)
pentatonic_notes = {
    'C4': 261.626,
    'Eb': 311.127,
    'F': 349.228,
    'G': 391.995,
    'Bb': 466.164
}

def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    buf = deque([random.random() - 0.5 for i in range(N)])

    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()

    samples = np.array(samples * 32767, 'int16')
    return samples

for note_name, freq in pentatonic_notes.items():
    print(note_name)
    note = generateNote(freq)
    display(Audio(note, rate=44100))

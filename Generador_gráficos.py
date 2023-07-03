import time
import random
import wave
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import sounddevice as sd
import os

# Configuración de tamaño del gráfico
size = (6, 3)

# Notas pentatónicas
pentatonic_notes = {
    'A': 0,
    'C': 3,
    'D': 5,
    'E': 7,
    'G': 10
}

# Función para generar una nota utilizando el algoritmo de Karplus-Strong
def generate_note_freq(freq):
    sample_rate = 44100
    duration = 1.0
    delay = sample_rate / freq

    # Crea una lista de muestras iniciales aleatorias
    samples = [random.uniform(-1, 1) for _ in range(int(delay))]
    samples = deque(samples)

    # Genera las muestras de la nota
    num_samples = int(sample_rate * duration * 0.01)
    for _ in range(num_samples):
        sample = 0.5 * (samples[0] + samples[1])
        samples.append(sample)
        samples.popleft()

    # Normaliza las muestras entre -32767 y 32767 (rango de valores de 16 bits)
    samples = np.array(samples) * 32767 / max(abs(max(samples)), abs(min(samples)))
    samples = samples.astype(np.int16)

    return samples

# Función para guardar una nota en un archivo WAV
def write_wav_file(filename, samples):
    with wave.open(filename, 'w') as wave_file:
        wave_file.setnchannels(1)  # Mono
        wave_file.setsampwidth(2)  # 16 bits por muestra
        wave_file.setframerate(44100)  # Tasa de muestreo de 44100 Hz
        wave_file.writeframes(samples.tobytes())

# Función para reproducir el audio de una nota
def play_audio(samples):
    sd.play(samples, samplerate=44100)

# Función para visualizar el gráfico de onda de una nota
def visualize_wave(samples, color):
    plt.figure(figsize=size)
    plt.plot(samples, color=color)
    plt.axis('off')
    plt.show()

# Función principal
def main():
    print("""
       |---------------------------------------------------|
       |Generando sonidos con el algoritmo de Karplus-Strong|
       |---------------------------------------------------|
    """)

    # Crea y guarda las notas pentatónicas
    print('Creando notas pentatónicas...')
    for note, shift in pentatonic_notes.items():
        filename = note + '.wav'
        if not os.path.exists(filename):
            frequency = 440.0 * 2 ** (shift / 12)
            samples = generate_note_freq(frequency)
            print('Creando ' + filename + '...')
            write_wav_file(filename, samples)
        else:
            print(filename + ' ya ha sido creado. Saltando al siguiente archivo...')

    # Reproduce y visualiza las notas pentatónicas
    try:
        for _ in range(5):  # Reproducir 5 notas pentatónicas
            note = random.choice(list(pentatonic_notes.keys()))
            filename = note + '.wav'
            samples = generate_note_freq(440.0 * 2 ** (pentatonic_notes[note] / 12))
            color = random.choice(['blue', 'red', 'green', 'yellow', 'orange'])
            play_audio(samples)
            visualize_wave(samples, color)
            time.sleep(1)  # Esperar 1 segundo entre notas
    except KeyboardInterrupt:
        sd.stop()

# Llamada a la función principal
if __name__ == '__main__':
    main()

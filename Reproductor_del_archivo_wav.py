import pygame
import random
# reproducir un archivo wav
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # diccionario de notas
        self.notes = {}
    # Agrega una nota
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # tocar una nota
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' not found!')
    def playRandom(self):
        """tocar una nota al azar"""
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
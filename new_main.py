def main():
    parser=argparse.ArgumentParser(description="Generating sounds with Karplus String Algorithm")
    #Añade cuatro argumentos opcionales para inicializar
    parser.add_argument('--display', action='store_true',required=False)
    parser.add_argument('--play', action='store_true',required=False)
    parser.add_argument('--piano', action='store_true',required=False)
    args=parser.parse_args()

    #Muestra gráficos si el argumento --mostrar se ingreso por la línea de comandos
    if args.display:
        gShowPlot = True
        plt.ion()

    #Crear una instancia de la clase NotePlayer
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
            #Añade notas al diccionario de la clase NotePlayer.
            nplayer.add(name+'.wav')

            #Reproduce una nota si el valor de args.display es True.
            if args.display:
                nplayer.play(name+'.wav')
                time.sleep(0.5)

    #Reproduce una melodía aleatoria
    if args.play:
        while True:
            try:
                nplayer.playRandom()
                #Descansa de 1 a 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
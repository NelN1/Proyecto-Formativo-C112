def writeWAVE(fname,data):
    #abrir documento
    file=wave.open(fname,'wb')
    #Parámetros del archivo WAV
    nChannels=1
    sampleWidth=2
    frameRate=44100
    nFrames=44100
    #establecer parámetros
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()
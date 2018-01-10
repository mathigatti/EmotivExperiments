from psychopy import visual, core, event, gui, data
from psychopy import parallel
from random import shuffle,randint
import datetime
import time
import gtk
from marcas import *

# Marcas
marca_espacio       = 11
marca_fantasma      = 2
marca_pacman        = 1
marca_fin_trial     = 22
marca_inicio        = 41
marca_fin_bloque    = 32
marca_final         = 42

def addGoesStimulus(shuffledStimulusList):
    for j in range(len(shuffledStimulusList)):
        if shuffledStimulusList[j] == 1:
            shuffledStimulusList[j] = randint(1,4)
            shuffle(shuffledStimulusList)

def imagesToShow(shuffledStimulusList, stimuli):
    image = []

    for pos in range(0,len(shuffledStimulusList)):
        image.append(stimuli[0])
        if shuffledStimulusList[pos] == 1 :
            image[pos] = stimuli[1]
        if shuffledStimulusList[pos] == 2 :
            image[pos] = stimuli[2]
        if shuffledStimulusList[pos] == 3 :
            image[pos] = stimuli[3]
        if shuffledStimulusList[pos] == 4 :
            image[pos] = stimuli[4]

    return image

def isOddNumber(i):
    return  i % 2 == 1

def isEvenNumber(i):
    return not isOddNumber(i)

def loadInitialScreenAndFlip(win, pantalla_inicio, negro, res):
    pantini = visual.ImageStim(win, image=pantalla_inicio, units= 'pix', size = (700,471), contrast=1.0, opacity=1.0)
    msg1 = visual.TextStim(win, text="[Presione ENTER para continuar]", pos =((res[0]*0.15),(-res[1]*0.45)), color=negro, colorSpace='hex')
    pantini.draw()
    msg1.draw()
    win.flip()

def loadEndingExperimentScreenAndFlip(win, negro, res, cond):
    fondo = visual.Rect(win, width=res[0]+10, height=res[1]+10, fillColor=negro, fillColorSpace='hex')
    if cond == 'pacman':
        msg1 = visual.TextStim(win, text="MUY BIEN!! FIN DE DE LA PRIMERA PARTE", color=blanco, colorSpace='hex',alignHoriz='center', alignVert='center')
        msg2 = visual.TextStim(win, text="Muchas gracias por participar!", pos=(0.0,(-res[1]*0.05)), color=blanco, colorSpace='hex')
    elif cond == 'angry':
        msg1 = visual.TextStim(win, text="MUY BIEN!! YA TERMINO EL JUEGO", color=blanco, colorSpace='hex',alignHoriz='center', alignVert='center')
        msg2 = visual.TextStim(win, text="Muchas gracias por participar!", pos=(0.0,(-res[1]*0.05)), color=blanco, colorSpace='hex')

    fondo.draw()
    msg1.draw()
    msg2.draw()
    win.flip()


def loadEndingMessageAndFlip(win, res, negro, blanco):
    fondo = visual.Rect(win, width=res[0]+10, height=res[1]+10, fillColor=negro, fillColorSpace='hex')
    msg1 = visual.TextStim(win, text="FIN DE PRACTICA", color=blanco, colorSpace='hex', alignHoriz='center', alignVert='center')
    fondo.draw()
    msg1.draw()
    win.flip()

def loadRestingMessageAndFlip(win, negro):
    win.clearBuffer()
    msg = visual.TextStim(win, text="Aprovecha este momento para descansar la vista", color=negro, colorSpace='hex', alignHoriz='center', alignVert='center')
    msg.draw()
    win.flip()

def loadInterStimulusImageAndFlip(win):
    loadInterStimulusImage(win)
    win.flip()

def loadStimulusImage(win,image):
    msg = visual.ImageStim(win, image=image, units= 'deg', size = (8.84,8.84),contrast=1.0, opacity=1.0)
    msg.draw()


def loadInterStimulusImage(win):
    msg = visual.ImageStim(win, image="./estimulo/cruz.png", units= 'deg', size = (2.0,2.0), contrast=1.0, opacity=1.0)
    msg.draw()

def loadInstructionsAndFlip(win, negro, blanco, res):
    fondo = visual.Rect(win, width=res[0]+10, height=res[1]+10, fillColor=negro, fillColorSpace='hex')
    msg1 = visual.TextStim(win, text="BLOQUE " + str(i/2+1), pos=(-200, 240), color=blanco, colorSpace='hex')
    msg2 = visual.TextStim(win, text="tecla [ n ] para continuar", color=blanco, colorSpace='hex',alignHoriz='center', alignVert='center')
    msg3 = visual.TextStim(win, text="tecla [ t ] para pasar al siguiente bloque", pos=(0.0,(-res[1]*0.05)), color=blanco, colorSpace='hex')
    msg4 = visual.TextStim(win, text="tecla [ q ] para salir", pos=(0.0,(-res[1]*0.10)), color=blanco, colorSpace='hex')
    fondo.draw()
    msg1.draw()
    msg2.draw()
    msg3.draw()
    msg4.draw()
    win.flip()

def isDivisibleBy(i,n):
    return i % n == 0

def preparationScreensExperiment(esperar, terminar, termino_bloque, isFirst, negro, blanco, res, pantalla_inicio, win, core, Nsess, dataFile):

    win.clearBuffer()
    while esperar:
        if isDivisibleBy(i,3):
            if termino_bloque:
                termino_bloque = False
                loadInterStimulusImageAndFlip(win)
                core.wait(1)

            loadInitialScreenAndFlip(win, pantalla_inicio, negro, res)
            event.waitKeys(keyList=['return'])

            loadInstructionsAndFlip(win, negro, blanco, res)
            keys = event.waitKeys(keyList=['q','t','n'])

            for key in keys:
                if key == 'q':
                    marcas(q,p,marca_final)
                    dataFile
                    keysToString = "; ".join(str(x) for x in keys)
                    dataFile.write(keysToString)
                    dataFile.close()
                    win.close()
                    core.quit()
                    time.sleep(1)
                    break
                elif key == 't':
                    i = i + 3
                    t_presionada = True
                    if i >= Nsess:
                        esperar = 0
                        terminar = 1
                        break
                elif key == 'n':
                    esperar = 0
                    win.color=gris

        else:
            win.clearBuffer()
            loadRestingMessageAndFlip(win, negro)
            time.sleep(3)
            esperar = 0

    return esperar, terminar, termino_bloque, isFirst, dataFile

def preparationScreens(esperar, terminar, termino_bloque, isFirst, negro, blanco, res, pantalla_inicio, win, core, Nsess):
    while esperar:
        if isFirst:
            isFirst = False
            loadInitialScreenAndFlip(win, pantalla_inicio, negro, res)
            event.waitKeys(keyList=['return'])

        if isEvenNumber(i):
            if termino_bloque:
                termino_bloque = False
                loadInterStimulusImageAndFlip(win)
                core.wait(1)

            loadInstructionsAndFlip(win, negro, blanco, res)
            keys = event.waitKeys(keyList=['q','t','n'])

            for key in keys:
                if key == 'q':
                    win.close()
                    core.quit()
                    break
                elif key == 't':
                    i = i + 2
                    if i >= Nsess:
                        terminar = 1
                        esperar = 0
                elif key == 'n':
                    win.color= gris
                    esperar = 0

        else:
            loadRestingMessageAndFlip(win, negro)
            time.sleep(3)
            esperar = 0

    return esperar, terminar, termino_bloque, isFirst

def anIterationOfTheExperimentGame(primera_iter, initTime, win, imagen, ISI, StimDur, initTimeStamp, q, p):

    # Pongo la cruz
    win.flip()
    c = initTime.getTime()

    tiempo = []

    if primera_iter:
        c = initTimeStamp
        primera_iter = False

    tiempo.append(c)

    # Preparo la imagen
    loadStimulusImage(win,imagen[k])

    # Espero
    while initTime.getTime() < (ISI + c):
        if event.getKeys(timeStamped=initTime, keyList=['space']):
            print "Mando marca", marca_espacio, time.time()
            marcas(q,p,marca_espacio)

    # Pongo la imagen
    win.flip()
    a = initTime.getTime()

    if (imagen[k] == "./estimulo/PACMAN.png"):
        marcas(q,p,marca_pacman)
    else:
        marcas(q,p,marca_fantasma)
    tiempo.append(a)
    tiempos.append(tiempo)

    # Preparo la cruz
    loadInterStimulusImage(win)

    # Espero
    while initTime.getTime() < (StimDur + a):
        if event.getKeys(timeStamped=initTime, keyList=['space']):
            marcas(q,p,marca_espacio)

    return primera_iter

def anIterationOfTheGame(primera_iter, initTime, win, imagen, ISI, StimDur, initTimeStamp):

    # Pongo la cruz
    win.flip()
    c = initTime.getTime()

    if primera_iter:
        c = initTimeStamp
        primera_iter = False

    # Preparo la imagen
    loadStimulusImage(win,imagen[k])

    # Espero
    while initTime.getTime() < (ISI + c):
        if event.getKeys(timeStamped=initTime, keyList=['space']):
            True

    # Pongo la imagenDD/MM/AA
    win.flip()
    a = initTime.getTime()

    # Preparo la cruz
    loadInterStimulusImage(win)

    # Espero
    while initTime.getTime() < (StimDur + a):
        if event.getKeys(timeStamped=initTime, keyList=['space']):
            True

    return primera_iter


def gameScreens(primera_iter, initTime, res, win, gris, imagen, ISI, StimDur, shuffledStimulusList):
    fondo = visual.Rect(win, width=res[0]+10, height=res[1]+10, fillColor=gris, fillColorSpace='hex')
    loadInterStimulusImage(win)

    initTime.reset()
    initTimeStamp = initTime.getTime()

    # Ciclo de cada sesion
    for k in xrange(len(shuffledStimulusList)):
        primera_iter = anIterationOfTheGame(primera_iter, initTime, win, imagen, ISI, StimDur, initTimeStamp)

    return primera_iter


def experimentGameScreens(primera_iter, initTime, res, win, gris, imagen, ISI, StimDur, shuffledStimulusList, q, p):
    fondo = visual.Rect(win, width=res[0]+10, height=res[1]+10, fillColor=gris, fillColorSpace='hex')
    loadInterStimulusImage(win)

    initTime.reset()

    if isDivisibleBy(i,3):
        marca_inicio = 100
    else: marca_inicio = 20

    initTimeStamp = initTime.getTime()

    marcas(q,p,marca_inicio)

    # ciclo de cada sesion
    for k in xrange(len(shuffledStimulusList)):
        primera_iter = anIterationOfTheExperimentGame(primera_iter, initTime, win, imagen, ISI, StimDur, initTimeStamp, q, p, marca_espacio)

    return primera_iter

def run_training(win, proporcion, pruebas, Nsess, StimDur, ISI,res,gris,negro,blanco,stimuli,pantalla_inicio):

    # Estimulos
    noGoes = int(proporcion*pruebas);

    stimulusList = [1 for i in xrange(pruebas-noGoes)] + [0 for i in xrange(noGoes)]
    initTime = core.Clock()
    isFirst = True

    i = 0
    while i < Nsess:
        shuffledStimulusList = list(stimulusList)

        addGoesStimulus(shuffledStimulusList)

        imagen = imagesToShow(shuffledStimulusList, stimuli)

        esperar = 1
        terminar = 0
        termino_bloque = False

        esperar, terminar, termino_bloque, isFirst = preparationScreens(esperar, terminar, termino_bloque, isFirst, negro, blanco, res, pantalla_inicio, win, core, Nsess)

        if not terminar:

                primera_iter = True

                primera_iter = gameScreens(primera_iter, initTime, win, imagen, ISI, StimDur, shuffledStimulusList)

                # Pongo la ultima cruz
                win.flip()
                c = initTime.getTime()

                # Espero
                while initTime.getTime() < (ISI + c):
                    True

        # siguiente sesion
        if isOddNumber(i):
            termino_bloque = True
        i = i + 1

    loadInitialScreenAndFlip(win, pantalla_inicio, negro, res)
    core.wait(4)

def finalMark(cond):
    if cond == 'angry':
        return 42
    elif cond == 'pacman':
        return 142
    else:
        raise Exception("Invalid condition please choose 'angry' or 'pacman'")

def run_experiment(dataFile, win, proporcion, pruebas, Nsess, StimDur, ISI, q, p,res,gris,negro,blanco,stimuli,pantalla_inicio,cond):

    marca_final = finalMark(cond)

    # Estimulos
    noGoes = int(proporcion*pruebas);

    stimulusList = [1 for i in xrange(pruebas-noGoes)] + [0 for i in xrange(noGoes)]

    initTime = core.Clock()

    keys = []

    i = 0
    while i < Nsess:
        shuffledStimulusList = list(stimulusList)

        addGoesStimulus(shuffledStimulusList)

        imagen = imagesToShow(shuffledStimulusList, stimuli)

        esperar = 1
        terminar = 0
        termino_bloque = False

        win.clearBuffer()
        esperar, terminar, termino_bloque, isFirst, dataFile = preparationScreensExperiment(esperar, terminar, termino_bloque, isFirst, negro, blanco, res, pantalla_inicio, win, core, Nsess,dataFile)

        if not terminar:
            tiempos = []
            primera_iter = True

            primera_iter = experimentGameScreens(primera_iter, initTime, res, win, gris, imagen, ISI, StimDur, shuffledStimulusList, q, p)

            # Pongo la ultima cruz
            win.flip()
            c = initTime.getTime()

            # Espero
            while initTime.getTime() < (ISI + c):
                if event.getKeys(timeStamped=initTime, keyList=['space']):
                    marcas(q,p,marca_espacio)

            if isDivisibleBy(i,3):
                marcas(q,p,marca_fin_bloque)
                termino_bloque = True
            else:
                marcas(q,p,marca_fin_trial)

            # almaceno datos
            keys = keys + ['; Sesion ' + str(i+1)] + ['La lista generada fue: ' + str(shuffledStimulusList)] + ['Apariciones de las imagenes: '] + tiempos

            # siguiente sesion
            i = i + 1

    loadEndingExperimentScreenAndFlip(win, negro, res, cond)

    marcas(q,p,marca_final)
    core.wait(4)

    keysToString = "; ".join(str(x) for x in keys)
    dataFile
    dataFile.write(keysToString)

    if cond == 'angry':
        dataFile.close()
        win.close()
        core.quit()


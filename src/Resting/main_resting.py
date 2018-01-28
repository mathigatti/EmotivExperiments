from __future__ import division
from psychopy import visual, core, event, gui, data
from psychopy.tools.filetools import fromFile, toFile
import datetime
import time
import os
from marcas import *
from random import randint
from resting import *

VIDEOS = ['./videos/video1.mp4','./videos/video2.mp4','./videos/video3.mp4','./videos/video4.mp4','./videos/video5.mp4']

def experimentForm():
	# INFO SUJETO
	expInfo = {NAME:'nombre',BIRTHDATE:'DD/MM/AA',VIDEO:'0', EXPERIMENT_TYPE:'conductual',OPERATOR:''}

	# Presento cuadro para rellenar
	dlg = gui.DlgFromDict(expInfo, title='Formulario')
	if not(dlg.OK):
		core.quit()
	else:
		fileName = expInfo[NAME]
		if not os.path.exists(DATA_PATH + fileName):
			os.makedirs(DATA_PATH + fileName)
		nombreEDF = DATA_PATH + fileName + "/" + str(datetime.date.today()) + '_' + fileName
		fileName = DATA_PATH + fileName + '/' + str(datetime.date.today()) + '_' +fileName+'.csv'
		dataFile = open(fileName, 'a')
		texto = expInfo[NAME] + '; ' + str(datetime.datetime.now()) + '; ' + expInfo[BIRTHDATE] + '; ' + expInfo[VIDEO] + '; ' + expInfo[EXPERIMENT_TYPE] + '; ' + expInfo[OPERATOR] 
	dataFile.write(texto)

	return expInfo

def chooseVideo(video):
	if video == '0':
		return randint(0,4)
	else:
		try:
			return int(video) - 1
		except:
			raise Exception("Invalid video")

def setWindow():
	panCompleta = True
	win = visual.Window([], monitor="testMonitor", units="pix",  color='#808080', colorSpace='hex', fullscr=panCompleta)
	win.setMouseVisible(False)
	#win = visual.Window((800, 600))
	return win

def setMovie(win, video):
	movie = visual.MovieStim(win, video, size=(1280, 720), flipVert=False, flipHoriz=False, loop=False)
	print('orig movie size=%s' % movie.size)
	print('duration=%.2fs' % movie.duration)
	return movie

def insertMarks(expInfo):
	ponermarcas  = []
	if expInfo[EXPERIMENT_TYPE] == EMOTIV:
		from multiprocessing import Process, Queue
		import guardar
		q_marcas = Queue()
		p = Process(target = guardar.save_data, args=(nombreEDF, q_marcas, ))
		p.start()
		ponermarcas = 1
	elif expInfo[EXPERIMENT_TYPE] == TRADITIONAL_EEG:
		from parallel import Parallel # Version sugerida por Fede (ver mail 02/08/2016)
		q_marcas = Parallel() # Version sugerida por Fede (ver mail 02/08/2016)
		q_marcas.setData(0) # Solo para asegurarse de que arranque con todos los pins abajo
		ponermarcas = 2
	elif expInfo[EXPERIMENT_TYPE] == CONDUCTUAL:
		q_marcas = 1
		ponermarcas = 0
	return ponermarcas, q_marcas

def main():
	expInfo = experimentForm()
	
	n = chooseVideo(expInfo[VIDEO])

	win = setWindow()
	movie = setMovie(win, VIDEOS[n])

	ponermarcas, q_marcas = insertMarks(expInfo)
	correr_resting(win,movie,q_marcas,ponermarcas)
	
	win.close()
	core.quit()

if __name__ == "__main__":
	main()

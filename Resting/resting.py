from __future__ import division
from psychopy import visual, core, event, gui, data
import time
import marcas
from marcas import *
from constants import *

def correr_resting(win,mov,q_marcas,ponermarcas): #q_marcas,ponermarcas):

	inicio = core.Clock()
	marcas(q_marcas,ponermarcas,M_INICIO)

	while mov.status != visual.FINISHED:
		mov.draw()
		win.flip()
		marcas(q_marcas,ponermarcas,M_INICIO)
		if event.getKeys(timeStamped=inicio, keyList=['p']):
			mov.pause()
			marcas(q_marcas,ponermarcas,M_INICIO_PAUSA)
			event.waitKeys(timeStamped=inicio, keyList=['p'])
			mov.play()
			marcas(q_marcas,ponermarcas,M_FINAL_PAUSA)
		elif event.getKeys(timeStamped=inicio, keyList=['q']):
			break
			marcas(q_marcas,ponermarcas,M_FINAL)
	marcas(q_marcas,ponermarcas,M_FINAL)


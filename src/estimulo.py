from psychopy import visual, core, event, gui, data
from random import shuffle,randint
import datetime
import time
#import numpy as np
#import math
#from psychopy.tools.filetools import fromFile, toFile

def correr_experimento(infoSesion, q, win):
	# Inicializo parametros del experimento
	proporcion = 0.7
	pruebas = 10
	Nsess = infoSesion[1]

	dataFile = infoSesion[0]		
	
	# Tiempos
	StimDur = 0.2
	ISI = 1


	# Marcas

	marca_espacio		= 1
	marca_fantasma		= 10
	marca_pacman		= 11
	marca_fin_trial		= 30
	marca_inicio		= 100
	marca_fin_bloque	= 200
	marca_final		= 300

	# Estimulos
	producto = int(proporcion*pruebas);

	lista = [1 for i in xrange(pruebas-producto)] + [0 for i in xrange(producto)]

	inicio = core.Clock()

	teclas = []

	i = 0
	primero = True
	while i < Nsess:
		listaMezclada = list(lista)
	
		for j in range(len(listaMezclada)):
			if listaMezclada[j] == 1:
				listaMezclada[j] = randint(1,4)
		shuffle(listaMezclada)

		imagen = []
		for pos in range(0,len(listaMezclada)):
			imagen.append("./estimulo/PACMAN.png")
			if listaMezclada[pos] == 1 :
				imagen[pos] = "./estimulo/FANTASMA_AZUL.png"	
			if listaMezclada[pos] == 2 :
				imagen[pos] = "./estimulo/FANTASMA_NARANJA.png"	
			if listaMezclada[pos] == 3 :
				imagen[pos] = "./estimulo/FANTASMA_ROJO.png"	
			if listaMezclada[pos] == 4 :
				imagen[pos] = "./estimulo/FANTASMA_VERDE.png"

		esperar = 1
		termino_bloque = False
		win.clearBuffer()					
		while esperar:
			if (primero):
				msg = visual.ImageStim(win, image="./estimulo/pantalla_inicio.png", units= 'pix', size = (412,412), contrast=1.0, opacity=1.0)
				msg.draw()
				win.flip()
				event.waitKeys(['q','n','t','space'])
				primero = False
			if (i % 2 == 0):
				if termino_bloque:
					termino_bloque = False
					msg = visual.ImageStim(win, image="./estimulo/cruz.png", units= 'pix', size = (100,100), contrast=1.0, opacity=1.0)
					msg.draw()
					win.flip()
					core.wait(1)
				win.clearBuffer()					
				win.color='#000000'
				recta = visual.Rect(win, width=1370, height=770, fillColor='#000000', fillColorSpace='hex')
				msg1 = visual.TextStim(win, text="BLOQUE " + str(i/2+1), pos=(-200, 240), color='#FFFFFF', colorSpace='hex')
				msg2 = visual.TextStim(win, text="Presione la tecla n para continuar", color='#FFFFFF', colorSpace='hex',alignHoriz='center', alignVert='center')			
				recta.draw()
				msg1.draw()
				msg2.draw()

				win.flip()

				keys = event.waitKeys(['q','t','n'])
				for key in keys:		
					if key == 'q':
						q.put(marca_final)
						win.close()
						core.quit()
						teclasAString = "; ".join(str(x) for x in teclas)
						dataFile.write(teclasAString)
						dataFile.close()
						time.sleep(1)
						break
					elif key == 't':
						i = i + 2
						t_presionada = True
						if i >= Nsess:
							q.put(marca_final)
							win.close()
							core.quit()
							teclasAString = "; ".join(str(x) for x in teclas)
							dataFile.write(teclasAString)
							dataFile.close()
							time.sleep(1)
							break
					elif key == 'n':
						esperar = 0
						win.color='#808080'
					
			else:
				win.clearBuffer()
				msg = visual.TextStim(win, text="Aprovecha este momento para descansar la vista", color='#000000', colorSpace='hex', alignHoriz='center', alignVert='center')
				msg.draw()
				win.flip()

				time.sleep(3)
				esperar = 0

		tiempos = []
		primera_iter = True
	
		msg = visual.ImageStim(win, image="./estimulo/cruz.png", units= 'pix', size = (100,100))
		msg.draw()

		inicio.reset()
		if (i % 2 == 0):		
			marca_inicio = 100
		else: marca_inicio = 20
		b = inicio.getTime()	
		q.put(marca_inicio)	

		# ciclo de cada sesion
		for k in xrange(len(listaMezclada)):		
			# Pongo la cruz			
			win.flip()
			c = inicio.getTime()
			tiempo = []

			if primera_iter:
				c = b
				primera_iter = False
			tiempo.append(c)

			# Preparo la imagen
			msg = visual.ImageStim(win, image=imagen[k], units= 'pix', size = (512,512))
			msg.draw()

			# Espero
			while inicio.getTime() < (ISI + c):
				if event.getKeys(timeStamped=inicio, keyList=['space']):
					q.put(marca_espacio)				

			# Pongo la imagen
			win.flip()
			a = inicio.getTime()

			if (imagen[k] == "./estimulo/PACMAN.png"):
				q.put(marca_pacman)
			else:
				q.put(marca_fantasma)
			tiempo.append(a)
			tiempos.append(tiempo)

			# Preparo la cruz
			msg = visual.ImageStim(win, image="./estimulo/cruz.png", units= 'pix', size = (100,100), contrast=1.0, opacity=1.0)
			msg.draw()

			# Espero
			while inicio.getTime() < (StimDur + a):
				if event.getKeys(timeStamped=inicio, keyList=['space']):
					q.put(marca_espacio)	



		# Pongo la ultima cruz			
		win.flip()
		c = inicio.getTime()

		# Espero
		while inicio.getTime() < (ISI + c):
			if event.getKeys(timeStamped=inicio, keyList=['space']):
				q.put(marca_espacio)				

		if i % 2 == 1:
			q.put(marca_fin_bloque)
			termino_bloque = True
		else: q.put(marca_fin_trial)

		# almaceno datos
		teclas = teclas + ['; Sesion ' + str(i+1)] + ['La lista generada fue: ' + str(listaMezclada)] + ['Apariciones de las imagenes: '] + tiempos

	# siguiente sesion
		i = i + 1
	q.put(marca_final)

	win.close()

	teclasAString = "; ".join(str(x) for x in teclas)
	dataFile.write(teclasAString)

	dataFile.close()
	core.quit()

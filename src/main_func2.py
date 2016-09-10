from psychopy import visual, core, event, gui, data
from random import shuffle,randint
from psychopy.tools.filetools import fromFile, toFile
from multiprocessing import Process, Queue
import estimulo
import entrenamiento
import guardar
import datetime
import os

def main():
	# Info de la sesion
	expInfo = {'Nombre':'nombre', 'Edad':'edad', 'Nacimiento':'DD/MM/AA', 'Mano':'mano'}

	# Presento cuadro para rellenar
	dlg = gui.DlgFromDict(expInfo, title='Formulario')
	if not(dlg.OK):
		core.quit()
	else:
		fileName = expInfo['Nombre']
		if not os.path.exists('./Datos/' + fileName):
		    os.makedirs('./Datos/' + fileName)
		dataFile = open('./Datos/' + fileName + '/' + str(datetime.date.today()) + '_' +fileName+'.csv', 'a')
		nombreEDF = './Datos/' + fileName + "/" + str(datetime.date.today()) + '_' + fileName
		texto = expInfo['Nombre'] + '; ' + str(datetime.datetime.now()) + '; ' + expInfo['Edad'] + '; ' + expInfo['Nacimiento'] + '; ' + expInfo['Mano']
	dataFile.write(texto)

	pantCompleta = True
	win = visual.Window([512,512], monitor="miMonitor", units="pix",  color='#808080', colorSpace='hex', fullscr=pantCompleta)
	win.setMouseVisible(False)

	entrenamiento.correr_entrenamiento(4,win)
#	entrenamiento.correr_entrenamiento(4,win)

	q_marcas = Queue()
	p = Process(target = guardar.save_data, args=(nombreEDF, q_marcas, ))
	p.start()
	infoSesion = [dataFile]
	infoSesion.append(18)
	estimulo.correr_experimento(infoSesion, q_marcas, win)
	
if __name__ == "__main__":
	main()

# Entrenamiento:
# 2 trials de 20 imagenes c/u = 40 imagenes (Fin de bloque cada 2 triales, hay 1 bloque)
# Estimulo:
# 18 trials de 50 imagenes c/u = 900 imagenes (Fin de bloque cada 2 trials, hay 9 bloques)
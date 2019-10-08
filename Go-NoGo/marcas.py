import time

def marcas(q,p,MARCA):
	if p == 1:
		from multiprocessing import Process, Queue
		q.put(MARCA)
		time.sleep(.005)
	elif p == 2:
		from parallel import Parallel
		q.setData(MARCA) # MARCA va de 1 a 255, tambien se puede hacer levantando pins especificos (mandando el binario)
		time.sleep(.005) # En una pagina decia .003... yo le pondria un poco mas, es la duracion de la marca. Depende tb a que frecuencia esta sampleando.
		q.setData(0)
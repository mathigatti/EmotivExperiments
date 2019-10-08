import mne
import matplotlib.pyplot as plt
import numpy
import sys
import datetime


def main(opcion, nombre_test, desde, hasta):
	raw = mne.io.read_raw_edf(nombre_test)
	print(raw.ch_names)

	sfreq = raw.info['sfreq']

	cantidad = len(raw[0][1])
	duracion = raw[0][1][cantidad-1]

	data, times = raw[17:19, int(sfreq * 0):int(sfreq * duracion)]
	data2, times2 = raw[23, int(sfreq * 0):int(sfreq * duracion)]

	marcas = []
	for i in range(0,len(data2[0])):
		if data2[0][i] != 0:
			marcas.append([data2[0][i],times2[i]])

	diferencias = []
	
	print ("\n" + str( marcas[len(marcas)-2][0]) + " ")
	print marcas[len(marcas)-20][0]
	diferencia = marcas[len(marcas)-2][1] -marcas[len(marcas)-20][1]
	print("\n" + str(diferencia))

	for i in range(0,len(marcas)-1):
			diferencias.append(marcas[i+1][1]-marcas[i][1])


	print(marcas)
	print("\n" + str(diferencias))


	times3 = []
	for i in range(0,len(data[0])):
		data[0][i] = data[0][i]/100
		data[1][i] = data[1][i]/100
		data2[0][i] = data2[0][i] + 5
		times3.append(times[i]*1000)

	data = numpy.concatenate((data,data2))


	#Grafico multiple

	plt.ion()

	fig = plt.figure()
	ax = fig.gca()
	ax.set_autoscale_on(False)
	ax.plot(times3, data.T, label='test')

	if (opcion == 0 or opcion == 1):
		for i in range(0,int(duracion)):
			plt.cla() # descarto datos de los ejes de fig
			ax.plot(times3, data.T, label='test')	
			x_max = (i+1)*1000
			ax.axis([0,x_max,4,250])

		#	fig.savefig('./Graficos/grafico' + str(i) + '.svg', format='svg', dpi=1200) # guardar graficos
			plt.draw() # animado

		raw_input("done >>")
	
	if (opcion == 0 or opcion == 2):

		desde = int(duracion)*desde*1000
		hasta = int(duracion)*hasta*1000
		
		plt.cla() # descarto datos de los ejes de fig
		ax.plot(times3, data.T, label='test')	
		x_min = int(desde)
		x_max = int(hasta)
		ax.axis([x_min,x_max,4,250])

		plt.draw() # graficar

	raw_input("done >>")  


	fig.clf() # descarto datos de fig


	"""

	#Codigo extra que no hace nada en especial

	d, t = raw[raw.ch_names.index('MARKER'), :]
	plt.plot(d[0,:3000])

	"""

	return 0


if __name__=='__main__':
    sys.exit(main( int(sys.argv[2]), str(sys.argv[1]), float(sys.argv[3]), float(sys.argv[4]) ))

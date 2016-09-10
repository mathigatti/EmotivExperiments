import emotiv.Emotiv as EM
import time

def save_data(salidaDatos, q_marcas):

	emo = EM.Emotiv(True, False, (1,1))
	emo.connect()
	emo.setup()
	emo.setBufferSizeInSecs(5.0)
	emo.enableForUser(0)
	emo.setEdfOutput(salidaDatos)
	emo.startWriting()
	emo.start()

	salida = False

	while not salida:
		if not q_marcas.empty():
			marca = q_marcas.get()
			if marca == 300:
				salida = True
			emo.mark(0, marca)

	time.sleep(2)

	emo.stop()
	emo.disconnect()

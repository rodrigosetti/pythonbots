from pythonbots.globais import *

mira = False
acel = MAX_GIRO * .01

def ccoria(handler):
	"""
	Movimentacao: Anda sempre de re bem devagar e com pouco giro
	Ataque: Mantem sempre o canhao junto a proa, ao detectar efetua um
		giro para alinha a proa com a borda de deteccao do radar, na
		tentativa de alinhar o canhao com o alvo(se este estiver parado),
		em seguida comeca a atirar e fechar a mira com pouca aceleracao
		em direcao ao alvo
	"""

	global mira, acel

	dist, id = handler.scan()	# scaneia

	# achou inimigo
	if dist < VISAO:

		if not mira:
			handler.girar(handler.getArco()/2.0 - handler.getVelAngular())

		handler.acelerar(.1)
		if handler.getTemperatura() < TEMP_DANOSA - AQUECIMENTO_TIRO:
			handler.atirar()
		mira = True
		handler.setArco(handler.getArco() - .01)

	elif mira:

		mira = False
		handler.girar(handler.getArco()/2.0)
		acel = MAX_GIRO * .01

	else:

		handler.acelerar(-.5)
		handler.girar(acel - handler.getVelAngular())
		handler.setArco(PI/4.0)

		if acel < MAX_GIRO:
			acel += .0001
		else:
			acel = MAX_GIRO * .01

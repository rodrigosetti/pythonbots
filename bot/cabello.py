from pythonbots.globais import *

indo = False
wait = 30

def cabello(handler):
	"""
	Movimentacao: Leste-Oeste
	Scan: gira o canhao no mesmo sentido com angulacao PI/4
	Ataque: Ao detectar inimigo ele para e tenta travar a mira sempre atirando
	"""

	global indo, wait

	# alinha
	if handler.getDirecao() > 0.1 or handler.getDirecao() < -0.1:
		handler.girar(min(MAX_GIRO, -handler.getDirecao()) if handler.getDirecao() < 0 else max(-MAX_GIRO, -handler.getDirecao()))

	# achou inimigo
	dist, id = handler.scan()
	if dist < VISAO:
		handler.girarCanhao(.01)
		if handler.getTemperatura() < TEMP_DANOSA - AQUECIMENTO_TIRO:
			handler.atirar()

		handler.setArco(handler.getArco() - .05)

	else:

		handler.setArco(PI/4.0)
		handler.acelerar(.5 if indo else -.5)
		handler.girarCanhao(.05)

	wait -= 1 if wait > 0 else 0

	if wait == 0 and (handler.getPosicao().x >= TAM_X - (RAIO*2) or handler.getPosicao().x <= RAIO*2):
		indo = not indo
		wait = 30

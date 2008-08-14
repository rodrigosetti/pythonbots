from pythonbots.globais import *
import random

atitude = 'procurando'
acel = .01
cont = 10
wait = 10
lastVida = .0

def rodolfo(handler):
	"""
	Movimentacao: parado e girando, e move em direcao ao alvo quando detecta
	Ataque: Mantem o canhao junto a proa, ao detectar alvo comecao a mover-se
		em direcao a ele, atirar e fechar a mira
	"""

	global atitude, acel, cont, wait, lastVida

	dist, id = handler.scan()	# scaneia

	# achou inimigo
	if dist < VISAO:
		if handler.getTemperatura() < TEMP_DANOSA - AQUECIMENTO_TIRO:
			handler.atirar()

		handler.setArco(handler.getArco() - .01) # diminue arco
		handler.acelerar(.6 if dist > VISAO/2 else .4)
		atitude = 'mirou'
	elif atitude == 'mirou':	# perdeu
		atitude = 'tentar-direita'


	if atitude == 'tentar-direita' and cont-1 > 0:
		cont -= 1
		handler.girar(MAX_GIRO/2.0)
	elif atitude == 'tentar-direita':
		atitude = 'tentar-esquerda'
		cont = 10

	if atitude == 'tentar-esquerda' and cont + 9 > 0:
		cont -= 1
		handler.girar(-MAX_GIRO/2.0)
	elif atitude == 'tentar-esquerda':
		atitude = 'procurando'
		cont = 10

	if atitude == 'procurando':
		handler.girar(MAX_GIRO/6.0)
		handler.acelerar(acel)
		acel = .1 if acel >= MAX_ACEL/2.0 else .002
		handler.setArco(.5)

	wait -= 1 if wait > 0 else 0

	# trata colisao
	if wait == 0 and (handler.getPosicao().x >= TAM_X - (RAIO*2) or handler.getPosicao().x <= RAIO*2 or \
	   handler.getPosicao().y >= TAM_Y - (RAIO*2) or handler.getPosicao().y <= RAIO*2):
		wait = int(PI / MAX_GIRO) * 2
		handler.girar(random.choice([PI, -PI]))
	elif wait == 0 and handler.getVida() <= lastVida - DANO_TIRO:
		acel = MAX_ACEL / 2.5
		wait = 100

	lastVida = handler.getVida()

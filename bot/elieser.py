from pythonbots.globais import *
from pythonbots.vector import Vector
from math import atan2
import random

lastVida = 0
mira = False
taxa_giro = .1

def elieser(handler):
	"""
	Movimenacao: constante com angulo de giro aleatorio
	Ataque: Mantem o canhao sempre em um angulo reto em relacao a proa,
		ao detectar inimigo ele para e tenta travar a mira
	Defesa: Ao detectar dano, ele supoe que o atacante esteja na direcao do
		seu canhao, e, por manter o canhao sempre em um angulo reto em relacao
		a proa, efetua um movimento para frene ou para tras para tentar sair
		da corrente	de tiros.
	"""

	global lastVida, mira, taxa_giro

	if handler.getVida() > lastVida:
		handler.girarCanhao(PI/2)
		first_giro = False

	# scaneia
	dist, id = handler.scan()

	# se tem alguem na mira
	if dist < VISAO:

		mira = True

		# diminui arco
		handler.setArco(handler.getArco() - .05)

		# atira se nao esta muito quente e se arco eh pequeno
		if handler.getTemperatura() < TEMP_DANOSA - AQUECIMENTO_TIRO and \
		random.uniform(MIN_ARCO, DPI) > handler.getArco():
			handler.atirar()

	# se perdeu de vista
	else:

		if mira:
			mira = False

		if random.randint(0,100) == 0:
			taxa_giro = random.uniform(-.1, .1)

		# aumenta tamanho do arco se eh menor que PI/2
		if handler.getArco() < PI/3:
			handler.setArco(handler.getArco() + .05)

		# procura ir para o centro
		handler.girar(taxa_giro)
		handler.acelerar(1)

	# se ta levando chumbo
	if handler.getVida() < lastVida:
		# da meia volta e cai fora
		if handler.getTemperatura() < TEMP_DANOSA - AQUEC_VELOCIDADE(abs(handler.getVelocidade().length()) + MAX_ACEL*2):
			handler.acelerar(MAX_ACEL * random.choice((-2,2)))

	# avita paredes
	if not mira and (handler.getPosicao().x >= TAM_X - (RAIO*4) or handler.getPosicao().x <= RAIO*4 or \
	   handler.getPosicao().y >= TAM_Y - (RAIO*4) or handler.getPosicao().y <= RAIO*4):
		handler.girar(MAX_GIRO)

	lastVida = handler.getVida()

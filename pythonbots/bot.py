import time, random
from globais import *
from math import sin, cos, sqrt
from vector import Vector
import arena

indice_count = 0

#
# Classe handler, uso do jogador
#
class Handler(object):
	
	def __init__(self, bot):
		self._bot = bot

	#
	# Leitura de parametros
	#
	def isAtivo(self):
		return self._bot.ativo

	def getVelocidade(self):
		return self._bot.velocidade

	def getPosicao(self):
		return self._bot.posicao

	def getDirecao(self):
		return self._bot.direcao

	def getCanhao(self):
		return self._bot.canhao

	def getArco(self):
		return self._bot.arco

	def getVelAngular(self):
		return self._bot.vel_angular

	def getVida(self):
		return self._bot.vida

	def getTemperatura(self):
		return self._bot.temp

	def getIndice(self):
		return self._bot.indice

	#
	# Leitura de percepcao do mundo
	#
	# scaneia e retorna proximidade e indice de outro bot
	def scan(self):
		return self._bot.arena.scan(self._bot)

	# numero de bots vivos
	def getNumeroVivos(self):
		return self._bot.arena.vivos()

	#
	# Acoes
	#
	def acelerar(self, acel):
		self._bot.aceleracao += acel

	def girar(self, ang):
		self._bot.acel_giro += ang

	def girarCanhao(self, ang):
		self._bot.acel_canhao += ang

	def setArco(self, arco):
		self._bot.set_arco = arco

	def atirar(self):
		if not self._bot.atirou:
			self._bot.arena.addTiro(self._bot)
			self._bot.shots += 1	# aumenta estatistica
			self._bot.temp += AQUECIMENTO_TIRO
			self._bot.atirou = True	# atira uma vez por turno

#
# Classe do que descreve o bot, para o sistema
#
class Bot(object):

	# estado: alguns valores iniciais padrao
	velocidade = Vector(.0, .0)
	posicao = Vector(.0, .0)
	direcao = .0
	canhao = .0
	arco = MIN_ARCO
	vel_angular = .0
	vida = MAX_VIDA
	temp = TEMP_NORMAL
	indice = 0
	ativo = True
	atirou = False

	# variacao dos valores
	aceleracao = .0
	acel_giro = .0
	acel_canhao = .0
	set_arco = arco

	# estatisticas
	shots = 0
	killed_by = None

	# construtor
	def __init__(self, arena, funcao):

		global indice_count

		# salva arena e funcao
		self.arena = arena
		self.funcao = funcao

		# inicia bot com algumas propriedades aleatorias
		self.posicao = Vector(random.uniform(RAIO, TAM_X-RAIO), random.uniform(RAIO, TAM_Y-RAIO))
		self.direcao = random.uniform(0, DPI)
		self.vel_angular = random.uniform(0, DPI)
		self.indice = indice_count
		indice_count += 1

		# inicializa estatisticas
		self.killed = []

		# cria handler(interface com o jogador)
		self.handler = Handler(self)

	def __str__(self):
		return self.funcao.__name__

	# atualiza fisica e parametros do bot
	def atualizar(self):		

		# atualiza posicao e direcao com base nas velocidades
		self.posicao += self.velocidade
		self.velocidade *= ATRITO if self.ativo else 0.8
		self.direcao += self.vel_angular
		self.vel_angular *= ATRITO_GIRO if self.ativo else 0.9		

		# gira canhao livremente se morto
		if not self.ativo:
			self.canhao += self.vel_angular * 2.0
		
		# atualiza velocidades com base nas aceleracoes
		self.velocidade += Vector(cos(self.direcao), sin(self.direcao)) * minabs(self.aceleracao, MAX_ACEL)
		self.aceleracao -= minabs(self.aceleracao, MAX_ACEL)

		self.vel_angular += minabs(self.acel_giro, MAX_GIRO)
		self.acel_giro -= minabs(self.acel_giro, MAX_GIRO)

		self.canhao += minabs(self.acel_canhao, MAX_GIRO_CANHAO)
		self.acel_canhao -= minabs(self.acel_canhao, MAX_GIRO_CANHAO)

		self.arco = self.set_arco	# seta novo arco(ou mesmo)

		# verifica se morreu
		if self.vida <= 0 and self.ativo:

			self.ativo = False	# mata
			self.vida = 0

			# explode bot!!
			self.velocidade *= IMPACTO_EXPLOSAO
			self.vel_angular = random.uniform(-PI/2.0,PI/2.0)
			self.temp = TEMP_MAX

			self.morte()	# chama callback

		#
		# Calculos com temperatura
		#

		# se esta muito quente... tira vida
		if self.temp >= TEMP_DANOSA and self.ativo:
			self.vida -= DANO_TEMP

		# resfria normalmente
		if self.temp > TEMP_NORMAL:
			self.temp -= RESFRIAMENTO

		# aquece de acordo com velocidade
		self.temp += AQUEC_VELOCIDADE(self.velocidade.length())

		# limita temperatura maxima
		self.temp = min(self.temp, TEMP_MAX)

		#
		# Trata colisao com as paredes
		#
		def colidio():
			self.vida -= DANO_COLISAO_PAREDE(self.velocidade.length())
			self.temp += AQUEC_COLISAO_PAREDE(self.velocidade.length())
			self.colisao_parede()	# chama callback

		if self.posicao.x < RAIO:
			colidio()
			self.posicao.x = RAIO
			self.velocidade.x *= -1
		elif self.posicao.x > TAM_X-RAIO:
			colidio()
			self.posicao.x = TAM_X-RAIO
			self.velocidade.x *= -1

		if self.posicao.y < RAIO:
			colidio()
			self.posicao.y = RAIO
			self.velocidade.y *= -1
		elif self.posicao.y > TAM_Y-RAIO:
			colidio()
			self.posicao.y = TAM_Y-RAIO
			self.velocidade.y *= -1

		# executa o diabo se estiver vivo
		if self.ativo:
			self.funcao(self.handler)	# chama a funcao do jogador
	
			# regulariza os valores
			self.set_arco = min(max(self.set_arco, MIN_ARCO), DPI)

			self.atirou = False	# deixa atirar de novo


	# callbacks
	def colisao_parede(self):
		pass

	def colisao_bot(self, outro):
		pass

	def colisao_tiro(self, tiro):
		pass

	def morte(self):
		pass

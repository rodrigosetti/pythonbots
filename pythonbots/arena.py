import bot
from globais import *
from math import sin, cos, sqrt, atan2
from numpy import mod
from vector import Vector

#
# Tiro
#
class Tiro(object):

	# constroi um tiro baseado em quem atirou
	def __init__(self, bot):
		self.bot = bot
		self.velocidade = Vector(cos(bot.direcao + bot.canhao), sin(bot.direcao + bot.canhao)) * VEL_TIRO
		self.posicao = bot.posicao + Vector(cos(bot.direcao + bot.canhao), sin(bot.direcao + bot.canhao)) * (RAIO*1.1)

	# atualiza tiro(incrementa posicao baseada na velocidade)
	def atualizar(self):
		self.posicao += self.velocidade

	# callbacks
	def colisao_bot(self, bot):
		pass

	def colisao_parede(self, arena):
		pass

#
# Arena: aonde todos os bots e objetos existem e interagem
#
class Arena(object):

	bots = []
	tiros = []
	ticks = 0
	
	def __init__(self, funcoes):
		self.funcoes = funcoes

	def start(self):
		self.tiros = []
		self.bots = []
		self.ticks = 0
		bot.indice_count = 0
		for f in self.funcoes:
			self.bots.append(bot.Bot(self, f))

	# adiciona tiro ao sistema
	def addTiro(self, tiro):
		self.tiros.append(tiro)

	# numero de bots vivos
	def vivos(self):
		return len(filter(lambda a: a.ativo, self.bots))

	# escaneia regiao
	def scan(self, bot):
		# menor distancia ate agora
		menor = VISAO
		ind = -1

		# itera todos bots
		for b in self.bots:
			# se nao eh o proprio e esta ativo
			if b is not bot and b.ativo:
				# calcula distancia entre os bots
				distancia = (bot.posicao - b.posicao).length()
				# verifica se a distancia esta dentro do limiar aceitavel
				# e eh menor que a menor encontrada ate agora
				if distancia-RAIO <= VISAO and distancia < menor:

					vet_canhao = Vector(cos(bot.direcao + bot.canhao), sin(bot.direcao + bot.canhao))
					vet_alvo = b.posicao - bot.posicao

					angulo = vet_canhao.angle(vet_alvo)

					if angulo <= mod(bot.arco/2.0 + atan2(RAIO, (bot.posicao - b.posicao).length()), PI):
						ind = b.indice
						menor = distancia
					
		return menor, ind

	# atualiza bots
	def atualizar(self):

		self.ticks += 1

		# itera todos os tiros
		for t in self.tiros:
			if (not (0 <= t.posicao.x <= TAM_X)) or (not (0 <= t.posicao.y <= TAM_Y)):
				t.colisao_parede(self)		# chama callback
				self.tiros.remove(t)	# tiro passou dos limites
			else:
				t.atualizar()	# atualiza tiro

		# itera todos bots
		for b in self.bots:
			# atualiza fisica e colisao com paredes
			b.atualizar()
		
			# itera novamente todos os bots
			for c in self.bots:
				# trata colisao com outro bot
				if c is not b:
					# calcula distancia entre os bots
					distancia = (b.posicao - c.posicao).length()
					# detecta colisao
					if distancia != 0 and distancia <= RAIO*2:
						b.colisao_bot(c)	# chama callback
						c.colisao_bot(b)	# chama callback

						colisao = (b.posicao - c.posicao)	# vetor colisao(ligando os dois)

						# projeta velocidades no vetor colisao
						trans_a = b.velocidade.projection(colisao)
						trans_b = c.velocidade.projection(colisao)

						# corrige posicoes
						r = (colisao.unit() * RAIO * 2) - colisao
						b.posicao += r / 2.0
						c.posicao -= r / 2.0

						# troca velocidades
						b.velocidade += trans_b - trans_a
						c.velocidade += trans_a - trans_b						

						# trocam velocidade angular
						b.vel_angular -= c.vel_angular * 2.0
						c.vel_angular -= b.vel_angular * 2.0

						# causa dano
						dano = DANO_COLISAO_BOT((b.velocidade - c.velocidade).length())
						if b.ativo: b.vida -= dano
						if c.ativo: c.vida -= dano

						# causa aquecimento
						aquec = AQUEC_COLISAO_BOT((b.velocidade - c.velocidade).length())
						b.temp += aquec
						c.temp += aquec

			# itera todos os tiros
			for t in self.tiros:
				# trata colisao com tiros
				distancia = (t.posicao - b.posicao).length()
				if distancia < RAIO:
					b.colisao_tiro(t)		# chama callback do bot
					t.colisao_bot(b)		# chama callback do tiro

					if b.ativo: b.vida -= DANO_TIRO		# calcula dano
					b.temp += AQUEC_COL_TIRO	# esquenta

					# transfere impulso
					b.velocidade += t.velocidade * IMPACTO_TIRO_VEL

					if not b.ativo:
						# meche com o angulo, se eh carcaca
						b.vel_angular += t.velocidade.length() * IMPACTO_TIRO_ANG
					elif b.vida <= 0:	# se o bot morreu agora
						# atualiza estatisticas
						b.killed_by = t.bot
						t.bot.killed.append(b)

					self.tiros.remove(t)		# remove tiro(bateu no bot)


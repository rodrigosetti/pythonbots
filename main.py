#! /usr/bin/python

import pygame, sys, optparse
from pythonbots.globais import *
from pgarena import Arena

#
# Funcao principal
#
def main():

	# Trata linha de comando
	parser = optparse.OptionParser()
	parser.add_option("-d", "--dt", dest="dt", default=25,
                  help="delay per frame(fps related)", metavar="DT")
	parser.add_option("-r", "--rounds", dest="rounds", default=1,
                  help="rounds to play", metavar="ROUNDS")
	parser.add_option("-a", "--arcs",
                  action="store_true", dest="mostrar_arcos", default=False,
                  help="Show scan arcs")
	parser.add_option("-s", "--sound",
                  action="store_true", dest="som", default=False,
                  help="Active sound effects")
	parser.add_option("-t", "--text-mode",
                  action="store_true", dest="modo_texto", default=False,
                  help="Text mode(no graphics): faster simulation")
	parser.add_option("-n", "--names",
                  action="store_true", dest="mostrar_nomes", default=False,
                  help="Show bot names")

	(options, args) = parser.parse_args()	# parseia

	# le bots da linha de comando
	funcoes = []
	for bot in args:
		funcoes.append(__import__('bot.' + bot, fromlist=[bot]).__dict__[bot])

	if len(funcoes) == 0:
		sys.stderr.write('No bots to load\n')
		sys.exit(1)

	if not options.modo_texto:
		clock = pygame.time.Clock()	# controle de fps
	else:
		print 'starting simulation...'

	# cria tabela de score
	score = [{'w':0, 'l':0, 't':0, 's':.0, 'kills':0, 'shots':0} for x in (funcoes)]

	# cria uma arena
	arena = Arena(options.modo_texto, funcoes)
	arena.score = score
	arena.rounds = options.rounds

	exec_jogo = True	# executando jogo

	# loop de rounds
	for round in xrange(int(options.rounds)):

		# verifica se foi dado o comando para sair do jogo
		if not exec_jogo:
			break

		arena.start()	# (re)inicializa arena
		arena.round = round
		arena.som = options.som
		arena.mostrar_arcos = options.mostrar_arcos
		arena.mostrar_nomes = options.mostrar_nomes

		dt = options.dt		# seta dt
		exec_round = True	# executando round
		end_round_ticks	= 100	# ticks no fim do round
		pause = False

		# loop de jogo
		while exec_round:

			# trata eventos do pygame
			if not options.modo_texto:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						exec_round = False
						exec_jogo = False
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							exec_round = False
						elif event.key == pygame.K_n:
							arena.mostrar_nomes = not arena.mostrar_nomes
						elif event.key == pygame.K_a:
							arena.mostrar_arcos = not arena.mostrar_arcos
						elif event.key == pygame.K_s:
							arena.som = not arena.som
						elif event.key == pygame.K_q:
							exec_round = False
							exec_jogo = False
						elif event.key == pygame.K_j:
							dt += 2
						elif event.key == pygame.K_k and dt > 2:
							dt -= 2
						elif event.key == pygame.K_p:
							pause = not pause

			# verifica se acabou o tempo ou acabou a batalha
			if arena.vivos() <= 1 or arena.ticks >= MAX_TEMPO:
				if not options.modo_texto:
					end_round_ticks -= 1
					if end_round_ticks == 0:
						break
				else:
					print 'match', round+1, 'of', options.rounds, 'done:',
					break

			# atualiza
			if not pause: arena.atualizar()

			if not options.modo_texto:
				arena.draw()	# desenha e mostra na tela
				clock.tick(dt)	# limita fps

		# calcula escore
		vivos = arena.vivos()
		empate = vivos != 1
		for i, bot in enumerate(arena.bots):
			score[i]['kills'] += len(bot.killed)
			score[i]['shots'] += bot.shots
			if bot.ativo:
				score[i]['s'] += SCORE(len(funcoes), vivos)
				if empate:
					score[i]['t'] += 1
				else:
					score[i]['w'] += 1
			else:
				score[i]['l'] += 1

	# mostra escore final:
	print '%s rounds played' % round if round>1 else 'one round played'
	print '%20s  %4s %4s %5s %5s %5s score' % ('name', 'wins', 'ties', 'loses', 'kills', 'shots')
	print '-------------------------------------------'
	for i, (f, bot) in enumerate(zip(funcoes, arena.bots)):
		print '%20s  %4d %4d %5d %5d %5d %4.2f' % \
		(f.__name__, score[i]['w'], score[i]['t'], score[i]['l'], \
		score[i]['kills'], score[i]['shots'], score[i]['s'])

	# finaliza
	pygame.quit()

if __name__ == '__main__':
	main()

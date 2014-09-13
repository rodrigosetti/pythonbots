# coding: utf-8
#
import pygame, random, os
import pythonbots.arena, pythonbots.bot
from pythonbots.globais import *
from math import sin, cos
from numpy import linspace

#
# Constantes graficas
#
CORES = (
(255,0,0),
(0,255,0),
(0,0,255),
(255,255,0),
(255,0,255),
(0,255,255),
(255,255,255),
(255,100,50),
(50,255,100),
(100,50,255),
(255,40,120),
(40,255,120),
(120,50,255),
)

AREA_INFERIOR = 70
BOT_INFO_X = 140
BOT_INFO_Y = 65
MAX_MSG = 4

#
# Classe bot extendida para tratar callbacks
#
class Bot(pythonbots.bot.Bot):

        # callbacks
        def colisao_parede(self):
                if self.arena.modo_texto: return
                if self.arena.som and self.arena.mixer: self.arena.snd_colisao_par.play(0, 20)  # toca som
                px = 0 if self.posicao.x <= RAIO else (TAM_X if self.posicao.x >= TAM_X-RAIO else self.posicao.x)
                py = 0 if self.posicao.y <= RAIO else (TAM_Y if self.posicao.y >= TAM_Y-RAIO else self.posicao.y)
                vx = -self.velocidade.x if self.posicao.x <= RAIO or self.posicao.x >= TAM_X-RAIO else self.velocidade.x
                vy = -self.velocidade.y if self.posicao.y <= RAIO or self.posicao.y >= TAM_Y-RAIO else self.velocidade.y

                # cria faiscas de colisao com parede
                for x in xrange(10):
                        self.arena.faiscas.append({'est':PI/2, 'pos':[px, py], 'vel': (vx*2 + random.uniform(-1, 1), vy*2 + random.uniform(-1,1))})

        def colisao_bot(self, outro):
                if self.arena.modo_texto: return
                if self.arena.som and self.arena.mixer: self.arena.snd_colisao_bot.play(0, 30)  # toca som
                pos = (self.posicao + outro.posicao)/2
                vel = (self.velocidade + outro.velocidade)/2
                for x in xrange(4):
                        self.arena.faiscas.append({'est':PI/2, 'pos':[pos.x, pos.y], 'vel': (vel.x*2 + random.uniform(-2, 2), vel.y*2 + random.uniform(-2,2))})

        def colisao_tiro(self, tiro):
                if self.arena.modo_texto: return
                if not self.ativo: self.time_of_death = (self.arena.ticks + self.time_of_death*2)/3
                if self.arena.som and self.arena.mixer: self.arena.snd_colisao_tiro.play(0, 25) # toca som
                self.arena.fumacas.append({'est':PI/2, 'pos':(tiro.posicao.x, tiro.posicao.y), 'col':(255,255,0), 'rad':10})

        def morte(self):
                self.arena.showMsg(str(self) + ' was killed by ' + (str(self.killed_by) if self.killed_by else 'accident') + '.')

                if self.arena.modo_texto:
                        return

                if self.arena.som and self.arena.mixer: self.arena.snd_morte.play()     # toca som
                self.time_of_death = self.arena.ticks   # marca o momento da morte

                # faiscas no painel
                for x in xrange(100):
                        px = random.uniform(TAM_X, BOT_INFO_X+TAM_X)
                        py = random.uniform(self.indice*BOT_INFO_Y,self.indice*BOT_INFO_Y + BOT_INFO_Y) if \
                                px <= TAM_X + 10 or px >= (BOT_INFO_X+TAM_X) - 10 else random.choice((self.indice*BOT_INFO_Y, self.indice*BOT_INFO_Y + BOT_INFO_Y))
                        self.arena.faiscas.append({'est':PI/2, \
                        'pos': [px, py], \
                        'vel': ((px - (TAM_X+BOT_INFO_X/2))/12.0 + random.uniform(-1,1), \
                        (py - (self.indice*BOT_INFO_Y + BOT_INFO_Y/2))/12.0 + random.uniform(-1,1))})

                # cria uma zona
                for x in xrange(10):
                        self.arena.fumacas.append({'est':PI/2, \
                        'pos':(self.posicao.x + random.uniform(-RAIO/2, RAIO/2), self.posicao.y + random.uniform(-RAIO/2, RAIO/2)), \
                        'col':(255,random.randint(0,255),random.randint(0,100)), 'rad': RAIO*4})

                for x in xrange(20):
                        self.arena.faiscas.append({'est':PI/2, 'pos':[self.posicao.x, self.posicao.y], \
                        'vel': (self.velocidade.x*2 + random.uniform(-4, 4), self.velocidade.y*2 + random.uniform(-4,4))})

                for x in xrange(20):
                        self.arena.destrocos.append({'est':PI/2, \
                        'pos':[self.posicao.x + random.uniform(-RAIO, RAIO), self.posicao.y + random.uniform(-RAIO, RAIO)], \
                        'vel': [self.velocidade.x*2 + random.uniform(-4, 4), self.velocidade.y*2 + random.uniform(-4,4)], \
                        'col' : CORES[self.indice]})

#
# Classe tiro extendida para tratar callbacks
#
class Tiro(pythonbots.arena.Tiro):

        def colisao_parede(self, arena):
                if arena.modo_texto: return
                arena.fumacas.append({'est':PI/2, 'pos':(self.posicao.x, self.posicao.y), 'col':(255,255,255), 'rad':6})

#
# classe Arena extendida para desenhar com pygame
#
class Arena(pythonbots.arena.Arena):

        # construtor
        def __init__(self, modo_texto, *args, **kargs):
                pythonbots.arena.Arena.__init__(self, *args, **kargs)

                self.modo_texto = modo_texto
                if not self.modo_texto:
                        pygame.init()
                        pygame.display.set_mode((TAM_X + BOT_INFO_X, TAM_Y + AREA_INFERIOR))
                        pygame.display.set_caption('Pythonbots')
                        self.screen = pygame.display.get_surface()

                        # fontes
                        self.font1 = pygame.font.Font(None, 12)
                        self.font2 = pygame.font.Font(None, 16)

                        # sons
                        if pygame.mixer.get_init():
                                self.snd_tiro = pygame.mixer.Sound(os.path.join('snd','tiro.wav'))
                                self.snd_tiro.set_volume(.1)
                                self.snd_colisao_bot = pygame.mixer.Sound(os.path.join('snd','colisao.wav'))
                                self.snd_colisao_bot.set_volume(.15)
                                self.snd_colisao_tiro = pygame.mixer.Sound(os.path.join('snd','colisao.wav'))
                                self.snd_colisao_tiro.set_volume(.1)
                                self.snd_colisao_par = pygame.mixer.Sound(os.path.join('snd','colisao.wav'))
                                self.snd_colisao_par.set_volume(.06)
                                self.snd_morte = pygame.mixer.Sound(os.path.join('snd','morte.wav'))
                                self.snd_morte.set_volume(.5)
                                self.mixer = True
                        else:
                                self.mixer = False

        # metodo sobreescrevido para funcionar com bot extendido
        def start(self):
                self.tiros = []
                self.bots = []
                self.msg = ['round started.']
                self.ticks = 0
                self.done = False
                if not self.modo_texto:
                        self.destrocos = []
                        self.faiscas = []
                        self.fumacas = []
                pythonbots.bot.indice_count = 0
                for f in self.funcoes:
                        self.bots.append(Bot(self, f))

        # adiciona tiro ao sistema(overloaded)
        def addTiro(self, bot):
                self.tiros.append(Tiro(bot))
                if not self.modo_texto and self.som  and self.mixer:
                        self.snd_tiro.play(0,15)

        # atualiza estado(overloaded)
        def atualizar(self):
                pythonbots.arena.Arena.atualizar(self)

                if not self.modo_texto:

                        # atualiza fumacas
                        for f in self.fumacas:
                                if 'vel' in f:
                                        f['pos'][0] += f['vel'][0]
                                        f['pos'][1] += f['vel'][1]
                                f['est'] -= .08
                                if f['est'] <= 0:
                                        self.fumacas.remove(f)

                        # atualiza faiscas
                        for f in self.faiscas:
                                f['pos'][0] += f['vel'][0]
                                f['pos'][1] += f['vel'][1]
                                f['est'] -= .1
                                if f['est'] <= 0:
                                        self.faiscas.remove(f)

                        # atualiza destrocos
                        for f in self.destrocos:
                                f['pos'][0] += f['vel'][0]
                                f['pos'][1] += f['vel'][1]
                                f['vel'][0] *= 0.8
                                f['vel'][1] *= 0.8
                                f['est'] -= .005
                                if f['est'] <= 0:
                                        self.destrocos.remove(f)

                        # atualiza bots
                        for bot in self.bots:
                                # solta fumaca negra se estiver com vida baixa
                                if bot.ativo and random.random()/2.0 > bot.vida/MAX_VIDA and random.random() < bot.velocidade.length()/MAX_ACEL:
                                        self.fumacas.append({'est':PI/2, 'pos':(bot.posicao.x, bot.posicao.y), 'col':(127,120,100), 'rad':8})
                                elif not bot.ativo and random.randint(0,self.ticks-bot.time_of_death) <= 10:
                                        self.fumacas.append({'est':PI/2, 'pos':[bot.posicao.x, bot.posicao.y], 'col':(127,120,100), 'rad':8, \
                                        'vel': (-.8 + random.uniform(-.1,.1),-.8 + random.uniform(-.1, .1))})

        #
        # Mostra mensagem, seja no modo grafico ou texto
        #
        def showMsg(self, msg):
                if self.modo_texto:
                        print msg
                else:
                        self.msg.insert(0, msg)
                        if len(self.msg) > MAX_MSG:
                                self.msg.pop()

        #
        # Desenha estado do jogo
        #
        def draw(self):

                if self.modo_texto: return

                # limpa tela
                self.screen.fill((0,0,0))

                vivos = self.vivos()

                # desenha bots
                for bot in self.bots:
                        if self.mostrar_arcos and bot.ativo:
                                # desenha arco
                                pygame.draw.aalines(self.screen, (50,50,50), True, \
                                [(bot.posicao.x + cos(bot.direcao + bot.canhao)*RAIO, bot.posicao.y + sin(bot.direcao + bot.canhao) * RAIO)] + \
                                [ (bot.posicao.x + cos((bot.direcao + bot.canhao) + x) * VISAO, \
                                  bot.posicao.y + sin((bot.direcao + bot.canhao) + x) * VISAO) for x in linspace(-bot.arco/2.0, bot.arco/2.0, 10)] )

                        if self.mostrar_nomes:
                                # desenha nome
                                nome = self.font1.render(bot.funcao.__name__, False, CORES[bot.indice])
                                self.screen.blit(nome, (bot.posicao.x - nome.get_size()[0]/2, bot.posicao.y + RAIO))

                        # desenha corpo
                        pygame.draw.aalines(self.screen, CORES[bot.indice] if bot.ativo else (50,50,50), True, \
                        ((bot.posicao.x + cos(bot.direcao)*RAIO, bot.posicao.y + sin(bot.direcao) * RAIO), \
                         (bot.posicao.x + cos(bot.direcao + 2.5)*RAIO, bot.posicao.y + sin(bot.direcao + 2.5)*RAIO),
                         (bot.posicao.x + cos(bot.direcao - 2.5)*RAIO, bot.posicao.y + sin(bot.direcao - 2.5)*RAIO)))
                        # desenha canhao
                        pygame.draw.aaline(self.screen, CORES[bot.indice] if bot.ativo else (50,50,50), \
                         (bot.posicao.x, bot.posicao.y), \
                         (bot.posicao.x + cos(bot.direcao + bot.canhao)*RAIO, bot.posicao.y + sin(bot.direcao + bot.canhao) * RAIO))

                        # se este eh o vencedor
                        if vivos == 1 and bot.ativo and not self.done:
                                self.showMsg(str(bot) + ' won the match!')
                                self.done = True

                # desenha tiros
                for tiro in self.tiros:
                        pygame.draw.line(self.screen, (255,255,255), (tiro.posicao.x, tiro.posicao.y), \
                        (tiro.posicao.x + tiro.velocidade.x, tiro.posicao.y + tiro.velocidade.y))

                # se ninguem eh vencedor
                if (vivos == 0 or self.ticks > MAX_TEMPO) and not self.done:
                        self.showMsg('the match was a tie.')
                        self.done = True

                # desenha paredes
                pygame.draw.rect(self.screen, (255,255,255), ((0,0),(TAM_X,TAM_Y)), 2)

                # limpa restante da tela
                pygame.draw.rect(self.screen, (0,0,0), ((0, TAM_Y), (TAM_X+BOT_INFO_X, AREA_INFERIOR)))
                pygame.draw.rect(self.screen, (0,0,0), ((TAM_X, 0), (BOT_INFO_X, TAM_Y)))

                for bot in self.bots:
                        # desenha informacoes laterais
                        pygame.draw.rect(self.screen, CORES[bot.indice] if bot.ativo else (80,80,80), ((TAM_X, bot.indice*BOT_INFO_Y),(BOT_INFO_X, BOT_INFO_Y)), 1)
                        nome = self.font2.render(bot.funcao.__name__, False, CORES[bot.indice] if bot.ativo else (80,80,80))
                        self.screen.blit(nome, (TAM_X + 4, bot.indice*BOT_INFO_Y + 2))
                        pygame.draw.rect(self.screen, (255,100,100) if bot.ativo else (80,80,80), \
                        ((TAM_X+4, bot.indice*BOT_INFO_Y + 32), (bot.temp / TEMP_MAX *(BOT_INFO_X-8), 14)))
                        if bot.ativo:
                                pvida = bot.vida / MAX_VIDA
                                pygame.draw.rect(self.screen, (0,255,0) if pvida >= .666 else ((255,255,0) if pvida >= .333 else (255,0,0)), \
                                ((TAM_X+4, bot.indice*BOT_INFO_Y + 16), (pvida *(BOT_INFO_X-8), 14)))
                                pygame.draw.line(self.screen, (255,0,0), \
                                (TAM_X+4 + (TEMP_DANOSA / TEMP_MAX * (BOT_INFO_X-8)), bot.indice*BOT_INFO_Y + 32),\
                                (TAM_X+4 + (TEMP_DANOSA / TEMP_MAX * (BOT_INFO_X-8)), bot.indice*BOT_INFO_Y + 45))
                        sinfo = self.font2.render(\
                        str(self.score[bot.indice]['w']) + ' / ' + str(self.score[bot.indice]['t']) + ' / ' + str(self.score[bot.indice]['l']),\
                        False, CORES[bot.indice] if bot.ativo else (80,80,80))
                        self.screen.blit(sinfo, (TAM_X + 4, bot.indice*BOT_INFO_Y + 48))

                # desenha informacoes na barra de baixo
                texto = self.font2.render( \
                '(Q)quit - show (N)ames - show (A)rcs - (S)ound - (ESC) next round - (P)ause - (J K) changes fps', False, (255,255,255))
                self.screen.blit(texto, (1, TAM_Y+6))
                texto = self.font2.render('match: ' + str(self.round+1) + ' / ' + str(self.rounds) + \
                '        time: ' + str(self.ticks) + ' / ' + str(MAX_TEMPO), False, (255,255,255))
                self.screen.blit(texto, (1, TAM_Y+26))
                for i, msg in enumerate(self.msg):      # desenha mensagens
                        texto = self.font2.render(msg, False, (255-(i*(255/MAX_MSG)),255-(i*(255/MAX_MSG)),255-(i*(255/MAX_MSG))))
                        self.screen.blit(texto, (TAM_X - texto.get_size()[0], TAM_Y+6 + i*16))

                # desenha fumacas
                for f in self.fumacas:
                        s = sin(f['est'])
                        pygame.draw.circle(self.screen, (int(f['col'][0]*s),int(f['col'][1]*s),int(f['col'][2]*s)) , map(int,f['pos']), int(f['rad']+4 - s*f['rad']), 4)

                # desenha faiscas
                for f in self.faiscas:
                        s = sin(f['est'])
                        pygame.draw.line(self.screen, (s*255,s*200,0), f['pos'], (f['pos'][0] + f['vel'][0], f['pos'][1] + f['vel'][1]), 1)

                # desenha destrocos
                for f in self.destrocos:
                        s = sin(f['est'])
                        pygame.draw.line(self.screen, (f['col'][0]*s,f['col'][1]*s,f['col'][2]*s), f['pos'], \
                        (f['pos'][0] + f['vel'][0], f['pos'][1] + f['vel'][1]), 2)

                pygame.display.flip()   # mostra na tela


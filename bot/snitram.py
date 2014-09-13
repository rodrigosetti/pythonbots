# coding: utf-8

from pythonbots.globais import *

wait = 0

def snitram(handler):
        """
        Movimentacao: Bastante movimentacao, com aceleracao e giro e giro do canhao
        Ataque: Nao altera o o angulo de radar e ao detectar inimigo
                reduz o giro do canhao e mantem atirando
        """

        global wait

        dist, i = handler.scan()        # escaneia

        # se achou bot
        if dist < VISAO:

                handler.girarCanhao(0.01)
                if handler.getTemperatura() < TEMP_DANOSA - AQUECIMENTO_TIRO:
                        handler.atirar()

        else:

                handler.setArco(PI/8.0)
                handler.acelerar(.8)
                handler.girar(.002)
                handler.girarCanhao(.05)

        wait -= 1 if wait > 0 else 0

        # trata colisao

        if wait == 0 and (handler.getPosicao().x >= TAM_X - (RAIO*2) or handler.getPosicao().x <= RAIO*2 or \
           handler.getPosicao().y >= TAM_Y - (RAIO*2) or handler.getPosicao().y <= RAIO*2):
                wait = 100
                handler.acelerar(-1.0)
                handler.girar(PI)


# Constantes multiplas de PI, para uso em calculos trigonometricos
PI = 3.1415926535897932384626433832795
DPI = 6.283185307179586476925286766559

# Macro para calcular o dano de uma colisao
def DANO_COLISAO_PAREDE(v):
	return v * 0.05

def DANO_COLISAO_BOT(v):
	return v * 0.1

# Macro para calcular o aquecimentos
def AQUEC_VELOCIDADE(v):
	return v * 0.03

def AQUEC_COLISAO_PAREDE(v):
	return v * 0.5

def AQUEC_COLISAO_BOT(v):
	return v * 0.6

def SCORE(b, s):
	return (b * b - 1) / float(s)

# macros de utilidade geral

# calcula qual numero tem o menor modulo
def minabs(a, b):
	return a if abs(a) < abs(b) else (b if a > 0 else -b)
#
#	Constantes globais
#
FATOR = 1.3125

DANO_TIRO = 4.0
AQUEC_COL_TIRO = 1.0
DANO_TEMP = 0.45

ATRITO = 0.7
ATRITO_GIRO = 0.1
VEL_TIRO = 8.0
MAX_ACEL = 1.5 * FATOR
MAX_GIRO = 0.1
MAX_GIRO_CANHAO = 0.3
MIN_ARCO = 0.01

TEMP_MAX = 100.0
TEMP_DANOSA = 75.0
TEMP_NORMAL = 25.0
RESFRIAMENTO = 0.5
AQUECIMENTO_TIRO = 2.0

MAX_VIDA = 150.0

RAIO = (int)(10*FATOR)
TAM_X = (int)(640*FATOR)
TAM_Y = (int)(480*FATOR)
VISAO = (int)(340*FATOR)

MAX_TEMPO = 10000

#
# Constantes para efeitos interessantes
#
IMPACTO_EXPLOSAO = 1.5
IMPACTO_TIRO_ANG = 0.01
IMPACTO_TIRO_VEL = 0.1


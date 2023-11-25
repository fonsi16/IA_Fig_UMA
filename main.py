#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import matriz

"""
VARIAVEIS
"""
DIAMETRO_RODA = 56
EIXO_CENTRAL = 114
DISTANCIA_ENTRE_QUADRADOS = 450
ANGULO_RODAR = 190

TAMANHO_MATRIZ = 3
TAMANHO_AMBIENTE = TAMANHO_MATRIZ + 1 

final = False  #Enquanto o programa não acaba
inicio = True  #Inicio da detecao das cores

robo_x = TAMANHO_AMBIENTE
robo_y = TAMANHO_AMBIENTE
"""
ARRAY
"""
matriz_jogo =[]
cores_lidas = []
pecas = []

"""
OBJETOS
"""
ev3 = EV3Brick()
garra = Motor(Port.A)
perna_direita = Motor(Port.B)
perna_esquerda = Motor(Port.C)
pernas = DriveBase(perna_esquerda, perna_direita, DIAMETRO_RODA, EIXO_CENTRAL)
sensor_cor = ColorSensor(Port.S2)
botao_deteta_cor = TouchSensor(Port.S3)

pernas.settings(190, 100, 190, 100)
"""
DEFINIÇÃO DE FUNÇÕES
"""
def anda_frente():
    pernas.straight(DISTANCIA_ENTRE_QUADRADOS)
    return 0

def anda_tras():
    pernas.straight(-DISTANCIA_ENTRE_QUADRADOS)
    return 0

def vira_direita():
    pernas.turn(-ANGULO_RODAR)
    wait(1000)
    return 0

def vira_esquerda():
    pernas.turn(ANGULO_RODAR)
    wait(1000)
    return 0

def gira():
    pernas.turn(2*ANGULO_RODAR)
    wait(1000)
    return 0

def deteta_cor():
    # Lê o valor da cor
    cor_detectada = sensor_cor.color()

    # Mapa de valores de cor para nomes de cor
    mapa_cores = {
        Color.BLACK: 'Preto',
        Color.BLUE: 'Azul',
        Color.GREEN: 'Verde',
        Color.YELLOW: 'Amarelo',
        Color.RED: 'Vermelho',
        Color.WHITE: 'Branco',
        Color.BROWN: 'Marrom'
    }

    # Determina a cor detectada
    cor_detectada_nome = mapa_cores.get(cor_detectada, 'Desconhecida')
    return cor_detectada_nome

def agarra_objeto():
    wait(1000)
    garra.run_time(200, 2000)
    ev3.speaker.say("Light weight")
    garra.stop() 
    return 0

def larga_objeto():
    wait(1000)
    garra.run_time(-200, 2000)
    ev3.speaker.say("Yeah Buddy")
    garra.stop() 
    return 0

def obtem_cor_por_indice(indice):
    if indice < len(cores_lidas):
        return cores_lidas[indice]
    else:
        return None 

def deteta_pecas():
    cor_detectada = deteta_cor()
    print('Cor detectada: ' + cor_detectada)

    if cor_detectada == 'Verde':
        cores_lidas.append(cor_detectada)
        pecas.append("+")
        ev3.speaker.say("Green")
        
    elif cor_detectada == 'Vermelho':
        cores_lidas.append(cor_detectada)
        pecas.append("X")
        ev3.speaker.say("Red")
        
    elif cor_detectada == 'Amarelo':
        cores_lidas.append(cor_detectada)
        pecas.append("O")
        ev3.speaker.say("Yellow")
        
    elif cor_detectada == 'Azul':
        cores_lidas.append(cor_detectada)
        pecas.append("-")
        ev3.speaker.say("Blue")
    
def leu_todas_pecas():
    i = 0
    while i < len(cores_lidas):
        cor = obtem_cor_por_indice(i)
        print(cor)
        i += 1

    print("Li todas as peças!")
    print(pecas)
            
def leitura_objetos():
    while (inicio):
        deteta_pecas()
        wait(2000)
        if botao_deteta_cor.pressed():
            inicio = False
            leu_todas_pecas()

def posicionar(linha, coluna):
    global robo_x, robo_y
    if linha==1:
        for i in range(TAMANHO_AMBIENTE):
            mo
        for i in range(TAMANHO_AMBIENTE-coluna):
            move_esquerda()


def volta_base():
    global robo_x, robo_y
    if (robo_y == TAMANHO_AMBIENTE and robo_x ==TAMANHO_AMBIENTE):
        return 1
            
def get_coordenada_vazia():
    global matriz_jogo
    for i in range(len(matriz_jogo)):
        if not (i==0 or i==TAMANHO_AMBIENTE):
            for j in range(len(matriz_jogo[i])):
                if not (j==0 or j==TAMANHO_AMBIENTE):
                    if matriz.verifica_vazio(matriz_jogo,i,j):
                        return [i,j]
                    
def coloca_peca(peca):
    global matriz_jogo
    coordenada = get_coordenada_vazia()
    if coordenada is not None:
        x = coordenada[0]
        y = coordenada[1]
        posicionar(x,y)
        matriz.inserir_objeto_matriz(peca,y,x,matriz_jogo)
        matriz.imprime_matriz(matriz_jogo)
        volta_base()

def jogar():
    global matriz_jogo
    for i in range(len(pecas)):
        coloca_peca(pecas[i])
    

#Função para saber se fez figura ou não (tem de ganhar os pontos) (temos de usar matriz)
#Função para ele ir buscar peça
#Função para ele ir meter peça a um lugar no tabuleiro

"""
    INICIO DO PROGRAMA
"""
ev3.speaker.beep()

#Cria uma matriz de Ambiente
matriz_jogo = matriz.cria_matriz(TAMANHO_MATRIZ+2)
matriz.imprime_matriz(matriz_jogo)

"""
    No início o robo verifica as cores que representam os símbolos 
        -AMARELO: O
        -VERMELHO: X
        -VERDE: +
        -AZUL: -
"""

"""
ev3.speaker.beep()
leitura_objetos()

jogar()
"""
           
#jogo()
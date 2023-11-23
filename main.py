#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


"""
VARIAVEIS
"""
DIAMETRO_RODA=56
EIXO_CENTRAL=114
DISTANCIA_ENTRE_QUADRADOS=550
ANGULO_RODAR=200

"""
ARRAY
"""
cores_lidas = []

"""
OBJETOS
"""
ev3 = EV3Brick()
garra = Motor(Port.A)
perna_direita = Motor(Port.B)
perna_esquerda = Motor(Port.C)
pernas = DriveBase(perna_esquerda, perna_direita, DIAMETRO_RODA, EIXO_CENTRAL)
sensor_cor = ColorSensor(Port.S2)

"""
DEFINIÇÃO DE FUNÇÕES
"""
ev3.speaker.beep()
def anda_frente():
    pernas.straight(DISTANCIA_ENTRE_QUADRADOS)
    return 0

def anda_tras():
    pernas.straight(-DISTANCIA_ENTRE_QUADRADOS)
    return 0

def vira_direita():
    pernas.turn(-ANGULO_RODAR)
    return 0

def vira_esquerda():
    pernas.turn(ANGULO_RODAR)
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
    garra.run_time(450, 2000)
    ev3.speaker.say("Light weight")
    garra.stop() 
    return 0

def larga_objeto():
    wait(1000)
    garra.run_time(-450, 2000)
    ev3.speaker.say("Yeah Buddy")
    garra.stop() 
    return 0


def obtem_cor_por_indice(indice):
    if indice < len(cores_lidas):
        return cores_lidas[indice]
    else:
        return None 

def deteta_pecas():
    while 1:
        cor_detectada = deteta_cor()
        print('Cor detectada: ' + cor_detectada)

        if cor_detectada == 'Verde':
            cores_lidas.append(cor_detectada)
            ev3.speaker.say("Green")
        elif cor_detectada == 'Vermelho':
            cores_lidas.append(cor_detectada)
            ev3.speaker.say("Red")
        elif cor_detectada == 'Amarelo':
            cores_lidas.append(cor_detectada)
            ev3.speaker.say("Yellow")
        elif cor_detectada == 'Azul':
            cores_lidas.append(cor_detectada)
            ev3.speaker.say("Blue")

        wait(1000)

    i = 0
    while i < len(cores_lidas):
        cor = obtem_cor_por_indice(i)
        print(cor)
        i += 1

    print("Li todas as peças!")

#Função para saber se fez figura ou não (tem de ganhar os pontos) (temos de usar matriz)
#Função para ele ir buscar peça
#Função para ele ir meter peça a um lugar no tabuleiro

"""
TESTE
"""
"""
while 1:
    cor_detectada = deteta_cor()
    print('Cor detectada: ' + cor_detectada)

    if cor_detectada == 'Verde':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Green")

        anda_frente()
        vira_esquerda()
        vira_esquerda()
        anda_tras()
    elif cor_detectada == 'Vermelho':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Red")

        anda_frente()
        vira_direita()
        vira_direita()
        anda_tras()    cor_detectada = deteta_cor()
        print('Cor detectada: ' + cor_detectada)

    elif cor_detectada == 'Amarelo':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Yellow")

        anda_frente()
        anda_tras()
        agarra_objeto()
        larga_objeto()
    elif cor_detectada == 'Azul':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Blue")

        anda_frente()
        vira_direita()
        anda_tras()

    elif cor_detectada == 'Amarelo':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Yellow")

        anda_frente()
        anda_tras()
        agarra_objeto()
        larga_objeto()
    elif cor_detectada == 'Azul':

        cores_lidas.append(cor_detectada)

        ev3.speaker.say("Blue")

        anda_frente()
        vira_direita()
        anda_tras()

    wait(1000)

    i = 0
    while i < len(cores_lidas):
        cor = obtem_cor_por_indice(i)
        print(cor)
        i += 1
"""

#deteta_pecas()
#jogo()
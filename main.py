#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
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
OBJETOS
"""
ev3 = EV3Brick()
perna_direita = Motor(Port.B)
perna_esquerda = Motor(Port.C)
pernas = DriveBase(perna_esquerda, perna_direita, DIAMETRO_RODA, EIXO_CENTRAL)


"""
DEFINIÇÃO DE FUNÇÕES
"""
ev3.speaker.beep()
def anda_frente():
    pernas.straight(DISTANCIA_ENTRE_QUADRADOS)
    return 0

def vira_direita():
    pernas.turn(-ANGULO_RODAR)
    return 0

def vira_esquerda():
    pernas.turn(ANGULO_RODAR)
    return 0

"""
TESTE
"""
while 1 :
    anda_frente()
    anda_frente()
    vira_esquerda()   
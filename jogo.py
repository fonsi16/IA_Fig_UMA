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
ANGULO_RODAR = 210

TAMANHO_MATRIZ = 3
TAMANHO_AMBIENTE = TAMANHO_MATRIZ + 1 

inicio = True

#Sentido
SUL = 1
OESTE = 2
NORTE = 3
ESTE = 4

sentido_robo = SUL
robo_x = TAMANHO_AMBIENTE
robo_y = TAMANHO_AMBIENTE
"""
ARRAY
"""
matriz_jogo =[]
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

def deteta_pecas():
    cor_detectada = deteta_cor()
    print('Cor detectada: ' + cor_detectada)

    if cor_detectada == 'Verde':
        pecas.append("+")
        ev3.speaker.say("Green")
        
    elif cor_detectada == 'Vermelho':
        pecas.append("X")
        ev3.speaker.say("Red")
        
    elif cor_detectada == 'Amarelo':
        pecas.append("O")
        ev3.speaker.say("Yellow")
        
    elif cor_detectada == 'Azul':
        pecas.append("-")
        ev3.speaker.say("Blue")
    
def leu_todas_pecas():
    print("Li todas as peças!")
    print(pecas)
            
def leitura_objetos():
    global inicio
    while (inicio):
        deteta_pecas()
        wait(2000)
        if botao_deteta_cor.pressed():
            inicio = False
            ev3.speaker.beep()
            leu_todas_pecas()

def posicionar(linha, coluna):
    global robo_x, robo_y
    x_volta = 0
    y_volta = 0
    sentido_volta = 0
    perimetro = verifica_perimetro(linha,coluna)
    if perimetro!=None:
        if perimetro==SUL:
            muda_sentido(OESTE)
            for i in range(TAMANHO_AMBIENTE - coluna):
                anda_frente()
                print("Andei")
                robo_x -= 1
                x_volta += 1
            muda_sentido(NORTE)
            for j in range(TAMANHO_AMBIENTE - linha -1):
                anda_frente()
                robo_y -= 1
                y_volta += 1
            sentido_volta = SUL
            print("Acabei")
        elif perimetro==ESTE:
            muda_sentido(NORTE)
            for j in range(TAMANHO_AMBIENTE - linha):
                anda_frente()
                robo_y -= 1
                y_volta += 1
            muda_sentido(OESTE)
            for i in range(TAMANHO_AMBIENTE - coluna -1):
                anda_frente()
                robo_x -= 1
                x_volta += 1
            sentido_volta = ESTE
        elif perimetro==OESTE:
            muda_sentido(OESTE)
            for i in range(TAMANHO_AMBIENTE - coluna +1):
                anda_frente()
                robo_x -= 1
                x_volta += 1
            muda_sentido(NORTE)
            for j in range(TAMANHO_AMBIENTE - linha):
                anda_frente()
                robo_y -= 1
                y_volta += 1
            muda_sentido(ESTE)
            sentido_volta = OESTE
        elif perimetro==NORTE:
            muda_sentido(NORTE)
            for j in range(TAMANHO_AMBIENTE - linha +1):
                anda_frente()
                robo_y -= 1
                y_volta += 1
            muda_sentido(OESTE)
            for i in range(TAMANHO_AMBIENTE - coluna):
                anda_frente()
                robo_x -= 1
                x_volta += 1
            muda_sentido(SUL)
            sentido_volta = NORTE
        return [x_volta, y_volta, sentido_volta]
    else:
        print("Não consigo chegar à casa")
        return [""]
    


def verifica_perimetro(linha, coluna):
    global matriz_jogo
    if matriz.verifica_vazio(matriz_jogo,linha+1,coluna):
        return SUL
    elif matriz.verifica_vazio(matriz_jogo,linha,coluna+1):
        return ESTE
    elif matriz.verifica_vazio(matriz_jogo,linha-1,coluna):
        return NORTE
    elif matriz.verifica_vazio(matriz_jogo,linha,coluna-1):
        return OESTE
    else:
        return None
    
def muda_sentido(sentido):
    global sentido_robo
    
    if(sentido == SUL):
        if(sentido_robo == NORTE):
            gira()
        elif(sentido_robo == ESTE):
            vira_direita()
        elif(sentido_robo == OESTE):
            vira_esquerda()
    
    elif(sentido == NORTE):
        if(sentido_robo == SUL):
            gira()
        elif(sentido_robo == OESTE):
            vira_direita()
        elif(sentido_robo == ESTE):
            vira_esquerda()
    
    elif(sentido == OESTE):
        if(sentido_robo == ESTE):
            gira()
        elif(sentido_robo == SUL):
            vira_direita()
        elif(sentido_robo == NORTE):
            vira_esquerda()
            
    elif(sentido == ESTE):
        if(sentido_robo == OESTE):
            gira()
        elif(sentido_robo == NORTE):
            vira_direita()
        elif(sentido_robo == SUL):
            vira_esquerda()
    
    sentido_robo = sentido
    
def voltar (x_voltar, y_voltar, sentido):
    global robo_x, robo_y

    if sentido==SUL:
        muda_sentido(SUL)
        for j in range(y_voltar):
            anda_frente()
            robo_y += 1
        muda_sentido(ESTE)
        for i in range(x_voltar):
            anda_frente()
            robo_x += 1
        muda_sentido(SUL)
    elif sentido==ESTE:
        muda_sentido(ESTE)
        for i in range(x_voltar):
            anda_frente()
            robo_x += 1
        muda_sentido(SUL)
        for j in range(y_voltar):
            anda_frente()
            robo_y += 1
    elif sentido==OESTE:
        muda_sentido(SUL)
        for j in range(y_voltar):
            anda_frente()
            robo_y += 1
        muda_sentido(ESTE)
        for i in range(x_voltar):
            anda_frente()
            robo_x += 1
        muda_sentido(SUL)
    elif sentido==NORTE:
        muda_sentido(ESTE)
        for i in range(x_voltar):
            anda_frente()
            robo_x += 1
        muda_sentido(SUL)
        for j in range(y_voltar):
            anda_frente()
            robo_y += 1
    
    
def volta_base_bordas():
    global robo_x, robo_y
    if (robo_y == TAMANHO_AMBIENTE and robo_x ==TAMANHO_AMBIENTE):
        muda_sentido(SUL)
        ev3.speaker.say("Home")
        return 1
    else:
        if (robo_y == 0 and robo_x < TAMANHO_AMBIENTE) or (robo_y == TAMANHO_AMBIENTE and robo_x < TAMANHO_AMBIENTE) :
            muda_sentido(ESTE)
            for i in range(TAMANHO_AMBIENTE - robo_x):
                anda_frente()
                robo_x+=1

        elif (robo_y < TAMANHO_AMBIENTE and robo_x == TAMANHO_AMBIENTE) or (robo_x == 0 and (robo_y > 0 and robo_y < TAMANHO_AMBIENTE)) :
            muda_sentido(SUL)
            for i in range(TAMANHO_AMBIENTE - robo_y):
                anda_frente()
                robo_y+=1
               
        return volta_base_bordas()
        
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
    
    x_voltar = 0
    y_voltar = 0
    sentido_voltar = 0
    if coordenada is not None:
        x = coordenada[0]
        y = coordenada[1]
        
        agarra_objeto()
        
        volta = posicionar(x,y)
        
        if volta == [""]:
            matriz.inserir_objeto_matriz("!",x,y,matriz_jogo)
            ev3.speaker.say("heavy weight")
            larga_objeto()
            return coloca_peca(peca)
        else:
            x_voltar = volta[0]
            y_voltar = volta[1]
            sentido_voltar = volta[2]
            
            pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.75)
            larga_objeto()
            pernas.straight(-DISTANCIA_ENTRE_QUADRADOS*0.75)
            matriz.inserir_objeto_matriz(peca,x,y,matriz_jogo)
            matriz.imprime_matriz(matriz_jogo)
            voltar(x_voltar, y_voltar, sentido_voltar)
            #volta_base_bordas()

def jogar():
    global matriz_jogo, pecas
    wait(5000)
    for i in range(len(pecas)):
        coloca_peca(pecas[i])
        
    ev3.speaker.say("I go hard in Salsa Jeans")
    

#Função para saber se fez figura ou não (tem de ganhar os p<ontos) (temos de usar matriz)
#Função para ele ir buscar peça
#Função para ele ir meter peça a um lugar no tabuleiro

"""
    INICIO DO PROGRAMA
"""

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

ev3.speaker.beep()
leitura_objetos()
#larga_objeto()
jogar()

           
#jogo()
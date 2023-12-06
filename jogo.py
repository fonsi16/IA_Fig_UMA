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
DISTANCIA_ENTRE_QUADRADOS = 680
ANGULO_RODAR = 230

TAMANHO_MATRIZ = 5
TAMANHO_AMBIENTE = TAMANHO_MATRIZ + 1 

inicio = True
pontos=0
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
"""
pecas = ["0", "0", "0", "0", "0",
         "0", "*", "0", "0", "0",
         "0", "0", "0", "+", "0",
         "0", "0", "0", "0", "0",
         "0", "0", "0", "0", "0"]
"""

pecas = ["X", "O", "X", "O", "O",
         "O", "X", "O", "O", "O",
         "X", "O", "X", "+", "O",
         "O", "O", "O", "O", "O",
         "O", "O", "O", "O", "O"]

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
    global robo_x, robo_y, sentido_robo
    
    # Atualize as coordenadas de acordo com o sentido atual do robô
    if sentido_robo == SUL:
        robo_y += 1
    elif sentido_robo == OESTE:
        robo_x -= 1
    elif sentido_robo == NORTE:
        robo_y -= 1
    elif sentido_robo == ESTE:
        robo_x += 1
    pernas.straight(DISTANCIA_ENTRE_QUADRADOS)
    ev3.speaker.say("forward")

def anda_tras():
    global robo_x, robo_y, sentido_robo
    
    # Atualize as coordenadas para trás de acordo com o sentido atual do robô
    if sentido_robo == SUL:
        robo_y -= 1
    elif sentido_robo == OESTE:
        robo_x += 1
    elif sentido_robo == NORTE:
        robo_y += 1
    elif sentido_robo == ESTE:
        robo_x -= 1
    pernas.straight(-DISTANCIA_ENTRE_QUADRADOS)
    ev3.speaker.say("backwards")

def vira_direita():
    global sentido_robo
    
    # Atualize o sentido do robô para virar à direita
    if sentido_robo == SUL:
        sentido_robo = OESTE
    elif sentido_robo == OESTE:
        sentido_robo = NORTE
    elif sentido_robo == NORTE:
        sentido_robo = ESTE
    elif sentido_robo == ESTE:
        sentido_robo = SUL
        
    pernas.turn(-ANGULO_RODAR)
    ev3.speaker.say("right")
    wait(1000)

def vira_esquerda():
    global sentido_robo
    
    # Atualize o sentido do robô para virar à esquerda
    if sentido_robo == SUL:
        sentido_robo = ESTE
    elif sentido_robo == OESTE:
        sentido_robo = SUL
    elif sentido_robo == NORTE:
        sentido_robo = OESTE
    elif sentido_robo == ESTE:
        sentido_robo = NORTE
        
    pernas.turn(ANGULO_RODAR)
    ev3.speaker.say("left")    
    wait(1000)
    return 0

def gira():
    global sentido_robo
    
    # Atualize o sentido do robô para virar à direita
    if sentido_robo == SUL:
        sentido_robo = NORTE
    elif sentido_robo == OESTE:
        sentido_robo = ESTE
    elif sentido_robo == NORTE:
        sentido_robo = SUL
    elif sentido_robo == ESTE:
        sentido_robo = OESTE
        
    pernas.turn(2*ANGULO_RODAR)
    wait(1000)

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

def larga_objeto():
    wait(1000)
    garra.run_time(-200, 2000)
    ev3.speaker.say("Yeah Buddy")
    garra.stop() 

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
            
def leitura_objetos():
    global inicio
    while (inicio):
        deteta_pecas()
        wait(2000)
        if botao_deteta_cor.pressed():
            inicio = False
            ev3.speaker.beep()

def posicionar(linha, coluna):
    global robo_x, robo_y
    caminho = melhor_rota(linha, coluna, [], [], 0)
    if(caminho!=[]):
        caminho.reverse()

        for i in range(len(caminho)-1):
            movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
                
        caminho.reverse()
    return caminho
   
def verifica_perimetro(linha, coluna):
    global matriz_jogo
    coordenadas=[]
    if matriz.verifica_vazio(matriz_jogo,linha+1,coluna):
        coordenadas.append([linha+1,coluna])
    if matriz.verifica_vazio(matriz_jogo,linha,coluna+1):
        coordenadas.append([linha,coluna+1])
    if matriz.verifica_vazio(matriz_jogo,linha-1,coluna):
        coordenadas.append([linha-1,coluna])
    if matriz.verifica_vazio(matriz_jogo,linha,coluna-1):
        coordenadas.append([linha,coluna-1])
    return coordenadas
    
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
    
def voltar (caminho):
    global matriz_jogo
    for i in range(len(caminho)-1):
        movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
    muda_sentido(SUL)
          
def get_coordenada_vazia():
    global matriz_jogo
    for i in range(len(matriz_jogo)):
        if not (i==0 or i==TAMANHO_AMBIENTE):
            for j in range(len(matriz_jogo[i])):
                if not (j==0 or j==TAMANHO_AMBIENTE):
                    if matriz.verifica_vazio(matriz_jogo,i,j):
                        return [i,j]

def melhor_rota(linha, coluna, caminho, nao_ir, contador):
    if (linha == TAMANHO_AMBIENTE) and (coluna == TAMANHO_AMBIENTE):
        return caminho
    
    elif (linha == 0 and coluna < TAMANHO_AMBIENTE) or (linha == TAMANHO_AMBIENTE and coluna < TAMANHO_AMBIENTE) :
        caminho.append([linha, coluna+1])
        return melhor_rota(linha, coluna+1, caminho, nao_ir, contador)
            
    elif (linha < TAMANHO_AMBIENTE and coluna == TAMANHO_AMBIENTE) or (coluna == 0 and (linha > 0 and linha < TAMANHO_AMBIENTE)) :
        caminho.append([linha+1, coluna])
        return melhor_rota(linha+1, coluna, caminho , nao_ir, contador)
    
    else:
        if [linha, coluna] in nao_ir:
            if (len(caminho)==0):
                contador+=1
                if(contador==len(verifica_perimetro(nao_ir[0][0],nao_ir[0][1]))):
                    return [] 
            caminho.pop()
            return melhor_rota(caminho[-1][0], caminho[-1][1], caminho, nao_ir, contador) 
        
        nao_ir.append([linha, coluna])
        coordenadas = verifica_perimetro(linha,coluna)
        
        if coordenadas != []:
            for i in range(len(coordenadas)):
                if(coordenadas[i] not in nao_ir):
                    caminho.append([coordenadas[i][0], coordenadas[i][1]])
                    return melhor_rota(coordenadas[i][0], coordenadas[i][1],
                                caminho, nao_ir, contador)
            caminho.pop()
            return melhor_rota(coordenadas[-1][0], coordenadas[-1][1],
                                caminho, nao_ir, contador)
        else:
            return []

def movimento(linha_atual, coluna_atual, proxima_linha, proxima_coluna):
    if (proxima_linha>linha_atual):
        muda_sentido(SUL)
        anda_frente()
    elif(proxima_linha<linha_atual):
        muda_sentido(NORTE)
        anda_frente()
    elif(proxima_coluna>coluna_atual):
        muda_sentido(ESTE)
        anda_frente()
    elif(proxima_coluna<coluna_atual):
        muda_sentido(OESTE)
        anda_frente()

def numero_pecas(peca):
    global matriz_jogo
    contador = 0
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if matriz_jogo[i][j] == peca :
                contador += 1
    return contador
            
def coloca_peca(peca):
    global matriz_jogo
    coordenada = get_coordenada_vazia()
    
    if coordenada is not None:
        x = coordenada[0]
        y = coordenada[1]
        
        agarra_objeto()
        
        volta = posicionar(x,y)
        
        if volta == []:
            matriz.inserir_objeto_matriz("!",x,y,matriz_jogo)
            ev3.speaker.say("heavy weight")
            larga_objeto()
            return coloca_peca(peca)
        else:    
            pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.75)
            larga_objeto()
            pernas.straight(-DISTANCIA_ENTRE_QUADRADOS*0.75)
            matriz.inserir_objeto_matriz(peca,x,y,matriz_jogo)
            matriz.imprime_matriz(matriz_jogo)
            voltar(volta)
            matriz.imprime_matriz(matriz_jogo)
            verifica_peca(peca,x,y)

def verifica_peca(peca, linha, coluna):
    global pontos, matriz_jogo
    coordenadas_limpar=[]
    contador=0
    seguida=True
    
    if peca == "-":
        contador_auxiliar = 0 
    
        for i in range(len(matriz_jogo[linha])):
            if(matriz_jogo[linha][i]=="-" and seguida):
                contador_auxiliar += 1
                coordenadas_limpar.append([linha,i])
                if contador_auxiliar>contador:
                    contador=contador_auxiliar
            elif(matriz_jogo[linha][i]=="-" and not seguida):
                seguida=True
                contador_auxiliar += 1
                coordenadas_limpar = []
                coordenadas_limpar.append([linha,i])
            else:
                seguida = False
                contador_auxiliar = 0
                
        if(contador>1):
            ev3.speaker.say("Did a minus")
            ev3.speaker.say(str(2**contador))
            pontos += 2**contador
            limpa_pecas(coordenadas_limpar)
      
    if peca == "+":
        #peca máxima
        if (numero_pecas(peca)>=(TAMANHO_MATRIZ*2-1) and (coluna==TAMANHO_AMBIENTE//2 or linha == TAMANHO_AMBIENTE//2)):
            for i in range(1,TAMANHO_AMBIENTE):
                if(seguida):
                    if not (matriz_jogo[TAMANHO_AMBIENTE//2][i] == "+" and matriz_jogo[i][TAMANHO_AMBIENTE//2] == "+"):
                        seguida = False
            if seguida:
                ev3.speaker.say("Did a plus")
                ev3.speaker.say(str(2**(TAMANHO_MATRIZ*2-1)))
                pontos += 2**(TAMANHO_MATRIZ*2-1)
                for i in range(1,TAMANHO_AMBIENTE):
                    matriz_jogo[TAMANHO_AMBIENTE//2][i] = " "
                    matriz_jogo[i][TAMANHO_AMBIENTE//2] = " "
        #menor
        #cantos ->> ímpossivel
        if((linha==1 and coluna==1) or
            (linha==1 and coluna==TAMANHO_AMBIENTE-1) or
            (linha==TAMANHO_AMBIENTE-1 and coluna== 1) or
            (linha==TAMANHO_AMBIENTE-1 and coluna==TAMANHO_AMBIENTE-1)):
            return 0

        #casos possíveis
        else:
            coordenadas=coordenadas_perimentros_mais(linha, coluna)
            for i in range(len(coordenadas)):
                if verifica_mais(coordenadas[i][0], coordenadas[i][1]):
                    break
    
    if peca == "X":
        #peca máxima
        if (numero_pecas(peca)>=(TAMANHO_MATRIZ*2-1) and (linha==2 or linha==4) and (coluna==2 or coluna==4) ):
            for i in range(1,TAMANHO_AMBIENTE):
                if seguida:
                    if not (matriz_jogo[i][i]=="X" and matriz_jogo[i][TAMANHO_AMBIENTE-i]=="X"):
                        seguida = False
            
            if seguida:
                ev3.speaker.say("Did a X")
                ev3.speaker.say(str(2**(TAMANHO_MATRIZ*2-1)))
                pontos += 2**(TAMANHO_MATRIZ*2-1)
                for i in range(1,TAMANHO_AMBIENTE):
                    matriz_jogo[i][i] = " "
                    matriz_jogo[i][TAMANHO_AMBIENTE-i] = " "
        
        #pecas possiveis
        coordenadas=coordenadas_perimentros_vezes(linha, coluna)
        if not verifica_x(linha, coluna):
            for i in range(len(coordenadas)):
                if verifica_x(coordenadas[i][0], coordenadas[i][1]):
                    break 

    if peca == "O":
        verifica_bola()
            
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if matriz_jogo[i][j]=="!":
                if(len(verifica_perimetro(i,j))>0):
                    matriz_jogo[i][j] = " "
 
def verifica_bola():
    global matriz_jogo, pontos
    
    #percorre a matriz por linha
    for i in range(1,TAMANHO_MATRIZ):
        
        #verifica se na linha existe uma bola
        if "O" in matriz_jogo[i]:
            
            #percorre as colunas
            for j in range(1, TAMANHO_AMBIENTE):
                
                #verifica se na posição atual, à direita e em baixo existe uma bola
                if(matriz_jogo[i][j]=="O" and matriz_jogo[i+1][j]=="O" and matriz_jogo[i][j+1]=="O"):
                    
                    #variaveis locais que irão ajudar (numa proxima coluna estas variaveis voltam a ficar a zero)
                    bolas_de_seguida=0
                    contador_horizontal=0
                    contador_vertical=0
                    seguinte=True
                    coordenadas_limpar=[]
                    
                    #adiciona a coordenada atual 
                    coordenadas_limpar.append([i,j])
                    
                    #verifica se nas proximas colunas quantos bolas de seguida existem
                    for proxima_coluna in range(j+1,TAMANHO_AMBIENTE):
                        if(matriz_jogo[i][proxima_coluna]=="O" and seguinte):
                            contador_horizontal+=1
                        else:
                            seguinte=False
                    
                    seguinte = True
                    
                    #verifica se nas proximas linhas quantos bolas de seguida existem
                    for proxima_linha in range(i+1,TAMANHO_AMBIENTE):
                        if(matriz_jogo[proxima_linha][j]=="O" and seguinte):
                            contador_vertical+=1
                        else:
                            seguinte=False
                     
                    """
                    se uma das variaveis é menor do que a outra
                    faz sentido fazer a menor porque a maior já náo será possível
                    """       
                    if(contador_vertical<contador_horizontal):
                        bolas_de_seguida=contador_vertical
                    else:
                        bolas_de_seguida=contador_horizontal
                    
                    """
                    adiciona ao array para limpar as
                    coordenadas que percorremos para baixo e 
                    para a direita onde contêm uma bola
                    """
                    for adicona_lixo in range(1,bolas_de_seguida+1):
                        coordenadas_limpar.append([i,j+adicona_lixo])
                        coordenadas_limpar.append([i+adicona_lixo,j])
                        
                    #caso a tenha mais que uma bola de seguida para baixo e para a direita
                    while (bolas_de_seguida>1):
                        seguinte=True
                        
                        """
                        verifica se na ultima linha de uma possivel bola existe o resto das 
                        bolas para formar a figura
                        
                        """
                        for linha_baixo in range(j+1,j+bolas_de_seguida+1):
                            if not (matriz_jogo[i+bolas_de_seguida][linha_baixo] == "O" and seguinte):
                                seguinte=False
                            else:
                                coordenadas_limpar.append([i+bolas_de_seguida,linha_baixo])
                        """
                        caso a ultima linha nao seja tudo bola verifica 
                        para uma vola menor diminuido a variavel
                        """
                        if not seguinte:
                            bolas_de_seguida-=1
                            
                            """
                            caso tenha passa para a a linha à direita
                            """
                        else:
                            """
                            verifica se na ultima linha de uma possivel bola existe o resto das 
                            bolas para formar a figura
                            """
                            for linha_direita in range(i+1, i+bolas_de_seguida+1):
                                if not (matriz_jogo[linha_direita][j+bolas_de_seguida] == "O" and seguinte):
                                    seguinte=False
                                else:
                                    coordenadas_limpar.append([linha_direita, j+bolas_de_seguida])
                                    
                            """
                            mesma coisa de cima 
                            """
                            if not seguinte:
                                bolas_de_seguida-=1
                                
                                """
                                caso verifique se que é uma bola adiciona
                                os pontos e limpa as coordenadas e acaba a função
                                """
                            else:
                                limpa_pecas(coordenadas_limpar)
                                pontos += 2**(len(coordenadas_limpar))
                                ev3.speaker.say("I Did a Ball")
                                ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                                return 0
                    
                    """
                    caso seja a menor bola 2 por 2
                    """
                    if(bolas_de_seguida==1 and matriz_jogo[i+1][j+1]=="O"):
                        coordenadas_limpar.append([i+1,j+1])
                        limpa_pecas(coordenadas_limpar)
                        pontos += 2**(len(coordenadas_limpar))
                        ev3.speaker.say("I Did a Ball")
                        ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                        return 0

def verifica_x(linha, coluna):
    global matriz_jogo, pontos
    if (matriz_jogo[linha-1][coluna-1] == "X" and
        matriz_jogo[linha+1][coluna+1] == "X" and 
        matriz_jogo[linha+1][coluna-1] == "X" and 
        matriz_jogo[linha-1][coluna+1] == "X"):
        
        matriz_jogo[linha-1][coluna-1] = " "
        matriz_jogo[linha+1][coluna+1] = " "
        matriz_jogo[linha+1][coluna-1] = " "
        matriz_jogo[linha-1][coluna+1] = " "
        matriz_jogo[linha][coluna] = " "
        
        ev3.speaker.say("Did a X")
        ev3.speaker.say(str(2**5))
        pontos += 2**5
        return True
    return False

def coordenadas_perimentros_vezes(linha, coluna):
    global matriz_jogo
    coordenadas=[[linha+1,coluna+1],[linha+1, coluna-1], [linha-1, coluna+1], [linha-1, coluna-1]]
    coordenadas_aux=[]
    for i in range(len(coordenadas)):
        if (matriz_jogo[coordenadas[i][0]][coordenadas[i][1]]=="X" and
            (coordenadas[i][0]>1 and coordenadas[i][0]<5) and
            (coordenadas[i][1]>1 and coordenadas[i][1<5])):
            coordenadas_aux.append(coordenadas[i])
    
    return coordenadas_aux
                        
def coordenadas_perimentros_mais(linha, coluna):
    global matriz_jogo
    coordenadas=[]
    if ((matriz_jogo[linha+1][coluna]=="+") and
        (linha+1 > 1 and linha+1 < TAMANHO_AMBIENTE-1) and
        (coluna>1 and coluna < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha+1, coluna])
        
    if ((matriz_jogo[linha-1][coluna]=="+") and
        (linha-1 > 1 and linha-1 < TAMANHO_AMBIENTE-1) and
        (coluna>1 and coluna < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha-1, coluna])
        
    if ((matriz_jogo[linha][coluna+1]=="+") and
        (linha > 1 and linha < TAMANHO_AMBIENTE-1) and
        (coluna+1>1 and coluna+1 < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha, coluna+1])
        
    if ((matriz_jogo[linha][coluna-1]=="+") and
        (linha> 1 and linha < TAMANHO_AMBIENTE-1) and
        (coluna-1 >1 and coluna-1 < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha, coluna-1])
    
    return coordenadas

def verifica_mais(linha, coluna):
    global matriz_jogo, pontos
    if (matriz_jogo[linha-1][coluna] == "+" and
        matriz_jogo[linha+1][coluna] == "+" and 
        matriz_jogo[linha][coluna+1] == "+" and 
        matriz_jogo[linha][coluna-1] == "+"):
        
        matriz_jogo[linha-1][coluna] = " "
        matriz_jogo[linha+1][coluna] = " "
        matriz_jogo[linha][coluna+1] = " "
        matriz_jogo[linha][coluna-1] = " "
        matriz_jogo[linha][coluna] = " "
        
        ev3.speaker.say("Did a plus")
        ev3.speaker.say(str(2**5))
        pontos += 2**5
        return True
    return False
          
def limpa_pecas(coordenadas_limpar):
    global matriz_jogo
    if(len(coordenadas_limpar)>0):
        for coodenada in coordenadas_limpar:
            matriz_jogo[coodenada[0]][coodenada[1]] = " "

def retira_pontos():
    global pontos, matriz_jogo, pecas
    contador = 0
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if (matriz_jogo[i][j]!=" ") and matriz_jogo[i][j]!="!":
                contador += 1
    if contador > 0:
        if(pontos - 2**contador<=0):
            pontos=0
        else:   
            pontos -= 2**contador


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
#leitura_objetos()
#larga_objeto()
jogar()
retira_pontos()
print(pontos)

           
#jogo()
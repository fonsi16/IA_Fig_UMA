#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import matriz

#VARIAVEIS
DIAMETRO_RODA = 56
EIXO_CENTRAL = 114
#Distância entre o centro de um quadrado e o próximo
DISTANCIA_ENTRE_QUADRADOS = 680
#Ângulo de 90 graus
ANGULO_RODAR = 230

#Tamanho da matriz/tabuleiro de jogo (tamanho de um lado)
TAMANHO_MATRIZ = 5 
#Tamanho da matriz do ambiente do robô (matriz que se pode movimentar)
TAMANHO_AMBIENTE = TAMANHO_MATRIZ + 1 

inicio = True
#Pontos totais do robô
pontos=0 

#Sentidos
SUL = 1
OESTE = 2
NORTE = 3
ESTE = 4

#Sentido do robô (sendo que começa sempre virado para Sul)
sentido_robo = SUL 
#Localização X do robô no tabuleiro
robo_x = TAMANHO_AMBIENTE 
#Localização Y do robô no tabuleiro
robo_y = TAMANHO_AMBIENTE 

#Array da matriz/ambiente de jogo
matriz_jogo =[]
#Array das peças lidas no inicio do jogo
"""
pecas = []
"""
pecas = ["X", "O", "X", "O", "O",
         "O", "X", "O", "O", "O",
         "X", "O", "X", "+", "O",
         "O", "O", "O", "O", "O",
         "O", "O", "O", "O", "O"]

#OBJETOS
#Brick do robô
ev3 = EV3Brick() 
#Garra do robô
garra = Motor(Port.A) 
#Perna direita do robô
perna_direita = Motor(Port.B) 
#Perna esquerda do robô
perna_esquerda = Motor(Port.C) 
#Junção das duas pernas do robô em um só objeto
pernas = DriveBase(perna_esquerda, perna_direita, DIAMETRO_RODA, EIXO_CENTRAL) 
#Sensor de cor
sensor_cor = ColorSensor(Port.S2) 
#Botão para começar jogo
botao_deteta_cor = TouchSensor(Port.S3) 

'''
Configuração das pernas (
    Velocidade de andamento,
    Acelaração de andamento,
    Velocidade de viragem,
    Acelaração de viragem)
'''
pernas.settings(190, 100, 190, 100)

#DEFINIÇÃO DE FUNÇÕES
#Robô anda para a frente um quadrado
def anda_frente():
    global robo_x, robo_y, sentido_robo
    
    #Atualiza as coordenadas de acordo com o sentido atual do robô
    if sentido_robo == SUL:
        robo_y += 1
    elif sentido_robo == OESTE:
        robo_x -= 1
    elif sentido_robo == NORTE:
        robo_y -= 1
    elif sentido_robo == ESTE:
        robo_x += 1
    #Diz que vai andar para a frente
    ev3.speaker.say("Forward")
    #Anda para a frente a distância de uma quadrado
    pernas.straight(DISTANCIA_ENTRE_QUADRADOS)

#Robô anda para a trás um quadrado  
def anda_tras():
    global robo_x, robo_y, sentido_robo
    
    # Atualiza as coordenadas de acordo com o sentido atual do robô
    if sentido_robo == SUL:
        robo_y -= 1
    elif sentido_robo == OESTE:
        robo_x += 1
    elif sentido_robo == NORTE:
        robo_y += 1
    elif sentido_robo == ESTE:
        robo_x -= 1
    #Diz que vai andar para trás
    ev3.speaker.say("Backwards")
    #Anda para trás a distância de uma quadrado
    pernas.straight(-DISTANCIA_ENTRE_QUADRADOS)

#Vira o robô 90 graus para a direita
def vira_direita():
    global sentido_robo
    
    # Atualiza o sentido do robô pois virou à direita
    if sentido_robo == SUL:
        sentido_robo = OESTE
    elif sentido_robo == OESTE:
        sentido_robo = NORTE
    elif sentido_robo == NORTE:
        sentido_robo = ESTE
    elif sentido_robo == ESTE:
        sentido_robo = SUL
    #Diz que vai virar para a direta
    ev3.speaker.say("Right")
    #Vira para a direita 90 graus
    pernas.turn(-ANGULO_RODAR)
    #Espera 1 segundo
    wait(1000)

#Vira o robô 90 graus para a esquerda
def vira_esquerda():
    global sentido_robo
    
    # Atualiza o sentido do robô pois virou à esquerda
    if sentido_robo == SUL:
        sentido_robo = ESTE
    elif sentido_robo == OESTE:
        sentido_robo = SUL
    elif sentido_robo == NORTE:
        sentido_robo = OESTE
    elif sentido_robo == ESTE:
        sentido_robo = NORTE
    #Diz que vai virar para a esquerda
    ev3.speaker.say("Left")    
    #Vira para a esquerda 90 graus
    pernas.turn(ANGULO_RODAR)
    #Espera 1 segundo
    wait(1000)
 
#Vira o robô 180 graus
def gira():
    global sentido_robo
    
    # Atualiza o sentido do robô pois virou 180 graus 
    if sentido_robo == SUL:
        sentido_robo = NORTE
    elif sentido_robo == OESTE:
        sentido_robo = ESTE
    elif sentido_robo == NORTE:
        sentido_robo = SUL
    elif sentido_robo == ESTE:
        sentido_robo = OESTE
    #Diz que vai virar
    ev3.speaker.say("Turn")
    #Vira 180 graus
    pernas.turn(2*ANGULO_RODAR)
    #Espera 1 segundo
    wait(1000)

#Deteta a cor passada no sensor de cores
def deteta_cor():
    #Lê o valor da cor
    cor_detetada = sensor_cor.color()

    #Mapa de valores de cor para nomes de cor
    mapa_cores = {
        Color.BLUE: 'Azul',
        Color.GREEN: 'Verde',
        Color.YELLOW: 'Amarelo',
        Color.RED: 'Vermelho',
    }

    #Determina a cor detetada
    cor_detetada_nome = mapa_cores.get(cor_detetada, 'Desconhecida')
    #Retorna o nome da cor detetada
    return cor_detetada_nome

#Fecha a garra do robô de modo a agarrar uma peça
def agarra_objeto():
    #Espera um segundo
    wait(1000)
    #Corre o motor a uma certa velocidade durante um período de tempo (Velocidade, Tempo)
    garra.run_time(200, 2000)
    #Indica que agarrou uma peça
    ev3.speaker.say("Light weight")
    #Para o motor
    garra.stop() 

#Abre a garra do robô de modo a largar uma peça
def larga_objeto():
    #Espera um segundo
    wait(1000)
    #Corre o motor a uma certa velocidade negativa durante um período de tempo (Velocidade, Tempo)
    garra.run_time(-200, 2000)
    #Indica que largou a peça
    ev3.speaker.say("Yeah Buddy")
    #Para o motor
    garra.stop() 

#Deteta a cor das peças passadas e adiciona no array das peças
def deteta_pecas():
    #Lê o nome da cor
    cor_detectada = deteta_cor()
    #Imprime a cor lida
    print('Cor detectada: ' + cor_detectada)

    #Adiciona a peça no array dependendo da cor
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

#Período da deteção de peças            
def leitura_objetos():
    global inicio
    #Enquanto estś no período de deteção
    while (inicio):
        #Deteta e guarda as peças
        deteta_pecas()
        #Espera 2 segundos
        wait(2000)
        #Se o botão foi clicado muda a variável para falso
        if botao_deteta_cor.pressed():
            inicio = False
            #Indica que acabou o período
            ev3.speaker.beep()

#Robô desloca-se para um sítio no tabuleiro (para meter a peça)
def posicionar(linha, coluna):
    global robo_x, robo_y
    #Descobre a melhor rota do sítio no tabuleiro até a localização do robô
    caminho = melhor_rota(linha, coluna, [], [], 0)
    #Se existe uma rota possível
    if(caminho!=[]):
        #Reverte a rota
        caminho.reverse()

        #Percorre a rota reversa assim indo da sua posição até ao sítio pertendido
        for i in range(len(caminho)-1):
            movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
                
        #Reverte a rota denovo assim voltando ao normal
        caminho.reverse()
    #Retorna a rota
    return caminho
   
#Verifica todas as peças à volta 
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


#Funcao que orienta o robo no sentido correto, quando se esta a mover
#recebendo a linha e coluna que esta agora, e a proxima linha e coluna
def movimento(linha_atual, coluna_atual, proxima_linha, proxima_coluna):

    #se o proximo movimento do robô é ir para baixo ele vai virar para sul
    if (proxima_linha>linha_atual):
        muda_sentido(SUL)
        anda_frente()

     #se o proximo movimento do robô é ir para cima ele vai virar para norte
    elif(proxima_linha<linha_atual):
        muda_sentido(NORTE)
        anda_frente()

     #se o proximo movimento do robô é ir para direita ele vai virar para este
    elif(proxima_coluna>coluna_atual):
        muda_sentido(ESTE)
        anda_frente()

     #se o proximo movimento do robô é ir para esquerda ele vai virar para oeste
    elif(proxima_coluna<coluna_atual):
        muda_sentido(OESTE)
        anda_frente()

#Funcao para verificar o numero de pecas dessa peca que tem na matriz de jogo
def numero_pecas(peca):
    global matriz_jogo

    #Variavel para adicionar quantas pecas tem 
    contador = 0
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if matriz_jogo[i][j] == peca :

                #Aumenta o contador
                contador += 1
    return contador
    
#Funcao para colocar a peca que recebeu na matriz
def coloca_peca(peca):

    global matriz_jogo, pecas

    #Recebe a coordenada onde pode colocar a peca
    coordenada = get_coordenada_vazia()
    
    #Se recebeu uma coordenada
    if coordenada is not None:

        #adiciona às variaveis os valores dessa coordenada 
        x = coordenada[0]
        y = coordenada[1]
        
        #Vai agarrar na proxima peca
        agarra_objeto()
        
        #Variavel que guarda as coordenadas necessarias para voltar
        volta = posicionar(x,y)
        
        #Se não consegue voltar quer dizer que não pode por lá a peca colocando um ! nesse lugar
        if volta == []:
            matriz.inserir_objeto_matriz("!",x,y,matriz_jogo)
            ev3.speaker.say("heavy weight")
            larga_objeto()
            return coloca_peca(peca)
         
         #se consegue por a peca nesse lugar vai colocar a peca e voltar para a casa inicial
         #tirando a peca da lista de pecas e verificar se fez uma figura depois de colocar essa peca
         #e permite visualizacao no terminal do que o robô fez
        else:    
            pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.75)
            larga_objeto()
            pernas.straight(-DISTANCIA_ENTRE_QUADRADOS*0.75)
            matriz.inserir_objeto_matriz(peca,x,y,matriz_jogo)
            matriz.imprime_matriz(matriz_jogo)
            voltar(volta)
            matriz.imprime_matriz(matriz_jogo)
            verifica_peca(peca,x,y)
            pecas.pop(0)

#Funcao chamada quando ele coloca uma peca na matriz de jogo
def verifica_peca(peca, linha, coluna):
    global pontos, matriz_jogo

    #variaveis para guardar a posicao de pecas 
    coordenadas_limpar=[]
    contador=0
    seguida=True
    
    if peca == "-":
        contador_auxiliar = 0 
    
        #Percorre a linha do ultimo "-" metido
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

     #Vai verificar se fez uma bola se a peca for "O"
    if peca == "O":
        verifica_bola()
            
    #Vai percorrer a matriz de jogo e vai verificar se os ! já tem espacos à volta livres em que o robo possa passar
    #e cheguar a esse !, limpando e permitindo ao robo voltar a por peca nesse lugar
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if matriz_jogo[i][j]=="!":
                if(len(verifica_perimetro(i,j))>0):
                    matriz_jogo[i][j] = " "
 
 #funcao para verificar se fez O
def verifica_bola():
    global matriz_jogo, pontos
    
    #Percorre a matriz por linha
    for i in range(1,TAMANHO_MATRIZ):
        
        #Verifica se na linha existe uma bola
        if "O" in matriz_jogo[i]:
            
            #Percorre as colunas
            for j in range(1, TAMANHO_AMBIENTE):
                
                #Verifica se na posição atual, à direita e em baixo existe uma bola
                if(matriz_jogo[i][j]=="O" and matriz_jogo[i+1][j]=="O" and matriz_jogo[i][j+1]=="O"):
                    
                    #Variaveis locais que irão ajudar (numa proxima coluna estas variaveis voltam a ficar a zero)
                    bolas_de_seguida=0
                    contador_horizontal=0
                    contador_vertical=0
                    seguinte=True
                    coordenadas_limpar=[]
                    
                    #Adiciona a coordenada atual 
                    coordenadas_limpar.append([i,j])
                    
                    #Verifica se nas proximas colunas quantos bolas de seguida existem
                    for proxima_coluna in range(j+1,TAMANHO_AMBIENTE):
                        if(matriz_jogo[i][proxima_coluna]=="O" and seguinte):
                            contador_horizontal+=1
                        else:
                            seguinte=False
                    
                    seguinte = True
                    
                    #Verifica se nas proximas linhas quantos bolas de seguida existem
                    for proxima_linha in range(i+1,TAMANHO_AMBIENTE):
                        if(matriz_jogo[proxima_linha][j]=="O" and seguinte):
                            contador_vertical+=1
                        else:
                            seguinte=False
                     
                    
                    #Se uma das variaveis é menor do que a outra
                    #faz sentido fazer a menor porque a maior já náo será possível
                          
                    if(contador_vertical<contador_horizontal):
                        bolas_de_seguida=contador_vertical
                    else:
                        bolas_de_seguida=contador_horizontal
                    
                    #Adiciona ao array para limpar as
                    #coordenadas que percorremos para baixo e 
                    #para a direita onde contêm uma bola
                    
                    for adicona_lixo in range(1,bolas_de_seguida+1):
                        coordenadas_limpar.append([i,j+adicona_lixo])
                        coordenadas_limpar.append([i+adicona_lixo,j])
                        
                    #Caso a tenha mais que uma bola de seguida para baixo e para a direita
                    while (bolas_de_seguida>1):
                        seguinte=True
                        
                        #Verifica se na ultima linha de uma possivel bola existe o resto das 
                        #bolas para formar a figura
                        
                        for linha_baixo in range(j+1,j+bolas_de_seguida+1):
                            if not (matriz_jogo[i+bolas_de_seguida][linha_baixo] == "O" and seguinte):
                                seguinte=False
                            else:
                                coordenadas_limpar.append([i+bolas_de_seguida,linha_baixo])
                        
                        #Caso a ultima linha nao seja tudo bola verifica 
                        #para uma vola menor diminuido a variavel
                        
                        if not seguinte:
                            bolas_de_seguida-=1
                            
                            
                            #Caso tenha passa para a a linha à direita
                            
                        else:
                            
                            #Verifica se na ultima linha de uma possivel bola existe o resto das 
                            #bolas para formar a figura
                            
                            for linha_direita in range(i+1, i+bolas_de_seguida+1):
                                if not (matriz_jogo[linha_direita][j+bolas_de_seguida] == "O" and seguinte):
                                    seguinte=False
                                else:
                                    coordenadas_limpar.append([linha_direita, j+bolas_de_seguida])
                                    
                            #Mesma coisa de cima 

                            if not seguinte:
                                bolas_de_seguida-=1
                                
                                #Caso verifique se que é uma bola adiciona
                                #os pontos e limpa as coordenadas e acaba a função

                            else:
                                limpa_pecas(coordenadas_limpar)
                                pontos += 2**(len(coordenadas_limpar))
                                ev3.speaker.say("I Did a Ball")
                                ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                                return 0
                    
                    #Caso seja a menor bola 2 por 2

                    if(bolas_de_seguida==1 and matriz_jogo[i+1][j+1]=="O"):
                        coordenadas_limpar.append([i+1,j+1])
                        limpa_pecas(coordenadas_limpar)
                        pontos += 2**(len(coordenadas_limpar))
                        ev3.speaker.say("I Did a Ball")
                        ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                        return 0

def verifica_x(linha, coluna):
    global matriz_jogo, pontos

    #Se houver um x na coluna à esquerda e linha de cima, E na linha de baixo e à direita,
    #E na linha de baixo e à esquerda, E na linha de cima e à direita 
    if (matriz_jogo[linha-1][coluna-1] == "X" and
        matriz_jogo[linha+1][coluna+1] == "X" and 
        matriz_jogo[linha+1][coluna-1] == "X" and 
        matriz_jogo[linha-1][coluna+1] == "X"):
        
        #Vai substituir essas posicoes de pecas e a do meio da figura por " " 
        matriz_jogo[linha-1][coluna-1] = " "
        matriz_jogo[linha+1][coluna+1] = " "
        matriz_jogo[linha+1][coluna-1] = " "
        matriz_jogo[linha-1][coluna+1] = " "
        matriz_jogo[linha][coluna] = " "
        
        #Vai dizer a figura que fez e os pontos dessa figura e adicionar esses pontos ao total de pontos
        ev3.speaker.say("Did a X")
        ev3.speaker.say(str(2**5))
        pontos += 2**5
        return True
    return False
 
 #coordenada para ver se tem um X no 3x3 dentro de 5x5
def coordenadas_perimentros_vezes(linha, coluna):
    global matriz_jogo

    #Lista onde de posicoes onde tem de ter x para fazer a figura
    coordenadas=[[linha+1,coluna+1],[linha+1, coluna-1], [linha-1, coluna+1], [linha-1, coluna-1]]

    #Lista auxiliar para guardar as coordenadas das pecas x que tem na matriz
    coordenadas_aux=[]

    #Vai percorrer a lista de coordenadas
    for i in range(len(coordenadas)):
        
        #coordenadas[i][0] pode ser linha+1 ou linha-1
        #coordenadas[i][1] pode ser coluna+1 ou coluna-1 
        #Assim se na matriz[linha+/-1][coluna+/-1] existe x, e essas posicoes estao dentro da matriz de jogo
        #adiciona à lista de coordenadas auxiliares
        if (matriz_jogo[coordenadas[i][0]][coordenadas[i][1]]=="X" and
            (coordenadas[i][0]>1 and coordenadas[i][0]<5) and
            (coordenadas[i][1]>1 and coordenadas[i][1]<5)):
            coordenadas_aux.append(coordenadas[i])
    
    return coordenadas_aux

 #coordenada para ver se tem + no 3x3 dentro do 5x5
def coordenadas_perimentros_mais(linha, coluna):
    global matriz_jogo

    #Variavel em que vamos adicionar as coordenadas
    coordenadas = []

    #Se houver + na linha de baixo da que ele recebeu e se essa linha esta na matriz de jogo, 
    #e se a coluna tambem esta na matriz
    #adiciona ao array de coordenadas essa peca + verificada
    if ((matriz_jogo[linha+1][coluna]=="+") and
        (linha+1 > 1 and linha+1 < TAMANHO_AMBIENTE-1) and
        (coluna>1 and coluna < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha+1, coluna])
        
    #Se houver + na linha de cima da que ele recebeu e se essa linha esta na matriz de jogo, 
    #e se a coluna tambem esta na matriz
    #adiciona ao array de coordenadas essa peca + verificada
    if ((matriz_jogo[linha-1][coluna]=="+") and
        (linha-1 > 1 and linha-1 < TAMANHO_AMBIENTE-1) and
        (coluna>1 and coluna < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha-1, coluna])
        
    #Se houver + na coluna da direita da que ele recebeu e se essa linha esta na matriz de jogo, 
    #e se a coluna tambem esta na matriz
    #adiciona ao array de coordenadas essa peca + verificada
    if ((matriz_jogo[linha][coluna+1]=="+") and
        (linha > 1 and linha < TAMANHO_AMBIENTE-1) and
        (coluna+1>1 and coluna+1 < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha, coluna+1])
        
    #Se houver + na coluna da esquerda da que ele recebeu e se essa linha esta na matriz de jogo, 
    #e se a coluna tambem esta na matriz
    #adiciona ao array de coordenadas essa peca + verificada
    if ((matriz_jogo[linha][coluna-1]=="+") and
        (linha> 1 and linha < TAMANHO_AMBIENTE-1) and
        (coluna-1 >1 and coluna-1 < TAMANHO_AMBIENTE-1)):
        coordenadas.append([linha, coluna-1])
    
    return coordenadas

def verifica_mais(linha, coluna):
    global matriz_jogo, pontos

    #Aqui verifica se tem um + em cima, em baixo, à direita e à esquerda do ultimo + que colocou
    if (matriz_jogo[linha-1][coluna] == "+" and
        matriz_jogo[linha+1][coluna] == "+" and 
        matriz_jogo[linha][coluna+1] == "+" and 
        matriz_jogo[linha][coluna-1] == "+"):
        
        #Se a condicao se se verificar vai mudar essas pecas para " " porque fez a figura
        matriz_jogo[linha-1][coluna] = " "
        matriz_jogo[linha+1][coluna] = " "
        matriz_jogo[linha][coluna+1] = " "
        matriz_jogo[linha][coluna-1] = " "
        matriz_jogo[linha][coluna] = " "
        
        #Diz que fez o mais e os pontos, e adiciona à variavel de pontos finais esses mesmos pontos que fez agora
        ev3.speaker.say("Did a plus")
        ev3.speaker.say(str(2**5))
        pontos += 2**5
        return True
    return False


#Funcao que sera chamada quando fizer uma figura, para retirar as pecas que formaram essa mesma figura          
def limpa_pecas(coordenadas_limpar):
    global matriz_jogo
    
    #Percorre as coordenadas onde tem as pecas da figura que formou para as retirar
    if(len(coordenadas_limpar)>0):
        for coodenada in coordenadas_limpar: 
            matriz_jogo[coodenada[0]][coodenada[1]] = " "

#Esta funcaoo vai percorrer o array da matriz de jogo e se tiver pecas no tabuleiro e no array
#de pecas vai fazer os calculos para retirar os pontos 
def retira_pontos():
    global pontos, matriz_jogo, pecas

    #Variavel para contar o numero de pecas
    contador = 0
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            
            #Se naquela coordenada houver algo diferente de " " e "!" que nao sao pecas vai adicionar ao contador
            if (matriz_jogo[i][j]!=" ") and matriz_jogo[i][j]!="!":
                contador += 1

    #Percorre o array de pecas que sobraram e adiciona ao contador
    for i in len(pecas):
        if pecas[i] != " ":
            contador += 1

    #Verifica se a variavel que conta as pecas e maior que zero
    if contador > 0:

        #Para o numero de pontos final nao ficar negativo, fica a zero 
        if(pontos - 2**contador<=0):
            pontos=0
        else:   
            pontos -= 2**contador

#Funcao que inicia o jogo, percorrendo as pecas do array e colocando-as na maatriz de jogo
def jogar():
    global matriz_jogo, pecas
    wait(5000)
    for i in range(len(pecas)):
        coloca_peca(pecas[i])
        
    ev3.speaker.say("I go hard in Salsa Jeans")
    


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
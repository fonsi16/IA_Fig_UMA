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

pecas_maximas=[]

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
matriz_jogo = []
matriz_heuristica = []
#Array das peças lidas no inicio do jogo

pecas = ['+', '+', '+', '+', '+',
         '-', '-', '*', '*', '*',
         '*', '*', '+', '+', '+',
         '*', '*', '*', '*', '0', 
         '0', '0', '+', '0', '0',
         '0', '0', '0', '-', '-',
         '-', '0']
pecas_antes_verificadas=[]

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

#VARIÁVEIS PARA A HEURÍSTICA DE 25 PEÇAS
#Variáveis para contagem das peças
pecas_bola = 0
pecas_menos = 0
pecas_mais = 0
pecas_x = 0

# Posições das peças da bola de 4 e 8
posicoes_bola4 = [(1,1),(1,2),(2,1),(2,2)]
posicoes_bola8 = [(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3)]

# Posições das peças  x
posicoes_x9 = [(5,1),(5,5),(4,2),(4,4),(1,1),(1,5),(2,2),(2,4),(3,3)]
posicoes_x5 = [(5,1),(5,3),(4,2),(3,1),(3,3)]

# Posições das peças +
posicoes_mais9 = [(1,3),(2,3),(3,1),(3,2),(3,4),(3,5),(5,3),(4,3),(3,3)]
posicoes_mais5 = [(5,4),(4,3),(4,4),(4,5),(3,4)]

# Posições das peças menos
posicoes_menos3 = [(2,5),(2,3),(2,4)]
posicoes_menos2 = [(2,5),(2,4)]

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

    #Vira para a direita 90 graus
    pernas.turn(-ANGULO_RODAR)

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
    #Vira para a esquerda 90 graus
    pernas.turn(0.75*ANGULO_RODAR)
 
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
    #Vira 180 graus
    pernas.turn(-1.75*ANGULO_RODAR)

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
    #Espera meio segundo
    wait(500)
    #Corre o motor a uma certa velocidade durante um período de tempo (Velocidade, Tempo)
    garra.run_time(200, 2000)
    #Indica que agarrou uma peça
    ev3.speaker.say("Light weight")
    #Para o motor
    garra.stop() 

#Abre a garra do robô de modo a largar uma peça
def larga_objeto():
    #Espera meio segundo
    wait(500)
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
        pecas.append("*")
        ev3.speaker.say("Red")
        
    elif cor_detectada == 'Amarelo':
        pecas.append("0")
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

#Verifica se todos os espaços à volta de um sítio do tabuleiro são vazios
def verifica_perimetro(linha, coluna):
    global matriz_jogo
    coordenadas=[]
    #Verifica os 4 espaços á volta
    if matriz.verifica_vazio(matriz_jogo,linha+1,coluna):
        coordenadas.append([linha+1,coluna])
    if matriz.verifica_vazio(matriz_jogo,linha,coluna+1):
        coordenadas.append([linha,coluna+1])
    if matriz.verifica_vazio(matriz_jogo,linha-1,coluna):
        coordenadas.append([linha-1,coluna])
    if matriz.verifica_vazio(matriz_jogo,linha,coluna-1):
        coordenadas.append([linha,coluna-1])
    #Retorna um array de coordenadas dos espaços vazios á volta do sítio
    return coordenadas
    
#Muda o sentido do robô dependendo do que recebe como argumento
def muda_sentido(sentido):
    global sentido_robo
    
    #Verifica o sentido para que quer mudar
    if(sentido == SUL):
        #Verifica o sentido do robô e vira respetivamente
        if(sentido_robo == NORTE):
            gira()
        elif(sentido_robo == ESTE):
            vira_direita()
        elif(sentido_robo == OESTE):
            vira_esquerda()
    
    elif(sentido == NORTE):
        #Verifica o sentido do robô e vira respetivamente
        if(sentido_robo == SUL):
            gira()
        elif(sentido_robo == OESTE):
            vira_direita()
        elif(sentido_robo == ESTE):
            vira_esquerda()
    
    elif(sentido == OESTE):
        #Verifica o sentido do robô e vira respetivamente
        if(sentido_robo == ESTE):
            gira()
        elif(sentido_robo == SUL):
            vira_direita()
        elif(sentido_robo == NORTE):
            vira_esquerda()
            
    elif(sentido == ESTE):
        #Verifica o sentido do robô e vira respetivamente
        if(sentido_robo == OESTE):
            gira()
        elif(sentido_robo == NORTE):
            vira_direita()
        elif(sentido_robo == SUL):
            vira_esquerda()
    
    #Muda o sentido do robô para o que acabou de mudar
    sentido_robo = sentido

#Funcao que orienta o robo no sentido correto, quando se esta a mover
#Recebendo a linha e coluna que esta agora, e a proxima linha e coluna
def movimento(linha_atual, coluna_atual, proxima_linha, proxima_coluna):

    #Se o proximo movimento do robô é ir para baixo ele vai virar para sul
    if (proxima_linha>linha_atual):
        muda_sentido(SUL)
        anda_frente()

    #Se o proximo movimento do robô é ir para cima ele vai virar para norte
    elif(proxima_linha<linha_atual):
        muda_sentido(NORTE)
        anda_frente()

    #Se o proximo movimento do robô é ir para direita ele vai virar para este
    elif(proxima_coluna>coluna_atual):
        muda_sentido(ESTE)
        anda_frente()

    #Se o proximo movimento do robô é ir para esquerda ele vai virar para oeste
    elif(proxima_coluna<coluna_atual):
        muda_sentido(OESTE)
        anda_frente()

#Volta para base percorrendo a rota/caminho
def voltar (caminho, linhas):
    
    # Percorre a rota/caminho assim indo da sua posição onde meteu a peça até à base
    for i in range(len(caminho)-1):
        movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
    
    # Se o robo foi por linhas, sai da linha e depois muda o sentido
    if linhas:
        pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.5)
        muda_sentido(SUL)
    else:
        muda_sentido(SUL)

#Funcao que devolve a melhor (primeira possível) rota/caminho para chegar a uma posição na matriz
def melhor_rota(linha, coluna, caminho, nao_ir, contador):
    """Retorna um array com as coordenadas a partir da célula mais próxima à coordenada onde o robô deseja colocar a peça.
    Esta é uma função recursiva, ou seja, será sempre chamada até alcançar a coordenada base do robô (6 por 6) ou se não conseguir retorna um array vazio.    

    Args:
        linha (int): Linha da posição onde vai meter a peça na matriz
        coluna (int): coluna da posição onde vai meter a peça na matriz
        caminho (array): Array com as coordenadas que o robô irá percorrer (que será preenchido nesta função)
        nao_ir (array): Array com as casas em que o robô não pode ir, pois são becos sem saída ou coordenadas já percorridas.
        contador (int): Contador que, ao chegar na primeira coordenada (da peça), incrementa se o número for igual às casas vazias ao redor, indicando que o robô não consegue chegar lá.

    Returns:
        caminho (array): array com as coordenadas até a casa do robô.
            Exemplo: Se a peça será colocada na coordenada [1,1]:
                caminho --> [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6]]
    """

    # Caso a linha e a coluna seja igual ao tamanho ambiente(onde o robo se encontra) quer dizer que achamos uma rota/caminho para chegar à peça 
    if (linha == TAMANHO_AMBIENTE) and (coluna == TAMANHO_AMBIENTE):
        return caminho
        """ Exemplo:
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   | # |
        """
    
    # Caso esteja nas bordas horizontais e numa coluna antes da última
    elif (linha == 0 and coluna < TAMANHO_AMBIENTE) or (linha == TAMANHO_AMBIENTE and coluna < TAMANHO_AMBIENTE) :
        # Irá adicionar ao caminha a coordena com linha igual à atual e proxima coluna ou seja aquela que está à direita
        caminho.append([linha, coluna+1])
        # Chama a recursiva e verifica se chegou ou não à posição do robo
        return melhor_rota(linha, coluna+1, caminho, nao_ir, contador)
        """ Exemplo:
            | # | # | # | # | # | # |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            |   |   |   |   |   |   |   |
            | # | # | # | # | # | # |   |
        """
    
    # Caso esteja nas bordas verticais e numa coluna antes da última
    elif (linha < TAMANHO_AMBIENTE and coluna == TAMANHO_AMBIENTE) or (coluna == 0 and (linha > 0 and linha < TAMANHO_AMBIENTE)) :
        # Irá adicionar ao caminha a coordena com coluna igual à atual e proxima linha ou seja aquela que está a baixo
        caminho.append([linha+1, coluna])
        # Chama a recursiva e verifica se chegou ou não à posição do robo
        return melhor_rota(linha+1, coluna, caminho , nao_ir, contador)
    
        """ Exemplo:
            |   |   |   |   |   |   | # |
            | # |   |   |   |   |   | # |
            | # |   |   |   |   |   | # |
            | # |   |   |   |   |   | # |
            | # |   |   |   |   |   | # |
            | # |   |   |   |   |   | # |
            |   |   |   |   |   |   |   |
        """
    
    # Caso a linha e a coluna não se encontre numa borda
    else:
        # Verifica se não existe coordenadas no caminho e se a coluna e a linha são as coordenadas da peça
        if (len(caminho)==0 and [linha, coluna] in nao_ir):
            contador+=1
            # Caso o contador seja igual aos espaços vazios que existem no perimetro da peça quer dizer que ele ja percorreu os espaços possíveis
            if(contador==len(verifica_perimetro(nao_ir[0][0],nao_ir[0][1]))):
                # O robo não consegue chegar lá então o caminho é vazio
                return []
        
        # Na primeira vez ele irá adicionar a coordenada da peça no array
        # Caso a coordena já exista no array não é necessário voltar a inseri-la 
        if [linha, coluna] not in nao_ir:
            nao_ir.append([linha, coluna])
            
        # Criamos um array coordenadas que irá receber as coordenadas em cruz onde existem espaços vazios
        coordenadas = verifica_perimetro(linha,coluna)
        
        # Caso hajam coordenadas vazias à volta da peça
        if coordenadas != []:
            # Iremos percorrer as coordenadas
            for i in range(len(coordenadas)):
                # Caso a coordena não esteja no array nao_ir
                if(coordenadas[i] not in nao_ir):
                    # Irá adcionar a coordenada ao caminho
                    caminho.append([coordenadas[i][0], coordenadas[i][1]])
                    # Irá chamar a recursiva para verificar a coordenada que adicionou ao caminho
                    return melhor_rota(coordenadas[i][0], coordenadas[i][1],
                                caminho, nao_ir, contador)
            
            # Caso tenha percorrido todas as coordenadas e nao tenha chamado a recursiva, ou seja entrou num beco sem saida
            # Elimina a ultima posição do array caminho
            caminho.pop()
            
            # Verifica se tem coordenadas no array caminho
            if(len(caminho)>0):
                # Chama a recursiva na ultima poscição do array caminho para verificar se ainda consegue chegar a uma borda
                return melhor_rota(caminho[-1][0], caminho[-1][1],
                                    caminho, nao_ir, contador)
            
            # Caso tenha voltado ao início
            else:
                # Chama a recursiva na poscição da peça para verificar se ainda consegue chegar a uma borda
                return melhor_rota(nao_ir[0][0], nao_ir[0][1],
                                    caminho, nao_ir, contador)
        
        # Caso não hajam coordenadas vazias à volta da peça
        else:
            return []

#Robô desloca-se para uma posição no tabuleiro (para meter a peça)
def posicionar(linha, coluna): 
    global robo_x, robo_y, matriz_jogo
    # Descobre a melhor rota/caminho do sítio no tabuleiro até a localização do robô
    caminho = melhor_rota(linha, coluna, [], [], 0)
    # Se existe uma rota/caminho possível
    if(caminho!=[]):
        # Reverte a rota/caminho
        caminho.reverse()

        # Percorre a rota/caminho reversa assim indo da sua posição até ao sítio pretendido
        for i in range(len(caminho)-1):
            movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
                
        # Se o robô não está de frente para o sítio onde vai meter a peça, muda o seu sentido
        if (linha>robo_y):
            muda_sentido(SUL)
        elif(linha<robo_y):
            muda_sentido(NORTE)
        elif(coluna>robo_x):
            muda_sentido(ESTE)
        elif(coluna<robo_x):
            muda_sentido(OESTE)
            
        # Reverte a rota/caminho denovo assim voltando ao normal
        caminho.reverse()
        # Retorna a rota/caminho
        return caminho, False
    # Caso não exista uma rota/caminho possível irá pelas linhas do tabuleiro
    else:
        # Cria um array caminho que irá receber as coordenadas que o robô irá percorrer
        # Percorre as colunas do tabuleiro até a anterior à coluna onde vai meter a peça
        for i in range(TAMANHO_AMBIENTE-coluna):
            caminho.append([TAMANHO_AMBIENTE, TAMANHO_AMBIENTE-i])
        # Percorre as linhas do tabuleiro até à linha onde vai meter a peça
        for i in range (TAMANHO_AMBIENTE-linha):
            caminho.append([TAMANHO_AMBIENTE-i-1, coluna+1])

        # Percorre a rota/caminho assim indo da sua posição até ao sítio pretendido
        for i in range(len(caminho)-1):
            movimento(caminho[i][0], caminho[i][1], caminho[i+1][0], caminho[i+1][1])
            # Depois de percorrer o tabuleiro até á coluna antes da de onde vai meter a peça anda meio quadrado para a frente de modo a se posicionar na linha
            if (i == TAMANHO_AMBIENTE - coluna - 2):
                pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.5)
            
        # Muda o seu sentido para o sítio onde vai meter a peça
        muda_sentido(OESTE)
        # Anda meio quadrado para a frente de modo a se posicionar na posição para meter a peça
        pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.5)
        # Larga a peça
        larga_objeto()
        # Anda meio quadrado para trás de modo a se posicionar na posição inicial
        pernas.straight(-DISTANCIA_ENTRE_QUADRADOS*0.5)

        # Reverte a rota/caminho denovo assim ficando da posição ate a localização do robô
        caminho.reverse()
        # Retorna a rota/caminho
        return caminho, True

# Função para limpar as peças nas coordenadas especificadas
def limpa_pecas(coordenadas_limpar):
    global matriz_jogo
    
    # Verifica se há coordenadas para limpar
    if len(coordenadas_limpar) > 0:
        # Percorre as coordenadas e limpa as peças na matriz de jogo
        for i in range(len(coordenadas_limpar)):
            matriz_jogo[coordenadas_limpar[i][0]][coordenadas_limpar[i][1]] = " "   

# Função para verificar o número de peças dessa peca que tem na matriz de jogo
def numero_pecas(peca):
    global matriz_jogo

    # Variável para contar quantas peças existem
    contador = 0
    for i in range(len(matriz_jogo)):
        for j in range(len(matriz_jogo[i])):
            if matriz_jogo[i][j] == peca:
                # Aumenta o contador
                contador += 1
    # Retorna o contador
    return contador

# Funcao para verificar se fez a figura da bola
def verifica_bola():
    global matriz_jogo, pontos
    
    # Percorre a matriz por linha
    for i in range(1, TAMANHO_MATRIZ):
        
        # Verifica se na linha existe uma bola
        if "0" in matriz_jogo[i]:
            
            # Percorre as colunas
            for j in range(1, TAMANHO_AMBIENTE):
                
                # Verifica se na posição atual, à direita e em baixo existe uma bola
                if (matriz_jogo[i][j] == "0" and matriz_jogo[i+1][j] == "0" and matriz_jogo[i][j+1] == "0"):
                    
                    # Variaveis locais que irão ajudar (numa proxima coluna estas variaveis voltam a ficar a zero)
                    bolas_de_seguida = 0
                    contador_horizontal = 0
                    contador_vertical = 0
                    seguinte = True
                    # Array para guardar as coordenadas que irá limpar
                    coordenadas_limpar = []
                    
                    # Adiciona a coordenada atual no array para limpar
                    coordenadas_limpar.append([i, j])
                    
                    # Verifica se nas proximas colunas quantos bolas de seguida existem
                    for proxima_coluna in range(j+1, TAMANHO_AMBIENTE):
                        if (matriz_jogo[i][proxima_coluna] == "0" and seguinte):
                            contador_horizontal += 1
                        else:
                            seguinte = False
                    
                    seguinte = True
                    
                    # Verifica se nas proximas linhas quantas bolas de seguida existem
                    for proxima_linha in range(i+1, TAMANHO_AMBIENTE):
                        if (matriz_jogo[proxima_linha][j] == "0" and seguinte):
                            contador_vertical += 1
                        else:
                            seguinte = False
                     
                    
                    # Se uma das variaveis é menor do que a outra faz sentido fazer a menor porque a maior já náo será possível
                            
                    """ Exemplo:
                        |   |   |   |   |   |   |   |
                        |   | 0 | 0 | 0 | 0 | 0 |   |
                        |   | 0 |   |   |   |   |   |
                        |   | 0 |   |   |   |   |   |
                        |   |   |   |   |   |   |   |
                        |   |   |   |   |   |   |   |
                        |   |   |   |   |   |   |   |
                        Fazemos para a variavel vertical pois é a menor só sera possivel fazer no maximo uma bola de 8 peças
                    """

                    # Comparação entre as variaveis  
                    if (contador_vertical < contador_horizontal):
                        bolas_de_seguida = contador_vertical
                    else:
                        bolas_de_seguida = contador_horizontal
                    
                    # Adiciona ao array para limpar as coordenadas que percorremos para baixo e para a direita onde contêm uma bola
                    for adicona_lixo in range(1, bolas_de_seguida+1):
                        coordenadas_limpar.append([i, j+adicona_lixo])
                        coordenadas_limpar.append([i+adicona_lixo, j])
                        
                    # Caso a tenha mais que uma bola de seguida para baixo e para a direita
                    while (bolas_de_seguida > 1):
                        seguinte = True
                        
                        # Verifica se na ultima linha de uma possivel bola existe o resto das bolas para formar a figura
                        for linha_baixo in range(j+1, j+bolas_de_seguida+1):
                            if not (matriz_jogo[i+bolas_de_seguida][linha_baixo] == "0" and seguinte):
                                seguinte = False
                            else:
                                coordenadas_limpar.append([i+bolas_de_seguida, linha_baixo])
                        
                        # Caso a ultima linha nao seja tudo bola verifica para uma bola menor diminuido a variavel
                        if not seguinte:
                            bolas_de_seguida -= 1   
                            
                        # Caso tenha passa para a a linha à direita
                        else:
                            
                            # Verifica se na ultima linha de uma possivel bola existe o resto das bolas para formar a figura
                            for linha_direita in range(i+1, i+bolas_de_seguida+1):
                                if not (matriz_jogo[linha_direita][j+bolas_de_seguida] == "0" and seguinte):
                                    seguinte = False
                                else:
                                    coordenadas_limpar.append([linha_direita, j+bolas_de_seguida])
                                    
                            # Caso a ultima linha nao seja tudo bola verifica para uma bola menor diminuido a variavel
                            if not seguinte:
                                bolas_de_seguida -= 1

                            # Caso verifique se que é uma bola adiciona os pontos e limpa as coordenadas e acaba a função
                            else:
                                limpa_pecas(coordenadas_limpar)
                                ev3.speaker.say("I Did a Ball")
                                ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                                return 0
                    
                    # Caso seja a menor bola 2 por 2
                    if (bolas_de_seguida == 1 and matriz_jogo[i+1][j+1] == "0"):
                        coordenadas_limpar.append([i+1, j+1])
                        limpa_pecas(coordenadas_limpar)
                        ev3.speaker.say("I Did a Ball")
                        ev3.speaker.say(str(2**(len(coordenadas_limpar))))
                        return 0

# Funcao para verificar se fez a figura do x
def verifica_x(linha, coluna):
    global matriz_jogo, pontos

    # Verifica se tem um x em cima, em baixo, à direita e à esquerda obliquamente ao ultimo x que colocou
    if (matriz_jogo[linha-1][coluna-1] == "*" and
        matriz_jogo[linha+1][coluna+1] == "*" and 
        matriz_jogo[linha+1][coluna-1] == "*" and 
        matriz_jogo[linha-1][coluna+1] == "*"):
        
        # Se a condição for verdadeira, as peças são alteradas para " " porque a figura foi formada
        matriz_jogo[linha-1][coluna-1] = " "
        matriz_jogo[linha+1][coluna+1] = " "
        matriz_jogo[linha+1][coluna-1] = " "
        matriz_jogo[linha-1][coluna+1] = " "
        matriz_jogo[linha][coluna] = " "
        
        # Informa que a figura de "*" foi formada e exibe a pontuação correspondente
        ev3.speaker.say("Did a X")
        ev3.speaker.say(str(2**5))
        return True
    
    return False
 
 #coordenada para ver se tem um X no 3x3 dentro de 5x5

# Função para obter as coordenadas das peças "*" que estão ao redor de uma determinada posição
def coordenadas_perimetros_vezes(linha, coluna):
    global matriz_jogo

    # Lista de posições onde devem ter "x" para formar a figura
    coordenadas = [[linha+1, coluna+1], [linha+1, coluna-1], [linha-1, coluna+1], [linha-1, coluna-1]]

    # Lista auxiliar para guardar as coordenadas das peças "x" presentes na matriz
    coordenadas_aux = []

    # Percorre a lista de coordenadas
    for i in range(len(coordenadas)):
        
        # Verifica se a posição contém uma peça "*" e se está dentro dos limites da matriz de jogo
        if (matriz_jogo[coordenadas[i][0]][coordenadas[i][1]] == "*" and
            (coordenadas[i][0] > 1 and coordenadas[i][0] < 5) and
            (coordenadas[i][1] > 1 and coordenadas[i][1] < 5)):
            # Adiciona as coordenadas à lista auxiliar
            coordenadas_aux.append(coordenadas[i])
    
    # Retorna a lista de coordenadas
    return coordenadas_aux

# Função para obter as coordenadas das peças "+" que estão ao redor de uma determinada posição
def coordenadas_perimetros_mais(linha, coluna):
    global matriz_jogo

    # Lista de posições onde devem ter "+" para formar a figura
    coordenadas = [[linha+1, coluna], [linha-1, coluna], [linha, coluna-1], [linha, coluna+1]]
    
    # Lista auxiliar para armazenar as coordenadas das peças "+" presentes na matriz
    coordenadas_aux = []  

    # Percorre a lista de coordenadas
    for i in range(len(coordenadas)):
        # Verifica se a posição contém uma peça "+" e se está dentro dos limites da matriz de jogo
        if (matriz_jogo[coordenadas[i][0]][coordenadas[i][1]] == "+" and
            (coordenadas[i][0] > 1 and coordenadas[i][0] < 5) and
            (coordenadas[i][1] > 1 and coordenadas[i][1] < 5)):
            # Adiciona as coordenadas à lista auxiliar
            coordenadas_aux.append(coordenadas[i])  
    
    # Retorna a lista de coordenadas
    return coordenadas_aux  

# Funcao para verificar se fez a figura do +
def verifica_mais(linha, coluna):
    global matriz_jogo, pontos

    # Verifica se há um "+" acima, abaixo, à direita e à esquerda da última posição onde foi colocado um "+"
    if (matriz_jogo[linha-1][coluna] == "+" and
        matriz_jogo[linha+1][coluna] == "+" and 
        matriz_jogo[linha][coluna+1] == "+" and 
        matriz_jogo[linha][coluna-1] == "+"):
        
        # Se a condição for verdadeira, as peças são alteradas para " " porque a figura foi formada
        matriz_jogo[linha-1][coluna] = " "
        matriz_jogo[linha+1][coluna] = " "
        matriz_jogo[linha][coluna+1] = " "
        matriz_jogo[linha][coluna-1] = " "
        matriz_jogo[linha][coluna] = " "
        
        # Informa que a figura de "+" foi formada e exibe a pontuação correspondente
        ev3.speaker.say("Did a plus")
        ev3.speaker.say(str(2**5))
        return True
    return False

# Função chamada quando ele coloca uma peça na matriz de jogo
def verifica_peca(peca, linha, coluna):
    global pontos, matriz_jogo

    # Lista de coordenadas para limpar
    coordenadas_limpar=[]
    # Variável para contar quantas peças seguidas existem
    contador=0
    seguida=True
    
    # Verifica se a peça é um "-"
    if peca == "-":
        contador_auxiliar = 0 
        
        # Percorre a linha do último "-" metido
        for i in range(len(matriz_jogo[linha])):
            # Caso seja um "-" e esteja seguida, incrementa o contador
            if(matriz_jogo[linha][i]=="-" and seguida):
                contador_auxiliar += 1
                coordenadas_limpar.append([linha,i])
                if contador_auxiliar>contador:
                    contador=contador_auxiliar
            # Caso seja um "-" mas não esteja seguida, começa a contar os de seguida de novo
            elif(matriz_jogo[linha][i]=="-" and not seguida):
                seguida=True
                contador_auxiliar += 1
                coordenadas_limpar = []
                coordenadas_limpar.append([linha,i])
            # Caso não seja um "-", não está seguida e reseta o contador
            else:
                seguida = False
                contador_auxiliar = 0
        
        # Caso tenha mais que 1 "-" seguido, limpa as peças e acaba a função
        if(contador>1):
            limpa_pecas(coordenadas_limpar)
      
    # Verifica se a peça é um "+"
    if peca == "+":
        # Verifica se fez a figura do "+" máxima (de 9 peças) que so tem um lugar possivel
        if (numero_pecas(peca)>=(TAMANHO_MATRIZ*2-1) and (coluna==TAMANHO_AMBIENTE//2 or linha == TAMANHO_AMBIENTE//2)):
            for i in range(1,TAMANHO_AMBIENTE):
                # Se é seguida
                if(seguida):
                    # Verifica se está na linha e na coluna do meio, senao nao é possivel
                    if not (matriz_jogo[TAMANHO_AMBIENTE//2][i] == "+" and matriz_jogo[i][TAMANHO_AMBIENTE//2] == "+"):
                        seguida = False
            # Se depois de verificar se é seguida continua a ser seguida quer dizer que fez figura máxima e limpa as peças
            if seguida:
                for i in range(1,TAMANHO_AMBIENTE):
                    matriz_jogo[TAMANHO_AMBIENTE//2][i] = " "
                    matriz_jogo[i][TAMANHO_AMBIENTE//2] = " "

        # Como não é a figura máxima, verifica se fez a figura do "+" pequena (de 5 peças)
        # Se meteu em algum dos cantos, não é possivel fazer a figura
        if((linha==1 and coluna==1) or
            (linha==1 and coluna==TAMANHO_AMBIENTE-1) or
            (linha==TAMANHO_AMBIENTE-1 and coluna== 1) or
            (linha==TAMANHO_AMBIENTE-1 and coluna==TAMANHO_AMBIENTE-1)):
            return 0

        # Se não meteu em nenhum dos cantos
        else:
            # Obtem todas as coordenadas onde pode fazer a figura do "+" a volta do que meteu
            coordenadas=coordenadas_perimetros_mais(linha, coluna)
            # Se o "+" que meteu não está a fazer a figura do "+", isto é, não é o meio da figura
            if not verifica_mais(linha, coluna):
                # Percorre as coordenadas dos ao redor
                for i in range(len(coordenadas)):
                    # Verifica se alguma dessas coordenadas faz a figura do "+"
                    if verifica_mais(coordenadas[i][0], coordenadas[i][1]):
                        break 
    
    # Verifica se a peça é um "*"
    if peca == "*":
        # Verifica se fez a figura do "*" máxima (de 9 peças) que so tem um lugar possivel
        if (numero_pecas(peca)>=(TAMANHO_MATRIZ*2-1) and (linha>=2 and linha<=4) and (coluna>=2 and coluna<=4) ):
            for i in range(1,TAMANHO_AMBIENTE):
                # Se é seguida
                if seguida:
                    # Verifica se está nas posições da peça máxima, senao nao é possivel
                    if not (matriz_jogo[i][i]=="*" and matriz_jogo[i][TAMANHO_AMBIENTE-i]=="*"):
                        seguida = False
            
            # Se depois de verificar se é seguida continua a ser seguida quer dizer que fez figura máxima e limpa as peças
            if seguida:
                for i in range(1,TAMANHO_AMBIENTE):
                    matriz_jogo[i][i] = " "
                    matriz_jogo[i][TAMANHO_AMBIENTE-i] = " "
        
        # Como não é a figura máxima, verifica se fez a figura do "*" pequena (de 5 peças)
        # Obtem todas as coordenadas onde pode fazer a figura do "*" a volta do que meteu            
        coordenadas=coordenadas_perimetros_vezes(linha, coluna)
        # Se o "*" que meteu não está a fazer a figura do "*", isto é, não é o meio da figura
        if not verifica_x(linha, coluna):
            # Percorre as coordenadas dos ao redor
            for i in range(len(coordenadas)):
                # Verifica se alguma dessas coordenadas faz a figura do "*"
                if verifica_x(coordenadas[i][0], coordenadas[i][1]):
                    break 

    # Verifica se a peça é um "0"/bola
    if peca == "0":
        # Verifica se fez a figura da bola máxima (de 16 peças) que so tem um lugar possivel
        if (numero_pecas(peca)>=((TAMANHO_MATRIZ*TAMANHO_MATRIZ) - ((TAMANHO_MATRIZ-2)*(TAMANHO_MATRIZ-2))) and (linha==1 or linha==TAMANHO_MATRIZ) and (coluna==1 or coluna==TAMANHO_MATRIZ) ):
            for i in range(1,TAMANHO_AMBIENTE):
                # Verifica a primeira e ultima linhas e colunas
                if not (matriz_jogo[1][i] == "0" and
                        matriz_jogo[TAMANHO_MATRIZ][i] == "0" and
                        matriz_jogo[i][1] == "0" and
                        matriz_jogo[i][TAMANHO_MATRIZ] == "0"):
                    # Caso haja uma peca diferente de "0" acaba a verificação
                    seguida=False
                    break

            # Se depois de verificar se é seguida continua a ser seguida quer dizer que fez figura máxima e limpa as peças  
            if seguida:
                for i in range(1,TAMANHO_AMBIENTE):
                    matriz_jogo[1][i] = " "
                    matriz_jogo[TAMANHO_MATRIZ][i]= " "
                    matriz_jogo[i][1]= " "
                    matriz_jogo[i][TAMANHO_MATRIZ]= " "
                
        # Como não é a figura máxima, verifica se fez as figuras das bolas pequenas (de 12/8/4 peças)
        else: 
            verifica_bola()

#Funcao para colocar a peca que recebeu na matriz de jogo
def coloca_peca(peca, x, y):

    global matriz_jogo

    #Recebe a coordenada onde pode colocar a peca
    coordenada = [x, y]
    
    #Se recebeu uma coordenada
    if coordenada is not None:

        #Adiciona às variaveis os valores dessa coordenada 
        x = coordenada[0]
        y = coordenada[1]
        
        #Vai agarrar na proxima peca
        agarra_objeto()
        
        #Variavel que guarda as coordenadas/array necessarias para voltar e se foi por linhas meter a peça
        volta, linhas = posicionar(x,y)
        
        #Se consegue por a peca nesse lugar vai colocar a peca e voltar para a casa inicial
        #Verificar se fez uma figura depois de colocar essa peca
         
        # Se foi por linhas
        # Se o linhas é verdadeiro, significa que teve que ir pelas linhas para meter a peça pois a peça nao tinha um caminho possivel
        if linhas:
            matriz.inserir_objeto_matriz(peca,x,y,matriz_jogo)
            #Voltar para a casa inicial
            voltar(volta, linhas)
            #Verificar se fez uma figura depois de colocar essa peca
            verifica_peca(peca,x,y)
            matriz.imprime_matriz(matriz_jogo)
        # Se foi por caminho normal
        else:
            #Pequenos ajustes para meter a peca
            pernas.straight(DISTANCIA_ENTRE_QUADRADOS*0.75)
            larga_objeto()
            pernas.straight(-DISTANCIA_ENTRE_QUADRADOS*0.75)
            matriz.inserir_objeto_matriz(peca,x,y,matriz_jogo)
            matriz.imprime_matriz(matriz_jogo)
            #Voltar para a casa inicial
            voltar(volta, linhas)
            #Verificar se fez uma figura depois de colocar essa peca
            verifica_peca(peca,x,y)
            matriz.imprime_matriz(matriz_jogo)

# Função para procurar uma coordenada vazia na matriz de jogo
def procura_coordenada_vazia():
    global matriz_jogo
    coordenadas=[]
    # Percorre a matriz de jogo
    for i in range(1,TAMANHO_AMBIENTE-1):
        for j in range(1,TAMANHO_AMBIENTE-1):
            # Se encontrar uma coordenada vazia adiciona ao array coordenadas
            if matriz_jogo[i][j]==" ":
                coordenadas=[i,j]
                return coordenadas

# Função para procurar uma coordenada na matriz de heuristica que corresponda à peça da figura especificada
def procura_coordenada(peca_fig):
    global matriz_heuristica, matriz_jogo

    for i in range(TAMANHO_MATRIZ):
        for j in range(TAMANHO_MATRIZ):
            # Verifica se a posição na matriz heurística não está vazia, se a peça da figura corresponde ao primeiro elemento da lista na matriz heurística e se a posição correspondente na matriz de jogo está vazia
            if matriz_heuristica[i][j] != [] and peca_fig == matriz_heuristica[i][j][0] and matriz_jogo[i+1][j+1] == " ":
                # Remove a peça da figura da lista na matriz heurística
                matriz_heuristica[i][j].pop(0)  
                # Coordenadas da posição vazia na matriz de jogo
                coordenadas = [i+1, j+1]  
                return coordenadas

# Função para procurar uma coordenada na matriz de heuristica que corresponda à peça da figura especificada, que neste caso é ou um x ou um +
def procura_coordenada_mais_e_vezes(peca_fig, conta):
    global matriz_heuristica, matriz_jogo

    for i in range(TAMANHO_MATRIZ):
        for j in range(TAMANHO_MATRIZ):
            # Se for uma peça grande e for meter uma peça no meio tem de meter todas as outras peças primeiro
            if i == 2 and j == 2 and conta != 9 and peca_fig[0] == 9:
                continue
            # Verifica se a posição na matriz heurística não está vazia, se a peça da figura corresponde ao primeiro elemento da lista na matriz heurística e se a posição correspondente na matriz de jogo está vazia
            if matriz_heuristica[i][j] != [] and peca_fig == matriz_heuristica[i][j][0] and matriz_jogo[i+1][j+1] == " ":
                # Remove a peça da figura da lista na matriz heurística
                matriz_heuristica[i][j].pop(0)
                # Coordenadas da posição vazia na matriz de jogo
                coordenadas = [i+1, j+1]
                return coordenadas

# Função para procurar uma coordenada na matriz de heuristica que corresponda à peça da figura especificada, que neste caso é um -
def procura_coordenada_menos(peca_fig, conta, tamanho):
    global matriz_heuristica, matriz_jogo
    coordenadas=[]
    # Se for um menos de 2 peças
    if conta%2!=0 or tamanho==2:
        for i in range(TAMANHO_MATRIZ):
            for j in range(TAMANHO_MATRIZ):
                # Verifica se a posição na matriz heurística não está vazia, se a peça da figura corresponde ao primeiro elemento da lista na matriz heurística e se a posição correspondente na matriz de jogo está vazia
                if matriz_heuristica[i][j]!=[] and peca_fig==matriz_heuristica[i][j][0] and matriz_jogo[i+1][j+1]==" ":
                    # Remove a peça da figura da lista na matriz heurística
                    matriz_heuristica[i][j].pop(0)
                    # Coordenadas da posição vazia na matriz de jogo
                    coordenadas=[i+1,j+1]
                    return coordenadas
    # Se for um menos de 3 peças
    else:
        contador=0
        for i in range(TAMANHO_MATRIZ):
            for j in range(TAMANHO_MATRIZ):
                # Verifica se a posição na matriz heurística não está vazia, se a peça da figura corresponde ao primeiro elemento da lista na matriz heurística e se a posição correspondente na matriz de jogo está vazia
                if matriz_heuristica[i][j]!=[] and peca_fig==matriz_heuristica[i][j][0] and matriz_jogo[i+1][j+1]==" ":
                    # Usa o contador de modo a não fazer um menos de 2 peças
                    if contador==1:    
                        # Remove a peça da figura da lista na matriz heurística
                        matriz_heuristica[i][j].pop(0)
                        # Coordenadas da posição vazia na matriz de jogo
                        coordenadas=[i+1,j+1]
                        return coordenadas
                    else:
                        contador+=1

# Função para remover figuras inteiras, isto é, todas as peças de uma figura do array inicial de peças
def remove_figuras(peca, quantidade):
    global pecas
    contador = 0
    i = 0
    # Enquanto o contador não for igual à quantidade de peças da figura e o i não for maior que o tamanho do array de peças
    while contador < quantidade and i < len(pecas):
        # Se a peça for igual à peça da figura, remove a peça do array de peças e incrementa o contador
        if pecas[i] == peca:
            pecas.pop(i)
            contador += 1
        else:
            i += 1

def maior_figura_possivel(limite, maximo_fig, maximo):
    global pecas
    total_bolas=0
    total_mais=0
    total_vezes=0
    total_menos=0
    for i in range(limite):
        if pecas[i]=="0" and maximo!="0":
            total_bolas+=1
            if(total_bolas in maximo_fig[0]):
                return [total_bolas,"0"]
        elif pecas[i]=="*" and maximo!="*":
            total_vezes+=1
            if(total_vezes in maximo_fig[2]):
                return [total_vezes,"*"]
        elif pecas[i]=="+" and maximo!="+":
            total_mais+=1
            if(total_mais in maximo_fig[1]):
                return [total_mais,"+"]
        elif pecas[i]=="-" and maximo!="-":
            total_menos+=1
            if(total_menos in maximo_fig[3]):
                return [total_menos,"-"]

def maior_figura(limite, maximo_fig):
    global pecas
    total_bolas=0
    total_mais=0
    total_vezes=0
    total_menos=0
    i=0
    for i in range(limite):
        if pecas[i]=="0":
            total_bolas+=1
            if(total_bolas in maximo_fig[0]):
                maximo_fig[0].remove(total_bolas)
                return [total_bolas,"0"]
        elif pecas[i]=="*":
            total_vezes+=1
            if(total_vezes in maximo_fig[2]):
                maximo_fig[2].remove(total_vezes)
                return [total_vezes,"*"]
        elif pecas[i]=="+":
            total_mais+=1
            if(total_mais in maximo_fig[1]):
                maximo_fig[1].remove(total_mais)
                return [total_mais,"+"]
        else:
            total_menos+=1
            if(total_menos in maximo_fig[3]):
                maximo_fig[3].remove(total_menos)
                return [total_menos,"-"]

def maximo_pontos(figuras):

    maior_valor = float('-inf')
    maior_figura = None

    for i, sublist in enumerate(figuras):
        if sublist:
            maximo_atual = max(sublist, default=float('-inf'))
            if maximo_atual > maior_valor:
                maior_valor = maximo_atual

                if i == 0:
                    maior_figura = "0"
                elif i == 1:
                    maior_figura = "+"
                elif i == 2:
                    maior_figura = "*"
                elif i == 3:
                    maior_figura = "-"

    return [maior_valor, maior_figura]

def conta_bolas(num_total):
    res=[]
    while 1:
        if num_total>=16:
            res.append(16)
            num_total=num_total-16
        else:
            if num_total>=4:
                resto = num_total%4
                if resto != 0:
                    res.append(num_total - resto)
                    num_total = resto
                else:
                    res.append(num_total)
                    break
            else:
                break
    return res

def conta_mais_vezes(num_total):
    res=[]
    while 1:
        if num_total>=9:
            res.append(9)
            num_total=num_total-9    
        else:
            if num_total>=5:
                res.append(5)
                num_total=num_total-5
            else:
                break
    return res

def conta_menos(num_total):
    res=[]
    
    while 1:
        if num_total>=3:
            res.append(3)
            num_total=num_total-3
        else:
            if num_total==2:
                res.append(2)
            break
        
    return res

def converter_num_possiveis(pecas):
    bolas_numero = conta_bolas(pecas[0])
    mais_numero = conta_mais_vezes(pecas[1])
    vezes_numero = conta_mais_vezes(pecas[2])
    menos_numero = conta_menos(pecas[3])
    
    # escolha=escolha_heuristica(bolas_numero, mais_numero, vezes_numero, menos_numero)    
    return [bolas_numero, mais_numero, vezes_numero, menos_numero]

def pecas_intervalo(final):
    num_bola=0
    num_mais=0
    num_vezes=0
    num_menos=0
    for i in range(final):
        if(pecas[i]=="0"):
            num_bola+=1
        elif(pecas[i]=="+"):
            num_mais+=1
        elif(pecas[i]=="*"):
            num_vezes+=1
        else:
            num_menos+=1
    return [num_bola, num_mais, num_vezes, num_menos]

def melhor_escolha():   
    # [0,+,*,-]
    global pecas
    
    pecas_aux=pecas
        
    escolha=[]
    
    poss_fig_global=pecas_intervalo(len(pecas))
    maximo_fig=converter_num_possiveis(poss_fig_global)
    print(maximo_fig)
    
    maximo=maximo_pontos(maximo_fig)
    print(maximo)
    while 1:
        if(len(pecas)>25):
            limite=25
        else:   
            limite=len(pecas)
        
        figura = maior_figura(limite, maximo_fig)
        
        if figura==None:
            
            pecas_inic=pecas_intervalo(limite)
            poss_fig=converter_num_possiveis(pecas_inic)
            # print(poss_fig)
            
            figura=maior_figura_possivel(limite, poss_fig, maximo[1])
            
            if figura!=None:
            
                remove_figuras(figura[1], figura[0])
            
                poss_fig_global=pecas_intervalo(len(pecas))
                maximo_fig=converter_num_possiveis(poss_fig_global)
                # print(maximo_fig)
                
            else:
                break
        else:
            remove_figuras(figura[1], figura[0])
        
        escolha.append(figura)
    
    pecas=pecas_aux
    
    return escolha

def verifica_concorencia(linha, coluna, peca):
    global matriz_heuristica
    contador=0
    for i in range(len(matriz_heuristica[linha][coluna])):
        if matriz_heuristica[linha][coluna][i] != peca:
            contador+=1
    return contador

def verifica_sitio_pecas_antes(linha, coluna, peca):
    global pecas_antes_verificadas, matriz_heuristica
    contador = 0
    for i in range(len(matriz_heuristica[linha][coluna])):
        for j in range(len(pecas_antes_verificadas)):
            if matriz_heuristica[linha][coluna][i] == peca and (pecas_antes_verificadas[j][0] != linha or pecas_antes_verificadas[j][1] != coluna or pecas_antes_verificadas[j][2] != peca):
                contador = i
                pecas_antes_verificadas.append([linha, coluna, peca])
    return contador

def verifica_sitio_peca_maxima(linha, coluna):
    global pecas_maximas
    contador=0
    for i in range(len(pecas_maximas)):
        if pecas_maximas[i] in matriz_heuristica[linha][coluna]:
            contador+=1
        return contador

def inserir_peca_heuristica(ordem, peca, linha, coluna):
    global matriz_heuristica, pecas_maximas
    
    for i in range(len(peca)):
        if peca[i] in matriz_heuristica[linha][coluna]:
            posicao=matriz_heuristica[linha][coluna].index(peca[i])
            if posicao==0:
                matriz_heuristica[linha][coluna].insert(0, ordem)
            else:
                matriz_heuristica[linha][coluna].insert(posicao, ordem)
            return 0

    matriz_heuristica[linha][coluna].append(ordem)

def posicao_bola_heuristica(tamanho,ordem,peca):
    global matriz_heuristica
    posicao=[]
    contador=0
    inicio_4=[[0,0],[1,1],[0,1],[1,0]]
    inicio_8=[[0,0],[0,1],[0,2],[1,0],[2,0],[2,2],[2,1],[1,2]]
    inicio_12=[[0,0],[0,1],[0,2],[0,3],[1,0],[2,0],[3,0],[3,1],[3,2],[3,3],[1,3],[2,3]]
    
    if tamanho==4:
        for z in range(len(inicio_4)):
            contador=verifica_concorencia(inicio_4[z][0],inicio_4[z][1],"0")
            contador+=verifica_sitio_peca_maxima(inicio_4[z][0],inicio_4[z][1])
            contador+=verifica_sitio_pecas_antes(inicio_4[z][0],inicio_4[z][1],peca)
            posicao=inicio_4
    elif tamanho==8:
        for z in range(len(inicio_8)):
            contador=verifica_concorencia(inicio_8[z][0],inicio_8[z][1],"0")
            contador+=verifica_sitio_peca_maxima(inicio_8[z][0],inicio_8[z][1])
            contador+=verifica_sitio_pecas_antes(inicio_8[z][0],inicio_8[z][1],peca)
            posicao=inicio_8
    else:
         for z in range(len(inicio_12)):
            contador=verifica_concorencia(inicio_12[z][0],inicio_12[z][1],"0")
            contador+=verifica_sitio_peca_maxima(inicio_12[z][0],inicio_12[z][1])
            contador+=verifica_sitio_pecas_antes(inicio_12[z][0],inicio_12[z][1],peca)
            posicao=inicio_12
    contador_aux=contador
    for i in range(TAMANHO_MATRIZ-(tamanho//4)):
        for j in range(TAMANHO_MATRIZ-(tamanho//4)):
            if(tamanho==4):
                contador=(verifica_concorencia(i,j,"0")+
                          verifica_concorencia(i,j+1,"0")+
                          verifica_concorencia(i+1,j,"0")+
                          verifica_concorencia(i+1,j+1,"0"))
                contador+=(verifica_sitio_peca_maxima(i,j)+
                          verifica_sitio_peca_maxima(i,j+1)+
                          verifica_sitio_peca_maxima(i+1,j)+
                          verifica_sitio_peca_maxima(i+1,j+1))
                contador+=(verifica_sitio_pecas_antes(i,j,peca)+
                          verifica_sitio_pecas_antes(i,j+1,peca)+
                          verifica_sitio_pecas_antes(i+1,j,peca)+
                          verifica_sitio_pecas_antes(i+1,j+1,peca))
                if contador<contador_aux:
                    contador_aux=contador
                    posicao=[[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
            elif(tamanho==8):
                contador=(verifica_concorencia(i,j,"0")+
                          verifica_concorencia(i,j+1,"0")+
                          verifica_concorencia(i,j+2,"0")+
                          verifica_concorencia(i+1,j,"0")+
                          verifica_concorencia(i+2,j,"0")+
                          verifica_concorencia(i+2,j+1,"0")+
                          verifica_concorencia(i+1,j+2,"0")+
                          verifica_concorencia(i+2,j+2,"0"))
                contador+=(verifica_sitio_peca_maxima(i,j)+
                          verifica_sitio_peca_maxima(i,j+1)+
                          verifica_sitio_peca_maxima(i,j+2)+
                          verifica_sitio_peca_maxima(i+1,j)+
                          verifica_sitio_peca_maxima(i+2,j)+
                          verifica_sitio_peca_maxima(i+2,j+1)+
                          verifica_sitio_peca_maxima(i+1,j+2)+
                          verifica_sitio_peca_maxima(i+2,j+2))
                contador+=(verifica_sitio_pecas_antes(i,j,peca)+
                          verifica_sitio_pecas_antes(i,j+1,peca)+
                          verifica_sitio_pecas_antes(i,j+2,peca)+
                          verifica_sitio_pecas_antes(i+1,j,peca)+
                          verifica_sitio_pecas_antes(i+2,j,peca)+
                          verifica_sitio_pecas_antes(i+2,j+1,peca)+
                          verifica_sitio_pecas_antes(i+1,j+2,peca)+
                          verifica_sitio_pecas_antes(i+2,j+2,peca))
                if contador<contador_aux:
                    contador_aux=contador
                    posicao=[[i,j],[i,j+1],[i,j+2],[i+1,j],[i+2,j],[i+2,j+1],[i+1,j+2],[i+2,j+2]]
            elif(tamanho==12):
                contador=(verifica_concorencia(i,j,"0")+
                          verifica_concorencia(i,j+1,"0")+
                          verifica_concorencia(i,j+2,"0")+
                          verifica_concorencia(i,j+3,"0")+
                          verifica_concorencia(i+1,j,"0")+
                          verifica_concorencia(i+2,j,"0")+
                          verifica_concorencia(i+3,j,"0")+
                          verifica_concorencia(i+2,j+3,"0")+
                          verifica_concorencia(i+3,j+1,"0")+
                          verifica_concorencia(i+3,j+2,"0")+
                          verifica_concorencia(i+3,j+3,"0")+
                          verifica_concorencia(i+1,j+3,"0"))
                contador+=(verifica_sitio_peca_maxima(i,j)+
                          verifica_sitio_peca_maxima(i,j+1)+
                          verifica_sitio_peca_maxima(i,j+2)+
                          verifica_sitio_peca_maxima(i,j+3)+
                          verifica_sitio_peca_maxima(i+1,j)+
                          verifica_sitio_peca_maxima(i+2,j)+
                          verifica_sitio_peca_maxima(i+3,j)+
                          verifica_sitio_peca_maxima(i+2,j+3)+
                          verifica_sitio_peca_maxima(i+3,j+1)+
                          verifica_sitio_peca_maxima(i+3,j+2)+
                          verifica_sitio_peca_maxima(i+3,j+3)+
                          verifica_sitio_peca_maxima(i+1,j+3))
                contador+=(verifica_sitio_pecas_antes(i,j,peca)+
                          verifica_sitio_pecas_antes(i,j+1,peca)+
                          verifica_sitio_pecas_antes(i,j+2,peca)+
                          verifica_sitio_pecas_antes(i,j+3,peca)+
                          verifica_sitio_pecas_antes(i+1,j,peca)+
                          verifica_sitio_pecas_antes(i+2,j,peca)+
                          verifica_sitio_pecas_antes(i+3,j,peca)+
                          verifica_sitio_pecas_antes(i+2,j+3,peca)+
                          verifica_sitio_pecas_antes(i+3,j+1,peca)+
                          verifica_sitio_pecas_antes(i+3,j+2,peca)+
                          verifica_sitio_pecas_antes(i+3,j+3,peca)+
                          verifica_sitio_pecas_antes(i+1,j+3,peca))
                if contador<contador_aux:
                    contador_aux=contador
                    posicao=[[i,j],[i,j+1],[i,j+2],[i,j+3],
                             [i+1,j],[i+2,j],[i+3,j],[i+2,j+3]
                             [i+3,j+1],[i+3,j+2],[i+3,j+3],[i+1,j+3]]
    for g in range(len(posicao)):
        inserir_peca_heuristica(ordem, peca, posicao[g][0],posicao[g][1])

def posicao_vezes_heuristica(ordem,peca):
    global matriz_heuristica
    posicao=[[0,0],[1,1],[2,2],[0,2],[2,0]]
    contador=(verifica_concorencia(0,0,"*")+verifica_concorencia(1,1,"*")+
              verifica_concorencia(2,2,"*")+verifica_concorencia(0,2,"*")+
              verifica_concorencia(2,0,"*"))
    contador+=(verifica_sitio_peca_maxima(0,0)+verifica_sitio_peca_maxima(1,1)+
              verifica_sitio_peca_maxima(2,2)+verifica_sitio_peca_maxima(0,2)+
              verifica_sitio_peca_maxima(2,0))
    contador+=(verifica_sitio_pecas_antes(0,0,peca)+verifica_sitio_pecas_antes(1,1,peca)+
              verifica_sitio_pecas_antes(2,2,peca)+verifica_sitio_pecas_antes(0,2,peca)+
              verifica_sitio_pecas_antes(2,0,peca))
    contador_aux=contador
    for i in range(1,TAMANHO_MATRIZ-1):
        for j in range(1,TAMANHO_MATRIZ-1):
            contador+=(verifica_concorencia(i,j,"*")+
                      verifica_concorencia(i-1,j-1,"*")+
                      verifica_concorencia(i+1,j+1,"*")+
                      verifica_concorencia(i-1,j+1,"*")+
                      verifica_concorencia(i+1,j-1,"*"))
            contador+=(verifica_sitio_peca_maxima(i,j)+
                      verifica_sitio_peca_maxima(i-1,j-1)+
                      verifica_sitio_peca_maxima(i+1,j+1)+
                      verifica_sitio_peca_maxima(i-1,j+1)+
                      verifica_sitio_peca_maxima(i+1,j-1))
            contador+=(verifica_sitio_pecas_antes(i,j,peca)+
                      verifica_sitio_pecas_antes(i-1,j-1,peca)+
                      verifica_sitio_pecas_antes(i+1,j+1,peca)+
                      verifica_sitio_pecas_antes(i-1,j+1,peca)+
                      verifica_sitio_pecas_antes(i+1,j-1,peca))
            if contador<contador_aux:
                contador_aux=contador
                posicao=[[i,j],[i-1,j-1],[i+1,j+1],[i-1,j+1],[i+1,j-1]]
    
    for z in range(len(posicao)):
        inserir_peca_heuristica(ordem,peca,posicao[z][0],posicao[z][1])

def posicao_mais_heuristica(ordem,peca):
    global matriz_heuristica
    posicao=[[1,0],[1,1],[2,1],[0,1],[1,2]]
    contador=(verifica_concorencia(1,0,"+")+verifica_concorencia(1,1,"+")+
              verifica_concorencia(2,1,"+")+verifica_concorencia(0,1,"+")+
              verifica_concorencia(1,2,"+"))
    contador+=(verifica_sitio_peca_maxima(1,0)+verifica_sitio_peca_maxima(1,1)+
              verifica_sitio_peca_maxima(2,1)+verifica_sitio_peca_maxima(0,1)+
              verifica_sitio_peca_maxima(1,2))
    contador+=(verifica_sitio_pecas_antes(1,0,peca)+verifica_sitio_pecas_antes(1,1,peca)+
              verifica_sitio_pecas_antes(2,1,peca)+verifica_sitio_pecas_antes(0,1,peca)+
              verifica_sitio_pecas_antes(1,2,peca))
    
    contador_aux=contador
    for i in range(1,TAMANHO_MATRIZ-1):
        for j in range(1,TAMANHO_MATRIZ-1):
            contador=(verifica_concorencia(i,j,"+")+
                      verifica_concorencia(i-1,j,"+")+
                      verifica_concorencia(i,j-1,"+")+
                      verifica_concorencia(i,j+1,"+")+
                      verifica_concorencia(i+1,j,"+"))
            contador+=(verifica_sitio_peca_maxima(i,j)+
                      verifica_sitio_peca_maxima(i-1,j)+
                      verifica_sitio_peca_maxima(i,j-1)+
                      verifica_sitio_peca_maxima(i,j+1)+
                      verifica_sitio_peca_maxima(i+1,j))
            contador+=(verifica_sitio_pecas_antes(i,j,peca)+
                      verifica_sitio_pecas_antes(i-1,j,peca)+
                      verifica_sitio_pecas_antes(i,j-1,peca)+
                      verifica_sitio_pecas_antes(i,j+1,peca)+
                      verifica_sitio_pecas_antes(i+1,j,peca))
            if contador<contador_aux:
                contador_aux=contador
                posicao=[[i,j],[i-1,j],[i,j-1],[i,j+1],[i+1,j]]
    
    for z in range(len(posicao)):
        inserir_peca_heuristica(ordem,peca,posicao[z][0],posicao[z][1])

def posicao_menos_heuristica(tamanho,ordem,peca):
    global matriz_heuristica
    posicao=[]
    contador=0
    if tamanho==2:
        contador=verifica_concorencia(0,0,"-")+verifica_concorencia(0,1,"-")
        contador+=verifica_sitio_peca_maxima(0,0)+verifica_sitio_peca_maxima(0,1)
        contador+=verifica_sitio_pecas_antes(0,0,peca)+verifica_sitio_pecas_antes(0,1,peca)
        posicao=[[0,0],[0,1]]
    elif tamanho==3:
        contador=verifica_concorencia(0,0,"-")+verifica_concorencia(0,1,"-")+verifica_concorencia(0,2,"-")
        contador+=verifica_sitio_peca_maxima(0,0)+verifica_sitio_peca_maxima(0,1)+verifica_sitio_peca_maxima(0,2)
        contador+=verifica_sitio_pecas_antes(0,0,peca)+verifica_sitio_pecas_antes(0,1,peca)+verifica_sitio_pecas_antes(0,2,peca)
        posicao=[[0,0],[0,1],[0,2]]
    contador_aux=contador
    for i in range(TAMANHO_MATRIZ):
        for j in range(TAMANHO_MATRIZ-tamanho):
            if tamanho==2:
                contador=verifica_concorencia(i,j,"-")+verifica_concorencia(i,j+1,"-")
                contador+=verifica_sitio_peca_maxima(i,j)+verifica_sitio_peca_maxima(i,j+1)
                contador+=verifica_sitio_pecas_antes(i,j,peca)+verifica_sitio_pecas_antes(i,j+1,peca)
            elif tamanho==3:
                contador=verifica_concorencia(i,j,"-")+verifica_concorencia(i,j+1,"-")+verifica_concorencia(i,j+2,"-")
                contador+=verifica_sitio_peca_maxima(i,j)+verifica_sitio_peca_maxima(i,j+1)+verifica_sitio_peca_maxima(i,j+2)
                contador+=verifica_sitio_pecas_antes(i,j,peca)+verifica_sitio_pecas_antes(i,j+1,peca)+verifica_sitio_pecas_antes(i,j+2,peca)
            if i==TAMANHO_MATRIZ-1:
                contador-=(10*tamanho)
            if contador<contador_aux:
                contador_aux=contador
                if tamanho==2:
                    posicao=[[i,j],[i,j+1]]
                else:
                    posicao=[[i,j],[i,j+1],[i,j+2]]
    
    for z in range(len(posicao)):
        inserir_peca_heuristica(ordem,peca,posicao[z][0],posicao[z][1])

def peca_tipo_maior(ordem, peca):
    global matriz_heuristica
    
    if ordem[1]=="+":
        inserir_peca_heuristica(ordem,peca,1,2)
        inserir_peca_heuristica(ordem,peca,2,2)
        inserir_peca_heuristica(ordem,peca,3,2)
        inserir_peca_heuristica(ordem,peca,2,1)
        inserir_peca_heuristica(ordem,peca,2,3)
    
    elif ordem[1]=="*":
        inserir_peca_heuristica(ordem,peca,1,1)
        inserir_peca_heuristica(ordem,peca,2,2)
        inserir_peca_heuristica(ordem,peca,3,3)
        inserir_peca_heuristica(ordem,peca,1,3)
        inserir_peca_heuristica(ordem,peca,3,1)
        
    else:
        bolas_lado=(ordem[0])//4
        
        inserir_peca_heuristica(ordem,peca,0,0)
        inserir_peca_heuristica(ordem,peca,bolas_lado,bolas_lado)
        
        for i in range(bolas_lado):
            inserir_peca_heuristica(ordem,peca,0,i+1)
            inserir_peca_heuristica(ordem,peca,i+1,0)
        
        if(bolas_lado>1):
            for j in range(1,bolas_lado):
                inserir_peca_heuristica(ordem,peca,bolas_lado,i)
                inserir_peca_heuristica(ordem,peca,i,bolas_lado)

def preenche_matriz_heuristica_maximo(maximo):
    global matriz_heuristica
    if "0"==maximo[1]:
        for i in range(TAMANHO_MATRIZ):
            for j in range(TAMANHO_MATRIZ):
                if (maximo[0] == 16 and (i == 0 or i == TAMANHO_MATRIZ - 1 or
                                        j == 0 or j == TAMANHO_MATRIZ - 1)) :
                    matriz_heuristica[i][j].append(maximo)
                    
    elif "+"==maximo[1]:
        for i in range(TAMANHO_MATRIZ):
            for j in range(TAMANHO_MATRIZ):
                if (maximo[0] == 9 and (i == 2 or j==2)):
                    matriz_heuristica[i][j].append(maximo)
                
    elif "*"==maximo[1]:
        for i in range(TAMANHO_MATRIZ):
            for j in range(TAMANHO_MATRIZ):
                if (maximo[0] == 9 and (j==TAMANHO_MATRIZ-1-i or j==i)):
                    matriz_heuristica[i][j].append(maximo)
    return 0

def posicao_pecas():
    global pecas, matriz_heuristica, pecas_maximas

    posicao_peca_maior=[]
    pecas_maiores_tipo=[]
    pecas_maiores=[]
    posicoes_visitadas=[]
    
    guarda_aux=[]
    
    ordem=melhor_escolha()
    
    # pecas maiores
    for i in range(len(ordem)):
        if ordem[i][0] in [16,9]:
            preenche_matriz_heuristica_maximo(ordem[i])
            posicao_peca_maior.append(i)
            posicoes_visitadas.append(i)
            if ordem[i][1] not in pecas_maiores_tipo:
                pecas_maiores_tipo.append(ordem[i][1])
                pecas_maiores.append(ordem[i])
    
    guarda_aux=pecas_maiores.copy()
    guarda_aux_posicao=posicao_peca_maior.copy()
    
    # pecas mesmo tipo 
    for z in range(len(ordem)):
        if z not in posicoes_visitadas:
            if z>posicao_peca_maior[0]:
                pecas_maiores.pop(0)
                posicao_peca_maior.pop(0)
            if ordem[z] not in pecas_maiores:
                if ordem[z][1] in pecas_maiores_tipo:
                    for k in range(len(pecas_maiores_tipo)):
                        if pecas_maiores_tipo[k]==ordem[z][1]:
                            peca_tipo_maior(ordem[z], pecas_maiores)
                            posicoes_visitadas.append(z)
            
    pecas_maiores=guarda_aux
    pecas_maximas=pecas_maiores.copy()
    posicao_peca_maior=guarda_aux_posicao
    
    #as outras pecas         
    for j in range(len(ordem)):
        if j not in posicoes_visitadas:
            if len(posicao_peca_maior)>0:
                while 1:
                    if(j>posicao_peca_maior[0]):
                        pecas_maiores.pop(0)
                        posicao_peca_maior.pop(0)
                    else:
                        break
                    if pecas_maiores==[]:
                        pecas_maiores.append([20,"-"])
                        break
            if ordem[j][1]=="-":
                posicao_menos_heuristica(ordem[j][0],ordem[j],pecas_maiores)
            elif ordem[j][1]=="+":
                posicao_mais_heuristica(ordem[j],pecas_maiores)
            elif ordem[j][1]=="*":
                posicao_vezes_heuristica(ordem[j],pecas_maiores)
            else:
                posicao_bola_heuristica(ordem[j][0],ordem[j],pecas_maiores)

    return ordem

#Funções para Heuristica de menos de 25 peças

def numero_pecas_dadas(peca):
    global pecas
    contador = 0

    if len(pecas) <= 25:
        for peca_i in pecas:
            if peca_i == peca:
                contador += 1
    else:
        for i in range(len(pecas)):
            if pecas[i] == peca:
                contador += 1
                
    return contador

def conta_x(peca, pecas_figura):
    global pecas
    contador = 0
    contador_x = 0

    if len(pecas) <= 25:
        for peca_i in pecas:
            if peca_i == peca:
                contador += 1
            if peca_i == "*":
                contador_x += 1
            if contador_x == pecas_figura:
                break
    else:
        for i in range(len(pecas)):
            if pecas[i] == peca:
                contador += 1
            if pecas[i] == "*":
                contador_x += 1
            if contador_x == pecas_figura:
                break
                    
    return contador

def conta_mais_25(peca, pecas_figura):
    global pecas
    contador = 0
    contador_x = 0

    if len(pecas) <= 25:
        for peca_i in pecas:
            if peca_i == peca:
                contador += 1
            if peca_i == "+":
                contador_x += 1
            if contador_x == pecas_figura:
                break
    else:
        for i in range(len(pecas)):
            if pecas[i] == peca:
                contador += 1
            if pecas[i] == "+":
                contador_x += 1
            if contador_x == pecas_figura:
                break
                    
    return contador

def conta_menos_25 (peca, pecas_figura):
    global pecas
    contador = 0
    contador_menos = 0

    if len(pecas) <= 25:
        for peca_i in pecas:
            if peca_i == peca:
                contador += 1
            if peca_i == "-":
                contador_menos += 1
            if contador_menos == pecas_figura:
                break
    else:
        for i in range(len(pecas)):
            if pecas[i] == peca:
                contador += 1
            if pecas[i] == "-":
                contador_menos += 1
            if contador_menos == pecas_figura:
                break
                    
    return contador

def conta_bola (peca, pecas_figura):
    global pecas
    contador = 0
    contador_menos = 0

    if len(pecas) <= 25:
        for peca_i in pecas:
            if peca_i == peca:
                contador += 1
            if peca_i == "0":
                contador_menos += 1
            if contador_menos == pecas_figura:
                break
    else:
        for i in range(len(pecas)):
            if pecas[i] == peca:
                contador += 1
            if pecas[i] == "0":
                contador_menos += 1
            if contador_menos == pecas_figura:
                break
                    
    return contador

def heuristica_simples(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    bolas_colocadas = 0
    x_colocadas = 0
    mais_colocadas = 0

    for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 3:
                    indexBola = 0
                    pontos += 2**4
            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais5[indexMais][0], posicoes_mais5[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":
                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2

def heuristica_bola3(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexX = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    menos_ordem = 0
    bolas_colocadas = 0
    x_colocadas = 0
    mais_colocadas = 0

    if (pecas_mais>=5 and pecas_x>=5 and (conta_mais_25("0",5)<=6 and conta_x("0",5)<=6)):

        posicoes_bola8 = [(3,2),(2,1),(1,1),(1,2),(1,3),(2,3),(3,3),(3,1)] 

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais5[indexMais][0], posicoes_mais5[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":
                if(pecas_menos>2):

                    bolas_antes_menos = conta_menos_25("0",3+menos_ordem)

                    if(bolas_antes_menos <= 5):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_mais>=5 and pecas_x<5):

            posicoes_bola8 = [(3,2),(2,1),(1,1),(1,2),(1,3),(3,3),(3,1),(2,3)] 

            posicoes_x = [(5,1),(5,3),(4,2),(5,2),(4,1)]

            for peca in pecas:
                if peca == "0":
                    coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 7:
                        indexBola = 0
                        pontos += 2**8
                if peca == "*":
                    coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                    indexX += 1
                    pecas_x -= 1
                    x_colocadas += 1
                if peca == "+":
                    coloca_peca(peca, posicoes_mais5[indexMais][0], posicoes_mais5[indexMais][1])
                    indexMais += 1
                    pecas_mais -= 1
                    mais_colocadas += 1
                    if indexMais > 4:
                        indexMais = 0
                        pontos += 2**5
                if peca == "-":
                    if(pecas_menos>2):

                        bolas_antes_menos = conta_menos_25("0",3+menos_ordem)

                        if(bolas_antes_menos <= 5):
                            coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                            indexMenos += 1
                            menos_colocadas += 1
                            if indexMenos > 2:
                                indexMenos = 0
                                pontos += 2**3
                                pecas_menos -= 3
                                menos_ordem += 3
                        else:
                            coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                            indexMenos += 1
                            menos_colocadas += 1
                            if indexMenos > 1:
                                indexMenos = 0
                                pontos += 2**2
                                pecas_menos -= 2
                                menos_ordem += 2
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                

    elif(pecas_x>=5 and pecas_mais<5):

        posicoes_bola8 = [(3,2),(2,1),(1,1),(1,2),(1,3),(2,3),(3,3),(3,1)] 

        posicoes_x = [(5,3),(5,5),(4,4),(3,5),(3,3)]
        posicoes_mais = [(3,4),(2,4),(2,5),(1,4),(2,3)]

        posicoes_menos2 = [(5,1),(5,2)]
        posicoes_menos3 = [(4,3),(4,1),(4,2)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":
                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
            
    else:

        posicoes_bola8 = [(3,2),(2,1),(1,1),(1,2),(1,3),(3,3),(3,1),(2,3)] 

        posicoes_x = [(5,1),(5,3),(4,2),(5,2)]
        posicoes_mais = [(5,4),(4,5),(5,5),(3,5)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8 
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":
                if(pecas_menos>2):

                    bolas_antes_menos = conta_menos_25("0",3+menos_ordem)

                    if(bolas_antes_menos <= 5):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2

def heuristica_bola4(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexX = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    menos_ordem = 0
    bolas_colocadas = 0
    x_colocadas = 0
    mais_colocadas = 0

    if(pecas_x>=9 and conta_x("0",9)<=8): 

        posicoes_bola12 = [(1,2),(1,4),(2,1),(3,1),(4,1),(4,3),(3,4),(4,4),(4,2),(1,1),(2,4),(1,3)]

        posicoes_menos3 = [(5,2),(5,4),(5,3)]
        posicoes_menos2 = [(5,2),(5,3)]
        posicoes_mais = [(2,5),(3,5),(4,5)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 11:
                    indexBola = 0
                    pontos += 2**12
            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":
                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
            

    elif(pecas_mais>=9 and conta_mais_25("0",9)<=8):

        posicoes_bola12 = [(1,1),(1,2),(1,4),(2,1),(4,1),(4,2),(2,4),(4,4),(3,4),(1,3),(3,1),(4,3)]

        posicoes_menos = [(5,1),(5,2)]
        posicoes_x = [(1,5),(5,5),(4,5),(2,5)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 11:
                    indexBola = 0
                    pontos += 2**12
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1 
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":
                coloca_peca(peca, posicoes_menos[indexMenos][0], posicoes_menos[indexMenos][1])
                indexMenos += 1
                menos_colocadas += 1
                if indexMenos > 1:
                    indexMenos = 0
                    pontos += 2**1
                    pecas_menos -= 2
            

    elif(pecas_mais>=5 and pecas_x>=5 and (conta_mais_25("0",5)<=7 and conta_x("0",5)<=7)):

        posicoes_bola12 = [(1,1),(1,2),(1,3),(1,4),(2,1),(4,1),(2,4),(3,1),(3,4),(4,4),(4,3),(4,2)] 

        posicoes_menos3 = [(2,2),(2,4),(2,3)]
        posicoes_menos2 = [(2,2),(2,3)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 11:
                    indexBola = 0
                    pontos += 2**12
            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais5[indexMais][0], posicoes_mais5[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":
                if(pecas_menos>2):

                    bolas_antes_menos = conta_menos_25("0",3+menos_ordem)

                    if(bolas_antes_menos <= 6):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_x>=5):

        posicoes_bola12 = [(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1),(2,4),(3,4),(4,2),(4,3),(4,4)]

        posicoes_x = [(5,3),(5,5),(3,3),(3,5),(4,4)]
        posicoes_mais = [(3,2),(5,2),(5,4),(5,1)]

        posicoes_menos3 = [(2,2),(2,4),(2,3)]
        posicoes_menos2 = [(2,2),(2,3)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 11:
                    indexBola = 0
                    pontos += 2**12
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":
                if(pecas_menos>2):

                    bolas_antes_menos = conta_menos_25("0",3+menos_ordem)

                    if(bolas_antes_menos <= 7):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            
        
    elif(pecas_mais>=5 and conta_mais_25("0",5)<=10):
        
        posicoes_bola12 = [(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1),(2,4),(4,2),(4,4),(4,3),(3,4)]

        posicoes_mais = [(2,3),(3,2),(3,3),(3,4),(4,3)]
        posicoes_x = [(5,5),(3,5),(5,4),(4,5)]
        posicoes_menos3 = [(5,1),(5,3),(5,2)]
        posicoes_menos2 = [(5,1),(5,2)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 11:
                    indexBola = 0
                    pontos += 2**12
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":
                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
            

    else:
        if(pecas_menos>=2):

            posicoes_bola12 = [(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1),(3,4),(4,4),(4,3),(4,2),(2,4)]
            
            posicoes_x = [(5,1),(5,3),(3,3),(5,2)] 
            posicoes_mais = [(5,4),(4,5),(5,5),(3,5)]

            posicoes_menos3 = [(2,5),(2,3),(2,4)]
            posicoes_menos2 = [(2,2),(2,3)]

            for peca in pecas:
                if peca == "0":
                    coloca_peca(peca, posicoes_bola12[indexBola][0], posicoes_bola12[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 11:
                        indexBola = 0
                        pontos += 2**12
                if peca == "*":
                    coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                    indexX += 1
                    pecas_x -= 1
                    x_colocadas += 1
                if peca == "+":
                    coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                    indexMais += 1
                    pecas_mais -= 1
                    mais_colocadas += 1
                if peca == "-":
                    if(pecas_menos>2):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                
        else:
            heuristica_bola3()

def heuristica_bola5(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexX = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    menos_ordem = 0
    bolas_colocadas = 0
    x_colocadas = 0
    mais_colocadas = 0

    pecas_x_inicio = pecas_x
    pecas_mais_inicio = pecas_mais

    posicoes_bola16 = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,5),(3,1),(3,5),(4,1),(4,5),(5,1),(5,5),(5,2),(5,4),(5,3)]

    posicoes_x = [(2,2),(2,4),(4,2),(4,4),(3,3)]
    posicoes_mais = [(2,3),(3,2),(3,4),(4,3),(3,3)]

    posicoes_menos3 = [(5,2),(5,4),(5,3)]
    posicoes_menos2 = [(5,2),(5,3)]

    posicoes_menos_mais = [(4,4),(4,2),(2,4)]
    posicoes_menos_x = [(4,3),(3,4),(3,2)]
    posicoes_menos_x_mais = [(3,3),(4,3),(4,4)]

    for peca in pecas:
        if peca == "0":
            coloca_peca(peca, posicoes_bola16[indexBola][0], posicoes_bola16[indexBola][1])
            indexBola += 1
            pecas_bola -= 1
            bolas_colocadas += 1
            if indexBola>15:
                indexBola = 0
                pontos += 2**16
        if peca == "*":
            coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
            indexX += 1
            pecas_x -= 1
            x_colocadas += 1
            if indexX>4:
                indexX = 0
                pontos += 2**5
        if peca == "+":
            coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
            indexMais += 1
            pecas_mais -= 1 
            mais_colocadas += 1
            if indexMais>4:
                indexMais = 0
                pontos += 2**5
        if peca == "-":

            if(pecas_menos>2):

                bolas_antes_menos3 = conta_menos_25("0",3+menos_ordem)
                bolas_antes_menos2 = conta_menos_25("0",2+menos_ordem)

                if(bolas_antes_menos3 <= 13):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                        menos_ordem += 3
                elif(bolas_antes_menos2 <= 14):
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
                else:
                    if(pecas_x_inicio>=5):
                        coloca_peca(peca, posicoes_menos_x[indexMenos][0], posicoes_menos_x[indexMenos][1]) 
                        indexMenos += 1
                        pecas_menos -= 1
                        menos_colocadas += 1
                        menos_ordem += 1
                    elif(pecas_mais_inicio>=5):
                        coloca_peca(peca, posicoes_menos_mais[indexMenos][0], posicoes_menos_mais[indexMenos][1]) 
                        indexMenos += 1
                        pecas_menos -= 1
                        menos_colocadas += 1
                        menos_ordem += 1
                    else:
                        coloca_peca(peca, posicoes_menos_x_mais[indexMenos][0], posicoes_menos_x_mais[indexMenos][1]) 
                        indexMenos += 1
                        pecas_menos -= 1
                        menos_colocadas += 1
                        menos_ordem += 1

            else:

                bolas_antes_menos = conta_menos_25("0",2+menos_colocadas)

                if(bolas_antes_menos <= 14):
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pecas_menos -= 2
                        menos_ordem += 2
                else:
                    if(pecas_x_inicio>=5):
                        coloca_peca(peca, posicoes_menos_x[indexMenos][0], posicoes_menos_x[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        menos_ordem += 1
                    elif(pecas_mais_inicio>=5):
                        coloca_peca(peca, posicoes_menos_mais[indexMenos][0], posicoes_menos_mais[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        menos_ordem += 1
                    else:
                        coloca_peca(peca, posicoes_menos_x_mais[indexMenos][0], posicoes_menos_x_mais[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        menos_ordem += 1
        
def heuristica_mais9(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexX = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    menos_ordem = 0
    bolas_colocadas = 0
    bolas_ordem = 0
    x_colocadas = 0
    mais_colocadas = 0

    if(pecas_x>=9):

        posicoes_x9 = [(5,5),(5,1),(4,4),(4,2),(2,4),(1,5),(2,2),(1,1),(3,3)]
        posicoes_mais9 = [(1,3),(2,3),(3,1),(3,2),(3,4),(3,5),(4,3),(5,3),(3,3)]

        posicoes_menos2 = [(1,4),(1,5)]
        posicoes_menos3 = [(5,2),(5,4),(5,3)]

        posicoes_bola_x = [(1,2),(2,1),(4,1),(5,2),(5,4),(4,5),(1,4)]
        posicoes_menos_x_mais = [(1,4),(2,5),(4,5)]

        x_antes_bola = conta_bola("*",4)

        for peca in pecas:
            if peca == "0":

                if(x_antes_bola<=6):
                    coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 3:
                        indexBola = 0
                        pontos += 2**4
                        pecas_bola -= 4
                        bolas_ordem += 4
                else:
                    coloca_peca(peca, posicoes_bola_x[indexBola][0], posicoes_bola_x[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1

            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1 
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":

                if(pecas_menos>2):

                    mais_antes_menos3 = conta_menos_25("+",3+menos_ordem)
                    x_antes_menos2 = conta_menos_25("*",2+menos_ordem)

                    if(mais_antes_menos3 <= 7):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    elif(x_antes_menos2 <= 5):
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                    else:
                        coloca_peca(peca, posicoes_menos_x_mais[indexMenos][0], posicoes_menos_x_mais[indexMenos][1]) 
                        indexMenos += 1
                        pecas_menos -= 1
                        menos_colocadas += 1
                        menos_ordem += 1

                else:

                    bolas_antes_menos = conta_menos_25("0",2+menos_ordem)

                    if(bolas_antes_menos <= 14):
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2
                    else:
                        coloca_peca(peca, posicoes_menos_x_mais[indexMenos][0], posicoes_menos_x_mais[indexMenos][1]) 
                        indexMenos += 1
                        pecas_menos -= 1
                        menos_colocadas += 1
                        menos_ordem += 1
            

    elif(pecas_bola>=8 and pecas_x>=5 and (conta_bola("+",8)<=2 and conta_x("+",5)<=2)):

        posicoes_mais9 = [(3,4),(4,3),(3,5),(5,3),(1,3),(2,3),(3,1),(3,2),(3,3)]
        posicoes_bola8 = [(1,1),(1,2),(2,1),(1,3),(3,2),(3,1),(3,3),(2,3)]
        posicoes_x5 = [(5,5),(5,3),(4,4),(3,5),(3,3)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
                    pecas_bola -= 8
                    bolas_ordem += 8
            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":

                if(pecas_menos>2):

                    bola_antes_menos3 = conta_menos_25("0",3+menos_ordem)

                    if(bola_antes_menos3 <= 7):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2 
                            pecas_menos -= 2
                            menos_ordem += 2

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_bola>=8 and conta_bola("+",8)<=4):

        posicoes_mais9 = [(3,4),(3,5),(4,3),(5,3),(1,3),(2,3),(3,1),(3,2),(3,3)]
        posicoes_bola8 = [(1,1),(1,2),(2,1),(1,3),(3,2),(3,1),(3,3),(2,3)]

        posicoes_x = [(5,1),(4,2),(5,5),(4,4),(2,2),(1,5),(4,1),(5,2)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
                    pecas_bola -= 8
                    bolas_ordem += 8
            if peca == "*":
                coloca_peca(peca, posicoes_x[indexX][0], posicoes_x[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":

                if(pecas_menos>2):

                    bola_antes_menos3 = conta_menos_25("0",3+menos_ordem)

                    if(bola_antes_menos3 <= 7):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_x>=5):

        posicoes_mais9 = [(3,4),(3,5),(4,3),(5,3),(2,3),(3,1),(3,2),(1,3),(3,3)]

        posicoes_x5 = [(4,4),(4,2),(2,4),(2,2),(3,3)]

        posicoes_menos3 = [(1,5),(1,3),(1,4)]
        posicoes_menos2 = [(1,5),(1,4)]

        posicoes_bola4 = [(1,1),(1,2),(2,1),(2,2)]

        posicoes_bola_x = [(1,1),(1,2),(2,1),(4,1),(5,1),(5,2),(5,4),(5,5),(4,5),(2,5)]

        for peca in pecas:
            if peca == "0":

                x_antes_bola = conta_bola("*",4+bolas_ordem)

                if(x_antes_bola<=3):
                    coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 3:
                        indexBola = 0
                        pontos += 2**4
                        bolas_ordem += 4
                else:
                    coloca_peca(peca, posicoes_bola_x[indexBola][0], posicoes_bola_x[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1

            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 4:
                    indexX = 0
                    pontos += 2**5
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1
                pecas_mais -= 1 
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":

                if(pecas_menos>2):

                    mais_antes_menos3 = conta_menos_25("+",3+menos_ordem)

                    if(mais_antes_menos3 <= 7):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            
    
    else:

        posicoes_mais9 = [(3,4),(3,5),(4,3),(5,3),(3,1),(3,2),(2,3),(1,3),(3,3)]

        posicoes_x = [(5,1),(4,2),(5,5),(4,4)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 3:
                    indexBola = 0
                    pontos += 2**4
                    pecas_bola -= 4
                    bolas_ordem += 4
            if peca == "*":
                coloca_peca(peca, posicoes_x5[indexX][0], posicoes_x5[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
            if peca == "+":
                coloca_peca(peca, posicoes_mais9[indexMais][0], posicoes_mais9[indexMais][1])
                indexMais += 1 
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 8:
                    indexMais = 0
                    pontos += 2**9
            if peca == "-":

                if(pecas_menos>2):

                    mais_antes_menos3 = conta_menos_25("+",3+menos_ordem)

                    if(mais_antes_menos3 <= 8):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            
def heuristica_x9(pecas_bola, pecas_mais, pecas_menos, pecas_x):
    global pecas, pontos, posicoes_bola4, posicoes_bola8, posicoes_x9, posicoes_x5, posicoes_mais5, posicoes_mais9, posicoes_menos3, posicoes_menos2

    pecas_bola = pecas_bola
    pecas_mais = pecas_mais
    pecas_menos = pecas_menos
    pecas_x = pecas_x

    indexBola = 0
    indexX = 0
    indexMais = 0
    indexMenos = 0

    menos_colocadas = 0
    menos_ordem = 0
    bolas_colocadas = 0
    bolas_ordem = 0
    x_colocadas = 0
    mais_colocadas = 0

    if(pecas_bola>=8 and pecas_mais>=5 and (conta_bola("*",8)<=6 and conta_mais_25("*",5)<=6)):

        posicoes_x9 = [(5,5),(4,2),(2,2),(2,4),(1,5),(5,1),(4,4),(1,1),(3,3)]
        posicoes_mais5 = [(5,4),(4,3),(4,5),(3,4),(4,4)]

        posicoes_menos3 = [(5,1),(5,3),(5,2)]
        posicoes_menos2 = [(5,2),(5,3)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
                    pecas_bola -= 8
                    bolas_ordem += 8
            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais5[indexMais][0], posicoes_mais5[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":

                if(pecas_menos>2):

                    x_antes_menos3 = conta_menos_25("*",3+menos_ordem)

                    if(x_antes_menos3 <= 5):
                        coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 2:
                            indexMenos = 0
                            pontos += 2**3
                            pecas_menos -= 3
                            menos_ordem += 3
                    else:
                        coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                        indexMenos += 1
                        menos_colocadas += 1
                        if indexMenos > 1:
                            indexMenos = 0
                            pontos += 2**2
                            pecas_menos -= 2
                            menos_ordem += 2

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_bola>=8 and conta_bola("*",8)<=7):

        posicoes_x9 = [(5,5),(4,2),(2,2),(2,4),(1,5),(5,1),(4,4),(1,1),(3,3)]

        posicoes_mais = [(4,3),(4,5),(3,4),(4,1),(2,5),(1,4),(3,5),(5,4)]

        posicoes_menos3 = [(5,2),(5,4),(5,3)]
        posicoes_menos2 = [(5,2),(5,3)]

        for peca in pecas:
            if peca == "0":
                coloca_peca(peca, posicoes_bola8[indexBola][0], posicoes_bola8[indexBola][1])
                indexBola += 1
                pecas_bola -= 1
                bolas_colocadas += 1
                if indexBola > 7:
                    indexBola = 0
                    pontos += 2**8
                    pecas_bola -= 8
                    bolas_ordem += 8
            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":

                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                        menos_ordem += 3

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2
            

    elif(pecas_mais>=5):

        posicoes_x9 = [(5,1),(5,5),(4,2),(4,4),(1,5),(2,4),(2,2),(1,1),(3,3)]

        posicoes_mais5 = [(2,3),(3,2),(3,4),(4,3),(3,3)]
    
        posicoes_menos3 = [(5,2),(5,4),(5,3)]
        posicoes_menos2 = [(5,2),(5,3)]

        posicoes_bola4 = [(2,1),(1,2),(2,2),(1,1)]

        posicoes_bola_x = [(1,2),(2,1),(1,3),(3,1),(1,4),(4,1),(2,5),(3,5),(4,5)]

        for peca in pecas:
            if peca == "0":

                x_antes_bola = conta_bola("*",4+bolas_ordem)

                if(x_antes_bola <= 7):
                    coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 3:
                        indexBola = 0
                        pontos += 2**4
                        bolas_ordem += 4
                else:
                    coloca_peca(peca, posicoes_bola_x[indexBola][0], posicoes_bola_x[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1

            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1 
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
                if indexMais > 4:
                    indexMais = 0
                    pontos += 2**5
            if peca == "-":

                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3
                        menos_ordem += 3

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2
                        menos_ordem += 2

    else:

        posicoes_bola4 = [(2,1),(1,2),(2,2),(1,1)]

        posicoes_bola_x = [(1,2),(2,1),(1,3),(3,1),(1,4),(4,1),(2,5),(3,5),(4,5)]

        posicoes_mais = [(2,3),(3,2),(3,4),(4,3)]

        posicoes_menos3 = [(5,2),(5,4),(5,3)]
        posicoes_menos2 = [(5,2),(5,3)]

        for peca in pecas:
            if peca == "0":

                x_antes_bola = conta_bola("*",4+bolas_ordem)

                if(x_antes_bola <= 7):
                    coloca_peca(peca, posicoes_bola4[indexBola][0], posicoes_bola4[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1
                    if indexBola > 3:
                        indexBola = 0
                        pontos += 2**4
                        bolas_ordem += 4
                else:
                    coloca_peca(peca, posicoes_bola_x[indexBola][0], posicoes_bola_x[indexBola][1])
                    indexBola += 1
                    pecas_bola -= 1
                    bolas_colocadas += 1

            if peca == "*":
                coloca_peca(peca, posicoes_x9[indexX][0], posicoes_x9[indexX][1])
                indexX += 1
                pecas_x -= 1
                x_colocadas += 1
                if indexX > 8:
                    indexX = 0
                    pontos += 2**9
            if peca == "+":
                coloca_peca(peca, posicoes_mais[indexMais][0], posicoes_mais[indexMais][1])
                indexMais += 1
                pecas_mais -= 1
                mais_colocadas += 1
            if peca == "-":

                if(pecas_menos>2):
                    coloca_peca(peca, posicoes_menos3[indexMenos][0], posicoes_menos3[indexMenos][1])
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 2:
                        indexMenos = 0
                        pontos += 2**3
                        pecas_menos -= 3

                else:
                    coloca_peca(peca, posicoes_menos2[indexMenos][0], posicoes_menos2[indexMenos][1]) 
                    indexMenos += 1
                    menos_colocadas += 1
                    if indexMenos > 1:
                        indexMenos = 0
                        pontos += 2**2
                        pecas_menos -= 2

def escolher_heuristica():
    global matriz_jogo, pecas, pecas_bola, pecas_mais, pecas_menos, pecas_x

    pecas_bola = numero_pecas_dadas("0")
    pecas_mais = numero_pecas_dadas("+")
    pecas_menos = numero_pecas_dadas("-")
    pecas_x = numero_pecas_dadas("*")

    #Heiristica bola 16
    #Heiristica bola 12
    #Heiristica mais de 9
    #Heiristica x de 9
    #Heiristica bola 8
    #Heiristica simples

    if(pecas_bola >= 16):
        heuristica_bola5(pecas_bola, pecas_mais, pecas_menos, pecas_x)
    elif(16 > pecas_bola >= 12):
        heuristica_bola4(pecas_bola, pecas_mais, pecas_menos, pecas_x)
    elif(pecas_mais >= 9):
        heuristica_mais9(pecas_bola, pecas_mais, pecas_menos, pecas_x)
    elif(pecas_x >= 9):
        heuristica_x9(pecas_bola, pecas_mais, pecas_menos, pecas_x)
    elif (12 > pecas_bola >= 8):
        heuristica_bola3(pecas_bola, pecas_mais, pecas_menos, pecas_x)
    else:
        heuristica_simples(pecas_bola, pecas_mais, pecas_menos, pecas_x)

#Funcao que inicia o jogo, percorrendo as pecas do array e colocando-as na matriz de jogo
def jogar():
    global matriz_jogo, matriz_heuristica, pecas, pontos

    if(len(pecas)>25):

        pecas_aux=pecas.copy()
        ordem=posicao_pecas()
        pecas=pecas_aux
        conta_bolas=0
        conta_mais=0
        conta_vezes=0
        conta_menos=0
        
        for q in range(len(ordem)):
            pontos+=2**ordem[q][0]
        
        for i in range(len(pecas)):
            tipo=pecas[i]
            if len(ordem)>0:
                if tipo=="0":
                    conta_bolas+=1
                elif tipo=="+":
                    conta_mais+=1
                elif tipo=="*":
                    conta_vezes+=1
                else:
                    conta_menos+=1
                for z in range(len(ordem)):
                    if tipo==ordem[z][1]:
                        if tipo=="0":
                            coordenadas=procura_coordenada(ordem[z], conta_bolas)
                            coloca_peca(pecas[i],coordenadas[0],coordenadas[1])
                            if conta_bolas==ordem[z][0]:
                                conta_bolas=0
                                ordem.pop(z)
                        elif tipo=="+":
                            coordenadas=procura_coordenada_mais_e_vezes(ordem[z], conta_mais)
                            coloca_peca(pecas[i],coordenadas[0],coordenadas[1])
                            if conta_mais==ordem[z][0]:
                                conta_mais=0
                                ordem.pop(z)
                        elif tipo=="*":
                            coordenadas=procura_coordenada_mais_e_vezes(ordem[z], conta_vezes)
                            coloca_peca(pecas[i],coordenadas[0],coordenadas[1])
                            if conta_vezes==ordem[z][0]:
                                conta_vezes=0
                                ordem.pop(z)
                        else:
                            coordenadas=procura_coordenada_menos(ordem[z], conta_menos, ordem[z][0])
                            coloca_peca(pecas[i],coordenadas[0],coordenadas[1])
                            if conta_menos==ordem[z][0]:
                                conta_menos=0
                                ordem.pop(z)
                                
                        break
            else:
                coordenadas=procura_coordenada_vazia()
                coloca_peca(pecas[i],coordenadas[0],coordenadas[1])
    else:

        escolher_heuristica()

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
    # for i in range(len(pecas)):
    #     if pecas[i] != " ":
    #         contador += 1

    #Verifica se a variavel que conta as pecas e maior que zero
    if contador > 0:

        #Para o numero de pontos final nao ficar negativo, fica a zero 
        if(pontos - 2**contador<=0):
            pontos=0
        else:   
            pontos -= 2**contador

"""
    INICIO DO PROGRAMA
"""

#Cria uma matriz de Ambiente
matriz_jogo = matriz.cria_matriz(TAMANHO_MATRIZ+2)
matriz_heuristica = matriz.cria_matriz_heuristica(TAMANHO_MATRIZ)
matriz.imprime_matriz(matriz_jogo)

"""
    No início o robo verifica as cores que representam os símbolos 
        -AMARELO: O
        -VERMELHO: X
        -VERDE: +
        -AZUL: -
"""

ev3.speaker.beep()
# leitura_objetos()
print(pecas)
# larga_objeto()
jogar()
retira_pontos()
print(pontos)

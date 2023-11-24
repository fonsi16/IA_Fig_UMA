"""
    [0|1|2|3|4]
    
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    """
    
def cria_matriz(colunas, linhas):
    matriz = []
    for i in range(linhas):
        matriz.append([])
        for z in range(colunas):
            matriz[i].append("-")
    return matriz

def imprime_matriz(matriz):
    for i in range(len(matriz)):
        linha = "|"
        for j in range(len(matriz[i])):
            linha +=" "+matriz[i][j]+" |"
        print(linha)
    return 0
    
def inserir_objeto_matriz(objeto,linha,coluna,matriz):
    for i in range(len(matriz)):
        if (i == linha-1):
            for j in range(len(matriz[i])):
                if (j == coluna-1):
                    matriz[i][j]=objeto


#tem de receber o objeto também para então mandar para o 'inserir_objeto_metriz' pq não vai ser sempre 'x'
#aqui ele coloca o objeto no primeiro espaço vazio que houver na matriz
def verifica_tem_objeto(matriz):
    vazio = True
    for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if(vazio == True):
                    if matriz[i][j] != "-":
                        j += 1
                    else:
                        inserir_objeto_matriz("x",i+1,j+1,matriz)
                        vazio = False

#vai verificar se ainda tem espaços em branco, se não houver nenhum significa que a matriz está toda preenchida
#e vai mandar o signal para acabar
def verifica_acabou(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != "-":
                j += 1
            else:
                return True #significa que ainda pode continuar a jogar

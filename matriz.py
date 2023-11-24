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
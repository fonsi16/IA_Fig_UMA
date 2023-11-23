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
            matriz[i].append("")
    return matriz

def imprime_matriz(matriz):
    for i in range(len(matriz)):
        linha = []
        for j in range(len(matriz[i])):
            linha.append(matriz[i][j])
        print(linha)
    return 0
    
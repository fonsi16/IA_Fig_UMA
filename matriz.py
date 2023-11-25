"""
    [0|1|2|3|4]
    
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    """
    
def cria_matriz(tamanho):
    matriz = []
    for i in range(tamanho):
        matriz.append([])
        for z in range(tamanho):
            matriz[i].append(" ")
    return matriz

def imprime_matriz(matriz):
    print("-="*3+"MATRIZ JOGO"+"-="*2)
    for i in range(len(matriz)):
        linha = "|"
        for j in range(len(matriz[i])):
            linha +=" "+matriz[i][j]+" |"
        print(linha)
    return 0
    
def inserir_objeto_matriz(objeto,linha,coluna,matriz):
    matriz[linha][coluna] =objeto
        
def verifica_vazio(matriz, linha, coluna):
    if matriz[linha][coluna] == " ":
        return True
    else:
        return False
    

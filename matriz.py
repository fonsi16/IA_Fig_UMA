"""
    [0|1|2|3|4]
    
   [ [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z]
    [z|z|z|z|z] ]
    """
    
# Cria uma matriz vazia com tamanho 'tamanho'
def cria_matriz(tamanho):
    matriz = []  # Inicializa uma lista vazia para representar a matriz
    for i in range(tamanho):
        matriz.append([])  # Adiciona uma lista vazia como linha da matriz
        for z in range(tamanho):
            matriz[i].append(" ")  # Adiciona espaços em branco para cada célula da matriz
    return matriz  # Retorna a matriz preenchida com espaços em branco

# Imprime a matriz formatada
def imprime_matriz(matriz):
    # Imprime um cabeçalho para a matriz de jogo
    print("-="*4 + "MATRIZ JOGO" + "-="*3)
    
    # Loop para percorrer as linhas da matriz
    for i in range(len(matriz)):
        linha = "|"  # Inicializa uma variável para representar uma linha da matriz com uma barra vertical no início
        # Loop para percorrer os elementos de cada linha da matriz
        for j in range(len(matriz[i])):
            linha += " " + matriz[i][j] + " |"  # Adiciona cada elemento formatado à linha com barras verticais
        print(linha)  # Imprime a linha formatada

# Insere um objeto em uma posição específica da matriz
def inserir_objeto_matriz(objeto, linha, coluna, matriz):
    matriz[linha][coluna] = objeto

# Verifica se uma célula específica da matriz está vazia
def verifica_vazio(matriz, linha, coluna):
    if matriz[linha][coluna] == " ":
        return True
    else:
        return False
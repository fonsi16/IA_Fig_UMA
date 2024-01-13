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
    # Inicializa uma lista vazia para representar a matriz
    matriz = []  
    for i in range(tamanho):
        # Adiciona uma lista vazia como linha da matriz
        matriz.append([])  
        for z in range(tamanho):
            # Adiciona espaços em branco para cada célula da matriz
            matriz[i].append(" ")  
    # Retorna a matriz preenchida com espaços em branco
    return matriz  

# Cria uma matriz heurística vazia com tamanho 'tamanho'
def cria_matriz_heuristica(tamanho):
    # Inicializa uma lista vazia para representar a matriz
    matriz = [] 
    for i in range(tamanho):
        # Adiciona uma lista vazia como linha da matriz
        matriz.append([]) 
        for z in range(tamanho):
            # Adiciona uma lista vazia como célula/posição da matriz
            matriz[i].append([]) 
    # Retorna a matriz preenchida com listas vazias 
    return matriz

# Imprime a matriz formatada
def imprime_matriz(matriz):
    # Imprime um cabeçalho para a matriz de jogo
    print("-="*4 + "MATRIZ JOGO" + "-="*3)
    
    # Loop para percorrer as linhas da matriz
    for i in range(len(matriz)):
        # Inicializa uma variável para representar uma linha da matriz com uma barra vertical no início
        linha = "|"  
        # Loop para percorrer os elementos de cada linha da matriz
        for j in range(len(matriz[i])):
            # Adiciona cada elemento formatado à linha com barras verticais
            linha += " " + matriz[i][j] + " |"  
        # Imprime a linha formatada
        print(linha)  

# Insere um objeto em uma posição específica da matriz
def inserir_objeto_matriz(objeto, linha, coluna, matriz):
    matriz[linha][coluna] = objeto

# Verifica se uma célula específica da matriz está vazia
def verifica_vazio(matriz, linha, coluna):
    if matriz[linha][coluna] == " ":
        return True
    else:
        return False
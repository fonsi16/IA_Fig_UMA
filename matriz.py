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
            matriz[i].append("")
    return matriz

def imprime_matriz(matriz):
    print("-="*5+"MATRIZ JOGO"+"-="*5)
    for i in range(len(matriz)):
        linha = "|"
        for j in range(len(matriz[i])):
            linha +=" "+matriz[i][j]+" |"
        print(linha)
    return 0
    
def inserir_objeto_matriz(objeto,linha,coluna,matriz):
    matriz[linha][coluna] =objeto


#tem de receber o objeto também para então mandar para o 'inserir_objeto_metriz' pq não vai ser sempre 'x'
#aqui ele coloca o objeto no primeiro espaço vazio que houver na matriz
def verifica_tem_objeto(matriz, objeto):
    vazio = True
    for i in range(len(matriz)):
        if(vazio == True):
            for j in range(len(matriz[i])):
                    if matriz[i][j] == "" :
                        inserir_objeto_matriz(objeto,i+1,j+1,matriz)
                        vazio = False
                        break
        
def verifica_vazio(matriz, linha, coluna):
    if matriz[linha][coluna] == "":
        return True
    else:
        return False
    

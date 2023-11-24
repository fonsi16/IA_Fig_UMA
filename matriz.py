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
    for i in range(len(matriz)):
        linha = "|"
        for j in range(len(matriz[i])):
            linha +=" "+matriz[i][j]+" |"
        print(linha)
    return 0
    
def inserir_objeto_matriz(objeto,linha,coluna,matriz):
    matriz[linha-1][coluna-1] =objeto


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
    

#vai verificar se ainda tem espaços em branco, se não houver nenhum significa que a matriz está toda preenchida
#e vai mandar o signal para acabar
def verifica_acabou(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != "-":
                j += 1
            else:
                return True #significa que ainda pode continuar a jogar

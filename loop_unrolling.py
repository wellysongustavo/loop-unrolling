# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import threading

"""
def getLinha(matriz, n):
    return [i for i in matriz[n]]

def getColuna(matriz, n):
    return [i[n] for i in matriz]   

# função para multiplicar as matrizez
def multiplica_matriz(mat1, mat2):
    matResultado = []                 
    for i in range(len(mat1)):           
        matResultado.append([])

        for j in range(len(mat1[0])):
            # multiplica cada linha de mat1 por cada coluna de mat2;
            listMult = [x*y for x, y in zip(getLinha(mat1, i), getColuna(mat2, j))]
            # e em seguida adiciona a matResultado a soma das multiplicações
            matResultado[i].append(sum(listMult))
    ret
    urn matResultado
"""    
# deve ser chamada em paralelo
def func(val1, val2, i, j, metodo, result):
    if metodo == 'thre':
        result[0][0][i][j] = val1 + val2
    else if metodo == 'proc':
        result[0][1][i][j]
    
    
#recebe e trata uma matriz
def unroll(args, func, method, results):
    if method == 'proc':
        for row in args:
            f = os.fork()
            if f == 0:
                func(row[0], row[1], row[2], row[3], metodo, results)
                
    else: # method == 'thre'
        for row in args:
            t = threading.Thread(target=func, args=(row[0], row[1], row[2], row[3], metodo, results))
            t.start()
        

#construindo duas matrizes para operar
linhas = 3
colunas = 3
matriz_1 = np.random.randint(10, size=(linhas,colunas))
matriz_2 = np.random.randint(10, size=(linhas,colunas))
linha_args = 0
args = np.full((linhas*colunas,4), 0)
# populando args com os elementos da matriz 1, matriz 2, linhas e colunas
for l in range(linhas):
    for c in range(colunas):
        args[linha_args][0] = matriz_1[l][c]
        args[linha_args][1] = matriz_2[l][c]
        args[linha_args][2] = l
        args[linha_args][3] = c
        linha_args = linha_args+1

#criando matrizes de resultado
result_soma_thre = np.full((linhas,colunas), 0)
result_soma_proc = np.full((linhas,colunas), 0)
result_mult_thre = np.full((linhas,colunas), 0)
result_mult_proc = np.full((linhas,colunas), 0)
results = [[result_soma_thre], #results[0][0]
           [result_soma_proc], #results[1][0]
           [result_mult_thre], #results[2][0]
           [result_mult_proc]] #results[3][0]

#unroll(args, func, 'proc', results)
unroll(args, func, 'thre', results)
print(matriz_1)
print(matriz_2)
print(results)

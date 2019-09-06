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
    return matResultado
"""    
# deve ser chamada em paralelo
def func(val1, val2, i, j, result):
    result[i][j] = val1 + val2
  
    
#recebe e trata uma matriz
def unroll(args, func, method, results):
    if method == 'proc':
        val = os.fork()
        if val == 0:
            print("Matriz resultado")
            """
            for indice in len(m1[0]):
                linha_m1 = m1[indice]
                coluna_m2 = m2[:, indice]
                
                proc_linha = os.fork()
                if proc_linha == 0:
                    func(linha_m1, coluna_m2)
            """
        else:
            """
            print("Matriz 1")
            for i in m1:
                func(i)
            print()

            print("Matriz 2")
            for i in m2:
                func(i)
            print()            
            """
    else: # method == 'thre'
        for row in args:
            t = threading.Thread(target=func, args=(row[0], row[1], row[2], row[3], results))
            t.start()
        

#construindo matriz args
args = [ [1, 5, 0, 0],
         [2, 6, 0, 1],
         [3, 7, 1, 0],
         [4, 8, 1, 1] ]
#populando matrizes de resultado
matC_unroll = [[0 for i in range(2)] for i in range(2)]
results = [[matC_unroll],
           [matC_unroll],
           [matC_unroll],
           [matC_unroll]]

#unroll(args, func, 'proc', results)
unroll(args, func, 'thre', results)]

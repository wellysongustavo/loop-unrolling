# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import threading


"""-----------------------------------UNROLL E FUNC------------------------------------------"""
"""------------------------------------------------------------------------------------------"""

# É chamada em paralelo
def func(m1, m2, i, j, metodo, op, result):
    if metodo == 'thre':
        if op == 'soma':
            result[0][0][i][j] = m1 + m2

        if op == 'multi':
            for item in range(len(m1)):
                result[2][0][i][j] += m1[item] * m2[item]
        
    if metodo == 'proc':
        if op == 'soma':
            # ERRO
            os.aquire()
            result[1][0][i][j] = m1 + m2
            os.release()
        if op == 'multi':
            # ERRO
            for item in range(len(m1)):
                os.aquire()
                result[3][0][i][j] += m1[item] * m2[item]
                os.release()
    
#recebe e trata uma matriz
def unroll(args, func, method, op, results):
    if method == 'proc':
        for arg in args:
            f = os.fork()
            if f == 0:
                func(arg[0], arg[1], arg[2], arg[3], method, op, results)
            else:
                os.wait()
                
    else: # method == 'thre'
        #soma
        for arg in args:
            t = threading.Thread(target=func, args=(arg[0], arg[1], arg[2], arg[3], method, op, results))
            t.start()
        #multiplicação

"""----------------------------------------GETS----------------------------------------------"""
"""------------------------------------------------------------------------------------------"""

def getColuna(matriz, c):
    coluna = [0 for i in range(len(matriz))]
    
    for l in range(len(matriz[0])):
        coluna[l] = matriz[l][c]
    
    return coluna

def getArgsSoma():
    args = [[0 for i in range(4)] for i in range(dimensao**2)]
    linha_args = 0
    for l in range(dimensao):
        for c in range(dimensao):
            args[linha_args] = [matriz_1[l][c], matriz_2[l][c], l, c]
            linha_args += 1
    return args

def getArgsMultiplicacao():
    args = [[0 for i in range(4)] for i in range(dimensao**2)]
    linha_args = 0
    for l in range(dimensao):
        for c in range(dimensao):
            args[linha_args] = [matriz_1[l], getColuna(matriz_2, c), l, c]
            linha_args += 1
    return args

def getImpressao(matriz, dimensao, texto):
    print(texto)
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matriz]))
    print('\n')

"""------------------------------------MATRIZES----------------------------------------------"""
"""------------------------------------------------------------------------------------------"""
#construindo duas matrizes aleatórias para operar
dimensao = 2
matriz_1 = np.random.randint(10, size=(dimensao,dimensao))
matriz_2 = np.random.randint(10, size=(dimensao,dimensao)) 
#criando matrizes de resultado
result_soma_thre = np.full((dimensao,dimensao), 0)
result_soma_proc = np.full((dimensao,dimensao), 0)
result_mult_thre = np.full((dimensao,dimensao), 0)
result_mult_proc = np.full((dimensao,dimensao), 0)
results = [[result_soma_thre], #results[0][0]
           [result_soma_proc], #results[1][0]
           [result_mult_thre], #results[2][0]
           [result_mult_proc]] #results[3][0]


"""------------------------------CHAMADAS USANDO THREADS-------------------------------------"""
"""------------------------------------------------------------------------------------------"""
# populando args para soma, com os elementos da matriz 1, matriz 2, linhas e colunas
args = getArgsSoma()
#chamando unroll para soma
unroll(args, func, 'thre', 'soma', results)

# populando args para multiplicação, com as linhas e colunas da matriz 1, matriz 2, index das linhas e colunas
args = getArgsMultiplicacao()
#chamando unroll para multiplicar
unroll(args, func, 'thre', 'multi', results)

"""------------------------------CHAMADAS USANDO PROCESSOS-------------------------------------"""
"""------------------------------------------------------------------------------------------"""
unroll(args, func, 'proc', 'soma', results)





"""-----------------------------------IMPRESSÃO----------------------------------------------"""
"""------------------------------------------------------------------------------------------"""
getImpressao(matriz_1, dimensao, "Matriz 1:")
getImpressao(matriz_2, dimensao, "Matriz 2:")
getImpressao(results[0][0], dimensao**2, "Resultado da soma [THREADS]:")
getImpressao(results[2][0], dimensao**2, "Resultado da multiplicação [THREADS]:")
# ^ FUNCIONANDO
"""\/ ERRO"""
getImpressao(results[1][0], dimensao, "Resultado da soma [PROCESSOS]:")
# -*- coding: utf-8 -*-
import timeit
import os, sys
import mmap
import signal
import struct
import posix_ipc
import numpy as np
import threading


"""-----------------------------------UNROLL E FUNC------------------------------------------"""
"""------------------------------------------------------------------------------------------"""

# É chamada em paralelo
def func(m1, m2, i, j, metodo, op, result):
    if metodo == 'thre':
        threading.currentThread()
        if op == 'soma':
            result[0][0][i][j] = m1 + m2

        if op == 'multi':
            for item in range(len(m1)):
                result[1][0][i][j] += m1[item] * m2[item]

    if metodo == 'seq':
        if op == 'soma':
            results[2][0][i][j] += m1 + m2
        if op == 'multi':
            for item in range(len(m1)):
                result[3][0][i][j] += m1[item] * m2[item]

    if metodo == 'proc':
       """
        if op == 'soma':
            # ERRO
            result[1][0][i][j] = m1 + m2
            sem.release()

        if op == 'multi':
            # ERRO
            for item in range(len(m1)):
                #sem.acquire()
                result[3][0][i][j] += m1[item] * m2[item]
                #sem.release()
    """
#recebe e trata uma matriz
def unroll(args, func, method, op, results):
    if method == 'thre' :
        for arg in args:
            t = threading.Thread(target=func, args=(arg[0], arg[1], arg[2], arg[3], method, op, results))
            t.start()

    if method == 'seq':
        for arg in args:
            func(arg[0], arg[1], arg[2], arg[3], method, op, results)

    if method == 'proc':
        """for arg in args:
            f = os.fork()
            if f == 0:
                semaforo.acquire()
                func(arg[0], arg[1], arg[2], arg[3], method, op, results)
                semaforo.release()
                os._exit(0)
            else:
                os.waitpid(f)"""
                
    
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
dimensao = 100
matriz_1 = np.random.randint(10, size=(dimensao,dimensao))
matriz_2 = np.random.randint(10, size=(dimensao,dimensao)) 
#criando matrizes de resultado
result_soma_thre = np.full((dimensao,dimensao), 0)
result_mult_thre = np.full((dimensao,dimensao), 0)
result_soma_seq = np.full((dimensao,dimensao), 0)
result_mult_seq = np.full((dimensao,dimensao), 0)
results = [[result_soma_thre], #results[0][0]
           [result_mult_thre], #results[1][0]
           [result_soma_seq], #results[2][0]
           [result_mult_seq]] #results[3][0]

"""------------------------------CHAMADAS SEQUENCIAIS-------------------------------------"""
"""------------------------------------------------------------------------------------------"""

args = getArgsSoma()

inicio_seq_soma = timeit.default_timer()
unroll(args, func, 'seq', 'soma', results)
fim_seq_soma = timeit.default_timer()
with open('soma_sequencial.txt', 'a') as file:
    file.write(str(fim_seq_soma-inicio_seq_soma)+"\n")

args = getArgsMultiplicacao()

inicio_seq_mult = timeit.default_timer()
unroll(args, func, 'seq', 'multi', results)
fim_seq_mult = timeit.default_timer()
with open('multiplicacao_sequencial.txt', 'a') as file:
    file.write(str(fim_seq_mult-inicio_seq_mult)+"\n")



"""------------------------------CHAMADAS USANDO THREADS-------------------------------------"""
"""------------------------------------------------------------------------------------------"""
# populando args para soma, com os elementos da matriz 1, matriz 2, linhas e colunas
args = getArgsSoma()

#chamando unroll para soma e calculando tempo de função
inicio_thre_soma = timeit.default_timer()
unroll(args, func, 'thre', 'soma', results)
fim_thre_soma = timeit.default_timer()
with open('soma_paralela_thread.txt', 'a') as file:
    file.write(str(fim_thre_soma-inicio_thre_soma)+"\n")

# populando args para multiplicação, com as linhas e colunas da matriz 1, matriz 2, index das linhas e colunas
args = getArgsMultiplicacao()

#chamando unroll para multiplicar
inicio_thre_mult = timeit.default_timer()
unroll(args, func, 'thre', 'multi', results)
fim_thre_mult = timeit.default_timer()
with open('multiplicacao_paralela_thread.txt', 'a') as file:
    file.write(str(fim_thre_mult-inicio_thre_mult)+"\n")

"""------------------------------CHAMADAS USANDO PROCESSOS-------------------------------------"""
"""--------------------------------------------------------------------------------------------"""

"""memory = posix_ipc.SharedMemory("matrix", flags = posix_ipc.O_CREAT, mode = 0o77, size = dimensao**2*24)
mapped_memory = mmap.mmap(memory.fd, memory.size)
memory.close_fd()

semaforo = posix_ipc.Semaphore("sem", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)

args = getArgsSoma()
unroll(args, mapped_memory, "proc", 'soma', results)"""


"""-----------------------------------IMPRESSÃO----------------------------------------------"""
"""------------------------------------------------------------------------------------------"""
getImpressao(matriz_1, dimensao, "Matriz 1:")
getImpressao(matriz_2, dimensao, "Matriz 2:")
getImpressao(results[0][0], dimensao**2, "Resultado da soma [THREADS]:")
getImpressao(results[1][0], dimensao**2, "Resultado da multiplicação [THREADS]:")
getImpressao(results[2][0], dimensao**2, "Resultado da soma [SEQUECIAL]:")
getImpressao(results[3][0], dimensao**2, "Resultado da multiplicação [SEQUECIAL]:")
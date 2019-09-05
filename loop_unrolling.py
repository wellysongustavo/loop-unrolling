# -*- coding: utf-8 -*-
import time
import os
import numpy as np

# deve ser chamada em paralelo
def func(matriz):
    #imprime a soma e a multiplicação ????
    for i in matriz:
        print(i, end="\t")
    print()

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
    

#recebe e trata uma matriz
def unroll(args, func, method, results):
    #criando matrizes randomicamente usando as dimensões recebidas em args
    m1 = np.random.randint(0,9,(args[0][0],args[0][1]))
    m2 = np.random.randint(0,9,(args[1][0],args[1][1]))

    if method == 'proc':
        val = os.fork()

        if val == 0:
            #matriz_multiplicada = multiplica_matriz(m1, m2)
            print("Matriz resultado")
            for indice in len(m1[0]):
                linha_m1 = m1[indice]
                coluna_m2 = m2[:, indice]
                
                proc_linha = os.fork()
                if proc_linha == 0:
                    func(linha_m1, coluna_m2)
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
#armazena os retornos de func
results = []

# envia qtd de linhas e colunas das matrizes

unroll([[2,2],
        [2,2]], func, 'proc', results)
#unroll([[5,3],[1,6]], func, 'proc', results)]

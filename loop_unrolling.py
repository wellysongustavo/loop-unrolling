# -*- coding: utf-8 -*-
import time
import os

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
    mat1 = [[2, 3], [4, 6]]

    if method == 'proc':
        val = os.fork()

        if val == 0:
            matriz_multiplicada = multiplica_matriz(args, mat1)
            print("Matriz resultado")
            for row in matriz_multiplicada:
                #aqui se bota o fork ????
                #results será a matriz resultado ???? se sim, como construir? não é com append
                func(row)
        else:
            print("Matriz args")
            for i in args:
                func(i)
            print()

            print("Matriz auxiliar")
            for i in mat1:
                func(i)
            print()            

#armazena os retornos de func
results = []
#executa a chamada para somar
unroll([[1,2],
        [3,4]], func, 'proc', results)
#unroll([[5,3],[1,6]], func, 'proc', results)]

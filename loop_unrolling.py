# -*- coding: utf-8 -*-
import time
import os

# deve ser chamada em paralelo
def func(elemento1, elemento2):
    #imprime a soma e a multiplicação ????
    print(str(elemento1)+" , "+str(elemento2))
    #esse retorno é algo pra guardar em results, mas o que ?????
    return 1

#recebe e trata uma matriz
def unroll(args, func, method, results):
    if method == 'proc':
        #para cada linha de args é uma chamada de func(elemento1, elemento2)
        for row in args:
            #aqui se bota o fork ????
            #results será a matriz resultado ???? se sim, como construir? não é com append
            results.append(func(row[0], row[1]))

#armazena os retornos de func
results = []

#executa a chamada para somar
unroll([[1,2],[3,4]], func, 'proc', results)
unroll([[5,3],[1,6]], func, 'proc', results)
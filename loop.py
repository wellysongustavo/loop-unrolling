import threading
import posix_ipc
import mmap
import os
import random

"""
========================================================================================
 ######  ########  #######  ##     ## ######## ##    ## ######## ####    ###    ##       
##    ## ##       ##     ## ##     ## ##       ###   ##    ##     ##    ## ##   ##       
##       ##       ##     ## ##     ## ##       ####  ##    ##     ##   ##   ##  ##       
 ######  ######   ##     ## ##     ## ######   ## ## ##    ##     ##  ##     ## ##       
      ## ##       ##  ## ## ##     ## ##       ##  ####    ##     ##  ######### ##       
##    ## ##       ##    ##  ##     ## ##       ##   ###    ##     ##  ##     ## ##       
 ######  ########  ##### ##  #######  ######## ##    ##    ##    #### ##     ## ########
 
========================================================================================
"""

"""
.--------.-------------------------.
| mtxA   | First matrix            |
:--------+-------------------------:
| mtxB   | Second matrix           |
:--------+-------------------------:
| RETURN | Matrix of the summation |
'--------'-------------------------'
"""

def sum_matrix (mtxA, mtxB):
    mtxC = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            mtxC[i][j] = mtxA[i][j] + mtxB[i][j]

    return mtxC

"""
.--------.-----------------------.
| mtxA   | First matrix          |
:--------+-----------------------:
| mtxB   | Second matrix         |
:--------+-----------------------:
| RETURN | Matrix of the product |
'--------'-----------------------'
"""

def prod_matrix (mtxA, mtxB):
    mtxC = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            for k in range(MATRIX_SIZE):
                mtxC[i][j] += mtxA[i][k] * mtxB[k][j]

    return mtxC

"""
===========================================================================
########     ###    ########     ###    ##       ##       ######## ##       
##     ##   ## ##   ##     ##   ## ##   ##       ##       ##       ##       
##     ##  ##   ##  ##     ##  ##   ##  ##       ##       ##       ##       
########  ##     ## ########  ##     ## ##       ##       ######   ##       
##        ######### ##   ##   ######### ##       ##       ##       ##       
##        ##     ## ##    ##  ##     ## ##       ##       ##       ##       
##        ##     ## ##     ## ##     ## ######## ######## ######## ######## 
===========================================================================
"""

"""
.--------.------------------------------------------------.
| val1   | Value of first matrix                          |
:--------+------------------------------------------------:
| val2   | Value of second matrix                         |
:--------+------------------------------------------------:
| i      | Row index                                      |
:--------+------------------------------------------------:
| j      | Column index                                   |
:--------+------------------------------------------------:
| res    | Reference to store the result of the operation |
'--------'------------------------------------------------'
"""

def add_t (val1, val2, i, j, res):
    res[i][j] = val1 + val2

def add_p (val1, val2, i, j, mem):
    res = val1 + val2
    write_to_memory(res, mem, i, j)

"""
.-----.------------------------------------------------.
| row | Row of the first matrix                        |
:-----+------------------------------------------------:
| col | Column of the second matrix                    |
:-----+------------------------------------------------:
| i   | Row index                                      |
:-----+------------------------------------------------:
| j   | Column index                                   |
:-----+------------------------------------------------:
| res | Reference to store the result of the operation |
'-----'------------------------------------------------'
"""

def prod_t (row, col, i, j, res):
    for k in range(len(row)):
        res[i][j] += row[k] * col[k]

def prod_p (row, col, i, j, mem):
    for k in range(len(row)):        
        curVal = read_from_memory(mem, i, j)
        newVal = curVal + row[k] * col[k]
        write_to_memory(newVal, mem, i, j)

"""
========================================================
##     ## ##    ## ########   #######  ##       ##       
##     ## ###   ## ##     ## ##     ## ##       ##       
##     ## ####  ## ##     ## ##     ## ##       ##       
##     ## ## ## ## ########  ##     ## ##       ##       
##     ## ##  #### ##   ##   ##     ## ##       ##       
##     ## ##   ### ##    ##  ##     ## ##       ##       
 #######  ##    ## ##     ##  #######  ######## ######## 
========================================================
"""

def unroll (args, func, results, method="process"):
    if method == "process":
        children = []
        for i in range(len(args)):
            child = os.fork()

            if child == 0:
                func(*args[i], results)
                os._exit(0)
            else:
                children.append(child)

        for child in children:
            os.waitpid(child, 0)
            
    else:
        for i in range(len(args)):
            arg = args[i]
            th = threading.Thread(target=func, args=(*arg, results))
            th.start()

"""
=======================================================
##     ## ######## #### ##       #### ######## ##    ## 
##     ##    ##     ##  ##        ##     ##     ##  ##  
##     ##    ##     ##  ##        ##     ##      ####   
##     ##    ##     ##  ##        ##     ##       ##    
##     ##    ##     ##  ##        ##     ##       ##    
##     ##    ##     ##  ##        ##     ##       ##    
 #######     ##    #### ######## ####    ##       ##    
=======================================================
"""

"""
.--------.--------------------------------------.
| mtx    | Origin matrix                        |
:--------+--------------------------------------:
| j      | Desired column                       |
:--------+--------------------------------------:
| RETURN | List with all values from the column |
'--------'--------------------------------------'
"""

def get_column (mtx, j):
    col = [0 for i in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        col[i] = mtx[i][j]

    return col


"""
.--------.--------------------------------.
| n      | Dimension of the square matrix |
:--------+--------------------------------:
| max    | Limit for the values           |
:--------+--------------------------------:
| RETURN | Matrix with random numbers     |
'--------'--------------------------------'
"""

def random_matrix (n, max):
    mtx = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            mtx[i][j] = random.randint(0, max)

    return mtx

"""
.--------.-----------------------------------------.
| mtxA   | First matrix                            |
:--------+-----------------------------------------:
| mtxB   | Second matrix                           |
:--------+-----------------------------------------:
| RETURN | Unroll compatible matrix with arguments |
'--------'-----------------------------------------'
"""

def generate_add_args (mtxA, mtxB):
    args = [[0 for i in range(4)] for i in range(MATRIX_SIZE * MATRIX_SIZE)]

    k = 0
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            args[k] = [mtxA[i][j], mtxB[i][j], i, j]
            k += 1

    return args

"""
.--------.-----------------------------------------.
| mtxA   | First matrix                            |
:--------+-----------------------------------------:
| mtxB   | Second matrix                           |
:--------+-----------------------------------------:
| RETURN | Unroll compatible matrix with arguments |
'--------'-----------------------------------------'
"""

def generate_prod_args (mtxA, mtxB):
    args = [[0 for i in range(4)] for i in range(MATRIX_SIZE * MATRIX_SIZE)]

    k = 0
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            args[k] = [mtxA[i], get_column(mtxB, j), i, j]
            k += 1

    return args

"""
.-------.----------------------.
| mtx   | Matrix to be printed |
:-------+----------------------:
| PRINT | Stylized matrix      |
'-------'----------------------'
"""

def print_matrix (mtx):
    print('|\t', end='')
    print('\t|\n|\t'.join(['\t'.join([str(cell) for cell in row]) for row in mtx]), end='')
    print('\t|')

def get_matrix (mem):
    mtx = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            mtx[i][j] = read_from_memory(mem, i, j)

    return mtx

"""
.-----.---------------------.
| val | Value to be written |
:-----+---------------------:
| mem | Mapped memory       |
:-----+---------------------:
| i   | Row index           |
:-----+---------------------:
| j   | Column index        |
'-----'---------------------'
"""

def write_to_memory (val, mem, i, j):
    k = (i * MATRIX_SIZE + j) * 24

    mem.seek(k)
    semaphore.acquire()
    mem.write(val.to_bytes(24, byteorder='big'))
    semaphore.release()

"""
.--------.------------------------------.
| mem    | Mapped memory                |
:--------+------------------------------:
| i      | Row index                    |
:--------+------------------------------:
| j      | Column index                 |
:--------+------------------------------:
| RETURN | Value store in mapped memory |
'--------'------------------------------'
"""

def read_from_memory (mem, i, j):
    k = (i * MATRIX_SIZE + j) * 24

    mem.seek(k)
    semaphore.acquire()
    val_bytes = mem.read(24)
    semaphore.release()
    val = int.from_bytes(val_bytes, byteorder='big')

    return val

"""
=================================
##     ##    ###    #### ##    ## 
###   ###   ## ##    ##  ###   ## 
#### ####  ##   ##   ##  ####  ## 
## ### ## ##     ##  ##  ## ## ## 
##     ## #########  ##  ##  #### 
##     ## ##     ##  ##  ##   ### 
##     ## ##     ## #### ##    ## 
=================================                                          
"""

# GENERATE TWO RANDOM MATRICES
MATRIX_SIZE = 3
MAX_VALUE = 10

matA = random_matrix(MATRIX_SIZE, MAX_VALUE)
matB = random_matrix(MATRIX_SIZE, MAX_VALUE)

# PRINT BOTH INITIAL MATRICES
print("""
 __    __     ______     ______   ______     __     __  __        ______    
/\ "-./  \   /\  __ \   /\__  _\ /\  == \   /\ \   /\_\_\_\      /\  __ \   
\ \ \-./\ \  \ \  __ \  \/_/\ \/ \ \  __<   \ \ \  \/_/\_\/_     \ \  __ \  
 \ \_\ \ \_\  \ \_\ \_\    \ \_\  \ \_\ \_\  \ \_\   /\_\/\_\     \ \_\ \_\ 
  \/_/  \/_/   \/_/\/_/     \/_/   \/_/ /_/   \/_/   \/_/\/_/      \/_/\/_/                                                                             
""")
print_matrix(matA)

print("""
 __    __     ______     ______   ______     __     __  __        ______    
/\ "-./  \   /\  __ \   /\__  _\ /\  == \   /\ \   /\_\_\_\      /\  == \   
\ \ \-./\ \  \ \  __ \  \/_/\ \/ \ \  __<   \ \ \  \/_/\_\/_     \ \  __<   
 \ \_\ \ \_\  \ \_\ \_\    \ \_\  \ \_\ \_\  \ \_\   /\_\/\_\     \ \_____\ 
  \/_/  \/_/   \/_/\/_/     \/_/   \/_/ /_/   \/_/   \/_/\/_/      \/_____/                                                                             
""")
print_matrix(matB)

print(""" 
  _____    _____     ____     _____   ______    _____    _____ 
 |  __ \  |  __ \   / __ \   / ____| |  ____|  / ____|  / ____|
 | |__) | | |__) | | |  | | | |      | |__    | (___   | (___  
 |  ___/  |  _  /  | |  | | | |      |  __|    \___ \   \___ \ 
 | |      | | \ \  | |__| | | |____  | |____   ____) |  ____) |
 |_|      |_|  \_\  \____/   \_____| |______| |_____/  |_____/ 
""")

# CREATE AND INITIALIZE SHARED MEMORY

shm_size = MATRIX_SIZE * MATRIX_SIZE * 24
memory = posix_ipc.SharedMemory("matrix", flags = posix_ipc.O_CREAT, mode = 0o77, size = shm_size)
mapped_memory = mmap.mmap(memory.fd, memory.size)
memory.close_fd()

semaphore = posix_ipc.Semaphore("test_sem", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)

mapped_memory.seek(0)
for k in range(MATRIX_SIZE * MATRIX_SIZE):
    mapped_memory.write(int(0).to_bytes(24, byteorder='big'))

args = generate_add_args(matA, matB)
unroll(args, add_p, mapped_memory, "process")

print("""
 ______     _____     _____     __     ______   __     ______     __   __    
/\  __ \   /\  __-.  /\  __-.  /\ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   
\ \  __ \  \ \ \/\ \ \ \ \/\ \ \ \ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  
 \ \_\ \_\  \ \____-  \ \____-  \ \_\    \ \_\  \ \_\  \ \_____\  \ \_\ \ _\ 
  \/_/\/_/   \/____/   \/____/   \/_/     \/_/   \/_/   \/_____/   \/_/ \/_/ 
""")

matC = get_matrix(mapped_memory)
print_matrix(matC)

print("""
 ______   ______     ______     _____     __  __     ______     ______  
/\  == \ /\  == \   /\  __ \   /\  __-.  /\ \/\ \   /\  ___\   /\__  _\ 
\ \  _-/ \ \  __<   \ \ \/\ \  \ \ \/\ \ \ \ \_\ \  \ \ \____  \/_/\ \/ 
 \ \_\    \ \_\ \_\  \ \_____\  \ \____-  \ \_____\  \ \_____\    \ \_\ 
  \/_/     \/_/ /_/   \/_____/   \/____/   \/_____/   \/_____/     \/_/ 
""")

mapped_memory.seek(0)
for k in range(MATRIX_SIZE * MATRIX_SIZE):
    mapped_memory.write(int(0).to_bytes(24, byteorder='big'))

args = generate_prod_args(matA, matB)
unroll(args, prod_p, mapped_memory)

matC = get_matrix(mapped_memory)
print_matrix(matC)



print(""" 
  _______   _    _   _____    ______              _____  
 |__   __| | |  | | |  __ \  |  ____|     /\     |  __ \ 
    | |    | |__| | | |__) | | |__       /  \    | |  | |
    | |    |  __  | |  _  /  |  __|     / /\ \   | |  | |
    | |    | |  | | | | \ \  | |____   / ____ \  | |__| |
    |_|    |_|  |_| |_|  \_\ |______| /_/    \_\ |_____/ 
""")

print("""
 ______     _____     _____     __     ______   __     ______     __   __    
/\  __ \   /\  __-.  /\  __-.  /\ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   
\ \  __ \  \ \ \/\ \ \ \ \/\ \ \ \ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  
 \ \_\ \_\  \ \____-  \ \____-  \ \_\    \ \_\  \ \_\  \ \_____\  \ \_\ \ _\ 
  \/_/\/_/   \/____/   \/____/   \/_/     \/_/   \/_/   \/_____/   \/_/ \/_/ 
""")

matC = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]
args = generate_add_args(matA, matB)
unroll(args, add_t, matC, "thread")
print_matrix(matC)

print("""
 ______   ______     ______     _____     __  __     ______     ______  
/\  == \ /\  == \   /\  __ \   /\  __-.  /\ \/\ \   /\  ___\   /\__  _\ 
\ \  _-/ \ \  __<   \ \ \/\ \  \ \ \/\ \ \ \ \_\ \  \ \ \____  \/_/\ \/ 
 \ \_\    \ \_\ \_\  \ \_____\  \ \____-  \ \_____\  \ \_____\    \ \_\ 
  \/_/     \/_/ /_/   \/_____/   \/____/   \/_____/   \/_____/     \/_/ 
""")

matC = [[0 for i in range(MATRIX_SIZE)] for i in range(MATRIX_SIZE)]
args = generate_prod_args(matA, matB)
unroll(args, prod_t, matC, "thread")
print_matrix(matC)
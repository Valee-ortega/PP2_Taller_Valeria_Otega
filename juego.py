import random 

"""
N: crear_matriz_vacia
D: crea una matriz cuadrada de n x n llena de ceros
E: n (int) - tamaño de la matriz
S: list - matriz de n x n con todos los elementos en 0
R: n debe ser mayor a 0
"""
def crear_matriz_vacia(n):
    if n == 0:
        return 'El número no puede ser cero'
    else:
        matriz= []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(0)
            matriz.append(fila)
        return matriz

"""
N: colocar_minas
D: coloca minas (-1) en posiciones aleatorias de la matriz
E: matriz, cantidad_minas
S: list - matriz con las minas colocadas (-1)
R: cantidad_minas debe ser menor o igual a n*n
"""

def colocar_minas(matriz, cantidad_minas):
    n = len(matriz)
    minas_colocadas = 0

    while minas_colocadas < cantidad_minas: # mientras que no hayan mas que el largo de la matriz
        fila = random.randint(0, n-1)
        columna = random.randint(0, n-1)

        if matriz[fila][columna] != -1: # si no hay minas
            matriz[fila][columna] = -1 # la colocamos
            minas_colocadas += 1 
    return matriz 



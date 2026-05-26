import random 

"""
N: crear_matriz_vacia
D: crea una matriz cuadrada de n x n llena de ceros
E: tamaño de la matriz
S: matriz de n x n con todos los elementos en 0
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

"""
    N: calcular_vecinos
    D: calcula cuántas minas hay alrededor de cada celda
    E: matriz con minas y ceros
    S: misma matriz donde los ceros se convierten en números 1..8
    R: las minas ya deben estar colocadas (-1)
    """

def calcular_vecinos(tablero_con_minas):
    
    tamaño = len(tablero_con_minas)
    
    for fila in range(tamaño):
        for columna in range(tamaño):
            
            # si es mina, la saltamos
            if tablero_con_minas[fila][columna] == -1:
                continue
            
            # contador de minas alrededor
            contador = 0
            
            # REVISAR CADA UNO DE LOS 8 VECINOS
            
            # vecino arriba-izquierda
            if fila - 1 >= 0 and columna - 1 >= 0:
                if tablero_con_minas[fila - 1][columna - 1] == -1:
                    contador = contador + 1
            
            # vecino arriba
            if fila - 1 >= 0:
                if tablero_con_minas[fila - 1][columna] == -1:
                    contador = contador + 1
            
            # vecino arriba-derecha
            if fila - 1 >= 0 and columna + 1 < tamaño:
                if tablero_con_minas[fila - 1][columna + 1] == -1:
                    contador = contador + 1
            
            # vecino izquierda
            if columna - 1 >= 0:
                if tablero_con_minas[fila][columna - 1] == -1:
                    contador = contador + 1
            
            # vecino derecha
            if columna + 1 < tamaño:
                if tablero_con_minas[fila][columna + 1] == -1:
                    contador = contador + 1
            
            # vecino abajo-izquierda
            if fila + 1 < tamaño and columna - 1 >= 0:
                if tablero_con_minas[fila + 1][columna - 1] == -1:
                    contador = contador + 1
            
            # vecino abajo
            if fila + 1 < tamaño:
                if tablero_con_minas[fila + 1][columna] == -1:
                    contador = contador + 1
            
            # vecino abajo-derecha
            if fila + 1 < tamaño and columna + 1 < tamaño:
                if tablero_con_minas[fila + 1][columna + 1] == -1:
                    contador = contador + 1
            
            # guardar el resultado en la celda
            if contador > 0:
                tablero_con_minas[fila][columna] = contador
    
    return tablero_con_minas

"""
N: inicializar_tablero_completo
D: crea y devuelve el tablero lógico completo (minas y numeros)
E: n, cantidad de minas
S: matriz n x n lista para jugar
R: total_minas debe ser menor a n*n
"""
def inicializar_tablero_completo(n, total_minas):
    tablero = crear_matriz_vacia(n)
    tablero = colocar_minas(tablero, total_minas)
    tablero = calcular_vecinos(tablero)
    return tablero

"""
N: inicializar_tablero_visible
D: crea el tablero de visibilidad con todo oculto
E: n - tamaño del tablero
S: matriz n x n llena de 0 (todo oculto)
R: n debe ser mayor a 0
"""
def inicializar_tablero_visible(n):
    return crear_matriz_vacia(n)


"""
N: revelar_celda
D: revela una celda. si es 0, revela recursivamente sus vecinos (efecto cascada)
E: tablero_logico, tablero_visible, fila, columna
S: True si sigue vivo, False si exploto
R: las coordenadas deben ser validas
"""
def revelar_celda(tablero_logico, tablero_visible, fila, columna):
    tamaño = len(tablero_logico)
    
    # validar limites del tablero
    if fila < 0 or fila >= tamaño or columna < 0 or columna >= tamaño:
        return True
    
    # si ya esta revelada o tiene bandera, no hacer nada
    if tablero_visible[fila][columna] != 0:
        return True
    
    # si es mina, game over
    if tablero_logico[fila][columna] == -1:
        tablero_visible[fila][columna] = 1
        return False
    
    # revelar la celda actual
    tablero_visible[fila][columna] = 1
    
    # si es 0 (celda vacia), revelar recursivamente los vecinos (efecto cascada)
    if tablero_logico[fila][columna] == 0:
        # revisar los 8 vecinos
        
        # arriba-izquierda
        revelar_celda(tablero_logico, tablero_visible, fila - 1, columna - 1)
        # arriba
        revelar_celda(tablero_logico, tablero_visible, fila - 1, columna)
        # arriba-derecha
        revelar_celda(tablero_logico, tablero_visible, fila - 1, columna + 1)
        # izquierda
        revelar_celda(tablero_logico, tablero_visible, fila, columna - 1)
        # derecha
        revelar_celda(tablero_logico, tablero_visible, fila, columna + 1)
        # abajo-izquierda
        revelar_celda(tablero_logico, tablero_visible, fila + 1, columna - 1)
        # abajo
        revelar_celda(tablero_logico, tablero_visible, fila + 1, columna)
        # abajo-derecha
        revelar_celda(tablero_logico, tablero_visible, fila + 1, columna + 1)
    
    return True


"""
N: colocar_bandera
D: coloca o quita una bandera en una celda oculta
E: tablero_visible, fila, columna
S: nuevo estado de la celda (0=oculta, 2=bandera)
R: solo se puede poner o quitar bandera si la celda esta oculta (0) o tiene bandera (2)
"""
def colocar_bandera(tablero_visible, fila, columna):
    if tablero_visible[fila][columna] == 0:
        tablero_visible[fila][columna] = 2      # poner bandera
    elif tablero_visible[fila][columna] == 2:
        tablero_visible[fila][columna] = 0      # quitar bandera
    
    return tablero_visible[fila][columna]

"""
N: contar_minas_restantes
D: calcula minas totales menos banderas colocadas
E: tablero_visible, total_minas
S: minas restantes
R: ninguna
"""
def contar_minas_restantes(tablero_visible, total_minas):
    banderas = 0
    tamaño = len(tablero_visible)
    for i in range(tamaño):
        for j in range(tamaño):
            if tablero_visible[i][j] == 2:
                banderas = banderas + 1
    return total_minas - banderas


"""
N: contar_celdas_reveladas
D: cuenta cuántas celdas están reveladas (estado 1)
E: tablero_visible
S: número de celdas reveladas
R: ninguna
"""
def contar_celdas_reveladas(tablero_visible):
    reveladas = 0
    tamaño = len(tablero_visible)
    for i in range(tamaño):
        for j in range(tamaño):
            if tablero_visible[i][j] == 1:
                reveladas = reveladas + 1
    return reveladas


"""
N: contar_banderas_colocadas
D: cuenta cuantas banderas hay en el tablero
E: tablero_visible
S: número de banderas
R: ninguna
"""
def contar_banderas_colocadas(tablero_visible):
    banderas = 0
    tamaño = len(tablero_visible)
    for i in range(tamaño):
        for j in range(tamaño):
            if tablero_visible[i][j] == 2:
                banderas = banderas + 1
    return banderas

"""
N: verificar_victoria
D: verifica si el jugador ha ganado (todas las celdas que no son mina están reveladas)
E: tablero_logico, tablero_visible 
S: True si ganó, False si no
R: ninguna
"""
def verificar_victoria(tablero_logico, tablero_visible):
    tamaño = len(tablero_logico)
    for i in range(tamaño):
        for j in range(tamaño):
            # si no es mina y no está revelada, todavía no ganó
            if tablero_logico[i][j] != -1:
                if tablero_visible[i][j] != 1:
                    return False
    return True


"""
N: mostrar_todas_minas
D: revela todas las minas del tablero (cuando el jugador pierde)
E: tablero_logico, tablero_visible
S: None (modifica tablero_visible)
R: ninguna
"""
def mostrar_todas_minas(tablero_logico, tablero_visible):
    tamaño = len(tablero_logico)
    for i in range(tamaño):
        for j in range(tamaño):
            if tablero_logico[i][j] == -1:
                tablero_visible[i][j] = 1


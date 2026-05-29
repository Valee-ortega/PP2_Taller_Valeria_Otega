"""
N: guardar_partida
D: guarda una partida ganada en el archivo ranking.txt
E: nombre, dificultad, tiempo,celdas reveladas, movimientos
S: True si se guardó correctamente, False si hubo error
R: el nombre no puede estar vacío, tiempo debe ser mayor a 0
"""
def guardar_partida(nombre, dificultad, tiempo, reveladas, movimientos):
    
    # VALIDACIONES
    # validar que el nombre no esté vacío
    if nombre == "":
        return False
    
    # validar que el nombre no sea solo espacios
    if nombre.strip() == "":
        return False
    
    if tiempo <= 0:
        return False
    
    if reveladas < 0:
        return False
    
    if movimientos < 0:
        return False
    
    try:
        # abrir archivo en modo "agregar" 
        # si el archivo no existe, python lo crea automatico
        archivo = open("ranking.txt", "a")
        
        # crear la línea con los datos separados por comas
        linea = f"{nombre},{dificultad},{tiempo},{reveladas},{movimientos}\n"
        
        archivo.write(linea)
        
        # cerrar el archivo, para guardar los cambios
        archivo.close()
        
        # devolver True para indicar que todo salió bien
        return True
        
    except:
        # si ocurre algún error, devolvemos False para indicar que falló
        return False

"""
N: cargar_todas_partidas
D: carga todas las partidas guardadas en el archivo ranking.txt
E: ninguna
S: lista de tuplas (nombre, dificultad, tiempo, reveladas, movimientos)
R: si el archivo no existe, devuelve lista vacía
"""
def cargar_todas_partidas():
    
    # lista para guardar las partidas
    partidas = []
    
    try:
        # intentar abrir el archivo en modo lectura
        archivo = open("ranking.txt", "r")
        
        # leer todas las líneas del archivo
        lineas = archivo.readlines()
        
        # cerrar el archivo después de leer
        archivo.close()
        
        for linea in lineas:
            # eliminar espacios y saltos de línea al inicio y final
            linea = linea.strip()

            # si la línea no está vacía
            if linea != "":
                datos = linea.split(",") 

                if len(datos) == 5:
                    nombre = datos[0]           
                    dificultad = datos[1]       
                    tiempo = int(datos[2]) # convertir a entero
                    reveladas = int(datos[3])  
                    movimientos = int(datos[4])
                    
                    # crear una tupla con los 5 datos y agregarla a la lista
                    # tupla porque no hay que modificarla despues
                    partidas.append((nombre, dificultad, tiempo, reveladas, movimientos))
    
    except FileNotFoundError:
        # no hace nada, simplemente devuelve list vacia
        pass
        
    except:
        # cualquier otro error devolver lista vacia 
        pass

    return partidas

"""
N: encontrar_menor
D: encuentra la partida con el menor tiempo en una lista
E: lista de partidas (cada partida es una tupla)
   (nombre, dificultad, tiempo, reveladas, movimientos)
S: la partida con el menor tiempo
R: la lista no debe estar vacía 
"""
def encontrar_menor(lista):
    menor = lista[0]
    for partida in lista:
        if partida[2] < menor[2]:
            menor = partida
    return menor

"""
N: eliminar
D: elimina un elemento especifico de una lista
E: lista original, elemento a eliminar
S: nueva lista sin el elemento eliminado
R: ninguna
"""

def eliminar(lista, elemento):
    nueva = []
    for x in lista:
        if x != elemento:
            nueva.append(x)
    return nueva

"""
N: obtener_top_10
D: obtiene las 10 mejores partidas de una dificultad
E: dificultad: "Facil", "Medio" o "Dificil"
S: lista con las 10 mejores partidas
R: ninguna
"""

def obtener_top_10(dificultad):

    # validar que la dificultad sea correcta
    if dificultad not in ["Facil", "Medio", "Dificil"]:
        return []

    # cargar y filtrar  segfun la dificultad 
    todas = cargar_todas_partidas()
    filtradas = [ ]
    for partida in todas:
        if partida[1] == dificultad:
            filtradas.append(partida)

    top_10 = [ ] # lista para guardar el top

    # para hacer una copia de la lista
    restantes = filtradas[:] # sin inicio ni fin para que copie todo 

    while len(top_10) < 10 and len(restantes) > 0:

        # agregar la de menor tiempo
        menor = encontrar_menor(restantes) 
        top_10.append(menor) 
        
        # eliminarla de la lista, para volver a evaluar y seguir sacando los otros menores
        restantes = eliminar(restantes, menor)

    return top_10


"""
N: es_mejor_tiempo
D: verifica si un tiempo está dentro del top 10 de una dificultad
E: dificultad, tiempo
S: True si el tiempo es mejor que el peor del top 10 (o si hay menos de 10)
R: tiempo debe ser mayor a 0
"""
def es_mejor_tiempo(dificultad, tiempo):
    
    if tiempo <= 0:
        return False
    
    top_10 = obtener_top_10(dificultad)
    
    # si hay menos de 10, cualquier tiempo entra
    if len(top_10) < 10:
        return True
    
    # el peor tiempo es el ultimo (indice 9)
    peor_tiempo = top_10[9][2]  # [9] es la posición 10, [2] es el tiempo
    return tiempo < peor_tiempo


"""
N: agregar_si_es_record
D: agrega una partida al ranking SOLO si es mejor que el peor del top 10
E: nombre, dificultad, tiempo, reveladas, movimientos
S: True si se agrego, False si no entro al top 10
R: nombre no puede estar vacio, tiempo debe ser mayor a 0
"""
def agregar_si_es_record(nombre, dificultad, tiempo, reveladas, movimientos):
    
    # validaciones
    if nombre == "" or nombre.strip() == "":
        return False
    if tiempo <= 0:
        return False
    
    # verificar si debe estar en el ranking
    if es_mejor_tiempo(dificultad, tiempo):
        guardar_partida(nombre, dificultad, tiempo, reveladas, movimientos)
        return True
    else:
        return False

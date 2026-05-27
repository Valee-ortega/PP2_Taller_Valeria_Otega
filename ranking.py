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
        
        # escribir la línea en el archivo
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
E: None
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


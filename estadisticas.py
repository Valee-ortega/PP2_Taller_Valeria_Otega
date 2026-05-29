import tkinter as tk
from tkinter import messagebox, simpledialog


"""
N: formatear_tiempo
D: convierte segundos a formato MM:SS
E: segundos
S: tiempo formateado
R: segundos debe ser >= 0
"""
def formatear_tiempo(segundos):
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos}:{segs:02d}"

"""
N: mostrar_estadisticas
D: muestra un messagebox con las estadísticas de la partida
E: nombre (str), dificultad (str), modo (str), tiempo (int),
   reveladas (int), banderas (int), resultado (str)
S: ninguna
R: ninguna
"""
def mostrar_estadisticas(nombre, dificultad, modo, tiempo, reveladas, banderas, resultado):
    
    tiempo_formateado = formatear_tiempo(tiempo)
    
    if nombre == "":
        nombre = "---"
    
    # crear el texto del mensaje
    mensaje = f"""
=====================================
     ESTADÍSTICAS DE LA PARTIDA
=====================================

Jugador:           {nombre}
Dificultad:        {dificultad}
Modo:              {modo}
Tiempo invertido o restante:  {tiempo_formateado}
Celdas reveladas:  {reveladas}
Banderas:          {banderas}
Resultado:         {resultado}

=====================================
"""
    
    # mostrar ventana con el mensaje
    messagebox.showinfo("Estadísticas de la partida", mensaje)


"""
N: pedir_nombre
D: pide el nombre al jugador cuando gana
E: ventana_padre (tk.Toplevel)
S: str - nombre del jugador
R: ninguna
"""
def pedir_nombre(ventana_padre):
    nombre = simpledialog.askstring("¡Victoria!", "¡Felicidades! Has ganado 🎉\n\nIngrese su nombre:", parent=ventana_padre)
    
    if nombre is None or nombre.strip() == "":
        nombre = "Anónimo"
    
    return nombre

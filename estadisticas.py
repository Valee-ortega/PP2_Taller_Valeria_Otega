import tkinter as tk
from tkinter import messagebox
from ranking import obtener_top_10

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
D: pide el nombre al jugador usando una ventana con Entry
E: ventana_padre (tk.Toplevel)
S: nombre del jugador
R: ninguna
"""
def pedir_nombre(ventana_padre):
    nombre = "Anónimo"  # valor por defecto
    
    # crear ventana para pedir nombre
    ventana_nombre = tk.Toplevel(ventana_padre)
    ventana_nombre.title("¡Victoria!")
    ventana_nombre.geometry("300x150")
    ventana_nombre.resizable(False, False)
    
    # hacer que la ventana sea modal (no se puede clickear la de atrás)
    ventana_nombre.transient(ventana_padre)
    ventana_nombre.grab_set()
    
    # mensaje de felicitación
    lbl_felicidades = tk.Label(ventana_nombre, text="¡Felicidades! Has ganado 🎉", font=("Arial", 12, "bold"))
    lbl_felicidades.pack(pady=10)
    
    # etiqueta y campo para ingresar nombre
    lbl_nombre = tk.Label(ventana_nombre, text="Ingrese su nombre:", font=("Arial", 10))
    lbl_nombre.pack()
    
    entry_nombre = tk.Entry(ventana_nombre, width=20)
    entry_nombre.pack(pady=5)
    entry_nombre.focus()  # poner el cursor aqui automaticamente
    
    # variable para guardar el resultado
    resultado = ["Anónimo"]  # lista mutable
    
    def guardar():
        nombre_ingresado = entry_nombre.get().strip()
        if nombre_ingresado != "":
            resultado[0] = nombre_ingresado
        ventana_nombre.destroy()
    
    # boton guardar
    btn_guardar = tk.Button(ventana_nombre, text="Guardar", width=10, command=guardar)
    btn_guardar.pack(pady=10)
    
    # permitir presionar Enter para guardar
    def on_enter(event):
        guardar()
    
    entry_nombre.bind("<Return>", on_enter)
    
    # esperar a que se cierre la ventana
    ventana_nombre.wait_window()
    
    return resultado[0]

"""
N: mostrar_ranking
D: muestra el top 10 de una dificultad en un messagebox
E: dificultad 
S: ninguna
R: ninguna
"""

def mostrar_ranking(dificultad):

    top_10 = obtener_top_10(dificultad)
    
    if not top_10:
        mensaje = f"No hay partidas guardadas en {dificultad}"
    else:
        # construir el mensaje
        mensaje = f"=== RANKING {dificultad} ===\n\n"
        
        for i, partida in enumerate(top_10, start=1):
            nombre = partida[0]
            tiempo = partida[2]
            reveladas = partida[3]
            movimientos = partida[4]
            
            minutos = tiempo // 60
            segs = tiempo % 60
            tiempo_str = f"{minutos}:{segs:02d}"
            
            mensaje += f"{i}. Nombre: {nombre} - Tiempo: {tiempo_str} - {reveladas} celdas reveladas - {movimientos} movimientos\n"
        
    messagebox.showinfo(f"Ranking {dificultad}", mensaje)

"""
N: mostrar_menu_ranking
D: muestra un menú para elegir qué ranking ver
E: ventana_padre (tk.Toplevel)
S: ninguna
R: ninguna
"""
def mostrar_menu_ranking(ventana_padre):
    
    ventana_menu = tk.Toplevel(ventana_padre)
    ventana_menu.title("Ver Ranking")
    ventana_menu.geometry("250x180")
    ventana_menu.resizable(False, False)
    
    lbl_titulo = tk.Label(ventana_menu, text="Seleccione dificultad:", font=("Arial", 12))
    lbl_titulo.pack(pady=15)
    
    btn_facil = tk.Button(ventana_menu, text="Fácil", width=15, command=lambda: [ventana_menu.destroy(), mostrar_ranking("Facil")])
    btn_facil.pack(pady=5)
    
    btn_medio = tk.Button(ventana_menu, text="Medio", width=15, command=lambda: [ventana_menu.destroy(), mostrar_ranking("Medio")])
    btn_medio.pack(pady=5)
    
    btn_dificil = tk.Button(ventana_menu, text="Difícil", width=15, command=lambda: [ventana_menu.destroy(), mostrar_ranking("Dificil")])
    btn_dificil.pack(pady=5)
    
    btn_cerrar = tk.Button(ventana_menu, text="Cerrar", width=10, command=ventana_menu.destroy)
    btn_cerrar.pack(pady=15)
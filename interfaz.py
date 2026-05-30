import tkinter as tk
from tkinter import messagebox # para mostrar mensajes emergentes (flotantes)
from juego import inicializar_tablero_completo, inicializar_tablero_visible, revelar_celda, colocar_bandera, verificar_victoria, contar_minas_restantes, contar_celdas_reveladas, contar_banderas_colocadas, mostrar_todas_minas
from estadisticas import mostrar_estadisticas, pedir_nombre, mostrar_menu_ranking
from ranking import agregar_si_es_record

# variable global para la ventana principal
ventana = None 

"""
N: mostrar_ventana_inicial
D: crea y muestra la ventana principal del juego con 3 botones
E: ninguna
S: ninguna
R: ninguna
"""
def mostrar_ventana_inicial():
    global ventana

    if ventana is None or not ventana.winfo_exists(): # si la ventana no existe o si existe pero fue destruida
        ventana = tk.Tk()
    else:
        ventana.deiconify() # muestra la ventana nuevamente
        return
    
    # title() pone el texto en la barra de titulo de la ventana
    ventana.title("Buscaminas")
    
    # geometry() define el tamaño: ancho x alto en píxeles
    ventana.geometry("600x600")
    
    # no permite redimencionar ancho ni alto
    ventana.resizable(False, False)
    
    # boton 1: NUEVA PARTIDA
    
    # Button() crea un boton
    # - la ventana donde va el boton
    # - el texto que se muestra en el boton
    # - ancho del boton
    # - alto del boton 
    boton_nueva = tk.Button(ventana, text="Nueva Partida", width=20,height=2,command=mostrar_configuracion)
    
    # pack() coloca el boton en la ventana
    # pady = margen de píxeles arriba y abajo (espacio entre botones)
    boton_nueva.pack(pady=50)

    # boton 2: VER RANKING
    boton_ranking = tk.Button(ventana,text="Ver Ranking",width=20,height=2, command=lambda: mostrar_menu_ranking(ventana) )
    boton_ranking.pack(pady=50)
     
    # botón 3: SALIR
    boton_salir = tk.Button(ventana, text="Salir", width=20, height=2, command=ventana.quit)
    boton_salir.pack(pady=50)
    
    # iniciar la ventana (bucle principal)
    # mainloop() mantiene la ventana abierta, bbucle infinito que espera acciones del usuario
    ventana.mainloop()

"""
N: mostrar_configuracion
D: crea y muestra la ventana para elegir dificultad y modo de juego
E: ninguns
S: ninguna
R: ninguna
"""
def mostrar_configuracion():

    # Toplevel() crea una ventana SECUNDARIA
    # no cierra la ventana principal, se abre encima
    ventana_config = tk.Toplevel()
    
    # titulo de la ventana
    ventana_config.title("Configuración de la partida")
    ventana_config.geometry("400x350") # tamaño de la ventana
    
    ventana_config.resizable(False, False) 

    # ===========
    # DIFICULTAD
   
    # Label es un texto que se muestra en la ventana
    # font define el tipo y tamaño de letra
    lbl_dificultad = tk.Label( ventana_config, text="Seleccione dificultad:", font=("Arial", 12) )
    lbl_dificultad.pack(pady=20)
    
    # variable para guardar la dificultad elegido
    dificultad_elegida = tk.StringVar(value="Facil")
    
    # Radiobutton: botones circulares donde solo UNO puede estar seleccionado
    # variable=dificultad_elegida: todos comparten la misma variable
    # value="Facil": este boton guarda "Facil" en la variable cuando se selecciona opción: Fácil
    radio_facil = tk.Radiobutton( ventana_config, text="Fácil (8x8, 10 minas)", variable=dificultad_elegida, value="Facil")
    
    # anchor="w": alinear a la izquierda (west)
    # padx=30: margen izquierdo de 30 píxeles
    radio_facil.pack(anchor="w", padx=30)
    
    # opción: Medio
    radio_medio = tk.Radiobutton( ventana_config, text="Medio (12x12, 25 minas)", variable=dificultad_elegida, value="Medio")
    radio_medio.pack(anchor="w", padx=30)
    
    # opción: Difícil
    radio_dificil = tk.Radiobutton( ventana_config, text="Difícil (16x16, 50 minas)", variable=dificultad_elegida, value="Dificil")
    radio_dificil.pack(anchor="w", padx=30)
    
    # ==============
    # MODO DE JUEGO

    lbl_modo = tk.Label(ventana_config, text="Seleccione modo de juego:", font=("Arial", 12))
    lbl_modo.pack(pady=20)
    
    # variable para guardar el modo elegido
    modo_elegido = tk.StringVar(value="Normal")
    
    # opcion: Normal
    radio_normal = tk.Radiobutton(ventana_config, text="Normal (sin límite de tiempo)", variable=modo_elegido, value="Normal")
    radio_normal.pack(anchor="w", padx=30)
    
    # opcion: Contrarreloj
    radio_contrarreloj = tk.Radiobutton(ventana_config, text="Contrarreloj (con límite de tiempo)", variable=modo_elegido, value="Contrarreloj")
    radio_contrarreloj.pack(anchor="w", padx=30)
    
    # ==============
    # BOTON INICIAR
    
    # lambda: se usa para pasar parametros a la funcion
    # .get() obtiene el valor de las variables StringVar
    boton_iniciar = tk.Button(ventana_config,text="INICIAR", width=15, height=2, bg="green", fg="white", 
        command=lambda: iniciar_partida(dificultad_elegida.get(), modo_elegido.get(), ventana_config))  # la ventana config para cerrarla despues
    
    boton_iniciar.pack(pady=20)


"""
N: iniciar_partida
D: cierra la ventana de configuración y abre el juego
E: dificultad, modo, ventana_config (tk.Toplevel)
S: ninguna
R: ninguna
"""
def iniciar_partida(dificultad, modo, ventana_config):

    # destroy() cierra la ventana de configuración
    ventana_config.destroy()
    
    # abrir la ventana del juego
    mostrar_ventana_juego(dificultad, modo)

"""
N: obtener_configuracion_dificultad
D: obtiene tamaño y cantidad de minas segun la dificultad
E: dificultad
S: tupla (tamaño, total_minas)
R: dificultad debe ser "Facil", "Medio" o "Dificil"
"""
def obtener_configuracion_dificultad(dificultad):
    if dificultad == "Facil":
        return (8, 10)
    elif dificultad == "Medio":
        return (12, 25)
    else:  # Dificil
        return (16, 50)
    
"""
N: crear_frame_superior
D: crea el frame superior con el contador de minas y el cronómetro
E: ventana_juego, total_minas, modo de juego
S: tupla (minas_restantes, lbl_tiempo)
R: ninguna
"""
def crear_frame_superior(ventana_juego, total_minas, modo):
    
    # crear frame
    frame_superior = tk.Frame(ventana_juego)
    frame_superior.pack(pady=10)
    
    # AGREGAR WIDGETS DENTRO DEL FRAME
    
    # etiqueta "Minas restantes:"
    lbl_minas_texto = tk.Label(frame_superior, text="Minas restantes:", font=("Arial", 12))
    lbl_minas_texto.pack(side="left", padx=10)
    
    # variable para actualizar el contador dinamicamente
    minas_restantes = tk.StringVar(value=str(total_minas))
    lbl_minas_valor = tk.Label(frame_superior, textvariable=minas_restantes, font=("Arial", 12, "bold"), fg="red")
    lbl_minas_valor.pack(side="left", padx=10)

    # CRONÓMETRO
    lbl_tiempo_texto = tk.Label(frame_superior, text="Tiempo:", font=("Arial", 12))
    lbl_tiempo_texto.pack(side="left", padx=20)
    
    # color según el modo
    if modo == "Normal":
        color_tiempo = "blue"
    else:
        color_tiempo = "orange"
    
    lbl_tiempo = tk.Label(frame_superior, text="0:00", font=("Arial", 12, "bold"), fg=color_tiempo)
    lbl_tiempo.pack(side="left", padx=10)
    
    return minas_restantes, lbl_tiempo


"""
N: crear_frame_inferior
D: crea el frame inferior con los botones de control
E: ventana_juego, dificultad, modo, tiempo actual
S: niguna
R: ninguna
"""
def crear_frame_inferior(ventana_juego, dificultad, modo, tiempo_actual):

    # crear frame
    frame_inferior = tk.Frame(ventana_juego)
    frame_inferior.pack(pady=10)
    
    # botón REINICIAR
    boton_reiniciar = tk.Button(frame_inferior, text="Reiniciar", width=10, command=lambda: reiniciar_partida(ventana_juego, dificultad, modo))
    boton_reiniciar.pack(side="left", padx=10)
    
    # botón ABANDONAR
    boton_abandonar = tk.Button(frame_inferior, text="Abandonar", width=10, command=lambda: abandonar_partida(ventana_juego, dificultad, modo, tiempo_actual))
    boton_abandonar.pack(side="left", padx=10)
    
    # botón VOLVER AL INICIO
    boton_volver = tk.Button(frame_inferior, text="Volver al inicio", width=15, command=lambda: volver_inicio(ventana_juego))
    boton_volver.pack(side="left", padx=10)


"""
N: crear_tablero_botones
D: crea la matriz de botones y asigna los eventos
E: frame_tablero, tamaño, tablero_logico, tablero_visible, juego_activo, primer_clic, actualizar_contador_minas, inciar_cronometro, ventana_juego, dificultad, modo, tiempo_actual, contador_movimientos
S: lista de botones creados 
R: ninguna
"""
def crear_tablero_botones(frame_tablero, tamaño, tablero_logico, tablero_visible, juego_activo, primer_clic, actualizar_contador_minas, iniciar_cronometro, ventana_juego, dificultad, modo,  tiempo_actual, contador_movimientos):
    
    botones = []
    
    # funcion para manejar clic izquierdo (revelar)
    def clic_izquierdo(fila, columna):
        nonlocal juego_activo, primer_clic, contador_movimientos # nonlocal porque pertenecen a la funcion exterior
        
        contador_movimientos += 1 # contar moviminetos

        if not juego_activo:
            return
        
        if tablero_visible[fila][columna] != 0: # si no esta oculta
            return
        
        # PRIMER CLIC: iniciar cronometro
        if primer_clic:
            primer_clic = False
            iniciar_cronometro()
        
        vivo = revelar_celda(tablero_logico, tablero_visible, fila, columna)
        actualizar_interfaz()
        
        if not vivo: # PERDIÓ
            juego_activo = False
            
            reveladas = contar_celdas_reveladas(tablero_visible)
            banderas = contar_banderas_colocadas(tablero_visible)

            mostrar_estadisticas("", dificultad, modo, tiempo_actual[0], reveladas, banderas, "Perdió")
            ventana_juego.destroy()
            return
    
        if verificar_victoria(tablero_logico, tablero_visible):
            juego_activo = False
            
            # calcular estadisticas para victoria
            reveladas = contar_celdas_reveladas(tablero_visible)
            banderas = contar_banderas_colocadas(tablero_visible)
            

            # pedir nomnre
            nombre = pedir_nombre(ventana_juego)

            es_record = agregar_si_es_record(nombre, dificultad, tiempo_actual[0], reveladas, contador_movimientos)

            # mostrar estadisticas

            mostrar_estadisticas(nombre, dificultad, modo, tiempo_actual[0], reveladas, banderas, "Ganó")
            
             # mostrar mensaje si es récord
            if es_record:
                messagebox.showinfo("¡Récord!", f"¡{nombre} has entrado al top 10 de {dificultad}!")
            
            ventana_juego.destroy()
            return
        
        
        actualizar_contador_minas()
    
    # funcion para manejar clic derecho (bandera)
    def clic_derecho(fila, columna):
        nonlocal juego_activo, contador_movimientos
        
        if not juego_activo:
            return
        
        if tablero_visible[fila][columna] == 0 or tablero_visible[fila][columna] == 2:
            
            contador_movimientos += 1 # contar movimikento

            colocar_bandera(tablero_visible, fila, columna)
            actualizar_interfaz()
            actualizar_contador_minas()
    
    # funcion para actualizar todos los botones segun tablero_visible
    def actualizar_interfaz():
        for fila in range(tamaño):
            for columna in range(tamaño):
                estado = tablero_visible[fila][columna]
                
                if estado == 0:  # oculta
                    botones[fila][columna].config(text="", relief="raised", bg="lightgray")
                elif estado == 2:  # bandera
                    botones[fila][columna].config(text="🚩", relief="sunken", bg="yellow")
                else:  # revelada
                    valor = tablero_logico[fila][columna]
                    if valor == -1:  # mina
                        botones[fila][columna].config(text="💣", relief="sunken", bg="red")
                    elif valor == 0:  # vacío
                        botones[fila][columna].config(text="", relief="sunken", bg="white")
                    else:  # número
                        if valor == 1:
                            color = "blue"
                        elif valor == 2:
                            color = "green"
                        elif valor == 3:
                            color = "red"
                        elif valor == 4:
                            color = "purple"
                        elif valor == 5:
                            color = "maroon"
                        elif valor == 6:
                            color = "turquoise"
                        elif valor == 7:
                            color = "black"
                        elif valor == 8:
                            color = "gray"
                        else:
                            color = "black"
                        botones[fila][columna].config(text=str(valor), relief="sunken", bg="white", fg=color)
    
    # crear los botones
    for fila in range(tamaño):
        fila_botones = []
        for columna in range(tamaño):
            boton = tk.Button(frame_tablero, width=2, height=1, relief="raised", bg="lightgray")
            boton.grid(row=fila, column=columna, padx=1, pady=1)
            
            boton.bind("<Button-1>", lambda event, f=fila, c=columna: clic_izquierdo(f, c))
            boton.bind("<Button-3>", lambda event, f=fila, c=columna: clic_derecho(f, c))
            
            fila_botones.append(boton)
        botones.append(fila_botones)
    
    return botones


"""
N: mostrar_ventana_juego
D: crea y muestra la ventana del juego con el tablero
E: dificultad, modo
S: ninguna
R: ninguna
"""
def mostrar_ventana_juego(dificultad, modo):
    
    # obtener configuracion segun dificultad
    tamaño, total_minas = obtener_configuracion_dificultad(dificultad)

    # inicializar tableros lógicos
    tablero_logico = inicializar_tablero_completo(tamaño, total_minas)
    tablero_visible = inicializar_tablero_visible(tamaño)
    
    # variables de estado del juego
    juego_activo = True
    primer_clic = True # inicaiar cronometro con el primer clic
    cronometro_activo = False   # si el cronómetro está corriendo
    contador_movimientos = 0   # contar los movimkientos

    # LISTA MUTABLE PARA EL TIEMPO (se puede modificar desde cualquier funcion)
    tiempo_actual = [0]  # [0] es el valor, se usa como tiempo_actual[0]
    
    # crear la ventana
    ventana_juego = tk.Toplevel()
    ventana_juego.title(f"Buscaminas - {dificultad} - {modo}")
    ancho = tamaño * 30 + 200
    alto = tamaño * 30 + 150
    ventana_juego.geometry(f"{ancho}x{alto}")
    ventana_juego.resizable(False, False)
    
    # crear frame superior
    minas_restantes, lbl_tiempo = crear_frame_superior(ventana_juego, total_minas, modo)

    #-------------------------
    # FUNCIONES DEL CRONOMETRO

    # funcion para formatear tiempol(segundos a MM:SS)
    def formatear_tiempo(segundos):
        minutos = segundos // 60
        segs = segundos % 60
        if segs < 10:
            return f"{minutos}:{segs:02d}"
        return f"{minutos}:{segs}"
    
    # funcion para actualizar el cronometro
    def actualizar_cronometro():
        nonlocal cronometro_activo, juego_activo
        
        if not cronometro_activo:
            return
        
        if not juego_activo:
            cronometro_activo = False # detener el cronometro
            return
        
        if modo == "Normal":
            tiempo_actual[0] = tiempo_actual[0] + 1
            lbl_tiempo.config(text=formatear_tiempo(tiempo_actual[0]))
            # programar proxima actualización (1000 ms = 1 segundo)
            ventana_juego.after(1000, actualizar_cronometro)
        
        else:
            # modo contrarreloj: resta segundos
            tiempo_actual[0]= tiempo_actual[0] - 1
            lbl_tiempo.config(text=formatear_tiempo(tiempo_actual[0]))
            
            # si el tiempo llega a 0, el jugador pierde
            if tiempo_actual[0] <= 0:
                juego_activo = False
                cronometro_activo = False
                mostrar_todas_minas(tablero_logico, tablero_visible)
                
                from estadisticas import mostrar_estadisticas
                reveladas = contar_celdas_reveladas(tablero_visible)
                banderas = contar_banderas_colocadas(tablero_visible)
                mostrar_estadisticas("", dificultad, modo, 0, reveladas, banderas, "Perdió")
                
                ventana_juego.destroy()
                return
            
            
            # programar proxima actualización
            ventana_juego.after(1000, actualizar_cronometro)

    # funcion para iniciar el cronometro 
    def iniciar_cronometro():
        nonlocal cronometro_activo, tiempo_actual
        
        if not cronometro_activo:
            cronometro_activo = True
            
            if modo == "Normal":
                tiempo_actual[0]= 0
            else:  # Contrarreloj
                if dificultad == "Facil":
                    tiempo_actual[0] = 180
                elif dificultad == "Medio":
                    tiempo_actual[0] = 480
                else:
                    tiempo_actual[0] = 900
            
            lbl_tiempo.config(text=formatear_tiempo(tiempo_actual[0]))
            actualizar_cronometro()
    
    # crear frame del tablero
    frame_tablero = tk.Frame(ventana_juego)
    frame_tablero.pack()


    # funcion para actualizar el contador de minas
    def actualizar_contador_minas():
        restantes = contar_minas_restantes(tablero_visible, total_minas)
        minas_restantes.set(str(restantes))

    crear_tablero_botones(frame_tablero, tamaño, tablero_logico, tablero_visible, juego_activo, primer_clic, actualizar_contador_minas, iniciar_cronometro, ventana_juego, dificultad, modo, tiempo_actual, contador_movimientos)
    
    # crear frame inferior
    crear_frame_inferior(ventana_juego, dificultad, modo, tiempo_actual)
    
#--------------------------------------
# funciones auxiliares para los botones
"""
N: reiniciar_partida
D: cierra la ventana actual y abre una nueva partida con la misma configuracion
E: ventana_juego, dificultad, modo
S: ningua
R: ninguna
"""
def reiniciar_partida(ventana_juego, dificultad, modo):
    ventana_juego.destroy()
    mostrar_ventana_juego(dificultad, modo)


"""
N: abandonar_partida
D: cierra la ventana del juego y muestra estadísticas de abandono
E: ventana_juego, dificultad, modo, tiempo_actual
S: ninguna
R: ninguna
"""

def abandonar_partida(ventana_juego, dificultad, modo, tiempo_actual):
    mostrar_estadisticas("", dificultad, modo, tiempo_actual[0], 0, 0, "Abandonó")
    ventana_juego.destroy()
   

"""
N: volver_inicio
D: cierra la ventana del juego y vuelve a la ventana inicial
E: ventana_juego
S: ninguna
R: ninguna
"""
def volver_inicio(ventana_juego):
    global ventana
    ventana_juego.destroy()
    ventana.deiconify() # mostrar la ventana prinicpal

mostrar_ventana_inicial()
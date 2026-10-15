import tkinter as tk
from tkinter import messagebox, ttk
import math
from modelo_grafo import Grafo
import algoritmos

class EditorGrafosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - FCCA BUAP | Gabriela Rendon Celis 202543260")
        self.root.geometry("1100x750")

    
        self.COLOR_FONDO = "#FFF0F5"         
        self.COLOR_PANEL_SUP = "#FFC0CB"    
        self.COLOR_PANEL_ALG = "#FFE4E1"    
        self.COLOR_NODO = "#E6E6FA"          
        self.COLOR_NODO_ORIGEN = "#FFFACD"   
        self.COLOR_NODO_VISITADO = "#D4EDDA" 
        self.COLOR_TEXTO = "#4A4A4A"         
        self.COLOR_ARISTA_BASE = "#8D8B8E"   
        self.COLOR_ARISTA_MST = "#82C99B"    
        self.COLOR_ARISTA_DESC = "#F08080"   

        self.root.configure(bg=self.COLOR_FONDO)

        self.grafo = Grafo()
        self.modo_actual = "nodo"
        self.nodo_origen_arista = None
        self.nodo_arrastrando = None


        self.pasos_algoritmo = []
        self.paso_actual_idx = 0
        self.reproduciendo = False
        
    
        self.ventana_matriz_floyd = None
        self.tabla_entries_floyd = []

        self.crear_interfaz()

    def crear_interfaz(self):
        
        panel_encabezado = tk.Frame(self.root, bg=self.COLOR_PANEL_SUP, padx=5, pady=4)
        panel_encabezado.pack(side=tk.TOP, fill=tk.X)

        lbl_autor = tk.Label(
            panel_encabezado, 
            text="Estudiante: Gabriela Rendon Celis | Editor de Grafos", 
            bg=self.COLOR_PANEL_SUP, 
            fg=self.COLOR_TEXTO, 
            font=("Arial", 11, "bold")
        )
        lbl_autor.pack(side=tk.LEFT, padx=10)

        
        panel_superior = tk.Frame(self.root, bg=self.COLOR_PANEL_SUP, padx=5, pady=5)
        panel_superior.pack(side=tk.TOP, fill=tk.X)

        tk.Label(panel_superior, text="Modo:", bg=self.COLOR_PANEL_SUP, fg=self.COLOR_TEXTO, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)

        btn_nodo = tk.Button(panel_superior, text="Agregar Nodo", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=lambda: self.cambiar_modo("nodo"))
        btn_nodo.pack(side=tk.LEFT, padx=2)

        btn_arista = tk.Button(panel_superior, text="Agregar Arista", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=lambda: self.cambiar_modo("arista"))
        btn_arista.pack(side=tk.LEFT, padx=2)

        btn_eliminar = tk.Button(panel_superior, text="Eliminar", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=lambda: self.cambiar_modo("eliminar"))
        btn_eliminar.pack(side=tk.LEFT, padx=2)

        btn_origen = tk.Button(panel_superior, text="Definir Origen", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=lambda: self.cambiar_modo("origen"))
        btn_origen.pack(side=tk.LEFT, padx=2)

        self.var_dirigido = tk.BooleanVar(value=False)
        chk_dirigido = tk.Checkbutton(panel_superior, text="Dirigido", variable=self.var_dirigido, command=self.actualizar_tipo_grafo, bg=self.COLOR_PANEL_SUP, fg=self.COLOR_TEXTO, font=("Arial", 9, "bold"))
        chk_dirigido.pack(side=tk.LEFT, padx=10)

        btn_matriz = tk.Button(panel_superior, text="Matriz de Adyacencia", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.abrir_ventana_matriz)
        btn_matriz.pack(side=tk.LEFT, padx=10)

        btn_limpiar = tk.Button(panel_superior, text="Limpiar Grafo", bg="#FFD1DC", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.limpiar_grafo)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)

    
        panel_algoritmos = tk.Frame(self.root, bg=self.COLOR_PANEL_ALG, padx=5, pady=5)
        panel_algoritmos.pack(side=tk.TOP, fill=tk.X)

        tk.Label(panel_algoritmos, text="Algoritmo:", bg=self.COLOR_PANEL_ALG, fg=self.COLOR_TEXTO, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.combo_algoritmo = ttk.Combobox(panel_algoritmos, values=["Kruskal", "Prim", "Dijkstra", "Floyd-Warshall"], state="readonly")
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.pack(side=tk.LEFT, padx=5)

        btn_ejecutar = tk.Button(panel_algoritmos, text="Iniciar Algoritmo", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.iniciar_algoritmo)
        btn_ejecutar.pack(side=tk.LEFT, padx=5)

        btn_anterior = tk.Button(panel_algoritmos, text="Anterior", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.paso_anterior)
        btn_anterior.pack(side=tk.LEFT, padx=2)

        btn_siguiente = tk.Button(panel_algoritmos, text="Siguiente Paso", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.paso_siguiente)
        btn_siguiente.pack(side=tk.LEFT, padx=2)

        btn_reproducir = tk.Button(panel_algoritmos, text="Auto Reproducir", bg="#FFFFFF", fg=self.COLOR_TEXTO, relief=tk.RAISED, command=self.toggle_reproduccion)
        btn_reproducir.pack(side=tk.LEFT, padx=2)

    
        self.lbl_estado = tk.Label(self.root, text="Seleccione una accion para comenzar.", bg=self.COLOR_PANEL_SUP, fg=self.COLOR_TEXTO, anchor="w", relief=tk.SUNKEN, font=("Arial", 10))
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

        
        self.canvas = tk.Canvas(self.root, bg=self.COLOR_FONDO, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

    def cambiar_modo(self, modo):
        self.modo_actual = modo
        self.nodo_origen_arista = None
        self.lbl_estado.config(text=f"Modo seleccionado: {modo.capitalize()}")

    def actualizar_tipo_grafo(self):
        self.grafo.es_dirigido = self.var_dirigido.get()
        self.redibujar_grafo()

    def limpiar_grafo(self):
        self.grafo = Grafo(es_dirigido=self.var_dirigido.get())
        self.pasos_algoritmo = []
        self.paso_actual_idx = 0
        if self.ventana_matriz_floyd and self.ventana_matriz_floyd.winfo_exists():
            self.ventana_matriz_floyd.destroy()
        self.lbl_estado.config(text="Grafo limpiado.")
        self.redibujar_grafo()

    def buscar_nodo_en_posicion(self, x, y):
        for nodo in self.grafo.nodos:
            dist = math.hypot(nodo.x - x, nodo.y - y)
            if dist <= 20:
                return nodo
        return None

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        nodo_clicado = self.buscar_nodo_en_posicion(x, y)

        if self.modo_actual == "nodo":
            if not nodo_clicado:
                if len(self.grafo.nodos) >= self.grafo.MAX_NODOS:
                    messagebox.showwarning("Limite alcanzado", "El grafo no puede tener mas de 20 nodos.")
                    return
                self.grafo.agregar_nodo(x, y)
                self.redibujar_grafo()
            else:
                self.nodo_arrastrando = nodo_clicado

        elif self.modo_actual == "arista":
            if nodo_clicado:
                if self.nodo_origen_arista is None:
                    self.nodo_origen_arista = nodo_clicado
                    self.lbl_estado.config(text=f"Origen seleccionado: {nodo_clicado.etiqueta}. Seleccione el destino.")
                else:
                    destino = nodo_clicado
                    if self.nodo_origen_arista.id != destino.id:
                        peso = self.pedir_peso_arista()
                        if peso is not None:
                            self.grafo.agregar_o_actualizar_arista(self.nodo_origen_arista.id, destino.id, peso)
                            self.lbl_estado.config(text=f"Arista agregada entre {self.nodo_origen_arista.etiqueta} y {destino.etiqueta}.")
                    self.nodo_origen_arista = None
                    self.redibujar_grafo()

        elif self.modo_actual == "eliminar":
            if nodo_clicado:
                self.grafo.eliminar_nodo(nodo_clicado.id)
                self.lbl_estado.config(text=f"Nodo {nodo_clicado.etiqueta} eliminado.")
                self.redibujar_grafo()

        elif self.modo_actual == "origen":
            if nodo_clicado:
                self.grafo.nodo_origen_seleccionado = nodo_clicado.id
                self.lbl_estado.config(text=f"Nodo origen definido: {nodo_clicado.etiqueta}.")
                self.redibujar_grafo()

    def on_canvas_drag(self, event):
        if self.modo_actual == "nodo" and self.nodo_arrastrando:
            self.nodo_arrastrando.x = event.x
            self.nodo_arrastrando.y = event.y
            self.redibujar_grafo()

    def on_canvas_release(self, event):
        self.nodo_arrastrando = None

    def pedir_peso_arista(self):
        ventana_peso = tk.Toplevel(self.root)
        ventana_peso.title("Peso de la arista")
        ventana_peso.geometry("250x120")
        ventana_peso.configure(bg=self.COLOR_FONDO)
        ventana_peso.transient(self.root)
        ventana_peso.grab_set()

        tk.Label(ventana_peso, text="Ingrese el peso:", bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO, font=("Arial", 10)).pack(pady=5)
        entry_peso = tk.Entry(ventana_peso, justify="center")
        entry_peso.insert(0, "1.0")
        entry_peso.pack(pady=5)

        resultado = [1.0]

        def confirmar():
            try:
                val = float(entry_peso.get())
                if val < 0:
                    messagebox.showerror("Error", "El peso no puede ser negativo.")
                    return
                resultado[0] = val
                ventana_peso.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un numero valido.")

        btn_ok = tk.Button(ventana_peso, text="Aceptar", bg=self.COLOR_PANEL_SUP, fg=self.COLOR_TEXTO, relief=tk.RAISED, command=confirmar)
        btn_ok.pack(pady=5)

        self.root.wait_window(ventana_peso)
        return resultado[0]

    def redibujar_grafo(self, aristas_destacadas=None, nodos_destacados=None, aristas_descartadas=None):
        self.canvas.delete("all")
        if aristas_destacadas is None:
            aristas_destacadas = []
        if nodos_destacados is None:
            nodos_destacados = []
        if aristas_descartadas is None:
            aristas_descartadas = []

        for a in self.grafo.aristas:
            n_origen = self.grafo.nodos[a.origen]
            n_destino = self.grafo.nodos[a.destino]

            color = self.COLOR_ARISTA_BASE
            ancho = 2

            par = (a.origen, a.destino)
            par_inv = (a.destino, a.origen)

            if par in aristas_destacadas or par_inv in aristas_destacadas:
                color = self.COLOR_ARISTA_MST
                ancho = 4
            elif par in aristas_descartadas or par_inv in aristas_descartadas:
                color = self.COLOR_ARISTA_DESC
                ancho = 2

            angle = math.atan2(n_destino.y - n_origen.y, n_destino.x - n_origen.x)
            r = 20
            x1 = n_origen.x + r * math.cos(angle)
            y1 = n_origen.y + r * math.sin(angle)
            x2 = n_destino.x - r * math.cos(angle)
            y2 = n_destino.y - r * math.sin(angle)

            if self.grafo.es_dirigido:
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color, width=ancho)
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            self.canvas.create_text(mx, my - 8, text=str(a.peso), fill="#5C5B5D", font=("Arial", 10, "bold"))

        for n in self.grafo.nodos:
            color_fondo = self.COLOR_NODO
            if n.id == self.grafo.nodo_origen_seleccionado:
                color_fondo = self.COLOR_NODO_ORIGEN
            if n.id in nodos_destacados:
                color_fondo = self.COLOR_NODO_VISITADO

            self.canvas.create_oval(n.x - 20, n.y - 20, n.x + 20, n.y + 20, fill=color_fondo, outline="#8A7B8E", width=2)
            self.canvas.create_text(n.x, n.y, text=n.etiqueta, fill=self.COLOR_TEXTO, font=("Arial", 12, "bold"))

    def abrir_ventana_matriz(self):
        v = tk.Toplevel(self.root)
        v.title("Matriz de Adyacencia")
        v.geometry("520x420")
        v.configure(bg=self.COLOR_FONDO)

        lbl = tk.Label(v, text="Edite los valores (use 'inf' o '0' para no conexion):", bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO, font=("Arial", 10, "bold"))
        lbl.pack(pady=8)

        matriz = self.grafo.obtener_matriz_adyacencia()
        n = len(self.grafo.nodos)

        frame_tabla = tk.Frame(v, bg=self.COLOR_PANEL_ALG, padx=8, pady=8)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        entries = []
        for i in range(n):
            fila_entries = []
            tk.Label(frame_tabla, text=self.grafo.nodos[i].etiqueta, bg=self.COLOR_PANEL_ALG, fg=self.COLOR_TEXTO, font=("Arial", 10, "bold")).grid(row=i+1, column=0)
            tk.Label(frame_tabla, text=self.grafo.nodos[i].etiqueta, bg=self.COLOR_PANEL_ALG, fg=self.COLOR_TEXTO, font=("Arial", 10, "bold")).grid(row=0, column=i+1)

            for j in range(n):
                e = tk.Entry(frame_tabla, width=6, justify="center", bg="#FFFFFF", fg=self.COLOR_TEXTO)
                val = matriz[i][j]
                if val == math.inf:
                    e.insert(0, "inf")
                else:
                    e.insert(0, str(val))
                e.grid(row=i+1, column=j+1, padx=2, pady=2)
                fila_entries.append(e)
            entries.append(fila_entries)

        def guardar():
            nueva_matriz = []
            try:
                for i in range(n):
                    fila = []
                    for j in range(n):
                        txt = entries[i][j].get().strip().lower()
                        if txt == "inf" or txt == "":
                            fila.append(math.inf)
                        else:
                            fila.append(float(txt))
                    nueva_matriz.append(fila)

                self.grafo.cargar_desde_matriz_adyacencia(nueva_matriz)
                self.redibujar_grafo()
                v.destroy()
                messagebox.showinfo("Exito", "Grafo actualizado desde la matriz.")
            except ValueError:
                messagebox.showerror("Error", "Valores invalidos en la matriz.")

        btn_guardar = tk.Button(v, text="Guardar Cambios", bg=self.COLOR_PANEL_SUP, fg=self.COLOR_TEXTO, relief=tk.RAISED, command=guardar)
        btn_guardar.pack(pady=8)

    def abrir_o_actualizar_matriz_floyd(self, matriz_estado):
        n = len(self.grafo.nodos)
        if not self.ventana_matriz_floyd or not self.ventana_matriz_floyd.winfo_exists():
            self.ventana_matriz_floyd = tk.Toplevel(self.root)
            self.ventana_matriz_floyd.title("Floyd-Warshall: Matriz de Distancias Mínimas")
            self.ventana_matriz_floyd.geometry("520x420")
            self.ventana_matriz_floyd.configure(bg=self.COLOR_FONDO)

            lbl = tk.Label(self.ventana_matriz_floyd, text="Matriz de Distancias (Paso a Paso):", bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO, font=("Arial", 11, "bold"))
            lbl.pack(pady=8)

            frame_tabla = tk.Frame(self.ventana_matriz_floyd, bg=self.COLOR_PANEL_ALG, padx=8, pady=8)
            frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.tabla_entries_floyd = []
            for i in range(n):
                fila_entries = []
                tk.Label(frame_tabla, text=self.grafo.nodos[i].etiqueta, bg=self.COLOR_PANEL_ALG, fg=self.COLOR_TEXTO, font=("Arial", 10, "bold")).grid(row=i+1, column=0)
                tk.Label(frame_tabla, text=self.grafo.nodos[i].etiqueta, bg=self.COLOR_PANEL_ALG, fg=self.COLOR_TEXTO, font=("Arial", 10, "bold")).grid(row=0, column=i+1)

                for j in range(n):
                    e = tk.Entry(frame_tabla, width=6, justify="center", bg="#FFFFFF", fg=self.COLOR_TEXTO, font=("Arial", 9, "bold"))
                    e.grid(row=i+1, column=j+1, padx=2, pady=2)
                    fila_entries.append(e)
                self.tabla_entries_floyd.append(fila_entries)

        
        if matriz_estado and self.tabla_entries_floyd:
            for i in range(n):
                for j in range(n):
                    entry = self.tabla_entries_floyd[i][j]
                    entry.delete(0, tk.END)
                    val = matriz_estado[i][j]
                    if val == math.inf:
                        entry.insert(0, "inf")
                    else:
                        entry.insert(0, str(round(val, 2)))

    def iniciar_algoritmo(self):
        alg = self.combo_algoritmo.get()
        if len(self.grafo.nodos) == 0:
            messagebox.showwarning("Atencion", "Cree un grafo antes de iniciar.")
            return

        origen = self.grafo.nodo_origen_seleccionado if self.grafo.nodo_origen_seleccionado is not None else 0

        if alg == "Kruskal":
            self.pasos_algoritmo = algoritmos.ejecutar_kruskal(self.grafo)
        elif alg == "Prim":
            self.pasos_algoritmo = algoritmos.ejecutar_prim(self.grafo, origen)
        elif alg == "Dijkstra":
            self.pasos_algoritmo = algoritmos.ejecutar_dijkstra(self.grafo, origen)
        elif alg == "Floyd-Warshall":
            self.pasos_algoritmo = algoritmos.ejecutar_floyd_warshall(self.grafo)

        self.paso_actual_idx = 0
        self.mostrar_paso_actual()

    def mostrar_paso_actual(self):
        if not self.pasos_algoritmo:
            return
        paso = self.pasos_algoritmo[self.paso_actual_idx]
        self.lbl_estado.config(text=f"Paso {self.paso_actual_idx + 1}/{len(self.pasos_algoritmo)}: {paso.descripcion}")
        
        self.redibujar_grafo(
            aristas_destacadas=paso.aristas_destacadas,
            nodos_destacados=paso.nodos_destacados,
            aristas_descartadas=paso.aristas_descartadas
        )

    
        if paso.matriz_estado is not None:
            self.abrir_o_actualizar_matriz_floyd(paso.matriz_estado)

    def paso_siguiente(self):
        if self.paso_actual_idx < len(self.pasos_algoritmo) - 1:
            self.paso_actual_idx += 1
            self.mostrar_paso_actual()

    def paso_anterior(self):
        if self.paso_actual_idx > 0:
            self.paso_actual_idx -= 1
            self.mostrar_paso_actual()

    def toggle_reproduccion(self):
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo:
            self.reproducir_animacion()

    def reproducir_animacion(self):
        if self.reproduciendo and self.paso_actual_idx < len(self.pasos_algoritmo) - 1:
            self.paso_siguiente()
            self.root.after(1000, self.reproducir_animacion)
        else:
            self.reproduciendo = False
import math

class Nodo:
    def __init__(self, id_nodo, etiqueta, x, y):
        self.id = id_nodo
        self.etiqueta = etiqueta
        self.x = x
        self.y = y

class Arista:
    def __init__(self, origen, destino, peso=1.0):
        self.origen = origen
        self.destino = destino
        self.peso = peso

class Grafo:
    MAX_NODOS = 20
    INF = math.inf

    def __init__(self, es_dirigido=False, es_ponderado=True):
        self.es_dirigido = es_dirigido
        self.es_ponderado = es_ponderado
        self.nodos = []  
        self.aristas = []  
        self.nodo_origen_seleccionado = None

    def obtener_etiqueta_siguiente(self):
        
        idx = len(self.nodos)
        if idx < 26:
            return chr(65 + idx)
        else:
            return f"{chr(65 + (idx % 26))}{idx // 26}"

    def agregar_nodo(self, x, y):
        if len(self.nodos) >= self.MAX_NODOS:
            return None
        id_nodo = len(self.nodos)
        etiqueta = self.obtener_etiqueta_siguiente()
        nuevo_nodo = Nodo(id_nodo, etiqueta, x, y)
        self.nodos.append(nuevo_nodo)
        return nuevo_nodo

    def eliminar_nodo(self, id_nodo):
    
        self.aristas = [a for a in self.aristas if a.origen != id_nodo and a.destino != id_nodo]
        
        self.nodos = [n for n in self.nodos if n.id != id_nodo]
        
        for idx, n in enumerate(self.nodos):
            n.id = idx
            n.etiqueta = self.obtener_etiqueta_siguiente_para_indice(idx)
      

    def obtener_etiqueta_siguiente_para_indice(self, idx):
        if idx < 26:
            return chr(65 + idx)
        else:
            return f"{chr(65 + (idx % 26))}{idx // 26}"

    def agregar_o_actualizar_arista(self, origen_id, destino_id, peso=1.0):
        if not self.es_ponderado:
            peso = 1.0
        
        arista_existente = self.buscar_arista(origen_id, destino_id)
        if arista_existente:
            arista_existente.peso = peso
        else:
            nueva_arista = Arista(origen_id, destino_id, peso)
            self.aristas.append(nueva_arista)

        if not self.es_dirigido:
            arista_inversa = self.buscar_arista(destino_id, origen_id)
            if arista_inversa:
                arista_inversa.peso = peso
            else:
                nueva_arista_inv = Arista(destino_id, origen_id, peso)
                self.aristas.append(nueva_arista_inv)

    def eliminar_arista(self, origen_id, destino_id):
        self.aristas = [a for a in self.aristas if not (a.origen == origen_id and a.destino == destino_id)]
        if not self.es_dirigido:
            self.aristas = [a for a in self.aristas if not (a.origen == destino_id and a.destino == origen_id)]

    def buscar_arista(self, origen_id, destino_id):
        for a in self.aristas:
            if a.origen == origen_id and a.destino == destino_id:
                return a
        return None

    def obtener_matriz_adyacencia(self):
        n = len(self.nodos)
        matriz = [[self.INF if i != j else 0.0 for j in range(n)] for i in range(n)]
        for a in self.aristas:
            if a.origen < n and a.destino < n:
                matriz[a.origen][a.destino] = a.peso
        return matriz

    def cargar_desde_matriz_adyacencia(self, matriz):
        self.aristas.clear()
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                val = matriz[i][j]
                if i != j and val != self.INF and val > 0:
                    self.aristas.append(Arista(i, j, float(val)))
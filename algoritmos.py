import math

class PasoAlgoritmo:
    def __init__(self, descripcion="", aristas_destacadas=None, nodos_destacados=None, aristas_descartadas=None, matriz_estado=None, info_adicional=None):
        self.descripcion = descripcion
        self.aristas_destacadas = aristas_destacadas if aristas_destacadas else []
        self.nodos_destacados = nodos_destacados if nodos_destacados else []
        self.aristas_descartadas = aristas_descartadas if aristas_descartadas else []
        self.matriz_estado = matriz_estado
        self.info_adicional = info_adicional if info_adicional else {}


def ejecutar_kruskal(grafo):
    pasos = []
    if grafo.es_dirigido:
        pasos.append(PasoAlgoritmo("Error: Kruskal requiere un grafo no dirigido."))
        return pasos

    n = len(grafo.nodos)
    if n == 0:
        pasos.append(PasoAlgoritmo("El grafo esta vacio."))
        return pasos


    aristas_unicas = []
    visitadas = set()
    for a in grafo.aristas:
        par = tuple(sorted((a.origen, a.destino)))
        if par not in visitadas and a.origen != a.destino:
            visitadas.add(par)
            aristas_unicas.append((a.peso, a.origen, a.destino))

    aristas_unicas.sort(key=lambda x: x[0])

    padre = list(range(n))

    def buscar(i):
        if padre[i] == i:
            return i
        padre[i] = buscar(padre[i])
        return padre[i]

    def unir(i, j):
        root_i = buscar(i)
        root_j = buscar(j)
        if root_i != root_j:
            padre[root_i] = root_j
            return True
        return False

    aristas_mst = []
    aristas_descartadas = []

    pasos.append(PasoAlgoritmo("Inicio de Kruskal. Aristas ordenadas por peso."))

    for peso, u, v in aristas_unicas:
        u_etiqueta = grafo.nodos[u].etiqueta
        v_etiqueta = grafo.nodos[v].etiqueta

        if buscar(u) != buscar(v):
            unir(u, v)
            aristas_mst.append((u, v))
            pasos.append(PasoAlgoritmo(
                f"Se selecciona la arista ({u_etiqueta} - {v_etiqueta}) con peso {peso}. No forma ciclos.",
                aristas_destacadas=list(aristas_mst),
                aristas_descartadas=list(aristas_descartadas)
            ))
        else:
            aristas_descartadas.append((u, v))
            pasos.append(PasoAlgoritmo(
                f"Se descarta la arista ({u_etiqueta} - {v_etiqueta}) con peso {peso} porque forma un ciclo.",
                aristas_destacadas=list(aristas_mst),
                aristas_descartadas=list(aristas_descartadas)
            ))

    pasos.append(PasoAlgoritmo(
        "Algoritmo de Kruskal finalizado.",
        aristas_destacadas=list(aristas_mst),
        aristas_descartadas=list(aristas_descartadas)
    ))
    return pasos


def ejecutar_prim(grafo, nodo_inicio_id=0):
    pasos = []
    if grafo.es_dirigido:
        pasos.append(PasoAlgoritmo("Error: Prim requiere un grafo no dirigido."))
        return pasos

    n = len(grafo.nodos)
    if n == 0 or nodo_inicio_id >= n:
        pasos.append(PasoAlgoritmo("Seleccione un nodo de origen valido."))
        return pasos

    visitados = {nodo_inicio_id}
    aristas_mst = []

    pasos.append(PasoAlgoritmo(
        f"Inicio de Prim desde el nodo {grafo.nodos[nodo_inicio_id].etiqueta}.",
        nodos_destacados=list(visitados)
    ))

    while len(visitados) < n:
        mejor_arista = None
        min_peso = math.inf

        for a in grafo.aristas:
            if (a.origen in visitados and a.destino not in visitados):
                if a.peso < min_peso:
                    min_peso = a.peso
                    mejor_arista = (a.origen, a.destino)
            elif (a.destino in visitados and a.origen not in visitados):
                if a.peso < min_peso:
                    min_peso = a.peso
                    mejor_arista = (a.destino, a.origen)

        if mejor_arista is None:
            pasos.append(PasoAlgoritmo("El grafo es no conexo. No se puede completar el MST."))
            break

        u, v = mejor_arista
        visitados.add(v)
        aristas_mst.append((u, v))

        v_etiqueta = grafo.nodos[v].etiqueta
        pasos.append(PasoAlgoritmo(
            f"Se agrega el nodo {v_etiqueta} al MST mediante la arista con peso {min_peso}.",
            aristas_destacadas=list(aristas_mst),
            nodos_destacados=list(visitados)
        ))

    pasos.append(PasoAlgoritmo(
        "Algoritmo de Prim finalizado.",
        aristas_destacadas=list(aristas_mst),
        nodos_destacados=list(visitados)
    ))
    return pasos


def ejecutar_dijkstra(grafo, origen_id=0):
    pasos = []
    n = len(grafo.nodos)
    if n == 0 or origen_id >= n:
        pasos.append(PasoAlgoritmo("Seleccione un nodo origen valido."))
        return pasos

    distancias = [math.inf] * n
    previos = [None] * n
    visitados = [False] * n

    distancias[origen_id] = 0.0

    origen_etiqueta = grafo.nodos[origen_id].etiqueta
    pasos.append(PasoAlgoritmo(
        f"Inicio de Dijkstra desde el nodo {origen_etiqueta}.",
        nodos_destacados=[origen_id],
        info_adicional={"distancias": list(distancias)}
    ))

    for _ in range(n):
    
        u = -1
        min_dist = math.inf
        for i in range(n):
            if not visitados[i] and distancias[i] < min_dist:
                min_dist = distancias[i]
                u = i

        if u == -1 or distancias[u] == math.inf:
            break

        visitados[u] = True
        u_etiqueta = grafo.nodos[u].etiqueta

        pasos.append(PasoAlgoritmo(
            f"Nodo actual visitado: {u_etiqueta} con distancia acumulada {distancias[u]}.",
            nodos_destacados=[i for i, v in enumerate(visitados) if v],
            info_adicional={"distancias": list(distancias)}
        ))

        # Revisar vecinos
        for a in grafo.aristas:
            if a.origen == u:
                v = a.destino
                if not visitados[v]:
                    nueva_dist = distancias[u] + a.peso
                    if nueva_dist < distancias[v]:
                        distancias[v] = nueva_dist
                        previos[v] = u
                        v_etiqueta = grafo.nodos[v].etiqueta
                        pasos.append(PasoAlgoritmo(
                            f"Se actualiza la distancia hacia {v_etiqueta}: {nueva_dist}.",
                            nodos_destacados=[i for i, val in enumerate(visitados) if val],
                            aristas_destacadas=[(u, v)],
                            info_adicional={"distancias": list(distancias)}
                        ))

    pasos.append(PasoAlgoritmo(
        "Algoritmo de Dijkstra finalizado.",
        nodos_destacados=[i for i, v in enumerate(visitados) if v],
        info_adicional={"distancias": list(distancias), "previos": previos}
    ))
    return pasos


def ejecutar_floyd_warshall(grafo):
    pasos = []
    n = len(grafo.nodos)
    if n == 0:
        pasos.append(PasoAlgoritmo("El grafo esta vacio."))
        return pasos

    dist = grafo.obtener_matriz_adyacencia()


    matriz_inicial = [fila[:] for fila in dist]
    pasos.append(PasoAlgoritmo(
        "Inicio de Floyd-Warshall. Matriz inicial de distancias construida.",
        matriz_estado=matriz_inicial
    ))

    for k in range(n):
        k_etiqueta = grafo.nodos[k].etiqueta
        for i in range(n):
            for j in range(n):
                if dist[i][k] != math.inf and dist[k][j] != math.inf:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        matriz_paso = [fila[:] for fila in dist]
        pasos.append(PasoAlgoritmo(
            f"Matriz de distancias considerando el nodo {k_etiqueta} como intermediario.",
            matriz_estado=matriz_paso,
            nodos_destacados=[k]
        ))

    pasos.append(PasoAlgoritmo(
        "Algoritmo de Floyd-Warshall finalizado.",
        matriz_estado=[fila[:] for fila in dist]
    ))
    return pasos
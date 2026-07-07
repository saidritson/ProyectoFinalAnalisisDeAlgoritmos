INF = 9999

def reconstruir_camino(padre, nodo):
    camino = [nodo]

    while nodo in padre:
        nodo = padre[nodo]
        camino.insert(0, nodo)
    
    return camino

def h(nodo_actual, nodo_meta, coordenadas):
    if nodo_actual not in coordenadas or nodo_meta not in coordenadas:
        return 0.0

    x1, y1 = coordenadas[nodo_actual]
    x2, y2 = coordenadas[nodo_meta]

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def obtener_vecinos(nodo_actual, grafo):
    return list(grafo.get(nodo_actual, {}).keys())

def costo(actual, vecino, grafo):
    """Obtiene el peso de la arista entre actual y vecino."""
    return grafo.get(actual, {}).get(vecino, INF)

def aEstrella(inicio, meta, grafo, coordenadas, guardar_historial=False): 
    """
    Algoritmo A* (A-Star)
    Encuentra la ruta más corta entre un nodo de inicio y uno de meta utilizando
    una heurística (distancia euclidiana) para optimizar la búsqueda.
    
    Args:
        inicio (int): Nodo de origen.
        meta (int): Nodo destino.
        grafo (dict): Representación del grafo en formato de lista de adyacencia.
        coordenadas (dict): Coordenadas espaciales de cada nodo para la heurística.
        guardar_historial (bool): Si es True, captura el estado para la animación.
        
    Returns:
        tuple: (ruta_optima, costo_total, historial_opcional) o (None, INF) si no hay ruta.
    """
    abiertos = set()
    cerrados = set()
    g = {}
    f = {}
    padre = {}
    
    historial = []
    
    def capturar_estado(nodo_actual=None, arista_actual=None):
        if not guardar_historial: return
        estado_nodos = {}
        # Identificar todos los nodos para colorearlos de blanco
        # We can deduce them from `coordenadas` keys
        for nodo in coordenadas.keys():
            if nodo in cerrados:
                estado_nodos[nodo] = "#000000" # Negro
            elif nodo in abiertos:
                estado_nodos[nodo] = "#888888" # Gris
            else:
                estado_nodos[nodo] = "#ffffff" # Blanco
                
        if nodo_actual is not None:
            estado_nodos[nodo_actual] = "#0055ff" # Azul
            
        # We also create a distances array mapped by index to match UI expectations
        dist_list = []
        for i in range(len(coordenadas)):
            dist_list.append(g.get(i, INF))
            
        historial.append({
            "nodos": estado_nodos,
            "arista_actual": arista_actual,
            "distancias": dist_list,
            "predecesores": [] # No se mostrara tabla de predecesores
        })

    abiertos.add(inicio)
    g[inicio] = 0.0
    f[inicio] = h(inicio, meta, coordenadas)
    
    capturar_estado()

    while abiertos:
        # Extraer el nodo en 'abiertos' con el menor valor de f(n)
        actual = None
        min_f = INF
        for nodo in abiertos:
            if f.get(nodo, INF) < min_f:
                min_f = f[nodo]
                actual = nodo
        
        # Condición de éxito: Si llegamos a la meta, reconstruimos la ruta
        if actual == meta:
            camino = reconstruir_camino(padre, actual)
            if guardar_historial:
                capturar_estado(actual)
                return camino, g[actual], historial
            return camino, g[actual]
        
        abiertos.remove(actual)
        cerrados.add(actual)
        capturar_estado(actual)

        # Expansión de vecinos
        for vecino in obtener_vecinos(actual, grafo):
            if vecino in cerrados:
                continue

            g_tentativo = g[actual] + costo(actual, vecino, grafo)

            # Si el vecino no está en abiertos, o encontramos una ruta mejor
            if vecino not in abiertos:
                abiertos.add(vecino)
            elif g_tentativo >= g.get(vecino, INF):
                continue

            padre[vecino] = actual
            g[vecino] = g_tentativo
            f[vecino] = g_tentativo + h(vecino, meta, coordenadas)
            
            capturar_estado(actual, (actual, vecino))

    if guardar_historial:
        return None, INF, []
    return None, INF
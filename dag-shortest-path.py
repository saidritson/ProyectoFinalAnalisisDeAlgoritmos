class arista:
    def __init__(self, origen, destino, peso):
        self.origen = origen
        self.destino = destino
        self.peso = peso

INF = 9999

def ordenamiento_topologico(V, lista_aristas):
    """
    Obtiene el orden topológico de los vértices.
    Retorna la lista de vértices en orden topológico, 
    o None si el grafo contiene ciclos.
    """
    adj = {i: [] for i in range(V)}
    for e in lista_aristas:
        adj[e.origen].append(e.destino)
        
    visitado = [0] * V # 0: no visitado, 1: visitando (en la pila actual), 2: visitado completamente
    stack = []
    
    def dfs(v):
        visitado[v] = 1
        for u in adj[v]:
            if visitado[u] == 1: # Encontramos un nodo que estamos visitando actualmente -> Ciclo
                return False
            if visitado[u] == 0:
                if not dfs(u):
                    return False
        visitado[v] = 2
        stack.append(v)
        return True
        
    for i in range(V):
        if visitado[i] == 0:
            if not dfs(i):
                return None # Hay un ciclo, no es un DAG
                
    return stack[::-1]

def dag_shortest_path(V, origen, lista_aristas, guardar_historial=False):
    """
    Ejecuta el algoritmo de camino más corto en un Grafo Acíclico Dirigido (DAG).
    """
    dist = [INF] * V
    padre = [-1] * V
    
    historial = []
    
    def capturar_estado(arista_actual=None, terminar=False):
        if not guardar_historial: return
        estado_nodos = {}
        for i in range(V):
            if terminar:
                estado_nodos[i] = "#000000" if dist[i] < INF else "#ffffff"
            elif dist[i] < INF:
                estado_nodos[i] = "#888888" # Gris (descubierto)
            else:
                estado_nodos[i] = "#ffffff" # Blanco (no descubierto)
                
        historial.append({
            "nodos": estado_nodos,
            "arista_actual": arista_actual,
            "distancias": list(dist),
            "predecesores": list(padre)
        })

    # Paso 1: Obtener el orden topológico
    lista_topologica = ordenamiento_topologico(V, lista_aristas)
    
    if lista_topologica is None:
        if guardar_historial: return None, None, []
        return None, None # Indica que hay ciclo

    # Paso 2: Inicializar distancias
    dist[origen] = 0
    capturar_estado()
    
    adj = {i: [] for i in range(V)}
    for e in lista_aristas:
        adj[e.origen].append(e)

    # Paso 3: Relajar las aristas en ese orden
    for u in lista_topologica:
        for e in adj[u]:
            v = e.destino
            capturar_estado((u, v))
            if dist[u] != INF and dist[u] + e.peso < dist[v]:
                dist[v] = dist[u] + e.peso
                padre[v] = u
                capturar_estado((u, v))

    if guardar_historial:
        capturar_estado(terminar=True)
        return dist, padre, historial
        
    return dist, padre

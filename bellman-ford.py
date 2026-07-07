class arista:
    def __init__(self, origen, destino, peso):
        self.origen = origen
        self.destino = destino
        self.peso = peso

INF = 9999

def bellman_ford(V, origen, lista_aristas, guardar_historial=False):
    """
    Ejecuta el algoritmo de Bellman-Ford para encontrar los caminos más cortos
    desde un nodo origen hacia el resto de los nodos, permitiendo aristas con
    peso negativo y detectando ciclos negativos.
    
    Args:
        V (int): Número total de vértices en el grafo.
        origen (int): Nodo de inicio.
        lista_aristas (list[arista]): Lista con todas las aristas del grafo.
        guardar_historial (bool): Habilita la captura del estado interno para animación.
        
    Returns:
        tuple: (distancias, predecesores, historial_opcional) o (None, None, [])
               si se detecta un ciclo de costo negativo.
    """
    dist = [INF] * V
    padre = [-1] * V
    dist[origen] = 0
    
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

    capturar_estado()

    # Relajación de aristas:
    # Según la teoría, el camino más corto simple en un grafo de V vértices
    # puede tener como máximo V-1 aristas. Por lo tanto, iteramos V-1 veces.
    for _ in range(V - 1):
            for e in lista_aristas:
                 capturar_estado((e.origen, e.destino))
                 if dist[e.origen] != INF and dist[e.origen] + e.peso < dist[e.destino]:
                      dist[e.destino] = dist[e.origen] + e.peso
                      padre[e.destino] = e.origen
                      capturar_estado((e.origen, e.destino))

    # Detección de ciclos negativos:
    # Si después de V-1 iteraciones aún podemos relajar una arista,
    # significa que existe un ciclo de costo negativo en el grafo.
    for e in lista_aristas:
         if dist[e.origen] != INF and dist[e.origen] + e.peso < dist[e.destino]:
              if guardar_historial: return None, None, []
              return None, None
         
    if guardar_historial:
        capturar_estado(terminar=True)
        return dist, padre, historial
        
    return dist, padre
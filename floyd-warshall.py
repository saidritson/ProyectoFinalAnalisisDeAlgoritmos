INF = float('inf')

def print_matrix(matrix, step_name):
    print(f"--- {step_name} ---")
    print("     A    B    C    D")
    for i, row in enumerate(matrix):
        row_str = f"{chr(65+i)} |"
        for val in row:
            if val == INF:
                row_str += f"{'INF':>4}"
            else:
                row_str += f"{val:>4}"
        print(row_str)
    print()

def floyd_warshall(graph, guardar_historial=False):
    """
    Ejecuta el algoritmo de Floyd-Warshall para encontrar los caminos más cortos
    entre todos los pares de vértices en un grafo dirigido y ponderado.
    
    Args:
        graph (list[list[int]]): Matriz de adyacencia del grafo, donde graph[i][j]
                                 es el peso de la arista (i, j). INF si no existe.
        guardar_historial (bool): Habilita la captura del estado de la matriz.
        
    Returns:
        tuple: (matriz_distancias, matriz_predecesores, historial_opcional)
    """
    V = len(graph)
    
    historial = []
    
    def capturar_estado(k, i, j):
        if not guardar_historial: return
        estado_nodos = {}
        for n in range(V):
            estado_nodos[n] = "#000000"
            
        if k != -1: estado_nodos[k] = "#0055ff" # Azul (puente)
        if i != -1: estado_nodos[i] = "#00ff00" # Verde (origen)
        if j != -1: estado_nodos[j] = "#FFD700" # Dorado (destino)
        
        # Capturamos la matriz COMPLETA de distancias (VxV)
        dist_matrix = [row[:] for row in dist]
        
        historial.append({
            "nodos": estado_nodos,
            "arista_actual": None,
            "distancias": dist_matrix,
            "predecesores": [],
            "fw_info": f"Puente: {chr(65+k)} | Origen: {chr(65+i)} | Destino: {chr(65+j)}" if k != -1 else "Inicialización"
        })
    
    # 1. Preparación (Matriz Inicial)
    dist = [row[:] for row in graph]
    
    # nxt[i][j] guardará el siguiente nodo en el camino más corto desde i hasta j.
    nxt = [[-1 if graph[i][j] == INF or i == j else j for j in range(V)] for i in range(V)]
    
    # print_matrix(dist, "Matriz Inicial (k = -1)")
    capturar_estado(-1, -1, -1)
    
    # 2. Iteración sobre nodos puente (k)
    for k in range(V):
        for i in range(V):
            for j in range(V):
                capturar_estado(k, i, j)
                # Relajación: Verificar si la ruta i -> k -> j es más óptima
                if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
                    capturar_estado(k, i, j)
                    
        # print_matrix(dist, f"Iteración k = {k}")

    if guardar_historial:
        return dist, nxt, historial
    return dist, nxt

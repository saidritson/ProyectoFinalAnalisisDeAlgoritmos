import networkx as nx

def nx_to_dijkstra_grafo(G):
    import dijkstra
    n = G.number_of_nodes()
    grafo = dijkstra.Grafo(n)
    for u, v, data in G.edges(data=True):
        grafo.matriz[u][v] = data['weight']
    return grafo

def nx_to_bellman_ford(G):
    import importlib
    bellman_ford = importlib.import_module("bellman-ford")
    aristas = []
    for u, v, data in G.edges(data=True):
        aristas.append(bellman_ford.arista(u, v, data['weight']))
    return G.number_of_nodes(), aristas

def nx_to_floyd_warshall(G):
    import importlib
    floyd_warshall = importlib.import_module("floyd-warshall")
    n = G.number_of_nodes()
    matrix = [[floyd_warshall.INF for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u, v, data in G.edges(data=True):
        matrix[u][v] = data['weight']
    return matrix

def nx_to_astar(G):
    grafo = {}
    coordenadas = {}
    for node, data in G.nodes(data=True):
        grafo[node] = {}
        coordenadas[node] = (data['x'], data['y'])
    
    for u, v, data in G.edges(data=True):
        grafo[u][v] = data['weight']
    
    return grafo, coordenadas

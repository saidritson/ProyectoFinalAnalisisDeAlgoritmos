import networkx as nx
import random

def generate_random_graph(num_nodes=10, prob_edge=0.15, max_weight=20):
    G = nx.DiGraph()
    
    # Primero agregamos los nodos
    for i in range(num_nodes):
        G.add_node(i, label=chr(65 + i))
        
        
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < prob_edge:
                weight = random.randint(1, max_weight)
                G.add_edge(i, j, weight=weight)
                
    # Asegurar que el grafo este conectado
    for i in range(num_nodes - 1):
        if not G.has_edge(i, i+1):
            G.add_edge(i, i+1, weight=random.randint(1, max_weight))
            
    # Calcular posiciones con Spring Layout para que se vea bien
    pos = nx.spring_layout(G, seed=42)
    for node, coords in pos.items():
        # Escalar coordenadas para PyVis y A*
        G.nodes[node]['x'] = float(coords[0]) * 500
        G.nodes[node]['y'] = float(coords[1]) * 500
        
    return G

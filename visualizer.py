from pyvis.network import Network

def visualize_graph(G, path=None, filename="graph.html", state=None):
    # Crear red PyVis
    net = Network(height="700px", width="100%", directed=True, bgcolor="#222222", font_color="white")
    
    # Configurar fisicas para que sean estaticas
    net.toggle_physics(False)
    
    # Agregar nodos
    for node, data in G.nodes(data=True):
        label = f"{data['label']} ({node})"
        
        color = "#97c2fc" # Azul claro por defecto
        size = 15
        x = data.get('x', 0)
        y = data.get('y', 0)
        
        # Modo Animación
        if state and "nodos" in state:
            color = state["nodos"].get(node, color)
            # Agregar distancias a la etiqueta
            if "distancias" in state:
                dist_val = state["distancias"][node]
                # Si no es una matriz 2D (es decir, no es Floyd-Warshall), dibujamos el label
                if not isinstance(dist_val, list):
                    if dist_val < 9999: # 9999 is INF
                        import sys
                        if dist_val < sys.maxsize:
                            label += f"\nDist: {dist_val}"
            
        # Resaltar nodos de la ruta (modo final)
        elif path and node in path:
            color = "#ff4b4b" # Rojo para la ruta
            size = 25
            if node == path[0]:
                label = f"Inicio: {label}"
                color = "#00ff00"
            elif node == path[-1]:
                label = f"Fin: {label}"
                color = "#FFD700" # Dorado
                
        net.add_node(node, label=label, title=label, color=color, size=size, x=x, y=y, physics=False)
        
    # Agregar aristas
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        color = "#666666"
        width = 1
        
        # Modo Animación
        if state and "arista_actual" in state and state["arista_actual"]:
            au, av = state["arista_actual"]
            if u == au and v == av:
                color = "#0055ff"
                width = 4
        # Resaltar aristas de la ruta (modo final)
        elif path:
            for i in range(len(path)-1):
                if path[i] == u and path[i+1] == v:
                    color = "#ff4b4b"
                    width = 4
                    break
                    
        net.add_edge(u, v, title=f"Costo: {weight}", label=str(weight), color=color, width=width)
        
    # Generar HTML
    net.save_graph(filename)
    
    # Leer contenido HTML
    with open(filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    return html_content

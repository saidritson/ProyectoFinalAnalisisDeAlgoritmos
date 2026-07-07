import streamlit as st # Forzar recarga completa de modulos
import streamlit.components.v1 as components
import time
import pandas as pd
import graph_generator
import adapters
import visualizer
import importlib

# Forzar recarga de módulos importados para evitar errores de caché
importlib.reload(visualizer)
importlib.reload(adapters)
import sys
import importlib

# Importar los algoritmos
import dijkstra
importlib.reload(dijkstra)
bellman_ford = importlib.import_module("bellman-ford")
importlib.reload(bellman_ford)
floyd_warshall = importlib.import_module("floyd-warshall")
importlib.reload(floyd_warshall)
a_star = importlib.import_module("a-star")
importlib.reload(a_star)

st.set_page_config(page_title="Sistema Inteligente de Rutas", layout="wide")

st.title("🗺️ Sistema Inteligente de Rutas usando Grafos")
st.markdown("Proyecto 3 - Análisis de Algoritmos. Encuentra la ruta más corta entre ciudades y compara el rendimiento de los algoritmos.")

# --- Session State ---
if 'graph' not in st.session_state:
    st.session_state.graph = graph_generator.generate_random_graph(10)
    
if 'selected_path' not in st.session_state:
    st.session_state.selected_path = None

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuración")

if st.sidebar.button("Generar Nuevo Grafo Aleatorio"):
    st.session_state.graph = graph_generator.generate_random_graph(10)
    st.session_state.selected_path = None
    st.rerun()
    
st.sidebar.divider()

G = st.session_state.graph
nodes = list(G.nodes(data=True))
node_options = {n: f"{d['label']} ({n})" for n, d in nodes}

origen = st.sidebar.selectbox("Ciudad Origen", options=list(node_options.keys()), format_func=lambda x: node_options[x])
destino = st.sidebar.selectbox("Ciudad Destino", options=list(node_options.keys()), format_func=lambda x: node_options[x], index=min(1, len(node_options)-1))

st.sidebar.subheader("Modo de Operación")
modo = st.sidebar.radio("Selecciona el modo", ["Comparar Algoritmos", "Animación Paso a Paso"])

if modo == "Comparar Algoritmos":
    st.sidebar.subheader("Seleccionar Algoritmos")
    use_dijkstra = st.sidebar.checkbox("Dijkstra", value=True)
    use_bellman = st.sidebar.checkbox("Bellman-Ford", value=True)
    use_floyd = st.sidebar.checkbox("Floyd-Warshall", value=False)
    use_astar = st.sidebar.checkbox("A* (A-Star)", value=False)

    if st.sidebar.button("Calcular Rutas y Comparar", type="primary"):
        if origen == destino:
            st.sidebar.error("El origen y destino deben ser diferentes.")
        else:
            results = []
            path_to_draw = None
        
            # --- Dijkstra ---
            if use_dijkstra:
                start_time = time.perf_counter()
                d_grafo = adapters.nx_to_dijkstra_grafo(G)
                distancias, predecesores = d_grafo.dijkstra(origen)
                end_time = time.perf_counter()
            
                costo = distancias[destino]
                camino = []
                if costo != sys.maxsize:
                    nodo = destino
                    while nodo != -1:
                        camino.append(nodo)
                        nodo = predecesores[nodo]
                    camino.reverse()
            
                if not path_to_draw and camino:
                    path_to_draw = camino
                
                results.append({
                    "Algoritmo": "Dijkstra",
                    "Tiempo (ms)": (end_time - start_time) * 1000,
                    "Costo": costo if costo != sys.maxsize else "Inalcanzable",
                    "Ruta": " -> ".join([node_options[n] for n in camino]) if camino else "Sin ruta"
                })
            
            # --- Bellman-Ford ---
            if use_bellman:
                start_time = time.perf_counter()
                V, aristas = adapters.nx_to_bellman_ford(G)
                dist, padre = bellman_ford.bellman_ford(V, origen, aristas)
                end_time = time.perf_counter()
            
                if dist is None:
                    st.error("Ciclo negativo detectado por Bellman-Ford")
                else:
                    costo = dist[destino]
                    camino = []
                    if costo != bellman_ford.INF:
                        nodo = destino
                        while nodo != -1 and nodo != origen:
                            camino.append(nodo)
                            nodo = padre[nodo]
                        if nodo == origen:
                            camino.append(origen)
                            camino.reverse()
                        else:
                            camino = [] # Si no hay camino
                        
                    if not path_to_draw and camino:
                        path_to_draw = camino
                    
                    results.append({
                        "Algoritmo": "Bellman-Ford",
                        "Tiempo (ms)": (end_time - start_time) * 1000,
                        "Costo": costo if costo != bellman_ford.INF else "Inalcanzable",
                        "Ruta": " -> ".join([node_options[n] for n in camino]) if camino else "Sin ruta"
                    })
                
            # --- Floyd-Warshall ---
            if use_floyd:
                start_time = time.perf_counter()
                matrix = adapters.nx_to_floyd_warshall(G)
                dist_matrix, nxt_matrix = floyd_warshall.floyd_warshall(matrix)
                end_time = time.perf_counter()
            
                costo = dist_matrix[origen][destino]
                camino = []
                if costo != floyd_warshall.INF:
                    camino = [origen]
                    u = origen
                    v = destino
                    while u != v:
                        u = nxt_matrix[u][v]
                        if u == -1:
                            camino = []
                            break
                        camino.append(u)
                    
                if not path_to_draw and camino:
                    path_to_draw = camino
                
                results.append({
                    "Algoritmo": "Floyd-Warshall",
                    "Tiempo (ms)": (end_time - start_time) * 1000,
                    "Costo": costo if costo != floyd_warshall.INF else "Inalcanzable",
                    "Ruta": " -> ".join([node_options[n] for n in camino]) if camino else "Sin ruta"
                })
            
            # --- A-Star ---
            if use_astar:
                start_time = time.perf_counter()
                grafo_astar, coord = adapters.nx_to_astar(G)
                camino, costo = a_star.aEstrella(origen, destino, grafo_astar, coord)
                end_time = time.perf_counter()
            
                if not path_to_draw and camino:
                    path_to_draw = camino
                
                results.append({
                    "Algoritmo": "A*",
                    "Tiempo (ms)": (end_time - start_time) * 1000,
                    "Costo": costo if costo != a_star.INF else "Inalcanzable",
                    "Ruta": " -> ".join([node_options[n] for n in camino]) if camino else "Sin ruta"
            })
            
        st.session_state.results = results
        st.session_state.selected_path = path_to_draw

if modo == "Animación Paso a Paso":
    st.sidebar.subheader("Seleccionar Algoritmo para Animar")
    algo_anim = st.sidebar.selectbox("Algoritmo", ["Dijkstra", "Bellman-Ford", "Floyd-Warshall", "A* (A-Star)"])
    
    if st.sidebar.button("Generar Animación", type="primary"):
        if origen == destino:
            st.sidebar.error("El origen y destino deben ser diferentes.")
        else:
            if algo_anim == "Dijkstra":
                d_grafo = adapters.nx_to_dijkstra_grafo(G)
                _, _, historial = d_grafo.dijkstra(origen, guardar_historial=True)
            elif algo_anim == "Bellman-Ford":
                V, aristas = adapters.nx_to_bellman_ford(G)
                _, _, historial = bellman_ford.bellman_ford(V, origen, aristas, guardar_historial=True)
            elif algo_anim == "Floyd-Warshall":
                matrix = adapters.nx_to_floyd_warshall(G)
                _, _, historial = floyd_warshall.floyd_warshall(matrix, guardar_historial=True)
            elif algo_anim == "A* (A-Star)":
                grafo_astar, coord = adapters.nx_to_astar(G)
                _, _, historial = a_star.aEstrella(origen, destino, grafo_astar, coord, guardar_historial=True)
                
            st.session_state.historial = historial
            st.session_state.anim_paso = 0
            if "slider_paso" in st.session_state:
                st.session_state.slider_paso = 0

# --- Main Content ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualización del Grafo")
    path_to_draw = st.session_state.get('selected_path')
    
    if modo == "Animación Paso a Paso" and 'historial' in st.session_state and st.session_state.historial:
        total_pasos = len(st.session_state.historial) - 1
        
        if "slider_paso" not in st.session_state:
            st.session_state.slider_paso = 0
            
        # Botones de navegacion
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn1:
            if st.button("⬅️ Anterior"):
                st.session_state.slider_paso = max(0, st.session_state.slider_paso - 1)
        with col_btn3:
            if st.button("Siguiente ➡️"):
                st.session_state.slider_paso = min(total_pasos, st.session_state.slider_paso + 1)
                
        paso_actual = st.slider("Paso de la iteración", 0, total_pasos, key="slider_paso")
        st.session_state.anim_paso = paso_actual
        
        estado_actual = st.session_state.historial[paso_actual]
        html_content = visualizer.visualize_graph(st.session_state.graph, None, "graph_anim.html", estado_actual)
    else:
        html_content = visualizer.visualize_graph(st.session_state.graph, path_to_draw)
        
    components.html(html_content, height=720)
    
    # Leyenda de Colores
    st.markdown("### Leyenda de Colores")
    if modo == "Animación Paso a Paso":
        if algo_anim == "Floyd-Warshall":
            st.markdown("🟢 **Verde:** Ciudad Origen actual | 🟡 **Dorado:** Ciudad Destino actual | 🔵 **Azul:** Ciudad Puente (escala)")
        else:
            st.markdown("⚪ **Blanco:** No descubierto | 🔘 **Gris:** Descubierto (en proceso) | ⚫ **Negro:** Totalmente procesado | 🔵 **Azul:** Evaluando actualmente")
    else:
        st.markdown("🔴 **Rojo:** Ruta más corta encontrada | 🟢 **Verde:** Ciudad Origen | 🟡 **Dorado:** Ciudad Destino")

with col2:
    if modo == "Animación Paso a Paso":
        st.subheader("Información del Paso")
        if 'historial' in st.session_state and st.session_state.historial:
            estado = st.session_state.historial[st.session_state.anim_paso]
            st.markdown(f"**Paso:** {st.session_state.anim_paso} de {len(st.session_state.historial)-1}")
            
            if "fw_info" in estado:
                st.info(estado["fw_info"])
            
            if estado["arista_actual"]:
                u, v = estado["arista_actual"]
                st.markdown(f"**Evaluando arista:** {node_options[u]} -> {node_options[v]}")
            elif not "fw_info" in estado:
                st.markdown("**Evaluando arista:** Ninguna")
                
            # Mostrar tabla de distancias
            if algo_anim == "Floyd-Warshall":
                matrix_data = estado["distancias"]
                import sys
                import pandas as pd
                cols = [chr(65+c) for c in range(len(matrix_data))]
                df_matrix = pd.DataFrame(matrix_data, columns=cols, index=cols)
                # Reemplazar infinitos por "INF" para visualización
                df_matrix = df_matrix.replace([sys.maxsize, 9999, float('inf')], "INF")
                st.dataframe(df_matrix, use_container_width=True, height=400)
            else:
                dist_data = []
                import sys
                import pandas as pd
                for i, dist in enumerate(estado["distancias"]):
                    dist_str = "INF" if dist == sys.maxsize or dist == 9999 or dist == float('inf') else str(dist)
                    dist_data.append({"Ciudad": node_options[i], "Distancia": dist_str})
                st.dataframe(pd.DataFrame(dist_data), use_container_width=True, height=400)
        else:
            st.info("Presiona 'Generar Animación' en la barra lateral para comenzar.")
            
    else:
        st.subheader("📊 Resultados y Tiempos")
    if hasattr(st.session_state, 'results') and st.session_state.results:
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df.drop(columns=["Ruta"]), use_container_width=True)
        
        st.subheader("Tiempos de Ejecución")
        st.bar_chart(df.set_index("Algoritmo")["Tiempo (ms)"])
        
        # Determinar cual algoritmo fue mas rapido
        if len(df) > 1:
            fastest_alg = df.loc[df["Tiempo (ms)"].idxmin()]["Algoritmo"]
            st.success(f"🏆 El algoritmo más rápido fue **{fastest_alg}**")
            
        st.info(f"**Ruta encontrada:**\n{df.iloc[0]['Ruta']}")
    else:
        st.info("Selecciona un Origen, un Destino y los Algoritmos en la barra lateral para ver los resultados.")

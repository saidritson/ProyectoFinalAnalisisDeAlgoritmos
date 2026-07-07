import sys

class Grafo:
    def __init__(self, total_nodos):
        self.total_nodos = total_nodos
        # Creamos la matriz de adyacencia llena de ceros (sin conexiones)
        self.matriz = [[0 for columna in range(total_nodos)]
                       for fila in range(total_nodos)]
        
    def nombre_del_nodo(self, indice):
        """Convierte un indice (0, 1, 2...) al nombre del nodo ('A', 'B', 'C'...)."""
        return chr(indice + 65)  # 65 = 'A' en ASCII
    
    def buscar_nodo_mas_cercano(self, distancias, visitado):
        """
        Busca el nodo NO visitado que tenga la menor distancia acumulada.
        Es como preguntarse: "De todos los nodos que me faltan, cual es el mas cercano?"
        """
        distancia_minima = sys.maxsize
        nodo_mas_cercano = -1
        for i in range(self.total_nodos):
            if not visitado[i] and distancias[i] < distancia_minima:
                distancia_minima = distancias[i]
                nodo_mas_cercano = i
        return nodo_mas_cercano
    
    def reconstruir_camino(self, predecesor, origen, destino):
        """
        Reconstruye el camino mas corto desde el origen hasta un destino,
        siguiendo los predecesores hacia atras.
        """
        if destino == origen:
            return self.nombre_del_nodo(origen)
        camino = []
        nodo = destino
        while nodo != -1:
            camino.append(self.nombre_del_nodo(nodo))
            nodo = predecesor[nodo]
        camino.reverse()
        return " -> ".join(camino)
    
    def imprimir_estado(self, distancias, visitado):
        """Imprime el estado actual de las distancias y nodos visitados."""
        print("  Nodo   Distancia   Visitado")
        print("  ----   ---------   --------")
        for i in range(self.total_nodos):
            dist = "INF" if distancias[i] == sys.maxsize else str(distancias[i])
            vis = "[X]" if visitado[i] else "[ ]"
            print(f"   {self.nombre_del_nodo(i)}       {dist:<5}       {vis}")

    def dijkstra(self, nodo_origen, guardar_historial=False):
        """
        Algoritmo de Dijkstra:
        Encuentra la distancia mas corta desde un nodo origen hacia todos los demas.
        """
        INFINITO = sys.maxsize
        # =============================================
        distancias = [INFINITO] * self.total_nodos
        visitado = [False] * self.total_nodos
        predecesor = [-1] * self.total_nodos
        distancias[nodo_origen] = 0
        
        print("Estado inicial:")
        self.imprimir_estado(distancias, visitado)
        
        historial = []
        
        def capturar_estado(nodo_actual=None, arista_actual=None):
            """Captura el estado de los nodos (colores) y estructuras de datos."""
            if not guardar_historial: return
            estado_nodos = {}
            for i in range(self.total_nodos):
                if visitado[i]:
                    estado_nodos[i] = "#000000"
                elif distancias[i] < INFINITO:
                    estado_nodos[i] = "#888888"
                else:
                    estado_nodos[i] = "#ffffff"
            
            if nodo_actual is not None:
                estado_nodos[nodo_actual] = "#0055ff"
                
            historial.append({
                "nodos": estado_nodos,
                "arista_actual": arista_actual,
                "distancias": list(distancias),
                "predecesores": list(predecesor)
            })
            
        capturar_estado()

        for iteracion in range(1, self.total_nodos):
            nodo_actual = self.buscar_nodo_mas_cercano(distancias, visitado)
            if nodo_actual == -1: break
            visitado[nodo_actual] = True
            capturar_estado(nodo_actual)
            
            print(f"\n--- Iteracion {iteracion}: Procesando nodo "
                  f"{self.nombre_del_nodo(nodo_actual)} "
                  f"(distancia = {distancias[nodo_actual]}) ---")
            
            for vecino in range(self.total_nodos):
                peso_arista = self.matriz[nodo_actual][vecino]
                existe_arista = (peso_arista != 0)
                no_fue_visitado = (not visitado[vecino])
                es_alcanzable = (distancias[nodo_actual] != INFINITO)
                
                if existe_arista and no_fue_visitado and es_alcanzable:
                    capturar_estado(nodo_actual, (nodo_actual, vecino))
                    nueva_distancia = distancias[nodo_actual] + peso_arista
                    
                    if nueva_distancia < distancias[vecino]:
                        distancia_anterior = "INF" if distancias[vecino] == INFINITO else str(distancias[vecino])
                        print(f"  {self.nombre_del_nodo(nodo_actual)}"
                              f" -> {self.nombre_del_nodo(vecino)}"
                              f" : {distancias[nodo_actual]} + {peso_arista}"
                              f" = {nueva_distancia}"
                              f" < {distancia_anterior}"
                              f"  =>  distancia[{self.nombre_del_nodo(vecino)}] = {nueva_distancia}")
                        distancias[vecino] = nueva_distancia
                        predecesor[vecino] = nodo_actual
                        capturar_estado(nodo_actual, (nodo_actual, vecino))
            self.imprimir_estado(distancias, visitado)
        # =============================================
        # PASO 3: MOSTRAR RESULTADOS
        # =============================================
        print("\n===================================================")
        print("  RESULTADO FINAL")
        print("===================================================\n")
        print("Nodo    Distancia    Camino mas corto")
        print("----    ---------    ----------------")
        for i in range(self.total_nodos):
            camino = self.reconstruir_camino(predecesor, nodo_origen, i)
            print(f" {self.nombre_del_nodo(i)}         {distancias[i]}          {camino}")
            
        if guardar_historial:
            capturar_estado()
            return distancias, predecesor, historial
            
        return distancias, predecesor

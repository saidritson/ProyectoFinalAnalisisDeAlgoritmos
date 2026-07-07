# Visualizador Interactivo de Algoritmos de Búsqueda de Rutas (Pathfinding) 🗺️

Este proyecto es una aplicación web interactiva desarrollada en Python utilizando Streamlit. Su objetivo es visualizar y comparar el funcionamiento y rendimiento de los cuatro algoritmos de búsqueda de rutas más importantes de la Teoría de Grafos.

## Algoritmos Implementados 🧠
1. **Dijkstra:** Encuentra el camino más corto desde un nodo de origen hacia todos los demás nodos en grafos con pesos positivos.
2. **Bellman-Ford:** Encuentra el camino más corto manejando aristas con pesos negativos y es capaz de detectar ciclos negativos.
3. **Floyd-Warshall:** Encuentra las distancias mínimas entre todos los pares de nodos del grafo utilizando programación dinámica (Matriz VxV).
4. **A* (A-Star):** Encuentra la ruta más rápida hacia un destino específico utilizando una heurística (distancia euclidiana) para guiar la búsqueda y optimizar el tiempo.

## Requisitos Previos ⚙️
Para correr este proyecto en tu máquina local, necesitas tener **Python 3.8+** instalado. Además, deberás instalar las siguientes librerías de Python:

- `streamlit` (Para la interfaz web)
- `networkx` (Para la creación y manipulación de grafos)
- `pyvis` (Para la visualización interactiva de nodos)
- `pandas` (Para las tablas de datos y matrices)

Puedes instalar todas las dependencias corriendo el siguiente comando en tu terminal:
```bash
pip install streamlit networkx pyvis pandas
```

## ¿Cómo ejecutar el proyecto? 🚀

1. Clona este repositorio o descarga los archivos en una carpeta de tu computadora.
2. Abre una terminal (o consola de comandos) y navega hasta la carpeta del proyecto.
3. Ejecuta el siguiente comando para levantar el servidor de Streamlit:
```bash
streamlit run app.py
```
4. Se abrirá automáticamente una pestaña en tu navegador web por defecto (generalmente en `http://localhost:8501`). Si no se abre sola, copia y pega esa dirección en tu navegador.

## Modos de Uso 🎮

La aplicación cuenta con dos modos principales que puedes seleccionar desde el menú lateral izquierdo:

* **Modo Comparar Algoritmos:** Te permite seleccionar los algoritmos que deseas medir. Genera un grafo, calcula las rutas y te muestra una tabla comparativa con los tiempos de ejecución en milisegundos y los costos de las rutas para saber cuál es el más eficiente.
* **Modo Animación Paso a Paso:** Al seleccionar un algoritmo específico, puedes utilizar un deslizador (slider) para ver la ejecución iteración por iteración. Verás cómo cambian de color los nodos (Blanco = No descubierto, Gris = Procesando, Negro = Completado), las aristas que se evalúan y cómo se actualizan las distancias en tiempo real (mostrando tablas o matrices dependiendo del algoritmo).

## Notas para el equipo 📝
El código fuente incluye documentación y *docstrings* formales en cada uno de los algoritmos (`dijkstra.py`, `bellman-ford.py`, etc.). Pueden abrir los archivos para leer una explicación matemática de cómo se realiza la relajación de aristas y la captura de historial.
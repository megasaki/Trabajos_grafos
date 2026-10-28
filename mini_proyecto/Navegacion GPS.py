import heapq

class SistemaGPS:
    def __init__(self):
        # Estructura de grafo ponderado: ciudad -> {destino: tiempo_en_minutos}
        self.grafo: dict[str, dict[str, float]] = {}

    def agregar_ciudad(self, nombre: str) -> bool:
        """Agrega una ciudad aislada si no existe previamente en el sistema."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la ciudad no puede estar vacio.")
        if nombre not in self.grafo:
            self.grafo[nombre] = {}
            return True
        return False

    def agregar_ruta(self, origen: str, destino: str, tiempo: float) -> None:
        """Agrega o actualiza una autopista dirigida entre dos ciudades con su tiempo en minutos."""
        origen = origen.strip()
        destino = destino.strip()
        
        if tiempo < 0:
            raise ValueError("El tiempo de recorrido en minutos no puede ser negativo.")
        
        self.agregar_ciudad(origen)
        self.agregar_ciudad(destino)
        self.grafo[origen][destino] = tiempo

    def obtener_ciudades(self) -> list[str]:
        """Retorna la lista de todas las ciudades registradas."""
        return list(self.grafo.keys())

    def consultar_ruta_mas_rapida(self, inicio: str, fin: str) -> tuple[float, list[str]]:
        """
        Calcula la ruta mas rapida entre dos ciudades utilizando el algoritmo de Dijkstra.
        Retorna una tupla con (tiempo_total_minutos, lista_exacta_de_ciudades).
        """
        inicio = inicio.strip()
        fin = fin.strip()

        if inicio not in self.grafo or fin not in self.grafo:
            raise KeyError(f"Una o ambas ciudades ('{inicio}', '{fin}') no estan registradas en el sistema.")

        distancias: dict[str, float] = {nodo: float('inf') for nodo in self.grafo}
        predecesores: dict[str, str | None] = {nodo: None for nodo in self.grafo}
        distancias[inicio] = 0.0
        
        # Cola de prioridad que almacena tuplas: (tiempo_acumulado, ciudad_actual)
        cola = [(0.0, inicio)]

        while cola:
            tiempo_actual, actual = heapq.heappop(cola)

            if actual == fin:
                break

            if tiempo_actual > distancias[actual]:
                continue

            for vecino, peso in self.grafo.get(actual, {}).items():
                nuevo_tiempo = tiempo_actual + peso
                if nuevo_tiempo < distancias[vecino]:
                    distancias[vecino] = nuevo_tiempo
                    predecesores[vecino] = actual
                    heapq.heappush(cola, (nuevo_tiempo, vecino))

        if distancias[fin] == float('inf'):
            return float('inf'), []

        # Reconstruccion del recorrido completo (camino exacto)
        ruta = []
        actual = fin
        while actual is not None:
            ruta.append(actual)
            actual = predecesores[actual]
        ruta.reverse()

        return distancias[fin], ruta


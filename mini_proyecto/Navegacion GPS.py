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

def interfaz_consola():
    gps = SistemaGPS()
    
    # Carga de datos iniciales de prueba
    gps.agregar_ruta("Managua", "Tipitapa", 25.0)
    gps.agregar_ruta("Managua", "Masaya", 30.0)
    gps.agregar_ruta("Masaya", "Granada", 20.0)
    gps.agregar_ruta("Tipitapa", "Juigalpa", 90.0)

    while True:
        print("\n========================================")
        print("    SISTEMA DE NAVEGACION GPS - MENU    ")
        print("========================================")
        print("1. Ver todas las ciudades y rutas")
        print("2. Agregar nueva ruta o ciudad")
        print("3. Consultar ruta mas rapida")
        print("4. Salir")
        
        opcion = input("Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            ciudades = gps.obtener_ciudades()
            if not ciudades:
                print("\nNo hay ciudades registradas en el sistema.")
            else:
                print("\n--- MAPA DE CIUDADES Y AUTOPISTAS ---")
                for ciudad, destinos in gps.grafo.items():
                    print(f"Ciudad: {ciudad}")
                    if not destinos:
                        print("  -> Sin autopistas salientes registradas.")
                    for dest, tiempo in destinos.items():
                        print(f"  -> Conecta con {dest} [Tiempo: {tiempo} minutos]")

        elif opcion == "2":
            try:
                print("\n--- AGREGAR NUEVA RUTA ---")
                origen = input("Ingrese ciudad de origen: ").strip()
                destino = input("Ingrese ciudad de destino: ").strip()
                tiempo_str = input("Ingrese el tiempo de viaje en minutos: ").strip()
                
                tiempo = float(tiempo_str)
                gps.agregar_ruta(origen, destino, tiempo)
                print("\nRuta agregada exitosamente al sistema.")
            except ValueError as e:
                print(f"\nError de validacion: {e}")

        elif opcion == "3":
            try:
                print("\n--- CONSULTAR RUTA MAS RAPIDA ---")
                origen = input("Ingrese ciudad de origen: ").strip()
                fin = input("Ingrese ciudad de destino: ").strip()
                
                tiempo_total, ruta = gps.consultar_ruta_mas_rapida(origen, fin)
                
                if tiempo_total == float('inf'):
                    print(f"\nNo existe una ruta posible entre '{origen}' y '{fin}'.")
                else:
                    print(f"\nResultado de la busqueda:")
                    print(f"  - Tiempo total estimado: {tiempo_total} minutos")
                    print(f"  - Recorrido completo: {' -> '.join(ruta)}")
            except (KeyError, ValueError) as e:
                print(f"\nError: {e}")

        elif opcion == "4":
            print("\nSaliendo del Sistema de Navegacion GPS. Hasta pronto.")
            break
        else:
            print("\nOpcion invalida. Por favor, seleccione un numero del 1 al 4.")

if __name__ == "__main__":
    interfaz_consola()
class GrafoDirigidoDFS:
    def __init__(self):
        self.adyacencia: dict[str, list[str]] = {}

    def agregar_arista(self, origen: str, destino: str) -> None:
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        if destino not in self.adyacencia:
            self.adyacencia[destino] = []
        if destino not in self.adyacencia[origen]:
            self.adyacencia[origen].append(destino)

    def dfs_iterativo(self, inicio: str) -> list[str]:
        """Realiza un recorrido en profundidad (DFS) iterativo usando una pila."""
        if inicio not in self.adyacencia:
            return []
            
        visitados = set()
        orden = []
        pila = [inicio]
        
        while pila:
            actual = pila.pop()
            if actual not in visitados:
                visitados.add(actual)
                orden.append(actual)
                # Extender en orden inverso para respetar la precedencia LIFO
                vecinos = self.adyacencia.get(actual, [])
                pila.extend(reversed(vecinos))
                
        return orden

if __name__ == "__main__":
    # --- PRUEBA DEL EJERCICIO 1 ---
    g = GrafoDirigidoDFS()
    g.agregar_arista("A", "B")
    g.agregar_arista("A", "C")
    g.agregar_arista("B", "D")
    g.agregar_arista("C", "E")

    resultado = g.dfs_iterativo("A")
    print("Test [1] DFS Iterativo desde 'A':", resultado)
    # Resultado esperado: ['A', 'B', 'D', 'C', 'E'] (o similar según orden de vecinos)
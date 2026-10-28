class GrafoDirigidoCiclos:
    def __init__(self):
        self.adyacencia: dict[str, list[str]] = {}

    def agregar_arista(self, origen: str, destino: str) -> None:
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        if destino not in self.adyacencia:
            self.adyacencia[destino] = []
        if destino not in self.adyacencia[origen]:
            self.adyacencia[origen].append(destino)

    def tiene_ciclos(self) -> bool:
        """Detecta si el grafo dirigido contiene al menos un ciclo usando DFS."""
        visitados = set()
        en_camino = set()

        def dfs_visitar(nodo: str) -> bool:
            visitados.add(nodo)
            en_camino.add(nodo)

            for vecino in self.adyacencia.get(nodo, []):
                if vecino not in visitados:
                    if dfs_visitar(vecino):
                        return True
                elif vecino in en_camino:
                    return True  # Ciclo detectado

            en_camino.remove(nodo)
            return False

        for nodo in self.adyacencia:
            if nodo not in visitados:
                if dfs_visitar(nodo):
                    return True
        return False

if __name__ == "__main__":
    # --- PRUEBA DEL EJERCICIO 2 ---
    # Grafo sin ciclos (Acíclico)
    g1 = GrafoDirigidoCiclos()
    g1.agregar_arista("A", "B")
    g1.agregar_arista("B", "C")
    print("Test [2a] ¿Grafo 1 tiene ciclos?", g1.tiene_ciclos()) # Debe dar False

    # Grafo con ciclo (A -> B -> C -> A)
    g2 = GrafoDirigidoCiclos()
    g2.agregar_arista("A", "B")
    g2.agregar_arista("B", "C")
    g2.agregar_arista("C", "A")
    print("Test [2b] ¿Grafo 2 tiene ciclos?", g2.tiene_ciclos()) # Debe dar True
from typing import List, Set
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def pausa():
    input("[ENTER] para continuar...")


# valida si se puede colocar una reina en (fila, col)
def es_seguro(tablero: List[int], fila: int, col: int) -> bool:
    for i in range(fila):
        if tablero[i] == col:                 # misma columna
            return False
        if tablero[i] - i == col - fila:      # diagonal principal
            return False
        if tablero[i] + i == col + fila:      # diagonal secundaria
            return False
    return True


# dibuja el tablero en consola
def imprimir_tablero(tablero, analizadas, n, titulo="", ver_analizadas=True):
    print("\n" + titulo)
    print("    " + " ".join(str(c) for c in range(n)))
    for i in range(n):
        fila = []
        for j in range(n):
            if tablero[i] == j:
                fila.append("♛")
            elif ver_analizadas and j in analizadas[i]:
                fila.append("×")
            else:
                fila.append(".")
        print(f" {i}  " + " ".join(fila))


# el algoritmo de backtracking
def colocar_reina(tablero, fila, n, soluciones, analizadas, retrocesos):

    if fila == n:
        soluciones.append(tablero[:])
        return

    for col in range(n):

        # registra la casilla como analizada
        analizadas[fila].add(col)

        if es_seguro(tablero, fila, col):

            # coloca la reina
            tablero[fila] = col

            # limpia las marcas de las filas de abajo
            for f in range(fila + 1, n):
                analizadas[f].clear()

            # avanza a la siguiente fila
            colocar_reina(tablero, fila + 1, n, soluciones, analizadas, retrocesos)

            # muestra el tablero antes de deshacer la decision
            if retrocesos[0] < 3:
                retrocesos[0] += 1
                imprimir_tablero(tablero, analizadas, n,
                                 f"ANTES DEL RETROCESO #{retrocesos[0]} (fila {fila}, col {col})")
                pausa()

            # quita la reina (backtracking)
            


# visualizacion grafica en 3D
def visualizar_3d(sol):
    n = len(sol)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # tablero
    for i in range(n):
        for j in range(n):
            color = 0.9 if (i + j) % 2 == 0 else 0.3
            ax.bar3d(j, n - i - 1, 0, 1, 1, 0.1, color=(color, color, color))

    # reinas
    for fila, col in enumerate(sol):
        ax.bar3d(col + 0.2, n - fila - 1 + 0.2, 0.1, 0.6, 0.6, 1, color="#C44E52")

    ax.set_zticks([])
    ax.set_xlabel("Columnas")
    ax.set_ylabel("Filas")
    ax.set_title(f"Primera solucion 3D  N = {n}")
    plt.show()


def main():
    n = int(input("Ingrese N (numero de reinas): "))

    tablero = [-1] * n
    soluciones = []
    analizadas = [set() for _ in range(n)]
    retrocesos = [0]

    print(f"\nTablero de {n} x {n}.  ♛ = reina   × = casilla analizada   . = libre")
    print("Resolviendo con Backtracking...\n")
    pausa()

    colocar_reina(tablero, 0, n, soluciones, analizadas, retrocesos)

    print(f"\nTOTAL DE SOLUCIONES ENCONTRADAS: {len(soluciones)}")

    if soluciones:
        imprimir_tablero(soluciones[0], analizadas, n,
                         "PRIMERA SOLUCION:", ver_analizadas=False)
        print("\nMostrando la primera solucion en 3D...")
        visualizar_3d(soluciones[0])


if __name__ == "__main__":
    main()
"""
===============================================================================
 PROBLEMA DE LAS N-REINAS (8-REINAS GENERALIZADO) CON BACKTRACKING
 Programacion IV - Unidad 3: Tecnicas y Algoritmos para Programacion Competitiva
===============================================================================

 Cumple la consigna del examen:
   1) Ejecuta con 8 damas y, justo ANTES de que se produzca un retroceso,
      imprime todo el tablero con la solucion parcial alcanzada, identificando
      las casillas analizadas.
   2) Repite esa impresion 3 veces (las 3 primeras veces que ocurre).
   3) Al alcanzar la PRIMERA solucion, muestra el tablero en 3D (matplotlib).
   4) Al terminar, informa cuantas soluciones encontro el programa.

 Ademas esta generalizado: funciona para cualquier N en un tablero de N x N.
===============================================================================
"""

from typing import List, Set

# Cuantas fotos "antes del retroceso" se muestran (la consigna pide 3)
RETROCESOS_A_MOSTRAR = 3

# Simbolos del tablero en consola
SIMBOLO_REINA = "Q"      # reina colocada
SIMBOLO_ANALIZADA = "x"  # casilla que el algoritmo probo y descarto
SIMBOLO_VACIA = "."      # casilla que ni siquiera se analizo


# =============================================================================
# 1. UTILIDADES DE CONSOLA
# =============================================================================

def pausa(mensaje: str = "\n[ENTER] para continuar..."):
    """Detiene la ejecucion hasta que el usuario presione ENTER."""
    try:
        input(mensaje)
    except EOFError:
        pass


def imprimir_tablero(tablero: List[int],
                     analizadas: List[Set[int]],
                     n: int,
                     titulo: str = "",
                     mostrar_analizadas: bool = True):
    """
    Dibuja el tablero en consola.
      Q = reina colocada
      x = casilla analizada y descartada
      . = casilla no analizada
    'tablero[f] = c' significa: en la fila f hay una reina en la columna c.
    'tablero[f] = -1' significa: esa fila todavia no tiene reina.
    """
    if titulo:
        print("\n" + "=" * 60)
        print(titulo)
        print("=" * 60)

    # Encabezado con el numero de columna
    print("     " + "  ".join(f"{c}" for c in range(n)))

    for fila in range(n):
        celdas = []
        for col in range(n):
            if tablero[fila] == col:
                celdas.append(SIMBOLO_REINA)
            elif mostrar_analizadas and col in analizadas[fila]:
                celdas.append(SIMBOLO_ANALIZADA)
            else:
                celdas.append(SIMBOLO_VACIA)
        print(f"  {fila}  " + "  ".join(celdas))

    # Resumen en texto de donde quedo cada reina
    colocadas = [(f, c) for f, c in enumerate(tablero) if c != -1]
    if colocadas:
        detalle = ", ".join(f"F{f}C{c}" for f, c in colocadas)
        print(f"\n  Reinas colocadas ({len(colocadas)}): {detalle}")
    else:
        print("\n  Reinas colocadas (0): ninguna")


# =============================================================================
# 2. VERIFICACION DE RESTRICCIONES (la "poda" del backtracking)
# =============================================================================

def es_seguro(tablero: List[int], fila: int, col: int) -> bool:
    """
    Devuelve True si se puede colocar una reina en (fila, col) sin que sea
    atacada por las reinas ya colocadas en las filas anteriores.

    No hace falta revisar la fila porque el algoritmo coloca UNA sola reina
    por fila. Se revisan tres cosas:
      - misma columna
      - diagonal principal   (fila - columna es constante)
      - diagonal secundaria  (fila + columna es constante)
    """
    for i in range(fila):
        if tablero[i] == col:                    # misma columna
            return False
        if tablero[i] - i == col - fila:         # diagonal principal
            return False
        if tablero[i] + i == col + fila:         # diagonal secundaria
            return False
    return True


# =============================================================================
# 3. VISUALIZACION 3D DE LA PRIMERA SOLUCION
# =============================================================================

def visualizar_3d(solucion: List[int]):
    """
    Dibuja el tablero y las reinas como barras 3D con matplotlib.
    Cerrar la ventana permite que el programa continue.
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (activa el 3D)
    except ImportError:
        print("\n[AVISO] matplotlib no esta instalado, no se puede mostrar el 3D.")
        print("        Instalalo con:  pip install matplotlib")
        return

    n = len(solucion)
    figura = plt.figure(figsize=(8, 7))
    ejes = figura.add_subplot(111, projection="3d")

    # ---- Casillas del tablero: barras planas tipo damero ----
    xs, ys, zs, anchos, fondos, alturas, colores = [], [], [], [], [], [], []
    for fila in range(n):
        for col in range(n):
            xs.append(col)
            ys.append(n - 1 - fila)   # invertido para que la fila 0 quede arriba
            zs.append(0.0)
            anchos.append(0.95)
            fondos.append(0.95)
            alturas.append(0.1)
            tono = 0.85 if (fila + col) % 2 == 0 else 0.35
            colores.append((tono, tono, tono))

    ejes.bar3d(xs, ys, zs, anchos, fondos, alturas,
               color=colores, edgecolor="black", linewidth=0.2, shade=True)

    # ---- Reinas: torres mas altas sobre su casilla ----
    rx, ry, rz, ra, rf, rh = [], [], [], [], [], []
    for fila, col in enumerate(solucion):
        rx.append(col + 0.15)
        ry.append(n - 1 - fila + 0.15)
        rz.append(0.1)
        ra.append(0.65)
        rf.append(0.65)
        rh.append(1.2)

    ejes.bar3d(rx, ry, rz, ra, rf, rh,
               color="#C44E52", edgecolor="black", linewidth=0.6, shade=True)

    ejes.set_xlim(0, n)
    ejes.set_ylim(0, n)
    ejes.set_zlim(0, 1.6)
    ejes.set_xticks(range(n))
    ejes.set_yticks(range(n))
    ejes.set_zticks([])
    ejes.set_xlabel("Columnas")
    ejes.set_ylabel("Filas (invertidas)")
    ejes.set_title(f"Primera solucion en 3D para N = {n}", fontweight="bold")
    ejes.view_init(elev=30, azim=45)

    print("\n>> Mostrando la PRIMERA solucion en 3D. Cerra la ventana para seguir.")
    plt.tight_layout()
    plt.show()


# =============================================================================
# 4. EL ALGORITMO DE BACKTRACKING
# =============================================================================

def colocar_reina(tablero: List[int],
                  fila: int,
                  n: int,
                  soluciones: List[List[int]],
                  analizadas: List[Set[int]],
                  estado: dict):
    """
    Intenta colocar una reina en 'fila' y sigue recursivamente hacia abajo.

    Parametros mutables que se comparten entre todas las llamadas:
      tablero    -> posicion actual de cada reina
      soluciones -> lista donde se guardan las soluciones completas
      analizadas -> por cada fila, el conjunto de columnas ya probadas
      estado     -> contadores (retrocesos mostrados, nodos visitados, etc.)
    """

    # ---- CASO BASE: llegamos mas alla de la ultima fila = solucion completa ----
    if fila == n:
        soluciones.append(tablero[:])   # copia, no la referencia

        if len(soluciones) == 1:        # solo con la PRIMERA solucion
            imprimir_tablero(tablero, analizadas, n,
                             "PRIMERA SOLUCION ENCONTRADA",
                             mostrar_analizadas=False)
            visualizar_3d(tablero[:])
        return

    # ---- Bandera para detectar el retroceso ----
    # Si al recorrer todas las columnas de esta fila no pudimos colocar
    # ninguna reina, significa que esta rama esta muerta y hay que retroceder.
    coloco_alguna = False

    for col in range(n):
        estado["nodos"] += 1

        # Registramos que esta casilla FUE ANALIZADA por el algoritmo
        analizadas[fila].add(col)

        if es_seguro(tablero, fila, col):
            coloco_alguna = True

            # 1) Colocamos la reina
            tablero[fila] = col

            # 2) Limpiamos las marcas de las filas de mas abajo,
            #    porque empiezan un analisis nuevo con este contexto
            for f in range(fila + 1, n):
                analizadas[f].clear()

            # 3) RECURSION: avanzamos a la siguiente fila
            colocar_reina(tablero, fila + 1, n, soluciones, analizadas, estado)

            # 4) BACKTRACKING: quitamos la reina para probar la siguiente columna
            tablero[fila] = -1

    # ---- AQUI SE ACTIVA EL RETROCESO ----
    # Ninguna columna de esta fila fue viable: la rama no lleva a ninguna parte.
    if not coloco_alguna and estado["retrocesos_mostrados"] < RETROCESOS_A_MOSTRAR:
        estado["retrocesos_mostrados"] += 1
        titulo = (f"ANTES DEL RETROCESO #{estado['retrocesos_mostrados']}  "
                  f"->  la fila {fila} no admite ninguna reina")
        imprimir_tablero(tablero, analizadas, n, titulo)
        print(f"\n  Casillas analizadas en la fila {fila}: "
              f"{sorted(analizadas[fila])}  (todas invalidas)")
        print(f"  El algoritmo retrocede a la fila {fila - 1} "
              f"para probar otra alternativa.")
        pausa()

    if not coloco_alguna:
        estado["retrocesos_totales"] += 1


# =============================================================================
# 5. PROGRAMA PRINCIPAL
# =============================================================================

def main():
    print("=" * 60)
    print(" PROBLEMA DE LAS N-REINAS CON BACKTRACKING")
    print(" Programacion IV - Unidad 3")
    print("=" * 60)

    # Lectura de N (por defecto 8, como pide la consigna)
    entrada = input("\nIngrese N (ENTER para usar 8): ").strip()
    if entrada == "":
        n = 8
    else:
        try:
            n = int(entrada)
        except ValueError:
            print("Valor invalido, se usara N = 8.")
            n = 8

    if n < 1:
        print("N debe ser al menos 1. Se usara N = 8.")
        n = 8

    # Estructuras de datos
    tablero = [-1] * n                        # -1 = fila sin reina
    soluciones: List[List[int]] = []          # todas las soluciones halladas
    analizadas = [set() for _ in range(n)]    # casillas probadas por fila
    estado = {
        "retrocesos_mostrados": 0,   # cuantas fotos ya imprimimos (max 3)
        "retrocesos_totales": 0,     # cuantos retrocesos reales hubo
        "nodos": 0,                  # cuantas casillas evaluo el algoritmo
    }

    print(f"\nTablero de {n} x {n}. Se mostraran {RETROCESOS_A_MOSTRAR} estados "
          f"'ANTES DEL RETROCESO'.")
    print(f"Leyenda:  {SIMBOLO_REINA} = reina   "
          f"{SIMBOLO_ANALIZADA} = casilla analizada y descartada   "
          f"{SIMBOLO_VACIA} = sin analizar")
    pausa("\n[ENTER] para iniciar la busqueda...")

    # Arranque del backtracking desde la fila 0
    colocar_reina(tablero, 0, n, soluciones, analizadas, estado)

    # ---- Resultados finales ----
    print("\n" + "=" * 60)
    print(" RESULTADOS FINALES")
    print("=" * 60)
    print(f"  Tamano del tablero .............. {n} x {n}")
    print(f"  TOTAL DE SOLUCIONES ENCONTRADAS .. {len(soluciones)}")
    print(f"  Retrocesos totales ............... {estado['retrocesos_totales']}")
    print(f"  Casillas evaluadas (nodos) ....... {estado['nodos']}")

    if soluciones:
        print(f"\n  Primera solucion (columna por fila): {soluciones[0]}")
    else:
        print(f"\n  No existe solucion para N = {n}.")
    print("=" * 60)


if __name__ == "__main__":
    main()
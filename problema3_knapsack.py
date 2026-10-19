"""
Problema 3 - KNAPSACK 0/1: cartera de inversion en startups
Presupuesto: $10M. Proyectos (nombre, costo, ROI) en millones.
"""


def knapsack_01(items, capacidad):
    """
    dp[i][w] = mejor ROI usando los primeros i proyectos con presupuesto w.
      si costo_i > w : dp[i][w] = dp[i-1][w]
      si no          : dp[i][w] = max(dp[i-1][w], roi_i + dp[i-1][w-costo_i])
    Complejidad: O(n * W) tiempo y espacio.
    """
    n = len(items)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, costo, roi = items[i - 1]
        for w in range(capacidad + 1):
            dp[i][w] = dp[i - 1][w]                                   # no tomarlo
            if costo <= w:
                dp[i][w] = max(dp[i][w], roi + dp[i - 1][w - costo])  # tomarlo
    return dp


def backtracking(dp, items, capacidad):
    """
    Recupera los proyectos elegidos: si dp[i][w] != dp[i-1][w], el
    proyecto i fue tomado y se sigue con w - costo_i. Complejidad: O(n).
    """
    elegidos, w = [], capacidad
    pasos = []
    for i in range(len(items), 0, -1):
        tomado = dp[i][w] != dp[i - 1][w]
        pasos.append((i, w, dp[i][w], dp[i - 1][w], tomado))
        if tomado:
            elegidos.append(items[i - 1])
            w -= items[i - 1][1]
    return elegidos[::-1], pasos


def main():
    items = [("HealthTech", 3, 7), ("AI Startup", 5, 9),
             ("GreenTech", 2, 4), ("Fintech", 4, 6)]
    cap = 10

    dp = knapsack_01(items, cap)
    print("=== Tabla dp completa (filas = proyectos, columnas w = 0..10) ===")
    print("            w: " + " ".join(f"{w:>2}" for w in range(cap + 1)))
    nombres = ["(ninguno)"] + [it[0] for it in items]
    for i, fila in enumerate(dp):
        print(f"{nombres[i]:>12}: " + " ".join(f"{v:>2}" for v in fila))

    elegidos, pasos = backtracking(dp, items, cap)
    print("\n=== Backtracking ===")
    for i, w, v, v_ant, tomado in pasos:
        accion = "TOMAR" if tomado else "no tomar"
        print(f"  dp[{i}][{w}]={v} vs dp[{i-1}][{w}]={v_ant} -> {accion} {items[i-1][0]}")

    costo = sum(e[1] for e in elegidos)
    print("\nCartera optima:", [e[0] for e in elegidos])
    print(f"Costo total: ${costo}M | ROI maximo: ${dp[len(items)][cap]}M")
    print("\nComplejidad: O(n*W) tiempo y espacio; backtracking O(n).")


if __name__ == "__main__":
    main()
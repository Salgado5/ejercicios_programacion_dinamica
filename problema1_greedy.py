"""
Problema 1 - GREEDY REAL: sistema de cajero automatico
Dispensar 87.500 COP con billetes [50000, 20000, 10000, 5000, 1000].
"""
import math


def greedy_cambio(monto, denominaciones):
    """
    Greedy: en cada paso toma la mayor denominacion que quepa.
    Retorna (billetes, restante, traza).
    Complejidad: O(n log n) por el ordenamiento + O(n) del recorrido.
    """
    billetes = {}
    restante = monto
    traza = []
    for d in sorted(denominaciones, reverse=True):   # de mayor a menor
        cantidad = restante // d                     # cuantos billetes caben
        if cantidad > 0:
            billetes[d] = cantidad
            restante -= cantidad * d                 # actualizar saldo
        traza.append((d, cantidad, restante))
    return billetes, restante, traza


def dp_cambio_minimo(maximo, denominaciones):
    """
    Programacion dinamica para comparar: dp[m] = minimo de billetes
    para formar m. Complejidad: O(maximo * n) tiempo, O(maximo) espacio.
    """
    dp = [math.inf] * (maximo + 1)
    dp[0] = 0
    for m in range(1, maximo + 1):
        for d in denominaciones:
            if d <= m and dp[m - d] + 1 < dp[m]:
                dp[m] = dp[m - d] + 1
    return dp


def contraejemplo_greedy(denominaciones, limite=60000):
    """Primer monto donde greedy usa mas billetes (o falla) que el optimo."""
    dp = dp_cambio_minimo(limite, denominaciones)
    for m in range(1, limite + 1):
        billetes, rest, _ = greedy_cambio(m, denominaciones)
        usados = sum(billetes.values())
        if dp[m] != math.inf and (rest != 0 or usados > dp[m]):
            return m, billetes, dp[m]
    return None


def main():
    monto = 87500
    denoms = [50000, 20000, 10000, 5000, 1000]

    print("=== Traza paso a paso (monto = 87.500) ===")
    billetes, restante, traza = greedy_cambio(monto, denoms)
    for d, c, r in traza:
        print(f"  billete {d:>6}: {c} -> queda {r}")
    print("Billetes:", billetes)
    print("No dispensable:", restante, "(87.500 no es multiplo de 1.000)")

    print("\n=== Agregando billete de 7000 ===")
    denoms2 = denoms + [7000]
    b2, r2, _ = greedy_cambio(monto, denoms2)
    print("Greedy para 87.500:", b2, "| no dispensable:", r2)
    m, bg, opt = contraejemplo_greedy(denoms2)
    print(f"Contraejemplo: monto {m}: greedy usa {bg} "
          f"({sum(bg.values())} billetes) pero el optimo son {opt}.")
    print("Conclusion: con 7000 greedy YA NO es siempre optimo.")

    print("\nComplejidad: O(n log n) tiempo, O(n) espacio.")


if __name__ == "__main__":
    main()
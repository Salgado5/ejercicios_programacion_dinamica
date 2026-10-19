"""
Problema 4 - LCS (Longest Common Subsequence): control de versiones
v1: "DEPLOY-PROD-DB-01"    v2: "DEVELOP-DEBUG-01"
"""


def lcs_tabla(a, b):
    """
    dp[i][j] = longitud de la LCS de a[:i] y b[:j].
      si a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
      si no              : dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    Complejidad: O(m * n) tiempo y espacio.
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs_backtracking(dp, a, b):
    """
    Reconstruye una LCS desde dp[m][n]. En empate sube (i-1).
    Retorna (cadena, coincidencias) con (caracter, pos_en_a, pos_en_b).
    Complejidad: O(m + n).
    """
    i, j = len(a), len(b)
    res, camino = [], []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:          # coincidencia: se toma y sube en diagonal
            res.append(a[i - 1])
            camino.append((a[i - 1], i, j))
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(res)), camino[::-1]


def main():
    v1, v2 = "DEPLOY-PROD-DB-01", "DEVELOP-DEBUG-01"
    dp = lcs_tabla(v1, v2)

    print("=== Tabla dp completa ===")
    print("     " + "  ".join(f"{c:>2}" for c in "-" + v2))
    for i in range(len(v1) + 1):
        etiqueta = "-" if i == 0 else v1[i - 1]
        print(f"  {etiqueta} " + "  ".join(f"{v:>2}" for v in dp[i]))

    lcs, camino = lcs_backtracking(dp, v1, v2)
    print("\n=== Backtracking (coincidencias) ===")
    for c, i, j in camino:
        print(f"  '{c}'  v1[{i}]  v2[{j}]")

    print(f"\nLCS = \"{lcs}\"  (longitud {len(lcs)})")
    print(f"Eliminados de v1: {len(v1)-len(lcs)} | anadidos en v2: {len(v2)-len(lcs)}")
    print("Significado: es lo que se conserva sin cambios entre versiones;"
          " el resto son diferencias (lo que usa 'diff').")
    print("\nComplejidad: O(m*n) tiempo y espacio; backtracking O(m+n).")


if __name__ == "__main__":
    main()
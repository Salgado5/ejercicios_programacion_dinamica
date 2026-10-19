# Tarea — Algoritmos Ávidos y Programación Dinámica

**Informe**

**Jose Manuel Salgado**

**Ingeniería de sistemas**

Soluciones a 4 problemas reales de ingeniería, implementadas en Python (código comentado) con análisis de complejidad.

## Estructura del repositorio

| Archivo | Contenido |
|---|---|
| `problema1_greedy.py` | Problema 1 — Greedy: cajero automático |
| `problema2_huffman.py` | Problema 2 — Huffman: compresión de logs |
| `problema3_knapsack.py` | Problema 3 — Knapsack 0/1: inversión en startups |
| `problema4_lcs.py` | Problema 4 — LCS: control de versiones |
| `README.md` | Este informe |

Cada archivo se ejecuta por separado: `python problema1_greedy.py` (igual para los demás). Solo requiere Python 3.

## Resumen de resultados

| Problema | Técnica | Resultado | Tiempo | Espacio |
|---|---|---|---|---|
| 1. Cajero | Greedy | 87.000 dispensables (6 billetes), sobran 500 | O(n log n) | O(n) |
| 2. Logs | Huffman | 595 bits, ahorro 31,61 % vs longitud fija | O(n log n) | O(n) |
| 3. Inversión | Knapsack 0/1 | ROI máximo $20M (HealthTech + AI Startup + GreenTech) | O(n·W) | O(n·W) |
| 4. Versiones | LCS | `DELOP-DB-01` (longitud 11) | O(m·n) | O(m·n) |

---

## Problema 1 — Greedy: sistema de cajero automático

**Enunciado:** dispensar **87.500 COP** con billetes de [50000, 20000, 10000, 5000, 1000].

### Algoritmo
En cada paso se toma la mayor denominación que quepa en el monto restante (`cantidad = restante // denominación`) y se actualiza el saldo.

### Traza paso a paso
| Billete | Cantidad | Cálculo | Restante |
|:-:|:-:|:-:|:-:|
| 50.000 | 1 | 87.500 ÷ 50.000 = 1 | 37.500 |
| 20.000 | 1 | 37.500 ÷ 20.000 = 1 | 17.500 |
| 10.000 | 1 | 17.500 ÷ 10.000 = 1 | 7.500 |
| 5.000 | 1 | 7.500 ÷ 5.000 = 1 | 2.500 |
| 1.000 | 2 | 2.500 ÷ 1.000 = 2 | 500 |

> **Observación importante:** 87.500 no es múltiplo de 1.000 (el billete más pequeño). Greedy entrega 1×50.000 + 1×20.000 + 1×10.000 + 1×5.000 + 2×1.000 = **87.000** (6 billetes) y quedan **500 COP** imposibles de dispensar con esas denominaciones. Ningún algoritmo puede dispensar ese monto exacto con ellas, así que el cajero debería rechazar o redondear la operación.

### ¿Qué pasa si se agrega un billete de $7.000?
Para 87.500 greedy da 50.000 + 20.000 + 10.000 + 7.000 = 87.000 (4 billetes). Pero **greedy deja de ser óptimo en general**, porque el sistema de denominaciones deja de ser canónico.

**Contraejemplo:** monto = 12.000. Greedy usa 10.000 + 1.000 + 1.000 = **3 billetes**; el óptimo es 7.000 + 5.000 = **2 billetes**. Para garantizar el óptimo se necesita programación dinámica: `dp[m] = 1 + min(dp[m − d])`.

### Complejidad
- Greedy: **O(n log n)** por ordenar las denominaciones + O(n) por recorrerlas (con n = 5 ó 6 es prácticamente O(1)). Espacio O(n).
- Alternativa DP: O(M·n) tiempo y O(M) espacio, con M el monto.

---

## Problema 2 — Huffman: compresión de logs de un servidor

**Enunciado:** un log repite ERROR(45), INFO(120), WARN(30), DEBUG(80), TRACE(15). Total = 290 palabras.

### Construcción del árbol paso a paso
| Paso | Se fusionan (las 2 menores) | Nuevo nodo |
|:-:|:-:|:-:|
| 1 | TRACE(15) + WARN(30) | 45 |
| 2 | ERROR(45) + [45](45) | 90 |
| 3 | DEBUG(80) + [90](90) | 170 |
| 4 | INFO(120) + [170](170) | 290 |

Árbol resultante (0 = izquierda, 1 = derecha):

```
[290]
|--0-- INFO (120)
+--1-- [170]
    |--0-- DEBUG (80)
    +--1-- [90]
        |--0-- ERROR (45)
        +--1-- [45]
            |--0-- TRACE (15)
            +--1-- WARN (30)
```

### Códigos binarios y bits usados
| Palabra | Frecuencia | Código | Longitud | Bits (frec × long.) |
|:-:|:-:|:-:|:-:|:-:|
| INFO | 120 | `0` | 1 | 120 |
| DEBUG | 80 | `10` | 2 | 160 |
| ERROR | 45 | `110` | 3 | 135 |
| WARN | 30 | `1111` | 4 | 120 |
| TRACE | 15 | `1110` | 4 | 60 |
| **Total** | 290 |  |  | **595** |

### Comparación
| Esquema | Bits totales | Ahorro con Huffman |
|:-:|:-:|:-:|
| Longitud fija (5 símbolos → 3 bits) | 870 | 31,61 % (275 bits) |
| Texto ASCII (8 bits por carácter) | 10.400 | 94,28 % (9.805 bits) |
| Huffman | 595 | — |

**Respuesta:** con Huffman se usan **595 bits** frente a 870 con longitud fija: se ahorra el **31,61 %** del espacio. Si el log se guardara como texto ASCII, el ahorro sería de 94,28 %.

### Complejidad
Con n símbolos hay n−1 fusiones, cada una con 2 extracciones y 1 inserción en el heap (O(log n)). Total: **O(n log n)**. Asignar códigos: O(n). Espacio: O(n).

---

## Problema 3 — Knapsack 0/1: inversión en startups

**Enunciado:** presupuesto de $10M. Proyectos (costo, ROI) en millones: HealthTech (3, 7), AI Startup (5, 9), GreenTech (2, 4), Fintech (4, 6).

### Recurrencia
```
dp[i][w] = dp[i-1][w]                                  si costo_i > w
dp[i][w] = max(dp[i-1][w], roi_i + dp[i-1][w-costo_i]) en otro caso
```

### Tabla dp completa (filas = proyectos considerados, columnas = presupuesto w)
| i \ w | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ∅ (0 proyectos) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1. HealthTech | 0 | 0 | 0 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| 2. AI Startup | 0 | 0 | 0 | 7 | 7 | 9 | 9 | 9 | 16 | 16 | 16 |
| 3. GreenTech | 0 | 0 | 4 | 7 | 7 | 11 | 11 | 13 | 16 | 16 | 20 |
| 4. Fintech | 0 | 0 | 4 | 7 | 7 | 11 | 11 | 13 | 16 | 17 | 20 |

### Backtracking (proyectos elegidos)
| Celda | dp[i][w] vs dp[i−1][w] | Decisión | Presupuesto restante |
|:-:|:-:|:-:|:-:|
| dp[4][10] | 20 vs 20 | No tomar Fintech | 10 |
| dp[3][10] | 20 vs 16 | Tomar GreenTech | 8 |
| dp[2][8] | 16 vs 7 | Tomar AI Startup | 3 |
| dp[1][3] | 7 vs 0 | Tomar HealthTech | 0 |

**Cartera óptima:** HealthTech + AI Startup + GreenTech. Costo total = 3 + 5 + 2 = $10M; **ROI máximo = 7 + 9 + 4 = $20M**. (La alternativa HealthTech + GreenTech + Fintech rinde solo $17M con $9M.)

### Complejidad
- Llenar la tabla: **O(n·W)** tiempo y espacio (n = 4, W = 10).
- Backtracking: O(n).
- Si solo se necesitara el valor óptimo, el espacio bajaría a O(W). Es un algoritmo pseudo-polinomial.

---

## Problema 4 — LCS: control de versiones de código fuente

**Enunciado:** dos versiones de un archivo de configuración:

- v1: `"DEPLOY-PROD-DB-01"` (17 caracteres)
- v2: `"DEVELOP-DEBUG-01"` (16 caracteres)

### Recurrencia
```
si v1[i] == v2[j]: dp[i][j] = dp[i-1][j-1] + 1
si no:             dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### Tabla dp completa (en **negrita** las coincidencias de la LCS)
|  | ∅ | D | E | V | E | L | O | P | - | D | E | B | U | G | - | 0 | 1 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ∅ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D | 0 | **1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| E | 0 | 1 | 2 | 2 | **2** | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| P | 0 | 1 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| L | 0 | 1 | 2 | 2 | 2 | **3** | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| O | 0 | 1 | 2 | 2 | 2 | 3 | **4** | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Y | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| - | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| P | 0 | 1 | 2 | 2 | 2 | 3 | 4 | **5** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| R | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| O | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| - | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | **6** | 6 | 6 | 6 | 6 | 6 | 7 | 7 | 7 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | **7** | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| B | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 7 | **8** | 8 | 8 | 8 | 8 | 8 |
| - | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 7 | 8 | 8 | 8 | **9** | 9 | 9 |
| 0 | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 7 | 8 | 8 | 8 | 9 | **10** | 10 |
| 1 | 0 | 1 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 7 | 8 | 8 | 8 | 9 | 10 | **11** |

### Reconstrucción por backtracking
Se parte de `dp[17][16]`: si los caracteres coinciden se toma y se sube en diagonal; si no, se va hacia la celda mayor (en empate, hacia arriba). Coincidencias: `D` (v1:1, v2:1), `E` (v1:2, v2:4), `L` (v1:4, v2:5), `O` (v1:5, v2:6), `P` (v1:8, v2:7), `-` (v1:12, v2:8), `D` (v1:13, v2:9), `B` (v1:14, v2:11), `-` (v1:15, v2:14), `0` (v1:16, v2:15), `1` (v1:17, v2:16).

> **LCS = `DELOP-DB-01`**, longitud **11**. (Puede existir más de una LCS de igual longitud; el desempate elegido determina cuál se obtiene.)

### ¿Qué significa en el contexto del versionado?
La LCS es la parte que se **conserva sin cambios** entre ambas versiones (11 de 17 caracteres ≈ 65 % de v1 y 69 % de v2). Lo que no pertenece a la LCS son diferencias: 6 caracteres eliminados de v1 y 5 añadidos en v2. Herramientas como `diff` y git usan esta idea para mostrar el cambio mínimo entre versiones. Aquí se ve que cambió el entorno (`PROD` → `DEVELOP`/`DEBUG`), mientras que la base de datos `DB-01` se mantiene.

### Complejidad
- Llenar la tabla: **O(m·n)** tiempo y espacio (m = 17, n = 16).
- Backtracking: O(m + n).
- Si solo se quiere la longitud, el espacio baja a O(min(m, n)).

---



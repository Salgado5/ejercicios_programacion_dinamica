"""
Problema 2 - HUFFMAN: compresion de logs de un servidor
Frecuencias: ERROR(45), INFO(120), WARN(30), DEBUG(80), TRACE(15).
"""
import heapq
import math


class NodoHuffman:
    def __init__(self, freq, simbolo=None, izq=None, der=None):
        self.freq = freq
        self.simbolo = simbolo      # None en nodos internos
        self.izq = izq
        self.der = der


def huffman(frecuencias):
    """
    Construye el arbol con un min-heap. El heap guarda (frecuencia, orden,
    nodo); 'orden' desempata de forma determinista.
    Retorna (raiz, pasos).
    Complejidad: O(n log n): n-1 fusiones de costo O(log n) cada una.
    """
    heap, orden = [], 0
    for simbolo, f in frecuencias.items():
        heapq.heappush(heap, (f, orden, NodoHuffman(f, simbolo)))
        orden += 1

    pasos = []
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)    # menor frecuencia  -> rama 0
        f2, _, b = heapq.heappop(heap)    # segunda menor     -> rama 1
        padre = NodoHuffman(f1 + f2, None, a, b)
        nombre = lambda n: n.simbolo if n.simbolo else f"[{n.freq}]"
        pasos.append((nombre(a), f1, nombre(b), f2, f1 + f2))
        heapq.heappush(heap, (padre.freq, orden, padre))
        orden += 1
    return heap[0][2], pasos


def asignar_codigos(nodo, prefijo="", tabla=None):
    """Recorrido en profundidad: izquierda = '0', derecha = '1'. O(n)."""
    if tabla is None:
        tabla = {}
    if nodo.simbolo is not None:
        tabla[nodo.simbolo] = prefijo or "0"
        return tabla
    asignar_codigos(nodo.izq, prefijo + "0", tabla)
    asignar_codigos(nodo.der, prefijo + "1", tabla)
    return tabla


def main():
    frec = {"ERROR": 45, "INFO": 120, "WARN": 30, "DEBUG": 80, "TRACE": 15}

    print("=== Construccion del arbol paso a paso ===")
    raiz, pasos = huffman(frec)
    for k, p in enumerate(pasos, 1):
        print(f"  Paso {k}: {p[0]}({p[1]}) + {p[2]}({p[3]}) = {p[4]}")

    print("\n=== Codigos binarios ===")
    codigos = asignar_codigos(raiz)
    for s, c in sorted(codigos.items(), key=lambda x: len(x[1])):
        print(f"  {s:<6} frec={frec[s]:>3}  codigo={c:<5} bits={frec[s]*len(c)}")

    total = sum(frec.values())
    bits_huff = sum(frec[s] * len(c) for s, c in codigos.items())
    bits_fijo = total * math.ceil(math.log2(len(frec)))          # 3 bits
    bits_ascii = sum(frec[s] * len(s) * 8 for s in frec)         # 8 bits/char

    print("\n=== Bits usados ===")
    print(f"  Longitud fija (3 bits): {bits_fijo}")
    print(f"  ASCII (8 bits/char)   : {bits_ascii}")
    print(f"  Huffman               : {bits_huff}")
    print(f"  Ahorro vs fijo : {100*(1-bits_huff/bits_fijo):.2f}%")
    print(f"  Ahorro vs ASCII: {100*(1-bits_huff/bits_ascii):.2f}%")
    print("\nComplejidad: O(n log n) tiempo, O(n) espacio.")


if __name__ == "__main__":
    main()
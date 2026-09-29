"""
Problema 1 - Laboratorio 8

Programa original en C:

    void function(int n) {
        int i, j, k, counter = 0;
        for (i = n/2; i <= n; i++) {
            for (j = 1; j+n/2 <= n; j++) {
                for (k = 1; k <= n; k = k*2) {
                    counter++;
                }
            }
        }
    }

Analisis:
    Ciclo i : de n/2 a n            ->  n/2 + 1 iteraciones
    Ciclo j : j + n/2 <= n, o sea j <= n/2  ->  n/2 iteraciones
    Ciclo k : k = k*2 hasta n       ->  floor(log2 n) + 1 iteraciones

    T(n) = (n/2 + 1) * (n/2) * (log2(n) + 1)  ~  (n^2 / 4) * log2(n)

    Complejidad: O(n^2 log n)
"""

import math
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))

import profiling_utils as pu


def funcion_problema1(n):
    """Traduccion directa del programa en C. Se usa // para la division entera."""
    counter = 0
    mitad = n // 2
    i = mitad
    while i <= n:
        j = 1
        while j + mitad <= n:
            k = 1
            while k <= n:
                counter += 1
                k = k * 2
            j += 1
        i += 1
    return counter


def operaciones_teoricas(n):
    """Numero exacto de veces que se ejecuta counter++."""
    if n < 1:
        return 0
    iter_i = n - n // 2 + 1
    iter_j = n - n // 2
    iter_k = int(math.floor(math.log2(n))) + 1
    return iter_i * iter_j * iter_k


if __name__ == "__main__":
    pu.reportar(
        nombre="Problema 1",
        funcion=funcion_problema1,
        estimador_ops=operaciones_teoricas,
        slug="problema1",
        etiqueta_teorica="O(n^2 log n)",
    )

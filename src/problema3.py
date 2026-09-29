"""
Problema 3 - Laboratorio 8

Programa original en C:

    void function(int n) {
        int i, j;
        for (i = 1; i <= n/3; i++) {
            for (j = 1; j <= n; j += 4) {
                printf("Sequence\n");
            }
        }
    }

Analisis:
    Ciclo i : de 1 a n/3            ->  n/3 iteraciones
    Ciclo j : de 1 a n con paso 4   ->  ceil(n/4) iteraciones

    T(n) = (n/3) * (n/4) = n^2 / 12

    Las constantes se descartan en notacion Big-Oh.

    Complejidad: O(n^2)

Nota: el printf se reemplaza por un contador, por la misma razon del Problema 2.
"""

import math
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))

import profiling_utils as pu


def funcion_problema3(n):
    """Traduccion directa del programa en C."""
    salidas = 0
    for _i in range(1, n // 3 + 1):
        j = 1
        while j <= n:
            salidas += 1  # aqui iba el printf("Sequence\n")
            j += 4
    return salidas


def operaciones_teoricas(n):
    """Numero exacto de veces que se ejecuta el cuerpo del ciclo interno."""
    if n < 1:
        return 0
    iter_i = n // 3
    iter_j = math.ceil(n / 4)
    return iter_i * iter_j


if __name__ == "__main__":
    pu.reportar(
        nombre="Problema 3",
        funcion=funcion_problema3,
        estimador_ops=operaciones_teoricas,
        slug="problema3",
        etiqueta_teorica="O(n^2)",
    )

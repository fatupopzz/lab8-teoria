"""
Problema 2 - Laboratorio 8

Programa original en C:

    void function(int n) {
        if (n <= 1) return;
        int i, j;
        for (i = 1; i <= n; i++) {
            for (j = 1; j <= n; j++) {
                printf("Sequence\n");
                break;
            }
        }
    }

Analisis:
    El break corta el ciclo j en su PRIMERA iteracion, asi que el ciclo interno
    cuesta 1 y no n. El ciclo i si corre n veces.

    T(n) = n * 1 = n

    Complejidad: O(n)

Nota: el printf se reemplaza por un contador. Imprimir un millon de lineas mide
la velocidad de la terminal, no la del algoritmo, y distorsiona por completo el
profiling. El numero de iteraciones es exactamente el mismo.
"""

import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))

import profiling_utils as pu


def funcion_problema2(n):
    """Traduccion directa del programa en C."""
    if n <= 1:
        return 0
    salidas = 0
    for _i in range(1, n + 1):
        for _j in range(1, n + 1):
            salidas += 1  # aqui iba el printf("Sequence\n")
            break
    return salidas


def operaciones_teoricas(n):
    """Numero exacto de veces que se ejecuta el cuerpo del ciclo interno."""
    if n <= 1:
        return 0
    return n


if __name__ == "__main__":
    pu.reportar(
        nombre="Problema 2",
        funcion=funcion_problema2,
        estimador_ops=operaciones_teoricas,
        slug="problema2",
        etiqueta_teorica="O(n)",
    )

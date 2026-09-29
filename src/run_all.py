"""
Corre el profiling de los tres problemas y genera todos los CSV y PNG de un solo.

Uso:
    python src/run_all.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import profiling_utils as pu
import problema1
import problema2
import problema3


def main():
    print("Laboratorio 8 - Teoria de la Computacion")
    print("Profiling de los tres problemas\n")
    print(f"Tope de iteraciones antes de omitir un caso: {pu.MAX_OPS:,}")

    pu.reportar(
        nombre="Problema 1",
        funcion=problema1.funcion_problema1,
        estimador_ops=problema1.operaciones_teoricas,
        slug="problema1",
        etiqueta_teorica="O(n^2 log n)",
    )

    pu.reportar(
        nombre="Problema 2",
        funcion=problema2.funcion_problema2,
        estimador_ops=problema2.operaciones_teoricas,
        slug="problema2",
        etiqueta_teorica="O(n)",
    )

    pu.reportar(
        nombre="Problema 3",
        funcion=problema3.funcion_problema3,
        estimador_ops=problema3.operaciones_teoricas,
        slug="problema3",
        etiqueta_teorica="O(n^2)",
    )

    print(f"\nListo. Revisa la carpeta: {pu.CARPETA_RESULTADOS}")


if __name__ == "__main__":
    main()

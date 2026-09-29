"""
Utilidades compartidas para medir tiempos, guardar tablas y generar graficas.

Laboratorio 8 - Teoria de la Computacion
"""

import csv
import os
import time

import matplotlib

matplotlib.use("Agg")  # backend sin ventana, para poder guardar PNG en cualquier maquina
import matplotlib.pyplot as plt


# Valores de n pedidos por el enunciado
VALORES_N = [1, 10, 100, 1000, 10000, 100000, 1000000]

# Tope de operaciones. Si la estimacion teorica de iteraciones supera este numero,
# el caso NO se ejecuta y se reporta como "no terminó". Esto evita dejar corriendo
# horas los casos con n grande: en esta maquina Python hace unas 1.8e7 iteraciones
# por segundo, asi que 1e9 iteraciones equivalen a cerca de un minuto de espera.
#
# Ejemplo: el Problema 1 con n = 1,000,000 necesitaria 4.25e11 iteraciones, o sea
# mas de 6 horas. Ese caso se reporta como "no terminó" y se extrapola de la
# formula teorica en el analisis.
MAX_OPS = 1_000_000_000

# Carpeta donde se escriben CSV y PNG
CARPETA_RESULTADOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultados"
)


def _repeticiones(n):
    """Para n pequeño el reloj no tiene resolucion suficiente, asi que se repite."""
    if n <= 100:
        return 100
    if n <= 1000:
        return 5
    return 1


def medir(funcion, n):
    """
    Corre funcion(n) varias veces y devuelve el mejor tiempo por corrida, en segundos.

    Se usa el minimo y no el promedio porque el minimo es el que menos ruido tiene
    (el sistema operativo solo puede hacer que una corrida tarde mas, nunca menos).
    """
    reps = _repeticiones(n)
    mejor = float("inf")
    for _ in range(reps):
        inicio = time.perf_counter()
        funcion(n)
        fin = time.perf_counter()
        mejor = min(mejor, fin - inicio)
    return mejor


def ejecutar_benchmark(nombre, funcion, estimador_ops, valores_n=None, max_ops=MAX_OPS):
    """
    Ejecuta el benchmark completo de un problema.

    nombre         : etiqueta del problema, por ejemplo "Problema 1"
    funcion        : la funcion a medir, recibe n
    estimador_ops  : funcion que recibe n y devuelve el numero teorico de iteraciones
    valores_n      : lista de n a probar
    max_ops        : tope de iteraciones antes de saltarse el caso

    Devuelve una lista de diccionarios con los resultados.
    """
    if valores_n is None:
        valores_n = VALORES_N

    print(f"\n=== {nombre} ===")
    resultados = []

    for n in valores_n:
        ops = estimador_ops(n)

        if ops > max_ops:
            print(f"  n = {n:>9,}  ->  omitido (estimado {ops:.3e} iteraciones)")
            resultados.append(
                {
                    "n": n,
                    "operaciones_estimadas": ops,
                    "tiempo_segundos": None,
                    "estado": "no terminó",
                }
            )
            continue

        tiempo = medir(funcion, n)
        print(f"  n = {n:>9,}  ->  {tiempo:.6f} s   ({ops:.3e} iteraciones)")
        resultados.append(
            {
                "n": n,
                "operaciones_estimadas": ops,
                "tiempo_segundos": tiempo,
                "estado": "ok",
            }
        )

    return resultados


def imprimir_tabla(nombre, resultados):
    """Imprime la tabla de tamaño de input vs tiempo en la consola."""
    print(f"\nTabla: {nombre}")
    print(f"{'n':>10} | {'tiempo (s)':>14} | {'iteraciones':>14}")
    print("-" * 46)
    for fila in resultados:
        if fila["estado"] == "ok":
            tiempo = f"{fila['tiempo_segundos']:.6f}"
        else:
            tiempo = "no terminó"
        print(f"{fila['n']:>10,} | {tiempo:>14} | {fila['operaciones_estimadas']:>14.3e}")


def guardar_csv(archivo, resultados):
    """Guarda los resultados en un CSV dentro de la carpeta resultados/."""
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta = os.path.join(CARPETA_RESULTADOS, archivo)

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "tiempo_segundos", "operaciones_estimadas", "estado"])
        for fila in resultados:
            writer.writerow(
                [
                    fila["n"],
                    fila["tiempo_segundos"] if fila["estado"] == "ok" else "",
                    fila["operaciones_estimadas"],
                    fila["estado"],
                ]
            )

    print(f"  CSV guardado en: {ruta}")
    return ruta


def graficar(titulo, archivo, resultados, etiqueta_teorica=None):
    """
    Genera la grafica de tamaño de input vs tiempo.

    Se usa escala log-log porque los valores de n van de 1 a 1,000,000: en escala
    lineal todos los puntos chicos quedarian pegados al eje.
    """
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta = os.path.join(CARPETA_RESULTADOS, archivo)

    medidos = [f for f in resultados if f["estado"] == "ok" and f["tiempo_segundos"] > 0]
    if not medidos:
        print("  No hay datos medidos, no se genera grafica.")
        return None

    xs = [f["n"] for f in medidos]
    ys = [f["tiempo_segundos"] for f in medidos]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, marker="o", linewidth=2, label="Tiempo medido")

    # Curva teorica escalada al ultimo punto medido, para comparar la forma
    if etiqueta_teorica is not None:
        ops = [f["operaciones_estimadas"] for f in medidos]
        if ops[-1] > 0:
            escala = ys[-1] / ops[-1]
            ax.plot(
                xs,
                [o * escala for o in ops],
                linestyle="--",
                linewidth=1.5,
                label=f"Curva teorica {etiqueta_teorica}",
            )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño del input (n)")
    ax.set_ylabel("Tiempo de ejecucion (segundos)")
    ax.set_title(titulo)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)

    print(f"  Grafica guardada en: {ruta}")
    return ruta


def reportar(nombre, funcion, estimador_ops, slug, etiqueta_teorica, valores_n=None):
    """Corre el benchmark, imprime la tabla y guarda CSV y PNG de un solo."""
    resultados = ejecutar_benchmark(nombre, funcion, estimador_ops, valores_n)
    imprimir_tabla(nombre, resultados)
    guardar_csv(f"{slug}.csv", resultados)
    graficar(f"{nombre}: {etiqueta_teorica}", f"{slug}.png", resultados, etiqueta_teorica)
    return resultados

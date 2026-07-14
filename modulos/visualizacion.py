# -*- coding: utf-8 -*-
"""
Módulo de VISUALIZACIÓN — gráficos generados con matplotlib.

Como MEDIC-UTP es un sistema de consola (sin interfaz gráfica), los
gráficos no se muestran en pantalla: se guardan como imágenes PNG dentro
de la carpeta reportes/ para su revisión posterior.
"""

import os

import matplotlib
matplotlib.use("Agg")  # Backend sin pantalla: solo genera archivos de imagen
import matplotlib.pyplot as plt

from modulos import estado
from modulos.ui_consola import subtitulo, mensaje_info, mensaje_ok
from modulos.analisis_datos import df_pacientes, df_facturas, df_citas

CARPETA_REPORTES = "reportes"


def _guardar(fig, nombre_archivo):
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta = os.path.join(CARPETA_REPORTES, nombre_archivo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def grafico_pacientes_por_seguro():
    """Gráfico de barras: cantidad de pacientes por tipo de seguro."""
    df = df_pacientes()
    if df.empty:
        return None
    conteo = df["seguro"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(conteo.index, conteo.values, color="#4C72B0")
    ax.set_title("Pacientes por tipo de seguro")
    ax.set_xlabel("Tipo de seguro")
    ax.set_ylabel("Cantidad de pacientes")
    for i, valor in enumerate(conteo.values):
        ax.text(i, valor, str(valor), ha="center", va="bottom")

    return _guardar(fig, "pacientes_por_seguro.png")


def grafico_ingresos_por_especialidad():
    """Gráfico de barras: ingresos totales facturados por especialidad."""
    df = df_facturas()
    if df.empty:
        return None
    ingresos = df.groupby("especialidad")["total"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(ingresos.index, ingresos.values, color="#55A868")
    ax.set_title("Ingresos por especialidad médica")
    ax.set_xlabel("Especialidad")
    ax.set_ylabel("Ingreso total (S/.)")
    ax.tick_params(axis="x", rotation=35)

    return _guardar(fig, "ingresos_por_especialidad.png")


def grafico_citas_por_estado():
    """Gráfico circular: proporción de citas según su estado."""
    df = df_citas()
    if df.empty:
        return None
    conteo = df["estado"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(conteo.values, labels=conteo.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribución de citas por estado")

    return _guardar(fig, "citas_por_estado.png")


def grafico_edad_pacientes():
    """Histograma de la distribución de edades de los pacientes."""
    df = df_pacientes()
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["edad"], bins=10, color="#C44E52", edgecolor="black")
    ax.set_title("Distribución de edades de pacientes")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Frecuencia")

    return _guardar(fig, "edad_pacientes.png")


def generar_graficos():
    """Genera todos los gráficos disponibles según los datos actuales."""
    print(subtitulo("GENERAR GRÁFICOS (matplotlib)"))

    if not estado.pacientes and not estado.citas and not estado.facturas:
        mensaje_info("No hay datos suficientes para graficar todavía.")
        return

    generadas = list(filter(None, [
        grafico_pacientes_por_seguro(),
        grafico_edad_pacientes(),
        grafico_ingresos_por_especialidad(),
        grafico_citas_por_estado(),
    ]))

    if not generadas:
        mensaje_info("No hay datos suficientes para graficar todavía.")
        return

    mensaje_ok(f"Se generaron {len(generadas)} gráfico(s) en la carpeta '{CARPETA_REPORTES}/':")
    for ruta in generadas:
        print(f"    - {ruta}")

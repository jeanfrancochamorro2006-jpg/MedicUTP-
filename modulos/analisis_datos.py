# -*- coding: utf-8 -*-
"""
Módulo de ANÁLISIS DE DATOS — pandas, numpy y programación funcional.

Este módulo transforma las colecciones en memoria (listas de objetos) en
DataFrames de pandas para realizar limpieza, agregación y análisis
estadístico con numpy, y refuerza el paradigma funcional aplicando
map(), functools.reduce() y funciones de orden superior sobre las mismas
colecciones (multiparadigma: POO + funcional + análisis de datos).
"""

from functools import reduce

import numpy as np
import pandas as pd

from modulos import estado
from modulos.ui_consola import titulo, subtitulo, linea, mensaje_info, pausa
from modulos.validaciones import leer_entero


# =====================================================================
# CONSTRUCCIÓN DE DATAFRAMES (limpieza y transformación de datos)
# =====================================================================

def df_pacientes():
    """Convierte la lista de pacientes en un DataFrame de pandas."""
    return pd.DataFrame([p.a_dict() for p in estado.pacientes])


def df_medicos():
    """Convierte la lista de médicos en un DataFrame de pandas."""
    return pd.DataFrame([m.a_dict() for m in estado.medicos])


def df_citas():
    """Convierte la lista de citas en un DataFrame de pandas."""
    return pd.DataFrame([c.a_dict() for c in estado.citas])


def df_facturas():
    """
    Convierte la lista de facturas en un DataFrame de pandas, enriquecido
    con la especialidad y el nombre del médico de la cita asociada
    (transformación/"join" de datos entre colecciones).
    """
    filas = []
    for f in estado.facturas:
        cita = f.obtener_cita()
        d = f.a_dict()
        d["especialidad"] = cita.obtener_medico().obtener_especialidad()
        d["medico"] = cita.obtener_medico().obtener_nombre()
        d["seguro_paciente"] = cita.obtener_paciente().obtener_seguro()
        filas.append(d)
    return pd.DataFrame(filas)


# =====================================================================
# ANÁLISIS ESTADÍSTICO — pandas + numpy
# =====================================================================

def analizar_pacientes():
    """Estadísticas de pacientes con pandas (describe/groupby) y numpy."""
    print(titulo("ANÁLISIS DE PACIENTES (pandas + numpy)", "-"))

    df = df_pacientes()
    if df.empty:
        mensaje_info("No hay pacientes registrados para analizar.")
        return

    print("\n  Resumen estadístico de la edad (pandas.describe()):")
    print(df["edad"].describe().to_string())

    edades = df["edad"].to_numpy()
    print("\n  Métricas adicionales con numpy:")
    print(f"    Media (np.mean)        : {np.mean(edades):.2f}")
    print(f"    Desviación estándar    : {np.std(edades):.2f}")
    print(f"    Mediana (np.median)    : {np.median(edades):.2f}")
    print(f"    Percentil 25 / 75      : {np.percentile(edades, 25):.1f} / {np.percentile(edades, 75):.1f}")

    print("\n  Distribución por tipo de seguro (pandas.groupby):")
    conteo = df.groupby("seguro")["dni"].count().sort_values(ascending=False)
    print(conteo.to_string())

    # Refuerzo funcional: nombres normalizados con map() + lambda
    nombres_formato = list(map(lambda n: n.strip().title(), df["nombre"]))
    print(f"\n  Nombres normalizados con map()+title(): {nombres_formato[:5]}"
          f"{' ...' if len(nombres_formato) > 5 else ''}")


def analizar_facturacion():
    """
    Análisis de ingresos con pandas/numpy, y verificación cruzada del
    ingreso total usando functools.reduce() (estilo funcional puro).
    """
    print(titulo("ANÁLISIS DE FACTURACIÓN (pandas + numpy)", "-"))

    df = df_facturas()
    if df.empty:
        mensaje_info("No hay comprobantes registrados para analizar.")
        return

    total_pandas = df["total"].sum()
    # Verificación funcional: mismo total calculado con reduce() sobre los objetos
    total_reduce = reduce(lambda acc, f: acc + f.obtener_total(), estado.facturas, 0.0)

    print(f"\n  Ingreso total (pandas.sum)      : S/. {total_pandas:.2f}")
    print(f"  Ingreso total (functools.reduce): S/. {total_reduce:.2f}")

    print("\n  Ingresos y ticket promedio por especialidad (groupby + numpy):")
    resumen = df.groupby("especialidad")["total"].agg(["sum", "mean", "count"])
    resumen.columns = ["Ingreso Total", "Ticket Promedio", "N° Comprobantes"]
    print(resumen.round(2).to_string())

    montos = df["total"].to_numpy()
    print("\n  Estadísticos del monto facturado (numpy):")
    print(f"    Máximo   : S/. {np.max(montos):.2f}")
    print(f"    Mínimo   : S/. {np.min(montos):.2f}")
    print(f"    Varianza : {np.var(montos):.2f}")

    print("\n  Comprobantes por tipo (Boleta / Factura):")
    print(df["tipo_comprobante"].value_counts().to_string())


def analizar_citas():
    """Analiza el estado y la distribución mensual de las citas con pandas."""
    print(titulo("ANÁLISIS DE AGENDAMIENTO (pandas)", "-"))

    df = df_citas()
    if df.empty:
        mensaje_info("No hay citas registradas para analizar.")
        return

    print("\n  Citas por estado (pandas.value_counts):")
    print(df["estado"].value_counts().to_string())

    df["mes"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce").dt.strftime("%m/%Y")
    print("\n  Citas por mes:")
    print(df.groupby("mes").size().sort_index().to_string())

    print("\n  Médicos con más citas asignadas:")
    print(df["medico"].value_counts().head(5).to_string())


def exportar_reportes_csv():
    """Exporta los DataFrames actuales a archivos CSV dentro de reportes/."""
    import os
    print(subtitulo("EXPORTAR REPORTES A CSV"))

    os.makedirs("reportes", exist_ok=True)
    exportados = []
    for nombre, constructor in (
        ("pacientes", df_pacientes),
        ("medicos", df_medicos),
        ("citas", df_citas),
        ("facturas", df_facturas),
    ):
        df = constructor()
        if not df.empty:
            ruta = os.path.join("reportes", f"{nombre}.csv")
            df.to_csv(ruta, index=False, encoding="utf-8-sig")
            exportados.append(ruta)

    if not exportados:
        mensaje_info("No hay datos suficientes para exportar.")
        return

    print("\n  Archivos generados:")
    for ruta in exportados:
        print(f"    - {ruta}")


def menu_analisis_datos():
    """PASO 4: ANÁLISIS DE DATOS — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 4 ]  ANÁLISIS DE DATOS"))

        opciones_menu = [
            "Análisis de Pacientes (pandas/numpy)",
            "Análisis de Facturación (pandas/numpy)",
            "Análisis de Agendamiento (pandas)",
            "Exportar Reportes a CSV",
            "Generar Gráficos (matplotlib)",
            "Volver al Menú Principal",
        ]
        for i, op in enumerate(opciones_menu, start=1):
            num = "0" if op == "Volver al Menú Principal" else str(i)
            print(f"  {num}. {op}")
        print(linea("-"))

        op = leer_entero(
            f"Opción (0-{len(opciones_menu)-1}): ",
            minimo=0, maximo=len(opciones_menu) - 1
        )

        if op == 0:
            return
        elif op == 1:
            analizar_pacientes()
            pausa()
        elif op == 2:
            analizar_facturacion()
            pausa()
        elif op == 3:
            analizar_citas()
            pausa()
        elif op == 4:
            exportar_reportes_csv()
            pausa()
        elif op == 5:
            from modulos.visualizacion import generar_graficos
            generar_graficos()
            pausa()

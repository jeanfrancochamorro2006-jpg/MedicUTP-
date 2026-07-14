# -*- coding: utf-8 -*-
"""
Módulo de diseño de consola.

Centraliza toda la lógica de presentación en funciones puras reutilizables
(no dependen de estado externo, solo de sus parámetros), lo que permite
cambiar el estilo visual del sistema desde un solo lugar.
"""

from modulos.estado import ANCHO_CONSOLA


def linea(caracter="=", ancho=ANCHO_CONSOLA):
    """Devuelve una línea decorativa del ancho indicado."""
    return caracter * ancho


def titulo(texto, caracter="="):
    """Devuelve un bloque de título centrado entre líneas decorativas."""
    return (
        f"\n{linea(caracter)}\n"
        f"{texto.center(ANCHO_CONSOLA)}\n"
        f"{linea(caracter)}"
    )


def subtitulo(texto):
    """Encabezado de sección secundaria con guiones."""
    return f"\n{linea('-')}\n  {texto}\n{linea('-')}"


def fila_tabla(*celdas, anchos):
    """Formatea una fila de tabla alineando columnas con anchos fijos."""
    partes = [str(c).ljust(w) for c, w in zip(celdas, anchos)]
    return "  " + " | ".join(partes)


def encabezado_tabla(columnas, anchos):
    """Imprime la fila de encabezado de tabla y su separador visual."""
    print(fila_tabla(*columnas, anchos=anchos))
    print("  " + "-+-".join("-" * w for w in anchos))


def mensaje_ok(texto):
    """Mensaje de éxito con ícono visual."""
    print(f"\n  [+]  {texto}")


def mensaje_error(texto):
    """Mensaje de error con ícono visual."""
    print(f"\n  [!]  {texto}")


def mensaje_info(texto):
    """Mensaje informativo con ícono visual."""
    print(f"\n  [i]  {texto}")


def pausa():
    """Detiene la ejecución hasta que el usuario presione ENTER."""
    input("\n  Presione ENTER para continuar...")

# -*- coding: utf-8 -*-
"""
Funciones de entrada y validación de datos por consola.

Todas usan try/except para controlar errores del usuario y devuelven
únicamente valores ya validados, sin dejar avanzar el flujo con datos
incorrectos.
"""

import datetime

from modulos.ui_consola import mensaje_error


def leer_cadena(mensaje):
    """Lee texto y asegura que no esté vacío."""
    while True:
        entrada = input(f"  {mensaje}").strip()
        if entrada:
            return entrada
        mensaje_error("Este campo es obligatorio.")


def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero controlando errores con try/except."""
    while True:
        try:
            valor = int(input(f"  {mensaje}"))
            if minimo is not None and valor < minimo:
                mensaje_error(f"El valor mínimo es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                mensaje_error(f"El valor máximo es {maximo}.")
                continue
            return valor
        except ValueError:
            mensaje_error("Ingrese únicamente números enteros.")


def leer_dni(mensaje):
    """Valida un DNI de exactamente 8 dígitos."""
    while True:
        dni = input(f"  {mensaje}").strip()
        if dni.isdigit() and len(dni) == 8:
            return dni
        mensaje_error("El DNI debe tener exactamente 8 dígitos.")


def leer_fecha(mensaje):
    """
    Lee y valida una fecha en formato DD/MM/AAAA usando try/except.
    Comprueba que la fecha no sea anterior al día de hoy.
    """
    while True:
        texto = input(f"  {mensaje}").strip()
        try:
            fecha = datetime.datetime.strptime(texto, "%d/%m/%Y")
            hoy = datetime.datetime.now().replace(hour=0, minute=0,
                                                    second=0, microsecond=0)
            if fecha < hoy:
                mensaje_error("La fecha no puede ser anterior a hoy.")
                continue
            return texto
        except ValueError:
            mensaje_error("Formato incorrecto. Use DD/MM/AAAA (ej: 25/07/2026).")


def elegir_de_tupla(mensaje, opciones):
    """
    Muestra una tupla de opciones numeradas y retorna la elegida.
    Usa enumerate() para iterar con índice automático.
    Ejemplo de uso: elegir_de_tupla("Seguro:", TIPOS_SEGURO)
    """
    print(f"\n  {mensaje}")
    for i, op in enumerate(opciones, start=1):
        print(f"    {i}. {op}")
    idx = leer_entero(f"Elija (1-{len(opciones)}): ", minimo=1, maximo=len(opciones))
    return opciones[idx - 1]

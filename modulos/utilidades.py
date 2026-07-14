# -*- coding: utf-8 -*-
"""
Funciones puras de utilidad, reutilizadas por varios módulos.

Se mantienen aquí (sin entrada/salida por consola) para que puedan
probarse directamente con unittest.
"""

from modulos.estado import pacientes, medicos, citas

# Multiplicadores oficiales de SUNAT para el dígito verificador (módulo 11)
_MULTIPLICADORES_RUC = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]


def buscar_paciente(dni):
    """Recorre la lista de pacientes buscando por DNI. Retorna None si no existe."""
    for p in pacientes:
        if p.obtener_dni() == dni:
            return p
    return None


def buscar_medico(dni):
    """Recorre la lista de médicos buscando por DNI. Retorna None si no existe."""
    for m in medicos:
        if m.obtener_dni() == dni:
            return m
    return None


def buscar_cita(id_cita):
    """Busca una cita por su ID. Retorna None si no existe."""
    return next((c for c in citas if c.obtener_id() == id_cita), None)


def generar_ruc10(dni_paciente):
    """
    Genera un RUC 10 (persona natural con negocio) a partir del DNI,
    aplicando el algoritmo oficial de dígito verificador módulo 11 de SUNAT.

    Es una función pura: mismo DNI de entrada siempre produce el mismo RUC.
    """
    ruc_base = "10" + dni_paciente
    suma = sum(int(ruc_base[i]) * _MULTIPLICADORES_RUC[i] for i in range(10))
    resto = suma % 11
    verificador = 11 - resto
    if verificador == 11:
        verificador = 0
    elif verificador == 10:
        verificador = 1
    return ruc_base + str(verificador)

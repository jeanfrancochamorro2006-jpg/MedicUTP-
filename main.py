# -*- coding: utf-8 -*-
"""
MEDIC-UTP - Sistema de Citas Médicas y Facturación
Curso: Programación Orientada a Objetos (POO)

Flujo del sistema:
    REGISTRO  ->  AGENDAMIENTO  ->  FACTURACIÓN  ->  ANÁLISIS DE DATOS

Este archivo solo orquesta el menú principal. La lógica de cada módulo
vive en el paquete modulos/ (registro, agendamiento, facturación,
persistencia y análisis de datos) y las entidades del dominio en
clases/ y polimorfismo/.
"""

import sys
import datetime

from modulos import estado
from modulos.ui_consola import titulo, linea, pausa
from modulos.validaciones import leer_entero
from modulos.persistencia import cargar_base_datos
from modulos.registro import menu_registro
from modulos.agendamiento import menu_agendamiento
from modulos.facturacion import menu_facturacion
from modulos.analisis_datos import menu_analisis_datos


def resumen_general():
    """
    Panel de resumen rápido mostrado al inicio del menú principal.
    Usa datetime para la fecha/hora y f-strings con alineación.
    """
    ahora = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")
    print(titulo("RESUMEN DEL SISTEMA"))
    print(f"  {'Fecha y hora':<25}: {ahora}")
    print(f"  {'Pacientes registrados':<25}: {len(estado.pacientes)}")
    print(f"  {'Medicos registrados':<25}: {len(estado.medicos)}")
    print(f"  {'Especialidades activas':<25}: {len(estado.indice_especialidad)}")
    print(f"  {'Citas agendadas':<25}: {len(estado.citas)}")
    pendientes = len([c for c in estado.citas if c.obtener_estado() == "Pendiente"])
    print(f"  {'Citas pendientes':<25}: {pendientes}")
    print(f"  {'Comprobantes emitidos':<25}: {len(estado.facturas)}")


def main():
    cargar_base_datos()

    print(titulo(f"  {estado.VERSION_SISTEMA[0]}  v{estado.VERSION_SISTEMA[1]}"))
    print(f"{'Sistema de Citas Medicas y Facturacion'.center(estado.ANCHO_CONSOLA)}")
    print(linea())
    pausa()

    while True:
        resumen_general()

        print(titulo("MENÚ PRINCIPAL"))
        print("  REGISTRO -> AGENDAMIENTO -> FACTURACIÓN -> ANÁLISIS DE DATOS")
        print(linea("-"))
        print("  1. PASO 1 -> REGISTRO")
        print("  2. PASO 2 -> AGENDAMIENTO")
        print("  3. PASO 3 -> FACTURACIÓN")
        print("  4. PASO 4 -> ANÁLISIS DE DATOS (pandas / numpy / matplotlib)")
        print("  0. Salir del Sistema")
        print(linea())

        op = leer_entero("Opción (0-4): ", minimo=0, maximo=4)

        if op == 1:
            menu_registro()
        elif op == 2:
            menu_agendamiento()
        elif op == 3:
            menu_facturacion()
        elif op == 4:
            menu_analisis_datos()
        elif op == 0:
            print(titulo("¡HASTA PRONTO!"))
            print(f"{'Gracias por utilizar MEDIC-UTP'.center(estado.ANCHO_CONSOLA)}")
            print(linea())
            sys.exit(0)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Módulo de REGISTRO — pacientes y médicos.

Requisitos demostrados en este módulo:
    [POO]            — Paciente (herencia múltiple), Medico (herencia simple)
    [TUPLAS]         — TIPOS_SEGURO, ESPECIALIDADES_VALIDAS
    [COLECCIONES]    — sets de DNI, diccionario índice_especialidad
    [FUNCIONAL]      — filter() + lambda para búsquedas
    [ENTRADA/SALIDA] — validación con try/except
"""

from clases.paciente import Paciente
from clases.medico import Medico

from modulos import estado
from modulos.estado import TIPOS_SEGURO, ESPECIALIDADES_VALIDAS, PRECIOS_SUGERIDOS
from modulos.ui_consola import (
    titulo, subtitulo, linea, encabezado_tabla, fila_tabla,
    mensaje_ok, mensaje_error, mensaje_info, pausa,
)
from modulos.validaciones import leer_cadena, leer_entero, leer_dni, elegir_de_tupla
from modulos.persistencia import guardar_base_datos
from polimorfismo.sobreescritura import imprimir_resumen_entidad
from polimorfismo.sobrecarga import BuscadorClinico


def registrar_paciente():
    print(subtitulo("REGISTRAR PACIENTE"))

    dni = leer_dni("DNI del paciente      : ")
    if dni in estado.dni_pacientes:
        mensaje_error("Ese paciente ya está registrado.")
        return
    nombre = leer_cadena("Nombre completo       : ")
    edad = leer_entero("Edad                  : ", minimo=0, maximo=120)
    telefono = leer_cadena("Teléfono              : ")
    seguro = elegir_de_tupla("Tipo de seguro:", TIPOS_SEGURO)

    nuevo = Paciente(dni, nombre, edad, telefono, seguro)
    estado.pacientes.append(nuevo)
    estado.dni_pacientes.add(dni)

    guardar_base_datos()
    mensaje_ok(f"Paciente '{nombre}' registrado con éxito.")


def registrar_medico():
    print(subtitulo("REGISTRAR MÉDICO"))

    dni = leer_dni("DNI del médico        : ")
    if dni in estado.dni_medicos:
        mensaje_error("Ese médico ya está registrado.")
        return
    nombre = leer_cadena("Nombre completo       : ")
    especialidad = elegir_de_tupla("Especialidad:", ESPECIALIDADES_VALIDAS)
    consultorio = leer_entero("N° de consultorio     : ", minimo=1, maximo=99)

    precio_sug = PRECIOS_SUGERIDOS.get(especialidad, 80)
    print(f"  [i] Precio de consulta sugerido para {especialidad}: S/. {precio_sug}")
    precio_consulta = leer_entero("Precio de consulta (mín. S/. 10): ", minimo=10)

    nuevo = Medico(dni, nombre, especialidad, consultorio, precio_consulta)
    estado.medicos.append(nuevo)
    estado.dni_medicos.add(dni)
    estado.indice_especialidad.setdefault(especialidad, []).append(nuevo)

    guardar_base_datos()
    mensaje_ok(f"Médico '{nombre}' ({especialidad}) registrado con éxito.")


def mostrar_pacientes():
    print(titulo("LISTA DE PACIENTES"))

    if not estado.pacientes:
        mensaje_info("No hay pacientes registrados.")
        return

    anchos = [10, 24, 5, 13, 12]
    encabezado_tabla(["DNI", "Nombre", "Edad", "Telefono", "Seguro"], anchos)
    for p in estado.pacientes:
        print(fila_tabla(
            p.obtener_dni(), p.obtener_nombre(),
            p.obtener_edad(), p.obtener_telefono(),
            p.obtener_seguro(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(estado.pacientes)} paciente(s).")


def mostrar_medicos():
    print(titulo("LISTA DE MÉDICOS"))

    if not estado.medicos:
        mensaje_info("No hay médicos registrados.")
        return

    anchos = [10, 20, 16, 6, 8]
    encabezado_tabla(["DNI", "Nombre", "Especialidad", "Cons.", "Precio"], anchos)
    for m in estado.medicos:
        print(fila_tabla(
            m.obtener_dni(), m.obtener_nombre(),
            m.obtener_especialidad(), m.obtener_consultorio(),
            f"S/. {m.obtener_precio_consulta():.0f}",
            anchos=anchos
        ))
    print(f"\n  Total: {len(estado.medicos)} médico(s).")


def buscar_pacientes_por_seguro():
    """Filtra la lista de pacientes por tipo de seguro usando filter() + lambda."""
    print(subtitulo("BUSCAR PACIENTES POR SEGURO"))
    seguro = elegir_de_tupla("Seleccione el tipo de seguro:", TIPOS_SEGURO)

    resultado = list(filter(lambda p: p.obtener_seguro() == seguro, estado.pacientes))

    if not resultado:
        mensaje_info(f"No hay pacientes con seguro '{seguro}'.")
        return

    print(f"\n  Pacientes con seguro '{seguro}':")
    anchos = [10, 24, 5, 13]
    encabezado_tabla(["DNI", "Nombre", "Edad", "Telefono"], anchos)
    for p in resultado:
        print(fila_tabla(
            p.obtener_dni(), p.obtener_nombre(),
            p.obtener_edad(), p.obtener_telefono(),
            anchos=anchos
        ))
    print(f"\n  Encontrado(s): {len(resultado)} paciente(s).")


def buscar_medicos_por_especialidad():
    """Consulta el diccionario índice inverso para listar médicos de una especialidad."""
    print(subtitulo("BUSCAR MÉDICOS POR ESPECIALIDAD"))
    especialidad = elegir_de_tupla("Seleccione la especialidad:", ESPECIALIDADES_VALIDAS)

    resultado = estado.indice_especialidad.get(especialidad, [])

    if not resultado:
        mensaje_info(f"No hay médicos de '{especialidad}'.")
        return

    print(f"\n  Médicos de '{especialidad}':")
    anchos = [10, 24, 6]
    encabezado_tabla(["DNI", "Nombre", "Cons."], anchos)
    for m in resultado:
        print(fila_tabla(
            m.obtener_dni(), m.obtener_nombre(),
            m.obtener_consultorio(),
            anchos=anchos
        ))
    print(f"\n  Encontrado(s): {len(resultado)} médico(s).")


def buscar_poo_sobrecarga():
    """
    [POO] Función interactiva para demostrar Polimorfismo.
    Utiliza BuscadorClinico (Sobrecarga simulada) y llama a imprimir_resumen_entidad
    (Polimorfismo por Sobreescritura) para cada resultado encontrado.
    """
    print(subtitulo("BÚSQUEDA POO (SOBRECARGA Y SOBREESCRITURA)"))
    print("  1. Buscar en Colección de Pacientes")
    print("  2. Buscar en Colección de Médicos")
    op_tipo = leer_entero("Seleccione tipo de búsqueda (1-2): ", minimo=1, maximo=2)
    coleccion = estado.pacientes if op_tipo == 1 else estado.medicos

    print("\n  Filtros disponibles (Sobrecarga de Métodos):")
    print("    1. Buscar solo por DNI")
    print("    2. Buscar solo por Nombre")
    print("    3. Buscar por DNI y por Nombre simultáneamente")
    print("    4. No aplicar filtros (Mostrar todo)")
    op_filtro = leer_entero("Elija una opción (1-4): ", minimo=1, maximo=4)

    buscador = BuscadorClinico()
    resultado = []

    # Dependiendo de la opción del usuario, se llama al mismo método buscar
    # con diferentes firmas (Sobrecarga).
    if op_filtro == 1:
        dni = leer_dni("Ingrese DNI a buscar: ")
        resultado = buscador.buscar(coleccion, dni=dni)               # Firma 1
    elif op_filtro == 2:
        nombre = leer_cadena("Ingrese Nombre a buscar: ")
        resultado = buscador.buscar(coleccion, nombre=nombre)         # Firma 2
    elif op_filtro == 3:
        dni = leer_dni("Ingrese DNI a buscar: ")
        nombre = leer_cadena("Ingrese Nombre a buscar: ")
        resultado = buscador.buscar(coleccion, dni=dni, nombre=nombre)  # Firma 3
    else:
        resultado = buscador.buscar(coleccion)                        # Firma 4

    if not resultado:
        mensaje_info("No se encontraron registros con los criterios especificados.")
        return

    print(titulo("RESULTADOS (POLIMORFISMO DE SOBREESCRITURA)"))
    for elem in resultado:
        imprimir_resumen_entidad(elem)
    print(linea("-"))


def estadisticas_pacientes():
    """
    Calcula y muestra estadísticas de los pacientes registrados.
    Estructuras usadas: lista por comprensión, diccionario, set.
    """
    print(titulo("ESTADÍSTICAS DE PACIENTES", "-"))

    if not estado.pacientes:
        mensaje_info("No hay pacientes registrados aún.")
        return

    edades = [p.obtener_edad() for p in estado.pacientes]
    promedio = sum(edades) / len(edades)

    print(f"\n  Total de pacientes : {len(estado.pacientes)}")
    print(f"  Edad promedio      : {promedio:.1f} años")
    print(f"  Edad mínima        : {min(edades)} años")
    print(f"  Edad máxima        : {max(edades)} años")

    conteo_seguro = {}
    for p in estado.pacientes:
        seg = p.obtener_seguro()
        conteo_seguro[seg] = conteo_seguro.get(seg, 0) + 1

    print("\n  Distribucion por tipo de seguro:")
    for seg, cant in sorted(conteo_seguro.items()):
        barra = "=" * cant
        print(f"    {seg:<15} {barra}  ({cant})")

    todos_dnis = {p.obtener_dni() for p in estado.pacientes}
    print(f"\n  DNIs unicos registrados: {len(todos_dnis)}")


def estadisticas_medicos():
    """Muestra estadísticas de médicos usando el diccionario índice inverso."""
    print(titulo("ESTADÍSTICAS DE MÉDICOS", "-"))

    if not estado.medicos:
        mensaje_info("No hay médicos registrados aún.")
        return

    print(f"\n  Total de médicos registrados: {len(estado.medicos)}")

    if estado.indice_especialidad:
        print("\n  Médicos por especialidad:")
        for esp in sorted(estado.indice_especialidad.keys()):
            cantidad = len(estado.indice_especialidad[esp])
            print(f"    {esp:<22}: {cantidad} medico(s)")


def menu_registro():
    """PASO 1: REGISTRO — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 1 ]  REGISTRO"))

        opciones_menu = [
            "Registrar Paciente",
            "Registrar Médico",
            "Mostrar Pacientes",
            "Mostrar Médicos",
            "Buscar Pacientes por Seguro",
            "Buscar Médicos por Especialidad",
            "Estadísticas de Pacientes",
            "Estadísticas de Médicos",
            "Búsqueda POO (Sobrecarga/Polimorfismo)",
            "Volver al Menú Principal",
        ]
        for i, op in enumerate(opciones_menu, start=1):
            num = "0" if op == "Volver al Menú Principal" else str(i)
            print(f"  {num}. {op}")
        print(linea("-"))

        op = leer_entero(f"Opción (0-{len(opciones_menu)-1}): ",
                          minimo=0, maximo=len(opciones_menu) - 1)

        acciones = {
            1: registrar_paciente,
            2: registrar_medico,
            3: mostrar_pacientes,
            4: mostrar_medicos,
            5: buscar_pacientes_por_seguro,
            6: buscar_medicos_por_especialidad,
            7: estadisticas_pacientes,
            8: estadisticas_medicos,
            9: buscar_poo_sobrecarga,
        }

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()
            pausa()

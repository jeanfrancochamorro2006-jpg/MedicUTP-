# -*- coding: utf-8 -*-
"""
Módulo de AGENDAMIENTO — gestión de citas médicas.

Requisitos demostrados en este módulo:
    [LISTAS]         — lista 'citas', listas por comprensión
    [TUPLAS]         — ESTADOS_CITA, HORAS_ATENCION como catálogos
    [COLECCIONES]    — set slots_ocupados, diccionarios contadores
    [ENTRADA/SALIDA] — leer_fecha(), menú con opciones numeradas
    [DISEÑO CONSOLA] — subtitulo(), encabezado_tabla(), fila_tabla()
"""

from clases.cita import Cita

from modulos import estado
from modulos.estado import ESTADOS_CITA, HORAS_ATENCION
from modulos.ui_consola import titulo, subtitulo, linea, encabezado_tabla, fila_tabla, mensaje_ok, mensaje_error, mensaje_info, pausa
from modulos.validaciones import leer_cadena, leer_entero, leer_dni, leer_fecha, elegir_de_tupla
from modulos.persistencia import guardar_base_datos
from modulos.utilidades import buscar_paciente, buscar_medico


def agendar_cita():
    """
    Registra una nueva cita médica.
    Pasos: elegir paciente → elegir médico → elegir fecha →
           elegir hora (tupla) → ingresar motivo → guardar.
    """
    print(subtitulo("AGENDAR NUEVA CITA"))

    if not estado.pacientes:
        mensaje_error("No hay pacientes registrados. Vaya al módulo de REGISTRO.")
        return
    dni_p = leer_dni("DNI del paciente      : ")
    paciente = buscar_paciente(dni_p)
    if not paciente:
        mensaje_error("Paciente no encontrado. Regístrelo primero.")
        return

    if not estado.medicos:
        mensaje_error("No hay médicos registrados. Vaya al módulo de REGISTRO.")
        return
    dni_m = leer_dni("DNI del médico        : ")
    medico = buscar_medico(dni_m)
    if not medico:
        mensaje_error("Médico no encontrado. Regístrelo primero.")
        return

    fecha = leer_fecha("Fecha de la cita (DD/MM/AAAA): ")
    hora = elegir_de_tupla("Hora de atención:", HORAS_ATENCION)

    slot = (medico.obtener_dni(), fecha, hora)
    if slot in estado.slots_ocupados:
        mensaje_error(
            f"El Dr. {medico.obtener_nombre()} ya tiene cita "
            f"el {fecha} a las {hora}. Elija otra hora o fecha."
        )
        return

    motivo = leer_cadena("Motivo de consulta    : ")

    nueva = Cita(paciente, medico, fecha, hora, motivo)
    estado.citas.append(nueva)
    estado.slots_ocupados.add(slot)

    guardar_base_datos()
    mensaje_ok(
        f"Cita #{nueva.obtener_id()} agendada: "
        f"{paciente.obtener_nombre()} con Dr. {medico.obtener_nombre()} "
        f"el {fecha} a las {hora}."
    )


def listar_citas():
    """Muestra todas las citas registradas en tabla formateada."""
    print(titulo("LISTADO DE CITAS MÉDICAS"))

    if not estado.citas:
        mensaje_info("No hay citas registradas.")
        return

    anchos = [4, 18, 18, 11, 6, 10]
    encabezado_tabla(["ID", "Paciente", "Medico", "Fecha", "Hora", "Estado"], anchos)
    for c in estado.citas:
        print(fila_tabla(
            f"#{c.obtener_id()}",
            c.obtener_paciente().obtener_nombre(),
            c.obtener_medico().obtener_nombre(),
            c.obtener_fecha(),
            c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(estado.citas)} cita(s).")


def cambiar_estado_cita():
    """Busca una cita por ID y permite cambiar su estado."""
    print(subtitulo("CAMBIAR ESTADO DE CITA"))

    if not estado.citas:
        mensaje_info("No hay citas registradas.")
        return

    mapa_citas = {c.obtener_id(): c for c in estado.citas}

    try:
        id_buscado = int(input("  ID de la cita        : "))
    except ValueError:
        mensaje_error("Ingrese un número de ID válido.")
        return

    if id_buscado not in mapa_citas:
        mensaje_error(f"No existe la cita con ID #{id_buscado}.")
        return

    cita = mapa_citas[id_buscado]

    print(f"\n  Paciente : {cita.obtener_paciente().obtener_nombre()}")
    print(f"  Medico   : {cita.obtener_medico().obtener_nombre()}")
    print(f"  Fecha    : {cita.obtener_fecha()}  {cita.obtener_hora()}")
    print(f"  Estado   : {cita.obtener_estado()}")

    nuevo_estado = elegir_de_tupla("Nuevo estado:", ESTADOS_CITA)
    cita.cambiar_estado(nuevo_estado)
    guardar_base_datos()
    mensaje_ok(f"Cita #{id_buscado} actualizada a estado '{nuevo_estado}'.")


def buscar_citas_por_paciente():
    """Filtra la lista de citas por DNI de paciente usando filter() + lambda."""
    print(subtitulo("BUSCAR CITAS POR PACIENTE"))

    dni = leer_dni("DNI del paciente      : ")
    paciente = buscar_paciente(dni)
    if not paciente:
        mensaje_error("Paciente no encontrado.")
        return

    resultado = list(filter(lambda c: c.obtener_paciente().obtener_dni() == dni, estado.citas))

    if not resultado:
        mensaje_info(f"No hay citas para '{paciente.obtener_nombre()}'.")
        return

    print(f"\n  Citas de '{paciente.obtener_nombre()}':")
    anchos = [4, 18, 11, 6, 10]
    encabezado_tabla(["ID", "Medico", "Fecha", "Hora", "Estado"], anchos)
    for c in resultado:
        print(fila_tabla(
            f"#{c.obtener_id()}",
            c.obtener_medico().obtener_nombre(),
            c.obtener_fecha(), c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(resultado)} cita(s).")


def buscar_citas_por_medico():
    """Filtra la lista de citas por DNI de médico usando filter() + lambda."""
    print(subtitulo("BUSCAR CITAS POR MÉDICO"))

    dni = leer_dni("DNI del médico        : ")
    medico = buscar_medico(dni)
    if not medico:
        mensaje_error("Médico no encontrado.")
        return

    resultado = list(filter(lambda c: c.obtener_medico().obtener_dni() == dni, estado.citas))

    if not resultado:
        mensaje_info(f"No hay citas para 'Dr. {medico.obtener_nombre()}'.")
        return

    print(f"\n  Citas del Dr. '{medico.obtener_nombre()}':")
    anchos = [4, 22, 11, 6, 10]
    encabezado_tabla(["ID", "Paciente", "Fecha", "Hora", "Estado"], anchos)
    for c in resultado:
        print(fila_tabla(
            f"#{c.obtener_id()}",
            c.obtener_paciente().obtener_nombre(),
            c.obtener_fecha(), c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(resultado)} cita(s).")


def resumen_agendamiento():
    """Estadísticas del módulo de agendamiento."""
    print(titulo("RESUMEN DE AGENDAMIENTO", "-"))

    if not estado.citas:
        mensaje_info("No hay citas registradas aún.")
        return

    conteo_estado = {}
    for c in estado.citas:
        est = c.obtener_estado()
        conteo_estado[est] = conteo_estado.get(est, 0) + 1

    print(f"\n  Total de citas registradas : {len(estado.citas)}")
    print("\n  Citas por estado:")
    for est in ESTADOS_CITA:
        cant = conteo_estado.get(est, 0)
        barra = "=" * cant
        print(f"    {est:<12} {barra}  ({cant})")

    pendientes = [c for c in estado.citas if c.obtener_estado() == "Pendiente"]
    print(f"\n  Citas pendientes           : {len(pendientes)}")

    conteo_medico = {}
    for c in estado.citas:
        nom = c.obtener_medico().obtener_nombre()
        conteo_medico[nom] = conteo_medico.get(nom, 0) + 1
    mas_citas = max(conteo_medico, key=conteo_medico.get)
    print(f"  Medico con mas citas       : {mas_citas} ({conteo_medico[mas_citas]})")


def menu_agendamiento():
    """PASO 2: AGENDAMIENTO — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 2 ]  AGENDAMIENTO"))

        opciones_menu = [
            "Agendar Nueva Cita",
            "Listar Todas las Citas",
            "Buscar Citas por Paciente",
            "Buscar Citas por Médico",
            "Cambiar Estado de Cita",
            "Resumen de Agendamiento",
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

        acciones = {
            1: agendar_cita,
            2: listar_citas,
            3: buscar_citas_por_paciente,
            4: buscar_citas_por_medico,
            5: cambiar_estado_cita,
            6: resumen_agendamiento,
        }

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()
            pausa()

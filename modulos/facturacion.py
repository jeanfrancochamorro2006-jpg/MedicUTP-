# -*- coding: utf-8 -*-
"""
Módulo de FACTURACIÓN — boletas y facturas electrónicas.
"""

import datetime

from clases.factura import Factura

from modulos import estado
from modulos.ui_consola import titulo, subtitulo, linea, encabezado_tabla, fila_tabla, mensaje_ok, mensaje_error, mensaje_info, pausa
from modulos.validaciones import leer_cadena, leer_entero, elegir_de_tupla
from modulos.persistencia import guardar_base_datos
from modulos.utilidades import buscar_cita, generar_ruc10
from modulos.exportar_pdf import guardar_boleta_pdf
from polimorfismo.sobreescritura import imprimir_resumen_entidad


def construir_lineas_boleta(factura):
    """
    Arma línea por línea el contenido del comprobante (boleta o factura).
    Se usa tanto para imprimirlo en consola como para exportarlo a PDF,
    de modo que ambas salidas sean siempre idénticas.
    """
    cita = factura.obtener_cita()
    paciente = cita.obtener_paciente()
    medico = cita.obtener_medico()

    parts = factura.obtener_fecha_emision().split()
    fecha_em = parts[0] if len(parts) > 0 else factura.obtener_fecha_emision()
    hora_em = " ".join(parts[1:]) if len(parts) > 1 else "10:00 AM"

    tipo = factura.obtener_tipo_comprobante()
    prefix = "F001" if tipo == "Factura" else "B001"
    n_comprobante = f"{prefix}-{factura.obtener_id():06d}"

    lineas = [
        "============================================================",
        "                     MEDIC-UTP",
        "          SISTEMA DE CITAS MÉDICAS Y FACTURACIÓN",
        "============================================================",
        "",
        f"                 {tipo.upper()} ELECTRÓNICA",
        "------------------------------------------------------------",
        f"N° {tipo}        : {n_comprobante}",
        f"Fecha Emisión    : {fecha_em}",
        f"Hora Emisión     : {hora_em}",
        "",
    ]

    if tipo == "Factura":
        lineas += [
            f"Adquirente       : {factura.obtener_razon_social()}",
            f"RUC              : {factura.obtener_ruc()}",
            "",
            f"Paciente         : {paciente.obtener_nombre()}",
            f"DNI              : {paciente.obtener_dni()}",
        ]
    else:
        lineas += [
            f"Paciente         : {paciente.obtener_nombre()}",
            f"DNI              : {paciente.obtener_dni()}",
        ]

    lineas += [
        f"Seguro           : {paciente.obtener_seguro()}",
        "",
        f"Médico           : Dr(a). {medico.obtener_nombre()}",
        f"Especialidad     : {medico.obtener_especialidad()}",
        f"Consultorio      : {medico.obtener_consultorio():02d}",
        "",
        "------------------------------------------------------------",
        "DETALLE DE LA ATENCIÓN",
        "------------------------------------------------------------",
        f"Fecha de la cita : {cita.obtener_fecha()}",
        f"Hora de la cita  : {cita.obtener_hora()}",
        f"Motivo           : {cita.obtener_motivo()}",
        "",
        f"Precio Consulta  : S/. {factura.obtener_monto_consulta():.2f}",
        f"Descuento Seguro : S/. {factura.obtener_descuento():.2f}",
        "-----------------------------------------",
        f"TOTAL A PAGAR    : S/. {factura.obtener_total():.2f}",
        "-----------------------------------------",
        "",
        f"Estado de Pago   : {factura.obtener_estado_pago()}",
        f"Método de Pago   : {factura.obtener_metodo_pago()}",
        "",
        "============================================================",
        "        Gracias por confiar en MEDIC-UTP",
        "     Conserve este comprobante de atención",
        "============================================================",
    ]
    return lineas


def imprimir_boleta_ascii(factura):
    """Imprime el comprobante en consola en formato ASCII."""
    print()
    for linea_texto in construir_lineas_boleta(factura):
        print(linea_texto)
    print()


def generar_factura():
    """Registra y genera una nueva boleta o factura para una cita completada."""
    print(subtitulo("GENERAR COMPROBANTE"))

    if not estado.citas:
        mensaje_error("No hay citas registradas en el sistema.")
        return

    try:
        id_cita = int(input("  Ingrese el ID de la Cita    : "))
    except ValueError:
        mensaje_error("El ID de la cita debe ser un número entero.")
        return

    cita = buscar_cita(id_cita)
    if not cita:
        mensaje_error(f"No se encontró la cita con ID #{id_cita}.")
        return

    if cita.obtener_estado() != "Completada":
        mensaje_error(
            f"No se puede facturar. La cita está '{cita.obtener_estado()}'.\n"
            f"  Sólo se permiten facturas para citas con estado 'Completada'."
        )
        return

    factura_previa = next((f for f in estado.facturas if f.obtener_cita_id() == id_cita), None)
    if factura_previa:
        mensaje_error(
            f"Conflicto: Ya existe un comprobante (ID #{factura_previa.obtener_id()}) "
            f"generado para la cita #{id_cita}."
        )
        return

    tipo_comprobante = elegir_de_tupla("Tipo de comprobante:", ("Boleta", "Factura"))

    ruc = ""
    razon_social = ""

    if tipo_comprobante == "Factura":
        dni_paciente = cita.obtener_paciente().obtener_dni()
        ruc = generar_ruc10(dni_paciente)
        print(f"  [i] RUC 10 Generado automáticamente: {ruc}")
        razon_social = leer_cadena("Razón Social (Empresa)      : ")

    metodo_pago = elegir_de_tupla("Método de pago:", ("Efectivo", "Yape"))

    max_id = max([f.obtener_id() for f in estado.facturas], default=0)
    nuevo_id = max_id + 1

    fecha_emision = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")

    nuevo_comprobante = Factura(
        id=nuevo_id,
        cita=cita,
        fecha_emision=fecha_emision,
        tipo_comprobante=tipo_comprobante,
        estado_pago="Completo",
        ruc=ruc,
        razon_social=razon_social,
        metodo_pago=metodo_pago
    )
    estado.facturas.append(nuevo_comprobante)

    guardar_base_datos()
    mensaje_ok(f"{tipo_comprobante} #{nuevo_id} generada con éxito para la Cita #{id_cita}.")

    imprimir_boleta_ascii(nuevo_comprobante)

    ruta_pdf = guardar_boleta_pdf(nuevo_comprobante, construir_lineas_boleta(nuevo_comprobante))
    mensaje_ok(f"Comprobante descargado en PDF: {ruta_pdf}")


def listar_facturas():
    """Muestra todas las facturas/boletas en una tabla formateada."""
    print(titulo("LISTADO DE COMPROBANTES"))

    if not estado.facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    anchos = [4, 8, 8, 22, 10, 10]
    encabezado_tabla(["ID", "Cita ID", "Tipo", "Paciente/Cliente", "Total", "Estado"], anchos)
    for f in estado.facturas:
        cliente = (
            f.obtener_razon_social() if f.obtener_tipo_comprobante() == "Factura"
            else f.obtener_cita().obtener_paciente().obtener_nombre()
        )
        print(fila_tabla(
            f"#{f.obtener_id()}",
            f"#{f.obtener_cita_id()}",
            f.obtener_tipo_comprobante(),
            cliente,
            f"S/. {f.obtener_total():.2f}",
            f.obtener_estado_pago(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(estado.facturas)} comprobante(s).")


def buscar_factura_por_id():
    """Busca una factura/boleta por ID y muestra su resumen usando polimorfismo."""
    print(subtitulo("BUSCAR COMPROBANTE POR ID"))

    if not estado.facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    try:
        id_buscado = int(input("  Ingrese ID del Comprobante  : "))
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return

    factura = next((f for f in estado.facturas if f.obtener_id() == id_buscado), None)
    if not factura:
        mensaje_error(f"No existe el comprobante con ID #{id_buscado}.")
        return

    print("\n  Resumen obtenido mediante polimorfismo:")
    imprimir_resumen_entidad(factura)


def mostrar_detalle_factura():
    """Muestra todos los detalles de cobro de un comprobante específico en formato ASCII."""
    print(subtitulo("DETALLE DE COMPROBANTE"))

    if not estado.facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    try:
        id_buscado = int(input("  Ingrese ID del Comprobante  : "))
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return

    factura = next((f for f in estado.facturas if f.obtener_id() == id_buscado), None)
    if not factura:
        mensaje_error(f"No existe el comprobante con ID #{id_buscado}.")
        return

    imprimir_boleta_ascii(factura)


def descargar_comprobante_pdf():
    """Genera el PDF de un comprobante ya existente, buscándolo por ID."""
    print(subtitulo("DESCARGAR COMPROBANTE EN PDF"))

    if not estado.facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    try:
        id_buscado = int(input("  Ingrese ID del Comprobante  : "))
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return

    factura = next((f for f in estado.facturas if f.obtener_id() == id_buscado), None)
    if not factura:
        mensaje_error(f"No existe el comprobante con ID #{id_buscado}.")
        return

    ruta_pdf = guardar_boleta_pdf(factura, construir_lineas_boleta(factura))
    mensaje_ok(f"Comprobante descargado en PDF: {ruta_pdf}")


def menu_facturacion():
    """PASO 3: FACTURACIÓN — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 3 ]  FACTURACIÓN"))

        opciones_menu = [
            "Generar Factura",
            "Listar Facturas",
            "Buscar Factura por ID",
            "Mostrar Detalle de Factura",
            "Descargar Comprobante en PDF",
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
            1: generar_factura,
            2: listar_facturas,
            3: buscar_factura_por_id,
            4: mostrar_detalle_factura,
            5: descargar_comprobante_pdf,
        }

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()
            pausa()

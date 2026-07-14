# -*- coding: utf-8 -*-
"""
Módulo de EXPORTACIÓN A PDF — comprobantes de facturación.

Genera un archivo PDF con el mismo contenido, en el mismo orden y con
tipografía monoespaciada, tal como se muestra el comprobante en la
consola (boleta o factura electrónica).
"""

import os

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

CARPETA_COMPROBANTES = os.path.join("reportes", "comprobantes")

_FUENTE = "Courier"
_TAMANIO_FUENTE = 9
_INTERLINEA = 12
_MARGEN_IZQUIERDO = 30
_MARGEN_SUPERIOR = 30


def guardar_boleta_pdf(factura, lineas):
    """
    Escribe 'lineas' (la misma lista de texto impresa en consola) dentro
    de un PDF y lo guarda en reportes/comprobantes/. Retorna la ruta del
    archivo generado.
    """
    os.makedirs(CARPETA_COMPROBANTES, exist_ok=True)

    tipo = factura.obtener_tipo_comprobante()
    prefijo = "Factura" if tipo == "Factura" else "Boleta"
    nombre_archivo = f"{prefijo}_{factura.obtener_id():06d}.pdf"
    ruta = os.path.join(CARPETA_COMPROBANTES, nombre_archivo)

    ancho, alto = A5
    pdf = canvas.Canvas(ruta, pagesize=A5)
    pdf.setTitle(f"{prefijo} #{factura.obtener_id()} - MEDIC-UTP")

    y = alto - _MARGEN_SUPERIOR
    pdf.setFont(_FUENTE, _TAMANIO_FUENTE)

    for texto in lineas:
        if y < _MARGEN_SUPERIOR:
            pdf.showPage()
            pdf.setFont(_FUENTE, _TAMANIO_FUENTE)
            y = alto - _MARGEN_SUPERIOR
        pdf.drawString(_MARGEN_IZQUIERDO, y, texto)
        y -= _INTERLINEA

    pdf.save()
    return ruta

# -*- coding: utf-8 -*-
"""
Estado global en memoria de MEDIC-UTP.

Centraliza las colecciones (listas, tuplas y colecciones) que se comparten
entre los módulos de Registro, Agendamiento, Facturación y Análisis de
Datos. Todos los módulos importan estas variables y las mutan con
append()/add()/setdefault() en lugar de reasignarlas, para que el mismo
objeto en memoria sea visible desde cualquier parte del sistema.
"""

# =====================================================================
# TUPLAS — catálogos de opciones válidas (datos que no cambian)
# =====================================================================

ESPECIALIDADES_VALIDAS = (
    "Cardiología", "Dermatología", "Neurología", "Pediatría",
    "Traumatología", "Oftalmología", "Ginecología", "Oncología",
    "Psiquiatría", "Medicina General",
)

TIPOS_SEGURO = ("SIS", "ESSALUD", "Particular", "Otro")

VERSION_SISTEMA = ("MEDIC-UTP", "1.0", "2026")

ESTADOS_CITA = ("Pendiente", "Completada", "Cancelada")

HORAS_ATENCION = (
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "12:00", "14:00", "14:30", "15:00",
    "15:30", "16:00", "16:30", "17:00",
)

PRECIOS_SUGERIDOS = {
    "Cardiología": 150, "Dermatología": 120, "Neurología": 180, "Pediatría": 90,
    "Traumatología": 130, "Oftalmología": 110, "Ginecología": 140, "Oncología": 200,
    "Psiquiatría": 160, "Medicina General": 70,
}

ANCHO_CONSOLA = 60


# =====================================================================
# LISTAS — colecciones principales de objetos en memoria
# =====================================================================

pacientes = []   # Lista de objetos Paciente
medicos = []     # Lista de objetos Medico
citas = []       # Lista de objetos Cita
facturas = []    # Lista de objetos Factura


# =====================================================================
# COLECCIONES — sets y diccionarios de apoyo (búsquedas O(1))
# =====================================================================

dni_pacientes = set()     # DNIs de pacientes ya registrados
dni_medicos = set()       # DNIs de médicos ya registrados
slots_ocupados = set()    # Tuplas (dni_medico, fecha, hora) reservadas

indice_especialidad = {}  # {especialidad: [Medico, ...]}

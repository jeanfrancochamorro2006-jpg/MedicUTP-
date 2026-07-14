# -*- coding: utf-8 -*-
"""
Persistencia del sistema en un archivo JSON (db.json).

db.json se excluye del control de versiones porque su contenido cambia en
cada ejecución del programa y no forma parte del código fuente.
"""

import os
import json

from clases.paciente import Paciente
from clases.medico import Medico
from clases.cita import Cita, _contador_cita_global
from clases.factura import Factura

from modulos import estado
from modulos.utilidades import buscar_paciente, buscar_medico

DB_PATH = "db.json"


def guardar_base_datos():
    """Guarda pacientes, médicos, citas y facturas en db.json."""
    datos = {
        "pacientes": [p.a_dict() for p in estado.pacientes],
        "medicos": [m.a_dict() for m in estado.medicos],
        "citas": [
            {
                "id": c.obtener_id(),
                "paciente_dni": c.obtener_paciente().obtener_dni(),
                "medico_dni": c.obtener_medico().obtener_dni(),
                "fecha": c.obtener_fecha(),
                "hora": c.obtener_hora(),
                "motivo": c.obtener_motivo(),
                "estado": c.obtener_estado(),
            } for c in estado.citas
        ],
        "facturas": [f.a_dict() for f in estado.facturas],
    }
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"\n  [!] Error al guardar la base de datos: {e}")


def cargar_base_datos():
    """Carga pacientes, médicos, citas y facturas desde db.json si existe."""
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Cargar Pacientes
        for p_dict in datos.get("pacientes", []):
            p = Paciente(
                dni=p_dict["dni"],
                nombre=p_dict["nombre"],
                edad=p_dict["edad"],
                telefono=p_dict["telefono"],
                seguro=p_dict["seguro"],
            )
            estado.pacientes.append(p)
            estado.dni_pacientes.add(p.obtener_dni())

        # Cargar Médicos
        for m_dict in datos.get("medicos", []):
            m = Medico(
                dni=m_dict["dni"],
                nombre=m_dict["nombre"],
                especialidad=m_dict["especialidad"],
                consultorio=m_dict["consultorio"],
                precio_consulta=m_dict.get("precio_consulta", 0.0),
            )
            estado.medicos.append(m)
            estado.dni_medicos.add(m.obtener_dni())
            estado.indice_especialidad.setdefault(m.obtener_especialidad(), []).append(m)

        # Cargar Citas
        max_id = 0
        for c_dict in datos.get("citas", []):
            p = buscar_paciente(c_dict["paciente_dni"])
            m = buscar_medico(c_dict["medico_dni"])
            if p and m:
                c = Cita(
                    paciente=p,
                    medico=m,
                    fecha=c_dict["fecha"],
                    hora=c_dict["hora"],
                    motivo=c_dict["motivo"],
                )
                c._id = c_dict["id"]
                # Migración automática del estado "Atendida" a "Completada"
                nuevo_estado = c_dict["estado"]
                if nuevo_estado == "Atendida":
                    nuevo_estado = "Completada"
                c.cambiar_estado(nuevo_estado)
                estado.citas.append(c)
                max_id = max(max_id, c._id)
                estado.slots_ocupados.add(
                    (m.obtener_dni(), c.obtener_fecha(), c.obtener_hora())
                )

        _contador_cita_global[0] = max_id

        # Cargar Facturas
        for f_dict in datos.get("facturas", []):
            cita = next((c for c in estado.citas if c.obtener_id() == f_dict["cita_id"]), None)
            if cita:
                f = Factura(
                    id=f_dict["id"],
                    cita=cita,
                    fecha_emision=f_dict["fecha_emision"],
                    tipo_comprobante=f_dict["tipo_comprobante"],
                    estado_pago=f_dict.get("estado_pago", "Completo"),
                    ruc=f_dict.get("ruc", ""),
                    razon_social=f_dict.get("razon_social", ""),
                    metodo_pago=f_dict.get("metodo_pago", "Efectivo"),
                )
                f._monto_consulta = f_dict["monto_consulta"]
                f._descuento = f_dict["descuento"]
                f._total = f_dict["total"]
                estado.facturas.append(f)
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"\n  [!] Error al cargar la base de datos: {e}")

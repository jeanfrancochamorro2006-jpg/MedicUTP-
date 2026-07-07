# -*- coding: utf-8 -*-
"""
Clase Factura - Entidad del módulo de facturación.
"""

class Factura:
    """
    Representa la factura de una cita médica completada.
    """
    def __init__(self, id, cita, fecha_emision, tipo_comprobante, estado_pago="Completo", ruc="", razon_social="", metodo_pago="Efectivo"):
        self._id = id
        self._cita = cita
        self._cita_id = cita.obtener_id()
        self._fecha_emision = fecha_emision
        self._tipo_comprobante = tipo_comprobante
        self._monto_consulta = 0.0
        self._descuento = 0.0
        self._total = 0.0
        self._estado_pago = estado_pago
        self._ruc = ruc
        self._razon_social = razon_social
        self._metodo_pago = metodo_pago
        self.calcular_total()

    # Getters
    def obtener_id(self): return self._id
    def obtener_cita(self): return self._cita
    def obtener_cita_id(self): return self._cita_id
    def obtener_fecha_emision(self): return self._fecha_emision
    def obtener_tipo_comprobante(self): return self._tipo_comprobante
    def obtener_monto_consulta(self): return self._monto_consulta
    def obtener_descuento(self): return self._descuento
    def obtener_total(self): return self._total
    def obtener_estado_pago(self): return self._estado_pago
    def obtener_ruc(self): return self._ruc
    def obtener_razon_social(self): return self._razon_social
    def obtener_metodo_pago(self): return self._metodo_pago

    # Setters
    def establecer_id(self, id): self._id = id
    def establecer_cita(self, cita):
        self._cita = cita
        self._cita_id = cita.obtener_id()
        self.calcular_total()
    def establecer_cita_id(self, cita_id): self._cita_id = cita_id
    def establecer_fecha_emision(self, fecha_emision): self._fecha_emision = fecha_emision
    def establecer_tipo_comprobante(self, tipo_comprobante): self._tipo_comprobante = tipo_comprobante
    def establecer_monto_consulta(self, monto_consulta): self._monto_consulta = monto_consulta
    def establecer_descuento(self, descuento): self._descuento = descuento
    def establecer_total(self, total): self._total = total
    def establecer_estado_pago(self, estado_pago): self._estado_pago = estado_pago
    def establecer_ruc(self, ruc): self._ruc = ruc
    def establecer_razon_social(self, razon_social): self._razon_social = razon_social
    def establecer_metodo_pago(self, metodo_pago): self._metodo_pago = metodo_pago

    def calcular_total(self):
        """
        Calcula el monto_consulta, descuento y total de la factura.
        """
        medico = self._cita.obtener_medico()
        self._monto_consulta = float(medico.obtener_precio_consulta())

        paciente = self._cita.obtener_paciente()
        seguro = paciente.obtener_seguro()

        # Descuentos:
        # ESSALUD -> 30%
        # SIS -> 20%
        # Particular -> 0%
        # Otro -> 10%
        if seguro == "ESSALUD":
            porcentaje = 0.30
        elif seguro == "SIS":
            porcentaje = 0.20
        elif seguro == "Particular":
            porcentaje = 0.0
        else:
            porcentaje = 0.10

        self._descuento = self._monto_consulta * porcentaje
        self._total = self._monto_consulta - self._descuento

    def a_dict(self):
        """Convierte el objeto Factura a diccionario para reportes y persistencia."""
        return {
            "id": self._id,
            "cita_id": self._cita_id,
            "fecha_emision": self._fecha_emision,
            "tipo_comprobante": self._tipo_comprobante,
            "monto_consulta": self._monto_consulta,
            "descuento": self._descuento,
            "total": self._total,
            "estado_pago": self._estado_pago,
            "ruc": self._ruc,
            "razon_social": self._razon_social,
            "metodo_pago": self._metodo_pago,
        }

    # Polimorfismo por Sobreescritura (Method Overriding)
    def obtener_resumen(self):
        """Retorna los datos específicos formateados de una factura."""
        return f"{self._tipo_comprobante} #{self._id} | Cita #{self._cita_id} | Total: S/. {self._total:.2f} | Estado: {self._estado_pago}"

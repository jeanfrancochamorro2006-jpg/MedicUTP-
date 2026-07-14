# -*- coding: utf-8 -*-
"""Pruebas unitarias de la clase Factura y del cálculo del RUC 10."""

import unittest

from clases.paciente import Paciente
from clases.medico import Medico
from clases.cita import Cita
from clases.factura import Factura
from modulos.utilidades import generar_ruc10


def _crear_cita(seguro="Particular", precio_consulta=100.0):
    paciente = Paciente(dni="12345678", nombre="Ana Torres", edad=30,
                         telefono="987654321", seguro=seguro)
    medico = Medico(dni="87654321", nombre="Luis Perez", especialidad="Pediatría",
                     consultorio=5, precio_consulta=precio_consulta)
    return Cita(paciente, medico, fecha="25/07/2026", hora="10:00", motivo="Control")


class TestFacturaCalcularTotal(unittest.TestCase):

    def _factura_para(self, seguro):
        cita = _crear_cita(seguro=seguro, precio_consulta=100.0)
        return Factura(id=1, cita=cita, fecha_emision="14/07/2026 10:00 AM",
                        tipo_comprobante="Boleta")

    def test_descuento_essalud_30_porciento(self):
        f = self._factura_para("ESSALUD")
        self.assertAlmostEqual(f.obtener_descuento(), 30.0)
        self.assertAlmostEqual(f.obtener_total(), 70.0)

    def test_descuento_sis_20_porciento(self):
        f = self._factura_para("SIS")
        self.assertAlmostEqual(f.obtener_descuento(), 20.0)
        self.assertAlmostEqual(f.obtener_total(), 80.0)

    def test_particular_sin_descuento(self):
        f = self._factura_para("Particular")
        self.assertAlmostEqual(f.obtener_descuento(), 0.0)
        self.assertAlmostEqual(f.obtener_total(), 100.0)

    def test_otro_seguro_10_porciento(self):
        f = self._factura_para("Otro")
        self.assertAlmostEqual(f.obtener_descuento(), 10.0)
        self.assertAlmostEqual(f.obtener_total(), 90.0)

    def test_a_dict_incluye_todos_los_campos(self):
        f = self._factura_para("Particular")
        d = f.a_dict()
        for campo in ("id", "cita_id", "total", "descuento", "monto_consulta",
                      "tipo_comprobante", "estado_pago"):
            self.assertIn(campo, d)


class TestGenerarRuc10(unittest.TestCase):
    """
    Verifica el algoritmo del dígito verificador módulo 11 de SUNAT
    usado para generar el RUC 10 a partir del DNI del paciente.
    """

    def test_ruc_tiene_11_digitos_y_empieza_en_10(self):
        ruc = generar_ruc10("45678912")
        self.assertEqual(len(ruc), 11)
        self.assertTrue(ruc.startswith("10"))
        self.assertTrue(ruc.isdigit())

    def test_ruc_es_determinista(self):
        self.assertEqual(generar_ruc10("12345678"), generar_ruc10("12345678"))

    def test_ruc_distinto_para_dni_distinto(self):
        self.assertNotEqual(generar_ruc10("12345678"), generar_ruc10("87654321"))

    def test_digito_verificador_calculado_manualmente(self):
        dni = "12345678"
        ruc_base = "10" + dni
        multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = sum(int(ruc_base[i]) * multiplicadores[i] for i in range(10))
        resto = suma % 11
        verificador = 11 - resto
        if verificador == 11:
            verificador = 0
        elif verificador == 10:
            verificador = 1
        esperado = ruc_base + str(verificador)
        self.assertEqual(generar_ruc10(dni), esperado)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Pruebas unitarias del módulo de análisis de datos (pandas/numpy).

Verifica que los DataFrames se construyan correctamente a partir de las
colecciones en memoria y que el cálculo de ingresos con pandas coincida
con el cálculo funcional equivalente (functools.reduce).
"""

import unittest
from functools import reduce

from clases.paciente import Paciente
from clases.medico import Medico
from clases.cita import Cita
from clases.factura import Factura

from modulos import estado
from modulos.analisis_datos import df_pacientes, df_facturas


class TestAnalisisDatos(unittest.TestCase):

    def setUp(self):
        # Se guarda el estado original y se limpia (in-place) para
        # aislar cada prueba sin romper la referencia compartida.
        self._pacientes_originales = list(estado.pacientes)
        self._medicos_originales = list(estado.medicos)
        self._citas_originales = list(estado.citas)
        self._facturas_originales = list(estado.facturas)
        estado.pacientes.clear()
        estado.medicos.clear()
        estado.citas.clear()
        estado.facturas.clear()

        p1 = Paciente(dni="60606060", nombre="Rosa Vidal", edad=33,
                       telefono="955555555", seguro="SIS")
        p2 = Paciente(dni="70707070", nombre="Tito Fano", edad=61,
                       telefono="955555556", seguro="ESSALUD")
        m1 = Medico(dni="80808080", nombre="Dra. Nina Cruz",
                    especialidad="Pediatría", consultorio=1, precio_consulta=90.0)

        c1 = Cita(p1, m1, fecha="21/07/2026", hora="08:00", motivo="Control")
        c1.cambiar_estado("Completada")
        c2 = Cita(p2, m1, fecha="22/07/2026", hora="08:30", motivo="Dolor")
        c2.cambiar_estado("Completada")

        f1 = Factura(id=1, cita=c1, fecha_emision="14/07/2026 09:00 AM", tipo_comprobante="Boleta")
        f2 = Factura(id=2, cita=c2, fecha_emision="14/07/2026 09:10 AM", tipo_comprobante="Boleta")

        estado.pacientes.extend([p1, p2])
        estado.medicos.append(m1)
        estado.citas.extend([c1, c2])
        estado.facturas.extend([f1, f2])

    def tearDown(self):
        estado.pacientes.clear()
        estado.medicos.clear()
        estado.citas.clear()
        estado.facturas.clear()
        estado.pacientes.extend(self._pacientes_originales)
        estado.medicos.extend(self._medicos_originales)
        estado.citas.extend(self._citas_originales)
        estado.facturas.extend(self._facturas_originales)

    def test_df_pacientes_columnas_y_filas(self):
        df = df_pacientes()
        self.assertEqual(len(df), 2)
        for columna in ("dni", "nombre", "edad", "seguro"):
            self.assertIn(columna, df.columns)

    def test_df_facturas_incluye_especialidad_del_medico(self):
        df = df_facturas()
        self.assertEqual(len(df), 2)
        self.assertTrue((df["especialidad"] == "Pediatría").all())

    def test_ingreso_total_pandas_coincide_con_reduce_funcional(self):
        df = df_facturas()
        total_pandas = df["total"].sum()
        total_reduce = reduce(lambda acc, f: acc + f.obtener_total(), estado.facturas, 0.0)
        self.assertAlmostEqual(total_pandas, total_reduce)


if __name__ == "__main__":
    unittest.main()

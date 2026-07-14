# -*- coding: utf-8 -*-
"""
Pruebas unitarias de BuscadorClinico (sobrecarga de métodos simulada)
y de la función polimórfica imprimir_resumen_entidad (sobreescritura).
"""

import io
import unittest
from contextlib import redirect_stdout

from clases.paciente import Paciente
from clases.medico import Medico
from polimorfismo.sobrecarga import BuscadorClinico
from polimorfismo.sobreescritura import imprimir_resumen_entidad


class TestBuscadorClinicoSobrecarga(unittest.TestCase):

    def setUp(self):
        self.pacientes = [
            Paciente(dni="11111111", nombre="Maria Lopez", edad=28,
                     telefono="900000001", seguro="SIS"),
            Paciente(dni="22222222", nombre="Mario Lopez", edad=45,
                     telefono="900000002", seguro="ESSALUD"),
        ]
        self.buscador = BuscadorClinico()

    def test_firma_sin_filtros_retorna_toda_la_coleccion(self):
        resultado = self.buscador.buscar(self.pacientes)
        self.assertEqual(len(resultado), 2)

    def test_firma_solo_dni(self):
        resultado = self.buscador.buscar(self.pacientes, dni="11111111")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].obtener_nombre(), "Maria Lopez")

    def test_firma_solo_nombre_busqueda_parcial(self):
        resultado = self.buscador.buscar(self.pacientes, nombre="lopez")
        self.assertEqual(len(resultado), 2)

    def test_firma_dni_y_nombre_combinados(self):
        resultado = self.buscador.buscar(self.pacientes, dni="22222222", nombre="mario")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].obtener_dni(), "22222222")

    def test_firma_dni_y_nombre_sin_coincidencia(self):
        resultado = self.buscador.buscar(self.pacientes, dni="11111111", nombre="mario")
        self.assertEqual(resultado, [])


class TestImprimirResumenEntidadPolimorfismo(unittest.TestCase):

    def test_llama_obtener_resumen_del_objeto_recibido(self):
        medico = Medico(dni="33333333", nombre="Sofia Cano",
                         especialidad="Neurología", consultorio=9,
                         precio_consulta=180.0)
        salida = io.StringIO()
        with redirect_stdout(salida):
            imprimir_resumen_entidad(medico)
        self.assertIn("Sofia Cano", salida.getvalue())
        self.assertIn("Neurología", salida.getvalue())

    def test_objeto_sin_obtener_resumen_no_lanza_excepcion(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            imprimir_resumen_entidad(object())
        self.assertIn("no soporta", salida.getvalue())


if __name__ == "__main__":
    unittest.main()

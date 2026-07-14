# -*- coding: utf-8 -*-
"""
Pruebas unitarias de las clases del dominio: constructores, herencia
simple, herencia múltiple, encapsulamiento y polimorfismo por
sobreescritura.
"""

import unittest

from clases.persona import Persona
from clases.contacto import InformacionContacto
from clases.paciente import Paciente
from clases.medico import Medico
from clases.cita import Cita


class TestHerenciaSimple(unittest.TestCase):
    """Medico hereda de Persona (herencia simple, vía super())."""

    def setUp(self):
        self.medico = Medico(dni="11223344", nombre="Carla Ruiz",
                              especialidad="Cardiología", consultorio=3,
                              precio_consulta=150.0)

    def test_medico_es_instancia_de_persona(self):
        self.assertIsInstance(self.medico, Persona)

    def test_medico_hereda_atributos_de_persona(self):
        self.assertEqual(self.medico.obtener_dni(), "11223344")
        self.assertEqual(self.medico.obtener_nombre(), "Carla Ruiz")

    def test_medico_sobreescribe_obtener_resumen(self):
        resumen = self.medico.obtener_resumen()
        self.assertIn("Cardiología", resumen)
        self.assertIn("Carla Ruiz", resumen)


class TestHerenciaMultiple(unittest.TestCase):
    """Paciente hereda de Persona e InformacionContacto (herencia múltiple)."""

    def setUp(self):
        self.paciente = Paciente(dni="55667788", nombre="Jorge Diaz", edad=40,
                                  telefono="999888777", seguro="SIS")

    def test_paciente_es_instancia_de_ambas_superclases(self):
        self.assertIsInstance(self.paciente, Persona)
        self.assertIsInstance(self.paciente, InformacionContacto)

    def test_paciente_hereda_telefono_de_informacion_contacto(self):
        self.assertEqual(self.paciente.obtener_telefono(), "999888777")

    def test_setter_seguro_valida_opciones_permitidas(self):
        self.paciente.establecer_seguro("ESSALUD")
        self.assertEqual(self.paciente.obtener_seguro(), "ESSALUD")
        self.paciente.establecer_seguro("Invalido")
        # El seguro inválido se ignora; conserva el último valor válido.
        self.assertEqual(self.paciente.obtener_seguro(), "ESSALUD")


class TestPolimorfismoSobreescritura(unittest.TestCase):
    """obtener_resumen() se comporta distinto según la subclase (overriding)."""

    def test_resumen_distinto_entre_paciente_y_medico(self):
        paciente = Paciente(dni="10101010", nombre="Eva Soto", edad=25,
                             telefono="900000000", seguro="Particular")
        medico = Medico(dni="20202020", nombre="Raul Vega",
                         especialidad="Dermatología", consultorio=2,
                         precio_consulta=120.0)
        self.assertNotEqual(paciente.obtener_resumen(), medico.obtener_resumen())
        self.assertIn("Paciente", paciente.obtener_resumen())
        self.assertIn("Médico", medico.obtener_resumen())


class TestComposicionCita(unittest.TestCase):
    """Cita compone objetos Paciente y Medico, y valida cambios de estado."""

    def setUp(self):
        paciente = Paciente(dni="30303030", nombre="Ines Rojas", edad=50,
                             telefono="911111111", seguro="Otro")
        medico = Medico(dni="40404040", nombre="Pablo Leon",
                         especialidad="Oftalmología", consultorio=7,
                         precio_consulta=110.0)
        self.cita = Cita(paciente, medico, fecha="20/07/2026", hora="09:00",
                          motivo="Revisión")

    def test_estado_inicial_pendiente(self):
        self.assertEqual(self.cita.obtener_estado(), "Pendiente")

    def test_cambiar_estado_valido(self):
        self.cita.cambiar_estado("Completada")
        self.assertEqual(self.cita.obtener_estado(), "Completada")

    def test_cambiar_estado_invalido_se_ignora(self):
        self.cita.cambiar_estado("Estado Inexistente")
        self.assertEqual(self.cita.obtener_estado(), "Pendiente")


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Clase Medico - Hereda de Persona (Herencia Simple).
"""

from clases.persona import Persona

class Medico(Persona):
    """
    Medico demuestra HERENCIA SIMPLE.
    Hereda directamente de la superclase Persona.
    """
    def __init__(self, dni, nombre, especialidad, consultorio, precio_consulta=0.0):
        # Inicializa la clase base Persona usando super()
        super().__init__(dni, nombre)
        
        # Atributos específicos del médico
        self._especialidad = especialidad
        self._consultorio = consultorio
        self._precio_consulta = precio_consulta

    # Métodos específicos
    def obtener_especialidad(self):
        return self._especialidad

    def obtener_consultorio(self):
        return self._consultorio

    def obtener_precio_consulta(self):
        return self._precio_consulta

    def establecer_precio_consulta(self, nuevo_precio):
        self._precio_consulta = nuevo_precio

    def a_dict(self):
        """Convierte el objeto Medico a diccionario para reportes."""
        return {
            "dni":          self._dni,
            "nombre":       self._nombre,
            "especialidad": self._especialidad,
            "consultorio":  self._consultorio,
            "precio_consulta": self._precio_consulta,
        }

    # Polimorfismo por Sobreescritura (Method Overriding)
    def obtener_resumen(self):
        """
        Sobreescribe el método obtener_resumen de la superclase Persona.
        Retorna los datos específicos formateados de un médico.
        """
        return f"Médico: Dr(a). {self._nombre} | Especialidad: {self._especialidad} | Consultorio: N° {self._consultorio} | Consulta: S/. {self._precio_consulta:.2f}"

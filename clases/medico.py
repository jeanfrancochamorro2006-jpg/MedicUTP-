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
    def __init__(self, dni, nombre, especialidad, consultorio):
        # Inicializa la clase base Persona usando super()
        super().__init__(dni, nombre)
        
        # Atributos específicos del médico
        self._especialidad = especialidad
        self._consultorio = consultorio

    # Métodos específicos
    def obtener_especialidad(self):
        return self._especialidad

    def obtener_consultorio(self):
        return self._consultorio

    def a_dict(self):
        """Convierte el objeto Medico a diccionario para reportes."""
        return {
            "dni":          self._dni,
            "nombre":       self._nombre,
            "especialidad": self._especialidad,
            "consultorio":  self._consultorio,
        }

    # Polimorfismo por Sobreescritura (Method Overriding)
    def obtener_resumen(self):
        """
        Sobreescribe el método obtener_resumen de la superclase Persona.
        Retorna los datos específicos formateados de un médico.
        """
        return f"Médico: Dr(a). {self._nombre} | Especialidad: {self._especialidad} | Consultorio: N° {self._consultorio}"

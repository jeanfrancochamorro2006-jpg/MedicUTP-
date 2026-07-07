# -*- coding: utf-8 -*-
"""
Clase Paciente - Hereda de Persona e InformacionContacto (Herencia Múltiple).
"""

from clases.persona import Persona
from clases.contacto import InformacionContacto

class Paciente(Persona, InformacionContacto):
    """
    Paciente demuestra HERENCIA MÚLTIPLE.
    Hereda atributos de identificación de Persona y atributos de comunicación de InformacionContacto.
    """
    def __init__(self, dni, nombre, edad, telefono, seguro="Particular"):
        # Inicialización explícita de ambas clases base
        Persona.__init__(self, dni, nombre)
        InformacionContacto.__init__(self, telefono)
        
        # Atributos específicos del Paciente
        self._edad = edad
        self._seguro = seguro

    # Métodos específicos
    def obtener_edad(self):
        return self._edad

    def obtener_seguro(self):
        return self._seguro

    def establecer_seguro(self, nuevo_seguro):
        """
        Setter para modificar el seguro.
        Demuestra el concepto de Setter al permitir cambiar el atributo con validación.
        """
        if nuevo_seguro in ("SIS", "ESSALUD", "Particular", "Otro"):
            self._seguro = nuevo_seguro
        else:
            print("  [!] Error: Tipo de seguro inválido.")

    def a_dict(self):
        """Convierte el objeto Paciente a diccionario para reportes."""
        return {
            "dni":      self._dni,
            "nombre":   self._nombre,
            "edad":     self._edad,
            "telefono": self._telefono,
            "seguro":   self._seguro,
        }

    # Polimorfismo por Sobreescritura (Method Overriding)
    def obtener_resumen(self):
        """
        Sobreescribe el método obtener_resumen de la superclase Persona.
        Retorna los datos específicos formateados de un paciente.
        """
        return f"Paciente: {self._nombre} | DNI: {self._dni} | Seguro: {self._seguro} | Edad: {self._edad} años"

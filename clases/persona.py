# -*- coding: utf-8 -*-
"""
Clase Persona - Base del sistema Medic-UTP.
Representa a cualquier persona registrada con DNI y nombre.
"""

class Persona:
    """
    Clase base (Superclase) que contiene los atributos comunes.
    Demuestra los conceptos de Clase, Objeto y Constructor (__init__).
    """
    def __init__(self, dni, nombre):
        # El constructor inicializa los atributos encapsulados (con guion bajo)
        self._dni = dni
        self._nombre = nombre

    # Métodos Getters para acceder a los atributos protegidos
    def obtener_dni(self):
        return self._dni

    def obtener_nombre(self):
        return self._nombre

    def obtener_resumen(self):
        """
        Método base de presentación.
        Este método será sobreescrito por las subclases (Polimorfismo por Sobreescritura).
        """
        return f"Persona: {self._nombre} | DNI: {self._dni}"

# -*- coding: utf-8 -*-
"""
Clase InformacionContacto - Utilizada para Herencia Múltiple.
Contiene información básica de contacto como el número de teléfono.
"""

class InformacionContacto:
    """
    Clase base secundaria para gestionar datos de contacto.
    Permite demostrar la HERENCIA MÚLTIPLE al heredarse junto con Persona.
    """
    def __init__(self, telefono):
        # Constructor que guarda el teléfono del contacto
        self._telefono = telefono

    def obtener_telefono(self):
        return self._telefono

    def establecer_telefono(self, nuevo_telefono):
        """
        Setter para modificar el teléfono.
        Valida que el teléfono tenga solo números antes de cambiarlo.
        """
        if nuevo_telefono.isdigit():
            self._telefono = nuevo_telefono
        else:
            print("  [!] Error: El teléfono debe contener solo números.")


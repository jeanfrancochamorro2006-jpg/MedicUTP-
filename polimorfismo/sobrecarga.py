# -*- coding: utf-8 -*-
"""
Polimorfismo por Sobrecarga de Métodos (Method Overloading)
Simulación de sobrecarga usando parámetros opcionales y valores por defecto.
"""

class BuscadorClinico:
    """
    Demuestra la simulación de Sobrecarga en Python.
    Permite buscar elementos en una colección usando diferentes criterios y firmas.
    """
    def buscar(self, coleccion, dni=None, nombre=None):
        """
        Método sobrecargado simulado.
        
        Firmas simuladas:
        - buscar(coleccion) -> Retorna toda la colección.
        - buscar(coleccion, dni=dni) -> Busca solo por DNI.
        - buscar(coleccion, nombre=nombre) -> Busca solo por coincidencia de nombre.
        - buscar(coleccion, dni=dni, nombre=nombre) -> Busca por DNI y Nombre a la vez.
        """
        # Caso 1: Búsqueda por DNI y Nombre a la vez
        if dni is not None and nombre is not None:
            return [elem for elem in coleccion 
                    if elem.obtener_dni() == dni and nombre.lower() in elem.obtener_nombre().lower()]
        
        # Caso 2: Búsqueda solo por DNI
        elif dni is not None:
            return [elem for elem in coleccion if elem.obtener_dni() == dni]
        
        # Caso 3: Búsqueda solo por Nombre
        elif nombre is not None:
            return [elem for elem in coleccion if nombre.lower() in elem.obtener_nombre().lower()]
        
        # Caso 4: Firma por defecto (retornar todos)
        else:
            return coleccion

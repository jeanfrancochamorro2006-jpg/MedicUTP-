# -*- coding: utf-8 -*-
"""
Polimorfismo por Sobreescritura (Method Overriding)
Demuestra cómo una misma función puede interactuar con diferentes objetos
que implementan el mismo método con diferentes comportamientos.
"""

def imprimir_resumen_entidad(entidad):
    """
    Función polimórfica que recibe un objeto (Paciente, Medico, o Persona)
    y llama a su método obtener_resumen().
    
    El comportamiento de esta función varía dinámicamente según el objeto que se pase.
    """
    if hasattr(entidad, "obtener_resumen"):
        print(f"  [Polimorfismo] -> {entidad.obtener_resumen()}")
    else:
        print("  [!] El objeto no soporta el método obtener_resumen().")

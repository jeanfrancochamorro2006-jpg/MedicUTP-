# -*- coding: utf-8 -*-
"""
MEDIC-UTP - Sistema de Citas Médicas y Facturación
Curso: Programación Orientada a Objetos (POO)

AVANCE 1: En esta entrega SOLO el módulo de REGISTRO está funcional.
          Los módulos de AGENDAMIENTO y FACTURACIÓN se muestran en el
          menú pero quedarán implementados en el siguiente avance.

Flujo del sistema:
    REGISTRO  ->  AGENDAMIENTO  ->  FACTURACIÓN
"""

import sys

# =====================================================================
# 1. HERENCIA SIMPLE: Clase base Persona y subclases Paciente y Medico
# =====================================================================
# Persona es la superclase. Paciente y Medico heredan de ella y
# comparten los atributos comunes _dni y _nombre (reutilización).
# =====================================================================

class Persona:
    """Clase base con atributos comunes (encapsulamiento con guion bajo)."""
    def __init__(self, dni, nombre):
        self._dni = dni
        self._nombre = nombre

    def obtener_dni(self):
        return self._dni

    def obtener_nombre(self):
        return self._nombre


class Paciente(Persona):
    """Paciente hereda de Persona (Herencia Simple)."""
    def __init__(self, dni, nombre, edad, telefono):
        super().__init__(dni, nombre)
        self._edad = edad
        self._telefono = telefono

    def obtener_edad(self):
        return self._edad

    def obtener_telefono(self):
        return self._telefono


class Medico(Persona):
    """Medico hereda de Persona (Herencia Simple)."""
    def __init__(self, dni, nombre, especialidad):
        super().__init__(dni, nombre)
        self._especialidad = especialidad

    def obtener_especialidad(self):
        return self._especialidad


# =====================================================================
# 2. ALMACENAMIENTO EN ARREGLOS (LISTAS EN MEMORIA)
# =====================================================================
pacientes = []   # arreglo de objetos Paciente
medicos = []     # arreglo de objetos Medico


# =====================================================================
# 3. FUNCIONES DE VALIDACIÓN (TRY/EXCEPT)
# =====================================================================

def leer_cadena(mensaje):
    """Lee texto y asegura que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("[!] Error: Este campo es obligatorio.")


def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero controlando errores con try/except."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"[!] El valor mínimo es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"[!] El valor máximo es {maximo}.")
                continue
            return valor
        except ValueError:
            print("[!] Error: Ingrese únicamente números enteros.")


def leer_dni(mensaje):
    """Valida un DNI de exactamente 8 dígitos."""
    while True:
        dni = input(mensaje).strip()
        if dni.isdigit() and len(dni) == 8:
            return dni
        print("[!] El DNI debe tener exactamente 8 dígitos.")


def buscar_paciente(dni):
    """Recorre el arreglo de pacientes buscando por DNI."""
    for p in pacientes:
        if p.obtener_dni() == dni:
            return p
    return None


def buscar_medico(dni):
    """Recorre el arreglo de médicos buscando por DNI."""
    for m in medicos:
        if m.obtener_dni() == dni:
            return m
    return None


# =====================================================================
# 4. FUNCIONES DE REGISTRO (ÚNICO MÓDULO FUNCIONAL EN ESTE AVANCE)
# =====================================================================

def registrar_paciente():
    print("\n--- REGISTRAR PACIENTE ---")
    dni = leer_dni("DNI del paciente: ")
    if buscar_paciente(dni):
        print("[!] Ese paciente ya está registrado.")
        return
    nombre = leer_cadena("Nombre completo: ")
    edad = leer_entero("Edad: ", minimo=0, maximo=120)
    telefono = leer_cadena("Teléfono: ")
    pacientes.append(Paciente(dni, nombre, edad, telefono))
    print(f"[+] Paciente '{nombre}' registrado con éxito.")


def registrar_medico():
    print("\n--- REGISTRAR MÉDICO ---")
    dni = leer_dni("DNI del médico: ")
    if buscar_medico(dni):
        print("[!] Ese médico ya está registrado.")
        return
    nombre = leer_cadena("Nombre completo: ")
    especialidad = leer_cadena("Especialidad: ")
    medicos.append(Medico(dni, nombre, especialidad))
    print(f"[+] Médico '{nombre}' registrado con éxito.")


def mostrar_pacientes():
    print("\n===== LISTA DE PACIENTES =====")
    if not pacientes:
        print("No hay pacientes registrados.")
        return
    print(f"{'DNI':<10} | {'Nombre':<25} | {'Edad':<5} | {'Teléfono':<12}")
    print("-" * 60)
    for p in pacientes:
        print(f"{p.obtener_dni():<10} | {p.obtener_nombre():<25} | {p.obtener_edad():<5} | {p.obtener_telefono():<12}")


def mostrar_medicos():
    print("\n===== LISTA DE MÉDICOS =====")
    if not medicos:
        print("No hay médicos registrados.")
        return
    print(f"{'DNI':<10} | {'Nombre':<25} | {'Especialidad':<20}")
    print("-" * 60)
    for m in medicos:
        print(f"{m.obtener_dni():<10} | {m.obtener_nombre():<25} | {m.obtener_especialidad():<20}")


# =====================================================================
# 5. SUBMENÚS DEL FLUJO
# =====================================================================

def menu_registro():
    """PASO 1: REGISTRO (módulo funcional en este avance)."""
    while True:
        print("\n" + "-" * 45)
        print("   [ PASO 1 ]  REGISTRO")
        print("-" * 45)
        print("1. Registrar Paciente")
        print("2. Registrar Médico")
        print("3. Mostrar Pacientes")
        print("4. Mostrar Médicos")
        print("0. Volver al Menú Principal")
        print("-" * 45)
        op = leer_entero("Opción (0-4): ", minimo=0, maximo=4)
        if op == 1:
            registrar_paciente()
        elif op == 2:
            registrar_medico()
        elif op == 3:
            mostrar_pacientes()
        elif op == 4:
            mostrar_medicos()
        elif op == 0:
            return


def menu_en_construccion(nombre):
    """PASO 2 y 3: aún no implementados en este avance."""
    print(f"\n[i] El módulo '{nombre}' estará disponible en el próximo avance.")


# =====================================================================
# 6. MENÚ PRINCIPAL
# =====================================================================

def main():
    while True:
        print("\n" + "=" * 45)
        print("          SISTEMA  MEDIC - UTP")
        print("=" * 45)
        print("  REGISTRO -> AGENDAMIENTO -> FACTURACIÓN")
        print("=" * 45)
        print("1. PASO 1 -> REGISTRO          (disponible)")
        print("2. PASO 2 -> AGENDAMIENTO      (próximamente)")
        print("3. PASO 3 -> FACTURACIÓN       (próximamente)")
        print("0. Salir del Sistema")
        print("=" * 45)
        op = leer_entero("Opción (0-3): ", minimo=0, maximo=3)
        if op == 1:
            menu_registro()
        elif op == 2:
            menu_en_construccion("AGENDAMIENTO")
        elif op == 3:
            menu_en_construccion("FACTURACIÓN")
        elif op == 0:
            print("\n¡Gracias por utilizar MEDIC-UTP!")
            sys.exit(0)


if __name__ == "__main__":
    main()

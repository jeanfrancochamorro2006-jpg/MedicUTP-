# -*- coding: utf-8 -*-
"""
MEDIC-UTP - Sistema de Citas Médicas y Facturación
Curso: Programación Orientada a Objetos (POO)

AVANCE 1: Módulo de REGISTRO funcional.
AVANCE 2: Módulo de AGENDAMIENTO funcional (nuevo en esta entrega).
          El módulo de FACTURACIÓN quedará para el siguiente avance.

Flujo del sistema:
    REGISTRO  ->  AGENDAMIENTO  ->  FACTURACIÓN
"""

import sys
import datetime
import os
import json



# =====================================================================
# [NUEVO] MÓDULO DE CONFIGURACIÓN — TUPLAS COMO CONSTANTES INMUTABLES
# =====================================================================
# Las tuplas son ideales para datos que NO deben cambiar en ejecución.
# Se usan como catálogos de opciones válidas para el sistema.
# =====================================================================

ESPECIALIDADES_VALIDAS = (                                 # [NUEVO] tupla de especialidades válidas
    "Cardiología", "Dermatología", "Neurología", "Pediatría",
    "Traumatología", "Oftalmología", "Ginecología", "Oncología",
    "Psiquiatría", "Medicina General"
)

TIPOS_SEGURO = ("SIS", "ESSALUD", "Particular", "Otro")   # [NUEVO] tupla de tipos de seguro

VERSION_SISTEMA = ("MEDIC-UTP", "1.0", "2025")            # [NUEVO] tupla de versión del sistema

ANCHO_CONSOLA = 60                                         # [NUEVO] constante de diseño de pantalla


# =====================================================================
# [NUEVO] MÓDULO DE DISEÑO DE CONSOLA
# =====================================================================
# Centraliza toda la lógica de presentación en funciones reutilizables.
# Permite cambiar el estilo visual desde un solo lugar (separación de capas).
# =====================================================================

def linea(caracter="=", ancho=ANCHO_CONSOLA):              # [NUEVO]
    """Devuelve una línea decorativa del ancho indicado."""
    return caracter * ancho


def titulo(texto, caracter="="):                           # [NUEVO]
    """Devuelve un bloque de título centrado entre líneas decorativas."""
    return (
        f"\n{linea(caracter)}\n"
        f"{texto.center(ANCHO_CONSOLA)}\n"
        f"{linea(caracter)}"
    )


def subtitulo(texto):                                      # [NUEVO]
    """Encabezado de sección secundaria con guiones."""
    return f"\n{linea('-')}\n  {texto}\n{linea('-')}"


def fila_tabla(*celdas, anchos):                           # [NUEVO]
    """Formatea una fila de tabla alineando columnas con anchos fijos."""
    partes = [str(c).ljust(w) for c, w in zip(celdas, anchos)]
    return "  " + " | ".join(partes)


def encabezado_tabla(columnas, anchos):                    # [NUEVO]
    """Imprime la fila de encabezado de tabla y su separador visual."""
    print(fila_tabla(*columnas, anchos=anchos))
    print("  " + "-+-".join("-" * w for w in anchos))


def mensaje_ok(texto):                                     # [NUEVO]
    """Mensaje de éxito con ícono visual."""
    print(f"\n  [+]  {texto}")


def mensaje_error(texto):                                  # [NUEVO]
    """Mensaje de error con ícono visual."""
    print(f"\n  [!]  {texto}")


def mensaje_info(texto):                                   # [NUEVO]
    """Mensaje informativo con ícono visual."""
    print(f"\n  [i]  {texto}")


def pausa():                                               # [NUEVO]
    """Detiene la ejecución hasta que el usuario presione ENTER."""
    input("\n  Presione ENTER para continuar...")


# =====================================================================
# 1. IMPORTACIÓN DE CLASES Y MÓDULOS DE POO (REORGANIZADO EN CARPETAS)
# =====================================================================
# Importamos las clases organizadas en carpetas profesionales en español.
# =====================================================================
from clases.persona import Persona
from clases.contacto import InformacionContacto # Herencia múltiple
from clases.paciente import Paciente             # Hereda de Persona e InformacionContacto
from clases.medico import Medico                 # Hereda de Persona (Herencia Simple)
from clases.cita import Cita                     # Composición de clases
from clases.factura import Factura               # Nueva clase de Facturación

# Importación de conceptos de Polimorfismo
from polimorfismo.sobreescritura import imprimir_resumen_entidad
from polimorfismo.sobrecarga import BuscadorClinico

# =====================================================================
# 2. ALMACENAMIENTO EN ARREGLOS (LISTAS EN MEMORIA)
# =====================================================================

pacientes = []   # Arreglo de objetos Paciente
medicos = []     # Arreglo de objetos Medico

# Conjuntos (set) para verificar DNIs duplicados en O(1).
dni_pacientes = set()                                      # Conjunto de DNIs de pacientes
dni_medicos   = set()                                      # Conjunto de DNIs de médicos

# Diccionario índice inverso: especialidad → lista de médicos.
indice_especialidad = {}                                   # Dict {especialidad: [Medico, ...]}


# =====================================================================
# 2B. CONFIGURACIONES DE AGENDAMIENTO
# =====================================================================

ESTADOS_CITA   = ("Pendiente", "Completada", "Cancelada")   # [TUPLAS] estados posibles de una cita
HORAS_ATENCION = (                                         # [TUPLAS] franjas horarias disponibles
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "12:00", "14:00", "14:30", "15:00",
    "15:30", "16:00", "16:30", "17:00",
)

citas = []             # [LISTAS] arreglo principal de objetos Cita
slots_ocupados = set() # [COLECCIONES] set de tuplas (dni_medico, fecha, hora) — evita doble reserva
facturas = []          # [LISTAS] arreglo principal de objetos Factura



# =====================================================================
# 3. FUNCIONES DE VALIDACIÓN (TRY/EXCEPT)
# =====================================================================

def leer_cadena(mensaje):
    """Lee texto y asegura que no esté vacío."""
    while True:
        entrada = input(f"  {mensaje}").strip()            # [NUEVO] indentación visual con f-string
        if entrada:
            return entrada
        mensaje_error("Este campo es obligatorio.")        # [NUEVO] usa función de diseño


def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero controlando errores con try/except."""
    while True:
        try:
            valor = int(input(f"  {mensaje}"))             # [NUEVO] indentación visual con f-string
            if minimo is not None and valor < minimo:
                mensaje_error(f"El valor mínimo es {minimo}.")  # [NUEVO]
                continue
            if maximo is not None and valor > maximo:
                mensaje_error(f"El valor máximo es {maximo}.")  # [NUEVO]
                continue
            return valor
        except ValueError:
            mensaje_error("Ingrese únicamente números enteros.")  # [NUEVO]


def leer_dni(mensaje):
    """Valida un DNI de exactamente 8 dígitos."""
    while True:
        dni = input(f"  {mensaje}").strip()                # [NUEVO] indentación visual con f-string
        if dni.isdigit() and len(dni) == 8:
            return dni
        mensaje_error("El DNI debe tener exactamente 8 dígitos.")  # [NUEVO]


# [NUEVO] ---------------------------------------------------------------
def elegir_de_tupla(mensaje, opciones):
    """
    Muestra una tupla de opciones numeradas y retorna la elegida.
    Usa enumerate() para iterar con índice automático.
    Ejemplo de uso: elegir_de_tupla("Seguro:", TIPOS_SEGURO)
    """
    print(f"\n  {mensaje}")
    for i, op in enumerate(opciones, start=1):             # enumerate() reemplaza contador manual
        print(f"    {i}. {op}")
    while True:
        idx = leer_entero(f"Elija (1-{len(opciones)}): ",
                          minimo=1, maximo=len(opciones))
        return opciones[idx - 1]
# -----------------------------------------------------------------------


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
# PERSISTENCIA EN JSON (db.json)
# =====================================================================
DB_PATH = "db.json"

def guardar_base_datos():
    """Guarda pacientes, médicos, citas y facturas en db.json."""
    datos = {
        "pacientes": [p.a_dict() for p in pacientes],
        "medicos": [m.a_dict() for m in medicos],
        "citas": [
            {
                "id": c.obtener_id(),
                "paciente_dni": c.obtener_paciente().obtener_dni(),
                "medico_dni": c.obtener_medico().obtener_dni(),
                "fecha": c.obtener_fecha(),
                "hora": c.obtener_hora(),
                "motivo": c.obtener_motivo(),
                "estado": c.obtener_estado()
            } for c in citas
        ],
        "facturas": [f.a_dict() for f in facturas]
    }
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"\n  [!] Error al guardar la base de datos: {e}")

def cargar_base_datos():
    """Carga pacientes, médicos, citas y facturas desde db.json si existe."""
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        # Cargar Pacientes
        for p_dict in datos.get("pacientes", []):
            p = Paciente(
                dni=p_dict["dni"],
                nombre=p_dict["nombre"],
                edad=p_dict["edad"],
                telefono=p_dict["telefono"],
                seguro=p_dict["seguro"]
            )
            pacientes.append(p)
            dni_pacientes.add(p.obtener_dni())
            
        # Cargar Médicos
        for m_dict in datos.get("medicos", []):
            m = Medico(
                dni=m_dict["dni"],
                nombre=m_dict["nombre"],
                especialidad=m_dict["especialidad"],
                consultorio=m_dict["consultorio"],
                precio_consulta=m_dict.get("precio_consulta", 0.0)
            )
            medicos.append(m)
            dni_medicos.add(m.obtener_dni())
            indice_especialidad.setdefault(m.obtener_especialidad(), []).append(m)
            
        # Cargar Citas
        from clases.cita import _contador_cita_global
        max_id = 0
        for c_dict in datos.get("citas", []):
            p = buscar_paciente(c_dict["paciente_dni"])
            m = buscar_medico(c_dict["medico_dni"])
            if p and m:
                c = Cita(
                    paciente=p,
                    medico=m,
                    fecha=c_dict["fecha"],
                    hora=c_dict["hora"],
                    motivo=c_dict["motivo"]
                )
                c._id = c_dict["id"]
                # Migración automática del estado "Atendida" a "Completada"
                estado = c_dict["estado"]
                if estado == "Atendida":
                    estado = "Completada"
                c.cambiar_estado(estado)
                citas.append(c)
                max_id = max(max_id, c._id)
                slots_ocupados.add((m.obtener_dni(), c.obtener_fecha(), c.obtener_hora()))
        
        _contador_cita_global[0] = max_id

        # Cargar Facturas
        for f_dict in datos.get("facturas", []):
            cita = next((c for c in citas if c.obtener_id() == f_dict["cita_id"]), None)
            if cita:
                f = Factura(
                    id=f_dict["id"],
                    cita=cita,
                    fecha_emision=f_dict["fecha_emision"],
                    tipo_comprobante=f_dict["tipo_comprobante"],
                    estado_pago=f_dict.get("estado_pago", "Completo"),
                    ruc=f_dict.get("ruc", ""),
                    razon_social=f_dict.get("razon_social", ""),
                    metodo_pago=f_dict.get("metodo_pago", "Efectivo")
                )
                f._monto_consulta = f_dict["monto_consulta"]
                f._descuento = f_dict["descuento"]
                f._total = f_dict["total"]
                facturas.append(f)
    except Exception as e:
        print(f"\n  [!] Error al cargar la base de datos: {e}")


# =====================================================================
# [NUEVO] MÓDULO DE ESTADÍSTICAS
# =====================================================================
# Funciones que operan sobre las colecciones para generar reportes.
# Demuestra: listas por comprensión, diccionarios contador,
#            set comprehension, sorted(), min(), max(), sum().
# =====================================================================

def estadisticas_pacientes():                              # [NUEVO]
    """
    Calcula y muestra estadísticas de los pacientes registrados.
    Estructuras usadas: lista por comprensión, diccionario, set.
    """
    print(titulo("ESTADÍSTICAS DE PACIENTES", "-"))

    if not pacientes:
        mensaje_info("No hay pacientes registrados aún.")
        return

    # Lista por comprensión: extraer solo las edades
    edades = [p.obtener_edad() for p in pacientes]
    promedio = sum(edades) / len(edades)

    print(f"\n  Total de pacientes : {len(pacientes)}")
    print(f"  Edad promedio      : {promedio:.1f} años")
    print(f"  Edad mínima        : {min(edades)} años")
    print(f"  Edad máxima        : {max(edades)} años")

    # Diccionario contador: cuántos pacientes hay por tipo de seguro
    conteo_seguro = {}
    for p in pacientes:
        seg = p.obtener_seguro()
        conteo_seguro[seg] = conteo_seguro.get(seg, 0) + 1

    print("\n  Distribucion por tipo de seguro:")
    for seg, cant in sorted(conteo_seguro.items()):
        barra = "=" * cant                                 # barra de texto proporcional
        print(f"    {seg:<15} {barra}  ({cant})")

    # Set comprehension: DNIs únicos (demostración de conjunto)
    todos_dnis = {p.obtener_dni() for p in pacientes}
    print(f"\n  DNIs unicos registrados: {len(todos_dnis)}")


def estadisticas_medicos():                                # [NUEVO]
    """
    Muestra estadísticas de médicos usando el diccionario índice inverso.
    """
    print(titulo("ESTADÍSTICAS DE MÉDICOS", "-"))

    if not medicos:
        mensaje_info("No hay médicos registrados aún.")
        return

    print(f"\n  Total de médicos registrados: {len(medicos)}")

    if indice_especialidad:
        print("\n  Médicos por especialidad:")
        for esp in sorted(indice_especialidad.keys()):
            cantidad = len(indice_especialidad[esp])
            print(f"    {esp:<22}: {cantidad} medico(s)")


# =====================================================================
# 4. FUNCIONES DE REGISTRO (ÚNICO MÓDULO FUNCIONAL EN ESTE AVANCE)
# =====================================================================

def registrar_paciente():
    print(subtitulo("REGISTRAR PACIENTE"))                 # [NUEVO] usa función de diseño

    dni = leer_dni("DNI del paciente      : ")
    if dni in dni_pacientes:                               # [NUEVO] búsqueda O(1) con set
        mensaje_error("Ese paciente ya está registrado.")  # [NUEVO]
        return
    nombre = leer_cadena("Nombre completo       : ")
    edad = leer_entero("Edad                  : ", minimo=0, maximo=120)
    telefono = leer_cadena("Teléfono              : ")
    seguro = elegir_de_tupla("Tipo de seguro:", TIPOS_SEGURO)  # [NUEVO] elige de tupla

    nuevo = Paciente(dni, nombre, edad, telefono, seguro)
    pacientes.append(nuevo)
    dni_pacientes.add(dni)                                 # [NUEVO] actualizar conjunto

    guardar_base_datos()                                   # Persistencia JSON
    mensaje_ok(f"Paciente '{nombre}' registrado con éxito.")  # [NUEVO]


def registrar_medico():
    print(subtitulo("REGISTRAR MÉDICO"))                   # [NUEVO] usa función de diseño

    dni = leer_dni("DNI del médico        : ")
    if dni in dni_medicos:                                 # [NUEVO] búsqueda O(1) con set
        mensaje_error("Ese médico ya está registrado.")    # [NUEVO]
        return
    nombre = leer_cadena("Nombre completo       : ")
    especialidad = elegir_de_tupla("Especialidad:", ESPECIALIDADES_VALIDAS)  # [NUEVO]
    consultorio = leer_entero("N° de consultorio     : ", minimo=1, maximo=99)  # [NUEVO]
    
    # Precios base sugeridos por especialidad para wow factor
    precios_sugeridos = {
        "Cardiología": 150, "Dermatología": 120, "Neurología": 180, "Pediatría": 90,
        "Traumatología": 130, "Oftalmología": 110, "Ginecología": 140, "Oncología": 200,
        "Psiquiatría": 160, "Medicina General": 70
    }
    precio_sug = precios_sugeridos.get(especialidad, 80)
    print(f"  [i] Precio de consulta sugerido para {especialidad}: S/. {precio_sug}")
    precio_consulta = leer_entero("Precio de consulta (mín. S/. 10): ", minimo=10)

    nuevo = Medico(dni, nombre, especialidad, consultorio, precio_consulta)
    medicos.append(nuevo)
    dni_medicos.add(dni)                                   # [NUEVO] actualizar conjunto
    indice_especialidad.setdefault(especialidad, []).append(nuevo)  # [NUEVO] actualizar dict

    guardar_base_datos()                                   # Persistencia JSON
    mensaje_ok(f"Médico '{nombre}' ({especialidad}) registrado con éxito.")  # [NUEVO]


def mostrar_pacientes():
    print(titulo("LISTA DE PACIENTES"))                    # [NUEVO] usa función de diseño

    if not pacientes:
        mensaje_info("No hay pacientes registrados.")      # [NUEVO]
        return

    # [NUEVO] tabla con anchos de columna fijos ---------------------------
    anchos = [10, 24, 5, 13, 12]
    encabezado_tabla(["DNI", "Nombre", "Edad", "Telefono", "Seguro"], anchos)
    for p in pacientes:
        print(fila_tabla(
            p.obtener_dni(), p.obtener_nombre(),
            p.obtener_edad(), p.obtener_telefono(),
            p.obtener_seguro(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(pacientes)} paciente(s).")
    # ---------------------------------------------------------------------


def mostrar_medicos():
    print(titulo("LISTA DE MÉDICOS"))                      # [NUEVO] usa función de diseño

    if not medicos:
        mensaje_info("No hay médicos registrados.")        # [NUEVO]
        return

    # [NUEVO] tabla con anchos de columna fijos ---------------------------
    anchos = [10, 20, 16, 6, 8]
    encabezado_tabla(["DNI", "Nombre", "Especialidad", "Cons.", "Precio"], anchos)
    for m in medicos:
        print(fila_tabla(
            m.obtener_dni(), m.obtener_nombre(),
            m.obtener_especialidad(), m.obtener_consultorio(),
            f"S/. {m.obtener_precio_consulta():.0f}",
            anchos=anchos
        ))
    print(f"\n  Total: {len(medicos)} médico(s).")
    # ---------------------------------------------------------------------


# [NUEVO] ---------------------------------------------------------------
def buscar_pacientes_por_seguro():
    """
    Filtra la lista de pacientes por tipo de seguro.
    Usa filter() con lambda sobre la lista de pacientes.
    """
    print(subtitulo("BUSCAR PACIENTES POR SEGURO"))
    seguro = elegir_de_tupla("Seleccione el tipo de seguro:", TIPOS_SEGURO)

    # filter() retorna un iterador; se convierte a lista para operar sobre él
    resultado = list(filter(lambda p: p.obtener_seguro() == seguro, pacientes))

    if not resultado:
        mensaje_info(f"No hay pacientes con seguro '{seguro}'.")
        return

    print(f"\n  Pacientes con seguro '{seguro}':")
    anchos = [10, 24, 5, 13]
    encabezado_tabla(["DNI", "Nombre", "Edad", "Telefono"], anchos)
    for p in resultado:
        print(fila_tabla(
            p.obtener_dni(), p.obtener_nombre(),
            p.obtener_edad(), p.obtener_telefono(),
            anchos=anchos
        ))
    print(f"\n  Encontrado(s): {len(resultado)} paciente(s).")


def buscar_medicos_por_especialidad():
    """
    Consulta el diccionario índice inverso para listar médicos
    de una especialidad sin recorrer toda la lista.
    """
    print(subtitulo("BUSCAR MÉDICOS POR ESPECIALIDAD"))
    especialidad = elegir_de_tupla("Seleccione la especialidad:", ESPECIALIDADES_VALIDAS)

    # dict.get() con valor por defecto evita KeyError si no existe la clave
    resultado = indice_especialidad.get(especialidad, [])

    if not resultado:
        mensaje_info(f"No hay médicos de '{especialidad}'.")
        return

    print(f"\n  Médicos de '{especialidad}':")
    anchos = [10, 24, 6]
    encabezado_tabla(["DNI", "Nombre", "Cons."], anchos)
    for m in resultado:
        print(fila_tabla(
            m.obtener_dni(), m.obtener_nombre(),
            m.obtener_consultorio(),
            anchos=anchos
        ))
    print(f"\n  Encontrado(s): {len(resultado)} médico(s).")


def buscar_poo_sobrecarga():
    """
    [POO] Función interactiva para demostrar Polimorfismo.
    Utiliza BuscadorClinico (Sobrecarga simulada) y llama a imprimir_resumen_entidad
    (Polimorfismo por Sobreescritura) para cada resultado encontrado.
    """
    print(subtitulo("BÚSQUEDA POO (SOBRECARGA Y SOBREESCRITURA)"))
    print("  1. Buscar en Colección de Pacientes")
    print("  2. Buscar en Colección de Médicos")
    op_tipo = leer_entero("Seleccione tipo de búsqueda (1-2): ", minimo=1, maximo=2)
    coleccion = pacientes if op_tipo == 1 else medicos
    
    print("\n  Filtros disponibles (Sobrecarga de Métodos):")
    print("    1. Buscar solo por DNI")
    print("    2. Buscar solo por Nombre")
    print("    3. Buscar por DNI y por Nombre simultáneamente")
    print("    4. No aplicar filtros (Mostrar todo)")
    op_filtro = leer_entero("Elija una opción (1-4): ", minimo=1, maximo=4)
    
    buscador = BuscadorClinico()
    resultado = []
    
    # Dependiendo de la opción del usuario, se llama al mismo método buscar con diferentes firmas (Sobrecarga)
    if op_filtro == 1:
        dni = leer_dni("Ingrese DNI a buscar: ")
        resultado = buscador.buscar(coleccion, dni=dni) # Firma 1: (coleccion, dni)
    elif op_filtro == 2:
        nombre = leer_cadena("Ingrese Nombre a buscar: ")
        resultado = buscador.buscar(coleccion, nombre=nombre) # Firma 2: (coleccion, nombre)
    elif op_filtro == 3:
        dni = leer_dni("Ingrese DNI a buscar: ")
        nombre = leer_cadena("Ingrese Nombre a buscar: ")
        resultado = buscador.buscar(coleccion, dni=dni, nombre=nombre) # Firma 3: (coleccion, dni, nombre)
    else:
        resultado = buscador.buscar(coleccion) # Firma 4: (coleccion)
        
    if not resultado:
        mensaje_info("No se encontraron registros con los criterios especificados.")
        return
        
    print(titulo("RESULTADOS (POLIMORFISMO DE SOBREESCRITURA)"))
    for elem in resultado:
        # Llama a la función polimórfica que invoca el obtener_resumen() de cada clase
        imprimir_resumen_entidad(elem)
    print(linea("-"))


def resumen_general():
    """
    Panel de resumen rápido mostrado al inicio del menú principal.
    Usa datetime para la fecha/hora y f-strings con alineación.
    """
    ahora = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")
    print(titulo("RESUMEN DEL SISTEMA"))
    print(f"  {'Fecha y hora':<25}: {ahora}")
    print(f"  {'Pacientes registrados':<25}: {len(pacientes)}")
    print(f"  {'Medicos registrados':<25}: {len(medicos)}")
    print(f"  {'Especialidades activas':<25}: {len(indice_especialidad)}")
    print(f"  {'Citas agendadas':<25}: {len(citas)}")          # [NUEVO]
    pendientes = len([c for c in citas                         # [NUEVO] lista por comprensión
                      if c.obtener_estado() == "Pendiente"])
    print(f"  {'Citas pendientes':<25}: {pendientes}")         # [NUEVO]
# -----------------------------------------------------------------------


# =====================================================================
# 4B. MÓDULO DE AGENDAMIENTO
# =====================================================================
# Requisitos demostrados en este módulo:
#   [LISTAS]        — lista 'citas', listas por comprensión
#   [TUPLAS]        — ESTADOS_CITA, HORAS_ATENCION como catálogos
#   [COLECCIONES]   — set slots_ocupados, diccionarios contadores
#   [ENTRADA/SALIDA]— leer_fecha(), menú con opciones numeradas
#   [DISEÑO CONSOLA]— subtitulo(), encabezado_tabla(), fila_tabla()
# =====================================================================

def leer_fecha(mensaje):
    """
    Lee y valida una fecha en formato DD/MM/AAAA usando try/except.
    Comprueba que la fecha no sea anterior al día de hoy.
    """
    while True:
        texto = input(f"  {mensaje}").strip()              # [ENTRADA/SALIDA] lectura de fecha
        try:
            fecha = datetime.datetime.strptime(texto, "%d/%m/%Y")
            hoy   = datetime.datetime.now().replace(hour=0, minute=0,
                                                    second=0, microsecond=0)
            if fecha < hoy:
                mensaje_error("La fecha no puede ser anterior a hoy.")
                continue
            return texto
        except ValueError:                                 # [ENTRADA/SALIDA] control de error de formato
            mensaje_error("Formato incorrecto. Use DD/MM/AAAA (ej: 25/07/2025).")


def agendar_cita():
    """
    Registra una nueva cita médica.
    Pasos: elegir paciente → elegir médico → elegir fecha →
           elegir hora (tupla) → ingresar motivo → guardar.
    """
    print(subtitulo("AGENDAR NUEVA CITA"))                 # [DISEÑO CONSOLA] encabezado de sección

    # ── 1. Seleccionar paciente por DNI ──────────────────────────────
    if not pacientes:
        mensaje_error("No hay pacientes registrados. Vaya al módulo de REGISTRO.")
        return
    dni_p    = leer_dni("DNI del paciente      : ")        # [ENTRADA/SALIDA] lectura de DNI
    paciente = buscar_paciente(dni_p)
    if not paciente:
        mensaje_error("Paciente no encontrado. Regístrelo primero.")
        return

    # ── 2. Seleccionar médico por DNI ────────────────────────────────
    if not medicos:
        mensaje_error("No hay médicos registrados. Vaya al módulo de REGISTRO.")
        return
    dni_m  = leer_dni("DNI del médico        : ")          # [ENTRADA/SALIDA] lectura de DNI
    medico = buscar_medico(dni_m)
    if not medico:
        mensaje_error("Médico no encontrado. Regístrelo primero.")
        return

    # ── 3. Fecha y hora ──────────────────────────────────────────────
    fecha = leer_fecha("Fecha de la cita (DD/MM/AAAA): ")  # [ENTRADA/SALIDA] lectura validada
    hora  = elegir_de_tupla("Hora de atención:", HORAS_ATENCION)  # [TUPLAS] elige de la tupla

    # Verificar conflicto: mismo médico + fecha + hora ya reservados
    slot = (medico.obtener_dni(), fecha, hora)             # [TUPLAS] tupla como clave del set
    if slot in slots_ocupados:                             # [COLECCIONES] búsqueda O(1) en set
        mensaje_error(
            f"El Dr. {medico.obtener_nombre()} ya tiene cita "
            f"el {fecha} a las {hora}. Elija otra hora o fecha."
        )
        return

    # ── 4. Motivo ────────────────────────────────────────────────────
    motivo = leer_cadena("Motivo de consulta    : ")       # [ENTRADA/SALIDA] lectura de texto

    # ── 5. Guardar ───────────────────────────────────────────────────
    nueva = Cita(paciente, medico, fecha, hora, motivo)
    citas.append(nueva)                                    # [LISTAS] agregar objeto a la lista
    slots_ocupados.add(slot)                               # [COLECCIONES] registrar slot en set

    guardar_base_datos()                                   # Persistencia JSON
    mensaje_ok(                                            # [DISEÑO CONSOLA] confirmación visual
        f"Cita #{nueva.obtener_id()} agendada: "
        f"{paciente.obtener_nombre()} con Dr. {medico.obtener_nombre()} "
        f"el {fecha} a las {hora}."
    )


def listar_citas():
    """Muestra todas las citas registradas en tabla formateada."""
    print(titulo("LISTADO DE CITAS MÉDICAS"))              # [DISEÑO CONSOLA] título de pantalla

    if not citas:                                          # [LISTAS] verificar si la lista está vacía
        mensaje_info("No hay citas registradas.")
        return

    anchos = [4, 18, 18, 11, 6, 10]
    encabezado_tabla(                                      # [DISEÑO CONSOLA] encabezado de tabla
        ["ID", "Paciente", "Medico", "Fecha", "Hora", "Estado"],
        anchos
    )
    for c in citas:                                        # [LISTAS] recorrer la lista de citas
        print(fila_tabla(                                  # [DISEÑO CONSOLA] fila alineada
            f"#{c.obtener_id()}",
            c.obtener_paciente().obtener_nombre(),
            c.obtener_medico().obtener_nombre(),
            c.obtener_fecha(),
            c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(citas)} cita(s).")             # [DISEÑO CONSOLA] pie de tabla


def cambiar_estado_cita():
    """
    Busca una cita por ID y permite cambiar su estado.
    Estados válidos definidos en la tupla ESTADOS_CITA.
    """
    print(subtitulo("CAMBIAR ESTADO DE CITA"))             # [DISEÑO CONSOLA] encabezado de sección

    if not citas:                                          # [LISTAS] verificar lista vacía
        mensaje_info("No hay citas registradas.")
        return

    # Diccionario temporal id → cita construido por comprensión
    mapa_citas = {c.obtener_id(): c for c in citas}       # [COLECCIONES] dict por comprensión

    try:
        id_buscado = int(input("  ID de la cita        : "))  # [ENTRADA/SALIDA] lectura de ID
    except ValueError:                                     # [ENTRADA/SALIDA] control de error
        mensaje_error("Ingrese un número de ID válido.")
        return

    if id_buscado not in mapa_citas:                       # [COLECCIONES] búsqueda en diccionario
        mensaje_error(f"No existe la cita con ID #{id_buscado}.")
        return

    cita = mapa_citas[id_buscado]

    # Mostrar datos actuales de la cita
    print(f"\n  Paciente : {cita.obtener_paciente().obtener_nombre()}")   # [DISEÑO CONSOLA]
    print(f"  Medico   : {cita.obtener_medico().obtener_nombre()}")       # [DISEÑO CONSOLA]
    print(f"  Fecha    : {cita.obtener_fecha()}  {cita.obtener_hora()}")  # [DISEÑO CONSOLA]
    print(f"  Estado   : {cita.obtener_estado()}")                        # [DISEÑO CONSOLA]

    nuevo_estado = elegir_de_tupla("Nuevo estado:", ESTADOS_CITA)  # [TUPLAS] opciones de la tupla
    cita.cambiar_estado(nuevo_estado)
    guardar_base_datos()                                   # Persistencia JSON
    mensaje_ok(f"Cita #{id_buscado} actualizada a estado '{nuevo_estado}'.")  # [DISEÑO CONSOLA]


def buscar_citas_por_paciente():
    """
    Filtra la lista de citas por DNI de paciente.
    Usa filter() + lambda sobre la lista de citas.
    """
    print(subtitulo("BUSCAR CITAS POR PACIENTE"))          # [DISEÑO CONSOLA] encabezado

    dni      = leer_dni("DNI del paciente      : ")        # [ENTRADA/SALIDA] lectura de DNI
    paciente = buscar_paciente(dni)
    if not paciente:
        mensaje_error("Paciente no encontrado.")
        return

    # filter() + lambda recorre la lista y selecciona coincidencias
    resultado = list(                                      # [LISTAS] resultado como lista
        filter(lambda c: c.obtener_paciente().obtener_dni() == dni, citas)
    )                                                      # [COLECCIONES] filter() sobre la lista

    if not resultado:
        mensaje_info(f"No hay citas para '{paciente.obtener_nombre()}'.")
        return

    print(f"\n  Citas de '{paciente.obtener_nombre()}':")
    anchos = [4, 18, 11, 6, 10]
    encabezado_tabla(["ID", "Medico", "Fecha", "Hora", "Estado"], anchos)  # [DISEÑO CONSOLA]
    for c in resultado:                                    # [LISTAS] recorrer lista filtrada
        print(fila_tabla(                                  # [DISEÑO CONSOLA] fila alineada
            f"#{c.obtener_id()}",
            c.obtener_medico().obtener_nombre(),
            c.obtener_fecha(), c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(resultado)} cita(s).")         # [DISEÑO CONSOLA] pie de tabla


def buscar_citas_por_medico():
    """
    Filtra la lista de citas por DNI de médico.
    Usa filter() + lambda sobre la lista de citas.
    """
    print(subtitulo("BUSCAR CITAS POR MÉDICO"))            # [DISEÑO CONSOLA] encabezado

    dni    = leer_dni("DNI del médico        : ")          # [ENTRADA/SALIDA] lectura de DNI
    medico = buscar_medico(dni)
    if not medico:
        mensaje_error("Médico no encontrado.")
        return

    resultado = list(                                      # [LISTAS] resultado como lista
        filter(lambda c: c.obtener_medico().obtener_dni() == dni, citas)
    )                                                      # [COLECCIONES] filter() sobre la lista

    if not resultado:
        mensaje_info(f"No hay citas para 'Dr. {medico.obtener_nombre()}'.")
        return

    print(f"\n  Citas del Dr. '{medico.obtener_nombre()}':")
    anchos = [4, 22, 11, 6, 10]
    encabezado_tabla(["ID", "Paciente", "Fecha", "Hora", "Estado"], anchos)  # [DISEÑO CONSOLA]
    for c in resultado:                                    # [LISTAS] recorrer lista filtrada
        print(fila_tabla(                                  # [DISEÑO CONSOLA] fila alineada
            f"#{c.obtener_id()}",
            c.obtener_paciente().obtener_nombre(),
            c.obtener_fecha(), c.obtener_hora(),
            c.obtener_estado(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(resultado)} cita(s).")         # [DISEÑO CONSOLA] pie de tabla


def resumen_agendamiento():
    """
    Estadísticas del módulo de agendamiento.
    Usa: lista por comprensión, diccionario contador, tupla de estados.
    """
    print(titulo("RESUMEN DE AGENDAMIENTO", "-"))          # [DISEÑO CONSOLA] título de pantalla

    if not citas:                                          # [LISTAS] verificar lista vacía
        mensaje_info("No hay citas registradas aún.")
        return

    # Diccionario contador: cuántas citas hay por cada estado
    conteo_estado = {}                                     # [COLECCIONES] diccionario contador
    for c in citas:                                        # [LISTAS] recorrer la lista
        est = c.obtener_estado()
        conteo_estado[est] = conteo_estado.get(est, 0) + 1

    print(f"\n  Total de citas registradas : {len(citas)}")  # [DISEÑO CONSOLA]
    print("\n  Citas por estado:")
    for est in ESTADOS_CITA:                               # [TUPLAS] itera en orden de la tupla
        cant  = conteo_estado.get(est, 0)                  # [COLECCIONES] consulta al diccionario
        barra = "=" * cant                                 # [DISEÑO CONSOLA] barra proporcional
        print(f"    {est:<12} {barra}  ({cant})")          # [DISEÑO CONSOLA] salida alineada

    # Lista por comprensión: filtrar solo citas pendientes
    pendientes = [c for c in citas                         # [LISTAS] lista por comprensión
                  if c.obtener_estado() == "Pendiente"]
    print(f"\n  Citas pendientes           : {len(pendientes)}")  # [DISEÑO CONSOLA]

    # Médico con más citas usando diccionario contador
    conteo_medico = {}                                     # [COLECCIONES] diccionario contador
    for c in citas:                                        # [LISTAS] recorrer lista
        nom = c.obtener_medico().obtener_nombre()
        conteo_medico[nom] = conteo_medico.get(nom, 0) + 1
    mas_citas = max(conteo_medico, key=conteo_medico.get)  # [COLECCIONES] máximo del dict
    print(f"  Medico con mas citas       : {mas_citas} ({conteo_medico[mas_citas]})")  # [DISEÑO CONSOLA]


def menu_agendamiento():
    """PASO 2: AGENDAMIENTO — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 2 ]  AGENDAMIENTO"))          # [DISEÑO CONSOLA] título de pantalla

        opciones_menu = [                                  # [LISTAS] lista de opciones del menú
            "Agendar Nueva Cita",
            "Listar Todas las Citas",
            "Buscar Citas por Paciente",
            "Buscar Citas por Médico",
            "Cambiar Estado de Cita",
            "Resumen de Agendamiento",
            "Volver al Menú Principal",
        ]
        for i, op in enumerate(opciones_menu, start=1):   # [LISTAS] recorrer con enumerate
            num = "0" if op == "Volver al Menú Principal" else str(i)
            print(f"  {num}. {op}")                        # [DISEÑO CONSOLA] opción numerada
        print(linea("-"))                                  # [DISEÑO CONSOLA] separador

        op = leer_entero(                                  # [ENTRADA/SALIDA] lectura de opción
            f"Opción (0-{len(opciones_menu)-1}): ",
            minimo=0, maximo=len(opciones_menu) - 1
        )

        acciones = {                                       # [COLECCIONES] diccionario de funciones
            1: agendar_cita,
            2: listar_citas,
            3: buscar_citas_por_paciente,
            4: buscar_citas_por_medico,
            5: cambiar_estado_cita,
            6: resumen_agendamiento,
        }

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()                                 # [COLECCIONES] despacho por diccionario
            pausa()                                        # [DISEÑO CONSOLA] pausa entre pantallas


def imprimir_boleta_ascii(factura):
    cita = factura.obtener_cita()
    paciente = cita.obtener_paciente()
    medico = cita.obtener_medico()
    
    parts = factura.obtener_fecha_emision().split()
    fecha_em = parts[0] if len(parts) > 0 else factura.obtener_fecha_emision()
    hora_em = " ".join(parts[1:]) if len(parts) > 1 else "10:00 AM"
    
    tipo = factura.obtener_tipo_comprobante()
    prefix = "F001" if tipo == "Factura" else "B001"
    n_comprobante = f"{prefix}-{factura.obtener_id():06d}"
    
    print("\n============================================================")
    print("                     MEDIC-UTP")
    print("          SISTEMA DE CITAS MÉDICAS Y FACTURACIÓN")
    print("============================================================")
    print(f"\n                 {tipo.upper()} ELECTRÓNICA")
    print("------------------------------------------------------------")
    print(f"N° {tipo}        : {n_comprobante}")
    print(f"Fecha Emisión    : {fecha_em}")
    print(f"Hora Emisión     : {hora_em}")
    
    if tipo == "Factura":
        print(f"\nAdquirente       : {factura.obtener_razon_social()}")
        print(f"RUC              : {factura.obtener_ruc()}")
        print(f"\nPaciente         : {paciente.obtener_nombre()}")
        print(f"DNI              : {paciente.obtener_dni()}")
    else:
        print(f"\nPaciente         : {paciente.obtener_nombre()}")
        print(f"DNI              : {paciente.obtener_dni()}")
        
    print(f"Seguro           : {paciente.obtener_seguro()}")
    print(f"\nMédico           : Dr(a). {medico.obtener_nombre()}")
    print(f"Especialidad     : {medico.obtener_especialidad()}")
    print(f"Consultorio      : {medico.obtener_consultorio():02d}")
    print("\n------------------------------------------------------------")
    print("DETALLE DE LA ATENCIÓN")
    print("------------------------------------------------------------")
    print(f"Fecha de la cita : {cita.obtener_fecha()}")
    print(f"Hora de la cita  : {cita.obtener_hora()}")
    print(f"Motivo           : {cita.obtener_motivo()}")
    print(f"\nPrecio Consulta  : S/. {factura.obtener_monto_consulta():.2f}")
    print(f"Descuento Seguro : S/. {factura.obtener_descuento():.2f}")
    print("-----------------------------------------")
    print(f"TOTAL A PAGAR    : S/. {factura.obtener_total():.2f}")
    print("-----------------------------------------")
    print(f"\nEstado de Pago   : {factura.obtener_estado_pago()}")
    print(f"Método de Pago   : {factura.obtener_metodo_pago()}")
    print("\n============================================================")
    print("        Gracias por confiar en MEDIC-UTP")
    print("     Conserve este comprobante de atención")
    print("============================================================\n")


def generar_factura():
    """Registra y genera una nueva boleta o factura para una cita completada."""
    print(subtitulo("GENERAR COMPROBANTE"))

    if not citas:
        mensaje_error("No hay citas registradas en el sistema.")
        return

    # Buscar la cita
    try:
        id_cita = int(input("  Ingrese el ID de la Cita    : "))
    except ValueError:
        mensaje_error("El ID de la cita debe ser un número entero.")
        return

    # Encontrar la cita
    cita = next((c for c in citas if c.obtener_id() == id_cita), None)
    if not cita:
        mensaje_error(f"No se encontró la cita con ID #{id_cita}.")
        return

    # Validar estado de la cita: sólo "Completada"
    if cita.obtener_estado() != "Completada":
        mensaje_error(
            f"No se puede facturar. La cita está '{cita.obtener_estado()}'.\n"
            f"  Sólo se permiten facturas para citas con estado 'Completada'."
        )
        return

    # Validar que no exista factura/boleta previa para esa cita
    factura_previa = next((f for f in facturas if f.obtener_cita_id() == id_cita), None)
    if factura_previa:
        mensaje_error(
            f"Conflicto: Ya existe un comprobante (ID #{factura_previa.obtener_id()}) "
            f"generado para la cita #{id_cita}."
        )
        return

    # Elegir tipo de comprobante
    tipo_comprobante = elegir_de_tupla("Tipo de comprobante:", ("Boleta", "Factura"))

    ruc = ""
    razon_social = ""

    # Si es Factura, generar RUC 10 automáticamente usando el DNI del paciente (Leyes SUNAT para personas naturales con negocio)
    if tipo_comprobante == "Factura":
        dni_paciente = cita.obtener_paciente().obtener_dni()
        ruc_base = "10" + dni_paciente
        # Algoritmo oficial SUNAT para módulo 11
        multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = sum(int(ruc_base[i]) * multiplicadores[i] for i in range(10))
        resto = suma % 11
        verificador = 11 - resto
        if verificador == 11:
            verificador = 0
        elif verificador == 10:
            verificador = 1
        ruc = ruc_base + str(verificador)
        
        print(f"  [i] RUC 10 Generado automáticamente: {ruc}")
        razon_social = leer_cadena("Razón Social (Empresa)      : ")

    # Elegir método de pago
    metodo_pago = elegir_de_tupla("Método de pago:", ("Efectivo", "Yape"))

    # Autoincrementar ID
    max_id = max([f.obtener_id() for f in facturas], default=0)
    nuevo_id = max_id + 1

    # Fecha de emisión actual (formato: DD/MM/AAAA hh:mm AM/PM)
    fecha_emision = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")

    # Crear comprobante
    nuevo_comprobante = Factura(
        id=nuevo_id,
        cita=cita,
        fecha_emision=fecha_emision,
        tipo_comprobante=tipo_comprobante,
        estado_pago="Completo",
        ruc=ruc,
        razon_social=razon_social,
        metodo_pago=metodo_pago
    )
    facturas.append(nuevo_comprobante)

    guardar_base_datos()
    mensaje_ok(f"{tipo_comprobante} #{nuevo_id} generada con éxito para la Cita #{id_cita}.")

    # Imprimir boleta/factura en formato ASCII
    imprimir_boleta_ascii(nuevo_comprobante)


def listar_facturas():
    """Muestra todas las facturas/boletas en una tabla formateada."""
    print(titulo("LISTADO DE COMPROBANTES"))

    if not facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    anchos = [4, 8, 8, 22, 10, 10]
    encabezado_tabla(["ID", "Cita ID", "Tipo", "Paciente/Cliente", "Total", "Estado"], anchos)
    for f in facturas:
        cliente = f.obtener_razon_social() if f.obtener_tipo_comprobante() == "Factura" else f.obtener_cita().obtener_paciente().obtener_nombre()
        print(fila_tabla(
            f"#{f.obtener_id()}",
            f"#{f.obtener_cita_id()}",
            f.obtener_tipo_comprobante(),
            cliente,
            f"S/. {f.obtener_total():.2f}",
            f.obtener_estado_pago(),
            anchos=anchos
        ))
    print(f"\n  Total: {len(facturas)} comprobante(s).")


def buscar_factura_por_id():
    """Busca una factura/boleta por ID y muestra su resumen usando polimorfismo."""
    print(subtitulo("BUSCAR COMPROBANTE POR ID"))

    if not facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    try:
        id_buscado = int(input("  Ingrese ID del Comprobante  : "))
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return

    factura = next((f for f in facturas if f.obtener_id() == id_buscado), None)
    if not factura:
        mensaje_error(f"No existe el comprobante con ID #{id_buscado}.")
        return

    print("\n  Resumen obtenido mediante polimorfismo:")
    imprimir_resumen_entidad(factura)


def mostrar_detalle_factura():
    """Muestra todos los detalles de cobro de un comprobante específico en formato ASCII."""
    print(subtitulo("DETALLE DE COMPROBANTE"))

    if not facturas:
        mensaje_info("No hay comprobantes registrados.")
        return

    try:
        id_buscado = int(input("  Ingrese ID del Comprobante  : "))
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return

    factura = next((f for f in facturas if f.obtener_id() == id_buscado), None)
    if not factura:
        mensaje_error(f"No existe el comprobante con ID #{id_buscado}.")
        return

    imprimir_boleta_ascii(factura)


def menu_facturacion():
    """PASO 3: FACTURACIÓN — submenú con opciones numeradas."""
    while True:
        print(titulo("[ PASO 3 ]  FACTURACIÓN"))

        opciones_menu = [
            "Generar Factura",
            "Listar Facturas",
            "Buscar Factura por ID",
            "Mostrar Detalle de Factura",
            "Volver al Menú Principal",
        ]
        for i, op in enumerate(opciones_menu, start=1):
            num = "0" if op == "Volver al Menú Principal" else str(i)
            print(f"  {num}. {op}")
        print(linea("-"))

        op = leer_entero(
            f"Opción (0-{len(opciones_menu)-1}): ",
            minimo=0, maximo=len(opciones_menu) - 1
        )

        acciones = {
            1: generar_factura,
            2: listar_facturas,
            3: buscar_factura_por_id,
            4: mostrar_detalle_factura,
        }

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()
            pausa()


# =====================================================================
# 5. SUBMENÚS DEL FLUJO
# =====================================================================

def menu_registro():
    """PASO 1: REGISTRO (módulo funcional en este avance)."""
    while True:
        print(titulo("[ PASO 1 ]  REGISTRO"))             # [NUEVO] usa función de diseño

        # [NUEVO] lista de opciones del menú ----------------------------------
        opciones_menu = [
            "Registrar Paciente",
            "Registrar Médico",
            "Mostrar Pacientes",
            "Mostrar Médicos",
            "Buscar Pacientes por Seguro",
            "Buscar Médicos por Especialidad",
            "Estadísticas de Pacientes",
            "Estadísticas de Médicos",
            "Búsqueda POO (Sobrecarga/Polimorfismo)",
            "Volver al Menú Principal",
        ]
        for i, op in enumerate(opciones_menu, start=1):
            num = "0" if op == "Volver al Menú Principal" else str(i)
            print(f"  {num}. {op}")
        print(linea("-"))
        # ---------------------------------------------------------------------

        op = leer_entero(f"Opción (0-{len(opciones_menu)-1}): ",
                         minimo=0, maximo=len(opciones_menu) - 1)

        # [NUEVO] diccionario de acciones: despacha funciones por clave -------
        acciones = {
            1: registrar_paciente,
            2: registrar_medico,
            3: mostrar_pacientes,
            4: mostrar_medicos,
            5: buscar_pacientes_por_seguro,
            6: buscar_medicos_por_especialidad,
            7: estadisticas_pacientes,
            8: estadisticas_medicos,
            9: buscar_poo_sobrecarga,
        }
        # ---------------------------------------------------------------------

        if op == 0:
            return
        elif op in acciones:
            acciones[op]()
            pausa()


def menu_en_construccion(nombre):
    """PASO 2 y 3: aún no implementados en este avance."""
    mensaje_info(f"El módulo '{nombre}' estará disponible en el próximo avance.")  # [NUEVO]
    pausa()                                                # [NUEVO]


# =====================================================================
# 6. MENÚ PRINCIPAL
# =====================================================================

def main():
    cargar_base_datos()                                    # Carga persistencia JSON
    # [NUEVO] pantalla de bienvenida con VERSION_SISTEMA (tupla) ----------
    print(titulo(f"  {VERSION_SISTEMA[0]}  v{VERSION_SISTEMA[1]}"))
    print(f"{'Sistema de Citas Medicas y Facturacion'.center(ANCHO_CONSOLA)}")
    print(linea())
    pausa()
    # -----------------------------------------------------------------------

    while True:
        resumen_general()                                  # [NUEVO] resumen antes del menú

        print(titulo("MENÚ PRINCIPAL"))                    # [NUEVO] usa función de diseño
        print("  REGISTRO -> AGENDAMIENTO -> FACTURACIÓN")
        print(linea("-"))                                  # [NUEVO]
        print("  1. PASO 1 -> REGISTRO          (disponible)")
        print("  2. PASO 2 -> AGENDAMIENTO      (disponible)")   # [NUEVO]
        print("  3. PASO 3 -> FACTURACIÓN       (disponible)")
        print("  0. Salir del Sistema")
        print(linea())                                     # [NUEVO]

        op = leer_entero("Opción (0-3): ", minimo=0, maximo=3)

        if op == 1:
            menu_registro()
        elif op == 2:
            menu_agendamiento()                                # [NUEVO] módulo ya funcional
        elif op == 3:
            menu_facturacion()
        elif op == 0:
            # [NUEVO] pantalla de despedida --------------------------------
            print(titulo("¡HASTA PRONTO!"))
            print(f"{'Gracias por utilizar MEDIC-UTP'.center(ANCHO_CONSOLA)}")
            print(linea())
            # ---------------------------------------------------------------
            sys.exit(0)


if __name__ == "__main__":
    main()

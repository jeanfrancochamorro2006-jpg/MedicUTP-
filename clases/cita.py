# -*- coding: utf-8 -*-
"""
Clase Cita - Entidad del módulo de agendamiento.
Asocia un Paciente y un Medico en una fecha y hora determinada.
"""

ESTADOS_CITA_BASE = ("Pendiente", "Completada", "Cancelada")

_contador_cita_global = [0]

class Cita:
    """
    Representa una cita médica entre un Paciente y un Médico.
    Demuestra composición de clases (relación entre múltiples objetos de clase).
    """
    def __init__(self, paciente, medico, fecha, hora, motivo):
        _contador_cita_global[0] += 1
        self._id = _contador_cita_global[0]             # ID autoincremental
        self._paciente = paciente                          # Objeto Paciente
        self._medico = medico                              # Objeto Medico
        self._fecha = fecha                                 # Fecha string "DD/MM/AAAA"
        self._hora = hora                                   # Hora string "HH:MM"
        self._motivo = motivo                               # Motivo de consulta
        self._estado = ESTADOS_CITA_BASE[0]                 # Estado inicial "Pendiente"

    # Getters
    def obtener_id(self):       return self._id
    def obtener_paciente(self): return self._paciente
    def obtener_medico(self):   return self._medico
    def obtener_fecha(self):    return self._fecha
    def obtener_hora(self):     return self._hora
    def obtener_motivo(self):   return self._motivo
    def obtener_estado(self):   return self._estado

    # Setters/Modificadores
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado de la cita si el nuevo estado es válido."""
        if nuevo_estado in ESTADOS_CITA_BASE:
            self._estado = nuevo_estado

    def a_dict(self):
        """Convierte la cita a diccionario para reportes."""
        return {
            "id":       self._id,
            "paciente": self._paciente.obtener_nombre(),
            "medico":   self._medico.obtener_nombre(),
            "fecha":    self._fecha,
            "hora":     self._hora,
            "motivo":   self._motivo,
            "estado":   self._estado,
        }

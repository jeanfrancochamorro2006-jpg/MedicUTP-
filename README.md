# 🏥 MEDIC-UTP — Sistema de Citas Médicas y Facturación

Proyecto universitario desarrollado en **Python**.

Sistema de escritorio en **consola** que gestiona el flujo de atención de una clínica:

```
REGISTRO  ->  AGENDAMIENTO  ->  FACTURACIÓN
```

## 📌 Estado del proyecto (Avance 1)

| Módulo | Estado |
|--------|--------|
| **REGISTRO** (pacientes y médicos) | ✅ Funcional |
| **AGENDAMIENTO** (citas) | 🔲 Próximo avance |
| **FACTURACIÓN** (IGV) | 🔲 Próximo avance |

## ⚙️ Funciones actuales

- Registrar pacientes y médicos.
- Listar pacientes y médicos.
- Validación de datos (DNI de 8 dígitos, edades numéricas, campos obligatorios).

## 🧩 Conceptos de POO aplicados

- **Herencia simple:** `Persona` → `Paciente` y `Medico`.
- **Encapsulamiento:** atributos protegidos (`_dni`, `_nombre`).
- **Programación procedimental:** funciones de entrada de datos.
- **Arreglos (listas):** almacenamiento en memoria.
- **Menús en consola:** navegación con bucles `while`.

## ▶️ Cómo ejecutar

```bash
python main.py
```

---
Desarrollado por **Jeanfranco Chamorro** — Universidad Tecnológica del Perú (UTP).

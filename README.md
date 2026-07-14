# 🏥 MEDIC-UTP — Sistema de Citas Médicas y Facturación

Proyecto universitario desarrollado en **Python**, ejecutado íntegramente por **consola**.

Sistema que gestiona el flujo de atención de una clínica:

```
REGISTRO  ->  AGENDAMIENTO  ->  FACTURACIÓN  ->  ANÁLISIS DE DATOS
```

## 📌 Estado del proyecto

| Módulo | Estado |
|--------|--------|
| **REGISTRO** (pacientes y médicos) | ✅ Funcional |
| **AGENDAMIENTO** (citas) | ✅ Funcional |
| **FACTURACIÓN** (boletas/facturas + descarga en PDF) | ✅ Funcional |
| **ANÁLISIS DE DATOS** (pandas / numpy / matplotlib) | ✅ Funcional |

## ⚙️ Funciones principales

- Registrar, listar y buscar pacientes y médicos (por seguro / especialidad).
- Agendar citas validando disponibilidad de médico, fecha y hora.
- Generar boletas y facturas electrónicas (con cálculo automático de RUC 10 y
  descuento según tipo de seguro) y **descargarlas en PDF**.
- Analizar los datos del sistema con `pandas`/`numpy` (estadísticas de
  pacientes, ingresos por especialidad, citas por mes) y exportarlos a CSV.
- Generar gráficos (`matplotlib`) guardados como imágenes en `reportes/`.

## 🧩 Conceptos aplicados

- **POO**: clases, objetos, constructores, encapsulamiento.
- **Herencia simple**: `Persona` → `Medico`.
- **Herencia múltiple**: `Persona` + `InformacionContacto` → `Paciente`.
- **Polimorfismo por sobreescritura**: `obtener_resumen()` en cada subclase.
- **Polimorfismo por sobrecarga (simulada)**: `BuscadorClinico.buscar()`.
- **Programación funcional**: `filter()`, `map()`, `functools.reduce()`, lambdas y comprensiones.
- **Estructuras de datos**: listas, tuplas (catálogos inmutables), sets y diccionarios.
- **Análisis de datos**: `pandas` (DataFrame, groupby, describe) y `numpy` (media, mediana, percentiles).

## 📂 Estructura del proyecto

```
MedicUTP-/
├── main.py                  # Orquesta el menú principal
├── requirements.txt
├── clases/                  # Entidades del dominio (POO)
├── polimorfismo/             # Sobrecarga y sobreescritura
├── modulos/                 # Lógica de cada paso del flujo
│   ├── estado.py             # Colecciones y catálogos compartidos
│   ├── ui_consola.py         # Diseño de pantallas
│   ├── validaciones.py       # Entrada/salida validada
│   ├── utilidades.py         # Búsquedas y RUC (funciones puras)
│   ├── persistencia.py       # Guardado/carga en db.json
│   ├── registro.py
│   ├── agendamiento.py
│   ├── facturacion.py
│   ├── exportar_pdf.py       # Descarga de comprobantes en PDF
│   ├── analisis_datos.py     # pandas / numpy
│   └── visualizacion.py      # Gráficos matplotlib
└── tests/                    # Pruebas unitarias (unittest)
```

## ▶️ Cómo ejecutar

```bash
pip install -r requirements.txt
python main.py
```

## ✅ Cómo correr las pruebas

```bash
python -m unittest discover -s tests -v
```

## 📄 Generar el informe del proyecto (Word)

```bash
python generar_informe.py
```

Genera `Informe_MedicUTP.docx`, listo para editar en Microsoft Word.

---
Desarrollado por el equipo MEDIC-UTP — Universidad Tecnológica del Perú (UTP).

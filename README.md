# CEPAIM Dashboard

Dashboard interactivo de análisis de datos para organización de servicios sociales. Visualiza información de participantes: sexo, edad, vulnerabilidad, distribución territorial.

## Tech Stack

- **Python 3.x** - Lenguaje principal
- **Pandas** - Procesamiento y análisis de datos
- **Plotly** - Visualizaciones interactivas
- **GeoPandas** - Datos geográficos y mapas
- **Streamlit** - Interfaz web del dashboard
- **Pytest** - Testing unitario

## Estructura del Proyecto

```
├── src/
│   ├── data_loader.py    # Carga y procesamiento de datos
│   └── charts.py         # Funciones de visualización
├── config/
│   └── settings.py       # Configuración centralizada
├── test/
│   └── test_data_loader.py  # Tests unitarios
├── docs/
│   ├── Aprendizaje.md    # Documentación de aprendizaje consolidada
│   ├── Diseno.md         # Plan de diseño y desarrollo
│   └── Registro_Trabajo.md # Registro diario de trabajo
├── old/                  # Código legacy (no utilizado)
├── requirements.txt
└── README.md
```

## Instalación

```bash
git clone https://github.com/emaljarilla/chartsFCC.git
cd chartsFCC
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
# Dashboard con Streamlit (legacy)
streamlit run old/proyecto_cepaim_2.py

# Tests
pytest -v
```

## Documentación

- **`CONTINUAR.md`** - Punto de entrada para continuar trabajo (usa "continuamos")
- **`docs/Aprendizaje.md`** - Plan de aprendizaje, examen diagnóstico, guía de testing
- **`docs/Diseno.md`** - Arquitectura, fases de desarrollo, plan de gráficos
- **`docs/Registro_Trabajo.md`** - Registro diario del progreso
- **`AGENTS.md`** - Guía técnica para asistentes de IA

## Datos

Este proyecto requiere datos de participantes (CSV) y shapefile de Comunidades Autónomas.

> **Nota**: Los datos no se incluyen en el repositorio por razones de privacidad y tamaño.

### Archivos necesarios

| Archivo | Descripción |
|---------|-------------|
| `data/cepaim.csv` | CSV con datos de participantes |
| `data/comunidad_autonoma.zip` | Shapefile de CCAA para mapas |

### Estructura esperada del CSV

El archivo `cepaim.csv` debe contener estas columnas:
- `Fecha de nacimiento` (dd/mm/YYYY)
- `Fecha` (dd/mm/YYYY)
- `Sexo` (H/M)
- `Nacionalidad`
- `Comunidad autónoma`
- `Vulnerable` (sí/no, 1/0, True/False)

## Características

- Análisis demográfico de participantes
- Distribución por sexo, edad y vulnerabilidad
- Visualizaciones geográficas por CCAA
- Gráficos interactivos con Plotly

## Tests

```bash
pytest -v
```

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## Acerca de

Dashboard desarrollado para generar la Memoria anual de la organización, permitiendo visualizar datos de participantes en programas sociales. La arquitectura modular permite reutilizar el código para otras organizaciones.

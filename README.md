# Dashboard CEPAIM - Proyecto de Portfolio

**Dashboard interactivo de análisis de datos para CEPAIM** (organización de servicios sociales)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Objetivo del Proyecto

Este proyecto es el **buque insignia de mi portfolio profesional** para demostrar habilidades en:
- **Python/Data Science**: Análisis de datos con Pandas
- **Visualización**: Gráficos interactivos con Plotly
- **Testing**: Arquitectura limpia con tests unitarios
- **Web Development**: Dashboard con Streamlit
- **CI/CD**: Automatización con GitHub Actions

## Características del Dashboard

### Visualizaciones Implementadas
- **Análisis demográfico**: Sexo, edad, vulnerabilidad
- **Distribución territorial**: Mapas de Comunidades Autónomas
- **Gráficos interactivos**: Donuts, barras, choropleths
- **Filtros dinámicos**: Selección por múltiples criterios

### Arquitectura Técnica
```
dashboard-cepaim/
├── src/                 # Código modular
│   ├── data_loader.py   # Carga y procesamiento de datos
│   ├── charts.py        # Funciones de visualización
│   └── app.py          # Dashboard Streamlit (en desarrollo)
├── config/              # Configuración centralizada
├── test/               # Tests unitarios (pytest)
├── data/               # Datos CSV y shapefiles
├── old/                # Scripts legacy (referencia)
└── docs/               # Documentación técnica
```

## Estado Actual del Proyecto

### Fase 1: Testing (75% completado)
- ✅ 17/22 tests unitarios implementados
- ✅ Configuración centralizada
- ✅ Módulos base creados
- 🔄 Bug crítico de nombres de columnas (corregir)
- ❌ Dashboard Streamlit (por implementar)

### Roadmap de 3 Meses
1. **Mes 1**: Fundamentos sólidos (testing + dashboard básico)
2. **Mes 2**: Funcionalidad completa (gráficos + interfaz)
3. **Mes 3**: Portfolio y publicación (deploy + documentación)

## Instalación Rápida

### Requisitos previos
- Python 3.9+
- pip

### Configuración del entorno
```bash
# Clonar repositorio
git clone https://github.com/usuario/dashboard-cepaim.git
cd dashboard-cepaim

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias principales
```txt
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
geopandas>=0.14.0
streamlit>=1.28.0
pytest>=7.4.0
```

## Ejecución

### Dashboard (en desarrollo)
```bash
streamlit run src/app.py
```

### Tests
```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar con coverage
pytest --cov=src --cov-report=term-missing

# Ejecutar tests específicos
pytest test/test_data_loader.py::test_calculate_age_cumple_anos -v
```

### Calidad de Código
```bash
# Linting con ruff
ruff check .
ruff check . --fix

# Type checking con mypy
mypy src/ --ignore-missing-imports
```

## Estructura de Datos

### CSV de Participantes (`data/cepaim.csv`)
Columnas en snake_case:
```csv
f_nacimiento,fecha,sexo,nacionalidad,comunidad,centro,vulnerable,...
```

### Shapefile de CCAA (`data/comunidad_autonoma.zip`)
Formato GeoJSON para visualización geográfica

## Plan de Aprendizaje

### Cursos Recomendados (Gratuitos)
1. **Python para Data Science**: [Coursera - Python: de explorador de datos a analista](https://coursera.org/learn/python-analista)
2. **JavaScript Moderno**: [javascript.info/es](https://es.javascript.info/)
3. **Testing**: Documentación oficial de [pytest](https://docs.pytest.org/)

### Semana Tipo Sugerida
- **Lunes-Miércoles**: Python/Data Science (2h/día)
- **Jueves-Viernes**: JavaScript (2h/día)
- **Sábado**: Desarrollo del proyecto (3-4h)
- **Domingo**: Repaso y planificación

## Contribuir

Este es un proyecto personal de aprendizaje. Si tienes sugerencias:

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/mejora`)
5. Abre un Pull Request

## Técnicas y Tecnologías

### Stack Principal
- **Backend**: Python 3.9+, Pandas, NumPy
- **Visualización**: Plotly, GeoPandas
- **Frontend**: Streamlit
- **Testing**: Pytest, Coverage
- **CI/CD**: GitHub Actions (en configuración)

### Patrones de Diseño
- Arquitectura modular (separación de responsabilidades)
- Configuración centralizada (sin hardcoding)
- Tests unitarios (TDD aproximado)
- Type hints (Python 3.9+)

## Portfolio y Demo

### Enlaces Importantes
- **Demo en vivo**: [Dashboard CEPAIM](https://dashboard-cepaim.streamlit.app/) (próximamente)
- **Documentación**: [Wiki del Proyecto](https://github.com/usuario/dashboard-cepaim/wiki)
- **Caso de Estudio**: [PDF descargable](docs/caso_de_estudio.pdf)

### Video Demo
[Ver demo del dashboard](https://youtu.be/ejemplo) (3 minutos)

## Roadmap de Desarrollo

### ✅ Completado
- [x] Análisis de requisitos
- [x] Arquitectura modular
- [x] Configuración centralizada
- [x] Tests unitarios básicos

### 🔄 En Progreso
- [ ] Corrección de bugs críticos
- [ ] Dashboard Streamlit mínimo
- [ ] Migración de gráficos legacy

### 📅 Próximas Funcionalidades
- [ ] Filtros interactivos
- [ ] Exportación de reportes
- [ ] Autenticación de usuarios
- [ ] API REST (futuro)

## Contacto

**Desarrollador**: Emilio Aljarilla  
**Email**: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)  
**LinkedIn**: [linkedin.com/in/tu-perfil](https://linkedin.com/in/tu-perfil)  
**GitHub**: [@tu-usuario](https://github.com/tu-usuario)

## Licencia

Este proyecto está bajo la licencia MIT - ver [LICENSE](LICENSE) para detalles.

## Agradecimientos

- **CEPAIM**: Por proporcionar datos reales (anonimizados)
- **Comunidad Python**: Por herramientas increíbles como Pandas y Plotly
- **Streamlit**: Por hacer dashboards accesibles

---

**Nota**: Este proyecto está en desarrollo activo. La documentación se actualiza regularmente. Para el estado más reciente, consulta los commits y issues en GitHub.

*Última actualización: 27 Marzo 2026*
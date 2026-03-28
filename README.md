# 🚀 SpaceHack - Análisis de Datos de Puertos Mundiales y Emisiones Marítimas

**Un repositorio profesional con código, datos e insights para logística sostenible.**

---

## 📁 Estructura del Proyecto

```
SpaceHack/
│
├── 📂 datasets/                     ← DATOS ORIGINALES
│   ├── pub150.csv                   (3.3 MB) - 3,804 puertos mundiales
│   └── transporte.csv               (71.4 MB) - 157,604 registros emisiones
│
├── 📂 codigo/                       ← SCRIPTS PYTHON
│   ├── analyzer_spacehack.py        → Core: Cargador de datos
│   ├── uso_datos_puertos.py         → 10 ejemplos prácticos + generador insights
│   └── visualizaciones.py           → Gráficos, tablas y reportes
│
├── 📂 insights/                     ← INSIGHTS GENERADOS (CSV)
│   ├── mega_puertos.csv             (214 KB) - 242 mega-puertos
│   ├── puertos_eco.csv              (552 KB) - 636 puertos eco-amigables
│   ├── emisiones_por_barco.csv      (1 KB) - 21 tipos de barco
│   └── top_50_puertos.csv           (49 KB) - Top 50
│
├── 📂 resultados/                   ← GRÁFICOS Y REPORTES (PNG + TXT)
│   ├── grafico_mega_puertos.png
│   ├── grafico_distribucion_tamaño.png
│   ├── grafico_emisiones_barco.png
│   ├── grafico_servicios_eco.png
│   ├── tabla_mega_puertos.png
│   ├── tabla_puertos_eco.png
│   ├── dashboard_ejecutivo.png
│   └── reporte_ejecutivo.txt
│
├── README.md                        ← Documentación principal
└── .gitignore                       ← Archivos excluidos de Git
```

---

## 🚀 Inicio Rápido

### 1️⃣ Generar Insights

```bash
cd codigo
python uso_datos_puertos.py
```

**Qué hace:**
- Lee datos crudos desde `../datasets/`
- Ejecuta 10 análisis distintos
- Exporta 4 CSV a `../insights/`

**Salida esperada:**
```
✓ Datos cargados
  • 3,804 puertos
  • 157,604 registros de emisiones

✓ Mega-puertos exportados (242 registros)
✓ Puertos eco exportados (636 registros)
...etc
```

---

### 2️⃣ Generar Visualizaciones

```bash
cd codigo
python visualizaciones.py
```

**Genera automáticamente:**
- 4 gráficos principales (PNG)
- 2 tablas ejecutivas (PNG)
- 1 dashboard 2x2 (PNG)
- 1 reporte ejecutivo (TXT)

**Todos guardados en `../resultados/`**

---

## 📊 Archivos Principales

### `analyzer_spacehack.py` (Core Data Loader)

**Propósito:** Clase unificada para cargar y procesar datos

```python
from analyzer_spacehack import PortEmissionsAnalyzer

# Usar
analyzer = PortEmissionsAnalyzer("datasets/pub150.csv", "datasets/transporte.csv")
analyzer.load_data()
analyzer.generate_report()
```

**Métodos:**
- `load_data()` - Carga ambos CSVs
- `explore_ports()` - Análisis de puertos
- `explore_emissions()` - Análisis de emisiones
- `generate_insights()` - 6 insights principales
- `generate_report()` - Reporte completo

---

### `uso_datos_puertos.py` (Ejemplos + Insights Generator)

**Propósito:** 10 ejemplos prácticos de acceso a datos y generación de insights

**Ejemplos incluidos:**

| # | Nombre | Genera |
|---|--------|--------|
| 1 | Análisis Completo | Consola |
| 2 | Paso a Paso | Consola |
| 3 | Acceso a Datos | Consola |
| 4 | Mega-Puertos | `mega_puertos.csv` |
| 5 | Por Región | Consola |
| 6 | Puertos Eco | `puertos_eco.csv` |
| 7 | Scoring Custom | Consola |
| 8 | Exportar JSON | Consola |
| 9 | Emisiones por Barco | `emisiones_por_barco.csv` |
| 10 | Búsqueda Flexible | Consola |

**Variables principales en el script:**

```python
puertos_df         # DataFrame: 3,804 puertos
emisiones_df       # DataFrame: 157,604 registros

# Acceso directo a insights generados:
datos_singapore    # Datos de puerto específico
datos_mega_puertos # 242 mega-puertos
datos_eco          # 636 puertos eco-amigables
```

---

### `visualizaciones.py` (Gráficos + Reportes)

**Propósito:** Transformar insights en gráficos y reportes ejecutivos

**Gráficos generados:**

1. **grafico_mega_puertos.png**
   - Top 20 mega-puertos por eslora
   - Gráfico de barras horizontal

2. **grafico_distribucion_tamaño.png**
   - Distribución de puertos por tamaño
   - Gráfico de pie con porcentajes

3. **grafico_emisiones_barco.png**
   - Emisiones promedio por tipo de barco (Top 15)
   - Gráfico de barras con degradado de color

4. **grafico_servicios_eco.png**
   - Servicios en puertos eco-amigables
   - Gráfico de pie

5. **tabla_mega_puertos.png**
   - Top 15 mega-puertos en formato tabla visual
   - Con números, países, tamaños y dimensiones

6. **tabla_puertos_eco.png**
   - Top 12 puertos eco-amigables en formato tabla
   - Indicadores de servicios (✓/✗)

7. **dashboard_ejecutivo.png**
   - 4 visualizaciones en 1 imagen
   - Ideal para presentaciones

8. **reporte_ejecutivo.txt**
   - Resumen en texto de todo el análisis
   - Listo para compartir por email

---

## 📈 Datos y Estadísticas

### Cobertura Global ✓

| Métrica | Valor |
|---------|-------|
| Total de Puertos | 3,804 |
| Países | 195 |
| Regiones | 347 |
| Registros de Emisiones | 157,604 |
| Años de Datos | 2023-2025 |

### Mega-Puertos ⛴️

| Categoría | Cantidad |
|-----------|----------|
| Mega-puertos (>250m x >10m) | 242 |
| Puertos "Very Large" | 428 |
| Eslora promedio máxima | ~200m |
| Calado promedio máximo | ~11m |

### Infraestructura Ambiental 🌿

| Servicio | Puertos | % |
|----------|---------|-----|
| Garbage Disposal | 1,313 | 34.5% |
| Ballast Disposal | 918 | 24.1% |
| Reparaciones | 712 | 18.7% |
| **Ambos servicios** | **636** | **16.7%** |

### Emisiones 💨

| Tipo de Barco | Registros | Emisiones Promedio |
|---------------|-----------|-------------------|
| CONTAINER | 960 | 6.1M tons CO2 |
| BULK_CARRIER | 960 | 5.0M tons CO2 |
| OIL_TANKER | 960 | 3.7M tons CO2 |
| ALL_VESSELS | 73,876 | 501k tons CO2 |

---

## 🔍 Ejemplos de Uso

### Acceder a datos de puerto específico

```python
# En uso_datos_puertos.py
datos_singapore = puertos_df[puertos_df['Main Port Name'] == 'Singapore']

print(f"Puerto: {datos_singapore.iloc[0]['Main Port Name']}")
print(f"País: {datos_singapore.iloc[0]['Country Code']}")
print(f"Tamaño: {datos_singapore.iloc[0]['Harbor Size']}")
```

### Filtrar mega-puertos

```python
mega_puertos = puertos_df[
    (pd.to_numeric(puertos_df['Maximum Vessel Length (m)'], errors='coerce') > 250) &
    (pd.to_numeric(puertos_df['Maximum Vessel Draft (m)'], errors='coerce') > 10)
]
print(f"Total: {len(mega_puertos)} mega-puertos")
```

### Calcular estadísticas por región

```python
por_region = puertos_df['Region Name'].value_counts()
print(por_region.head(10))
```

---

## 🛠️ Dependencias

```
pandas>=1.3.0          # Procesamiento de datos
numpy>=1.20.0          # Cálculos numéricos
matplotlib>=3.4.0      # Gráficos
seaborn>=0.11.0        # Visualización mejorada
```

### Instalación

```bash
pip install pandas numpy matplotlib seaborn
```

---

## 📝 Flujo de Datos

```
datasets/
├── pub150.csv (3.5 MB)       ──┐
└── transporte.csv (74 MB)    ──┤
                                 ├─→ analyzer_spacehack.py ──→ uso_datos_puertos.py ──→ insights/
                                 │       (Loader)             (Ejemplos)           (4 CSVs)
                                 │
                                 └────────────────────────────→ visualizaciones.py
                                         (Genera gráficos)      (7 PNGs + 1 TXT)
```

---

## 🎯 Casos de Uso

### 1. Para Reportería Ejecutiva
```bash
python visualizaciones.py
# → Genera dashboard_ejecutivo.png + reporte_ejecutivo.txt
```

### 2. Para Análisis Personalizado
Edita `uso_datos_puertos.py` – todos los ejemplos están listos para modificar

### 3. Para Integración en Scripts
```python
from analyzer_spacehack import PortEmissionsAnalyzer

analyzer = PortEmissionsAnalyzer("datasets/pub150.csv", "datasets/transporte.csv")
analyzer.load_data()
# Ahora tienes acceso a analyzer.ports_df y analyzer.emissions_df
```

### 4. Para Automatización
```bash
# Ejecutar análisis completo
python uso_datos_puertos.py && python visualizaciones.py
```

---

## 📊 Insights Generados

### 1. Mega-Puertos (242 identificados)
Puertos capaces de recibir buques ultra-grandes. Estratégicos para sostenibilidad.

### 2. Puertos Eco-Amigables (636 identificados)
Puertos con servicios ambientales completos (garbage + ballast disposal).

### 3. Emisiones por Barco
Top 10 tipos de barco por emisiones promedio – indica industria crítica.

### 4. Distribución Regional
347 regiones – cobertura global con concentración en zona templada.

---

## 🔗 Integración GitHub

```bash
# Clonar
git clone https://github.com/[usuario]/SpaceHack.git
cd SpaceHack

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar análisis
python uso_datos_puertos.py

# Generar visualizaciones
python visualizaciones.py
```

---

## 📞 Soporte

| Problema | Solución |
|----------|----------|
| "FileNotFoundError: pub150.csv" | Verifica que los CSV están en `datasets/` |
| "ImportError: No module named 'analyzer_spacehack'" | Asegúrate de estar en el directorio raíz del proyecto |
| Gráficos vacíos | Verifica que `uso_datos_puertos.py` se ejecutó primero |

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para análisis, educación y sostenibilidad.

---

## 👥 Créditos

**SPACEHACK Logística Net-Zero**
- Hackathon de sostenibilidad logística
- Datos: World Port Index (pub150) + Eurostat Emissions (transporte)
- Objetivo: Optimizar rutas marítimas reduciendo CO2

---

**Última actualización:** Marzo 2026  
**Versión:** 1.0  
**Estado:** ✅ Producción

```
SpaceHack
├─ .venv
│  ├─ Include
│  ├─ Lib
│  │  └─ site-packages
│  │     ├─ pip
│  │     │  ├─ py.typed
│  │     │  ├─ _internal
│  │     │  │  ├─ build_env.py
│  │     │  │  ├─ cache.py
│  │     │  │  ├─ cli
│  │     │  │  │  ├─ autocompletion.py
│  │     │  │  │  ├─ base_command.py
│  │     │  │  │  ├─ cmdoptions.py
│  │     │  │  │  ├─ command_context.py
│  │     │  │  │  ├─ index_command.py
│  │     │  │  │  ├─ main.py
│  │     │  │  │  ├─ main_parser.py
│  │     │  │  │  ├─ parser.py
│  │     │  │  │  ├─ progress_bars.py
│  │     │  │  │  ├─ req_command.py
│  │     │  │  │  ├─ spinners.py
│  │     │  │  │  ├─ status_codes.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ autocompletion.cpython-314.pyc
│  │     │  │  │     ├─ base_command.cpython-314.pyc
│  │     │  │  │     ├─ cmdoptions.cpython-314.pyc
│  │     │  │  │     ├─ command_context.cpython-314.pyc
│  │     │  │  │     ├─ index_command.cpython-314.pyc
│  │     │  │  │     ├─ main.cpython-314.pyc
│  │     │  │  │     ├─ main_parser.cpython-314.pyc
│  │     │  │  │     ├─ parser.cpython-314.pyc
│  │     │  │  │     ├─ progress_bars.cpython-314.pyc
│  │     │  │  │     ├─ req_command.cpython-314.pyc
│  │     │  │  │     ├─ spinners.cpython-314.pyc
│  │     │  │  │     ├─ status_codes.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ commands
│  │     │  │  │  ├─ cache.py
│  │     │  │  │  ├─ check.py
│  │     │  │  │  ├─ completion.py
│  │     │  │  │  ├─ configuration.py
│  │     │  │  │  ├─ debug.py
│  │     │  │  │  ├─ download.py
│  │     │  │  │  ├─ freeze.py
│  │     │  │  │  ├─ hash.py
│  │     │  │  │  ├─ help.py
│  │     │  │  │  ├─ index.py
│  │     │  │  │  ├─ inspect.py
│  │     │  │  │  ├─ install.py
│  │     │  │  │  ├─ list.py
│  │     │  │  │  ├─ lock.py
│  │     │  │  │  ├─ search.py
│  │     │  │  │  ├─ show.py
│  │     │  │  │  ├─ uninstall.py
│  │     │  │  │  ├─ wheel.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ cache.cpython-314.pyc
│  │     │  │  │     ├─ check.cpython-314.pyc
│  │     │  │  │     ├─ completion.cpython-314.pyc
│  │     │  │  │     ├─ configuration.cpython-314.pyc
│  │     │  │  │     ├─ debug.cpython-314.pyc
│  │     │  │  │     ├─ download.cpython-314.pyc
│  │     │  │  │     ├─ freeze.cpython-314.pyc
│  │     │  │  │     ├─ hash.cpython-314.pyc
│  │     │  │  │     ├─ help.cpython-314.pyc
│  │     │  │  │     ├─ index.cpython-314.pyc
│  │     │  │  │     ├─ inspect.cpython-314.pyc
│  │     │  │  │     ├─ install.cpython-314.pyc
│  │     │  │  │     ├─ list.cpython-314.pyc
│  │     │  │  │     ├─ lock.cpython-314.pyc
│  │     │  │  │     ├─ search.cpython-314.pyc
│  │     │  │  │     ├─ show.cpython-314.pyc
│  │     │  │  │     ├─ uninstall.cpython-314.pyc
│  │     │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ configuration.py
│  │     │  │  ├─ distributions
│  │     │  │  │  ├─ base.py
│  │     │  │  │  ├─ installed.py
│  │     │  │  │  ├─ sdist.py
│  │     │  │  │  ├─ wheel.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ base.cpython-314.pyc
│  │     │  │  │     ├─ installed.cpython-314.pyc
│  │     │  │  │     ├─ sdist.cpython-314.pyc
│  │     │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ exceptions.py
│  │     │  │  ├─ index
│  │     │  │  │  ├─ collector.py
│  │     │  │  │  ├─ package_finder.py
│  │     │  │  │  ├─ sources.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ collector.cpython-314.pyc
│  │     │  │  │     ├─ package_finder.cpython-314.pyc
│  │     │  │  │     ├─ sources.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ locations
│  │     │  │  │  ├─ base.py
│  │     │  │  │  ├─ _distutils.py
│  │     │  │  │  ├─ _sysconfig.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ base.cpython-314.pyc
│  │     │  │  │     ├─ _distutils.cpython-314.pyc
│  │     │  │  │     ├─ _sysconfig.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ main.py
│  │     │  │  ├─ metadata
│  │     │  │  │  ├─ base.py
│  │     │  │  │  ├─ importlib
│  │     │  │  │  │  ├─ _compat.py
│  │     │  │  │  │  ├─ _dists.py
│  │     │  │  │  │  ├─ _envs.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ _compat.cpython-314.pyc
│  │     │  │  │  │     ├─ _dists.cpython-314.pyc
│  │     │  │  │  │     ├─ _envs.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ pkg_resources.py
│  │     │  │  │  ├─ _json.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ base.cpython-314.pyc
│  │     │  │  │     ├─ pkg_resources.cpython-314.pyc
│  │     │  │  │     ├─ _json.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ models
│  │     │  │  │  ├─ candidate.py
│  │     │  │  │  ├─ direct_url.py
│  │     │  │  │  ├─ format_control.py
│  │     │  │  │  ├─ index.py
│  │     │  │  │  ├─ installation_report.py
│  │     │  │  │  ├─ link.py
│  │     │  │  │  ├─ release_control.py
│  │     │  │  │  ├─ scheme.py
│  │     │  │  │  ├─ search_scope.py
│  │     │  │  │  ├─ selection_prefs.py
│  │     │  │  │  ├─ target_python.py
│  │     │  │  │  ├─ wheel.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ candidate.cpython-314.pyc
│  │     │  │  │     ├─ direct_url.cpython-314.pyc
│  │     │  │  │     ├─ format_control.cpython-314.pyc
│  │     │  │  │     ├─ index.cpython-314.pyc
│  │     │  │  │     ├─ installation_report.cpython-314.pyc
│  │     │  │  │     ├─ link.cpython-314.pyc
│  │     │  │  │     ├─ release_control.cpython-314.pyc
│  │     │  │  │     ├─ scheme.cpython-314.pyc
│  │     │  │  │     ├─ search_scope.cpython-314.pyc
│  │     │  │  │     ├─ selection_prefs.cpython-314.pyc
│  │     │  │  │     ├─ target_python.cpython-314.pyc
│  │     │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ network
│  │     │  │  │  ├─ auth.py
│  │     │  │  │  ├─ cache.py
│  │     │  │  │  ├─ download.py
│  │     │  │  │  ├─ lazy_wheel.py
│  │     │  │  │  ├─ session.py
│  │     │  │  │  ├─ utils.py
│  │     │  │  │  ├─ xmlrpc.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ auth.cpython-314.pyc
│  │     │  │  │     ├─ cache.cpython-314.pyc
│  │     │  │  │     ├─ download.cpython-314.pyc
│  │     │  │  │     ├─ lazy_wheel.cpython-314.pyc
│  │     │  │  │     ├─ session.cpython-314.pyc
│  │     │  │  │     ├─ utils.cpython-314.pyc
│  │     │  │  │     ├─ xmlrpc.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ operations
│  │     │  │  │  ├─ build
│  │     │  │  │  │  ├─ build_tracker.py
│  │     │  │  │  │  ├─ metadata.py
│  │     │  │  │  │  ├─ metadata_editable.py
│  │     │  │  │  │  ├─ wheel.py
│  │     │  │  │  │  ├─ wheel_editable.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ build_tracker.cpython-314.pyc
│  │     │  │  │  │     ├─ metadata.cpython-314.pyc
│  │     │  │  │  │     ├─ metadata_editable.cpython-314.pyc
│  │     │  │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │  │     ├─ wheel_editable.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ check.py
│  │     │  │  │  ├─ freeze.py
│  │     │  │  │  ├─ install
│  │     │  │  │  │  ├─ wheel.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ prepare.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ check.cpython-314.pyc
│  │     │  │  │     ├─ freeze.cpython-314.pyc
│  │     │  │  │     ├─ prepare.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ pyproject.py
│  │     │  │  ├─ req
│  │     │  │  │  ├─ constructors.py
│  │     │  │  │  ├─ pep723.py
│  │     │  │  │  ├─ req_dependency_group.py
│  │     │  │  │  ├─ req_file.py
│  │     │  │  │  ├─ req_install.py
│  │     │  │  │  ├─ req_set.py
│  │     │  │  │  ├─ req_uninstall.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ constructors.cpython-314.pyc
│  │     │  │  │     ├─ pep723.cpython-314.pyc
│  │     │  │  │     ├─ req_dependency_group.cpython-314.pyc
│  │     │  │  │     ├─ req_file.cpython-314.pyc
│  │     │  │  │     ├─ req_install.cpython-314.pyc
│  │     │  │  │     ├─ req_set.cpython-314.pyc
│  │     │  │  │     ├─ req_uninstall.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ resolution
│  │     │  │  │  ├─ base.py
│  │     │  │  │  ├─ legacy
│  │     │  │  │  │  ├─ resolver.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ resolver.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ resolvelib
│  │     │  │  │  │  ├─ base.py
│  │     │  │  │  │  ├─ candidates.py
│  │     │  │  │  │  ├─ factory.py
│  │     │  │  │  │  ├─ found_candidates.py
│  │     │  │  │  │  ├─ provider.py
│  │     │  │  │  │  ├─ reporter.py
│  │     │  │  │  │  ├─ requirements.py
│  │     │  │  │  │  ├─ resolver.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ base.cpython-314.pyc
│  │     │  │  │  │     ├─ candidates.cpython-314.pyc
│  │     │  │  │  │     ├─ factory.cpython-314.pyc
│  │     │  │  │  │     ├─ found_candidates.cpython-314.pyc
│  │     │  │  │  │     ├─ provider.cpython-314.pyc
│  │     │  │  │  │     ├─ reporter.cpython-314.pyc
│  │     │  │  │  │     ├─ requirements.cpython-314.pyc
│  │     │  │  │  │     ├─ resolver.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ base.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ self_outdated_check.py
│  │     │  │  ├─ utils
│  │     │  │  │  ├─ appdirs.py
│  │     │  │  │  ├─ compat.py
│  │     │  │  │  ├─ compatibility_tags.py
│  │     │  │  │  ├─ datetime.py
│  │     │  │  │  ├─ deprecation.py
│  │     │  │  │  ├─ direct_url_helpers.py
│  │     │  │  │  ├─ egg_link.py
│  │     │  │  │  ├─ entrypoints.py
│  │     │  │  │  ├─ filesystem.py
│  │     │  │  │  ├─ filetypes.py
│  │     │  │  │  ├─ glibc.py
│  │     │  │  │  ├─ hashes.py
│  │     │  │  │  ├─ logging.py
│  │     │  │  │  ├─ misc.py
│  │     │  │  │  ├─ packaging.py
│  │     │  │  │  ├─ pylock.py
│  │     │  │  │  ├─ retry.py
│  │     │  │  │  ├─ subprocess.py
│  │     │  │  │  ├─ temp_dir.py
│  │     │  │  │  ├─ unpacking.py
│  │     │  │  │  ├─ urls.py
│  │     │  │  │  ├─ virtualenv.py
│  │     │  │  │  ├─ wheel.py
│  │     │  │  │  ├─ _jaraco_text.py
│  │     │  │  │  ├─ _log.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ appdirs.cpython-314.pyc
│  │     │  │  │     ├─ compat.cpython-314.pyc
│  │     │  │  │     ├─ compatibility_tags.cpython-314.pyc
│  │     │  │  │     ├─ datetime.cpython-314.pyc
│  │     │  │  │     ├─ deprecation.cpython-314.pyc
│  │     │  │  │     ├─ direct_url_helpers.cpython-314.pyc
│  │     │  │  │     ├─ egg_link.cpython-314.pyc
│  │     │  │  │     ├─ entrypoints.cpython-314.pyc
│  │     │  │  │     ├─ filesystem.cpython-314.pyc
│  │     │  │  │     ├─ filetypes.cpython-314.pyc
│  │     │  │  │     ├─ glibc.cpython-314.pyc
│  │     │  │  │     ├─ hashes.cpython-314.pyc
│  │     │  │  │     ├─ logging.cpython-314.pyc
│  │     │  │  │     ├─ misc.cpython-314.pyc
│  │     │  │  │     ├─ packaging.cpython-314.pyc
│  │     │  │  │     ├─ pylock.cpython-314.pyc
│  │     │  │  │     ├─ retry.cpython-314.pyc
│  │     │  │  │     ├─ subprocess.cpython-314.pyc
│  │     │  │  │     ├─ temp_dir.cpython-314.pyc
│  │     │  │  │     ├─ unpacking.cpython-314.pyc
│  │     │  │  │     ├─ urls.cpython-314.pyc
│  │     │  │  │     ├─ virtualenv.cpython-314.pyc
│  │     │  │  │     ├─ wheel.cpython-314.pyc
│  │     │  │  │     ├─ _jaraco_text.cpython-314.pyc
│  │     │  │  │     ├─ _log.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ vcs
│  │     │  │  │  ├─ bazaar.py
│  │     │  │  │  ├─ git.py
│  │     │  │  │  ├─ mercurial.py
│  │     │  │  │  ├─ subversion.py
│  │     │  │  │  ├─ versioncontrol.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ bazaar.cpython-314.pyc
│  │     │  │  │     ├─ git.cpython-314.pyc
│  │     │  │  │     ├─ mercurial.cpython-314.pyc
│  │     │  │  │     ├─ subversion.cpython-314.pyc
│  │     │  │  │     ├─ versioncontrol.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ wheel_builder.py
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     ├─ build_env.cpython-314.pyc
│  │     │  │     ├─ cache.cpython-314.pyc
│  │     │  │     ├─ configuration.cpython-314.pyc
│  │     │  │     ├─ exceptions.cpython-314.pyc
│  │     │  │     ├─ main.cpython-314.pyc
│  │     │  │     ├─ pyproject.cpython-314.pyc
│  │     │  │     ├─ self_outdated_check.cpython-314.pyc
│  │     │  │     ├─ wheel_builder.cpython-314.pyc
│  │     │  │     └─ __init__.cpython-314.pyc
│  │     │  ├─ _vendor
│  │     │  │  ├─ cachecontrol
│  │     │  │  │  ├─ adapter.py
│  │     │  │  │  ├─ cache.py
│  │     │  │  │  ├─ caches
│  │     │  │  │  │  ├─ file_cache.py
│  │     │  │  │  │  ├─ redis_cache.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ file_cache.cpython-314.pyc
│  │     │  │  │  │     ├─ redis_cache.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ controller.py
│  │     │  │  │  ├─ filewrapper.py
│  │     │  │  │  ├─ heuristics.py
│  │     │  │  │  ├─ LICENSE.txt
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ serialize.py
│  │     │  │  │  ├─ wrapper.py
│  │     │  │  │  ├─ _cmd.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ adapter.cpython-314.pyc
│  │     │  │  │     ├─ cache.cpython-314.pyc
│  │     │  │  │     ├─ controller.cpython-314.pyc
│  │     │  │  │     ├─ filewrapper.cpython-314.pyc
│  │     │  │  │     ├─ heuristics.cpython-314.pyc
│  │     │  │  │     ├─ serialize.cpython-314.pyc
│  │     │  │  │     ├─ wrapper.cpython-314.pyc
│  │     │  │  │     ├─ _cmd.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ certifi
│  │     │  │  │  ├─ cacert.pem
│  │     │  │  │  ├─ core.py
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ core.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ dependency_groups
│  │     │  │  │  ├─ LICENSE.txt
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ _implementation.py
│  │     │  │  │  ├─ _lint_dependency_groups.py
│  │     │  │  │  ├─ _pip_wrapper.py
│  │     │  │  │  ├─ _toml_compat.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ _implementation.cpython-314.pyc
│  │     │  │  │     ├─ _lint_dependency_groups.cpython-314.pyc
│  │     │  │  │     ├─ _pip_wrapper.cpython-314.pyc
│  │     │  │  │     ├─ _toml_compat.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ distlib
│  │     │  │  │  ├─ compat.py
│  │     │  │  │  ├─ LICENSE.txt
│  │     │  │  │  ├─ resources.py
│  │     │  │  │  ├─ scripts.py
│  │     │  │  │  ├─ t32.exe
│  │     │  │  │  ├─ t64-arm.exe
│  │     │  │  │  ├─ t64.exe
│  │     │  │  │  ├─ util.py
│  │     │  │  │  ├─ w32.exe
│  │     │  │  │  ├─ w64-arm.exe
│  │     │  │  │  ├─ w64.exe
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ compat.cpython-314.pyc
│  │     │  │  │     ├─ resources.cpython-314.pyc
│  │     │  │  │     ├─ scripts.cpython-314.pyc
│  │     │  │  │     ├─ util.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ distro
│  │     │  │  │  ├─ distro.py
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ distro.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ idna
│  │     │  │  │  ├─ codec.py
│  │     │  │  │  ├─ compat.py
│  │     │  │  │  ├─ core.py
│  │     │  │  │  ├─ idnadata.py
│  │     │  │  │  ├─ intranges.py
│  │     │  │  │  ├─ LICENSE.md
│  │     │  │  │  ├─ package_data.py
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ uts46data.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ codec.cpython-314.pyc
│  │     │  │  │     ├─ compat.cpython-314.pyc
│  │     │  │  │     ├─ core.cpython-314.pyc
│  │     │  │  │     ├─ idnadata.cpython-314.pyc
│  │     │  │  │     ├─ intranges.cpython-314.pyc
│  │     │  │  │     ├─ package_data.cpython-314.pyc
│  │     │  │  │     ├─ uts46data.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ msgpack
│  │     │  │  │  ├─ COPYING
│  │     │  │  │  ├─ exceptions.py
│  │     │  │  │  ├─ ext.py
│  │     │  │  │  ├─ fallback.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ exceptions.cpython-314.pyc
│  │     │  │  │     ├─ ext.cpython-314.pyc
│  │     │  │  │     ├─ fallback.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ packaging
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ LICENSE.APACHE
│  │     │  │  │  ├─ LICENSE.BSD
│  │     │  │  │  ├─ licenses
│  │     │  │  │  │  ├─ _spdx.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ _spdx.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ markers.py
│  │     │  │  │  ├─ metadata.py
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ pylock.py
│  │     │  │  │  ├─ requirements.py
│  │     │  │  │  ├─ specifiers.py
│  │     │  │  │  ├─ tags.py
│  │     │  │  │  ├─ utils.py
│  │     │  │  │  ├─ version.py
│  │     │  │  │  ├─ _elffile.py
│  │     │  │  │  ├─ _manylinux.py
│  │     │  │  │  ├─ _musllinux.py
│  │     │  │  │  ├─ _parser.py
│  │     │  │  │  ├─ _structures.py
│  │     │  │  │  ├─ _tokenizer.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ markers.cpython-314.pyc
│  │     │  │  │     ├─ metadata.cpython-314.pyc
│  │     │  │  │     ├─ pylock.cpython-314.pyc
│  │     │  │  │     ├─ requirements.cpython-314.pyc
│  │     │  │  │     ├─ specifiers.cpython-314.pyc
│  │     │  │  │     ├─ tags.cpython-314.pyc
│  │     │  │  │     ├─ utils.cpython-314.pyc
│  │     │  │  │     ├─ version.cpython-314.pyc
│  │     │  │  │     ├─ _elffile.cpython-314.pyc
│  │     │  │  │     ├─ _manylinux.cpython-314.pyc
│  │     │  │  │     ├─ _musllinux.cpython-314.pyc
│  │     │  │  │     ├─ _parser.cpython-314.pyc
│  │     │  │  │     ├─ _structures.cpython-314.pyc
│  │     │  │  │     ├─ _tokenizer.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ pkg_resources
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ platformdirs
│  │     │  │  │  ├─ android.py
│  │     │  │  │  ├─ api.py
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ macos.py
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ unix.py
│  │     │  │  │  ├─ version.py
│  │     │  │  │  ├─ windows.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ android.cpython-314.pyc
│  │     │  │  │     ├─ api.cpython-314.pyc
│  │     │  │  │     ├─ macos.cpython-314.pyc
│  │     │  │  │     ├─ unix.cpython-314.pyc
│  │     │  │  │     ├─ version.cpython-314.pyc
│  │     │  │  │     ├─ windows.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ pygments
│  │     │  │  │  ├─ console.py
│  │     │  │  │  ├─ filter.py
│  │     │  │  │  ├─ filters
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ formatter.py
│  │     │  │  │  ├─ formatters
│  │     │  │  │  │  ├─ _mapping.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ _mapping.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ lexer.py
│  │     │  │  │  ├─ lexers
│  │     │  │  │  │  ├─ python.py
│  │     │  │  │  │  ├─ _mapping.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ python.cpython-314.pyc
│  │     │  │  │  │     ├─ _mapping.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ modeline.py
│  │     │  │  │  ├─ plugin.py
│  │     │  │  │  ├─ regexopt.py
│  │     │  │  │  ├─ scanner.py
│  │     │  │  │  ├─ sphinxext.py
│  │     │  │  │  ├─ style.py
│  │     │  │  │  ├─ styles
│  │     │  │  │  │  ├─ _mapping.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ _mapping.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ token.py
│  │     │  │  │  ├─ unistring.py
│  │     │  │  │  ├─ util.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ console.cpython-314.pyc
│  │     │  │  │     ├─ filter.cpython-314.pyc
│  │     │  │  │     ├─ formatter.cpython-314.pyc
│  │     │  │  │     ├─ lexer.cpython-314.pyc
│  │     │  │  │     ├─ modeline.cpython-314.pyc
│  │     │  │  │     ├─ plugin.cpython-314.pyc
│  │     │  │  │     ├─ regexopt.cpython-314.pyc
│  │     │  │  │     ├─ scanner.cpython-314.pyc
│  │     │  │  │     ├─ sphinxext.cpython-314.pyc
│  │     │  │  │     ├─ style.cpython-314.pyc
│  │     │  │  │     ├─ token.cpython-314.pyc
│  │     │  │  │     ├─ unistring.cpython-314.pyc
│  │     │  │  │     ├─ util.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ pyproject_hooks
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ _impl.py
│  │     │  │  │  ├─ _in_process
│  │     │  │  │  │  ├─ _in_process.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ _in_process.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ _impl.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ README.rst
│  │     │  │  ├─ requests
│  │     │  │  │  ├─ adapters.py
│  │     │  │  │  ├─ api.py
│  │     │  │  │  ├─ auth.py
│  │     │  │  │  ├─ certs.py
│  │     │  │  │  ├─ compat.py
│  │     │  │  │  ├─ cookies.py
│  │     │  │  │  ├─ exceptions.py
│  │     │  │  │  ├─ help.py
│  │     │  │  │  ├─ hooks.py
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ models.py
│  │     │  │  │  ├─ packages.py
│  │     │  │  │  ├─ sessions.py
│  │     │  │  │  ├─ status_codes.py
│  │     │  │  │  ├─ structures.py
│  │     │  │  │  ├─ utils.py
│  │     │  │  │  ├─ _internal_utils.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __pycache__
│  │     │  │  │  │  ├─ adapters.cpython-314.pyc
│  │     │  │  │  │  ├─ api.cpython-314.pyc
│  │     │  │  │  │  ├─ auth.cpython-314.pyc
│  │     │  │  │  │  ├─ certs.cpython-314.pyc
│  │     │  │  │  │  ├─ compat.cpython-314.pyc
│  │     │  │  │  │  ├─ cookies.cpython-314.pyc
│  │     │  │  │  │  ├─ exceptions.cpython-314.pyc
│  │     │  │  │  │  ├─ help.cpython-314.pyc
│  │     │  │  │  │  ├─ hooks.cpython-314.pyc
│  │     │  │  │  │  ├─ models.cpython-314.pyc
│  │     │  │  │  │  ├─ packages.cpython-314.pyc
│  │     │  │  │  │  ├─ sessions.cpython-314.pyc
│  │     │  │  │  │  ├─ status_codes.cpython-314.pyc
│  │     │  │  │  │  ├─ structures.cpython-314.pyc
│  │     │  │  │  │  ├─ utils.cpython-314.pyc
│  │     │  │  │  │  ├─ _internal_utils.cpython-314.pyc
│  │     │  │  │  │  ├─ __init__.cpython-314.pyc
│  │     │  │  │  │  └─ __version__.cpython-314.pyc
│  │     │  │  │  └─ __version__.py
│  │     │  │  ├─ resolvelib
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ providers.py
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ reporters.py
│  │     │  │  │  ├─ resolvers
│  │     │  │  │  │  ├─ abstract.py
│  │     │  │  │  │  ├─ criterion.py
│  │     │  │  │  │  ├─ exceptions.py
│  │     │  │  │  │  ├─ resolution.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ abstract.cpython-314.pyc
│  │     │  │  │  │     ├─ criterion.cpython-314.pyc
│  │     │  │  │  │     ├─ exceptions.cpython-314.pyc
│  │     │  │  │  │     ├─ resolution.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ structs.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ providers.cpython-314.pyc
│  │     │  │  │     ├─ reporters.cpython-314.pyc
│  │     │  │  │     ├─ structs.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ rich
│  │     │  │  │  ├─ abc.py
│  │     │  │  │  ├─ align.py
│  │     │  │  │  ├─ ansi.py
│  │     │  │  │  ├─ bar.py
│  │     │  │  │  ├─ box.py
│  │     │  │  │  ├─ cells.py
│  │     │  │  │  ├─ color.py
│  │     │  │  │  ├─ color_triplet.py
│  │     │  │  │  ├─ columns.py
│  │     │  │  │  ├─ console.py
│  │     │  │  │  ├─ constrain.py
│  │     │  │  │  ├─ containers.py
│  │     │  │  │  ├─ control.py
│  │     │  │  │  ├─ default_styles.py
│  │     │  │  │  ├─ diagnose.py
│  │     │  │  │  ├─ emoji.py
│  │     │  │  │  ├─ errors.py
│  │     │  │  │  ├─ filesize.py
│  │     │  │  │  ├─ file_proxy.py
│  │     │  │  │  ├─ highlighter.py
│  │     │  │  │  ├─ json.py
│  │     │  │  │  ├─ jupyter.py
│  │     │  │  │  ├─ layout.py
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ live.py
│  │     │  │  │  ├─ live_render.py
│  │     │  │  │  ├─ logging.py
│  │     │  │  │  ├─ markup.py
│  │     │  │  │  ├─ measure.py
│  │     │  │  │  ├─ padding.py
│  │     │  │  │  ├─ pager.py
│  │     │  │  │  ├─ palette.py
│  │     │  │  │  ├─ panel.py
│  │     │  │  │  ├─ pretty.py
│  │     │  │  │  ├─ progress.py
│  │     │  │  │  ├─ progress_bar.py
│  │     │  │  │  ├─ prompt.py
│  │     │  │  │  ├─ protocol.py
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ region.py
│  │     │  │  │  ├─ repr.py
│  │     │  │  │  ├─ rule.py
│  │     │  │  │  ├─ scope.py
│  │     │  │  │  ├─ screen.py
│  │     │  │  │  ├─ segment.py
│  │     │  │  │  ├─ spinner.py
│  │     │  │  │  ├─ status.py
│  │     │  │  │  ├─ style.py
│  │     │  │  │  ├─ styled.py
│  │     │  │  │  ├─ syntax.py
│  │     │  │  │  ├─ table.py
│  │     │  │  │  ├─ terminal_theme.py
│  │     │  │  │  ├─ text.py
│  │     │  │  │  ├─ theme.py
│  │     │  │  │  ├─ themes.py
│  │     │  │  │  ├─ traceback.py
│  │     │  │  │  ├─ tree.py
│  │     │  │  │  ├─ _cell_widths.py
│  │     │  │  │  ├─ _emoji_codes.py
│  │     │  │  │  ├─ _emoji_replace.py
│  │     │  │  │  ├─ _export_format.py
│  │     │  │  │  ├─ _extension.py
│  │     │  │  │  ├─ _fileno.py
│  │     │  │  │  ├─ _inspect.py
│  │     │  │  │  ├─ _log_render.py
│  │     │  │  │  ├─ _loop.py
│  │     │  │  │  ├─ _null_file.py
│  │     │  │  │  ├─ _palettes.py
│  │     │  │  │  ├─ _pick.py
│  │     │  │  │  ├─ _ratio.py
│  │     │  │  │  ├─ _spinners.py
│  │     │  │  │  ├─ _stack.py
│  │     │  │  │  ├─ _timer.py
│  │     │  │  │  ├─ _win32_console.py
│  │     │  │  │  ├─ _windows.py
│  │     │  │  │  ├─ _windows_renderer.py
│  │     │  │  │  ├─ _wrap.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  ├─ __main__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ abc.cpython-314.pyc
│  │     │  │  │     ├─ align.cpython-314.pyc
│  │     │  │  │     ├─ ansi.cpython-314.pyc
│  │     │  │  │     ├─ bar.cpython-314.pyc
│  │     │  │  │     ├─ box.cpython-314.pyc
│  │     │  │  │     ├─ cells.cpython-314.pyc
│  │     │  │  │     ├─ color.cpython-314.pyc
│  │     │  │  │     ├─ color_triplet.cpython-314.pyc
│  │     │  │  │     ├─ columns.cpython-314.pyc
│  │     │  │  │     ├─ console.cpython-314.pyc
│  │     │  │  │     ├─ constrain.cpython-314.pyc
│  │     │  │  │     ├─ containers.cpython-314.pyc
│  │     │  │  │     ├─ control.cpython-314.pyc
│  │     │  │  │     ├─ default_styles.cpython-314.pyc
│  │     │  │  │     ├─ diagnose.cpython-314.pyc
│  │     │  │  │     ├─ emoji.cpython-314.pyc
│  │     │  │  │     ├─ errors.cpython-314.pyc
│  │     │  │  │     ├─ filesize.cpython-314.pyc
│  │     │  │  │     ├─ file_proxy.cpython-314.pyc
│  │     │  │  │     ├─ highlighter.cpython-314.pyc
│  │     │  │  │     ├─ json.cpython-314.pyc
│  │     │  │  │     ├─ jupyter.cpython-314.pyc
│  │     │  │  │     ├─ layout.cpython-314.pyc
│  │     │  │  │     ├─ live.cpython-314.pyc
│  │     │  │  │     ├─ live_render.cpython-314.pyc
│  │     │  │  │     ├─ logging.cpython-314.pyc
│  │     │  │  │     ├─ markup.cpython-314.pyc
│  │     │  │  │     ├─ measure.cpython-314.pyc
│  │     │  │  │     ├─ padding.cpython-314.pyc
│  │     │  │  │     ├─ pager.cpython-314.pyc
│  │     │  │  │     ├─ palette.cpython-314.pyc
│  │     │  │  │     ├─ panel.cpython-314.pyc
│  │     │  │  │     ├─ pretty.cpython-314.pyc
│  │     │  │  │     ├─ progress.cpython-314.pyc
│  │     │  │  │     ├─ progress_bar.cpython-314.pyc
│  │     │  │  │     ├─ prompt.cpython-314.pyc
│  │     │  │  │     ├─ protocol.cpython-314.pyc
│  │     │  │  │     ├─ region.cpython-314.pyc
│  │     │  │  │     ├─ repr.cpython-314.pyc
│  │     │  │  │     ├─ rule.cpython-314.pyc
│  │     │  │  │     ├─ scope.cpython-314.pyc
│  │     │  │  │     ├─ screen.cpython-314.pyc
│  │     │  │  │     ├─ segment.cpython-314.pyc
│  │     │  │  │     ├─ spinner.cpython-314.pyc
│  │     │  │  │     ├─ status.cpython-314.pyc
│  │     │  │  │     ├─ style.cpython-314.pyc
│  │     │  │  │     ├─ styled.cpython-314.pyc
│  │     │  │  │     ├─ syntax.cpython-314.pyc
│  │     │  │  │     ├─ table.cpython-314.pyc
│  │     │  │  │     ├─ terminal_theme.cpython-314.pyc
│  │     │  │  │     ├─ text.cpython-314.pyc
│  │     │  │  │     ├─ theme.cpython-314.pyc
│  │     │  │  │     ├─ themes.cpython-314.pyc
│  │     │  │  │     ├─ traceback.cpython-314.pyc
│  │     │  │  │     ├─ tree.cpython-314.pyc
│  │     │  │  │     ├─ _cell_widths.cpython-314.pyc
│  │     │  │  │     ├─ _emoji_codes.cpython-314.pyc
│  │     │  │  │     ├─ _emoji_replace.cpython-314.pyc
│  │     │  │  │     ├─ _export_format.cpython-314.pyc
│  │     │  │  │     ├─ _extension.cpython-314.pyc
│  │     │  │  │     ├─ _fileno.cpython-314.pyc
│  │     │  │  │     ├─ _inspect.cpython-314.pyc
│  │     │  │  │     ├─ _log_render.cpython-314.pyc
│  │     │  │  │     ├─ _loop.cpython-314.pyc
│  │     │  │  │     ├─ _null_file.cpython-314.pyc
│  │     │  │  │     ├─ _palettes.cpython-314.pyc
│  │     │  │  │     ├─ _pick.cpython-314.pyc
│  │     │  │  │     ├─ _ratio.cpython-314.pyc
│  │     │  │  │     ├─ _spinners.cpython-314.pyc
│  │     │  │  │     ├─ _stack.cpython-314.pyc
│  │     │  │  │     ├─ _timer.cpython-314.pyc
│  │     │  │  │     ├─ _win32_console.cpython-314.pyc
│  │     │  │  │     ├─ _windows.cpython-314.pyc
│  │     │  │  │     ├─ _windows_renderer.cpython-314.pyc
│  │     │  │  │     ├─ _wrap.cpython-314.pyc
│  │     │  │  │     ├─ __init__.cpython-314.pyc
│  │     │  │  │     └─ __main__.cpython-314.pyc
│  │     │  │  ├─ tomli
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ _parser.py
│  │     │  │  │  ├─ _re.py
│  │     │  │  │  ├─ _types.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ _parser.cpython-314.pyc
│  │     │  │  │     ├─ _re.cpython-314.pyc
│  │     │  │  │     ├─ _types.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ tomli_w
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ _writer.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ _writer.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ truststore
│  │     │  │  │  ├─ LICENSE
│  │     │  │  │  ├─ py.typed
│  │     │  │  │  ├─ _api.py
│  │     │  │  │  ├─ _macos.py
│  │     │  │  │  ├─ _openssl.py
│  │     │  │  │  ├─ _ssl_constants.py
│  │     │  │  │  ├─ _windows.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ _api.cpython-314.pyc
│  │     │  │  │     ├─ _macos.cpython-314.pyc
│  │     │  │  │     ├─ _openssl.cpython-314.pyc
│  │     │  │  │     ├─ _ssl_constants.cpython-314.pyc
│  │     │  │  │     ├─ _windows.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ urllib3
│  │     │  │  │  ├─ connection.py
│  │     │  │  │  ├─ connectionpool.py
│  │     │  │  │  ├─ contrib
│  │     │  │  │  │  ├─ appengine.py
│  │     │  │  │  │  ├─ ntlmpool.py
│  │     │  │  │  │  ├─ pyopenssl.py
│  │     │  │  │  │  ├─ securetransport.py
│  │     │  │  │  │  ├─ socks.py
│  │     │  │  │  │  ├─ _appengine_environ.py
│  │     │  │  │  │  ├─ _securetransport
│  │     │  │  │  │  │  ├─ bindings.py
│  │     │  │  │  │  │  ├─ low_level.py
│  │     │  │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  │  └─ __pycache__
│  │     │  │  │  │  │     ├─ bindings.cpython-314.pyc
│  │     │  │  │  │  │     ├─ low_level.cpython-314.pyc
│  │     │  │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ appengine.cpython-314.pyc
│  │     │  │  │  │     ├─ ntlmpool.cpython-314.pyc
│  │     │  │  │  │     ├─ pyopenssl.cpython-314.pyc
│  │     │  │  │  │     ├─ securetransport.cpython-314.pyc
│  │     │  │  │  │     ├─ socks.cpython-314.pyc
│  │     │  │  │  │     ├─ _appengine_environ.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ exceptions.py
│  │     │  │  │  ├─ fields.py
│  │     │  │  │  ├─ filepost.py
│  │     │  │  │  ├─ LICENSE.txt
│  │     │  │  │  ├─ packages
│  │     │  │  │  │  ├─ backports
│  │     │  │  │  │  │  ├─ makefile.py
│  │     │  │  │  │  │  ├─ weakref_finalize.py
│  │     │  │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  │  └─ __pycache__
│  │     │  │  │  │  │     ├─ makefile.cpython-314.pyc
│  │     │  │  │  │  │     ├─ weakref_finalize.cpython-314.pyc
│  │     │  │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  │  ├─ six.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ six.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ poolmanager.py
│  │     │  │  │  ├─ request.py
│  │     │  │  │  ├─ response.py
│  │     │  │  │  ├─ util
│  │     │  │  │  │  ├─ connection.py
│  │     │  │  │  │  ├─ proxy.py
│  │     │  │  │  │  ├─ queue.py
│  │     │  │  │  │  ├─ request.py
│  │     │  │  │  │  ├─ response.py
│  │     │  │  │  │  ├─ retry.py
│  │     │  │  │  │  ├─ ssltransport.py
│  │     │  │  │  │  ├─ ssl_.py
│  │     │  │  │  │  ├─ ssl_match_hostname.py
│  │     │  │  │  │  ├─ timeout.py
│  │     │  │  │  │  ├─ url.py
│  │     │  │  │  │  ├─ wait.py
│  │     │  │  │  │  ├─ __init__.py
│  │     │  │  │  │  └─ __pycache__
│  │     │  │  │  │     ├─ connection.cpython-314.pyc
│  │     │  │  │  │     ├─ proxy.cpython-314.pyc
│  │     │  │  │  │     ├─ queue.cpython-314.pyc
│  │     │  │  │  │     ├─ request.cpython-314.pyc
│  │     │  │  │  │     ├─ response.cpython-314.pyc
│  │     │  │  │  │     ├─ retry.cpython-314.pyc
│  │     │  │  │  │     ├─ ssltransport.cpython-314.pyc
│  │     │  │  │  │     ├─ ssl_.cpython-314.pyc
│  │     │  │  │  │     ├─ ssl_match_hostname.cpython-314.pyc
│  │     │  │  │  │     ├─ timeout.cpython-314.pyc
│  │     │  │  │  │     ├─ url.cpython-314.pyc
│  │     │  │  │  │     ├─ wait.cpython-314.pyc
│  │     │  │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  │  ├─ _collections.py
│  │     │  │  │  ├─ _version.py
│  │     │  │  │  ├─ __init__.py
│  │     │  │  │  └─ __pycache__
│  │     │  │  │     ├─ connection.cpython-314.pyc
│  │     │  │  │     ├─ connectionpool.cpython-314.pyc
│  │     │  │  │     ├─ exceptions.cpython-314.pyc
│  │     │  │  │     ├─ fields.cpython-314.pyc
│  │     │  │  │     ├─ filepost.cpython-314.pyc
│  │     │  │  │     ├─ poolmanager.cpython-314.pyc
│  │     │  │  │     ├─ request.cpython-314.pyc
│  │     │  │  │     ├─ response.cpython-314.pyc
│  │     │  │  │     ├─ _collections.cpython-314.pyc
│  │     │  │  │     ├─ _version.cpython-314.pyc
│  │     │  │  │     └─ __init__.cpython-314.pyc
│  │     │  │  ├─ vendor.txt
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     └─ __init__.cpython-314.pyc
│  │     │  ├─ __init__.py
│  │     │  ├─ __main__.py
│  │     │  ├─ __pip-runner__.py
│  │     │  └─ __pycache__
│  │     │     ├─ __init__.cpython-314.pyc
│  │     │     ├─ __main__.cpython-314.pyc
│  │     │     └─ __pip-runner__.cpython-314.pyc
│  │     └─ pip-26.0.1.dist-info
│  │        ├─ entry_points.txt
│  │        ├─ INSTALLER
│  │        ├─ licenses
│  │        │  ├─ AUTHORS.txt
│  │        │  ├─ LICENSE.txt
│  │        │  └─ src
│  │        │     └─ pip
│  │        │        └─ _vendor
│  │        │           ├─ cachecontrol
│  │        │           │  └─ LICENSE.txt
│  │        │           ├─ certifi
│  │        │           │  └─ LICENSE
│  │        │           ├─ dependency_groups
│  │        │           │  └─ LICENSE.txt
│  │        │           ├─ distlib
│  │        │           │  └─ LICENSE.txt
│  │        │           ├─ distro
│  │        │           │  └─ LICENSE
│  │        │           ├─ idna
│  │        │           │  └─ LICENSE.md
│  │        │           ├─ msgpack
│  │        │           │  └─ COPYING
│  │        │           ├─ packaging
│  │        │           │  ├─ LICENSE
│  │        │           │  ├─ LICENSE.APACHE
│  │        │           │  └─ LICENSE.BSD
│  │        │           ├─ pkg_resources
│  │        │           │  └─ LICENSE
│  │        │           ├─ platformdirs
│  │        │           │  └─ LICENSE
│  │        │           ├─ pygments
│  │        │           │  └─ LICENSE
│  │        │           ├─ pyproject_hooks
│  │        │           │  └─ LICENSE
│  │        │           ├─ requests
│  │        │           │  └─ LICENSE
│  │        │           ├─ resolvelib
│  │        │           │  └─ LICENSE
│  │        │           ├─ rich
│  │        │           │  └─ LICENSE
│  │        │           ├─ tomli
│  │        │           │  └─ LICENSE
│  │        │           ├─ tomli_w
│  │        │           │  └─ LICENSE
│  │        │           ├─ truststore
│  │        │           │  └─ LICENSE
│  │        │           └─ urllib3
│  │        │              └─ LICENSE.txt
│  │        ├─ METADATA
│  │        ├─ RECORD
│  │        ├─ REQUESTED
│  │        └─ WHEEL
│  ├─ pyvenv.cfg
│  └─ Scripts
│     ├─ activate
│     ├─ activate.bat
│     ├─ activate.fish
│     ├─ Activate.ps1
│     ├─ deactivate.bat
│     ├─ pip.exe
│     ├─ pip3.14.exe
│     ├─ pip3.exe
│     ├─ python.exe
│     └─ pythonw.exe
├─ analyzer_spacehack.py
├─ auditor.py
├─ auditor_final.py
├─ audit_NL_RTM.json
├─ audit_US_LGB.json
├─ check_csv.py
├─ dashboard_ejecutivo.png
├─ datasets
│  ├─ pub150.csv
│  └─ transporte.csv
├─ diagnostico.py
├─ ESTRUCTURA_FINAL.md
├─ generar_flota.py
├─ grafico_distribucion_tamaño.png
├─ grafico_emisiones_barco.png
├─ grafico_mega_puertos.png
├─ grafico_servicios_eco.png
├─ insights
│  ├─ emisiones_por_barco.csv
│  ├─ mega_puertos.csv
│  ├─ puertos_eco.csv
│  └─ top_50_puertos.csv
├─ README.md
├─ reporte_ejecutivo.txt
├─ tabla_mega_puertos.png
├─ tabla_puertos_eco.png
├─ uso_datos_puertos.py
├─ visualizaciones.py
└─ __pycache__
   ├─ analyzer_spacehack.cpython-314.pyc
   └─ auditor_final.cpython-314.pyc

```#   P r o y e c t o S p a c e H a c k  
 
# Prueba Técnica — Ingeniero(a) de IA/Datos y Soporte (Junior) — Salva Health

Análisis y modelado sobre un dataset clínico de pacientes con señales ECG, orientado a predecir si un electrocardiograma es Normal o Anormal. 
El proyecto cubre limpieza y versionamiento de datos, análisis exploratorio (incluyendo la señal ECG cruda), ingeniería de
características y un modelo baseline de clasificación (Regresión Logística).

## Contenido

- **Calidad de datos**: detección y tratamiento de nulos, duplicados, valores imposibles y
  formatos de fecha inconsistentes, con versionamiento de cada etapa (`data/v1_raw`,`data/v2_clean`,`data/v3_features`).
- **EDA**: análisis de variables clínicas y de la señal ECG cruda (250 Hz, 10s por paciente), incluyendo verificación de consistencia de la señal y comparación de variables por grupo.
- **Feature engineering**: cálculo de IMC y desviación estándar de la señal (`std_mV`).
- **Modelado**: Regresión Logística con `class_weight='balanced'`, evaluada con precision, recall, F1 y AUC-ROC, y comparada contra el dataset sin limpiar.
- **Reporte técnico**: `reports/Prueba_Técnica_Salva_Health.pdf`, con metodología, decisiones, limitaciones y trabajo futuro.

## Cómo correrlo

### 1. Requisitos previos
- Python 3.10+
- Una cuenta de Azure Storage.

### 2. Instalación
```
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Variables de entorno
Crea un archivo `.env` en la raíz del proyecto con la cadena de conexión a Azure Storage:
AZURE_CONNECTION_STRING=<tu_connection_string>

### 4. Ejecución
Los notebooks deben correrse en orden, desde la carpeta `notebooks/`:

1. `01_data_quality.ipynb` — carga el dataset crudo, aplica limpieza y genera `data/v2_clean`.
2. `02_exploratory_data_analysis.ipynb` — EDA de variables clínicas y de señal ECG.
3. `03_feature_engineering.ipynb` — calcula IMC y `std_mV`, genera `data/v3_features`.
4. `04_modeling.ipynb` — entrena y evalúa el modelo baseline, compara dataset limpio vs. crudo.

Las señales ECG (`data/v1_raw/senales/`) se leen localmente por paciente (`id_paciente.csv`); el
resto de los datasets tabulares se consumen desde Azure Storage.

## Estructura del repositorio
Buscando la mantenibilidad del código se separaron las responsabilidades. Es por esto que los notebooks están separados según su función, además
en la carpeta src se encuentra con diferentes utils ya que se busca reutilizar funciones, como por ejemplo de limpieza o validación a lo largo
de todo el proyecto. Además, se cuenta con archivos como constants o enum para reducir la cantidad de texto hardcodeado en el código y que este sea 
más fácil de mantener.
├── data
│   ├── README_VERSIONING.md
│   ├── v1_raw
│   │   ├── pacientes.csv
│   │   └── senales
│   ├── v2_clean
│   │   ├── pacientes_clean.csv
│   │   ├── pacientes_clean_metadata.json
│   │   └── version_changes.json
│   └── v3_features
│       ├── pacientes_features.csv
│       ├── pacientes_features_metadata.json
│       └── version_changes.json
├── notebooks
│   ├── 01_data_quality.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modeling.ipynb
├── reports
│   └── Prueba_Técnica_Salva_Health.pdf
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── cloud_storage.py
│   ├── constants.py
│   ├── data_quality.py
│   ├── data_versioning.py
│   ├── eda_utils.py
│   ├── enums.py
│   ├── modeling_utils.py
│   └── outlier_detection.py

"""
Constants and text messages used across the project.
"""

from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.environ.get('AZURE_CONNECTION_STRING')

PATHS_PROJECT = {
    'signals': '../data/v1_raw/senales/',
    'v2': '../data/v2_clean/version_changes.json',
    'v3': '../data/v3_features/version_changes.json',
    'readme': '../data/README_VERSIONING.md'
}

VALIDATION_MESSAGES = {
    'file_not_found': 'File not found: {}',
    'directory_created': 'Directory created: {}',
    'version_saved': 'Version {} saved to: {}',
    'records_info': 'Records: {}',
    'columns_info': 'Columns: {}',
}

TRANSFORMATION_DESCRIPTIONS = {
    'missing_values': {
        'name': 'Missing values',
        'description': 'Removed records with null values in any column',
        'justification': 'Nulls represented less than 4% of total; removal avoids introducing assumptions'
    },
    'invalid_ages': {
        'name': 'Invalid ages',
        'description': 'Removed negative ages and ages > 120 years',
        'justification': 'Clinically impossible values, suggest data entry errors'
    },
    'duplicates': {
        'name': 'Duplicate records',
        'description': 'Removed duplicate records',
        'justification': 'Patient ID must be unique'
    },
    'date_standardization': {
        'name': 'Date standardization',
        'description': 'Converted all dates to datetime format (YYYY-MM-DD)',
        'justification': 'Inconsistent formats prevented temporal analysis'
    },
    'outlier_removal': {
        'name': 'Outlier removal',
        'description': 'Removed multivariate outliers using Mahalanobis distance',
        'justification': 'Multivariate outliers could distort the model. Heart rate outliers were retained due to potential clinical relevance.'
    },
    'feature_engineering': {
        'name': 'Feature engineering',
        'description': 'Added IMC (Body Mass Index) calculated from weight and height',
        'justification': 'IMC is a clinically relevant indicator of body composition'
    },
    'ecg_features': {
        'name': 'ECG signal features',
        'description': 'Added std_mv (standard deviation of ECG signal)',
        'justification': 'Captures variability in the ECG signal, which may differ between Normal and Anormal patients'
    }
}

COLUMNS = {
    'patient_id': 'id_paciente',
    'age': 'edad_paciente',
    'sex': 'sexo',
    'weight': 'peso_kg',
    'height': 'altura_cm',
    'date': 'fecha_registro',
    'heart_rate': 'frecuencia_cardiaca_media_bpm',
    'ecg_lead': 'derivacion_ecg',
    'sampling_rate': 'frecuencia_muestreo_hz',
    'label': 'etiqueta',
    'imc': 'imc',
    'std_mv': 'std_mV',
}
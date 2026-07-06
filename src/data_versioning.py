"""
Data versioning utilities.

This module provides functions to version datasets and document changes
between versions, ensuring traceability of data transformations.
"""

import os
import json
from datetime import datetime


def ensure_directory(path):
    """
    Create directory if it does not exist.
    
    path(str) : Directory path to create
    """
    os.makedirs(path, exist_ok=True)


def save_clean_dataset(df, filepath, metadata=None):
    """
    Save cleaned dataset and optional metadata.

    df(pandas.DataFrame) : Cleaned dataset
    filepath(str) : Path where the CSV will be saved
    metadata(dict, optional) : Metadata to save alongside the dataset
    """
    ensure_directory(os.path.dirname(filepath))
    df.to_csv(filepath, index=False)
    
    if metadata:
        metadata_path = filepath.replace('.csv', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)


def create_version_changes(original_records, cleaned_records, transformations):
    """
    Create version change documentation.

    original_records(int) : Number of records in original dataset
    cleaned_records(int) : Number of records in cleaned dataset
    transformations(list of dict) : List of transformation steps with description and justification
    
    Returns:
    dict : Version change documentation
    """
    return {
        'version_from': '1.0',
        'version_to': '2.0',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {
            'original_records': original_records,
            'cleaned_records': cleaned_records,
            'records_removed': original_records - cleaned_records,
            'removal_percentage': round(((original_records - cleaned_records) / original_records) * 100, 2)
        },
        'transformations': transformations
    }


def save_version_changes(changes, filepath):
    """
    Save version changes to JSON file.
    
    changes(dict) : Version change documentation
    filepath(str) : Path where the JSON will be saved
    """
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        json.dump(changes, f, indent=2)


def create_versioning_readme(output_path, versions_info):
    """
    Create README file documenting all dataset versions.

    output_path(str) : Path where the README will be saved
    versions_info(dict) : Information about each version
    """
    ensure_directory(os.path.dirname(output_path))
    
    content = """# Data Versioning

This document describes the different versions of the dataset used in this project.

## Version 1.0 - Raw Data
- **Location**: `v1_raw/`
- **File**: `pacientes.csv`
- **Records**: 515
- **Description**: Original dataset as received, without any modifications.
- **Signals**: `senales/` directory contains ECG signals for each patient.

## Version 2.0 - Clean Data
- **Location**: `v2_clean/`
- **File**: `pacientes_clean.csv`
- **Records**: {clean_records}
- **Description**: Dataset after quality corrections.
- **Transformations**: See `version_changes.json` for complete details.

## Version 3.0 - Feature Engineered Data
- **Location**: `v3_features/`
- **Status**: Pending
- **Description**: Pending
"""
    
    with open(output_path, 'w') as f:
        f.write(content.format(**versions_info))
# Data Versioning

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
- **Records**: 475
- **Description**: Dataset after quality corrections.
- **Transformations**: See `version_changes.json` for complete details.

## Version 3.0 - Feature Engineered Data
- **Location**: `v3_features/`
- - **File**: `pacientes_features.csv`
- **Records**: 475
- **Description**: Dataset with derived variables and ECG signal features.
- **Transformations**: See `version_changes.json` for complete details.

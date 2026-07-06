"""
Enumerations and catalog values used across the project.
"""
from enum import Enum

class Month(str, Enum):
    """Month name to number mapping."""
    JANUARY = "01"
    FEBRUARY = "02"
    MARCH = "03"
    APRIL = "04"
    MAY = "05"
    JUNE = "06"
    JULY = "07"
    AUGUST = "08"
    SEPTEMBER = "09"
    OCTOBER = "10"
    NOVEMBER = "11"
    DECEMBER = "12"

    @classmethod
    def to_dict(cls):
        return {month.name.capitalize(): month.value for month in cls}

class AgeLimits:
    """Age validation limits."""
    MIN = 0
    MAX = 120

class OutlierConfig:
    """Outlier detection configuration."""
    QUANTILE = 0.995

class DataVersion:
    """Data version constants."""
    ORIGINAL_RECORDS = 515
    RAW_PATH = '../data/v1_raw/pacientes.csv'
    CLEAN_FILE = '../data/v2_clean/pacientes_clean.csv'
    FEATURES_FILE = '../data/v3_features/pacientes_features.csv'
"""
Source code utilities.
"""

from .enums import Month, AgeLimits, OutlierConfig, DataVersion
from .constants import COLUMNS, TRANSFORMATION_DESCRIPTIONS, PATHS_PROJECT
from .data_quality import (
    fix_date,
    standardize_dates,
    get_missing_values_report,
    remove_missing_values,
    remove_duplicates,
    filter_age,
    print_unique_values,
    print_multiple_unique_values,
    compare_mean_median,
    get_duplicate_report,
)
from .outlier_detection import (
    detect_multivariate_outliers,
    remove_multivariate_outliers,
    plot_combined_boxplots,
    plot_scatter_with_outliers
)
from .data_versioning import (
    ensure_directory,
    save_clean_dataset,
    create_version_changes,
    save_version_changes,
    create_versioning_readme
)
from .cloud_storage import (
    upload_csv_to_azure, 
    read_csv_from_azure
)
from .eda_utils import (
    get_categorical_summary,
    get_numerical_summary,
    plot_categorical_distribution,
    plot_numerical_distribution,
    plot_correlation_heatmap,
    get_signal_summary,
    plot_ecg_examples,
    plot_box_grid,
    load_ecg_signal,
)
from .modeling_utils import (
    load_patient_dataset,
    prepare_dataset_for_modeling,
    plot_confusion_matrix,
    prepare_features,
    train_and_evaluate,
    plot_error_by_quantile_bar
)

__all__ = [
    # enums
    'Month',
    'AgeLimits',
    'OutlierConfig',
    'DataVersion',
    # constants
    'COLUMNS',
    'TRANSFORMATION_DESCRIPTIONS',
    'PATHS_PROJECT',
    # data_quality
    'fix_date',
    'standardize_dates',
    'get_missing_values_report',
    'remove_missing_values',
    'remove_duplicates',
    'filter_age',
    'compare_mean_median',
    'print_unique_values',
    'print_multiple_unique_values',
    'get_duplicate_report',
    # outlier_detection
    'detect_multivariate_outliers',
    'remove_multivariate_outliers',
    'plot_combined_boxplots',
    'plot_scatter_with_outliers',
    # data_versioning
    'ensure_directory',
    'copy_raw_data',
    'save_clean_dataset',
    'create_version_changes',
    'save_version_changes',
    'create_versioning_readme',
    # cloud_storage
    'upload_csv_to_azure',
    'read_csv_from_azure',
    # eda_utils
    'get_categorical_summary',
    'get_numerical_summary',
    'plot_categorical_distribution',
    'plot_numerical_distribution',
    'plot_correlation_heatmap',
    'get_signal_summary',
    'plot_ecg_examples',
    'plot_box_grid',
    'load_ecg_signal',
    # modeling_utils
    'load_patient_dataset',
    'prepare_dataset_for_modeling',
    'plot_confusion_matrix',
    'plot_error_by_quantile_bar',
    'prepare_features',
    'train_and_evaluate'
]
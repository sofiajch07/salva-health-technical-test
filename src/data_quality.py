"""
Data quality utilities for cleaning and validation.
"""

import pandas as pd
from src.enums import Month, AgeLimits

def fix_date(date_str):
    """
    Convert various date formats to YYYY-MM-DD.
    
    Supported formats:
    - 2023-10-04 -> 2023-10-04
    - 27/01/2023 -> 2023-01-27
    - June 09, 2023 -> 2023-06-09
    """
    date_str = date_str.strip().strip('"')
    
    # Format 1: YYYY-MM-DD
    if '-' in date_str and len(date_str) == 10:
        return date_str
    
    # Format 2: DD/MM/YYYY
    if '/' in date_str:
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    
    # Format 3: Month DD, YYYY
    months = Month.to_dict()
    for month_name, month_num in months.items():
        if month_name in date_str:
            parts = date_str.replace(',', '').split()
            day = parts[1].zfill(2)
            year = parts[2]
            return f"{year}-{month_num}-{day}"
    
    return date_str


def standardize_dates(df, column_name):
    """
    Apply date standardization to a column.
    
    df(pandas.DataFrame): DataFrame containing the date column
    column_name(str): Name of the column to standardize
    
    Returns:
    pandas.DataFrame : DataFrame with standardized dates
    """
    df = df.copy()
    df[column_name] = df[column_name].apply(fix_date)
    df[column_name] = pd.to_datetime(df[column_name])
    return df


def get_duplicate_report(df):
    """
    Generate duplicate records report.
    """
    total_duplicates = df.duplicated().sum()
    return {
        'total_duplicates': total_duplicates,
        'duplicate_percentage': (total_duplicates / len(df)) * 100
    }


def get_missing_values_report(df):
    """
    Generate missing values report.
    
    df(pandas.DataFrame)
    
    Returns:
    pandas.DataFrame : Report with missing counts and percentages
    """
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    report = pd.DataFrame({
        'Column': missing_count.index,
        'Missing_Count': missing_count.values,
        'Percentage': missing_percent.values
    })
    return report[report['Missing_Count'] > 0]


def remove_missing_values(df, subset=None):
    """
    Remove rows with missing values.

    df(pandas.DataFrame): DataFrame containing the data
    subset(list, optional): Columns to check for nulls. If None, checks all columns.
    
    Returns:
    pandas.DataFrame : DataFrame with missing values removed
    """
    return df.dropna(subset=subset)


def remove_duplicates(df, subset=None, keep='first'):
    """
    Remove duplicate rows.
    
    df(pandas.DataFrame): DataFrame containing the data
    subset(list, optional): Columns to check for duplicates
    keep(str, default 'first'): Which duplicate to keep
    
    Returns:
    pandas.DataFrame : DataFrame with duplicates removed
    """
    return df.drop_duplicates(subset=subset, keep=keep)


def filter_age(df, age_column='edad_paciente'):
    """
    Filter ages to valid range.

    df(pandas.DataFrame): DataFrame containing the data
    age_column(str): Name of the age column

    Returns:
    pandas.DataFrame : DataFrame with valid ages
    """
    return df.query(
        f'{age_column} <= {AgeLimits.MAX} and {age_column} >= {AgeLimits.MIN}'
    )

def print_unique_values(df, column_name, column_label=None):
    """
    Print unique values of a column with a descriptive label.
    
    df(pandas.DataFrame): DataFrame containing the column
    column_name (str): Name of the column to inspect
    column_label (str, optional): Descriptive label to print. If None, uses column_name.
    
    Returns:
    None
    """
    if column_label is None:
        column_label = column_name
    
    unique_vals = df[column_name].unique()
    print(f"{column_label} unique values: {unique_vals}")
    print(f"Number of unique values: {len(unique_vals)}")

def compare_mean_median(df, columns):
    """
    Compare mean and median for multiple columns.
    
    df (pandas.DataFrame): DataFrame containing the data
    columns (list): List of column names to compare
    
    Returns:
    pandas.DataFrame : Comparison table
    """
    comparison = []
    for col in columns:
        mean_val = df[col].mean()
        median_val = df[col].median()
        diff = mean_val - median_val
        
        comparison.append({
            'Variable': col,
            'Media': round(mean_val, 2),
            'Mediana': round(median_val, 2),
            'Diferencia': round(diff, 2)
        })
    
    return pd.DataFrame(comparison)

def print_multiple_unique_values(df, columns_with_labels):
    """
    Print unique values for multiple columns.
    
    df(pandas.DataFrame): DataFrame containing the columns
    columns_with_labels (list of tuples): List of (column_name, label) tuples
    
    Returns:
    None
    """
    for column_name, label in columns_with_labels:
        print_unique_values(df, column_name, label)
        print("-" * 40)
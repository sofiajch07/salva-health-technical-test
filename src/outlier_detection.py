"""
Outlier detection utilities.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

from src.enums import OutlierConfig

def detect_multivariate_outliers(df, columns, quantile=OutlierConfig.QUANTILE):
    """
    Detect multivariate outliers using Mahalanobis distance.

    df(pandas.DataFrame): DataFrame containing the data
    columns(list): Column names to use for outlier detection
    quantile(float): Quantile for chi-square cutoff
    
    Returns:
    tuple : (DataFrame with outliers, mask)
        - DataFrame: Original data with outlier flag
        - ndarray: Boolean mask (True = outlier)
    """
    data = df[columns].values
    
    # Calculate covariance and mean
    covariance = np.cov(data, rowvar=False)
    covariance_inv = np.linalg.matrix_power(covariance, -1)
    center = np.mean(data, axis=0)
    
    # Calculate Mahalanobis distances
    distances = []
    for point in data:
        diff = point - center
        distance = diff.T.dot(covariance_inv).dot(diff)
        distances.append(distance)
    distances = np.array(distances)
    
    # Calculate cutoff
    degrees = len(columns)
    cutoff = chi2.ppf(quantile, degrees)
    
    # Create outlier mask
    outlier_mask = distances > cutoff
    
    # Create result DataFrame
    result = df.copy()
    result['mahalanobis_distance'] = distances
    result['is_outlier'] = outlier_mask
    
    return result, outlier_mask


def remove_multivariate_outliers(df, columns, quantile=OutlierConfig.QUANTILE):
    """
    Remove multivariate outliers from DataFrame.
    
    df(pandas.DataFrame): DataFrame containing the data
    columns(list): Column names to use for outlier detection
    quantile(float): Quantile for chi-square cutoff
    
    Returns:
    pandas.DataFrame : DataFrame without outliers
    """
    _, outlier_mask = detect_multivariate_outliers(df, columns, quantile)
    return df[~outlier_mask]


def plot_combined_boxplots(df, columns, figsize=(12, 10)):
    """
    Create boxplots for multiple variables in a grid.
    
    df(pandas.DataFrame): DataFrame containing the data
    columns(list): Column names to plot
    figsize(tuple, default (12, 10)): Figure size
    
    Returns:
    matplotlib.figure.Figure
    """
    n_cols = 2
    n_rows = (len(columns) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    for i, col in enumerate(columns):
        axes[i].boxplot(df[col].dropna())
        axes[i].set_title(f'Boxplot: {col}')
        axes[i].set_ylabel(col)
    
    # Hide unused subplots
    for j in range(len(columns), len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    return fig


def plot_scatter_with_outliers(df, x_col, y_col, outlier_mask=None, figsize=(8, 6)):
    """
    Create scatter plot with outliers highlighted.

    df(pandas.DataFrame): DataFrame containing the data
    x_col(str): Column name for x-axis
    y_col(str): Column name for y-axis
    outlier_mask(array-like, optional):
        Boolean mask for outliers (True = outlier)
    figsize(tuple, default (8, 6)): Figure size

    Returns:
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if outlier_mask is not None:
        # Plot non-outliers
        ax.scatter(
            df[~outlier_mask][x_col],
            df[~outlier_mask][y_col],
            label='Normal'
        )
        # Plot outliers
        ax.scatter(
            df[outlier_mask][x_col],
            df[outlier_mask][y_col],
            color='red',
            label='Outlier'
        )
        ax.legend()
    else:
        ax.scatter(df[x_col], df[y_col])
    
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f'Scatter plot: {x_col} vs {y_col}')
    
    plt.tight_layout()
    return fig
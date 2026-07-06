"""
EDA utilities for exploratory data analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


def get_categorical_summary(df, column):
    """
    Generate frequency and percentage summary for a categorical variable.
    
    Returns:
    pandas.DataFrame: Frequency and percentage table
    """
    counts = df[column].value_counts()
    percentages = df[column].value_counts(normalize=True) * 100
    
    summary = pd.DataFrame({
        'Category': counts.index,
        'Frequency': counts.values,
        'Percentage': percentages.values.round(1)
    })
    return summary


def get_numerical_summary(df, column):
    """
    Generate statistical summary for a numerical variable.
    
    Returns:
    pandas.DataFrame: Descriptive statistics
    """
    return df[column].describe().round(2)


def plot_categorical_distribution(df, column, title=None, ax=None):
    """
    Plot distribution of a categorical variable.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    sns.barplot(data=counts, x=column, y='count', ax=ax, palette='Set2')
    
    ax.set_title(title or f'Distribución de {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frecuencia')
    
    for i, v in enumerate(counts['count']):
        ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    return ax


def plot_numerical_distribution(df, column, title=None, ax=None, bins=20):
    """
    Plot histogram and KDE of a numerical variable.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    
    sns.histplot(data=df, x=column, bins=bins, kde=True, ax=ax)
    
    ax.set_title(title or f'Distribución de {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frecuencia')
    
    return ax


def plot_correlation_heatmap(df, columns, title=None, figsize=(10, 8)):
    """
    Plot correlation matrix heatmap.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    corr_matrix = df[columns].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, ax=ax, cbar_kws={'shrink': 0.8})
    
    ax.set_title(title or 'Matriz de Correlación')
    plt.tight_layout()
    return fig

def load_ecg_signal(patient_id, signals_path):
    """
    Load the ECG signal for a single patient.

    Returns:
    pandas.DataFrame: columns t_seg, ecg_mV
    """
    return pd.read_csv(f"{signals_path}{patient_id}.csv")


def get_signal_summary(patient_id, signals_path):
    """
    Compute basic descriptors for a patient's ECG signal.

    Returns:
    dict: n_samples, duration_seg, sampling_rate_hz, std_mV, range_mV
    """
    signal = load_ecg_signal(patient_id, signals_path)
    dt = signal['t_seg'].diff().median() # periodo de muestreo
    return {
        'id_paciente': patient_id,
        'n_samples': len(signal),
        'duration_seg': round(signal['t_seg'].iloc[-1], 3),
        'sampling_rate_hz': round(1 / dt) if dt else None, # frecuencia muestreo
        'std_mV': round(signal['ecg_mV'].std(), 4), # desviación estándar
        'range_mV': round(signal['ecg_mV'].max() - signal['ecg_mV'].min(), 4), # maxima varianza menos mínima
    }


def plot_ecg_examples(df, signals_path, label_col, id_col, n_per_class=2):
    """
    Plot example ECG signals for each label class.
    """
    labels = df[label_col].unique() # Normal y anormal
    fig, axes = plt.subplots(len(labels), n_per_class, figsize=(14, 3 * len(labels)), squeeze=False) # muestra aleatoria

    for row, label in enumerate(labels):
        sample_ids = df.loc[df[label_col] == label, id_col].sample(n_per_class, random_state=42)
        for col, patient_id in enumerate(sample_ids):
            signal = load_ecg_signal(patient_id, signals_path)
            ax = axes[row, col]
            ax.plot(signal['t_seg'], signal['ecg_mV'])
            ax.set_title(f'{label} — {patient_id}')
            ax.set_xlabel('Tiempo (s)')
            ax.set_ylabel('ECG (mV)') 

    plt.tight_layout()
    return fig

def plot_box_grid(df, specs, ncols=2, figsize=None):
    """
    Plot a grid of boxplots from a list of specs.

    specs(list of dict): Each dict needs: num_col, cat_col, title.
    Optional: hue_col, xlabel, ylabel.
    """
    n = len(specs)
    nrows = math.ceil(n / ncols)
    if figsize is None:
        figsize = (7 * ncols, 6 * nrows)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
    axes_flat = axes.flatten()

    for ax, spec in zip(axes_flat, specs):
        hue_col = spec.get('hue_col')
        if hue_col:
            sns.boxplot(data=df, x=spec['cat_col'], y=spec['num_col'], hue=hue_col, ax=ax, palette='Set2')
            ax.legend(title=hue_col)
        else:
            sns.boxplot(data=df, x=spec['cat_col'], y=spec['num_col'], ax=ax, color=sns.color_palette('Set2')[0])

        ax.set_title(spec['title'])
        ax.set_xlabel(spec.get('xlabel', spec['cat_col']))
        ax.set_ylabel(spec.get('ylabel', spec['num_col']))

    for ax in axes_flat[n:]:
        ax.axis('off')

    plt.tight_layout()
    return fig
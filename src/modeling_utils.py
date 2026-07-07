"""
Modeling utilities: data loading, evaluation plots for the classification model.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.base import clone
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

from src.constants import connection_string, COLUMNS, PATHS_PROJECT, NORMAL, ANORMAL
from src.cloud_storage import read_csv_from_azure
from src.eda_utils import get_signal_summary


def load_patient_dataset(container, filename):
    """
    Load the patient dataset from Azure Storage for modeling.

    container(str): Container name in Azure Storage
    filename(str): File name in the container

    Returns:
    pandas.DataFrame
    """
    return read_csv_from_azure(connection_string, container, filename)


def prepare_dataset_for_modeling(df, is_raw=False):
    """
    Prepare any dataset for modeling by adding derived features (IMC, std_mV).

    For raw datasets (is_raw=True): loads signals from local files.
    For clean datasets (is_raw=False): assumes features already exist.

    df(pandas.DataFrame): Dataset to prepare
    is_raw(bool, default False):
        If True, adds IMC and extracts std_mV from signals.
        If False, ensures IMC and std_mV exist.

    Returns:
    pandas.DataFrame. DataFrame ready for feature selection
    """
    df = df.copy()
    
    if is_raw:
        df[COLUMNS['imc']] = df[COLUMNS['weight']] / ((df[COLUMNS['height']] / 100) ** 2)

        unique_ids = df[COLUMNS['patient_id']].unique()
        signal_summaries = pd.DataFrame([
            get_signal_summary(patient_id, PATHS_PROJECT['signals']) 
            for patient_id in unique_ids
        ])
        df = df.merge(signal_summaries, on=COLUMNS['patient_id'])
    
    return df


def prepare_features(df, model_features, sex_col, label_col):
    """
    Build X, Y from a dataframe: select features, encode sex, encode label.

    df(pandas.DataFrame): Input dataframe
    model_features(list): List of feature column names
    sex_col(str): Name of the sex column
    label_col(str): Name of the label column

    Returns:
    tuple : (X, Y)
        Features DataFrame and target Series
    """
    available_features = [col for col in model_features if col in df.columns]
    X = df[available_features].copy()
    
    X = X.dropna()

    Y = df.loc[X.index, label_col]
    Y = (Y == ANORMAL).astype(int)
    
    X = pd.get_dummies(X, columns=[sex_col], drop_first=True)
    
    return X, Y


def plot_confusion_matrix(y_true, y_pred, title='Matriz de Confusión'):
    """
    Plot an annotated confusion matrix heatmap.
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=[NORMAL, ANORMAL],
                yticklabels=[NORMAL, ANORMAL], ax=ax)
    ax.set_xlabel('Predicción')
    ax.set_ylabel('Real')
    ax.set_title(title)
    plt.tight_layout()
    return fig


def train_and_evaluate(X, Y, semilla=42, val_ratio=0.15, test_ratio=0.15):
    """
    Full train/val/test pipeline for the baseline Logistic Regression model.

    Returns:
    dict : Model results
    """
    x_train, x_val_test, y_train, y_val_test = train_test_split(
        X, Y, test_size=val_ratio + test_ratio, random_state=semilla, stratify=Y
    )
    x_val, x_test, y_val, y_test = train_test_split(
        x_val_test, y_val_test, test_size=test_ratio / (test_ratio + val_ratio),
        random_state=semilla, stratify=y_val_test
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_val_scaled = scaler.transform(x_val)

    modelo = LogisticRegression(class_weight='balanced', random_state=semilla)
    modelo.fit(x_train_scaled, y_train)

    proba_val = modelo.predict_proba(x_val_scaled)[:, 1]
    pred_val = modelo.predict(x_val_scaled)

    modelo_final = clone(modelo)
    x_train_val = pd.concat([x_train, x_val])
    y_train_val = pd.concat([y_train, y_val])
    x_train_val_scaled = scaler.fit_transform(x_train_val)
    x_test_scaled = scaler.transform(x_test)

    modelo_final.fit(x_train_val_scaled, y_train_val)
    proba_test = modelo_final.predict_proba(x_test_scaled)[:, 1]
    pred_test = modelo_final.predict(x_test_scaled)

    metrics_val = {
        'precision': precision_score(y_val, pred_val),
        'recall': recall_score(y_val, pred_val),
        'f1': f1_score(y_val, pred_val),
        'auc_roc': roc_auc_score(y_val, proba_val),
    }
    metrics_test = {
        'precision': precision_score(y_test, pred_test),
        'recall': recall_score(y_test, pred_test),
        'f1': f1_score(y_test, pred_test),
        'auc_roc': roc_auc_score(y_test, proba_test),
    }

    return {
        'modelo_final': modelo_final,
        'x_test': x_test, 'y_test': y_test, 'pred_test': pred_test, 'proba_test': proba_test,
        'y_val': y_val, 'pred_val': pred_val,
        'metrics_val': metrics_val,
        'metrics_test': metrics_test,
    }

def plot_error_by_quantile_bar(y_true, proba_pred, variable, variable_name, 
                               n_quantiles=4, title=None, ax=None):
    """
    Plot mean absolute error by quantiles of a continuous variable (bar chart).

    Parameters:
    y_true(array-like): True labels
    proba_pred(array-like): Predicted probabilities
    variable(array-like): Continuous variable to group by
    variable_name(str): Name of the variable for labeling
    n_quantiles(int): Number of quantiles to create
    title(str, optional): Custom title for the plot
    ax(matplotlib.axes.Axes, optional): Axes to plot on. If None, creates a new figure.

    Returns:
    tuple : (ax, error_df)
    """
    quantiles = pd.qcut(variable, q=n_quantiles, labels=[f'Q{i+1}' for i in range(n_quantiles)])

    error_df = pd.DataFrame({
        'error_absoluto': abs(y_true.values - proba_pred),
        'quantil': quantiles
    })

    error_summary = error_df.groupby('quantil')['error_absoluto'].mean().reset_index()
    error_summary.columns = ['quantil', 'error_promedio']

    print(f"\nError promedio por cuartil de {variable_name.upper()}")
    print(error_summary.to_string(index=False))

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(error_summary['quantil'], error_summary['error_promedio'],
                  color=sns.color_palette('Set2', n_quantiles), edgecolor='black')

    ax.set_title(title or f'Error promedio por cuartil de {variable_name}')
    ax.set_xlabel(f'Cuartil de {variable_name}')
    ax.set_ylabel('Error absoluto promedio')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.002,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)

    return ax, error_df
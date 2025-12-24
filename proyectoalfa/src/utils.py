import pandas as pd
import os

def load_power_data():
    """Carga el dataset de potencia instalada desde la carpeta data."""
    filepath = os.path.join("data", "potencia-instalada.csv")
    df = pd.read_csv(filepath)
    # Convertir fecha si es necesario
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'])
    return df
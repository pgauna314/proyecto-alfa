# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Fichas técnicas generadas desde datos oficiales.")

    # Cargar CSV (ruta relativa desde modules/)
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(csv_path):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return

    df = pd.read_csv(csv_path)

    # Toma el registro más reciente por central
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
    df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')

    # Filtros
    regiones = ["Todas"] + sorted(df['region'].dropna().unique().tolist())
    region = st.sidebar.selectbox("Región", regiones)

    fuentes = ["Todas"] + sorted(df['fuente_generacion'].dropna().unique().tolist())
    fuente = st.sidebar.selectbox("Fuente", fuentes)

    # Aplicar filtros
    df_f = df.copy()
    if region != "Todas":
        df_f = df_f[df_f['region'] == region]
    if fuente != "Todas":
        df_f = df_f[df_f['fuente_generacion'] == fuente]

    # Selector de central
    if df_f.empty:
        st.warning("No hay centrales con esos filtros.")
        return

    central = st.selectbox("Seleccioná una central", df_f['agente_descripcion'].unique())
    datos = df_f[df_f['agente_descripcion'] == central].iloc[0]

    # Ficha
    st.subheader(f"⚡ {central}")
    st.markdown(f"""
    - **Región**: {datos['region']}
    - **Tecnología**: {datos['tecnologia']}
    - **Fuente**: {datos['fuente_generacion']}
    - **Potencia instalada**: {datos['potencia_instalada_mw']:.1f} MW
    - **Código**: `{datos['central']}`
    """)
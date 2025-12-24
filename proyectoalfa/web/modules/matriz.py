# modules/matriz.py
import streamlit as st
import pandas as pd
import os

def mostrar_matriz():
    st.title("📊 Matriz Energética Nacional")
    
    # Ruta al CSV: desde modules/ → salir a proyectomayer/ → entrar a data/
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    
    if not os.path.exists(ruta_csv):
        st.error(f"❌ Archivo no encontrado en:\n`{ruta_csv}`")
        st.info("Asegurate de que la carpeta `data/` esté en la raíz del proyecto.")
        return

    try:
        df = pd.read_csv(ruta_csv)
        st.success(f"✅ Cargados {len(df)} registros.")
        
        # Filtros
        regiones = ["Todas"] + sorted(df["region"].dropna().unique().tolist())
        region = st.sidebar.selectbox("Región", regiones)
        
        if region != "Todas":
            df = df[df["region"] == region]
        
        # Mostrar datos
        st.subheader(f"Potencia total: {df['potencia_instalada_mw'].sum():,.0f} MW")
        st.dataframe(df[[
            "central", "region", "tecnologia", "potencia_instalada_mw"
        ]].head(20))
        
    except Exception as e:
        st.error(f"Error al leer el CSV: {e}")
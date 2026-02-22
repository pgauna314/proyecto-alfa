import streamlit as st
import pandas as pd
import plotly.express as px
from modules.palettes import ENERGY_THEME  # Importamos tu paleta centralizada

def mostrar_resumen():
    st.title("⚡ Matriz Energética Nacional")
    
    # Datos 
    # Usamos ENERGY_THEME para que coincida con el resto de la App y el Libro
    data = {
        'Fuente': ['Térmica', 'Hidráulica', 'Renovables', 'Nuclear'],
        'Capacidad_MW': [25300, 10800, 5500, 1750],
        'Despacho_MW': [13500, 4800, 3200, 1650],
        'Color': [
            ENERGY_THEME['Termica'], 
            ENERGY_THEME['Hidraulica'], 
            ENERGY_THEME['Renovables'], 
            ENERGY_THEME['Nuclear']
        ]
    }
    df = pd.DataFrame(data)

    # Mapa de colores para Plotly Express
    mapa_colores = {row['Fuente']: row['Color'] for i, row in df.iterrows()}

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Capacidad Instalada (%)")
        fig1 = px.pie(df, values='Capacidad_MW', names='Fuente', hole=0.4,
                      color='Fuente', color_discrete_map=mapa_colores)
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Despacho Actual (%)")
        fig2 = px.pie(df, values='Despacho_MW', names='Fuente', hole=0.4,
                      color='Fuente', color_discrete_map=mapa_colores)
        st.plotly_chart(fig2, use_container_width=True)
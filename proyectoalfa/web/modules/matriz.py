import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_matriz():
    st.title("⚡ Matriz Energética Nacional")
    
    # Datos (Podemos luego mover esto a un CSV externo)
    data = {
        'Fuente': ['Térmica', 'Hidráulica', 'Renovables', 'Nuclear'],
        'Capacidad_MW': [25300, 10800, 5500, 1750],
        'Despacho_MW': [13500, 4800, 3200, 1650],
        'Color': ['#E69F00', '#56B4E9', '#009E73', '#F0E442']
    }
    df = pd.DataFrame(data)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Capacidad Instalada (%)")
        fig1 = px.pie(df, values='Capacidad_MW', names='Fuente', hole=0.4,
                      color='Fuente', color_discrete_map={row['Fuente']: row['Color'] for i, row in df.iterrows()})
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Despacho Actual (%)")
        fig2 = px.pie(df, values='Despacho_MW', names='Fuente', hole=0.4,
                      color='Fuente', color_discrete_map={row['Fuente']: row['Color'] for i, row in df.iterrows()})
        st.plotly_chart(fig2, use_container_width=True)

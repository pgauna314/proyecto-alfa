import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide")

# 2. DATOS TÉCNICOS (Capacidad Instalada SADI aprox. 2024/2025)
# Valores en MW para el cálculo, pero mostraremos %
data_sadi = {
    'Fuente': ['Térmica', 'Hidráulica', 'Renovables', 'Nuclear'],
    'Capacidad_MW': [25300, 10800, 5500, 1750],
    'Despacho_Actual_MW': [13500, 4800, 3200, 1650], # Valores de ejemplo
    'Color': ['#E69F00', '#56B4E9', '#009E73', '#F0E442'] # Paleta daltónicos
}
df = pd.DataFrame(data_sadi)

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", ["Matriz Energética", "Capítulo II: Sistemas"])

# 4. CONTENIDO PRINCIPAL
if menu == "Matriz Energética":
    st.title("⚡ Estado de la Matriz Energética (SADI)")
    st.markdown("Comparativa porcentual de Capacidad Instalada vs. Despacho Real.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Capacidad Instalada (%)")
        fig_cap = px.pie(
            df, values='Capacidad_MW', names='Fuente',
            color='Fuente', color_discrete_map={row['Fuente']: row['Color'] for i, row in df.iterrows()},
            hole=0.4
        )
        fig_cap.update_traces(textinfo='percent')
        st.plotly_chart(fig_cap, use_container_width=True)
        st.caption("Distribución de la potencia máxima que el sistema puede generar.")

    with col2:
        st.subheader("Despacho Actual (%)")
        fig_desp = px.pie(
            df, values='Despacho_Actual_MW', names='Fuente',
            color='Fuente', color_discrete_map={row['Fuente']: row['Color'] for i, row in df.iterrows()},
            hole=0.4
        )
        fig_desp.update_traces(textinfo='percent')
        st.plotly_chart(fig_desp, use_container_width=True)
        st.caption("Distribución de la energía que se está consumiendo ahora.")

    st.divider()

    # GRÁFICO DE BARRAS DE UTILIZACIÓN
    st.subheader("Factor de Utilización por Fuente")
    # Calculamos qué % de su propia capacidad está usando cada fuente
    df['Utilizacion'] = (df['Despacho_Actual_MW'] / df['Capacidad_MW']) * 100
    
    fig_util = px.bar(
        df, x='Fuente', y='Utilizacion', 
        color='Fuente', color_discrete_map={row['Fuente']: row['Color'] for i, row in df.iterrows()},
        labels={'Utilizacion': '% de Uso de Capacidad'}
    )
    st.plotly_chart(fig_util, use_container_width=True)
    st.info("Este gráfico muestra cuánta 'reserva' tiene cada fuente. Si una barra llega al 100%, esa fuente no puede dar más energía.")


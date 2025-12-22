import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Datos de Referencia (SADI - Argentina)
capacidad_data = {
    'Fuente': ['Térmica', 'Hidráulica', 'Renovables', 'Nuclear'],
    'MW_Instalados': [25300, 10800, 5500, 1750],
    'Color': ['#E69F00', '#56B4E9', '#009E73', '#F0E442'] # Paleta daltónicos
}
df_cap = pd.DataFrame(capacidad_data)

# Datos de Generación Típica (Para la Torta)
generacion_data = {
    'Fuente': ['Térmica', 'Hidráulica', 'Eólica/Solar', 'Nuclear'],
    'Generación [MW]': [12800, 4200, 3100, 1650],
    'Color': ['#E69F00', '#56B4E9', '#009E73', '#F0E442']
}
df_gen = pd.DataFrame(generacion_data)

# 3. Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", ["Matriz Energética", "Capítulo II: Sistemas"])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# 4. Contenido Principal
if menu == "Matriz Energética":
    st.title("⚡ Análisis de la Matriz Energética Nacional")
    st.markdown("""
    Esta sección permite visualizar la **oferta y demanda** del Sistema Argentino de Interconexión (SADI). 
    Analizamos tanto la capacidad instalada como el despacho real de energía.
    """)

    # --- FILA 1: Gráfico de Torta y Métricas ---
    col_pie, col_met = st.columns([1.5, 1])
    
    with col_pie:
        st.subheader("Despacho de Generación Actual")
        fig_pie = px.pie(
            df_gen, 
            values='Generación [MW]', 
            names='Fuente',
            color='Fuente',
            color_discrete_map={row['Fuente']: row['Color'] for index, row in df_gen.iterrows()},
            hole=0.4
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_met:
        st.subheader("Estado del Sistema")
        total_gen = df_gen['Generación [MW]'].sum()
        nuclear_gen = df_gen[df_gen['Fuente'] == 'Nuclear']['Generación [MW]'].values[0]
        porc_nuclear = (nuclear_gen / total_gen) * 100

        st.metric("Generación Total", f"{total_gen} MW")
        st.metric("Aporte Nuclear", f"{nuclear_gen} MW", f"{porc_nuclear:.1f}% del despacho")
        
        st.info("""
        **Nota Pedagógica:** Observá que aunque la capacidad instalada nuclear es menor en MW totales, 
        su despacho es constante. Es la 'base' del sistema que permite la estabilidad.
        """)

    st.divider()

    # --- FILA 2: Curva de Demanda Histórica ---
    st.subheader("Demanda vs. Capacidad Máxima")
    epoca = st.select_slider("Seleccione Época del Año:", options=["Invierno", "Verano"])
    
    # Simulación de curvas
    horas = list(range(24))
    demanda = [19000, 18000, 17500, 17000, 17200, 18000, 20000, 22000, 24000, 25000, 26000, 27000, 
               27500, 28000, 27800, 27000, 26500, 27000, 28500, 29000, 28000, 26000, 23000, 21000] if epoca == "Verano" else \
              [16000, 15000, 14500, 14200, 14500, 16000, 18000, 20000, 21000, 21500, 21800, 22000,
               21500, 21000, 20500, 20000, 21000, 23000, 24500, 25000, 24000, 22000, 19000, 17500]
    
    cap_total = df_cap['MW_Instalados'].sum()

    fig_dem = go.Figure()
    fig_dem.add_trace(go.Scatter(x=horas, y=demanda, fill='tozeroy', name='Demanda (MW)', line=dict(color='#56B4E9')))
    fig_dem.add_trace(go.Scatter(x=horas, y=[cap_total]*24, name='Capacidad Instalada Total', line=dict(color='#D55E00', dash='dash')))
    
    fig_dem.update_layout(xaxis_title="Hora", yaxis_title="Potencia (MW)")
    st.plotly_chart(fig_dem, use_container_width=True)

# --- SECCIÓN CAPÍTULO II (Esqueleto) ---
elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Capítulo II: Análisis de Sistemas")
    st.write("Contenido técnico en desarrollo para acompañar el libro.")

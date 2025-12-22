import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración
st.set_page_config(page_title="Proyecto MAYER", layout="wide")

# 2. Datos Inteligentes (Valores de referencia SADI)
# Capacidad Instalada (MW) - Datos aprox. actuales
capacidad_data = {
    'Fuente': ['Térmica', 'Hidráulica', 'Renovables', 'Nuclear'],
    'MW_Instalados': [25300, 10800, 5500, 1750] 
}
df_cap = pd.DataFrame(capacidad_data)

# Histórico de Demanda Típica (Verano vs Invierno)
horas = list(range(24))
demanda_verano = [19000, 18000, 17500, 17000, 17200, 18000, 20000, 22000, 24000, 25000, 26000, 27000, 
                  27500, 28000, 27800, 27000, 26500, 27000, 28500, 29000, 28000, 26000, 23000, 21000]
demanda_invierno = [16000, 15000, 14500, 14200, 14500, 16000, 18000, 20000, 21000, 21500, 21800, 22000,
                    21500, 21000, 20500, 20000, 21000, 23000, 24500, 25000, 24000, 22000, 19000, 17500]

# --- INTERFAZ ---
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Secciones:", ["Matriz y Capacidad", "Capítulo II: Sistemas"])

if menu == "Matriz y Capacidad":
    st.title("📊 Análisis de Suficiencia Energética")
    st.markdown("Comparativa entre la **Capacidad Instalada** y la **Curva de Carga** histórica.")

    # 1. Gráfico de Barras de Capacidad (Paleta daltónicos)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Capacidad Instalada")
        # Paleta: Azul (#0072B2), Naranja (#E69F00), Verde (#009E73), Vermillion (#D55E00)
        fig_cap = go.Figure(data=[
            go.Bar(name='Instalada', x=df_cap['Fuente'], y=df_cap['MW_Instalados'], marker_color='#0072B2')
        ])
        fig_cap.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cap, use_container_width=True)
        
        st.info(f"**Total Instalado:** {df_cap['MW_Instalados'].sum()} MW")

    with col2:
        st.subheader("Curva de Demanda vs. Techo de Generación")
        epoca = st.select_slider("Seleccione Época del Año:", options=["Invierno", "Verano"])
        
        demanda_select = demanda_verano if epoca == "Verano" else demanda_invierno
        cap_total = df_cap['MW_Instalados'].sum()

        fig_dem = go.Figure()
        # Área de demanda
        fig_dem.add_trace(go.Scatter(x=horas, y=demanda_select, fill='tozeroy', name='Demanda (MW)',
                                     line=dict(color='#E69F00', width=3)))
        # Línea de capacidad máxima
        fig_dem.add_trace(go.Scatter(x=horas, y=[cap_total]*24, name='Capacidad Total',
                                     line=dict(color='#D55E00', dash='dash')))
        
        fig_dem.update_layout(xaxis_title="Hora del día", yaxis_title="MW", height=350)
        st.plotly_chart(fig_dem, use_container_width=True)

    st.divider()
    
    # 2. La reflexión pedagógica para el libro
    st.markdown("### El Rol de la Energía Nuclear en el Balance")
    c1, c2 = st.columns(2)
    with c1:
        st.write("""
        **¿Por qué Atucha II es estratégica?**
        Incluso si la 'Capacidad Total' parece alta, muchas fuentes (como las renovables o las hidroeléctricas en sequía) 
        no están disponibles al 100%. La energía nuclear provee lo que llamamos **Carga de Base**.
        """)
    with c2:
        nuclear_cap = 1750 # Atucha I + II + Embalse
        reserva = cap_total - max(demanda_select)
        st.metric("Reserva de Potencia en Pico", f"{reserva} MW", delta_color="normal")
        st.caption("Margen de maniobra del sistema antes de entrar en emergencia.")

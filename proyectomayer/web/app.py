import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Barra Lateral Única
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", [
        "Inicio", 
        "Capítulo II: Sistemas", 
        "Matriz Energética (CAMMESA)"
    ])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")
    st.info("Soporte interactivo para el estudio de sistemas térmicos.")

# 3. Contenido Principal

# --- SECCIÓN: INICIO ---
if menu == "Inicio":
    st.title("Estudio de Sistemas Térmicos")
    st.write("Bienvenido a la plataforma interactiva del Proyecto MAYER.")
    st.markdown("""
    Este sitio funciona como complemento dinámico del libro. Aquí podrás:
    * Analizar sistemas térmicos reales (Atucha II).
    * Validar balances de masa y energía.
    * Monitorear la matriz energética nacional.
    """)

# --- SECCIÓN: CAPÍTULO II ---
elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Análisis de Sistemas: El Generador de Vapor")
    
    st.markdown("""
    ### 1. Definición del Volumen de Control
    Como se describe en la **Figura 2.1** del libro, definimos nuestro sistema 
    rodeando el fluido secundario dentro del Generador de Vapor.
    """)

    # Espacio para figura
    with st.container(border=True):
        st.write("🖼️ **[ Aquí se insertará la Figura 2.1 del libro ]**")
        st.caption("Diagrama de flujos y límites del sistema para el Generador de Vapor de Atucha II.")

    st.divider()

    st.markdown("### 2. Balance de Energía en el Sistema")
    
    m = 950.4
    h_ent = 950
    h_sal = 2770
    Q_mw = m * (h_sal - h_ent) / 1000

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Ecuación de Balance:**")
        st.latex(r"\dot{Q} = \dot{m} (h_{sal} - h_{ent})")
        st.write("Donde:")
        st.write(f"* $\dot{{m}}$ = {m} kg/s")
        st.write(f"* $h_{{ent}}$ = {h_ent} kJ/kg")
        st.write(f"* $h_{{sal}}$ = {h_sal} kJ/kg")

    with col2:
        st.write("**Resultado del Cálculo:**")
        st.metric("Calor transferido (Q)", f"{Q_mw:.1f} MWt")
        st.info("Este valor representa la potencia térmica que el circuito primario cede al secundario.")

    st.divider()
    
    st.markdown("""
    ### 3. Formalización del Concepto
    A partir de este análisis, observamos que la elección del límite es arbitraria pero fundamental:
    * Si el límite incluyera ambos circuitos, el sistema sería **adiabático**.
    * Al incluir solo el secundario, el calor cruza la frontera y debe contabilizarse.
    """)

# --- SECCIÓN: MATRIZ ENERGÉTICA ---
elif menu == "Matriz Energética (CAMMESA)":
    st.title("⚡ Monitoreo de la Matriz Energética Argentina")
    st.markdown("""
    Datos simulados basados en los informes de **CAMMESA**. La energía nuclear 
    proporciona la estabilidad necesaria para el Sistema Argentino de Interconexión (SADI).
    """)

    data = {
        'Fuente': ['Térmica', 'Hidráulica', 'Nuclear', 'Eólica', 'Solar', 'Biomasa'],
        'Generación (MW)': [12500, 4200, 1650, 3100, 800, 250],
        'Color': ['#808080', '#1f77b4', '#ff4b4b', '#2ca02c', '#ffea00', '#8c564b']
    }
    df = pd.DataFrame(data)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Distribución por Fuente")
        fig_pie = px.pie(df, values='Generación (MW)', names='Fuente', 
                         color='Fuente', color_discrete_sequence=df['Color'].tolist(),
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Impacto Nuclear")
        total_mw = df['Generación (MW)'].sum()
        nuclear_mw = df[df['Fuente'] == 'Nuclear']['Generación (MW)'].values[0]
        porcentaje_nuclear = (nuclear_mw / total_mw) * 100
        
        st.metric("Potencia Total", f"{total_mw} MW")
        st.metric("Aporte Nuclear", f"{nuclear_mw} MW", f"{porcentaje_nuclear:.1f}%")
        st.info("La energía nuclear actúa como carga base, garantizando el suministro independientemente del clima.")

    st.divider()
    st.subheader("Histórico de Demanda Típica (SADI)")
    chart_data = pd.DataFrame({
        'Hora': list(range(24)),
        'Demanda (MW)': [14000, 13200, 12800, 12500, 12700, 13500, 15000, 17000, 18500, 19000, 19500, 20000, 
                         19800, 19500, 19200, 19000, 19500, 21000, 22500, 23000, 22000, 20000, 18000, 16000]
    })
    st.line_chart(chart_data, x='Hora', y='Demanda (MW)')

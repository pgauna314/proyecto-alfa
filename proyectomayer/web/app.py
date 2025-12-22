import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", ["Inicio", "Capítulo II: Sistemas"])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# 3. Contenido Principal
if menu == "Inicio":
    st.title("Estudio de Sistemas Térmicos")
    st.write("Bienvenido a la plataforma interactiva del Proyecto MAYER.")

elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Análisis de Sistemas: El Generador de Vapor")
    
    # Este bloque vincula directamente con el texto de tu libro
    st.markdown("""
    ### 1. Definición del Volumen de Control
    Como se describe en la **Figura 2.1** del libro, definimos nuestro sistema 
    rodeando el fluido secundario dentro del Generador de Vapor.
    """)

    # ESPACIO PARA TU FIGURA DEL LIBRO
    # Cuando tengas la imagen, reemplazaremos este cuadro por st.image()
    st.container(border=True):
        st.write("🖼️ **[ Aquí se insertará la Figura 2.1 del libro ]**")
        st.caption("Diagrama de flujos y límites del sistema para el Generador de Vapor de Atucha II.")

    st.divider()

    st.markdown("### 2. Balance de Energía en el Sistema")
    
    # Parámetros técnicos alineados con Atucha II
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
    
    # Sección de formalización pedagógica
    st.markdown("""
    ### 3. Formalización del Concepto
    A partir de este análisis, observamos que la elección del límite es arbitraria pero fundamental:
    * Si el límite incluyera ambos circuitos, el sistema sería **adiabático**.
    * Al incluir solo el secundario, el calor cruza la frontera y debe contabilizarse.
    """)





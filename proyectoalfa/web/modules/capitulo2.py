import streamlit as st

def mostrar_cap2():
    st.title("⚛️ Capítulo II: Análisis de Sistemas")
    
    st.markdown("### Balance de Energía: El Generador de Vapor")
    
    with st.container(border=True):
        st.write("🖼️ **[ Espacio para Figura 2.1 del libro ]**")
    
    # Cálculos técnicos
    m = 950.4
    h_ent, h_sal = 950, 2770
    Q_mw = m * (h_sal - h_ent) / 1000
    
    st.metric("Calor Transferido (Q)", f"{Q_mw:.1f} MWt")

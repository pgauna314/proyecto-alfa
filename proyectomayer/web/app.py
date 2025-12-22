import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="🏗️")

# 2. Barra Lateral (Navegación y Botones)
with st.sidebar:
    st.title("🏗️ Hola AYU")
    st.divider()
    
    # Menú de Secciones
    menu = st.radio("Secciones del Libro:", 
                    ["Inicio", "Capítulo II: Sistemas", "Observatorio de Datos"])
    
    st.divider()
    st.write("### Recursos Externos")
    
    # Botones de acceso rápido
    st.link_button("📺 Canal de YouTube", "https://youtube.com/@TuCanal")
    st.link_button("📚 Libro Completo (PDF)", "https://github.com/TuUsuario/Proyecto-Mayer/libro/main.pdf")
    
    st.divider()
    st.info("Autor: Dr. Pablo Gauna")

# 3. Panel Principal
if menu == "Inicio":
    st.title("Bienvenidos al Proyecto MAYER")
    st.markdown("""
    Este sitio es el soporte dinámico para el estudio de la termodinámica aplicada.
    Aquí transformamos las ecuaciones del libro en herramientas de cálculo reales.
    """)
    st.image("https://www.na-sa.com.ar/assets/images/centrales/atucha2_header.jpg", caption="Central Nuclear Atucha II")

elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Capítulo II: Sistemas y Balances")
    
    st.markdown("""
    En este capítulo, abordaremos los conceptos fundamentales de **sistema, balance de materia 
    y balance de energía**, aplicándolos al funcionamiento de una central térmica.
    """)
    
    st.warning("🔍 **Enfoque Inductivo:** Analizamos la generación antes de las definiciones abstractas.")

    # Simulador de Balance para Atucha II
    st.subheader("Simulador de Balance de Masa y Energía (CNA II)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Entradas al Generador de Vapor**")
        caudal = st.slider("Caudal másico ($kg/s$)", 800.0, 1100.0, 950.4)
        temp_ent = st.number_input("Temp. Entrada ($°C$)", value=220)
    
    with col2:
        st.write("**Resultado del Balance**")
        # Un cálculo lineal simple para ilustrar el concepto de balance
        potencia = (caudal * 0.78) 
        st.metric("Potencia Térmica Transferida", f"{potencia:.1f} MWt")
        
        st.write("A mayor caudal, mayor transferencia de energía, manteniendo el balance del sistema.")

elif menu == "Observatorio de Datos":
    st.title("🔭 Observatorio de Datos")
    st.write("Visualización de parámetros históricos de Atucha II.")
    # Aquí podrías poner un gráfico más adelante
    st.bar_chart([745, 740, 745, 730, 745])



#archivo inicio.py
import streamlit as st

def mostrar_inicio():
    st.header("Bienvenidos al Proyecto α")
    st.subheader("Termodinámica de la Conversión de Energía en Argentina")
    
    st.markdown("""
    Este entorno es una plataforma pedagógica integral diseñada para el estudio de la termodinámica aplicada 
    a la realidad productiva nacional. El **Proyecto α** propone un aprendizaje situado, vinculando 
    el rigor científico con la soberanía tecnológica.
    """)

    st.divider()

    # Presentación de los Módulos
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 📖 Módulo λ\n**El Libro**")
        st.write("Fundamentos teóricos y formalismo matemático. El texto base que analiza plantas de potencia y sistemas de frío en Argentina.")

    with col2:
        st.success("### ⚙️ Módulo Σ\n**La App**")
        st.write("Motor de cálculo y simulación. Herramienta para resolver balances de masa y energía de forma instantánea y precisa.")

    with col3:
        st.warning("### 📺 Módulo ϕ\n**YouTube**")
        st.write("Flujo dinámico y visual. Resolución de casos prácticos, tutoriales de la app y visitas virtuales a plantas reales.")

    st.divider()

    st.markdown("""
    ### 🏗️ ¿Cómo trabajar en este entorno?
    1. **Navegación:** Utilizá el menú lateral para acceder al **Σ - Laboratorio de Propiedades** para tus cálculos o al **λ - Capítulo II** para la teoría.
    2. **Propósito:** El objetivo es liberar la carga de cálculo mecánico para centrarse en el **análisis de procesos térmicos** y la optimización energética.
    3. **Contexto:** Encontrarás datos de la red eléctrica nacional y casos de estudio de la industria local para entender la termodinámica desde nuestro territorio.
    """)

    st.info("💡 **Soberanía Educativa:** Este proyecto busca que el estudiante de ingeniería disponga de herramientas propias, desvinculadas de manuales o software que no contemplan nuestra realidad industrial.")
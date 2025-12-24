import streamlit as st

def mostrar_matriz():
    st.header("📊 Matriz Energética Nacional")
    st.subheader("Argentina – Año 2024")
    
    st.markdown("""
    La matriz eléctrica argentina refleja un mix energético en transición, con una fuerte presencia de fuentes renovables y térmicas fósiles, junto con una base hidroeléctrica y nuclear estable.
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 🔥 Térmicas Fósiles\n**~60%**\nGas natural y fuel oil dominan la generación en horas pico y en invierno.")
    
    with col2:
        st.success("### 💧 Hidroeléctricas\n**~25%**\nYacyretá, Salto Grande y el complejo Chocón–Cerros Colorados son pilares del sistema.")
    
    with col3:
        st.warning("### 🌬️ Renovables\n**~12%**\nEólica (en Patagonia y Centro) y solar (NOA) crecen aceleradamente.")

    st.divider()

    st.markdown("""
    ### 📌 Clasificación por fuente (aproximada)
    - **Térmicas**: 60% (gas natural, carbón, fuel oil)
    - **Hidroeléctricas**: 25%
    - **Nuclear**: 4% (Atucha I, Atucha II, Embalse)
    - **Renovables variables**: 11% (eólica, solar, biomasa)
    """)

    st.info("💡 **Enfoque pedagógico**: Este módulo busca contextualizar los ciclos termodinámicos estudiados en el libro (Rankine, Brayton, etc.) dentro de la realidad de la operación del sistema eléctrico argentino.")
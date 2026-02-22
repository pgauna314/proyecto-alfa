import streamlit as st

def mostrar_resumen():
    """
    Renderiza el contenido teórico y glosario. 
    Se eliminan encabezados redundantes para integrarse con cap2_main.py.
    """
    
    st.markdown("""
    Este capítulo es el corazón de la termodinámica técnica. Aquí dejamos de ver 
    sustancias en reposo y empezamos a estudiar el **flujo de energía y materia** a través de equipos industriales.
    """)

    # --- CONTENIDO PEDAGÓGICO ---
    st.info("""
    **Enfoque del Proyecto α:** Mientras que en el libro físico encontrás las deducciones 
    matemáticas, en esta plataforma nos enfocamos en la **jerarquía de las fronteras**. 
    Antes de operar cualquier ecuación, es vital definir qué flujos cruzan tu volumen de estudio.
    """)

    st.divider()

    # --- GLOSARIO DINÁMICO ---
    st.subheader("📖 Glosario de Conceptos Críticos")
    st.write("Explorá los términos clave que utilizaremos en los simuladores:")
    
    conceptos = {
        "Frontera del Sistema": "Superficie (real o imaginaria) que delimita nuestro volumen de estudio. Es la 'aduana' por donde pasan la masa y la energía.",
        "Estado Estacionario": "Régimen donde las propiedades en cada punto del equipo no varían con el tiempo ($\dot{m}_{in} = \dot{m}_{out}$).",
        "Entalpía ($h$)": "La propiedad fundamental en sistemas abiertos. Representa la energía total del fluido en movimiento: $h = u + Pv$.",
        "Volumen de Control": "Una región fija en el espacio elegida para el análisis de sistemas donde existe flujo de masa."
    }

    # Renderizado en columnas para mayor legibilidad
    cols = st.columns(2)
    for i, (termino, definicion) in enumerate(conceptos.items()):
        with cols[i % 2]:
            with st.expander(f"🔍 {termino}"):
                st.write(definicion)

    st.write("") 
    st.markdown("> **Nota:** Podés validar tu comprensión de estos términos en la pestaña de **Autoevaluación**.")

def render():
    """Mantiene compatibilidad con llamadas genéricas."""
    mostrar_resumen()
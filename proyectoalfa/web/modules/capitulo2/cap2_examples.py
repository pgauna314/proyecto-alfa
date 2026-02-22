import streamlit as st
from . import ex2_1_condensador
# from . import ex2_2_tobera  # Próximamente

def examples_render():
    """
    Orquestador de ejemplos prácticos. 
    Se integra en la pestaña 'Ejemplos' del cap2_main.
    """
    
    st.markdown("""
    En esta sección aplicaremos los balances de masa y energía mediante **simuladores dinámicos**. 
    Resolvé los desafíos planteados en cada equipo para validar tu capacidad de cálculo.
    """)

    # --- MENÚ DE NAVEGACIÓN INTERNO ---
    st.subheader("🚀 Seleccioná un Caso de Estudio")
    
    ejemplos_disponibles = {
        "--- Elegir un equipo para simular ---": None,
        "1. Balance en Condensador (Intercambio de Calor)": ex2_1_condensador.run_example,
        # "2. Tobera (Balance de Masa)": ex2_2_tobera.run_example,
    }

    seleccion = st.selectbox(
        "¿Qué equipo querés analizar?", 
        options=list(ejemplos_disponibles.keys()),
        label_visibility="collapsed" 
    )

    st.divider()

    # --- LÓGICA DE CARGA ---
    if seleccion != "--- Elegir un equipo para simular ---" and ejemplos_disponibles[seleccion] is not None:
        # Ejecutamos el ejemplo seleccionado
        ejemplos_disponibles[seleccion]()
    else:
        # Estado inicial: Guía para el usuario
        st.info("Seleccioná un equipo del menú superior para comenzar la simulación.")
        
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            **Objetivos de aprendizaje:**
            * **Identificar** flujos de entrada y salida ($ \dot{m} $).
            * **Definir** fronteras de sistema efectivas.
            * **Calcular** calores de intercambio y eficiencias.
            * **Validar** la competencia de cálculo del capítulo.
            """)
        with col2:
            # Una imagen técnica de mayor calidad o un esquema conceptual
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Rankine_cycle_layout.png/300px-Rankine_cycle_layout.png", 
                     caption="Integración de equipos en ciclos de potencia")

def render():
    """Mantiene compatibilidad con el enrutador."""
    examples_render()
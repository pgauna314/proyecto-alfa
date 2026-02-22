import streamlit as st

def run_example():
    st.header("Caso de Estudio: Condensador de Vapor")
    
    # --- 1. ENUNCIADO, DATOS Y ESQUEMA ---
    st.subheader("1. Enunciado del Problema")
    
    col_enunciado, col_esquema = st.columns([1.5, 1])
    
    with col_enunciado:
        st.write("""
        Se requiere realizar el balance de energía de un condensador industrial de superficie. 
        El vapor de agua entra por la carcasa y cede energía al agua de enfriamiento que circula 
        por el interior de los tubos. No existe mezcla entre ambos fluidos.
        """)
        
    with col_esquema:
        # Intentamos cargar la imagen con la nueva sintaxis 'width' de 2026
        try:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Condenser_layout_1.svg/500px-Condenser_layout_1.svg.png", 
                     caption="Figura 2.1: Esquema de flujos en un condensador.",
                     width='stretch') 
        except:
            # Si falla la carga externa, mostramos un esquema de bloques textual
            st.error("No se pudo cargar la imagen externa.")
            st.markdown("""
            **Esquema de Flujos:**
            ```
            Vapor (h_ent) ---> [ CONDENSADOR ] ---> Vapor (h_sal)
                                    ^
                                    |
            Agua (h_ent)  ----------+----------  Agua (h_sal)
            ```
            """)

    

    with st.container(border=True):
        st.markdown("**Datos de Planta:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fluido de Trabajo (Vapor)**")
            st.write(r"- Flujo másico ($\dot{m}_{v}$): **120 kg/s**")
            st.write(r"- Entalpía entrada ($h_{v,ent}$): **2550 kJ/kg**")
            st.write(r"- Entalpía salida ($h_{v,sal}$): **200 kJ/kg**")
        with col2:
            st.markdown("**Fluido Refrigerante (Agua)**")
            st.write(r"- Entalpía entrada ($h_{a,ent}$): **63 kJ/kg**")
            st.write(r"- Entalpía salida ($h_{a,sal}$): **105 kJ/kg**")

    st.divider()

    # --- 2. GUÍA DE RESOLUCIÓN PASO A PASO ---
    st.subheader("2. Guía de Resolución")

    # Paso A: Ecuación General
    with st.expander("Paso A: Primer Principio para Sistemas Abiertos", expanded=True):
        st.write("Partimos de la ecuación general para un sistema abierto en estado estacionario:")
        st.latex(r"\sum \dot{Q} - \sum \dot{W} = \sum \dot{m}_{sal} \left( h + \frac{V^2}{2} + gz \right)_{sal} - \sum \dot{m}_{ent} \left( h + \frac{V^2}{2} + gz \right)_{ent}")
        
        st.write("**Simplificaciones del modelo:**")
        st.markdown(r"""
        * **Frontera adiabática:** El equipo está aislado ($\sum \dot{Q} = 0$).
        * **Sin trabajo de eje:** El equipo es estático ($\sum \dot{W} = 0$).
        * **Energías mecánicas:** Se desestiman variaciones de energía cinética y potencial ($\Delta ec \approx 0, \Delta ep \approx 0$).
        """)

    # Paso B: Desarrollo de la Sumatoria
    with st.expander("Paso B: Desarrollo de flujos y reordenamiento"):
        st.write("Expandimos los flujos que atraviesan la frontera del sistema:")
        st.latex(r"0 = (\dot{m}_{v} h_{v,sal} + \dot{m}_{a} h_{a,sal}) - (\dot{m}_{v} h_{v,ent} + \dot{m}_{a} h_{a,ent})")
        
        st.write("Reordenamos agrupando los términos por fluido:")
        st.latex(r"\dot{m}_{v} (h_{v,ent} - h_{v,sal}) = \dot{m}_{a} (h_{a,sal} - h_{a,ent})")

    # Paso C: Modelo Matemático
    with st.expander("Paso C: Despeje del Flujo de Agua"):
        st.write(r"Despejamos la incógnita ($\dot{m}_{a}$):")
        st.latex(r"\dot{m}_{a} = \frac{\dot{m}_{v} (h_{v,ent} - h_{v,sal})}{(h_{a,sal} - h_{a,ent})}")

    # --- 3. VALIDACIÓN NUMÉRICA ---
    st.divider()
    st.subheader("3. Validación de Resultados")
    
    valor_objetivo = (120 * (2550 - 200)) / (105 - 63)
    
    entrada_usuario = st.number_input(
        r"Ingresá el flujo de agua calculado ($\dot{m}_{a}$) [kg/s]:", 
        min_value=0.0, 
        format="%.2f"
    )

    if st.button("Verificar Resolución"):
        error_relativo = abs(entrada_usuario - valor_objetivo) / valor_objetivo
        if error_relativo < 0.01:
            st.success(f"✅ ¡Correcto! El flujo másico de agua necesario es {valor_objetivo:.2f} kg/s.")
            st.balloons()
        else:
            st.error("❌ El resultado no es correcto. Revisá los valores de las entalpías.")

def render():
    run_example()
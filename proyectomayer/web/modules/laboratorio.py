import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    st.write("Configurá el estado, elegí el diagrama y ejecutá el diagnóstico pedagógico.")

    # --- ÁREA DE CONFIGURACIÓN INTEGRADA ---
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sustancias_map = {"Agua": "Water", "Amoníaco": "Ammonia", "Aire": "Air", "R134a": "R134a"}
            nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
            sustancia = sustancias_map[nombre_user]
        with c2:
            par = st.selectbox("Par de variables:", ["P y h", "P y T", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        # Segunda fila de configuración
        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.4f")
                p_pa = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=100.0)
                t_k = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
                x_in = v2
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
                h_j = v2 * 1000
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=20.0)
                t_k = v2 + 273.15
        with i3:
            st.write("") # Espaciador
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    # --- LÓGICA DE EJECUCIÓN ---
    if ejecutar:
        try:
            # Variables de estado
            t_plot, s_plot, p_plot, v_plot = 0, 0, 0, 0
            
            # EL CUENTO (Contenedor con estilo)
            expander_cuento = st.expander("📖 Ver el relato del diagnóstico (Paso a paso)", expanded=True)
            
            if par == "P y h":
                hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                h_in = v2
                
                with expander_cuento:
                    st.write(f"1. Entramos a la tabla de **{nombre_user}** por presión: **{v1} bar**.")
                    st.write(f"2. Identificamos los límites de la campana: $h_f = {hf:.2f}$ kJ/kg y $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        st.info(f"**Resultado:** Tu entalpía ({h_in}) es menor a la de líquido saturado. El estado es **Líquido Comprimido**.")
                    elif h_in > hg:
                        st.warning(f"**Resultado:** Tu entalpía ({h_in}) supera la de vapor saturado. El estado es **Vapor Sobrecalentado**.")
                    else:
                        x = (h_in - hf) / (hg - hf)
                        st.success(f"**Resultado:** La entalpía cae dentro de la campana. Es una **Mezcla** con título $x = {x:.4f}$.")
                
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                p_plot = v1
                v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- GRÁFICOS ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min, t_crit - 0.1, 100)
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf+sg[::-1], y=[t-273.15 for t in t_vec]*2, fill='toself', name='Campana', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]", height=500)
            else:
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                fig.add_trace(go.Scatter(x=vf+vg[::-1], y=[PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]*2, fill='toself', name='Campana', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]", height=500)

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ **Combinación imposible:** Los datos ingresados no corresponden a un estado físico real para el {nombre_user}.")
    else:
        st.info("💡 Completá los datos arriba y hacé clic en **Ejecutar Diagnóstico**.")
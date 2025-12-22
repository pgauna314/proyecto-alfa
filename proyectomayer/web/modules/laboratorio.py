import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    st.write("Configurá el estado, elegí el diagrama y ejecutá el diagnóstico pedagógico.")

    # --- PANEL DE CONFIGURACIÓN ---
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sustancias_map = {
                "Agua": "Water", 
                "Amoníaco": "Ammonia", 
                "Aire": "Air", 
                "R134a": "R134a"
            }
            nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
            sustancia = sustancias_map[nombre_user]
        with c2:
            par = st.selectbox("Par de variables:", ["P y T", "P y h", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f", min_value=0.01)
                p_pa = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=150.0, format="%.2f")
                t_k_base = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
                x_in = v2
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
                h_j = v2 * 1000
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=150.0)
                t_k_input = v2 + 273.15
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    # --- EJECUCIÓN DEL CÁLCULO ---
    if ejecutar:
        try:
            # Inicializamos variables de estado para el punto
            t_plot, s_plot, p_plot, v_plot = 0, 0, 0, 0

            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                # CASO 1: P y T
                if par == "P y T":
                    t_in = v2
                    t_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
                    st.write(f"1. A una presión de **{v1} bar**, la temperatura de ebullición es **{t_sat:.2f} °C**.")
                    
                    if t_in < t_sat - 0.05:
                        estado = "Líquido Comprimido"
                        st.info(f"**Resultado:** Como tu temperatura ({t_in} °C) es **menor** a $T_{{sat}}$, el estado es **{estado}**.")
                    elif t_in > t_sat + 0.05:
                        estado = "Vapor Sobrecalentado"
                        st.warning(f"**Resultado:** Como tu temperatura ({t_in} °C) es **mayor** a $T_{{sat}}$, el estado es **{estado}**.")
                    else:
                        estado = "Saturación"
                        st.success(f"**Resultado:** Estás en la línea de saturación. Es una mezcla de líquido y vapor.")
                    
                    t_plot = t_in
                    p_plot = v1
                    s_plot = PropsSI('S', 'P', p_pa, 'T', t_in + 273.15, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'T', t_in + 273.15, sustancia)

                # CASO 2: P y h
                elif par == "P y h":
                    h_in = v2
                    hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                    st.write(f"1. A **{v1} bar**, los límites de la campana son $h_f = {hf:.2f}$ y $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        estado = "Líquido Comprimido"
                        st.info(f"**Resultado:** Dado que $h$ ({h_in}) < $h_f$, el estado es **{estado}**.")
                    elif h_in > hg:
                        estado = "Vapor Sobrecalentado"
                        st.warning(f"**Resultado:** Dado que $h$ ({h_in}) > $h_g$, el estado es **{estado}**.")
                    else:
                        estado = "Mezcla"
                        x = (h_in - hf) / (hg - hf)
                        st.success(f"**Resultado:** El punto cae dentro de la campana. Es una **Mezcla**.")
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")

                    t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                    p_plot = v1
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

                # CASO 3: P y x / T y x (Saturados)
                elif "x" in par:
                    st.success("**Resultado:** Definiste el estado por título (x), por lo que estás en zona de **Mezcla**.")
                    if "P" in par:
                        t_plot = PropsSI('T', 'P', p_pa, 'Q', x_in, sustancia) - 273.15
                        s_plot = PropsSI('S', 'P', p_pa, 'Q', x_in, sustancia) / 1000
                        p_plot = v1
                        v_plot = 1 / PropsSI('D', 'P', p_pa, 'Q', x_in, sustancia)
                    else:
                        p_plot = PropsSI('P', 'T', t_k_base, 'Q', x_in, sustancia) / 100000
                        s_plot = PropsSI('S', 'T', t_k_base, 'Q', x_in, sustancia) / 1000
                        t_plot = v1
                        v_plot = 1 / PropsSI('D', 'T', t_k_base, 'Q', x_in, sustancia)

            # --- GENERAR GRÁFICO ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min + 0.5, t_crit - 0.2, 100)
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=[t-273.15 for t in t_vec]*2, 
                                         fill='toself', fillcolor='rgba(0,100,255,0.05)', line=dict(color='blue'), name='Campana'))
                
                # Isobara punteada
                s_range = np.linspace(min(sf)*0.8, max(sg)*1.2, 50)
                t_iso = [PropsSI('T', 'P', p_plot*100000, 'S', s*1000, sustancia)-273.15 for s in s_range]
                fig.add_trace(go.Scatter(x=s_range, y=t_iso, line=dict(color='orange', dash='dot'), name=f'Isobara {p_plot:.2f} bar'))
                
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers+text', text=[f"  Punto Actual"],
                                         textposition="top right", marker=dict(color='red', size=14, symbol='x'), name='Estado'))
                fig.update_layout(xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")

            else: # P-v
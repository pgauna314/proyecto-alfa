import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sustancias_map = {"Agua": "Water", "Amoníaco": "Ammonia", "Aire": "Air", "R134a": "R134a"}
            nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
            sustancia = sustancias_map[nombre_user]
        with c2:
            par = st.selectbox("Par de variables:", ["P y T", "P y h", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f")
                p_pa = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=150.0)
                t_k = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=150.0)
                t_k_input = v2 + 273.15
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                # --- LÓGICA PARA P y T ---
                if par == "P y T":
                    t_in = v2
                    t_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
                    
                    st.write(f"1. Buscamos la temperatura de saturación a **{v1} bar**.")
                    st.write(f"2. Encontramos que $T_{{sat}} = {t_sat:.2f}$ °C.")
                    
                    if t_in < t_sat - 0.01:
                        estado = "Líquido Comprimido"
                        st.info(f"**Resultado:** Como tu temperatura ({t_in} °C) es **menor** a $T_{{sat}}$, el agua aún no hierve. Es **{estado}**.")
                    elif t_in > t_sat + 0.01:
                        estado = "Vapor Sobrecalentado"
                        st.warning(f"**Resultado:** Como tu temperatura ({t_in} °C) es **mayor** a $T_{{sat}}$, el agua ya se evaporó totalmente. Es **{estado}**.")
                    else:
                        estado = "Mezcla (Punto Crítico de Sat.)"
                        st.success(f"**Resultado:** Estás justo en la temperatura de ebullición. Sin el título (x), no podemos saber cuánta mezcla hay.")

                    t_plot = t_in
                    s_plot = PropsSI('S', 'P', p_pa, 'T', t_in + 273.15, sustancia) / 1000
                    p_plot = v1
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'T', t_in + 273.15, sustancia)

                # --- LÓGICA PARA P y h ---
                elif par == "P y h":
                    h_in = v2
                    hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                    st.write(f"1. En tablas para **{v1} bar**: $h_f = {hf:.2f}$ y $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        estado = "Líquido Comprimido"
                        st.info(f"**Resultado:** Como $h$ ({h_in}) < $h_f$, el estado es **{estado}**.")
                    elif h_in > hg:
                        estado = "Vapor Sobrecalentado"
                        st.warning(f"**Resultado:** Como $h$ ({h_in}) > $h_g$, el estado es **{estado}**.")
                    else:
                        x = (h_in - hf) / (hg - hf)
                        st.success(f"**Resultado:** Mezcla con título:")
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")
                    
                    t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                    p_plot = v1
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- GRÁFICOS (REPARADOS) ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min + 0.1, t_crit - 0.1, 100)
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=[t-273.15 for t in t_vec]*2, fill='toself', name='Campana', line=dict(color='blue')))
                
                # Isobara para que se vea el camino
                s_vals = np.linspace(min(sf)*0.9, max(sg)*1.1, 50)
                t_iso = [PropsSI('T', 'P', p_pa, 'S', s*1000, sustancia)-273.15 for s in s_vals]
                fig.add_trace(go.Scatter(x=s_vals, y=t_iso, line=dict(color='orange', dash='dash'), name=f'Isobara {v1} bar'))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")

            else: # P-v
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                p_sat = [PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=p_sat*2, fill='toself', name='Campana', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Hubo un problema con los datos. Asegúrate de que la presión y temperatura estén dentro de los límites de la tabla.")
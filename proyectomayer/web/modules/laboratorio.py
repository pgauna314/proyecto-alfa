import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    st.write("Configurá el estado, elegí el diagrama y ejecutá el diagnóstico.")

    # --- PANEL DE CONFIGURACIÓN ---
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
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=150.0)
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            t_plot, s_plot, p_plot, v_plot = 0.0, 0.0, 0.0, 0.0

            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                if par == "P y T":
                    t_in = v2
                    t_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
                    st.write(f"1. A **{v1} bar**, la temperatura de saturación es **{t_sat:.2f} °C**.")
                    if t_in < t_sat - 0.1:
                        st.info(f"**Resultado:** Líquido Comprimido ({t_in} < {t_sat:.2f})")
                    elif t_in > t_sat + 0.1:
                        st.warning(f"**Resultado:** Vapor Sobrecalentado ({t_in} > {t_sat:.2f})")
                    else:
                        st.success("**Resultado:** Estado de Saturación.")
                    t_plot, p_plot = t_in, v1
                    s_plot = PropsSI('S', 'P', p_pa, 'T', t_in + 273.15, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'T', t_in + 273.15, sustancia)

                elif par == "P y h":
                    h_in = v2
                    hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                    st.write(f"1. Límites a **{v1} bar**: $h_f = {hf:.2f}$, $h_g = {hg:.2f}$ kJ/kg.")
                    if h_in < hf: st.info("Líquido Comprimido")
                    elif h_in > hg: st.warning("Vapor Sobrecalentado")
                    else:
                        x = (h_in - hf) / (hg - hf)
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")
                    t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                    p_plot, v_plot = v1, 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- GRÁFICOS CON ESCALA CONTROLADA ---
            t_crit = PropsSI('Tcrit', sustancia) - 273.15
            t_min = PropsSI('Tmin', sustancia) - 273.15
            t_vec = np.linspace(t_min + 0.1, t_crit - 0.1, 100)
            
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t+273.15, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t+273.15, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=list(t_vec) + list(t_vec)[::-1], fill='toself', fillcolor='rgba(0,100,255,0.1)', line=dict(color='blue'), name='Campana'))
                
                # Isobara limitada
                s_range = np.linspace(min(sf), max(sg)*1.3, 50)
                t_iso = [PropsSI('T', 'P', p_plot*100000, 'S', s*1000, sustancia)-273.15 for s in s_range]
                fig.add_trace(go.Scatter(x=s_range, y=t_iso, line=dict(color='orange', dash='dot'), name='Isobara'))
                
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Estado'))
                # AJUSTE DE ESCALA: No más de 100 grados sobre el punto crítico o el punto de estado
                fig.update_layout(yaxis=dict(range=[t_min, max(t_crit, t_plot) + 50]), xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")

            else: # P-v
                vf = [1/PropsSI('D', 'T', t+273.15, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t+273.15, 'Q', 1, sustancia) for t in t_vec]
                psat = [PropsSI('P', 'T', t+273.15, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=psat + psat[::-1], fill='toself', fillcolor='rgba(0,255,100,0.1)', line=dict(color='green'), name='Campana'))
                
                v_range = np.logspace(np.log10(min(vf)*0.5), np.log10(max(vg)*10), 50)
                p_iso = [PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000 for v in v_range]
                fig.add_trace(go.Scatter(x=v_range, y=p_iso, line=dict(color='purple', dash='dot'), name='Isoterma'))
                
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Estado'))
                # AJUSTE DE ESCALA P-v
                p_crit = PropsSI('Pcrit', sustancia)/100000
                fig.update_layout(xaxis_type="log", yaxis_type="log", yaxis=dict(range=[np.log10(0.01), np.log10(p_crit*5)]), xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
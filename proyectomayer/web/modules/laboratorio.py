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
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f", min_value=0.01)
                p_pa = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=150.0, format="%.2f")
                t_k = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=150.0)
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            # --- CÁLCULOS DE ESTADO ---
            if par == "P y T":
                t_in = v2
                t_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
                t_plot, p_plot = t_in, v1
                s_plot = PropsSI('S', 'P', p_pa, 'T', t_in + 273.15, sustancia) / 1000
                v_plot = 1 / PropsSI('D', 'P', p_pa, 'T', t_in + 273.15, sustancia)
                
                with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                    st.write(f"1. A **{v1} bar**, la temperatura de saturación es **{t_sat:.2f} °C**.")
                    if t_in < t_sat - 0.1:
                        st.info(f"**Líquido Comprimido**: {t_in}°C < {t_sat:.2f}°C")
                    elif t_in > t_sat + 0.1:
                        st.warning(f"**Vapor Sobrecalentado**: {t_in}°C > {t_sat:.2f}°C")
                    else:
                        st.success("**Estado de Saturación**: T coincide con T_sat.")

            elif par == "P y h":
                h_in = v2
                hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                p_plot, v_plot = v1, 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)
                
                with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                    st.write(f"1. Límites a **{v1} bar**: $h_f = {hf:.2f}$, $h_g = {hg:.2f}$ kJ/kg.")
                    if h_in < hf: st.info("Líquido Comprimido")
                    elif h_in > hg: st.warning("Vapor Sobrecalentado")
                    else:
                        x = (h_in - hf) / (hg - hf)
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")

            # --- GRÁFICOS PULIDOS ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min + 0.5, t_crit - 0.1, 100)
            
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                # Campana cerrada
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=[t-273.15 for t in t_vec] + [t-273.15 for t in t_vec][::-1], 
                                         fill='toself', fillcolor='rgba(0,100,255,0.05)', line=dict(color='blue', width=1), name='Campana'))
                
                # Isobara Dinámica
                s_iso = np.linspace(min(sf)*0.8, max(sg)*1.2, 100)
                t_iso = [PropsSI('T', 'P', p_pa, 'S', s*1000, sustancia)-273.15 for s in s_iso]
                fig.add_trace(go.Scatter(x=s_iso, y=t_iso, line=dict(color='orange', dash='dot'), name=f'Isobara {p_plot} bar'))
                
                # Punto de estado
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers+text', 
                                         text=[f"  ({s_plot:.2f}, {t_plot:.1f})"], textposition="top right",
                                         marker=dict(color='red', size=12, symbol='circle'), name='Estado Actual'))
                fig.update_layout(xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]", hovermode='x')

            else: # P-v
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                p_sat = [PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=p_sat + p_sat[::-1], fill='toself', 
                                         fillcolor='rgba(0,255,100,0.05)', line=dict(color='green', width=1), name='Campana'))
                
                # Isoterma Dinámica
                v_iso = np.logspace(np.log10(min(vf)*0.5), np.log10(max(vg)*5), 100)
                p_iso = [PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000 for v in v_iso]
                fig.add_trace(go.Scatter(x=v_vals, y=p_iso, line=dict(color='purple', dash='dot'), name=f'Isoterma {t_plot:.1f} °C'))
                
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers+text',
                                         text=[f"  v={v_plot:.3f}"], textposition="top right",
                                         marker=dict(color='red', size=12), name='Estado Actual'))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error en el diagnóstico: {e}")
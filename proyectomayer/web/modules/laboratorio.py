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
            par = st.selectbox("Par de variables:", ["P y h", "P y T", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f")
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
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            t_plot, s_plot, p_plot, v_plot = 0, 0, 0, 0
            
            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                if par == "P y h":
                    h_in = v2
                    hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                    st.write(f"1. En tablas para **{v1} bar**: $h_f = {hf:.2f}$ y $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        st.info(f"**Líquido Comprimido**: $h$ ({h_in}) < $h_f$.")
                    elif h_in > hg:
                        st.warning(f"**Vapor Sobrecalentado**: $h$ ({h_in}) > $h_g$.")
                    else:
                        x = (h_in - hf) / (hg - hf)
                        st.success(f"**Mezcla Bifásica**: El valor está entre $h_f$ y $h_g$.")
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")
                    
                    t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                    p_plot = v1
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- DIBUJO DE GRÁFICOS ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min + 0.1, t_crit - 0.5, 100)
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                # Campana
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf+sg[::-1], y=[t-273.15 for t in t_vec]*2, fill='toself', name='Campana', line=dict(color='gray')))
                
                # ISOBARA (P constante)
                s_iso = np.linspace(min(sf)*0.8, max(sg)*1.2, 100)
                t_iso = [PropsSI('T', 'P', p_pa, 'S', s*1000, sustancia)-273.15 for s in s_iso]
                fig.add_trace(go.Scatter(x=s_iso, y=t_iso, name=f'Isobara {v1} bar', line=dict(dash='dash', color='orange')))
                
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=15), name='ESTADO'))

            else: # P-v
                # Campana
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                pf = [PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf+vg[::-1], y=pf+pf[::-1], fill='toself', name='Campana', line=dict(color='gray')))
                
                # ISOTERMA (T constante)
                v_iso = np.logspace(np.log10(min(vf)*0.5), np.log10(max(vg)*2), 100)
                p_iso = [PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000 for v in v_iso]
                fig.add_trace(go.Scatter(x=v_iso, y=p_iso, name=f'Isoterma {t_plot:.1f}°C', line=dict(dash='dash', color='purple')))
                
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=15), name='ESTADO'))
                fig.update_layout(xaxis_type="log", yaxis_type="log")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
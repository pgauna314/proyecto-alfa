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
                t_k_base = v1 + 273.15
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
            # --- 1. INICIALIZACIÓN CRÍTICA ---
            # Esto evita el error "local variable not associated with a value"
            t_plot, s_plot, p_plot, v_plot = 0.0, 0.0, 0.0, 0.0

            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                # CASO P y T
                if par == "P y T":
                    t_in = v2
                    t_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
                    st.write(f"1. A una presión de **{v1} bar**, la temperatura de saturación es **{t_sat:.2f} °C**.")
                    
                    if t_in < t_sat - 0.1:
                        st.info(f"**Resultado:** Líquido Comprimido ({t_in} < {t_sat:.2f})")
                    elif t_in > t_sat + 0.1:
                        st.warning(f"**Resultado:** Vapor Sobrecalentado ({t_in} > {t_sat:.2f})")
                    else:
                        st.success("**Resultado:** Estado de Saturación.")
                    
                    t_plot, p_plot = t_in, v1
                    s_plot = PropsSI('S', 'P', p_pa, 'T', t_in + 273.15, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa, 'T', t_in + 273.15, sustancia)

                # CASO P y h
                elif par == "P y h":
                    h_in = v2
                    hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                    st.write(f"1. Límites a **{v1} bar**: $h_f = {hf:.2f}$, $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        st.info(f"**Resultado:** Líquido Comprimido ($h < h_f$)")
                    elif h_in > hg:
                        st.warning(f"**Resultado:** Vapor Sobrecalentado ($h > h_g$)")
                    else:
                        x = (h_in*1000 - hf*1000) / (hg*1000 - hf*1000)
                        st.success(f"**Resultado:** Mezcla con título:")
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")
                    
                    t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                    p_plot, v_plot = v1, 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

                # CASO P y x
                elif par == "P y x":
                    x_in = v2
                    st.success(f"**Resultado:** Mezcla saturada definida por título $x = {x_in}$")
                    t_plot = PropsSI('T', 'P', p_pa, 'Q', x_in, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa, 'Q', x_in, sustancia) / 1000
                    p_plot, v_plot = v1, 1 / PropsSI('D', 'P', p_pa, 'Q', x_in, sustancia)

                # CASO T y x
                elif par == "T y x":
                    x_in = v2
                    t_k = v1 + 273.15
                    st.success(f"**Resultado:** Mezcla saturada a {v1} °C")
                    p_pa_calc = PropsSI('P', 'T', t_k, 'Q', x_in, sustancia)
                    p_plot = p_pa_calc / 100000
                    t_plot = v1
                    s_plot = PropsSI('S', 'T', t_k, 'Q', x_in, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'T', t_k, 'Q', x_in, sustancia)

            # --- 2. GRÁFICOS (con rangos seguros) ---
            t_crit = PropsSI('Tcrit', sustancia) - 273.15
            t_min = PropsSI('Tmin', sustancia) - 273.15
            t_vec = np.linspace(t_min + 1, t_crit - 0.5, 100)
            
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t+273.15, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t+273.15, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=list(t_vec) + list(t_vec)[::-1], fill='toself', fillcolor='rgba(0,100,255,0.1)', line=dict(color='blue'), name='Campana'))
                
                # Isobara
                s_range = np.linspace(min(sf)*0.8, max(sg)*1.2, 50)
                t_iso = []
                s_iso_final = []
                for s in s_range:
                    try:
                        temp = PropsSI('T', 'P', p_plot*100000, 'S', s*1000, sustancia) - 273.15
                        if temp < 1000:
                            t_iso.append(temp)
                            s_iso_final.append(s)
                    except: continue
                fig.add_trace(go.Scatter(x=s_iso_final, y=t_iso, line=dict(color='orange', dash='dot'), name='Isobara'))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Estado'))
                fig.update_layout(yaxis=dict(range=[t_min-10, max(t_crit, t_plot)+50]), xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")

            else: # P-v
                vf = [1/PropsSI('D', 'T', t+273.15, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t+273.15, 'Q', 1, sustancia) for t in t_vec]
                psat = [PropsSI('P', 'T', t+273.15, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=psat + psat[::-1], fill='toself', fillcolor='rgba(0,255,100,0.1)', line=dict(color='green'), name='Campana'))
                
                v_range = np.logspace(np.log10(min(vf)*0.5), np.log10(max(vg)*10), 50)
                p_iso = []
                v_iso_final = []
                for v in v_range:
                    try:
                        pres = PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000
                        p_iso.append(pres)
                        v_iso_final.append(v)
                    except: continue
                fig.add_trace(go.Scatter(x=v_iso_final, y=p_iso, line=dict(color='purple', dash='dot'), name='Isoterma'))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Estado'))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")
import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

# --- PALETA OKABE-ITO (Accesibilidad) ---
PALETA = {
    "Termica": "#D55E00",    # Bermellón (Isobara/Calor)
    "Fluido": "#0072B2",     # Azul (Campana/Agua)
    "Estado": "#E69F00",     # Naranja (Punto actual)
    "Renovable": "#009E73",  # Verde (P-v)
    "Fondo": "#F0F2F6"
}

def call_cp(target, p1, v1, p2, v2, fluid):
    """Llamada segura a CoolProp para Python 3.12."""
    # Convertimos a bytes solo si es necesario, 
    # pero en 3.12 con la librería bien instalada, el string suele andar.
    return PropsSI(target, p1, v1, p2, v2, fluid)

def mostrar_laboratorio():
    st.title("🧪 Calculadora de Propiedades")
    st.markdown("Cálculo de estados termodinámicos - **Proyecto α**")

    # --- CONFIGURACIÓN ---
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            sustancia = st.selectbox("Sustancia:", ["Water", "Ammonia", "Air", "R134a"])
        with c2:
            par = st.selectbox("Par de variables:", ["P y T", "P y x", "P y h"])
        with c3:
            diagrama = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            v1 = st.number_input("Presión (bar)", value=1.013, format="%.3f")
            p_pa = v1 * 100000 # Conversión a Pascales
        with i2:
            if "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=25.0)
                prop2_val = v2 + 273.15
                prop2_name = 'T'
            elif "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
                prop2_val = v2
                prop2_name = 'Q'
            else: # h
                v2 = st.number_input("Entalpía (kJ/kg)", value=100.0)
                prop2_val = v2 * 1000
                prop2_name = 'H'
        with i3:
            st.write("")
            st.write("")
            calcular = st.button("🚀 Calcular", type="primary", use_container_width=True)

    if calcular:
        try:
            # --- CÁLCULOS ---
            t_k = call_cp('T', 'P', p_pa, prop2_name, prop2_val, sustancia)
            s_jkg = call_cp('S', 'P', p_pa, prop2_name, prop2_val, sustancia)
            d_kgm3 = call_cp('D', 'P', p_pa, prop2_name, prop2_val, sustancia)
            h_jkg = call_cp('H', 'P', p_pa, prop2_name, prop2_val, sustancia)

            # --- RESULTADOS ---
            st.subheader("📊 Resultados en Estado Estable")
            res1, res2, res3, res4 = st.columns(4)
            res1.metric("Temperatura", f"{t_k - 273.15:.2f} °C")
            res2.metric("Densidad", f"{d_kgm3:.2f} kg/m³")
            res3.metric("Entropía", f"{s_jkg/1000:.3f} kJ/kgK")
            res4.metric("Entalpía", f"{h_jkg/1000:.1f} kJ/kg")

            # --- GRÁFICO ---
            t_crit = call_cp('T_critical', 'P', 0, 'T', 0, sustancia)
            t_min = call_cp('Tmin', 'P', 0, 'T', 0, sustancia)
            t_vec = np.linspace(t_min + 0.1, t_crit - 0.1, 50)

            fig = go.Figure()

            if "T-s" in diagrama:
                sf = [call_cp('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [call_cp('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                
                # Campana (Azul Fluido)
                fig.add_trace(go.Scatter(x=sf+sg[::-1], y=[t-273.15 for t in t_vec]+[t-273.15 for t in t_vec][::-1], 
                                         fill='toself', fillcolor='rgba(0, 114, 178, 0.1)', 
                                         line=dict(color=PALETA["Fluido"]), name="Campana"))
                # Punto de Estado (Naranja)
                fig.add_trace(go.Scatter(x=[s_jkg/1000], y=[t_k-273.15], mode='markers', 
                                         marker=dict(color=PALETA["Estado"], size=15, symbol='diamond'), name="Estado Actual"))
                fig.update_layout(xaxis_title="Entropía [kJ/kgK]", yaxis_title="Temperatura [°C]")
            
            else: # P-v
                vf = [1/call_cp('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/call_cp('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                psat = [call_cp('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]
                
                fig.add_trace(go.Scatter(x=vf+vg[::-1], y=psat+psat[::-1], fill='toself', 
                                         fillcolor='rgba(0, 158, 115, 0.1)', line=dict(color=PALETA["Renovable"]), name="Campana"))
                fig.add_trace(go.Scatter(x=[1/d_kgm3], y=[v1], mode='markers', 
                                         marker=dict(color=PALETA["Termica"], size=15, symbol='diamond'), name="Estado"))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="Vol. Esp [m³/kg]", yaxis_title="Presión [bar]")

            fig.update_layout(template="plotly_white", height=500)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.info("💡 Configurá los parámetros y presioná **Calcular**.")

if __name__ == "__main__":
    mostrar_laboratorio()
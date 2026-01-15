import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from CoolProp.CoolProp import PropsSI

# --- PALETA OKABE-ITO ---
PALETA = {
    "Saturacion": "#0072B2", 
    "Ciclo": "#D55E00",      
    "Fondo": "rgba(86, 180, 233, 0.1)"
}

def render_graficos():
    st.subheader("📊 Diagrama T-s Dinámico")
    
    try:
        # 1. Generar campana de saturación con CoolProp
        # Calcular curva de líquido saturado
        T_crit = PropsSI('TCRIT', 'Water') - 273.15  # Temperatura crítica en °C
        T_range = np.linspace(0.01, T_crit - 0.1, 100)  # Desde casi 0°C hasta casi crítica
        
        s_liquid = []
        s_vapor = []
        T_points = []
        
        for T_C in T_range:
            try:
                T_K = T_C + 273.15
                # Punto de líquido saturado
                s_l = PropsSI('S', 'T', T_K, 'Q', 0, 'Water') / 1000  # kJ/kgK
                # Punto de vapor saturado
                s_v = PropsSI('S', 'T', T_K, 'Q', 1, 'Water') / 1000  # kJ/kgK
                
                s_liquid.append(s_l)
                s_vapor.append(s_v)
                T_points.append(T_C)
            except:
                continue
        
        # Crear DataFrame para la campana
        df_campana = pd.DataFrame({
            'T': T_points,
            's_liquid': s_liquid,
            's_vapor': s_vapor
        })
        
        # 2. Cálculo de Ciclo Rankine Real
        P_alta = 10e5  # 10 bar = 1e6 Pa
        P_baja = 0.1e5  # 0.1 bar = 10e3 Pa
        T_sobrecalentado = 350 + 273.15  # 350°C
        
        # Estado 1: Líquido saturado a P_baja (entrada bomba)
        try:
            s1 = PropsSI('S', 'P', P_baja, 'Q', 0, 'Water') / 1000
            T1 = PropsSI('T', 'P', P_baja, 'Q', 0, 'Water') - 273.15
        except Exception as e:
            st.error(f"Error en estado 1: {e}")
            s1, T1 = 0.5, 50
        
        # Estado 2: Salida bomba (líquido comprimido a P_alta, isoentrópico)
        try:
            # Para bomba isoentrópica, s2 = s1
            s2 = s1
            # Buscar temperatura a P_alta con s constante
            T2 = PropsSI('T', 'P', P_alta, 'S', s1*1000, 'Water') - 273.15
        except Exception as e:
            st.error(f"Error en estado 2: {e}")
            s2, T2 = s1, T1 + 10
        
        # Puntos intermedios para evaporación a P_alta
        try:
            # Líquido saturado a P_alta
            s3_l = PropsSI('S', 'P', P_alta, 'Q', 0, 'Water') / 1000
            T3 = PropsSI('T', 'P', P_alta, 'Q', 0, 'Water') - 273.15
            
            # Vapor saturado a P_alta
            s3_v = PropsSI('S', 'P', P_alta, 'Q', 1, 'Water') / 1000
        except Exception as e:
            st.error(f"Error en evaporación: {e}")
            s3_l, s3_v = s2 + 1, s2 + 5
            T3 = T2 + 100
        
        # Estado 4: Vapor sobrecalentado
        try:
            s4 = PropsSI('S', 'P', P_alta, 'T', T_sobrecalentado, 'Water') / 1000
            T4 = T_sobrecalentado - 273.15
        except Exception as e:
            st.error(f"Error en estado 4: {e}")
            s4, T4 = s3_v + 1, T3 + 100
        
        # Estado 5: Salida turbina (a P_baja, isoentrópico)
        try:
            s5 = s4  # Expansión isoentrópica
            # Calcular calidad para verificar si está en zona bifásica
            try:
                # Intentar obtener temperatura directamente
                T5 = PropsSI('T', 'P', P_baja, 'S', s4*1000, 'Water') - 273.15
            except:
                # Si falla, calcular calidad
                s_l = PropsSI('S', 'P', P_baja, 'Q', 0, 'Water') / 1000
                s_v = PropsSI('S', 'P', P_baja, 'Q', 1, 'Water') / 1000
                calidad = (s4 - s_l) / (s_v - s_l)
                T5 = PropsSI('T', 'P', P_baja, 'Q', calidad, 'Water') - 273.15
        except Exception as e:
            st.error(f"Error en estado 5: {e}")
            s5, T5 = s4, T4 - 100
        
        # Construir el ciclo en orden correcto
        # 1→2: Compresión en bomba
        # 2→3: Calentamiento del líquido comprimido hasta saturación
        # 3→3': Evaporación (líquido saturado a vapor saturado)
        # 3'→4: Sobrecalentamiento
        # 4→5: Expansión en turbina
        # 5→1: Condensación
        
        s_ciclo = [s1, s2, s3_l, s3_v, s4, s5, s1]
        T_ciclo = [T1, T2, T3, T3, T4, T5, T1]
        
        # Mostrar datos de depuración
        with st.expander("🔍 Datos de depuración"):
            st.write("**Campana:**")
            st.write(f"Temperatura crítica: {T_crit:.1f} °C")
            st.write(f"Puntos calculados: {len(df_campana)}")
            
            st.write("**Estados del ciclo:**")
            estados_data = {
                'Estado': ['1', '2', '3 (líq sat)', "3' (vap sat)", '4', '5'],
                's [kJ/kgK]': [f"{s:.3f}" for s in [s1, s2, s3_l, s3_v, s4, s5]],
                'T [°C]': [f"{T:.1f}" for T in [T1, T2, T3, T3, T4, T5]]
            }
            st.table(pd.DataFrame(estados_data))
        
        # Crear figura
        fig = go.Figure()
        
        # Dibujar campana de saturación
        if len(df_campana) > 0:
            # Curva de líquido saturado
            fig.add_trace(go.Scatter(
                x=df_campana['s_liquid'],
                y=df_campana['T'],
                mode='lines',
                line=dict(color=PALETA["Saturacion"], width=2),
                name='Líquido saturado'
            ))
            
            # Curva de vapor saturado
            fig.add_trace(go.Scatter(
                x=df_campana['s_vapor'],
                y=df_campana['T'],
                mode='lines',
                line=dict(color=PALETA["Saturacion"], width=2),
                name='Vapor saturado',
                fill='tonexty',
                fillcolor=PALETA["Fondo"]
            ))
        
        # Dibujar ciclo Rankine
        fig.add_trace(go.Scatter(
            x=s_ciclo,
            y=T_ciclo,
            mode='lines+markers',
            line=dict(color=PALETA["Ciclo"], width=3),
            fill='toself',
            fillcolor='rgba(213, 94, 0, 0.2)',
            marker=dict(size=8, color=PALETA["Ciclo"]),
            name='Ciclo Rankine Real'
        ))
        
        # Etiquetar estados
        estados_labels = ['1', '2', '3', "3'", '4', '5']
        for i, (s, T, label) in enumerate(zip(s_ciclo[:-1], T_ciclo[:-1], estados_labels)):
            if label:  # Solo para estados con etiqueta
                fig.add_annotation(
                    x=s,
                    y=T,
                    text=f"<b>{label}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=PALETA["Ciclo"],
                    font=dict(size=14, color=PALETA["Ciclo"]),
                    bgcolor="white",
                    bordercolor=PALETA["Ciclo"],
                    borderwidth=1,
                    borderpad=4
                )
        
        # Configurar layout
        fig.update_layout(
            template="plotly_white",
            title="Diagrama Temperatura-Entropía (T-s) del Agua",
            xaxis_title="Entropía específica, s [kJ/kg·K]",
            yaxis_title="Temperatura, T [°C]",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.8)"
            ),
            hovermode='closest',
            width=800,
            height=600
        )
        
        # Configurar ejes
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Información sobre el ciclo
        st.markdown("""
        ### 📖 Explicación del Ciclo Rankine
        **Estados:**
        1. **Líquido saturado** a baja presión (entrada bomba)
        2. **Líquido comprimido** a alta presión (salida bomba)
        3. **Líquido saturado** a alta presión (entrada caldera)
        3'. **Vapor saturado** a alta presión (fin evaporación)
        4. **Vapor sobrecalentado** a alta presión (salida caldera)
        5. **Mezcla líquido-vapor** a baja presión (salida turbina)
        
        **Procesos:**
        - **1→2**: Compresión isoentrópica en bomba
        - **2→3→3'**: Calentamiento isobárico en caldera
        - **3'→4**: Sobrecalentamiento isobárico
        - **4→5**: Expansión isoentrópica en turbina
        - **5→1**: Condensación isobárica en condensador
        """)
        
    except Exception as e:
        st.error(f"❌ Error en el cálculo: {str(e)}")
        st.info("💡 **Solución de problemas:**")
        st.write("1. Verifica que CoolProp esté instalado: `pip install CoolProp`")
        st.write("2. Asegúrate de usar 'Water' como fluido (no 'water' en minúsculas)")
        st.write("3. Las presiones deben estar en Pascales (1 bar = 100,000 Pa)")
        st.write("4. Las temperaturas deben estar en Kelvin para los cálculos")
        
        # Mostrar traza completa del error en modo expandible
        with st.expander("🔧 Detalles técnicos del error"):
            import traceback
            st.code(traceback.format_exc())

# Nota: Para ejecutar esta función en Streamlit, asegúrate de tener:
# pip install streamlit plotly pandas numpy CoolProp
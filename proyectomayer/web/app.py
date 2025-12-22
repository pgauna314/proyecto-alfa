import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", ["Inicio", "Capítulo II: Sistemas"])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# 3. Contenido Principal
if menu == "Inicio":
    st.title("Estudio de Sistemas Térmicos")
    st.write("Bienvenido a la plataforma interactiva del Proyecto MAYER.")

elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Análisis de Sistemas: El Generador de Vapor")
    
    st.markdown("### Esquema de Flujos y Límites del Sistema")
    
    # Diagrama de Graphviz
    st.graphviz_chart('''
        digraph {
            rankdir=LR;
            node [shape=box, style=filled, color=lightgrey, fontname="Arial"];
            
            subgraph cluster_0 {
                label = "VOLUMEN DE CONTROL (Secundario)";
                color=red;
                style=dashed;
                GV [label="GENERADOR DE VAPOR", shape=cylinder, fillcolor=white];
            }
            
            Entrada [label="Agua de Alimentación\\n(m_ent, h_ent)", fillcolor="#e1f5fe"];
            Salida [label="Vapor Saturado\\n(m_sal, h_sal)", fillcolor="#fff9c4"];
            Primario [label="Calor Primario (Q)\\nReactor", shape=ellipse, fillcolor="#ffcdd2"];
            
            Entrada -> GV [label=" m_ent"];
            GV -> Salida [label=" m_sal"];
            Primario -> GV [style=bold, color=red, label=" Q_transferido"];
        }
    ''')

    st.info("Este diagrama representa el balance de un sistema abierto. El límite (línea roja) define qué flujos cruzan la frontera.")

    # Resto de los cálculos...




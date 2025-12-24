import streamlit as st
import sys
import os

actual_dir = os.path.dirname(os.path.abspath(__file__))
if actual_dir not in sys.path:
    sys.path.append(actual_dir)

# IMPORTAR TODOS LOS MÓDULOS
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
from modules.laboratorio import mostrar_laboratorio
# NO importes wiki aquí; se importa solo cuando se necesita

st.set_page_config(page_title="Proyecto α - Termodinámica", layout="wide", page_icon="α")

# BARRA LATERAL CON MENÚ
with st.sidebar:
    menu = st.radio("Entorno de Trabajo:", [
        "Inicio (Proyecto α)", 
        "Matriz Energética Nacional", 
        "Módulo Σ: Simulador de Procesos", 
        "Módulo λ: Fundamentos de Sistemas",
        "Wiki",          # ← esta línea debe estar
        "Autor"
    ])

# ENRUTADOR
if menu == "Inicio (Proyecto α)":
    mostrar_inicio()
elif menu == "Matriz Energética Nacional":
    mostrar_matriz()
elif menu == "Módulo Σ: Simulador de Procesos":
    mostrar_laboratorio()
elif menu == "Módulo λ: Fundamentos de Sistemas":
    mostrar_cap2()
elif menu == "Wiki":
    from modules import wiki  # ← se importa aquí, solo cuando se elige
    wiki.main()
elif menu == "Autor":
    mostrar_autor()
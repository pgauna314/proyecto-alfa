import streamlit as st
from pathlib import Path
import os

def main():
    st.title("📚 Wiki")
    st.markdown("Explorá la historia y tecnología de las centrales eléctricas argentinas.")

    # **LÍNEA CLAVE CORREGIDA:**
    # Esto sube desde 'modules' hasta 'web', y luego entra a 'wiki_data'
    base_dir = Path(__file__).parent.parent  # Ahora apunta a /web
    wiki_content_dir = base_dir / "wiki_data"

    st.sidebar.info(f"Buscando en: {wiki_content_dir}")  # Línea para depurar
    st.sidebar.write("---")
    st.sidebar.subheader("🔍 Depuración de rutas")    

    entries = {
        "Río Turbio": "centrales/rio-turbio.md",  # Ruta RELATIVA a wiki_data/
    }

    selected = st.selectbox("Seleccioná una entrada", list(entries.keys()))
    
    # Construir la ruta final
    file_path = wiki_content_dir / entries[selected]

    if file_path.exists():
        st.markdown(file_path.read_text(encoding="utf-8"))
    else:
        # Mensaje de error más informativo
        st.error(f"❌ Archivo no encontrado.")
        st.code(f"Ruta buscada: {file_path}")

# Nota: Asegúrate de que en app.py se llame a esta función así:
# from modules.wiki import main as wiki_main; wiki_main()
import streamlit as st
from pathlib import Path

def main():
    st.title("📚 Wiki")
    st.markdown("Explorá la historia y tecnología de las centrales eléctricas argentinas.")

    # Obtener la ruta base del proyecto (web/)
    base_dir = Path(__file__).parent.parent  # Esto sube de modules/ a web/
    
    entries = {
        "Río Turbio": "wiki_data/centrales/rio-turbio.md",
    }

    selected = st.selectbox("Seleccioná una entrada", list(entries.keys()))
    
    # Construir la ruta completa
    path = base_dir / entries[selected]

    # Para depuración (puedes comentar luego)
    st.write(f"Base dir: {base_dir}")
    st.write(f"Ruta buscada: {path}")
    st.write(f"¿Existe?: {path.exists()}")

    if path.exists():
        st.markdown(path.read_text(encoding="utf-8"))
    else:
        st.error(f"⚠️ Archivo no encontrado: {path}")
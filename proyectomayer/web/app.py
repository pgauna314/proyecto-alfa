# web/modules/wiki.py
import streamlit as st
from pathlib import Path

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Explorá la historia y tecnología de las centrales eléctricas argentinas.")

    entries = {
        "Río Turbio": "wiki_data/centrales/rio-turbio.md",
    }

    selected = st.selectbox("Seleccioná una entrada", list(entries.keys()))
    path = Path(entries[selected])

    # --- LÍNEAS DE DEBUG (OPCIONALES PERO ÚTILES) ---
    # st.write("Ruta buscada:", path.resolve())
    # st.write("¿Existe?", path.exists())

    if path.exists():
        st.markdown(path.read_text(encoding="utf-8"))
    else:
        st.warning("⚠️ Entrada en construcción.")
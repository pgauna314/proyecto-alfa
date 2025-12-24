import streamlit as st
from pathlib import Path

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Explorá la historia, tecnología y contexto de las centrales eléctricas argentinas.")

    # Definir entradas
    entries = {
        "Río Turbio": "wiki_data/centrales/rio-turbio.md",
        "Atucha II": "wiki_data/centrales/atucha-ii.md",
        "San Nicolás": "wiki_data/centrales/san-nicolas.md",
        "Soberanía energética": "wiki_data/conceptos/soberania-energetica.md",
    }

    selected = st.selectbox("Seleccioná una entrada:", list(entries.keys()))
    path = Path(entries[selected])

    if path.exists():
        st.markdown(path.read_text(encoding="utf-8"))
    else:
        st.warning("⚠️ Entrada en construcción.")
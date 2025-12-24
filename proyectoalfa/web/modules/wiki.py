# modules/wiki.py
import streamlit as st
from pathlib import Path

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Fichas técnicas de centrales eléctricas.")
    
    # Ruta a wiki_data: desde modules/ → salir a proyectomayer/ → entrar a wiki_data/
    wiki_dir = Path(__file__).parent.parent / "wiki_data"
    entries = {
        "Río Turbio": "centrales/rio-turbio.md",
    }
    
    selected = st.selectbox("Seleccioná una central", list(entries.keys()))
    file_path = wiki_dir / entries[selected]
    
    if file_path.exists():
        st.markdown(file_path.read_text(encoding="utf-8"))
    else:
        st.error(f"❌ Archivo no encontrado:\n`{file_path}`")
        if wiki_dir.exists():
            st.write("Archivos en wiki_data:")
            st.write([f.name for f in wiki_dir.rglob("*.md")])
        else:
            st.warning("⚠️ La carpeta `wiki_data` no existe.")
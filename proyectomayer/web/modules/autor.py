import streamlit as st

def mostrar_autor():
    st.title("👤 Sobre el Autor y el Proyecto")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Aquí podés poner tu foto. Por ahora dejamos un placeholder.
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
    
    with col2:
        st.subheader("Tu Nombre / Institución")
        st.write("""
        Ingeniero / Docente / Investigador apasionado por la termodinámica 
        y la generación de energía a gran escala.
        
        El **Proyecto MAYER** nace de la necesidad de cerrar la brecha entre 
        las ecuaciones de los libros de texto y la operación real de una 
        central como Atucha II.
        """)
        
        st.markdown("### Contacto y Redes")
        st.write("📩 [tu@email.com](mailto:tu@email.com)")
        st.write("🔗 [LinkedIn / Portfolio](https://linkedin.com)")

    st.divider()
    
    st.subheader("La Visión del Proyecto")
    st.info("""
    "La ingeniería no se aprende solo leyendo, se aprende rompiendo y reconstruyendo balances." 
    Este entorno interactivo es el resultado de buscar una pedagogía 4.0 para la ingeniería nuclear argentina.
    """)

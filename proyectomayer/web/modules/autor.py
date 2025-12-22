import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Sobre el Autor")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Intentamos las dos rutas más comunes en Streamlit Cloud
        ruta_foto = "web/assets/autor.jpg"
        ruta_alt = "assets/autor.jpg"
        
        if os.path.exists(ruta_foto):
            st.image(ruta_foto, width=250)
        elif os.path.exists(ruta_alt):
            st.image(ruta_alt, width=250)
        else:
            # Avatar genérico si la foto falla
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
            st.caption("Imagen no encontrada en assets/autor.jpg")
    
    with col2:
        st.header("Ing. Gauna")
        st.markdown("""
        **Autor del Proyecto MAYER** Especialista en Ingeniería Térmica y Sistemas Nucleares.
        
        Este entorno digital complementa el estudio detallado de los sistemas de la 
        Central Nuclear Atucha II, permitiendo una transición fluida entre la 
        teoría del libro y la práctica computacional.
        """)
        
        st.info("📩 **Contacto:** [tu-email@correo.com](mailto:tu-email@correo.com)")

    # Separador visual
    st.divider()
    
    # Aquí podrías usar el TXT que mencionaste si contiene alguna descripción extra
    st.subheader("El Proyecto")
    st.write("Desarrollado para optimizar el aprendizaje de balances de masa y energía.")

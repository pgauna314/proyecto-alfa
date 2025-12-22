import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Sobre el Autor y el Proyecto")
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        # Intentamos varias rutas posibles para que no falle en el servidor
        posibles_rutas = [
            "web/assets/fotoGauna2.jpg",
            "assets/fotoGauna2.jpg",
            "fotoGauna2.jpg"
        ]
        
        foto_cargada = False
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                st.image(ruta, width=250, use_container_width=True)
                foto_cargada = True
                break
        
        if not foto_cargada:
            # Placeholder si la ruta falla
            st.warning("Foto no encontrada. Verifique que esté en web/assets/")
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
    
    with col2:
        st.header("Ing. Gauna")
        st.subheader("Autor del Proyecto MAYER")
        
        st.write("""
        Especialista en Sistemas Térmicos y Energía Nuclear. 
        Este proyecto es el resultado de la integración entre el análisis técnico 
        de Atucha II y las nuevas tecnologías de visualización de datos.
        
        El objetivo es proporcionar a los estudiantes y profesionales una herramienta 
        dinámica para comprender los balances de masa y energía en centrales de potencia.
        """)
        
        st.divider()
        
        # Iconos de contacto (puedes cambiarlos)
        c1, c2 = st.columns(2)
        with c1:
            st.write("📩 **Contacto:** [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)")
        with c2:
            st.write("🔗 **LinkedIn:** [Perfil Profesional](https://linkedin.com)")

    st.divider()
    st.markdown("#### Sobre el Proyecto MAYER")
    st.info("El nombre del proyecto rinde homenaje a la excelencia en ingeniería térmica y busca democratizar el acceso a simuladores técnicos de alta precisión.")


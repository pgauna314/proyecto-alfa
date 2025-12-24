import streamlit as st

def mostrar_autor():
    """Muestra la información del autor del proyecto"""
    
    st.header("👤 Autor del Proyecto α")
    st.markdown("---")
    
    # Usar columnas para mejor presentación
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Puedes poner una imagen si tienes: st.image("tu_foto.jpg")
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #4CAF50; border-radius: 10px;'>
        <span style='font-size: 50px;'>👨‍💻</span><br>
        <strong>Foto</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Pablo Gauna")
        st.markdown("""
        **Rol:** Desarrollador y Estudiante  
        **Formación:** Ingeniería en Energía  
        **Contacto:** pgauna314@gmail.com  
        **GitHub:** [pgauna314](https://github.com/pgauna314)
        """)
    
    st.markdown("---")
    
    # Sección de motivación
    st.subheader("🚀 Motivación del Proyecto")
    
    st.markdown("""
    Este proyecto nace de una necesidad concreta: **fusionar el rigor académico con la realidad productiva nacional**.
    
    ### Objetivos principales:
    
    1.  **🔧 Herramientas propias**: Desarrollar software educativo adaptado a nuestra industria energética.
    2.  **📚 Contexto local**: Analizar casos reales de centrales argentinas, no ejemplos genéricos.
    3.  **🎓 Soberanía educativa**: Proveer recursos libres para la formación de ingenieros.
    4.  **🌐 Accesibilidad**: Crear una plataforma web gratuita para estudiantes y profesionales.
    
    ### Filosofía:
    
    > "No podemos depender de manuales extranjeros que ignoran nuestra matriz energética. 
    > La termodinámica se aprende aplicándola a Río Turbio, Yacyretá o Cañadón León, 
    > no a casos teóricos descontextualizados."
    """)
    
    st.markdown("---")
    
    # Agradecimientos
    st.subheader("🙏 Agradecimientos")
    st.markdown("""
    - A los docentes que fomentan el pensamiento crítico y la creación de herramientas propias.
    - A la comunidad open-source que hace posible proyectos como este.
    - A los ingenieros de las centrales argentinas, cuya experiencia es la verdadera fuente de datos.
    """)
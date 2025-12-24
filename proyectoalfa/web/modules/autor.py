import streamlit as st

def mostrar_autor():
    st.title("👨‍💻 Autor del Proyecto α")
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border: 2px solid #4CAF50; border-radius: 10px;'>
        <span style='font-size: 60px;'>👤</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Pablo Gauna")
        st.markdown("""
        **📧 Contacto:** pgauna314@gmail.com  
        **🐙 GitHub:** [pgauna314](https://github.com/pgauna314)  
        **🎓 Formación:** Ingeniería en Energía  
        **📍 Ubicación:** Argentina
        """)
    
    st.divider()
    
    st.markdown("""
    ### 🚀 Motivación del Proyecto
    
    Este proyecto nace de la necesidad de contar con **herramientas educativas propias** 
    para el estudio de la termodinámica, adaptadas a la realidad energética argentina.
    
    **Objetivos principales:**
    1. Crear software educativo libre y accesible
    2. Contextualizar la teoría con casos de centrales argentinas
    3. Promover la soberanía tecnológica en la formación de ingenieros
    
    ### 💡 Filosofía
    > "No podemos depender únicamente de manuales extranjeros que ignoran 
    > nuestra matriz energética. La termodinámica se aprende aplicándola 
    > a casos reales de nuestra industria."
    """)
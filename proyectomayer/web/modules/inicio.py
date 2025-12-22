import streamlit as st

def mostrar_inicio():
    st.title("🚀 Proyecto MAYER")
    st.subheader("Plataforma Interactiva de Ingeniería Nuclear y Térmica")
    
    st.markdown("""
    Bienvenido al soporte digital del libro **Estudio de Sistemas Térmicos: Atucha II**. 
    Este entorno ha sido diseñado para que los conceptos teóricos del libro 
    cobren vida mediante simulaciones y datos en tiempo real.
    
    ### 📖 ¿Cómo utilizar esta plataforma?
    1. **Navegación:** Utilizá el menú de la izquierda para moverte entre capítulos.
    2. **Interactividad:** Encontrarás sliders y gráficos que podés manipular para ver cómo cambian los balances de energía.
    3. **Datos Reales:** La sección de Matriz Energética se alimenta de datos del SADI para contextualizar el aporte de la central.
    """)
    
    st.info("💡 **Consejo:** Tené el libro a mano. Cuando veas el ícono de 'Web' en las páginas del PDF, significa que hay un módulo interactivo esperándote aquí.")

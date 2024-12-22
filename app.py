import streamlit as st
from pages import dashboard, bilanco, gelir_tablosu, rasyo_analiz

# Sayfa yönlendirme
def main():
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfa Seçimi", ("Dashboard", "Bilanço", "Gelir Tablosu", "Rasyo Analiz"))
    
    if page == "Dashboard":
        dashboard.show()
    elif page == "Bilanço":
        bilanco.show()
    elif page == "Gelir Tablosu":
        gelir_tablosu.show()
    elif page == "Rasyo Analiz":
        rasyo_analiz.show()

if __name__ == "__main__":
    main()

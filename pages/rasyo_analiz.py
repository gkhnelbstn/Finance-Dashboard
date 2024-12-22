import streamlit as st
import pandas as pd

def load_data(filepath):
    try:
        return pd.read_excel(filepath, sheet_name=None)
    except Exception as e:
        st.error(f"Excel dosyası okunurken hata oluştu: {e}")
        return None

def show():
    st.title("📊 Rasyo Analiz Tabloları")
    filepath = "./data/rasyo_analiz.xlsx"
    data = load_data(filepath)
    
    if data:
        sheet_names = list(data.keys())
        selected_sheet = st.sidebar.selectbox("Sayfa Seçimi", sheet_names)
        st.write(f"**{selected_sheet}** sayfası:")
        st.dataframe(data[selected_sheet])
        st.download_button(
            label="CSV olarak indir",
            data=data[selected_sheet].to_csv(index=False).encode('utf-8'),
            file_name=f"{selected_sheet}.csv",
            mime='text/csv',
        )
    else:
        st.warning("Veri yüklenemedi.")

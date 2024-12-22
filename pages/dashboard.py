import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 

def load_balance_sheet(filepath):
    try:
        # Veriyi yükle
        data = pd.read_excel(filepath)
        
        # "Kalem" sütununu indeks olarak ayarla
        data.set_index("Kalem", inplace=True)
        
        # Satır ve sütun isimlerinden baştaki ve sondaki boşlukları kaldır
        data.index = data.index.str.strip()
        data.columns = data.columns.str.strip()
        
        return data
    except Exception as e:
        st.error(f"Veri yüklenemedi: {e}")
        return None


def get_total_by_category(data, category_name):
    try:
        # Belirtilen kategorinin toplam satırını al
        total_row = data.loc[category_name]
        return total_row
    except KeyError:
        st.error(f"Kategori bulunamadı: {category_name}")
        return None



def plot_trend(total_data, title, ylabel):
    fig = px.line(total_data, markers=True, title=title, labels={'index': 'Dönem', 'value': ylabel})
    fig.update_layout(xaxis_title='Dönem', yaxis_title=ylabel)
    st.plotly_chart(fig)

def plot_pie(total_data, title):
    fig = px.pie(total_data, values=total_data.values, names=total_data.index, title=title)
    st.plotly_chart(fig)

def show():
    st.title("📊 Balance Sheet Dashboard")

    # Excel dosyasını yükle
    filepath = "./data/bilanco.xlsx"
    data = load_balance_sheet(filepath)

    if data is not None:
        # Anahtar kategorilerden toplam verileri al
        st.subheader("Toplamlar")
        toplam_varliklar = get_total_by_category(data, "Toplam Dönen Varlıklar") + \
                           get_total_by_category(data, "Toplam Duran Varlıklar")
        toplam_yukumlulukler = get_total_by_category(data, "Toplam Kısa Vadeli Yükümlülükler") + \
                               get_total_by_category(data, "Toplam Uzun Vadeli Yükümlülükler")
        toplam_ozkaynaklar = get_total_by_category(data, "Toplam Özkaynaklar")

        if toplam_varliklar is not None and toplam_yukumlulukler is not None and toplam_ozkaynaklar is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("Toplam Varlıklar", f"{toplam_varliklar.sum():,.2f} TRY")
            col2.metric("Toplam Yükümlülükler", f"{toplam_yukumlulukler.sum():,.2f} TRY")
            col3.metric("Toplam Özkaynaklar", f"{toplam_ozkaynaklar.sum():,.2f} TRY")

        # Trend analizleri
        st.subheader("Trend Analizi")
        if toplam_varliklar is not None:
            plot_trend(toplam_varliklar, "Toplam Varlıklar Trend Analizi", "TRY")
        if toplam_yukumlulukler is not None:
            plot_trend(toplam_yukumlulukler, "Toplam Yükümlülükler Trend Analizi", "TRY")
        if toplam_ozkaynaklar is not None:
            plot_trend(toplam_ozkaynaklar, "Toplam Özkaynaklar Trend Analizi", "TRY")

        # Dağılım grafikleri
        st.subheader("Dağılım Grafikleri")
        if toplam_varliklar is not None:
            plot_pie(toplam_varliklar, "Toplam Varlıklar Dağılımı")
        if toplam_yukumlulukler is not None:
            plot_pie(toplam_yukumlulukler, "Toplam Yükümlülükler Dağılımı")
    else:
        st.warning("Veri yüklenemedi. Lütfen dosya yolunu kontrol edin.")

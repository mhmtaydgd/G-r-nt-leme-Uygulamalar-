import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def histogram_equal():
    # Histogram hesaplama fonksiyonu
    def histogram_hesapla(goruntu):
        histogram = np.zeros(256, dtype=int)
        for i in range(goruntu.shape[0]):
            for j in range(goruntu.shape[1]):
                yogunluk = goruntu[i, j]
                histogram[yogunluk] += 1
        return histogram

    # Eşikleme fonksiyonu
    def eşikle(goruntu, eşik_değeri):
        eşiklenmiş_görüntü = np.where(goruntu > eşik_değeri, 255, 0).astype(np.uint8)
        return eşiklenmiş_görüntü


    st.title('Histogram ve Eşikleme Uygulaması')

    # Fotoğraf yükleme
    uploaded_file = st.file_uploader("Lütfen bir fotoğraf yükleyin", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Fotoğrafı yükle
        original_image = Image.open(uploaded_file)
        gray_image = original_image.convert('L')
        gray_image_array = np.array(gray_image)

        # Orijinal görüntünün histogramını hesapla
        original_histogram = histogram_hesapla(gray_image_array)

        # Orijinal görüntüyü göster
        st.subheader('Orijinal Görüntü')
        st.image(original_image, caption='Orijinal Görüntü', use_column_width=True)

        # Orijinal görüntü histogramı
        st.subheader('Orijinal Görüntü Histogramı')
        plt.figure(figsize=(10, 5))
        plt.title('Orijinal Görüntü Histogramı')
        plt.xlabel('Piksel Yoğunluğu')
        plt.ylabel('Frekans')
        plt.bar(range(256), original_histogram, width=1, color='black')
        st.pyplot(plt)

        # Eşik değeri seçme
        threshold = st.slider('Eşik Değeri:', 0, 255, 128)

        if st.button('Histogram Uygula'):
            # Eşikleme işlemi
            eşiklenmiş_görüntü = eşikle(gray_image_array, threshold)

            # Eşiklenmiş görüntüyü gösterme
            st.subheader('Eşiklenmiş Görüntü')
            st.image(eşiklenmiş_görüntü, caption='Eşiklenmiş Görüntü', use_column_width=True)

            # Eşiklenmiş görüntü histogramı
            eşiklenmiş_histogram = histogram_hesapla(eşiklenmiş_görüntü)
            st.subheader('Eşiklenmiş Görüntü Histogramı')
            plt.figure(figsize=(10, 5))
            plt.title('Eşiklenmiş Görüntü Histogramı')
            plt.xlabel('Piksel Yoğunluğu')
            plt.ylabel('Frekans')
            plt.bar(range(256), eşiklenmiş_histogram, width=1, color='black')
            st.pyplot(plt)

if __name__ == "__main__":
    histogram_equal()

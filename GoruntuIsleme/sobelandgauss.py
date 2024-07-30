import cv2
import numpy as np
import streamlit as st
from PIL import Image

def sobel_gauss_canny():
    def sobel_filter(image, threshold):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
        sobely = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
        gradient_x = cv2.filter2D(gray, -1, sobelx)
        gradient_y = cv2.filter2D(gray, -1, sobely)
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        gradient_magnitude = (gradient_magnitude / np.max(gradient_magnitude) * 255).astype(np.uint8)
        thresholded = np.zeros_like(gradient_magnitude)
        thresholded[gradient_magnitude > threshold] = 255
        return thresholded

    def gaussian_kernel(size, sigma=1):
        """Gaussian kernel oluşturma fonksiyonu."""
        k = size // 2
        kernel = np.fromfunction(
            lambda x, y: (1 / (2 * np.pi * sigma**2)) * np.exp(
                - ((x - k)**2 + (y - k)**2) / (2 * sigma**2)),
            (size, size)
        )
        return kernel / np.sum(kernel)

    def apply_gaussian_filter(image, kernel):
        """Görüntüye Gaussian filtresi uygulama fonksiyonu."""
        return cv2.filter2D(image, -1, kernel)
    
    def canny_edge_detection(image, threshold):
        """Canny kenar algılama fonksiyonu."""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        edges = cv2.Canny(blurred_image, threshold // 2, threshold)
        return edges
    
    st.title("Sobel Gauss ve Canny Filtre Uygulama")

    uploaded_file = st.file_uploader("Lütfen bir fotoğraf yükleyin", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        st.image(image, caption='Yüklenen Fotoğraf', use_column_width=True)
        
        sobel_threshold = st.slider("Sobel Eşik Değeri", 0, 255, 100)

        if st.button('Sobel Filtresi Uygula'):
            # Sobel filtresi uygulama
            sobel_image = sobel_filter(image, sobel_threshold)
            st.image(sobel_image, caption='Sobel Filtresi Uygulanmış Fotoğraf', use_column_width=True)
       
        kernel_size = st.slider("Gauss Kernel Boyutu", 3, 15) 
        gauss_threshold = st.slider("Gauss Eşik Değeri", 0, 255, 100)
        
        if st.button('Gauss Filtresi Uygula'):
            # Gaussian filtresi uygulama
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Kernel boyutunun tek sayı olduğundan emin olun
            if kernel_size % 2 == 0:
                kernel_size += 1

            # Gaussian kernel oluştur
            sigma = 1.0  # Sigma değerini sabit tutuyoruz, çünkü kullanıcı eşik değeri giriyor.
            kernel = gaussian_kernel(kernel_size, sigma)

            # Gaussian filtreyi uygula
            filtered_image = apply_gaussian_filter(gray_image, kernel)

            # Eşikleme işlemi
            _, thresholded_image = cv2.threshold(filtered_image, gauss_threshold, 255, cv2.THRESH_BINARY)
            st.image(thresholded_image, caption="Gauss Filtresi Uygulanmış ve Eşiklenmiş Görüntü", use_column_width=True)
        
        canny_threshold = st.slider("Canny Eşik Değeri", 0, 255, 100)
        
        if st.button('Canny Filtresi Uygula'):
            # Canny kenar algılama
            canny_image = canny_edge_detection(image, canny_threshold)
            st.image(canny_image, caption='Canny Kenar Algılama Sonucu', use_column_width=True)

if __name__ == "__main__":
    sobel_gauss_canny()

import streamlit as st
import cv2
from PIL import Image
import numpy as np

def region_grow():
    def region_growing(image, seed, threshold=5):
        rows, cols = image.shape
        segmented_image = np.zeros((rows, cols), dtype=np.uint8)
        visited = np.zeros((rows, cols), dtype=np.bool8)
        
        seed_x, seed_y = seed
        seed_value = image[seed_x, seed_y]
        
        region_points = [(seed_x, seed_y)]
        
        while region_points:
            x, y = region_points.pop(0)
            
            if visited[x, y]:
                continue
            
            visited[x, y] = True
            segmented_image[x, y] = 255
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and not visited[nx, ny]:
                        neighbor_value = image[nx, ny]
                        if abs(int(neighbor_value) - int(seed_value)) <= threshold:
                            region_points.append((nx, ny))
        
        return segmented_image

    st.title("Region Growing")

    uploaded_file = st.file_uploader("Lütfen bir fotoğraf yükleyin", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_array = np.array(image)
        st.image(image, caption='Yüklediğiniz Fotoğraf', use_column_width=True)

        if st.button("Konum"):
            if "mouse_x" not in st.session_state:
                st.session_state.mouse_x = -1
            if "mouse_y" not in st.session_state:
                st.session_state.mouse_y = -1

            def on_mouse(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    st.session_state.mouse_x = x
                    st.session_state.mouse_y = y

            window_name = "Image"
            cv2.imshow(window_name, image_array)
            cv2.setMouseCallback(window_name, on_mouse)

            st.write("Görüntü üzerinde bir noktaya tıklayın ve pencereyi kapatmak için bir tuşa basın.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if st.session_state.mouse_x != -1 and st.session_state.mouse_y != -1:
                x = st.session_state.mouse_x
                y = st.session_state.mouse_y
                color = image_array[y, x]
                st.write(f"Koordinatlar: ({x}, {y})")
                st.write(f"Renk Değeri: {color}")
                st.session_state.seed_x = x
                st.session_state.seed_y = y

        st.write("Bölge büyütme işlemi için bir başlangıç noktası seçin.")
        seed_x = st.number_input("Başlangıç Noktası X Koordinatı", min_value=0, max_value=gray_image.shape[0]-1, value=st.session_state.get('seed_x', 0))
        seed_y = st.number_input("Başlangıç Noktası Y Koordinatı", min_value=0, max_value=gray_image.shape[1]-1, value=st.session_state.get('seed_y', 0))
        threshold = st.slider("Eşik Değeri", min_value=0, max_value=255, value=5)

        if st.button('Region Growing Uygula'):
            segmented_image = region_growing(gray_image, (seed_x, seed_y), threshold)
            st.image(segmented_image, caption='Region Growing Sonucu', use_column_width=True)

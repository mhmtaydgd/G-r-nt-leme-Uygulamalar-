import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import cv2

def color_and_matris_selection():

    def rgb_to_grayscale(image_array):
        grayscale_image = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
        return grayscale_image.astype(np.uint8)


    def grayscale_to_binary(grayscale_image, threshold=128):
        binary_image = (grayscale_image > threshold) * 255
        return binary_image.astype(np.uint8)

    def show_pixel_matrix(image_array, x_start, y_start, x_end, y_end):
        st.write("Seçilen Bölgenin Matris Değeri:")
        st.write(image_array[y_start:y_end, x_start:x_end])

    def draw_rectangle(image, x_start, y_start, x_end, y_end, color):
        draw = ImageDraw.Draw(image)
        draw.rectangle([x_start, y_start, x_end, y_end], outline=color, width=2)

    st.title("Görüntü Dönüştürme")
    uploaded_file = st.file_uploader("Lütfen bir fotoğraf yükleyin", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:

        image = Image.open(uploaded_file)
        image_array = np.array(image)

        st.image(image, caption='Yüklenen Görüntü', use_column_width=True)

        conversion_type = st.selectbox(
            "Dönüştürme Tipini Seçin",
            ("Orijinal", "Gri Seviye", "Binary", "Matris")
        )

        if conversion_type == "Orijinal":
            st.image(image, caption='Orijinal Görüntü', use_column_width=True)

        elif conversion_type == "Gri Seviye":
            grayscale_image = rgb_to_grayscale(image_array)
            st.image(grayscale_image, caption='Gri Seviye Görüntü', use_column_width=True, channels='GRAY')

        elif conversion_type == "Binary":
            grayscale_image = rgb_to_grayscale(image_array)
            binary_image = grayscale_to_binary(grayscale_image)
            st.image(binary_image, caption='Binary Görüntü', use_column_width=True, channels='GRAY')

        elif conversion_type == "Matris":
            if "mouse_x" not in st.session_state:
                st.session_state.mouse_x = -1
            if "mouse_y" not in st.session_state:
                st.session_state.mouse_y = -1

            if "start_x" not in st.session_state:
                st.session_state.start_x = -1
            if "start_y" not in st.session_state:
                st.session_state.start_y = -1

            if "end_x" not in st.session_state:
                st.session_state.end_x = -1
            if "end_y" not in st.session_state:
                st.session_state.end_y = -1

            def on_mouse(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    st.session_state.mouse_x = x
                    st.session_state.mouse_y = y
                    st.session_state.start_x = x
                    st.session_state.start_y = y
                elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                    st.session_state.end_x = x
                    st.session_state.end_y = y

            window_name = "Image"
            cv2.imshow(window_name, image_array)
            cv2.setMouseCallback(window_name, on_mouse)

            st.write("Görüntü üzerinde bir başlangıç noktası belirleyin, basılı tutun ve bir dikdörtgen oluşturmak için sürükleyin.")
            st.write("Dikdörtgen oluşturduktan sonra pencereyi kapatmak için bir tuşa basın.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if (st.session_state.start_x != -1 and st.session_state.start_y != -1 and
                    st.session_state.end_x != -1 and st.session_state.end_y != -1):
                x_start = min(st.session_state.start_x, st.session_state.end_x)
                y_start = min(st.session_state.start_y, st.session_state.end_y)
                x_end = max(st.session_state.start_x, st.session_state.end_x)
                y_end = max(st.session_state.start_y, st.session_state.end_y)
                
                # Dikdörtgeni çiz
                draw_rectangle(image, x_start, y_start, x_end, y_end, "red")
                st.image(image, caption='Seçilen Bölge', use_column_width=True)

                show_pixel_matrix(image_array, x_start, y_start, x_end, y_end)

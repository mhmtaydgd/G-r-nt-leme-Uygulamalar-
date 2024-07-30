import streamlit as st
from colorselect import color_and_matris_selection
from morfoprocess import morphological_operations
from sobelandgauss import sobel_gauss_canny
from histogram import histogram_equal
from regiongrowing import region_grow

# Session state ile aktif butonu takip etme
if 'active_button' not in st.session_state:
    st.session_state.active_button = 'Renk ve Matris Seçimi'

# Butonların yerleştirilmesi ve stillendirilmesi için yardımcı fonksiyon
def create_button(button_name, display_name):
    style = f"""
    <style>
    div.stButton > button {{
        background-color: lightgray;
        color: black;
        width: 100%;
        height: 50px;
        border: none;
        border-radius: 5px;
        margin-bottom: 5px;
    }}
    .active {{
        background-color: lightblue;
        color: white;
    }}
    </style>
    """
    button_clicked = st.sidebar.button(display_name)
    if button_clicked:
        st.session_state.active_button = button_name
    return button_clicked

st.markdown(
    """
    <style>
    div.stsidebar > sidebar {
        
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: blue;
        color: white;
        width: 100%;
        height: 50px;
        margin-bottom: 5px;
        border: none;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Kenar çubuğunda butonların oluşturulması
st.sidebar.markdown("""
    <style>
    .center-text {
        text-align: center;
        font-weight: bold;
        font-size: 50px;
    }
    </style>
    <div class="center-text">Menü</div>
    """, unsafe_allow_html=True)

if create_button('Renk ve Matris Seçimi', 'Renk ve Matris Seçimi'):
    st.session_state.active_button = 'Renk ve Matris Seçimi'
if create_button('Morfolojik İşlem', 'Morfolojik İşlem'):
    st.session_state.active_button = 'Morfolojik İşlem'
if create_button('Sobel Gauss ve Canny', 'Sobel Gauss ve Canny'):
    st.session_state.active_button = 'Sobel Gauss ve Canny'
if create_button('Histogram', 'Histogram'):
    st.session_state.active_button = 'Histogram'
if create_button('Region Growing', 'Region Growing'):
    st.session_state.active_button = 'Region Growing'


# Aktif butona göre işlem yapma
if st.session_state.active_button == 'Renk ve Matris Seçimi':
    
    color_and_matris_selection()
    
elif st.session_state.active_button == 'Morfolojik İşlem':

    morphological_operations()

elif st.session_state.active_button == 'Sobel Gauss ve Canny':
    
    sobel_gauss_canny() 

elif st.session_state.active_button == 'Histogram':

    histogram_equal()
    
elif st.session_state.active_button == 'Region Growing':

    region_grow()
    
# CSS ile butonların boyutlarını eşitleme
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 50px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
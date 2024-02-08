import streamlit as st
import base64


def color_sidebar():
    page_by_img = """
    <style>
    [data-testid="stSidebar"] {background-color: #f5f0eb}
    </style>
    """
    st.markdown(page_by_img, unsafe_allow_html=True)


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def background_image(file) -> None:
    """
    affiche une image en fond d'écran
    :param file: image à afficher
    """
    img = get_img_as_base64(file)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover
    }}</style>"""
    st.markdown(page_bg_img, unsafe_allow_html=True)


def color_page():
    color_sidebar()
    page_by_img = """
    <style>
    [data-testid="stAppViewContainer"] {background-color: #d8f2f0}
    </style>
    """
    st.markdown(page_by_img, unsafe_allow_html=True)

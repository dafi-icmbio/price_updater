import streamlit as st


add_sidebar_logo = st.logo(
    "images/logo icmbio.png",
    size="large"
)

add_sidebar_title = st.sidebar.title(
    "ICMBio/DAFI"
)

add_selectbox = st.sidebar.selectbox(
    "Selecione a concessão de interesse:",
    ("Chapada dos Veadeiros", "Aparados da Serra")
)


import streamlit as st

st.set_page_config(
    page_title="ICMBio - DAFI",  
    page_icon="images/logo icmbio.png",
    layout="centered",              
    initial_sidebar_state="expanded" 
)

prices_page = st.Page("tools/prices.py", title="Preços Vigentes", default=True, icon=":material/attach_money:")

fine_page = st.Page("tools/fine.py", title="Calculadora de Juros", icon=":material/calculate:")

pg = st.navigation([prices_page, fine_page])

pg.run()

add_sidebar_logo = st.logo(
    "images/logo icmbio.png",
    size="large"
)



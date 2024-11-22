import streamlit as st
from src.park.park_factory import ParkFactory
from src.utils import translate_month
import pandas as pd

from datetime import datetime

st.set_page_config(
    page_title="ICMBio - DAFI",  
    page_icon="images/logo icmbio.png",
    layout="centered",              
    initial_sidebar_state="expanded" 
)

add_sidebar_logo = st.logo(
    "images/logo icmbio.png",
    size="large"
)

add_sidebar_title = st.sidebar.title(
    "ICMBio/DAFI"
)

add_selectbox = st.sidebar.selectbox(
    "Selecione a concessão de interesse:",
    ("Chapada dos Veadeiros", "Aparados da Serra", "Itatiaia"),
    key="park"
)

park = ParkFactory.create_park(park=st.session_state.park)

st.title("Instituto Chico Mendes de Conservação da Biodiversidade - ICMBio :leaves:", anchor="title")

st.markdown("### Divisão de Apoio à Fiscalização das Delegações")

st.divider()

st.markdown(f"##### Informações para o Parque Nacional {str(st.session_state.park)}:")

st.write("")

st.markdown(f"""
            Preços em Reais (R$) praticados
            em **{translate_month(datetime.today().date().strftime("%B"))}
            de {datetime.today().date().strftime("%Y")}**
            """)

st.dataframe(
    pd.DataFrame(
        park.get_info_table(),
        index=[0]
    ),
    hide_index=True
)
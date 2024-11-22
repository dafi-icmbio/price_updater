import streamlit as st
from src.park.park_factory import ParkFactory
import pandas as pd

from datetime import datetime


add_sidebar_logo = st.logo(
    "images/logo icmbio.png",
    size="large"
)

add_sidebar_title = st.sidebar.title(
    "ICMBio/DAFI"
)

add_selectbox = st.sidebar.selectbox(
    "Selecione a concessão de interesse:",
    ("Chapada dos Veadeiros", "Aparados da Serra"),
    key="park"
)

park = ParkFactory.create_park(park=st.session_state.park)

st.markdown(f"Preços em {datetime.today().date().strftime("%B de %Y")} para {str(st.session_state.park)}")

st.write(
    pd.DataFrame(
        park.get_info_table(),
        index=[0]
    )
)
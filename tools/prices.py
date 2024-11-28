import streamlit as st
from src.park.park_factory import ParkFactory
from src.utils import translate_month
import pandas as pd

from datetime import datetime

add_selectbox = st.sidebar.selectbox(
    "Selecione a concessão de interesse:",
    ("Chapada dos Veadeiros", 
     "Itatiaia", 
     "Tijuca - Trem Corcovado",
     "Tijuca - Paineiras",
     "Fernando de Noronha",
     "Aparados da Serra e Serra Geral", 
     "Iguaçu - Cataratas",
     "Iguaçu - Ilha do Sol"),
    key="park",
    placeholder="Ex.: Itatiaia",
    index=None
)
try:

    query_params = st.query_params.park

    park = ParkFactory.create_park(park=query_params)

    st.query_params.clear()

except AttributeError:

    park = ParkFactory.create_park(park=st.session_state.park)


st.markdown("## Instituto Chico Mendes de Conservação da Biodiversidade - ICMBio :leaves:")

st.markdown("### Divisão de Apoio à Fiscalização das Delegações")

st.divider()

if park:

    st.markdown(f"<h5>Informações para o <span style = 'color:green'> Parque Nacional {park.name}: </span></h5>",
                unsafe_allow_html=True)

    st.write("")

    st.markdown(f"""
                Preços em Reais (R$) autorizados
                em **{translate_month(datetime.today().date().strftime("%B"))}
                de {datetime.today().date().strftime("%Y")}***
                """)

    st.dataframe(
        pd.DataFrame(
            park.get_info_table(),
            index=[0]
        ),
        hide_index=True,

    )

    st.write("")

    st.markdown("Evolução do preço base")

    st.line_chart(
        park.get_price_var_table(),
        x="VALDATA",
        y="VALPRECO",
        y_label= "Preço autorizado (R$)",
        x_label= "Data",
        color = "#133337"
    )

    st.markdown(
        f"""<em><p style= 'color:gray; font-size:12px'>*O valores dispostos nesta página 
        são apenas referenciais, cuja validade deve ser confirmada por meio
        dos instrumentos legais publicados pelo ICMBio.</p></em>""",
        unsafe_allow_html=True
    )

else:
    st.markdown("# :material/arrow_back:")
    st.markdown(
        """Por favor, selecione na barra lateral uma concessão de
        interesse para visualizar os dados disponíveis."""
    )
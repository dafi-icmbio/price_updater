import streamlit as st
from datetime import datetime, timedelta

from src.utils.fine_math import calculate_fine

st.markdown("## Instituto Chico Mendes de Conservação da Biodiversidade - ICMBio :leaves:")

st.markdown("### Divisão de Apoio à Fiscalização das Delegações")

st.divider()

st.markdown("##### Calculadora de Juros e Multa por Mora")

st.markdown("""O cálculo aqui proposto se aplica apenas
            àquelas Concessões as quais não há
            previsão contratual sobre as taxas a serem
            assumidas quando da existência de atrasos no pagamento
            da outorga.
            """)

st.markdown("""Esta ferramenta foi desenvolvida com base no apontado pela 
            Procuradoria Federal Especializada junto ao ICMBio na 
            NOTA nº 00027/2024/COMAD/PFE-ICMBIO/PGF/AGU (SEI 18236413) 
            e com o disposto no Despacho Interlocutório (SEI 16380236).""")


with st.form(key="fine_form", clear_on_submit=False):


    valor_gru = st.number_input("Valor da GRU (R$)", key="valor_gru")

    data_vencimento_gru = st.date_input("Data de Vencimento", 
                                        value="today", 
                                        format="DD/MM/YYYY", 
                                        key="data_vencimento_gru",
                                        )

    data_pagamento_gru = st.date_input("Data de Pagamento", 
                                    value = (datetime.today() + timedelta(days=1)), 
                                    format="DD/MM/YYYY", 
                                    key="data_pagamento_gru",
                                    )

    submitted = st.form_submit_button("Calcular")

    if submitted:

        with st.spinner("Calculando"):
        
            fine = calculate_fine(valor_gru, data_vencimento_gru, data_pagamento_gru)

        st.metric("Valor devido:", value=f"R$ {round(valor_gru + fine,2)}", delta=f"R$ {round(fine,2)}")


st.markdown(
    f"""<em><p style= 'color:gray; font-size:12px'>*O valores dispostos nesta página 
    são apenas referenciais, cuja validade deve ser confirmada por meio
    dos instrumentos legais publicados pelo ICMBio.</p></em>""",
    unsafe_allow_html=True
)
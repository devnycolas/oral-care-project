import pandas as pd
import streamlit as st
import plotly.express as px
from dashboard import montarDash, montarDashDois, montarDashTres, montarDashQuatro, montarDashCinco, montarDashSeis
from Modules.dados import pegar_dados

# Para exeutar:
# streamlit run main.py

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

texto = "testando"
df = pegar_dados()

texto
df


montarDash(col1, df)
montarDashDois(col2, df)
montarDashTres(col3, df)
montarDashQuatro(col4, df)
montarDashCinco(col5, df)
montarDashSeis(col6, df)

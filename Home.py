import streamlit as st
import plotly.express as px
import pandas as pd

from paginas.Dash_pesquisa import *
from paginas.Participantes import *
from paginas.Sobre import *

from Modules.dados import pegar_dados



pages = {
    "Sobre": sobre,
    "Dash Pesquisa": dash_pesquisa,
    "Pesquisados": participantes,
}

st.sidebar.title("Navegação")
selected_page = st.sidebar.selectbox("Selecione uma página", list(pages.keys()))
df = pegar_dados()

pages[selected_page](df)
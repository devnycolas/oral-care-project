import pandas as pd
import streamlit as st
import plotly.express as px
from dashboard import montarDash
from Modules.dados import pegar_dados

# Para exeutar:
# streamlit run main.py
texto = "testando"
df = pegar_dados()

texto
df

montarDash(st, df)

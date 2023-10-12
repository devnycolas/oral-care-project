import pandas as pd
import streamlit as st
import plotly.express as px

# Para exeutar:
# streamlit run main.py

from Modules.Dados.dados import pegar_dados
df = pegar_dados()
df.to_excel('pesquisa_oral_care.xlsx', index=False)

df


fig = px.bar(df, 
             x='Cidade', 
             y='Idade', 
             orientation='v',
             title='exemplo')
st.plotly_chart(fig)

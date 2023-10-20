import streamlit as st
import plotly.express as px
import pandas as pd

def participantes(df):
    st.header("Sobre os pesquisados:")
    st.write("Graficos Voltados para quem respondeu a pesquisa")
    st.table(df)


import streamlit as st
import plotly.express as px
import pandas as pd

def dash_pesquisa(df: pd.DataFrame):
    st.header("Dash pesquisa: Tendências e Desafios no Cuidado de Saúde Bucal")
    st.write("Graficos Voltados para o oral care")
    plot_renda_conhece_oc(df)


def plot_renda_conhece_oc(df):
    # rendaxconhece oral care
    # Crie uma coluna auxiliar com 1 para "Sim" e 0 para "Não"
    df['conhece_oral_care_bin'] = (df['conhece_oral_care'] == 'Sim').astype(int)
    # Use groupby e count para contar "Sim" e "Não" separadamente
    df_grouped = df.groupby(['renda_percapita', 'conhece_oral_care']).size().unstack(fill_value=0)
    # Renomeie as colunas
    df_grouped = df_grouped.rename(columns={'Sim': 'Total Sim', 'Não': 'Total Não'})
    # Reset o índice, se desejar
    df_grouped.reset_index(inplace=True)

    ordem = ["Não quero responder", "Menos de R$ 1.000,00", "R$ 1.000,00 a R$ 2.000,00", "R$ 2.001,00 a R$ 3.000,00", "R$ 3.001,00 a R$ 4.000,00", "Mais de R$ 4.000,00"]
    fig_renda_conhece_oc = px.bar(df_grouped, x='renda_percapita', y=['Total Sim', 'Total Não'], barmode='group',
             labels={'Total Sim': 'Sim', 'Total Não': 'Não'},
             title='Conhece o oral care baseado na renda:', color_discrete_map={'Sim': 'green', 'Não': 'red'})
    fig_renda_conhece_oc.update_xaxes(title_text='')  # Renomeie o título do eixo x
    fig_renda_conhece_oc.update_yaxes(title_text='Conhece')  # Renomeie o título do eixo y
    fig_renda_conhece_oc = fig_renda_conhece_oc.update_xaxes()
    fig_renda_conhece_oc.data[0].marker.color = '#d3ffce'  # Cor para "Sim"
    fig_renda_conhece_oc.data[1].marker.color = '#DC143C'    # Cor para "Não"
    # Adicione o valor total como texto nas barras
    fig_renda_conhece_oc.update_traces(text=df_grouped['Total Sim'], textangle=0, textposition='inside', selector=dict(name='Total Sim'))
    fig_renda_conhece_oc.update_traces(text=df_grouped['Total Não'], textangle=0 ,textposition='inside', selector=dict(name='Total Não'))
    fig_renda_conhece_oc.update_xaxes(categoryarray=ordem)
    st.plotly_chart(fig_renda_conhece_oc)
    #Qual situação socio economica mais conhece sobre o oral care?


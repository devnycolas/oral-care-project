import streamlit as st
import plotly.express as px
import pandas as pd
from .Dash_pesquisa import df_com_coords, plot_conhece_oral_care_cidade, plot_conhece_oral_care_genero


def apresentacao(df):
    plot_conhece_oral_care_cidade(df, st)
    plot_conhece_oral_care_idade(df, st)
    plot_conhece_oral_care_genero(df, st)
    col1, col2 = st.columns([2,2])
    plot_mapa_sim(df, col1)
    plot_mapa_nao(df, col2)


def plot_mapa_sim(df: pd.DataFrame, contx: st):
    # Filtrar o DataFrame com base na seleção da cidade
    filtered_df = df_com_coords(df)
    filtered_df = filtered_df[filtered_df['conhece_oral_care'] == 'Sim']
    filtered_df = filtered_df.query('cidade != "Outro"')
    
    fig = px.density_mapbox(filtered_df, lat='latitude', lon='longitude', radius=14,
                        center=dict(lat=-15.8235629, lon=-47.9768165), zoom=9,
                        mapbox_style="stamen-terrain", title="Onde conhecem o oral care?")
    contx.plotly_chart(fig, use_container_width=True)


def plot_mapa_nao(df: pd.DataFrame, contx: st):
    # Filtrar o DataFrame com base na seleção da cidade
    filtered_df = df_com_coords(df)
    filtered_df = filtered_df[filtered_df['conhece_oral_care'] == 'Não']
    filtered_df = filtered_df.query('cidade != "Outro"')
    
    fig = px.density_mapbox(filtered_df, lat='latitude', lon='longitude', radius=14,
                        center=dict(lat=-15.8235629, lon=-47.9768165), zoom=9,
                        mapbox_style="stamen-terrain", title="Onde não conhecem o oral care?")
    contx.plotly_chart(fig, use_container_width=True)


def plot_conhece_oral_care_idade(df: pd.DataFrame, contx: st):
    # Calcule as contagens por gênero e se conhecem o Oral Care
    smoking_gender_counts = df.groupby(['idade', 'conhece_oral_care']).size().unstack().fillna(0)
    # Reorganize os dados para criar o gráfico
    smoking_gender_counts = smoking_gender_counts.reset_index()
    smoking_gender_counts = pd.melt(smoking_gender_counts, id_vars='idade', var_name='Conhece Oral Care', value_name='Contagem')
    # Organize os dados em ordem crescente de contagem
    smoking_gender_counts = smoking_gender_counts.sort_values(by='Contagem', ascending=False)
    # Defina uma paleta de cores personalizada
    colors = {'Sim': '#d3ffce','Não': '#DC143C'}
    # Gráfico de Barras Empilhadas para Conhece Oral Care por Gênero (em ordem crescente)
    fig = px.bar(smoking_gender_counts, x='idade', y='Contagem', title="Conhece Oral Care por idade",
                            color='Conhece Oral Care', color_discrete_map=colors, barmode='group')
    # Personalize as cores
    #fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_xaxes(title_text='Idade')
    fig.update_yaxes(title_text='Quantidade')
    #fig.update_traces(text=smoking_gender_counts['Contagem'], textangle=0, textposition='outside')
    # Exiba o gráfico
    contx.plotly_chart(fig, use_container_width=True)

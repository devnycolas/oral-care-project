import plotly.express as px
import pandas as pd
import streamlit as st





def montarDash(st, df:pd.DataFrame):
    st.subheader('Gráfico de Barras para Gênero')
    gender_counts = df['genero'].value_counts()
    fig_gender = px.bar(gender_counts, x=gender_counts.index, y=gender_counts.values, labels={'x': 'Gênero', 'y': 'Contagem'})
    st.plotly_chart(fig_gender, use_container_width=True)


def montarDashDois(st, df:pd.DataFrame):
    st.subheader('Gráfico de Pizza para Hábito de Fumar')
    smoking_counts = df['habito_fumar'].value_counts()
    fig_smoking = px.pie(smoking_counts, names=smoking_counts.index, values=smoking_counts.values)
    st.plotly_chart(fig_smoking, use_container_width=True)


def montarDashTres(st, df:pd.DataFrame):
    st.subheader('Gráfico de Barras Empilhadas para Distribuição por Gênero e Cidade')
    fig_stacked_bar = px.bar(df, x='cidade', color='genero', title='Distribuição por Gênero e Cidade')
    st.plotly_chart(fig_stacked_bar, use_container_width=True)

def montarDashQuatro(st, df:pd.DataFrame):
    smoking_gender_counts = df.groupby(['genero', 'habito_fumar']).size().unstack().fillna(0)

    # Reorganize os dados para criar o gráfico
    smoking_gender_counts = smoking_gender_counts.reset_index()
    smoking_gender_counts = pd.melt(smoking_gender_counts, id_vars='genero', var_name='Hábito de Fumar', value_name='Contagem')

    # Organize os dados em ordem crescente de contagem
    smoking_gender_counts = smoking_gender_counts.sort_values(by='Contagem', ascending=False)

    # Gráfico de Barras Empilhadas para Hábito de Fumar por Gênero (em ordem crescente)
    st.subheader('Hábito de Fumar por Gênero')
    fig_stacked_bar = px.bar(smoking_gender_counts, x='genero', y='Contagem', color='Hábito de Fumar',
                            barmode='group')
    st.plotly_chart(fig_stacked_bar)

def montarDashCinco(st, df:pd.DataFrame):
    smoking_gender_counts = df.groupby(['genero', 'sobre_rotina_skin_care']).size().unstack().fillna(0)

    # Reorganize os dados para criar o gráfico
    smoking_gender_counts = smoking_gender_counts.reset_index()
    smoking_gender_counts = pd.melt(smoking_gender_counts, id_vars='genero', var_name='Rotina Skin Care', value_name='Contagem')

    # Organize os dados em ordem crescente de contagem
    smoking_gender_counts = smoking_gender_counts.sort_values(by='Contagem', ascending=False)

    # Gráfico de Barras Empilhadas para Rotina Skin Care por Gênero (em ordem crescente)
    st.subheader('Rotina Skin Care por Gênero')
    fig_stacked_bar = px.bar(smoking_gender_counts, x='genero', y='Contagem', color='Rotina Skin Care',
                            barmode='group')
    st.plotly_chart(fig_stacked_bar)    

def montarDashSeis(st, df:pd.DataFrame):
    smoking_gender_counts = df.groupby(['genero', 'conhece_oral_care']).size().unstack().fillna(0)

    # Reorganize os dados para criar o gráfico
    smoking_gender_counts = smoking_gender_counts.reset_index()
    smoking_gender_counts = pd.melt(smoking_gender_counts, id_vars='genero', var_name='Conhece Oral Care', value_name='Contagem')

    # Organize os dados em ordem crescente de contagem
    smoking_gender_counts = smoking_gender_counts.sort_values(by='Contagem', ascending=False)

    # Gráfico de Barras Empilhadas para Conhece Oral Care por Gênero (em ordem crescente)
    st.subheader('Conhece Oral Care por Gênero')
    fig_stacked_bar = px.bar(smoking_gender_counts, x='genero', y='Contagem', color='Conhece Oral Care',
                            barmode='group')
    st.plotly_chart(fig_stacked_bar)  
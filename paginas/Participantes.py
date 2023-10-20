import streamlit as st
import plotly.express as px
import pandas as pd

def participantes(df):
    st.header("Sobre os participantes:")
    st.write("Graficos Voltados para quem respondeu a pesquisa")
    col1, col2 = st.columns(2)
    col3 = st.columns(1)[0]
    plot_pizza_genero(df, col1)
    plot_habito_fumar(df, col2)
    plot_skin_care_genero(df, col3)


def plot_pizza_genero(df: pd.DataFrame, contx: st):
    cold_colors = ['#782f40', '#fa8072', '#b79c34', '#00274c', '#3c5656']
    # Atribua a paleta de cores frias ao gráfico e use a coluna 'genero' para definir as cores
    fig_pie = px.pie(df, names='genero', color='genero', title="Porcentagem de Participantes por Gênero",
                    color_discrete_map={gen: cold_colors[i] for i, gen in enumerate(df['genero'].unique())})
    contx.plotly_chart(fig_pie, use_container_width=True)

def plot_habito_fumar(df: pd.DataFrame, contx: st):
    cold_colors = ['#782f40', '#00274c', '#3c5656']
    # Atribua a paleta de cores frias ao gráfico e use a coluna 'genero' para definir as cores
    fig_pie = px.pie(df, names='plot_habito_fumar', color='plot_habito_fumar', title="Porcentagem de Pessoas com Hábito de Fumar",
                    color_discrete_map={gen: cold_colors[i] for i, gen in enumerate(df['plot_habito_fumar'].unique())})
    contx.plotly_chart(fig_pie, use_container_width=True)

def plot_skin_care_genero(df: pd.DataFrame, contx: st):
    routine_skin_care_counts = df.groupby(['genero', 'rotina_skin_care']).size().unstack().fillna(0)
    # Reorganize os dados para criar o gráfico
    routine_skin_care_counts = routine_skin_care_counts.reset_index()
    routine_skin_care_counts = pd.melt(routine_skin_care_counts, id_vars='genero', var_name='Rotina de Skin Care', value_name='Contagem')
    routine_skin_care_counts = routine_skin_care_counts.sort_values(by='Contagem', ascending=False)
    colors = {'Sim': '#782f40', 'Não': '#00274c'}
    # Gráfico de Barras para Rotina de Skin Care por Gênero
    fig_bar = px.bar(routine_skin_care_counts, x='genero', y='Contagem', title="Rotina de Skin Care por Gênero",
                    color='Rotina de Skin Care', color_discrete_map=colors, barmode='group')
    # Personalize as cores, se desejar
    fig_bar.update_traces(marker_line_color='black', marker_line_width=1)
    # Personalize os rótulos dos eixos, se necessário
    fig_bar.update_xaxes(title='Gênero')
    fig_bar.update_yaxes(title='Quantidade')
    # Exiba o gráfico
    contx.plotly_chart(fig_bar, use_container_width=True)

import streamlit as st
import plotly.express as px
import pandas as pd


def participantes(df):
    st.header("Sobre os participantes:")
    st.write("Graficos Voltados para quem respondeu a pesquisa")
    col1, col2 = st.columns(2)
    col3 = st.columns(1)[0]
    idade = st.columns([2, 1])
    escova = st.columns([2, 1])
    plot_pizza_genero(df, col1)
    plot_habito_fumar(df, col2)
    plot_skin_care_genero(df, col3)
    plot_idade_pesquisados(df, idade)
    plot_troca_escova_pesquisados(df, escova)


def plot_pizza_genero(df: pd.DataFrame, contx: st):
    cold_colors = ['#782f40', '#fa8072', '#b79c34', '#00274c', '#3c5656']
    # Atribua a paleta de cores frias ao gráfico e use a coluna 'genero' para definir as cores
    fig_pie = px.pie(df, names='genero', color='genero', title="Porcentagem de Participantes por Gênero",
                     color_discrete_map={gen: cold_colors[i] for i, gen in enumerate(df['genero'].unique())})
    contx.plotly_chart(fig_pie, use_container_width=True)


def plot_habito_fumar(df: pd.DataFrame, contx: st):
    cold_colors = ['#782f40', '#00274c', '#3c5656']
    # Atribua a paleta de cores frias ao gráfico e use a coluna 'genero' para definir as cores
    fig = px.pie(df, names='habito_fumar', color='habito_fumar', title="Porcentagem de Pessoas com Hábito de Fumar",
                 color_discrete_map={gen: cold_colors[i] for i, gen in enumerate(df['habito_fumar'].unique())})
    contx.plotly_chart(fig, use_container_width=True)


def plot_skin_care_genero(df: pd.DataFrame, contx: st):
    df_sc = df.groupby(['genero', 'rotina_skin_care']
                       ).size().unstack().fillna(0)
    # Reorganize os dados para criar o gráfico
    df_sc = df_sc.reset_index()
    df_sc = pd.melt(df_sc, id_vars='genero',
                    var_name='Rotina de Skin Care', value_name='Contagem')
    df_sc = df_sc.sort_values(by='Contagem', ascending=False)
    colors = {'Sim': '#782f40', 'Não': '#00274c'}
    # Gráfico de Barras para Rotina de Skin Care por Gênero
    fig = px.bar(df_sc, x='genero', y='Contagem', title="Rotina de Skin Care por Gênero",
                 color='Rotina de Skin Care', color_discrete_map=colors, barmode='group')
    # Personalize as cores, se desejar
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    # Personalize os rótulos dos eixos, se necessário
    fig.update_xaxes(title='Gênero')
    fig.update_yaxes(title='Quantidade')
    # Exiba o gráfico
    contx.plotly_chart(fig, use_container_width=True)


def plot_idade_pesquisados(df: pd.DataFrame, contx: list):
    # Crie um histograma das idades
    fig = px.histogram(
        df, x='idade', title="Distribuição de Idades dos Respondentes")
    fig.update_xaxes(title_text='Idade')
    fig.update_yaxes(title_text='Contagem')
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_traces(marker_color='#782f40')
    contx[0].plotly_chart(fig)
    media_idade = int(df['idade'].mean())

    # Exiba um st.metric com a média de idade
    contx[1].metric("Média de ", f'{media_idade} Anos')


def plot_troca_escova_pesquisados(df: pd.DataFrame, contx: st):
    ordem = ['Todo mês', 'A cada 3 meses',
             'A cada 6 meses', '1 vez por ano ou mais']
    # Converter a coluna 'substitui_escova_dentes' em uma variável categórica
    df['substitui_escova_dentes'] = df['substitui_escova_dentes'].astype(
        'category')
    agrupado = df.groupby(
        'substitui_escova_dentes').size().reset_index(name='Contagem')
    fig = px.bar(agrupado, x='substitui_escova_dentes', y='Contagem',
                 title="Substituição escova", barmode='group')

    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='Contagem')
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_traces(marker_color='#782f40')
    fig.update_xaxes(categoryarray=ordem)

    contx[0].plotly_chart(fig)
    media = int(df['frequencia_escova_dentes_diaria'].mean())
    contx[1].metric("Média de escovação diaria", f'{media} vezes')

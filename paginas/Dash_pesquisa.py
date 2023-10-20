import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
#from geopy.geocoders import Nominatim
import json
#geolocator = Nominatim(user_agent="geoapiExercises")
map_coords = {}
caminho_locales = '.\cache\locales.json'

ordem = ["Menos de R$ 1.000,00", "R$ 1.000,00 a R$ 2.000,00", "R$ 2.001,00 a R$ 3.000,00", "R$ 3.001,00 a R$ 4.000,00", "Mais de R$ 4.000,00", "Não quero responder"]
def dash_pesquisa(df: pd.DataFrame):
    st.header("Dash pesquisa: Tendências e Desafios no Cuidado de Saúde Bucal")
    st.write("Graficos Voltados para o oral care")
    cola = st.columns([2])
    colg = st.columns(1)
    rend1, rend2 = st.columns(2)
    col_sk1, col_sk2 = st.columns(2)
    #plot_mapa(df, st)
    plot_renda_conhece_oc(df, rend1)
    plot_agravantes(df, cola[0])
    plot_renda_conhece_produtos_oc(df, rend2)
    plot_skin_oc(df, col_sk1)
    plot_nskin_oc(df, col_sk2)
    conhece_oral_care_genero(df, colg[0])



def plot_renda_conhece_oc(df: pd.DataFrame, contx: st):
    
    # rendaxconhece oral care
    # Crie uma coluna auxiliar com 1 para "Sim" e 0 para "Não"
    df['conhece_oral_care_bin'] = (df['conhece_oral_care'] == 'Sim').astype(int)
    # Use groupby e count para contar "Sim" e "Não" separadamente
    df_grouped = df.groupby(['renda_percapita', 'conhece_oral_care']).size().unstack(fill_value=0)
    # Renomeie as colunas
    df_grouped = df_grouped.rename(columns={'Sim': 'Total Sim', 'Não': 'Total Não'})
    # Reset o índice, se desejar
    df_grouped.reset_index(inplace=True)

    
    fig = px.bar(df_grouped, x='renda_percapita', y=['Total Sim', 'Total Não'], barmode='group',
             labels={'Total Sim': 'Sim', 'Total Não': 'Não'},
             title='Conhece o oral care baseado na renda:', color_discrete_map={'Sim': 'green', 'Não': 'red'})
    fig.update_xaxes(title_text='')  # Renomeie o título do eixo x
    fig.update_yaxes(title_text='Conhece')  # Renomeie o título do eixo y
    fig = fig.update_xaxes()
    fig.data[0].marker.color = '#d3ffce'  # Cor para "Sim"
    fig.data[1].marker.color = '#DC143C'    # Cor para "Não"
    # Adicione o valor total como texto nas barras
    fig.update_traces(text=df_grouped['Total Sim'], textangle=0, textposition='inside', selector=dict(name='Total Sim'))
    fig.update_traces(text=df_grouped['Total Não'], textangle=0 ,textposition='inside', selector=dict(name='Total Não'))
    fig.update_xaxes(categoryarray=ordem)
    contx.plotly_chart(fig, use_container_width=True)
    #Qual situação socio economica mais conhece sobre o oral care?


def atribuir_rotulo(pontuacao):
    if pontuacao <= -3:
        return 'excelente'
    elif -2 <= pontuacao <= -1:
        return 'muito bom'
    elif 0 <= pontuacao <= 2:
        return 'bom'
    elif 3 <= pontuacao <= 5:
        return 'ruim'
    elif 5 <= pontuacao <= 7:
        return 'muito ruim'
    elif pontuacao > 7:
        return 'péssimo'
    else:
        return 'indefinido'
    

def df_com_agravante(df: pd.DataFrame):
    col_positivos = [ 'habito_fumar', 'pratica_raspagem_lingua','frequencia_escova_dentes_diaria', 'uso_fio_dental', 'substitui_escova_dentes', 'usa_enxaguante_bucal', 'usa_protetor_solar_labial','uso_frequente_hidratante_labial']
    col_negativos = ['habito_fumar', 'escovar_dentes_com_forca']
    mapeamento = {'Sim': -1, 'Não': 1, 'As vezes': 0, 'De vez em quando': 0, 
                  'Todo mês': -1, 'A cada 3 meses': 0, 'A cada 6 meses': 1, '1 vez por ano ou mais': 2,
                  1:-2, 2:-1, 3:0, 4:1, 5:2}
    mapeamento_negativo = {
        'sim':2, 'As vezes': 1, 'Não': 0 
    }
    # Aplicar os mapeamentos positivos e negativos
    df[col_positivos] = df[col_positivos].map(lambda x: mapeamento.get(x, 0))
    df[col_negativos] = df[col_negativos].map(lambda x: mapeamento_negativo.get(x, 0))

    # Soma dos resultados
    df['agravantes'] = df[col_positivos].sum(axis=1) + df[col_negativos].sum(axis=1)
    df['agravantes'] = df['agravantes'].apply(atribuir_rotulo)
    return df


def plot_agravantes(df: pd.DataFrame, contx: st):
    df_agravante = df_com_agravante(df)
    # Crie um gráfico de barras empilhadas usando Plotly Express
    df_grouped = df_agravante.groupby(['renda_percapita', 'agravantes']).size().unstack(fill_value=0)
    ordem_desejada = ["excelente", "muito bom", "bom", "ruim", "muito ruim", "péssimo"]
    df_grouped = df_grouped.reindex(columns=ordem_desejada)
    fig = px.bar(df_grouped, x=df_grouped.index, y=df_grouped.columns, title='Relação entre renda e cuidados com a boca',
                labels={'index': 'Renda Per Capita', 'value': 'Quantidade', 'classificacao': 'condição'},
                category_orders={"classificacao": ["excelente", "muito bom", "bom", "ruim", "muito ruim", "péssimo"]},barmode='group')

    # Personalize as cores das barras
    colors = px.colors.qualitative.Set1[:6]# lista com 6 cores
    for i in range(len(fig.data)):
        fig.data[i].marker.color = colors[i]
    fig.update_xaxes(categoryarray=ordem)
    fig.update_xaxes(title_text='')
    

    contx.plotly_chart(fig, use_container_width=True)
    

def plot_renda_conhece_produtos_oc(df: pd.DataFrame, contx: st):
    
    # rendaxconhece oral care
    # Crie uma coluna auxiliar com 1 para "Sim" e 0 para "Não"
    df['conhece_oral_care_bin'] = (df['produtos_relacionados_oral_care'] == 'Sim').astype(int)
    # Use groupby e count para contar "Sim" e "Não" separadamente
    df_grouped = df.groupby(['renda_percapita', 'produtos_relacionados_oral_care']).size().unstack(fill_value=0)
    # Renomeie as colunas
    df_grouped = df_grouped.rename(columns={'Sim': 'Total Sim', 'Não': 'Total Não'})
    # Reset o índice, se desejar
    df_grouped.reset_index(inplace=True)

    
    fig = px.bar(df_grouped, x='renda_percapita', y=['Total Sim', 'Total Não'], barmode='group',
             labels={'Total Sim': 'Sim', 'Total Não': 'Não'},
             title='Conhece produtos de oral care baseado na renda:', color_discrete_map={'Sim': 'green', 'Não': 'red'})
    fig.update_xaxes(title_text='')  # Renomeie o título do eixo x
    fig.update_yaxes(title_text='Conhece')  # Renomeie o título do eixo y
    fig = fig.update_xaxes()
    fig.data[0].marker.color = '#d3ffce'  
    fig.data[1].marker.color = '#DC143C'   
    fig.update_traces(text=df_grouped['Total Sim'], textangle=0, textposition='inside', selector=dict(name='Total Sim'))
    fig.update_traces(text=df_grouped['Total Não'], textangle=0 ,textposition='inside', selector=dict(name='Total Não'))
    fig.update_xaxes(categoryarray=ordem)
    contx.plotly_chart(fig, use_container_width=True)
    

def plot_skin_oc(df: pd.DataFrame, contx: st):
    # Filtrar as entradas onde 'rotina_skin_care' é "Sim"
    df_filtrado = df[df['rotina_skin_care'] == 'Sim']

    # Calcular a porcentagem de "Sim" e "Não" em 'conhece_oral_care' para as entradas com 'rotina_skin_care' como "Sim"
    porcentagem_sim_nao = df_filtrado['conhece_oral_care'].value_counts(normalize=True) * 100

    # Criar um gráfico de pizza
    fig = px.pie(values=porcentagem_sim_nao, names=porcentagem_sim_nao.index,
                title='Quem pratica o skin care conhece o oral care?',
                labels={'names': 'conhece_oral_care', 'values': 'Porcentagem (%)'})
    cores = ['#d3ffce', '#DC143C']
    fig.update_traces(marker=dict(colors=cores))
    
    contx.plotly_chart(fig, use_container_width=True)


def plot_nskin_oc(df: pd.DataFrame, contx: st):
    # Filtrar as entradas onde 'rotina_skin_care' é "Não"
    df_filtrado = df[df['rotina_skin_care'] == 'Não']

    # Calcular a porcentagem de "Sim" e "Não" em 'conhece_oral_care' para as entradas com 'rotina_skin_care' como "Sim"
    porcentagem_sim_nao = df_filtrado['conhece_oral_care'].value_counts(normalize=True) * 100

    # Criar um gráfico de pizza
    fig = px.pie(values=porcentagem_sim_nao, names=porcentagem_sim_nao.index,
                title='Quem conhece o oral care mas não pratica o skin care?',
                labels={'names': 'conhece_oral_care', 'values': 'Porcentagem (%)'})
    cores = ['#d3ffce', '#DC143C']
    cores.reverse()
    fig.update_traces(marker=dict(colors=cores))
    
    contx.plotly_chart(fig, use_container_width=True)

def get_json_cache():
    try:
        locales = json.loads(caminho_locales)
        return locales
    except:
        return {}



def salvar_loc_cache():
    with open(caminho_locales, 'w') as arquivo_json:
        json.dump(map_coords, arquivo_json)


def df_com_coords(df: pd.DataFrame):
    map_coords = get_json_cache()
    
    salvar_loc_cache()
    return df


def plot_mapa(df: pd.DataFrame, contx: st):
    df_coord = df_com_coords(df)
    # Crie o objeto Densitymapbox
    conhece_oral_care_mapping = {'Sim': 1, 'Não': 0}
    df_coord['conhece_oral_care_numeric'] = df_coord['conhece_oral_care'].map(conhece_oral_care_mapping)
    df_coord['conhece_oral_care_numeric'] = df_coord['conhece_oral_care_numeric'].astype(int)
    densitymapbox = go.Densitymapbox(lat=df_coord['latitude'], lon=df_coord['longitude'], z=df_coord['conhece_oral_care_numeric'].count(), radius=10)

    # Personalize a escala de cores
    #densitymapbox.coloraxis.colorscale = [[0, 'red'], [1, 'green']]  # Personalize as cores conforme necessário

    # Configure o layout do mapa
    layout = go.Layout(mapbox_style="open-street-map",
                    mapbox_center={'lat': -23.5505, 'lon': -46.6333},
                    mapbox_zoom=10,
                    title="Mapa de Densidade de Conhecimento de Oral Care")

    # Crie a figura
    fig = go.Figure(data=densitymapbox, layout=layout)


    contx.plotly_chart(fig)

def conhece_oral_care_genero(df: pd.DataFrame, contx: st):
    # Calcule as contagens por gênero e se conhecem o Oral Care
    smoking_gender_counts = df.groupby(['genero', 'conhece_oral_care']).size().unstack().fillna(0)
    # Reorganize os dados para criar o gráfico
    smoking_gender_counts = smoking_gender_counts.reset_index()
    smoking_gender_counts = pd.melt(smoking_gender_counts, id_vars='genero', var_name='Conhece Oral Care', value_name='Contagem')
    # Organize os dados em ordem crescente de contagem
    smoking_gender_counts = smoking_gender_counts.sort_values(by='Contagem', ascending=False)
    # Defina uma paleta de cores personalizada
    colors = {'Sim': '#fa8072', 'Não': '#3c5656'}
    # Gráfico de Barras Empilhadas para Conhece Oral Care por Gênero (em ordem crescente)
    fig = px.bar(smoking_gender_counts, x='genero', y='Contagem', title="Conhece Oral Care por Gênero",
                            color='Conhece Oral Care', color_discrete_map=colors, barmode='group')
    # Personalize as cores
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_xaxes(title_text='Gênero')
    fig.update_yaxes(title_text='Quantidade')
    # Exiba o gráfico
    contx.plotly_chart(fig, use_container_width=True)

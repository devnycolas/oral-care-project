import streamlit as st
import plotly.express as px
import pandas as pd
ordem = ["Não quero responder", "Menos de R$ 1.000,00", "R$ 1.000,00 a R$ 2.000,00", "R$ 2.001,00 a R$ 3.000,00", "R$ 3.001,00 a R$ 4.000,00", "Mais de R$ 4.000,00"]
def dash_pesquisa(df: pd.DataFrame):
    st.header("Dash pesquisa: Tendências e Desafios no Cuidado de Saúde Bucal")
    st.write("Graficos Voltados para o oral care")
    
    plot_renda_conhece_oc(df, st)
    plot_agravantes(df, st)


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
    contx.plotly_chart(fig_renda_conhece_oc, use_container_width=True)
    #Qual situação socio economica mais conhece sobre o oral care?


def atribuir_rotulo(pontuacao):
    if pontuacao < -3:
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
    df[col_positivos] = df[col_positivos].applymap(lambda x: mapeamento.get(x, 0))
    df[col_negativos] = df[col_negativos].applymap(lambda x: mapeamento_negativo.get(x, 0))

    # Soma dos resultados
    df['agravantes'] = df[col_positivos].sum(axis=1) + df[col_negativos].sum(axis=1)
    st.plotly_chart(df)
    return df


def plot_agravantes(df: pd.DataFrame, contx: st):
    df_agravante = df_com_agravante(df)
    # Crie um gráfico de barras empilhadas usando Plotly Express
    df_grouped = df_agravante.groupby(['renda_percapita', 'agravantes']).size().unstack(fill_value=0)
    fig_agravantes = px.bar(df_grouped, x=df_grouped.index, y=df_grouped.columns, title='Correlação entre Renda Per Capita e agravantes',
                labels={'index': 'Renda Per Capita', 'value': 'Contagem', 'classificacao': 'agravantes'},
                category_orders={"classificacao": ["excelente", "muito bom", "bom", "ruim", "muito ruim", "péssimo"]},barmode='group')

    # Personalize as cores das barras
    colors = px.colors.qualitative.Set1[:6]# lista com 6 cores
    for i in range(6):
        fig_agravantes.data[i].marker.color = colors[i]
    fig_agravantes.update_xaxes(categoryarray=ordem)
    contx.plotly_chart(fig_agravantes)
    

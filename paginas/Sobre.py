import streamlit as st
import plotly.express as px
import pandas as pd
from Modules.dados import pegar_dados

def sobre(df: pd.DataFrame):
    st.title("Sobre a Equipe e o Projeto")

    # Seção do projeto de pesquisa de dados
    st.header("Projeto de Pesquisa de Dados")

    # Descrição do projeto
    st.markdown("Em parceria com uma equipe de odontologia, realizamos um projeto de pesquisa de dados focado em informações relacionadas aos cuidados bucais.")
    st.markdown("Nosso projeto permite integração em tempo real com o formulário de pesquisa, possibilitando a atualização dos valores caso um novo respondente preencha a pesquisa.")

    # Objetivos do projeto
    st.subheader("Objetivos do Projeto:")
    st.markdown("- Coletar dados relacionados à saúde bucal por meio de pesquisas online.")
    st.markdown("- Realizar análises de dados para identificar tendências e insights valiosos.")
    st.markdown("- Colaborar com a empresa de odontologia para melhorar a conscientização e os serviços de saúde bucal.")
    # Criar uma estrutura de colunas para colocar as imagens lado a lado
    col_img_1, col_img_2 = st.columns(2)

    col_img_1.image("Modules/img/odonto.jpg", width=300, caption="Equipe de Odonto")
    col_img_1.write("Equipe de odontologia que precisa de uma pesquisa e analise para apresentar os dados sobre Oral Care.")
    
    
    col_img_2.image("Modules/img/TI.jpg", width=300, caption="Equipe de TI")
    col_img_2.write("Equipe de TI com o objetivo de construir a pesquisa e a dash board para equipe de odontologia.")

    st.divider()
    # Exibir resultados do projeto, como um gráfico
    col1, col2 = st.columns(2)
    col1.subheader("Resultados do Projeto")

    participantes = int(df["genero"].count())
    col2.metric("Total de ", f'{participantes} participantes')


    # Criar um gráfico de barras para contar o número de pessoas por gênero com cores diferentes
    df_counts = df.groupby("genero").size().reset_index(name="Número de Pessoas")
    # Definir cores personalizadas para os gêneros
    colors = {'Masculino': 'blue', 'Feminino': 'pink', 'Não especificado': 'gray'}
    fig_bar = px.bar(df_counts, x="genero", y="Número de Pessoas", title="Número de Pessoas por Gênero", 
                    color="genero", color_discrete_map=colors)
    
    # Personalize o rótulo do eixo y
    fig_bar.update_yaxes(title="Número de Pessoas")

    
    # Exiba o gráfico
    st.plotly_chart(fig_bar, use_container_width=True)
    

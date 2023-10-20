import gspread
import pandas as pd
import re
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

def pegar_dados():
    # CÓDIGO DA PLANILHA, LOCALIZADO NA URL DA MESMA
    CODE = str(os.getenv('code'))

    # CRIANDO GOOGLE CLIENT
    gc = gspread.service_account(filename="keyconnect.json")

    # Abrindo a planilha pelo código
    sh = gc.open_by_key(CODE)

    # Acessando a planilha pelo título "Respostas ao formulário 1" em específico
    ws = sh.worksheet("Respostas ao formulário 1")

    # GERANDO UM DATAFRAME COM PANDAS
    df = pd.DataFrame(ws.get_all_records())
    df = renomear_colunas(df)
    df = organizarColunas(df)
    return df


def renomear_colunas(df):
    df = df.rename(columns={'Carimbo de data/hora': 'data/hora'})
    df = df.rename(columns={'Gênero:': 'genero'})
    df = df.rename(columns={'Possui o habito de fumar?': 'habito_fumar'})
    df = df.rename(columns={'Renda Per Capita:':'renda_percapita'})
    df = df.rename(columns={'Você possui rotina de skin care? ': 'rotina_skin_care'})
    df = df.rename(columns={'Sobre sua rotina de skin care:': 'sobre_rotina_skin_care'})
    df = df.rename(columns={'Você conhece o oral care?': 'conhece_oral_care'})
    df = df.rename(columns={'Você conhece produtos relacionados com o oral care?': 'produtos_relacionados_oral_care'})
    df = df.rename(columns={'Você pratica a raspagem da língua?': 'pratica_raspagem_lingua'})
    df = df.rename(columns={'Com qual frequência você escova os dentes diariamente?': 'frequencia_escova_dentes_diaria'})
    df = df.rename(columns={'Você faz uso do fio dental?': 'uso_fio_dental'})
    df = df.rename(columns={'Ao escovar os dentes você usa muita força?': 'escovar_dentes_com_forca'})
    df = df.rename(columns={'De quanto em quanto tempo você substitui a sua escova de dentes?': 'substitui_escova_dentes'})
    df = df.rename(columns={'Você utiliza enxaguante bucal?': 'usa_enxaguante_bucal'})
    df = df.rename(columns={'Você utiliza frequentemente protetor solar labial?': 'usa_protetor_solar_labial'})
    df = df.rename(columns={'Você faz uso frequente de hidratante labial?': 'uso_frequente_hidratante_labial'})
    df = df.rename(columns={'Nome': 'nome'})
    df = df.rename(columns={'Idade': 'idade'})
    df = df.rename(columns={'Email': 'email'})
    df = df.rename(columns={'Cidade': 'cidade'})

    return df


def organizarColunas(df):
    df = df[['genero', 'renda_percapita','habito_fumar','rotina_skin_care','sobre_rotina_skin_care','conhece_oral_care','produtos_relacionados_oral_care','pratica_raspagem_lingua','frequencia_escova_dentes_diaria','uso_fio_dental','escovar_dentes_com_forca','substitui_escova_dentes','usa_enxaguante_bucal','usa_protetor_solar_labial','uso_frequente_hidratante_labial','idade','cidade']]
    
    return df


def salvar_dataframe(df:pd.DataFrame):
    df.to_csv('\dados')

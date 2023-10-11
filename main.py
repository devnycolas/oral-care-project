import gspread
import pandas as pd
import re


# CÓDIGO DA PLANILHA, LOCALIZADO NA URL DA MESMA
CODE = "1Bo36gNyf1VuI9AFibuj7ppzKLm0ZNMy42Zx4S9fOpXQ"

# CRIANDO GOOGLE CLIENT
gc = gspread.service_account(filename="keyconnect.json")

# Abrindo a planilha pelo código
sh = gc.open_by_key(CODE)

# Acessando a planilha pelo título "Respostas ao formulário 1" em específico
ws = sh.worksheet("Respostas ao formulário 1")

# GERANDO UM DATAFRAME COM PANDAS
df = pd.DataFrame(ws.get_all_records())

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

# Função para limpar e formatar os nomes das colunas
def clean_column_name(column_name):
    # Converter para minúsculas
    column_name = column_name.lower()
    # Substituir espaços por underscores
    column_name = re.sub(r'\s', '_', column_name)
    return column_name


# Aplicar a função a todas as colunas do DataFrame
df.columns = df.columns.map(clean_column_name)
print(df)
df.to_excel('pesquisa_oral_care.xlsx', index=False)
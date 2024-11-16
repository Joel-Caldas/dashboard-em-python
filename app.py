import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração do Streamlit deve ser a primeira linha do código
st.set_page_config(page_title="Dashboard Imobiliária", layout="wide")

# Menu para navegação entre as seções
menu = ["Bairros Mais Procurados pelos Clientes", 
        "Bairros com Maior Número de Imóveis Ofertados", 
        "Desempenho das Mídias", 
        "Cadastrais de obras de construção civil por Bairros",
        "Interesse por Tipo de Imóvel nos Bairros Mais Procurados"]
opcao = st.sidebar.selectbox("Escolha uma opção", menu)

# Função para carregar os dados, com cache para melhorar a performance
@st.cache_data
def carregar_dados():
    file_path = "base_jlimobiliaria.xlsx"  # Ajuste conforme necessário
    df = pd.read_excel(file_path, decimal=',')
    return df

# Carregar os dados
df = carregar_dados()
df2 = pd.read_excel("imoveis_basecompleta.xlsx", decimal=',')
df3 = pd.read_excel("base_cno_final.xlsx", decimal=',')

# Limpeza de dados
df.drop(['Cliente', 'Telefone(s)', 'Email', '$ Venda', '$ Locação', 
         'Nome do condomínio/edifício', 'Referências', 'Usuário(s)'], axis=1, inplace=True)

df['Dt. Cadastro'] = pd.to_datetime(df['Dt. Cadastro'])
df['Data'] = df['Dt. Cadastro'].dt.date
df.drop('Dt. Cadastro', axis=1, inplace=True)

df['Bairro'] = df['Região'].str.split(',').str[0]
df.drop(['Região', 'Area'], axis=1, inplace=True)
df.dropna(inplace=True)

# Título do Dashboard
st.title("Dashboard - Análise Imobiliária")

# Exibir diferentes seções de acordo com a opção escolhida no menu
if opcao == "Bairros Mais Procurados pelos Clientes":
    st.header("Bairros Mais Procurados pelos Clientes")
    bairros_procurados = df['Bairro'].value_counts().head(10)
    fig1 = px.bar(bairros_procurados, x=bairros_procurados.index, y=bairros_procurados.values, 
                  labels={'x': 'Bairros', 'y': 'Procuras'}, title="Top 10 Bairros Mais Procurados")
    st.plotly_chart(fig1)

elif opcao == "Bairros com Maior Número de Imóveis Ofertados":
    st.header("Bairros com Maior Número de Imóveis Ofertados")
    bairros_ofertados = df2['Bairro'].value_counts().head(10)
    fig2 = px.bar(bairros_ofertados, x=bairros_ofertados.index, y=bairros_ofertados.values, 
                  labels={'x': 'Bairros', 'y': 'Ofertas'}, title="Top 10 Bairros com Mais Ofertas de Imóveis")
    st.plotly_chart(fig2)

elif opcao == "Desempenho das Mídias":
    st.header("Desempenho das Mídias")
    midias = df['Mídia'].value_counts()
    midias_categorias = midias[["Imovel Web", "ZAP", "Chaves Na Mão"]]
    midias_categorias["Outros"] = midias.drop(midias_categorias.index).sum()
    fig3 = px.pie(midias_categorias, values=midias_categorias.values, names=midias_categorias.index, 
                  title="Desempenho das Mídias")
    st.plotly_chart(fig3)

elif opcao == "Cadastrais de obras de construção civil por Bairros (Base Externa O Cadastro Nacional de Obras-CNO)":
    st.header("Cadastrais de obras de construção civil por Bairros")
    construcao = df3['Bairro'].value_counts().head(10)
    fig4 = px.bar(
        x=construcao.index, 
        y=construcao.values,
        labels={'x': 'Bairros', 'y': 'Obras por Bairros'},  # Corrigido: separação das chaves no dicionário de rótulos
        title="Distribuição de Obras de Construção Civil por Bairros"
    )
    st.plotly_chart(fig4)


elif opcao == "Interesse por Tipo de Imóvel nos Bairros Mais Procurados":
    st.header("Interesse por Tipo de Imóvel nos Bairros Mais Procurados")
    bairros_mais_procurados = df['Bairro'].value_counts().head(10).index
    df_interesse = df[df['Bairro'].isin(bairros_mais_procurados)]
    df_interesse = df_interesse.groupby(['Bairro', 'Tipo']).size().unstack().fillna(0)
    fig5 = px.bar(df_interesse, x=df_interesse.index, y=df_interesse.columns, 
                  title="Interesse por Tipo de Imóvel nos Bairros Mais Procurados", barmode='stack')
    st.plotly_chart(fig5)

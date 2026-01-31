import streamlit as st
import pandas as pd
import plotly.express as px

# configuração da página
# Define o título da página e o icone e o layout para ocupar a largura total
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="💸🎲",
    layout="wide",
)

# carregando os dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra Lateral - Filtros
st.sidebar.header("🔍Filtros🔎")

# Filtro de Ano
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_disponiveis = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)    

# Aplicando Filtros no DataFrame
# o Dataframe principal é filtrado com base nas seleções feitas na barra lateral
df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_disponiveis)) &
    (df["tamanho_empresa"].isin(tamanhos_selecionados)) 
]

# Conteúdo Principal do Dashboard
st.title("🎲 Dashboard de Ánalise de Salários na Área de Dados 💸")
st.markdown("Explore os dados slaariais na área de addos nos últimos anos. Utilize os filtros à esquerda para refinar sua análise")
st.markdown("---")

# Métricas Principais
st.subheader("📊 Métricas Gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean() 
    salario_max = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargp_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio = 0
    salario_max = 0
    total_registros = 0
    cargp_mais_frequente = "N/A"
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_max:,.0f}")
col3.metric("Total de Registros", total_registros)
col4.metric("Cargo Mais Frequente", cargp_mais_frequente)

st.markdown("---")

# Análises Visuais com Plotly
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title ="Top 10 Cargos por salário médio",
            labels={'usd': 'Média Salarial Anual em USD','cargo':''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição dos Salários Anuais em USD",
            labels={'usd': 'Faixa Salarial (USD)','count':''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            values='quantidade',
            names='tipo_trabalho',
            title="Proporção por Tipo de Trabalho",
            hole=0.4
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")


with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo']=='Data Scientist']
        media_ds_pais= df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_mapa = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title="Média Salarial de Data Scientists por País",
            labels={'usd': 'Média Salarial Anual em USD', 'residencia_iso3': 'País'})
        grafico_mapa.update_layout(title_x=0.1)
        st.plotly_chart(grafico_mapa, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

# tabela de dados detalhados
st.subheader("📋 Tabela de Dados Detalhados")
st.dataframe(df_filtrado, use_container_width=True)
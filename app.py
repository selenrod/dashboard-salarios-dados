import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# configuração da página
# Define o título da página e o icone e o layout para ocupar a largura total
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="💸🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# carregando os dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra Lateral - Filtros
st.sidebar.header("Filtros🔎")

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
st.title("Dashboard de Ánalise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise")
st.markdown("---")

# Métricas Principais
st.subheader("Métricas Gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean() 
    salario_min = df_filtrado["usd"].min()
    salario_max = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio = 0
    salario_max = 0
    total_registros = 0
    cargo_mais_frequente = "N/A"
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_max:,.0f}")
col3.metric("Salário Mínimo", f"${salario_min:,.0f}")
col4.metric("Total de Registros", total_registros)
col5.metric("Cargo Mais Frequente", cargo_mais_frequente)


st.markdown("---")

# Análises Visuais com Plotly
st.subheader("Gráficos")
# tabs 
tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Análise por Cargo", "Análise Geográfica", "Análise Avançada"])

# tab1 - visão geral
with tab1:
    if not df_filtrado.empty:
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_dist = px.histogram(
                df_filtrado,
                x='usd',
                nbins=40,
                title=" Distribuição dos Salários Anuais em USD",
                labels={'usd': 'Faixa Salarial (USD)', 'count': 'Frequência'},
                color_discrete_sequence=["#fafafa"],
                marginal='box'
            )
            fig_dist.update_layout(
                paper_bgcolor="#262730",
                plot_bgcolor="#262730",
                font={'color': "#fafafa"},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=True,
                xaxis=dict(gridcolor="#e9ecef", linecolor="#e9ecef"),
                yaxis=dict(gridcolor="#e9ecef", linecolor="#e9ecef")
            )
            fig_dist.update_traces(marker_line_color="#5A5A5A", marker_line_width=1)
            st.plotly_chart(fig_dist, use_container_width=True)

        with col_g2:
            fig_box = px.box(
                df_filtrado,
                x='senioridade',
                y='usd',
                title=" Boxplot dos Salários Anuais em USD",
                labels={'usd': 'Salário Anual (USD)'},
                color_discrete_sequence=["#fafafa"]
            )
            fig_box.update_layout(
                paper_bgcolor="#262730",
                plot_bgcolor="#262730",
                font={'color': "#fafafa"},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=False,
                xaxis=dict(gridcolor="#e9ecef", linecolor="#e9ecef"),
                yaxis=dict(gridcolor="#e9ecef", linecolor="#e9ecef")
            )
            st.plotly_chart(fig_box, use_container_width=True)

        col3_g3, col_g4 = st.columns(2)

        with col3_g3:
            remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
            remoto_contagem.columns = ['modalidade', 'quantidade']
            
            fig_remoto = px.pie(
                remoto_contagem,
                names='modalidade',
                values='quantidade',
                title=' Modalidade de Trabalho',
                hole=0.55,
                color_discrete_sequence=["#fafafa", "#5A5A5A", "#aeb1b4"]
            )
            fig_remoto.update_traces(
                textposition='outside',
                textinfo='percent+label',
                textfont_size=11,
                textfont_color='#fafafa'
            )
            fig_remoto.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=False,
                annotations=[dict(text=f'{total_registros:,}', x=0.5, y=0.5, font_size=16, showarrow=False, font_color='#212529')]
            )
            st.plotly_chart(fig_remoto, use_container_width=True)

        with col_g4:
            tamanho_contagem = df_filtrado['tamanho_empresa'].value_counts().reset_index()
            tamanho_contagem.columns = ['tamanho', 'quantidade']
            
            fig_tamanho = px.bar(
                tamanho_contagem,
                x='tamanho',
                y='quantidade',
                title=' Distribuição por Tamanho de Empresa',
                labels={'quantidade': 'Quantidade', 'tamanho': 'Tamanho'},
                color='quantidade',
                color_continuous_scale=["#fafafa", "#5A5A5A", "#aeb1b4"]
            )
            fig_tamanho.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da'),
                yaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da')
            )
            st.plotly_chart(fig_tamanho, use_container_width=True)
        
        if len(anos_selecionados) > 1:
            evolucao_ano = df_filtrado.groupby('ano').agg({'usd': ['mean', 'median']}).reset_index()
            evolucao_ano.columns = ['ano', 'media', 'mediana']
            
            fig_evolucao = go.Figure()
            
            fig_evolucao.add_trace(go.Scatter(
                x=evolucao_ano['ano'],
                y=evolucao_ano['media'],
                mode='lines+markers',
                name='Média',
                line=dict(color='#fafafa', width=2),
                marker=dict(size=8)
            ))
            
            fig_evolucao.add_trace(go.Scatter(
                x=evolucao_ano['ano'],
                y=evolucao_ano['mediana'],
                mode='lines+markers',
                name='Mediana',
                line=dict(color='#aeb1b4', width=2),
                marker=dict(size=8)
            ))
            
            fig_evolucao.update_layout(
                title='Evolução Salarial ao Longo dos Anos',
                xaxis_title='Ano',
                yaxis_title='Salário (USD)',
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode='x unified',
                xaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da'),
                yaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da')
            )
            st.plotly_chart(fig_evolucao, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
# tab2 - análise por cargo
with tab2:
    if not df_filtrado.empty:
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.caption("Cargos com maior remuneração média. Barras mais escuras indicam salários mais altos.")
            top_cargos = df_filtrado.groupby('cargo')['usd'].agg(['mean', 'count']).reset_index()
            top_cargos.columns = ['cargo', 'media', 'quantidade']
            top_cargos = top_cargos[top_cargos['quantidade'] >= 5].nlargest(15, 'media').sort_values('media', ascending=True)
            
            fig_top_cargos = px.bar(
                top_cargos,
                x='media',
                y='cargo',
                orientation='h',
                title="Top 15 Cargos por Salário Médio",
                labels={'media': 'Salário Médio (USD)', 'cargo': ''},
                color='media',
                color_continuous_scale=[[0, '#adb5bd'], [1, '#212529']],
                text=top_cargos['media'].apply(lambda x: f'${x:,.0f}')
            )
            fig_top_cargos.update_traces(textposition='outside', textfont_size=9, textfont_color='#fafafa')
            fig_top_cargos.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                coloraxis_showscale=False,
                height=500,
                xaxis=dict(gridcolor='#262730', linecolor='#e9ecef'),
                yaxis=dict(gridcolor='#262730', linecolor='#e9ecef')
            )
            st.plotly_chart(fig_top_cargos, use_container_width=True)
        
        with col_c2:
            st.caption("Cargos com maior número de registros no dataset. Barras mais escuras indicam maior frequência.")
            cargos_frequentes = df_filtrado['cargo'].value_counts().head(15).reset_index()
            cargos_frequentes.columns = ['cargo', 'quantidade']
            cargos_frequentes = cargos_frequentes.sort_values('quantidade', ascending=True)
            
            fig_freq_cargos = px.bar(
                cargos_frequentes,
                x='quantidade',
                y='cargo',
                orientation='h',
                title="Top 15 Cargos Mais Frequentes",
                labels={'quantidade': 'Quantidade', 'cargo': ''},
                color='quantidade',
                color_continuous_scale=[[0, '#adb5bd'], [1, '#212529']],
                text='quantidade'
            )
            fig_freq_cargos.update_traces(textposition='outside', textfont_size=9, textfont_color='#fafafa')
            fig_freq_cargos.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                coloraxis_showscale=False,
                height=500,
                xaxis=dict(gridcolor='#262730', linecolor='#e9ecef'),
                yaxis=dict(gridcolor='#262730', linecolor='#e9ecef')
            )
            st.plotly_chart(fig_freq_cargos, use_container_width=True)
        
        st.markdown("#### Salário por Cargo e Senioridade")
        st.caption("Matriz que cruza cargos e níveis de senioridade. Células mais escuras representam salários mais elevados.")
        
        cargos_populares = df_filtrado['cargo'].value_counts().head(8).index.tolist()
        df_comparativo = df_filtrado[df_filtrado['cargo'].isin(cargos_populares)]
        
        fig_heatmap = px.density_heatmap(
            df_comparativo,
            x='cargo',
            y='senioridade',
            z='usd',
            histfunc='avg',
            title="Heatmap: Salário Médio por Cargo e Senioridade",
            labels={'usd': 'Salário Médio (USD)'},
            color_continuous_scale=[[0, '#adb5bd'], [1, '#212529']]
        )
        fig_heatmap.update_layout(
            paper_bgcolor='#262730',
            plot_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'},
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.caption("Tamanho dos blocos representa o volume de registros. Cores mais escuras indicam salários maiores.")
        cargo_tree = df_filtrado.groupby('cargo').agg({'usd': 'mean', 'ano': 'count'}).reset_index()
        cargo_tree.columns = ['cargo', 'salario_medio', 'quantidade']
        cargo_tree = cargo_tree[cargo_tree['quantidade'] >= 5].head(20)
        
        fig_tree = px.treemap(
            cargo_tree,
            path=['cargo'],
            values='quantidade',
            color='salario_medio',
            title='Treemap: Cargos por Volume e Salário',
            color_continuous_scale=[[0, '#adb5bd'], [1, '#212529']],
            labels={'salario_medio': 'Salário Médio', 'quantidade': 'Quantidade'}
        )
        fig_tree.update_layout(
            paper_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'}
        )
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
# tab3 - análise geográfica
with tab3:
    if not df_filtrado.empty:
        st.markdown("#### Mapa Global de Salários")
        st.caption("Visualização geográfica dos salários médios. Países mais escuros oferecem maiores remunerações.")
        
        media_por_pais = df_filtrado.groupby('residencia_iso3').agg({'usd': ['mean', 'count']}).reset_index()
        media_por_pais.columns = ['pais', 'salario_medio', 'quantidade']
        
        fig_mapa = px.choropleth(
            media_por_pais,
            locations='pais',
            color='salario_medio',
            hover_name='pais',
            hover_data={'quantidade': True, 'salario_medio': ':,.0f'},
            color_continuous_scale='RdYlGn',
            title='Salário Médio por País de Residência',
            labels={'salario_medio': 'Salário Médio (USD)', 'quantidade': 'Registros'}
        )
        fig_mapa.update_layout(
            paper_bgcolor="#262730",
            geo=dict(
                bgcolor='#262730',
                showframe=False,
                showcoastlines=True,
                coastlinecolor='#000000',
                showland=True,
                landcolor='#f8f9fa',
                showocean=True,
                oceancolor='#262730'
            ),
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'},
            height=500
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        col_geo1, col_geo2 = st.columns(2)
        
        with col_geo1:
            st.caption("Países com os maiores salários médios (mín. 10 registros).")
            top_paises = media_por_pais[media_por_pais['quantidade'] >= 10].nlargest(10, 'salario_medio').sort_values('salario_medio', ascending=True)
            
            fig_paises = px.bar(
                top_paises,
                x='salario_medio',
                y='pais',
                orientation='h',
                title="Top 10 Países por Salário",
                labels={'salario_medio': 'Salário Médio (USD)', 'pais': 'País'},
                color='salario_medio',
                color_continuous_scale='RdYlGn',
                text=top_paises['salario_medio'].apply(lambda x: f'${x:,.0f}')
            )
            fig_paises.update_traces(textposition='outside', textfont_size=9, textfont_color='#fafafa')
            fig_paises.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='#262730', linecolor='#9da2a5'),
                yaxis=dict(gridcolor='#262730', linecolor='#9da2a5')
            )
            st.plotly_chart(fig_paises, use_container_width=True)
        
        with col_geo2:
            st.caption("Países com maior número de profissionais no dataset.")
            top_paises_volume = media_por_pais.nlargest(10, 'quantidade').sort_values('quantidade', ascending=True)
            
            fig_volume = px.bar(
                top_paises_volume,
                x='quantidade',
                y='pais',
                orientation='h',
                title="Top 10 Países por Volume",
                labels={'quantidade': 'Quantidade', 'pais': 'País'},
                color='quantidade',
                color_continuous_scale='RdYlGn',
                text='quantidade'
            )
            fig_volume.update_traces(textposition='outside', textfont_size=9, textfont_color='#fafafa')
            fig_volume.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='#262730', linecolor='#9da2a5'),
                yaxis=dict(gridcolor='#262730', linecolor='#9da2a5')
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        st.caption("Hierarquia mostrando como cada país distribui suas vagas entre modalidades de trabalho.")
        fig_sunburst = px.sunburst(
            df_filtrado.groupby(['residencia_iso3', 'remoto']).size().reset_index(name='quantidade'),
            path=['residencia_iso3', 'remoto'],
            values='quantidade',
            title='Distribuição: País e Modalidade de Trabalho',
            color='quantidade',
            color_continuous_scale='RdYlGn'
        )
        fig_sunburst.update_layout(
            paper_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'}
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
# tab4 - análise avançada
with tab4:
    if not df_filtrado.empty:
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            st.caption("Formato do violino mostra a densidade salarial. Box interno indica mediana e quartis.")
            fig_violin = px.violin(
                df_filtrado,
                x='remoto',
                y='usd',
                color='remoto',
                box=True,
                points='outliers',
                title="Distribuição Salarial por Modalidade",
                labels={'usd': 'Salário (USD)', 'remoto': 'Modalidade'},
                color_discrete_sequence=["#fafafa"]
            )
            fig_violin.update_layout(
                paper_bgcolor='#262730',
                plot_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=False,
                xaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da'),
                yaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da')
            )
            st.plotly_chart(fig_violin, use_container_width=True)
        
        with col_a2:
            st.caption("Comparação multidimensional entre níveis. Maior área indica melhor desempenho geral.")
            senior_stats = df_filtrado.groupby('senioridade').agg({'usd': ['mean', 'median', 'std', 'count']}).reset_index()
            senior_stats.columns = ['senioridade', 'media', 'mediana', 'desvio', 'quantidade']
            
            for col in ['media', 'mediana', 'desvio', 'quantidade']:
                senior_stats[f'{col}_norm'] = (senior_stats[col] - senior_stats[col].min()) / (senior_stats[col].max() - senior_stats[col].min() + 0.01)
            
            fig_radar = go.Figure()
            
            for idx, row in senior_stats.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row['media_norm'], row['mediana_norm'], row['desvio_norm'], row['quantidade_norm']],
                    theta=['Média', 'Mediana', 'Variabilidade', 'Volume'],
                    fill='toself',
                    name=row['senioridade'],
                    line_color=(["#fafafa"])[idx % len(["#fafafa"])]
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor='#e9ecef'),
                    bgcolor='#262730'
                ),
                title='Comparativo por Senioridade',
                paper_bgcolor='#262730',
                font={'color': '#fafafa'},
                title_font={'size': 14, 'color': '#fafafa'},
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        st.caption("Relação entre popularidade do cargo e remuneração. Tamanho da bolha indica variabilidade salarial.")
        cargo_scatter = df_filtrado.groupby('cargo').agg({'usd': ['mean', 'std'], 'ano': 'count'}).reset_index()
        cargo_scatter.columns = ['cargo', 'salario_medio', 'desvio', 'quantidade']
        cargo_scatter = cargo_scatter[cargo_scatter['quantidade'] >= 5].sort_values('salario_medio', ascending=True)
        
        fig_scatter = px.scatter(
            cargo_scatter,
            x='quantidade',
            y='salario_medio',
            size='desvio',
            color='salario_medio',
            hover_name='cargo',
            title='Volume de Vagas vs Salário Médio',
            labels={'quantidade': 'Número de Registros', 'salario_medio': 'Salário Médio (USD)', 'desvio': 'Variabilidade'},
            color_continuous_scale='RdYlGn',
            size_max=50
        )
        fig_scatter.update_layout(
            paper_bgcolor='#262730',
            plot_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'},
            xaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da'),
            yaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("#### Análise por Tipo de Contrato")
        st.caption("Comparação salarial entre tipos de contrato, segmentado por nível de senioridade.")
        
        contrato_stats = df_filtrado.groupby(['contrato', 'senioridade'])['usd'].mean().reset_index()
        
        fig_grouped = px.bar(
            contrato_stats,
            x='contrato',
            y='usd',
            color='senioridade',
            barmode='group',
            title='Salário Médio: Tipo de Contrato vs Senioridade',
            labels={'usd': 'Salário Médio (USD)', 'contrato': 'Tipo de Contrato', 'senioridade': 'Nível'},
            color_discrete_sequence=["#000000", "#6c757d", "#34373A", "#495057"]
        )
        fig_grouped.update_layout(
            paper_bgcolor='#262730',
            plot_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da'),
            yaxis=dict(gridcolor='#e9ecef', linecolor='#ced4da')
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
        st.caption("Proporção de profissionais em cada nível de carreira no mercado de dados.")
        funnel_data = df_filtrado['senioridade'].value_counts().reset_index()
        funnel_data.columns = ['senioridade', 'quantidade']
        ordem_senioridade = ['Junior', 'Pleno', 'Senior', 'Executive']
        funnel_data['ordem'] = funnel_data['senioridade'].apply(lambda x: ordem_senioridade.index(x) if x in ordem_senioridade else 99)
        funnel_data = funnel_data.sort_values('ordem')
        
        fig_funnel = px.funnel(
            funnel_data,
            x='quantidade',
            y='senioridade',
            title='Distribuição por Nível de Senioridade',
            color='senioridade',
            color_discrete_sequence=["#9da2a5"]
        )
        fig_funnel.update_layout(
            paper_bgcolor='#262730',
            font={'color': '#fafafa'},
            title_font={'size': 14, 'color': '#fafafa'},
            showlegend=False
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")


# tabela de dados detalhados
st.subheader("📋 Tabela de Dados Detalhados")

st.dataframe(df_filtrado, use_container_width=True)

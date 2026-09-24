import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Painel Xbox Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Cor de fundo geral */
    .stApp {
        background-color: #0f1216;
        color: #e2e8f0;
    }
    
    /* Estilo da sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #232a36;
    }
    
    /* Cards dos indicadores (KPIs) */
    .kpi-card {
        background: #171d25;
        border: 1px solid #263040;
        border-left: 4px solid #107C41;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 700;
    }
    .kpi-sub {
        color: #107C41;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Linhas divisórias e abas */
    hr {
        border-color: #263040;
    }
    button[data-baseweb="tab"] {
        color: #94a3b8;
        font-weight: 500;
    }
    button[aria-selected="true"] {
        color: #107C41 !important;
        border-bottom-color: #107C41 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def gerar_dados():
    np.random.seed(42)
    datas = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    categorias = ["Consoles", "Jogos Físicos", "Acessórios", "Game Pass", "Hardware PC"]
    plataformas = ["Xbox Series X|S", "PC Game Pass", "Xbox Cloud Gaming"]
    
    dados = {
        "Data": np.random.choice(datas, 1200),
        "Categoria": np.random.choice(categorias, 1200, p=[0.15, 0.30, 0.20, 0.25, 0.10]),
        "Plataforma": np.random.choice(plataformas, 1200, p=[0.50, 0.30, 0.20]),
        "Valor": np.random.uniform(40, 4200, 1200).round(2),
        "Quantidade": np.random.randint(1, 4, 1200)
    }
    df = pd.DataFrame(dados)
    df["Mês"] = df["Data"].dt.strftime("%Y-%m")
    return df

df = gerar_dados()

st.sidebar.markdown("### 🎮 Painel de Filtros")
st.sidebar.caption("Escolha as opções abaixo para atualizar os indicadores:")

plataformas_disponiveis = list(df["Plataforma"].unique())
filtro_plataforma = st.sidebar.multiselect(
    "Plataformas",
    options=plataformas_disponiveis,
    default=plataformas_disponiveis
)

categorias_disponiveis = list(df["Categoria"].unique())
filtro_categoria = st.sidebar.multiselect(
    "Categorias de Produto",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

df_filtrado = df[
    (df["Plataforma"].isin(filtro_plataforma)) &
    (df["Categoria"].isin(filtro_categoria))
]

st.title("Xbox — Vendas e Assinaturas Globais")
st.caption("Painel de acompanhamento do desempenho do ecossistema de jogos Xbox")
st.markdown("---")

if df_filtrado.empty:
    st.warning("Não há dados para os filtros escolhidos. Altere as seleções na barra lateral para continuar.")
    st.stop()

receita_total = df_filtrado["Valor"].sum()
total_transacoes = len(df_filtrado)
ticket_medio = receita_total / total_transacoes
top_categoria = df_filtrado["Categoria"].value_counts().index[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Receita Total</div>
        <div class="kpi-value">R$ {receita_total:,.2f}</div>
        <div class="kpi-sub">● Faturamento Bruto</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total de Pedidos</div>
        <div class="kpi-value">{total_transacoes:,}</div>
        <div class="kpi-sub">● Transações Registradas</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Ticket Médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.2f}</div>
        <div class="kpi-sub">● Média por Pedido</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Categoria Destaque</div>
        <div class="kpi-value" style="font-size: 1.35rem;">{top_categoria}</div>
        <div class="kpi-sub">● Mais Vendida</div>
    </div>
    """, unsafe_allow_html=True)

tab_graficos, tab_detalhes, tab_dados = st.tabs([
    "📈 Tendências e Categorias", 
    "📊 Vendas por Plataforma", 
    "📋 Dados Detalhados"
])

with tab_graficos:
    col_esq, col_dir = st.columns([1.5, 1])
    
    with col_esq:
        st.subheader("Receita ao Longo dos Meses")
        df_mensal = df_filtrado.groupby("Mês", as_index=False)["Valor"].sum()
        
        grafico_area = alt.Chart(df_mensal).mark_area(
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='#107C41', offset=0),
                    alt.GradientStop(color='rgba(16, 124, 65, 0.05)', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            ),
            line={'color': '#2ebd59', 'size': 2.5}
        ).encode(
            x=alt.X("Mês:N", title=None, axis=alt.Axis(labelColor="#94a3b8", labelAngle=0)),
            y=alt.Y("Valor:Q", title="Receita (R$)", axis=alt.Axis(labelColor="#94a3b8", gridColor="#263040", format="~s")),
            tooltip=[alt.Tooltip("Mês:N"), alt.Tooltip("Valor:Q", format=",.2f", title="Receita (R$)")]
        ).properties(height=320).configure_view(strokeOpacity=0).configure(background="transparent")
        
        st.altair_chart(grafico_area, use_container_width=True)

    with col_dir:
        st.subheader("Faturamento por Categoria")
        df_cat = df_filtrado.groupby("Categoria", as_index=False)["Valor"].sum().sort_values(by="Valor", ascending=False)
        
        grafico_barras = alt.Chart(df_cat).mark_bar(
            cornerRadiusTopRight=4,
            cornerRadiusBottomRight=4,
            color="#107C41"
        ).encode(
            x=alt.X("Valor:Q", title=None, axis=alt.Axis(labelColor="#94a3b8", gridColor="#263040", format="~s")),
            y=alt.Y("Categoria:N", sort="-x", title=None, axis=alt.Axis(labelColor="#cbd5e1")),
            tooltip=[alt.Tooltip("Categoria:N"), alt.Tooltip("Valor:Q", format=",.2f", title="Total (R$)")]
        ).properties(height=320).configure_view(strokeOpacity=0).configure(background="transparent")
        
        st.altair_chart(grafico_barras, use_container_width=True)

with tab_detalhes:
    st.subheader("Resultado por Plataforma de Acesso")
    df_plat = df_filtrado.groupby("Plataforma", as_index=False)["Valor"].sum()
    
    grafico_plat = alt.Chart(df_plat).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color="#2ebd59"
    ).encode(
        x=alt.X("Plataforma:N", title=None, axis=alt.Axis(labelColor="#cbd5e1", labelAngle=0)),
        y=alt.Y("Valor:Q", title="Total de Vendas (R$)", axis=alt.Axis(labelColor="#94a3b8", gridColor="#263040", format="~s")),
        tooltip=[alt.Tooltip("Plataforma:N"), alt.Tooltip("Valor:Q", format=",.2f")]
    ).properties(height=300).configure_view(strokeOpacity=0).configure(background="transparent")
    
    st.altair_chart(grafico_plat, use_container_width=True)

with tab_dados:
    st.subheader("Tabela com Filtros Aplicados")
    st.dataframe(df_filtrado, use_container_width=True)
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados em CSV",
        data=csv,
        file_name='vendas_xbox_filtradas.csv',
        mime='text/csv'
    )
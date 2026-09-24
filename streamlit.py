import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Painel Analytics",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0e0f13;
        --surface: #171920;
        --border: rgba(148, 163, 184, 0.10);
        --text: #e6edf3;
        --muted: #8b98a9;
        --accent: #ff3c28;
        --accent-dark: #e60012;
        --accent-blue: #0ab9e6;
    }

    /* Fundo geral com brilho verde suave */
    .stApp {
        background:
            radial-gradient(900px 500px at 0% 0%, rgba(255, 60, 40, 0.14), transparent 60%),
            radial-gradient(700px 400px at 100% 0%, rgba(10, 185, 230, 0.12), transparent 60%),
            var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16171d 0%, #0f1014 100%);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] h3 {
        color: var(--accent);
        font-weight: 700;
    }

    /* Título com degradê */
    .stApp h1 {
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, var(--accent) 0%, #ff8a7a 50%, var(--accent-blue) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .stApp h3 {
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* Cards dos indicadores (KPIs) */
    .kpi-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(145deg, rgba(24, 33, 43, 0.92), rgba(14, 20, 27, 0.92));
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent-blue));
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 60, 40, 0.40);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45), 0 0 24px rgba(255, 60, 40, 0.15);
    }
    .kpi-title {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .kpi-sub {
        color: var(--accent);
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Linhas divisórias e abas */
    hr {
        border-color: var(--border);
    }
    div[data-baseweb="tab-list"] {
        gap: 6px;
    }
    button[data-baseweb="tab"] {
        color: var(--muted);
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        padding: 8px 14px;
    }
    button[data-baseweb="tab"]:hover {
        color: var(--text);
        background: rgba(255, 60, 40, 0.07);
    }
    button[aria-selected="true"] {
        color: var(--accent) !important;
        background: rgba(255, 60, 40, 0.10) !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: var(--accent) !important;
    }

    /* Botão de download */
    .stDownloadButton button {
        background: linear-gradient(90deg, var(--accent-dark), var(--accent));
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.2rem;
        transition: filter 0.2s ease, transform 0.2s ease;
    }
    .stDownloadButton button:hover {
        filter: brightness(1.1);
        transform: translateY(-1px);
        color: #ffffff;
    }

    /* Tabela */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def gerar_dados():
    np.random.seed(42)
    datas = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    categorias = ["Consoles", "Jogos Físicos", "Acessórios", "Switch Online", "Amiibo"]
    plataformas = ["Nintendo Switch", "Switch OLED", "Switch Lite"]
    
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

st.sidebar.markdown("### 🍄 Painel de Filtros")
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

st.title("Vendas e Assinaturas Globais")
st.caption("Painel de acompanhamento do desempenho do ecossistema de jogos Nintendo")
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
                    alt.GradientStop(color='rgba(255, 60, 40, 0.02)', offset=0),
                    alt.GradientStop(color='rgba(255, 60, 40, 0.55)', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            ),
            line={'color': '#ff3c28', 'size': 2.5},
            interpolate='monotone'
        ).encode(
            x=alt.X("Mês:N", title=None, axis=alt.Axis(labelColor="#8b98a9", titleColor="#8b98a9", labelAngle=0)),
            y=alt.Y("Valor:Q", title="Receita (R$)", axis=alt.Axis(labelColor="#8b98a9", titleColor="#8b98a9", gridColor="rgba(148, 163, 184, 0.10)", domain=False, tickColor="rgba(0,0,0,0)", format="~s")),
            tooltip=[alt.Tooltip("Mês:N"), alt.Tooltip("Valor:Q", format=",.2f", title="Receita (R$)")]
        ).properties(height=320).configure_view(strokeOpacity=0).configure(background="transparent")
        
        st.altair_chart(grafico_area, use_container_width=True)

    with col_dir:
        st.subheader("Faturamento por Categoria")
        df_cat = df_filtrado.groupby("Categoria", as_index=False)["Valor"].sum().sort_values(by="Valor", ascending=False)
        
        grafico_barras = alt.Chart(df_cat).mark_bar(
            cornerRadiusTopRight=4,
            cornerRadiusBottomRight=4,
            color="#0ab9e6"
        ).encode(
            x=alt.X("Valor:Q", title=None, axis=alt.Axis(labelColor="#8b98a9", titleColor="#8b98a9", gridColor="rgba(148, 163, 184, 0.10)", domain=False, tickColor="rgba(0,0,0,0)", format="~s")),
            y=alt.Y("Categoria:N", sort="-x", title=None, axis=alt.Axis(labelColor="#e6edf3", domain=False, tickColor="rgba(0,0,0,0)")),
            tooltip=[alt.Tooltip("Categoria:N"), alt.Tooltip("Valor:Q", format=",.2f", title="Total (R$)")]
        ).properties(height=320).configure_view(strokeOpacity=0).configure(background="transparent")
        
        st.altair_chart(grafico_barras, use_container_width=True)

with tab_detalhes:
    st.subheader("Resultado por Plataforma de Acesso")
    df_plat = df_filtrado.groupby("Plataforma", as_index=False)["Valor"].sum()
    
    grafico_plat = alt.Chart(df_plat).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='#e60012', offset=0),
                alt.GradientStop(color='#ff3c28', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X("Plataforma:N", title=None, axis=alt.Axis(labelColor="#e6edf3", domain=False, tickColor="rgba(0,0,0,0)", labelAngle=0)),
        y=alt.Y("Valor:Q", title="Total de Vendas (R$)", axis=alt.Axis(labelColor="#8b98a9", titleColor="#8b98a9", gridColor="rgba(148, 163, 184, 0.10)", domain=False, tickColor="rgba(0,0,0,0)", format="~s")),
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
        file_name='vendas_nintendo_filtradas.csv',
        mime='text/csv'
    )
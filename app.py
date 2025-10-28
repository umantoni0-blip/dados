import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard • Salário x Idade x Sexo", layout="wide")

# =========================
# Dados padrão (do seu app)
# =========================
dados = [
    ["Masculino", 40190.82, 47],
    ["Masculino", 35433.00, 42],
    ["Masculino", 30186.02, 47],
    ["Masculino", 26471.00, 55],
    ["Masculino", 24664.32, 38],
    ["Feminino", 23654.48, 48],
    ["Masculino", 22575.00, 41],
    ["Masculino", 21200.70, 51],
    ["Masculino", 21184.19, 40],
    ["Masculino", 17107.84, 49],
    ["Masculino", 16169.00, 39],
    ["Masculino", 15956.00, 35],
    ["Masculino", 15675.00, 34],
    ["Masculino", 15379.44, 36],
    ["Feminino", 15254.51, 29],
    ["Feminino", 14500.00, 34],
    ["Masculino", 14210.47, 34],
    ["Masculino", 14118.32, 33],
    ["Masculino", 13011.00, 42],
    ["Masculino", 12809.98, 34],
    ["Masculino", 12101.97, 40],
    ["Masculino", 11998.96, 37],
    ["Masculino", 11360.00, 43],
    ["Masculino", 11200.00, 28],
    ["Masculino", 10764.26, 31],
    ["Masculino", 10733.00, 40],
    ["Masculino", 10326.00, 31],
    ["Masculino", 10191.68, 30],
    ["Feminino", 10022.80, 35],
    ["Masculino", 9984.66, 32],
    ["Masculino", 9808.33, 37],
    ["Masculino", 9292.00, 31],
    ["Masculino", 9197.86, 31],
    ["Masculino", 9047.04, 30],
    ["Masculino", 9000.00, 33],
    ["Masculino", 8726.64, 33],
    ["Masculino", 8389.93, 31],
    ["Masculino", 7965.03, 30],
    ["Feminino", 7890.81, 26],
    ["Masculino", 7627.39, 36],
    ["Feminino", 7559.64, 26],
    ["Masculino", 7509.48, 38],
    ["Masculino", 7371.00, 38],
    ["Masculino", 7331.75, 31],
    ["Masculino", 7208.73, 28],
    ["Masculino", 7011.65, 28],
    ["Feminino", 7000.00, 42],
    ["Feminino", 6705.79, 24],
    ["Masculino", 6485.66, 39],
    ["Masculino", 6447.00, 27],
    ["Masculino", 6046.20, 24],
    ["Masculino", 6045.60, 30],
    ["Masculino", 5934.00, 36],
    ["Masculino", 5814.00, 26],
    ["Masculino", 5671.27, 34],
    ["Feminino", 4750.00, 27],
    ["Masculino", 4538.25, 25],
    ["Feminino", 4434.58, 42],
    ["Feminino", 4000.00, 26],
    ["Feminino", 3695.36, 29],
    ["Masculino", 3010.73, 24],
    ["Masculino", 2500.00, 24],
    ["Masculino", 2500.00, 24],
    ["Masculino", 2267.20, 25],
    ["Feminino", 1902.00, 25],
    ["Masculino", 1800.00, 21],
    ["Masculino", 1445.00, 25],
]
df_default = pd.DataFrame(dados, columns=["Sexo", "Salario", "Idade"])

# ==================================
# Sidebar • Upload + Filtros
# ==================================
st.sidebar.header("Configurações")
uploaded = st.sidebar.file_uploader("Envie um CSV opcional (colunas: Sexo, Salario, Idade)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    # Normaliza nomes de colunas
    df.columns = [c.strip().capitalize() for c in df.columns]
    # Tenta converter vírgula decimal -> ponto
    if df["Salario"].dtype == "object":
        df["Salario"] = (
            df["Salario"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        )
    df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce")
    df["Idade"]   = pd.to_numeric(df["Idade"], errors="coerce")
    df = df.dropna(subset=["Sexo", "Salario", "Idade"])
else:
    df = df_default.copy()

sexos = sorted(df["Sexo"].dropna().unique().tolist())
sexo_sel = st.sidebar.multiselect("Sexo", options=sexos, default=sexos)
idade_min, idade_max = int(df["Idade"].min()), int(df["Idade"].max())
idade_range = st.sidebar.slider("Faixa etária", min_value=idade_min, max_value=idade_max, value=(idade_min, idade_max), step=1)

# Filtra
mask = (df["Sexo"].isin(sexo_sel)) & (df["Idade"].between(idade_range[0], idade_range[1]))
df_f = df.loc[mask].copy()

# =========================
# KPIs (cards superiores)
# =========================
st.title("💰 Dashboard — Salário × Idade × Sexo")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Registros", len(df_f))
col2.metric("Salário médio (R$)", f"{df_f['Salario'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Idade média (anos)", f"{df_f['Idade'].mean():.1f}")
col4.metric("Salário máx (R$)", f"{df_f['Salario'].max():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.caption("Use os filtros na barra lateral para refinar as análises.")

# =========================
# Abas de visualização
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Linhas (média por Idade e Sexo)",
    "🟢 Dispersão (pontos individuais)",
    "📦 Boxplot (distribuição por Sexo)",
    "📊 Histograma (Idade)"
])

# ---- Tab 1: Linhas (média por Idade e Sexo) ----
with tab1:
    st.subheader("Variação do salário conforme a idade (média por sexo)")
    df_media = (
        df_f.groupby(["Idade", "Sexo"], as_index=False)["Salario"]
        .mean()
        .sort_values(["Sexo", "Idade"])
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for sexo in df_media["Sexo"].unique():
        ss = df_media[df_media["Sexo"] == sexo]
        ax.plot(ss["Idade"], ss["Salario"], marker="o", label=sexo)

    ax.set_xlabel("Idade (anos)")
    ax.set_ylabel("Salário médio (R$)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(title="Sexo")
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown(
        "- **Quando usar**: gráfico de linhas é indicado para **tendência em variável contínua** (idade/tempo),"
        " comparando grupos (sexo)."
    )

    st.download_button(
        "⬇️ Baixar dados agregados (CSV)",
        data=df_media.to_csv(index=False).encode("utf-8"),
        file_name="media_salario_por_idade_sexo.csv",
        mime="text/csv"
    )

# ---- Tab 2: Dispersão (pontos) ----
with tab2:
    st.subheader("Pontos individuais de salário por idade (cores por sexo)")
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    for sexo in df_f["Sexo"].unique():
        ss = df_f[df_f["Sexo"] == sexo]
        ax2.scatter(ss["Idade"], ss["Salario"], label=sexo)
    ax2.set_xlabel("Idade (anos)")
    ax2.set_ylabel("Salário (R$)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(title="Sexo")
    fig2.tight_layout()
    st.pyplot(fig2)

# ---- Tab 3: Boxplot ----
with tab3:
    st.subheader("Distribuição salarial por sexo (boxplot)")
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    grupos = [df_f.loc[df_f["Sexo"] == s, "Salario"].values for s in sexo_sel]
    ax3.boxplot(grupos, labels=sexo_sel, vert=True, showfliers=True)
    ax3.set_ylabel("Salário (R$)")
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    fig3.tight_layout()
    st.pyplot(fig3)

# ---- Tab 4: Histograma de Idade ----
with tab4:
    st.subheader("Distribuição de idades (histograma)")
    fig4, ax4 = plt.subplots(figsize=(8, 4.5))
    ax4.hist(df_f["Idade"], bins=range(idade_min, idade_max + 2, 2))
    ax4.set_xlabel("Idade (anos)")
    ax4.set_ylabel("Frequência")
    ax4.grid(axis="y", linestyle="--", alpha=0.5)
    fig4.tight_layout()
    st.pyplot(fig4)

# Rodapé
st.caption("Fonte: base entregue pelo grupo. Gráficos gerados com matplotlib no Streamlit.")

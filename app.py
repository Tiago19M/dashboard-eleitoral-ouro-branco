import time

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Meu Dashboard"
)

BASE = Path(__file__).parent
PASTA_MAPAS = BASE / "mapas"

PASTA_TURNO1 = PASTA_MAPAS / "turno1"
PASTA_TURNO2 = PASTA_MAPAS / "turno2"
PASTA_DADOS = BASE / "dados"

candidatos = [
    "AUGUSTO JORGE CURY",
    "FLAVIO NANTES BOLSONARO",
    "LUIZ INÁCIO LULA DA SILVA",
    "RENAN ANTONIO FERREIRA DOS SANTOS",
    "RONALDO RAMOS CAIADO",
    "ROMEU ZEMA NETO",
]

nomes_exibicao = {
    "AUGUSTO JORGE CURY" : "Augusto Cury",
    "FLAVIO NANTES BOLSONARO" : "Flávio Bolsonaro",
    "LUIZ INÁCIO LULA DA SILVA" : "Lula",
    "RENAN ANTONIO FERREIRA DOS SANTOS" : "Renan Santos",
    "RONALDO RAMOS CAIADO" : "Caiado",
    "ROMEU ZEMA NETO" : "Romeu Zema",
}

paletas = {
    "FLAVIO NANTES BOLSONARO" : "#086788",
    "LUIZ INÁCIO LULA DA SILVA" : "#DD1C1A",
    "AUGUSTO JORGE CURY" : "#696773",
    "RENAN ANTONIO FERREIRA DOS SANTOS" : "#F0C808",
    "RONALDO RAMOS CAIADO" : "#109648",
    "ROMEU ZEMA NETO" : "#FF8200",
}


#DADOS

#Carregamento dos dados
@st.cache_data
def ler_csv_votos(caminho_dados):
    return pd.read_csv(caminho_dados)

def carregar_votos():
    caminho_dados = PASTA_DADOS / "votos_por_local.csv"
    if not caminho_dados.exists():
        return None
    return ler_csv_votos(caminho_dados)

#Exibição dos dados

def grafico_votos (por_candidato):
    df = por_candidato.reset_index()
    df.columns = ["candidato", "votos"]
    df["nome"] = df["candidato"].map(nomes_exibicao)
    df = df.sort_values("votos")

    fig =  px.bar(df, x="votos", y="nome", orientation="h", text = "votos", color="candidato", color_discrete_map=paletas)
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title = "Votos válidos",
        yaxis_title = "Candidato",
        height = 120 + 50 * len(df),
        showlegend = False,
    )
    return fig


def exibir_dados(turno):
    votos = carregar_votos()
    if votos is None:
        st.error(f"Arquivo {PASTA_DADOS / 'votos_por_local.csv'} não encontrado. Adquira-o no repositório do projeto e verifique se o caminho está correto.")
        return
    
    if turno == "1º Turno":
        nr_turno = 1
    else:
        nr_turno = 2

    df = votos[(votos["TURNO"] == nr_turno) & (votos["NM_VOTAVEL"].isin(candidatos))]

    por_candidato = df.groupby("NM_VOTAVEL")["QT_VOTOS"].sum().sort_values(ascending=False)
    total = por_candidato.sum()

    #Indicadores
    c1, c2, c3 = st.columns(3)
    c1.metric("Votos válidos", f"{total:,}".replace(",", "."))
    c2.metric("Locais de votação", df["NR_LOCAL_VOTACAO"].nunique())
    c3.metric("Mais votado", por_candidato.index[0], f"{(por_candidato.iloc[0] / total * 100).round(2)}%")

    #Gráfico de barras
    st.subheader("Votos por candidato")
    st.plotly_chart(grafico_votos(por_candidato))

    #Tabela com os percentuais por candidato
    st.subheader("Percentual de votos válidos por local de votação")
    tabela = (df.pivot_table(index=["NM_LOCAL_VOTACAO", "NM_BAIRRO"], columns="NM_VOTAVEL", values="PERCENTUAL").round(2).reset_index())
    st.write(tabela)

    st.download_button(
        "Baixar tabela (CSV)",
        tabela.to_csv(index=False).encode("utf-8"),
        file_name=f"votos_por_local_turno{nr_turno}.csv",
        mime="text/csv",
    )

    st.warning("Os dados de votação por local são referentes somente aos 6 candidatos mais votados de Ouro Branco.")

#MAPAS

mapas_turno1 = {
    "Augusto Jorge Cury" : "mapa_turno1_cury.html",
    "Flávio Nantes Bolsonaro" : "mapa_turno1_flavio.html",
    "Luiz Inácio Lula da Silva" : "mapa_turno1_lula.html",
    "Renan Antônio Ferreira dos Santos" : "mapa_turno1_renan.html",
    "Ronaldo Ramos Caiado" : "mapa_turno1_caiado.html",
    "Romeu Zema Neto" : "mapa_turno1_zema.html",
}

mapa_turno2 = "comparacao_votos_turno2.html"

#Leitura e exibição dos mapas (HTML)
@st.cache_data
def ler_html (pasta, nome_arquivo):
    return (Path(pasta) / nome_arquivo).read_text(encoding="utf-8")

def exibir_mapa(pasta, nome_arquivo, altura=600):
    try:
        components.html(ler_html(str(pasta), nome_arquivo), height=altura)
    except:
        st.error(f"Arquivo não encontrado: {Path(pasta) / nome_arquivo}")

def exibir_metodologia():
    with st.expander("Metodologia utilizada"):
        with st.expander("Coleta de dados"):
            st.write("""
                    Os dados relativos ao número de votos por seção eleitoral
                    por candidato foram retirados do site oficial do TSE num
                    recorte de Minas Gerais e, posteriormente, filtrados utilizando
                    a biblioteca "pandas", de maneira a preservar somente os dados
                    de Ouro Branco.
                    """)
            st.write("""
                    Informações de latitude e longitude de cada local de votação foram
                    obtidos também via site oficial do TSE, porém num .csv distinto. Então,
                    foi necessário unir localização geográfica com os dados de votação, via
                    turno, zona e seção (colunas em comum).
                    """)
            st.write("""
                    Por fim, os limites do município de Ouro Branco - necessários para a formação
                    dos polígonos de Voronoi - foram extraídos do site oficial do IBGE, no formato
                    geojson.
                    """)
        with st.expander("Definição das regiões de votação"):
            st.write("""O TSE não disponibiliza polígonos das seções eleitorais, apenas as coordenadas
                    dos locais de votação (22 no total). Assim, para determinar as áreas correspondentes
                    à cada um dos 22 pontos representativos dos locais de votação, adotou-se um diagrama
                    de Voronoi recortado pelo limite municipal (fornecido pelo IBGE). Nesse modelo, cada 
                    ponto do território de Ouro Branco foi atribuído ao local de votação mais próximo e, 
                    portanto, as representações se tratam de uma aproximação geométrica, e não da área real 
                    de captação de eleitores.""")




def exibir_barra_lateral ():
    st.sidebar.title("Filtros do Dashboard")
    turno = st.sidebar.radio("Turno", ["1º Turno", "2º Turno"])

    candidatoAtual = None

    if turno == "1º Turno":
        st.sidebar.subheader("Selecione o candidato")
        candidatoAtual = st.sidebar.selectbox(
            "Candidato",
            [
                "Augusto Jorge Cury",
                "Flávio Nantes Bolsonaro",
                "Luiz Inácio Lula da Silva",
                "Renan Antônio Ferreira dos Santos",
                "Ronaldo Ramos Caiado",
                "Romeu Zema Neto"
            ],
            label_visibility = "collapsed"
        )
    return turno, candidatoAtual


def pagina_principal (turno, candidatoEscolhido):
    st.markdown(
        """
        <h1 style = "
            text-align: center;
            font-size: 35px;
            white-space: nowrap;
        ">
            Mapeamento eleitoral - Ouro Branco
        </h1>
        """,
        unsafe_allow_html=True  
    )

    tab1, tab2 = st.tabs(["Gráficos", "Dados"])
    with tab1:
        if turno == "1º Turno":
            st.subheader(f"Porcentagem dos votos válidos por local de votação - {candidatoEscolhido}")
            exibir_mapa(PASTA_TURNO1, mapas_turno1[candidatoEscolhido])
        else:
            st.subheader(f"2º Turno: porcentagem de votos válidos de Flávio Bolsonaro vs Lula, por local de votação")
            exibir_mapa(PASTA_TURNO2, mapa_turno2)
            st.warning("Flávio Bolsonaro teve maioria de votos nas regiões de tom azul, enquanto Lula, nas regiões de tom vermelho")
        st.info("Passe o mouse sobre cada região para obter um maior detalhamento do resultado")
        exibir_metodologia()
    with tab2:
        exibir_dados(turno)

turno, candidatoEscolhido = exibir_barra_lateral()
pagina_principal(turno, candidatoEscolhido)

import streamlit as st
import pandas as pd

def exibir_barra_lateral ():
    st.sidebar.title("Filtros do Dashboard")
    st.sidebar.header("1º Turno")
    st.sidebar.subheader("Selecione o candidato")

    candidatoAtual = st.sidebar.selectbox(
        "",
        [
            "Augusto Jorge Cury",
            "Flávio Nantes Bolsonaro",
            "Luiz Inácio Lula da Silva",
            "Renan Antônio Ferreira dos Santos",
            "Ronaldo Ramos Caiado",
            "Romeu Zema Neto"
        ]
    )

def pagina_principal ():
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
        st.write("Add gráficos aqui")
    with tab2:
        st.write("Add dataframes com dados aqui")

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
st.set_page_config(
    layout="wide",
    page_title="Meu Dashboard"
)

pagina_principal()
exibir_barra_lateral()
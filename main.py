"""
main.py — Ponto de entrada do sistema de recomendação de artigos acadêmicos.

Pipeline:
    1. Carregar dados (CSVs)
    2. Construir grafo bipartido
    3. Construir projeção artigo-artigo (Jaccard)
    4. Filtrar arestas
    5. Menu interativo (usuário existente ou novo)
    6. Gerar e exibir recomendações (Vizinhos Diretos + RWR)
"""

# Importamos as funções de leitura que estão em src/utils.py
from src.utils import carregar_artigos, carregar_usuarios, carregar_interacoes, carregar_citacoes

# Importamos as funções dos módulos dos colegas
from src.grafo import construir_grafo_bipartido
from src.projecao import construir_projecao, filtrar_arestas


def pipeline(interacoes, limiar=0.1):
    """
    Executa o pipeline de construção do grafo e projeção.

    Parâmetros:
        interacoes: lista de tuplas (usuario_id, artigo_id)
        limiar: peso mínimo para manter uma aresta na projeção (default 0.1)

    Retorna:
        grafo: grafo bipartido usuário-artigo
        projecao_filtrada: projeção artigo-artigo com arestas filtradas
    """
    # Passo 2 do pipeline: constrói grafo bipartido a partir das interações
    grafo = construir_grafo_bipartido(interacoes)

    # Passo 3 do pipeline: projeção artigo-artigo usando similaridade de Jaccard
    projecao = construir_projecao(grafo)

    # Passo 4 do pipeline: remove arestas com peso abaixo do limiar
    projecao_filtrada = filtrar_arestas(projecao, limiar)

    return grafo, projecao_filtrada


# Este bloco só executa quando você roda "python main.py" diretamente
if __name__ == "__main__":

    # Passo 1 do pipeline: cada função lê um CSV e retorna uma estrutura de dados
    artigos = carregar_artigos("data/artigos.csv")          # dict com 30 artigos
    usuarios = carregar_usuarios("data/usuarios.csv")       # dict com 15 usuários
    interacoes = carregar_interacoes("data/interacoes.csv")  # lista de tuplas
    citacoes = carregar_citacoes("data/citacoes.csv")        # lista de tuplas

    # Passos 2, 3 e 4 do pipeline: grafo → projeção → filtragem
    grafo, projecao_filtrada = pipeline(interacoes)

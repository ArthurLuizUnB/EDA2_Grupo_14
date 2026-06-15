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

# Este bloco só executa quando você roda "python main.py" diretamente
if __name__ == "__main__":

    # Cada função lê um CSV e retorna uma estrutura de dados
    artigos = carregar_artigos("data/artigos.csv")          # dict com 30 artigos
    usuarios = carregar_usuarios("data/usuarios.csv")       # dict com 15 usuários
    interacoes = carregar_interacoes("data/interacoes.csv")  # lista de tuplas
    citacoes = carregar_citacoes("data/citacoes.csv")        # lista de tuplas

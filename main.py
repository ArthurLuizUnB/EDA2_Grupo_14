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

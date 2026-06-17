"""
grafo.py — Construção e manipulação do grafo bipartido usuário-artigo.
Estrutura de dados: Hash Map (dict) + Conjuntos (set).
"""

import utils

    #Carregando os dados
interacoes = utils.carregar_interacoes("caminho/para/interacoes.csv")

    #Inicializando dicionários nativos vazios
grafo_usuarios = {}
grafo_artigos = {}

    #Construindo as arestas
for usuario_id, artigo_id in interacoes:

    # Grafo de Usuários
    # Se o usuário ainda não está no dicionário, cria a chave com um set vazio
    if usuario_id not in grafo_usuarios:
        grafo_usuarios[usuario_id] = set()

    # Adiciona o artigo ao set do usuário
    grafo_usuarios[usuario_id].add(artigo_id)

    # Grafo de Artigos (Opcional)
    # Mesma lógica estrutural para o caminho reverso
    if artigo_id not in grafo_artigos:
        grafo_artigos[artigo_id] = set()

    grafo_artigos[artigo_id].add(usuario_id)

print(f"O usuário U01 interagiu com os artigos: {grafo_usuarios['U01']}")
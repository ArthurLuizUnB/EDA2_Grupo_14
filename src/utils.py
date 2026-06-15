"""
utils.py — Leitura e carregamento dos dados do sistema de recomendação.
Estrutura de dados: Dicionários (Hash Map) para acesso O(1) por ID.
"""

import csv


def carregar_artigos(caminho: str) -> dict:
    """
    Carrega o catálogo de artigos do CSV.

    Retorna:
        dict {id: {titulo, area, ano, resumo}}
    """
    artigos = {}
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            artigos[row['id']] = {
                'titulo': row['titulo'],
                'area': row['area'],
                'ano': row['ano'],
                'resumo': row['resumo'],
            }
    return artigos


def carregar_usuarios(caminho: str) -> dict:
    """
    Carrega o cadastro de usuários do CSV.

    Retorna:
        dict {id: {nome, area_principal}}
    """
    usuarios = {}
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            usuarios[row['id']] = {
                'nome': row['nome'],
                'area_principal': row['area_principal'],
            }
    return usuarios


def carregar_interacoes(caminho: str) -> list:
    """
    Carrega o histórico de interações do CSV.

    Retorna:
        lista de tuplas [(usuario_id, artigo_id), ...]
    """
    interacoes = []
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            interacoes.append((row['usuario_id'], row['artigo_id']))
    return interacoes


def carregar_citacoes(caminho: str) -> list:
    """
    Carrega as citações entre artigos do CSV.

    Retorna:
        lista de tuplas [(artigo_origem, artigo_destino), ...]
    """
    citacoes = []
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            citacoes.append((row['artigo_origem'], row['artigo_destino']))
    return citacoes

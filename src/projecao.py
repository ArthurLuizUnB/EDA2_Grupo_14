"""
projecao.py — Projeção artigo-artigo com similaridade de Jaccard + filtragem por limiar.
Estrutura de dados: Hash Map de Hash Maps (dict[str, dict[str, float]]) com pesos float.
"""

from src.GrafoBipartido import GrafoBipartido
from itertools import combinations


class ProjecaoArtigo:

    def __init__(self, grafo: GrafoBipartido, threshold: float = 0.10):
        """
        Constrói e filtra automaticamente o grafo de projeção artigo-artigo.

        Parâmetros:
            grafo     (GrafoBipartido): instância carregada com as interações.
            threshold (float): limiar mínimo de Jaccard para manter uma aresta. Default = 0.10.
        """
        self._threshold = threshold
        self._projecao  = self._construir(grafo)
        self._filtrar()

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS PRIVADOS
    # ──────────────────────────────────────────────────────────────────────────

    def _construir(self, grafo: GrafoBipartido) -> dict:
        """
        Percorre cada usuário e enumera os pares de artigos que ele leu com
        itertools.combinations, garantindo que só calculamos Jaccard para pares
        com ao menos um usuário em comum. Armazena em ambas as direções
        (grafo não-dirigido).

        Retorna:
            dict[str, dict[str, float]]: projecao[Ti][Tj] = J(Ti, Tj)
        """
        projecao = {}
        pares_candidatos = set()

        for usuario_id, artigos in grafo._grafo_usuarios.items():
            artigos_lista = sorted(artigos)
            for ti, tj in combinations(artigos_lista, 2):
                pares_candidatos.add((ti, tj))

        for ti, tj in pares_candidatos:
            jaccard = self._jaccard(grafo, ti, tj)
            if jaccard > 0.0:
                projecao.setdefault(ti, {})[tj] = jaccard
                projecao.setdefault(tj, {})[ti] = jaccard

        return projecao

    def _jaccard(self, grafo: GrafoBipartido, artigo_a: str, artigo_b: str) -> float:
        """
        Calcula a Similaridade de Jaccard entre dois artigos.

            J(A, B) = |U(A) ∩ U(B)| / |U(A) ∪ U(B)|

        Retorna:
            float: valor entre 0.0 e 1.0. Retorna 0.0 se a união for vazia.
        """
        usuarios_a = grafo.obter_usuarios_do_artigo(artigo_a)
        usuarios_b = grafo.obter_usuarios_do_artigo(artigo_b)

        intersecao = len(usuarios_a & usuarios_b)
        uniao      = len(usuarios_a | usuarios_b)

        if uniao == 0:
            return 0.0

        return intersecao / uniao

    def _filtrar(self) -> None:
        """
        Remove in-place todas as arestas com Jaccard abaixo do threshold.
        Artigos que ficam sem nenhum vizinho válido são removidos do grafo.
        """
        artigos_para_remover = []

        for artigo in self._projecao:
            self._projecao[artigo] = {
                vizinho: peso
                for vizinho, peso in self._projecao[artigo].items()
                if peso >= self._threshold
            }
            if not self._projecao[artigo]:
                artigos_para_remover.append(artigo)

        for artigo in artigos_para_remover:
            del self._projecao[artigo]

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS PÚBLICOS
    # ──────────────────────────────────────────────────────────────────────────

    def obter_vizinhos(self, artigo_id: str) -> dict:
        """
        Retorna o dicionário de vizinhos de um artigo com seus pesos Jaccard.

        Parâmetros:
            artigo_id (str): ID do artigo de consulta.

        Retorna:
            dict[str, float]: {artigo_vizinho: jaccard}. Vazio se não encontrado.
        """
        return self._projecao.get(artigo_id, {})

    def obter_vizinhos_ordenados(self, artigo_id: str) -> list:
        """
        Retorna os vizinhos de um artigo ordenados do mais ao menos similar.

        Parâmetros:
            artigo_id (str): ID do artigo de consulta.

        Retorna:
            list[tuple[str, float]]: pares (artigo_id, jaccard) em ordem decrescente.
        """
        return sorted(self.obter_vizinhos(artigo_id).items(), key=lambda par: par[1], reverse=True)

    def exibir_resumo(self) -> None:
        """
        Imprime estatísticas gerais do grafo projetado e os 5 pares mais similares.
        """
        total_nos     = len(self._projecao)
        total_arestas = sum(len(v) for v in self._projecao.values()) // 2
        grau_medio    = (
            sum(len(v) for v in self._projecao.values()) / total_nos
            if total_nos > 0 else 0
        )

        print("=" * 56)
        print("       RESUMO DA PROJEÇÃO ARTIGO-ARTIGO (Jaccard)")
        print("=" * 56)
        print(f"  Limiar (threshold)  : {self._threshold:.2f}")
        print(f"  Nós (artigos)       : {total_nos}")
        print(f"  Arestas             : {total_arestas}")
        print(f"  Grau médio          : {grau_medio:.2f}")

        todas_arestas = [
            (ti, tj, peso)
            for ti, vizinhos in self._projecao.items()
            for tj, peso in vizinhos.items()
            if ti < tj
        ]
        todas_arestas.sort(key=lambda x: x[2], reverse=True)

        print("\n  Top 5 pares mais similares:")
        for ti, tj, peso in todas_arestas[:5]:
            print(f"    {ti} ↔ {tj}  →  Jaccard = {peso:.4f}")
        print("=" * 56)

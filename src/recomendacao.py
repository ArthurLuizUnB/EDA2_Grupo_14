"""
recomendacao.py - Recomendação por vizinhos mais próximos.
"""


class HeapMinimoTopN:
    """
    Heap mínimo limitado a N itens no formato:
    (score, desempate, artigo_id, detalhes).
    """

    def __init__(self, capacidade):
        self._capacidade = capacidade
        self._dados = []

    def _prioridade_menor(self, item_a, item_b):
        if item_a[0] != item_b[0]:
            return item_a[0] < item_b[0]
        if item_a[1] != item_b[1]:
            return item_a[1] < item_b[1]
        return item_a[2] > item_b[2]

    def _prioridade_maior(self, item_a, item_b):
        if item_a[0] != item_b[0]:
            return item_a[0] > item_b[0]
        if item_a[1] != item_b[1]:
            return item_a[1] > item_b[1]
        return item_a[2] < item_b[2]

    def _subir(self, indice):
        while indice > 0:
            pai = (indice - 1) // 2
            if not self._prioridade_menor(self._dados[indice], self._dados[pai]):
                break
            self._dados[indice], self._dados[pai] = self._dados[pai], self._dados[indice]
            indice = pai

    def _descer(self, indice):
        tamanho = len(self._dados)
        while True:
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2
            menor = indice

            if esquerda < tamanho and self._prioridade_menor(self._dados[esquerda], self._dados[menor]):
                menor = esquerda
            if direita < tamanho and self._prioridade_menor(self._dados[direita], self._dados[menor]):
                menor = direita

            if menor == indice:
                break

            self._dados[indice], self._dados[menor] = self._dados[menor], self._dados[indice]
            indice = menor

    def inserir(self, item):
        if self._capacidade <= 0:
            return

        if len(self._dados) < self._capacidade:
            self._dados.append(item)
            self._subir(len(self._dados) - 1)
            return

        if self._prioridade_maior(item, self._dados[0]):
            self._dados[0] = item
            self._descer(0)

    def em_ordem_decrescente(self):
        itens = self._dados[:]
        self._ordenar_por_selecao(itens)
        return itens

    def _ordenar_por_selecao(self, itens):
        for i in range(len(itens)):
            maior = i
            for j in range(i + 1, len(itens)):
                if self._prioridade_maior(itens[j], itens[maior]):
                    maior = j
            if maior != i:
                itens[i], itens[maior] = itens[maior], itens[i]


class RecomendadorVizinhos:
    """
    Recomenda artigos a partir dos vizinhos diretos da projeção artigo-artigo.
    """

    def __init__(self, grafo_bipartido, projecao_artigos, catalogo_artigos):
        self._grafo_bipartido = grafo_bipartido
        self._projecao = projecao_artigos
        self._catalogo = catalogo_artigos

    def recomendar_para_usuario(self, usuario_id, quantidade=5):
        artigos_base = self._grafo_bipartido.obter_artigos_do_usuario(usuario_id)
        return self.recomendar_por_artigos(artigos_base, quantidade)

    def recomendar_por_artigos(self, artigos_base, quantidade=5):
        lidos = set(artigos_base)
        candidatos = {}

        for artigo_base in lidos:
            vizinhos = self._projecao.obter_vizinhos(artigo_base)
            for artigo_vizinho, peso in vizinhos.items():
                if artigo_vizinho in lidos:
                    continue

                if artigo_vizinho not in candidatos:
                    candidatos[artigo_vizinho] = {
                        "score": 0.0,
                        "conexoes": 0,
                        "maior_peso": 0.0,
                        "origens": [],
                    }

                candidatos[artigo_vizinho]["score"] += peso
                candidatos[artigo_vizinho]["conexoes"] += 1
                candidatos[artigo_vizinho]["origens"].append((artigo_base, peso))
                if peso > candidatos[artigo_vizinho]["maior_peso"]:
                    candidatos[artigo_vizinho]["maior_peso"] = peso

        heap = HeapMinimoTopN(quantidade)
        for artigo_id, dados in candidatos.items():
            item = (
                dados["score"],
                dados["conexoes"],
                artigo_id,
                dados,
            )
            heap.inserir(item)

        recomendacoes = []
        for score, conexoes, artigo_id, dados in heap.em_ordem_decrescente():
            metadados = self._catalogo.get(artigo_id, {})
            recomendacoes.append({
                "artigo_id": artigo_id,
                "titulo": metadados.get("titulo", "Título indisponível"),
                "area": metadados.get("area", "Área indisponível"),
                "ano": metadados.get("ano", "Ano indisponível"),
                "score": score,
                "conexoes": conexoes,
                "maior_peso": dados["maior_peso"],
                "origens": self._ordenar_origens(dados["origens"]),
            })

        return recomendacoes

    def _ordenar_origens(self, origens):
        ordenadas = origens[:]
        for i in range(len(ordenadas)):
            maior = i
            for j in range(i + 1, len(ordenadas)):
                if ordenadas[j][1] > ordenadas[maior][1]:
                    maior = j
                elif ordenadas[j][1] == ordenadas[maior][1] and ordenadas[j][0] < ordenadas[maior][0]:
                    maior = j
            if maior != i:
                ordenadas[i], ordenadas[maior] = ordenadas[maior], ordenadas[i]
        return ordenadas


def imprimir_recomendacoes(recomendacoes):
    if not recomendacoes:
        print("Nenhuma recomendação encontrada com os vizinhos diretos atuais.")
        return

    print("\n=== Recomendações por vizinhos mais próximos ===")
    for posicao, rec in enumerate(recomendacoes, start=1):
        print(
            f"{posicao}. {rec['artigo_id']} - {rec['titulo']} "
            f"({rec['area']}, {rec['ano']})"
        )
        print(
            f"   score={rec['score']:.4f} | conexões={rec['conexoes']} "
            f"| maior similaridade={rec['maior_peso']:.4f}"
        )
        explicacao = ", ".join(
            f"{origem} ({peso:.4f})" for origem, peso in rec["origens"]
        )
        print(f"   recomendado por proximidade com: {explicacao}")

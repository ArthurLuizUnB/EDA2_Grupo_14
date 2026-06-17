class GrafoBipartido:
    def __init__(self):

        self._grafo_usuarios = {}
        self._grafo_artigos = {}

    def adicionar_interacao(self, usuario_id, artigo_id):

        #Adiciona uma única aresta ao grafo bipartido.

        self._grafo_usuarios.setdefault(usuario_id, set()).add(artigo_id)
        self._grafo_artigos.setdefault(artigo_id, set()).add(usuario_id)

    def carregar_interacoes(self, interacoes):

        #Popula o grafo iterando sobre uma lista de tuplas (usuario_id, artigo_id).

        for usuario, artigo in interacoes:
            self.adicionar_interacao(usuario, artigo)

    def obter_artigos_do_usuario(self, usuario_id):
        """
        Retorna o conjunto de artigos com os quais o usuário interagiu.
        Usa o .get() para retornar um set vazio caso o usuário não exista,
        evitando o erro de KeyError.
        """
        return self._grafo_usuarios.get(usuario_id, set())

    def obter_usuarios_do_artigo(self, artigo_id):

        #Retorna o conjunto de usuários que interagiram com o artigo.

        return self._grafo_artigos.get(artigo_id, set())

    def exibir_resumo(self):
        #Método utilitário para checar o tamanho do grafo.
        print(f"Total de Usuários mapeados: {len(self._grafo_usuarios)}")
        print(f"Total de Artigos mapeados: {len(self._grafo_artigos)}")

    def imprimir_lista_adjacencia(self):
        """
        Imprime a lista de adjacência completa do grafo, mostrando
        as conexões de Usuários -> Artigos e de Artigos -> Usuários.
        """
        print("=== Lista de Adjacência: Usuários -> Artigos ===")
        if not self._grafo_usuarios:
            print("  Nenhum usuário registrado.")
        else:
            #Itera sobre o dicionário pegando a chave (usuario) e o valor (set de artigos)
            for usuario, artigos in self._grafo_usuarios.items():
                #O join com sorted apenas deixa a exibição mais bonita e em ordem alfabética
                artigos_formatados = ", ".join(sorted(artigos))
                print(f"  [{usuario}] salvou: {artigos_formatados}")

        print("\n=== Lista de Adjacência: Artigos -> Usuários ===")
        if not self._grafo_artigos:
            print("  Nenhum artigo registrado.")
        else:
            #Itera sobre o dicionário pegando a chave (artigo) e o valor (set de usuarios)
            for artigo, usuarios in self._grafo_artigos.items():
                usuarios_formatados = ", ".join(sorted(usuarios))
                print(f"  [{artigo}] foi salvo por: {usuarios_formatados}")
        print("================================================\n")

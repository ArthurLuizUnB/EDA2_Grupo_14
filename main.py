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

from src.utils import carregar_artigos, carregar_usuarios, carregar_interacoes, carregar_citacoes
from src.GrafoBipartido import GrafoBipartido
from src.projecao import ProjecaoArtigo
from src.recomendacao import recomendar_vizinhos_diretos, recomendar_rwr


def pipeline(interacoes, limiar=0.1):
    # Passo 2: constrói o grafo bipartido usuário-artigo
    grafo = GrafoBipartido()
    grafo.carregar_interacoes(interacoes)

    # Passos 3 e 4: calcula similaridade de Jaccard entre artigos e filtra pelo limiar
    projecao_filtrada = ProjecaoArtigo(grafo, threshold=limiar)

    return grafo, projecao_filtrada


def menu(grafo, projecao_filtrada, usuarios: dict, artigos: dict):
    """Passo 5: coleta informações do usuário para gerar as recomendações."""

    print("\n" + "=" * 56)
    print("   SISTEMA DE RECOMENDAÇÃO DE ARTIGOS ACADÊMICOS")
    print("=" * 56)
    print("\n[1] Sou um usuário existente")
    print("[2] Sou um usuário novo")
    print("[0] Sair")

    # input() lê o que o usuário digitou; .strip() remove espaços acidentais nas bordas
    opcao = input("\nEscolha uma opção: ").strip()

    if opcao == "0":
        print("Encerrando o sistema. Até logo!")
        return

    elif opcao == "1":
        # Itera sobre o dicionário de usuários exibindo ID, nome e área
        print("\nUsuários cadastrados:")
        for uid, dados in usuarios.items():
            print(f"  {uid} — {dados['nome']} ({dados['area_principal']})")  # f-string formata texto com variáveis

        # .upper() garante que 'u01' e 'U01' sejam tratados igual
        usuario_id = input("\nDigite seu ID de usuário: ").strip().upper()

        # Verifica se o ID digitado existe no dicionário de usuários
        if usuario_id not in usuarios:
            print(f"\n⚠ Usuário '{usuario_id}' não encontrado.")
            return

        # Consulta o grafo bipartido: retorna o set de artigos que o usuário já leu
        artigos_lidos = grafo.obter_artigos_do_usuario(usuario_id)

        print(f"\nOlá, {usuarios[usuario_id]['nome']}!")
        print(f"Você leu {len(artigos_lidos)} artigo(s):")

        # sorted() ordena os IDs dos artigos alfabeticamente para exibir em ordem
        for aid in sorted(artigos_lidos):
            # .get() busca o título; se não encontrar, usa o próprio ID como fallback
            titulo = artigos.get(aid, {}).get('titulo', aid)
            print(f"  [{aid}] {titulo}")

        # Passo 6: gera e exibe as recomendações com base nos artigos lidos
        recomendar_vizinhos_diretos(projecao_filtrada, artigos_lidos, artigos)
        recomendar_rwr(projecao_filtrada, artigos_lidos, artigos)

    elif opcao == "2":
        # set comprehension: extrai as áreas únicas de todos os artigos (sem repetição)
        # sorted() organiza as áreas em ordem alfabética
        areas_disponiveis = sorted({dados['area'] for dados in artigos.values()})

        # enumerate() gera o índice numérico automaticamente, começando em 1
        print("\nÁreas disponíveis:")
        for i, area in enumerate(areas_disponiveis, start=1):
            print(f"  [{i}] {area}")

        escolha = input("\nDigite o número da sua área de interesse: ").strip()

        # try/except protege contra entrada inválida (ex: letra no lugar de número)
        try:
            # int() converte a string digitada para número; -1 ajusta para índice base 0
            area_escolhida = areas_disponiveis[int(escolha) - 1]
        except (ValueError, IndexError):
            print("⚠ Opção inválida.")
            return

        # list comprehension: filtra apenas os artigos que pertencem à área escolhida
        artigos_da_area = [
            (aid, dados) for aid, dados in artigos.items()
            if dados['area'] == area_escolhida
        ]

        print(f"\nArtigos disponíveis em '{area_escolhida}':")
        for aid, dados in artigos_da_area:
            print(f"  [{aid}] {dados['titulo']} ({dados['ano']})")

        # Passo 6: gera e exibe as recomendações com base na área escolhida
        recomendar_vizinhos_diretos(projecao_filtrada, {aid for aid, _ in artigos_da_area}, artigos)
        recomendar_rwr(projecao_filtrada, {aid for aid, _ in artigos_da_area}, artigos)

    else:
        print("⚠ Opção inválida.")


if __name__ == "__main__":

    # Passo 1: carrega os dados dos CSVs
    artigos    = carregar_artigos("data/artigos.csv")
    usuarios   = carregar_usuarios("data/usuarios.csv")
    interacoes = carregar_interacoes("data/interacoes.csv")
    citacoes   = carregar_citacoes("data/citacoes.csv")

    # Passos 2, 3 e 4: grafo → projeção → filtragem
    grafo, projecao_filtrada = pipeline(interacoes)

    # Passo 5: menu interativo
    menu(grafo, projecao_filtrada, usuarios, artigos)

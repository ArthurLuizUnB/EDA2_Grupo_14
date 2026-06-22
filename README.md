# Sistema de Recomendação de Artigos Acadêmicos - EDA2_Grupo_14

> Trabalho de Estrutura de Dados 2 — Grafos  
> Linguagem: Python | Dataset: Fictício | Algoritmos: Jaccard 

---

## Estrutura do Projeto

```
recomendacao-artigos/
│
├── data/
│   ├── artigos.csv       # 30 artigos de CC/Engenharia de Software
│   ├── usuarios.csv      # 15 usuários com área de interesse
│   └── interacoes.csv    # Histórico: quem salvou qual artigo
│  
├── src/
│   ├── utils.py          # Leitura dos CSVs → dicionários (Hash Map)
│   ├── grafo.py          # Grafo bipartido usuário-artigo (dict + set)
│   ├── projecao.py       # Projeção artigo-artigo via Jaccard
│   └── recomendacao.py   # Vizinhos Diretos 
│
├── main.py               # Menu interativo e pipeline completo
└── README.md
```

---

## Como Executar

```bash
# Na raiz do projeto
python main.py
```

Não há dependências externas — apenas a biblioteca padrão do Python.

---
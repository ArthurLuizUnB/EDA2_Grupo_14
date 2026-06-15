# Sistema de Recomendação de Artigos Acadêmicos - EDA2_Grupo_14

> Trabalho de Estrutura de Dados 2 — Grafos  
> Linguagem: Python | Dataset: Fictício | Algoritmos: Jaccard + RWR

---

## Estrutura do Projeto

```
recomendacao-artigos/
│
├── data/
│   ├── artigos.csv       # 30 artigos de CC/Engenharia de Software
│   ├── usuarios.csv      # 15 usuários com área de interesse
│   ├── interacoes.csv    # Histórico: quem salvou qual artigo
│   └── citacoes.csv      # Citações entre artigos
│
├── src/
│   ├── utils.py          # Leitura dos CSVs → dicionários (Hash Map)
│   ├── grafo.py          # Grafo bipartido usuário-artigo (dict + set)
│   ├── projecao.py       # Projeção artigo-artigo via Jaccard
│   └── recomendacao.py   # Vizinhos Diretos + Random Walk with Restarts
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

## Modelagem do Grafo

### Grafo Bipartido (G)



### Projeção Artigo-Artigo (G')


---

## Algoritmos de Recomendação


---

## Estruturas de Dados

---

## Dataset Fictício

- **30 artigos** das áreas: Aprendizado de Máquina, Engenharia de Software, Sistemas Distribuídos, PLN, Grafos, Visão Computacional, Sistemas de Recomendação, Algoritmos e Segurança.
- **15 usuários** com perfis de área definidos.
- **~75 interações** distribuídas de forma coerente com o perfil de cada usuário.
- **~55 citações** entre artigos respeitando relações temáticas reais.

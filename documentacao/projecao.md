# Projeção Artigo-Artigo — Jaccard + Filtragem

> Documentação técnica do módulo `src/projecao.py`  
> EDA2 — Grupo 14 | Temática B: Sistema de Recomendação de Artigos Acadêmicos

---

## Por que precisamos de uma projeção?

O `GrafoBipartido` captura com precisão **quem interagiu com o quê**: usuários de um lado, artigos do outro, e arestas representando as interações. Mas para recomendar artigos, precisamos responder uma pergunta diferente:

> *"Dado que o usuário leu o artigo A, quais outros artigos são apreciados pelo mesmo tipo de público?"*

Para isso, precisamos de um grafo **artigo–artigo**, onde cada aresta representa a **semelhança de audiência** entre dois artigos. O processo de "colapsar" um dos lados do grafo bipartido para gerar um grafo unipartido chama-se **projeção**.

```
Grafo Bipartido                 Projeção Artigo-Artigo
───────────────                 ──────────────────────

U1 ──── T01                          T01
U1 ──── T03      ──────►            / | \
U2 ──── T03                       T03  T06  T13
U2 ──── T06                        \       /
U1 ──── T13                         T13──T06
```

A aresta entre T01 e T03 existe porque **pelo menos um usuário** leu ambos. O **peso** dessa aresta quantifica o quão fortemente os dois artigos são co-consumidos.

---

## Similaridade de Jaccard

### Definição

Para dois artigos A e B, sendo U(A) e U(B) os conjuntos de usuários que interagiram com cada um:

$$J(A, B) = \frac{|U(A) \cap U(B)|}{|U(A) \cup U(B)|}$$

| Valor        | Significado                                     |
|--------------|-------------------------------------------------|
| J = 1.0      | Exatamente os mesmos usuários leram A e B       |
| J = 0.5      | Metade da audiência combinada é compartilhada   |
| J = 0.0      | Nenhum usuário em comum                         |

A métrica é **simétrica** — J(A, B) = J(B, A) — portanto o grafo projetado é **não-dirigido**.

### Por que Jaccard e não contagem bruta?

A alternativa mais simples seria contar diretamente o número de usuários em comum: |U(A) ∩ U(B)|. O problema é que essa contagem **favorece artigos muito populares**.

**Exemplo concreto com os dados do projeto:**

- T01 tem 5 usuários, T30 tem 2 usuários, e eles compartilham 2 → contagem bruta = 2  
- T25 tem 3 usuários, T29 tem 3 usuários, e eles compartilham 3 → contagem bruta = 3

Pela contagem bruta, T25–T29 pareceria mais forte que T01–T30, mas na realidade T25 e T29 têm **exatamente** os mesmos leitores (Jaccard = 1.0), enquanto T01 e T30 têm apenas uma sobreposição parcial. O Jaccard captura isso corretamente ao normalizar pela união.

### Exemplo passo a passo

Dados do projeto — interações de T01 e T03:

```
U(T01) = {U01, U04, U05, U09, U13}   → 5 usuários
U(T03) = {U01, U04, U09, U13}         → 4 usuários  (U13 também leu T03)

Interseção = {U01, U04, U09, U13}     → 4 usuários em comum
União       = {U01, U04, U05, U09, U13} → 5 usuários no total

J(T01, T03) = 4 / 5 = 0.80
```

Resultado: T01 e T03 têm similaridade de 80% — são artigos lidos quase pelo mesmo público.

---

## Algoritmo de construção

### Abordagem ingênua vs. abordagem adotada

A abordagem ingênua testaria todos os pares de artigos: **O(|A|²)**. Com 30 artigos, isso são 435 pares — mas a maioria não teria nenhum usuário em comum, tornando o cálculo de Jaccard desnecessário.

A abordagem adotada percorre cada usuário e enumera apenas os pares de artigos que ele leu, usando `itertools.combinations`. Isso garante que **só calculamos Jaccard para pares que já sabemos ter ao menos um usuário em comum**.

```
Usuário U01 leu: [T01, T03, T05, T06, T13, T18, T26]
Pares gerados:   (T01,T03), (T01,T05), (T01,T06), (T03,T05), ...
                 → todos esses pares têm U01 em comum ✓
```

### Pseudocódigo

```
pares_candidatos ← conjunto vazio

para cada usuário u:
    artigos_u ← lista ordenada dos artigos de u
    para cada par (Ti, Tj) em combinations(artigos_u, 2):
        adicionar (Ti, Tj) ao conjunto de candidatos

para cada (Ti, Tj) em pares_candidatos:
    j ← |U(Ti) ∩ U(Tj)| / |U(Ti) ∪ U(Tj)|
    se j > 0:
        projecao[Ti][Tj] ← j
        projecao[Tj][Ti] ← j   ← grafo não-dirigido: inserimos nos dois sentidos
```

### Complexidade

| Etapa                      | Complexidade                          |
|----------------------------|---------------------------------------|
| Gerar pares candidatos     | O(\|U\| × d²), d = grau médio usuário |
| Calcular Jaccard por par   | O(min(\|U(Ti)\|, \|U(Tj)\|))          |
| Total                      | O(\|U\| × d² + \|pares\| × d_max)     |

Na prática, muito inferior a O(|A|²) para grafos esparsos como o do projeto.

---

## Estrutura de dados

O grafo projetado é armazenado como um **Hash Map de Hash Maps**:

```python
dict[str, dict[str, float]]

{
  "T01": {"T03": 0.80, "T06": 0.80, "T13": 0.50, "T18": 0.50, ...},
  "T03": {"T01": 0.80, "T06": 0.67, "T13": 0.67, ...},
  ...
}
```

| Operação                     | Custo         |
|------------------------------|---------------|
| Acesso à aresta (Ti, Tj)     | O(1) amortizado |
| Listar vizinhos de Ti        | O(grau(Ti))   |
| Inserção de nova aresta      | O(1) amortizado |
| Espaço total                 | O(\|E'\|), onde \|E'\| = nº de arestas da projeção |

A escolha de `dict` em vez de matriz N×N é justificada pela mesma razão que a lista de adjacência no grafo bipartido: **o grafo projetado também é esparso**. Mesmo com 30 artigos (435 pares possíveis), os dados do projeto geram apenas 92 arestas antes da filtragem — menos de 22% da densidade máxima.

---

## Filtragem por limiar (threshold)

### Motivação

Sem filtragem, qualquer par de artigos com ao menos 1 usuário em comum gera uma aresta — inclusive pares com Jaccard = 0.05, que representam co-ocorrências quase acidentais. Essas arestas fracas introduzem **ruído nas recomendações** e aumentam o custo dos algoritmos que consomem o grafo projetado.

### Efeito da filtragem

```
Antes (threshold = 0.0):             Depois (threshold = 0.30):

T01 ──0.80── T03                     T01 ──0.80── T03
T01 ──0.17── T30       ──────►       T01 ──0.80── T06
T01 ──0.80── T06                     T01 ──0.50── T13
T01 ──0.11── T04                     T01 ──0.50── T18
T01 ──0.50── T13                     T01 ──0.40── T26
...                                  (T30 e T04 removidas por peso < 0.30)
```

### Escolha do threshold

| Threshold | Comportamento                                                   |
|-----------|-----------------------------------------------------------------|
| 0.0       | Nenhuma filtragem; grafo denso com muito ruído                  |
| 0.10      | Conservador; remove apenas coincidências muito fracas (padrão) |
| 0.30      | Moderado; mantém apenas sobreposições de público relevantes     |
| 0.50      | Restritivo; só pares com maioria de audiência compartilhada     |

O threshold padrão de **0.10** foi escolhido como ponto de partida adequado para o tamanho do dataset (15 usuários, 30 artigos), preservando todas as relações com algum grau de consistência sem cortar informação relevante.

---

## Funções do módulo

| Função                      | Descrição                                                         |
|-----------------------------|-------------------------------------------------------------------|
| `construir_projecao(grafo)` | Gera o grafo projetado completo (sem filtro)                      |
| `_jaccard(grafo, a, b)`     | Calcula J(a, b) — função interna, prefixo `_` indica uso privado |
| `filtrar_projecao(p, thr)`  | Retorna novo grafo apenas com arestas ≥ threshold                 |
| `obter_vizinhos_ordenados(p, id)` | Lista vizinhos de um artigo por Jaccard decrescente         |
| `exibir_resumo_projecao(p)` | Imprime estatísticas e top-5 pares mais similares                 |

---

## Resultados com o dataset do projeto

Rodando com `threshold = 0.10`:

```
Nós (artigos) : 29
Arestas       : 92
Grau médio    : 6.34

Top 5 pares mais similares:
  T10 ↔ T14  →  Jaccard = 1.0000
  T10 ↔ T17  →  Jaccard = 1.0000
  T10 ↔ T23  →  Jaccard = 1.0000
  T25 ↔ T29  →  Jaccard = 1.0000
  T20 ↔ T29  →  Jaccard = 1.0000
```

Os pares com Jaccard = 1.0 são artigos lidos **exatamente** pelos mesmos usuários, o que faz sentido temático: T10, T14, T17 e T23 são todos de Engenharia de Software, e T20, T25 e T29 são todos de Sistemas Distribuídos.

---

## Integração com o restante do pipeline

```
utils.py                  GrafoBipartido.py          projecao.py
─────────                 ─────────────────          ───────────
carregar_interacoes()  →  carregar_interacoes()  →   construir_projecao()
                                                  →   filtrar_projecao()
                                                         │
                                                         ▼
                                                   recomendacao.py
                                                   (Vizinhos Diretos + RWR)
```

O grafo projetado e filtrado é a entrada direta de `recomendacao.py`. Cada aresta com peso J(Ti, Tj) representa a força da relação entre os dois artigos, que os algoritmos de recomendação usarão para propagar a relevância a partir dos artigos já lidos pelo usuário.

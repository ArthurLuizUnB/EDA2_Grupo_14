# Análise dos Resultados

## Visão geral do dataset

O dataset utilizado no projeto possui:

- 30 artigos cadastrados.
- 15 usuários.
- 78 interações usuário-artigo.
- 12 áreas temáticas diferentes.

Dos 30 artigos, 29 aparecem em pelo menos uma interação. O único artigo sem interação é o T19, da área de Inteligência Artificial. Por não possuir leitores associados, ele não entra na projeção artigo-artigo e não participa das recomendações baseadas em vizinhos.

## Resultado da projeção artigo-artigo

Com threshold igual a 0,10, a projeção artigo-artigo gerou:

- 29 nós.
- 92 arestas.
- Grau médio de 6,34.

Isso indica que o grafo projetado não ficou nem totalmente desconectado nem excessivamente denso. O threshold remove relações muito fracas, mas ainda preserva conexões suficientes para gerar recomendações para todos os usuários cadastrados.

## Pares com maior similaridade

Os pares mais fortes encontrados possuem Jaccard igual a 1,0. Isso significa que os dois artigos de cada par foram lidos exatamente pelo mesmo conjunto de usuários.

Exemplos:

| Par de artigos | Áreas | Jaccard |
|---|---|---:|
| T02 - T12 | Sistemas Distribuídos / Sistemas Distribuídos | 1,0000 |
| T03 - T06 | Aprendizado de Máquina / Processamento de Linguagem Natural | 1,0000 |
| T09 - T10 | Engenharia de Software / Engenharia de Software | 1,0000 |
| T09 - T14 | Engenharia de Software / Engenharia de Software | 1,0000 |
| T10 - T17 | Engenharia de Software / Engenharia de Software | 1,0000 |

Esses resultados mostram que o grafo conseguiu capturar agrupamentos coerentes. Artigos de Engenharia de Software, por exemplo, aparecem fortemente conectados porque foram consumidos pelo mesmo perfil de usuários. O par T03-T06 também é relevante, pois aproxima Aprendizado de Máquina e PLN, duas áreas naturalmente relacionadas no dataset.

## Componentes conectados

A projeção filtrada resultou em dois componentes conectados:

- Componente 1: 16 artigos.
- Componente 2: 13 artigos.

O maior componente agrupa principalmente artigos de Aprendizado de Máquina, PLN, Grafos, Sistemas de Recomendação, Visão Computacional e Recuperação de Informação. Isso acontece porque muitos usuários desses perfis compartilham artigos relacionados a modelos, redes, busca, grafos e recomendação.

O segundo componente reúne principalmente Engenharia de Software, Sistemas Distribuídos e Segurança Computacional. A separação indica que esses temas tiveram padrões de leitura mais internos, com pouca sobreposição de usuários em relação ao primeiro grupo.

Essa divisão é um resultado importante: ela mostra que a estrutura do grafo reflete comunidades temáticas formadas a partir do comportamento dos usuários.

## Recomendações para usuários existentes

O sistema gerou recomendações para todos os 15 usuários cadastrados. A média foi de 4,2 recomendações por usuário, considerando um máximo de 5.

### Exemplo 1: usuário U01

O usuário U01 possui histórico concentrado em Aprendizado de Máquina, PLN e Visão Computacional. As principais recomendações foram:

| Artigo recomendado | Área | Score | Conexões |
|---|---|---:|---:|
| T30 | Visão Computacional | 1,5333 | 4 |
| T22 | Processamento de Linguagem Natural | 1,3000 | 4 |
| T04 | Recuperação de Informação | 0,3611 | 3 |

A recomendação T30 faz sentido porque está conectada a quatro artigos já lidos pelo usuário, incluindo T05, T18, T13 e T01. Isso indica proximidade com o histórico de redes neurais, aprendizado profundo e visão computacional.

A recomendação T22 também é coerente, pois aparece ligada a artigos como T03, T06, T01 e T13. Como T06 é um artigo de PLN baseado em Transformers, a presença de T22 reforça a transição natural para representações vetoriais de palavras.

### Exemplo 2: usuário U04

O usuário U04 tem perfil de Processamento de Linguagem Natural. As principais recomendações foram:

| Artigo recomendado | Área | Score | Conexões |
|---|---|---:|---:|
| T26 | Aprendizado de Máquina | 1,9000 | 4 |
| T18 | Aprendizado de Máquina | 1,7667 | 4 |
| T05 | Visão Computacional | 1,0667 | 4 |

Esse resultado mostra que usuários de PLN recebem recomendações próximas de Aprendizado de Máquina. Isso é esperado no dataset, porque artigos de PLN como T06 e T22 compartilham leitores com artigos sobre modelos, transferência de aprendizado e redes neurais.

### Exemplo 3: usuário U08

O usuário U08 tem perfil de Engenharia de Software. A principal recomendação foi:

| Artigo recomendado | Área | Score | Conexões |
|---|---|---:|---:|
| T27 | Engenharia de Software | 2,5000 | 5 |

O artigo T27 foi recomendado com score alto porque está conectado a vários artigos já lidos pelo usuário dentro da mesma área. Esse é um exemplo de recomendação conservadora: o sistema permanece dentro da comunidade temática do usuário.

## Recomendações para usuários novos

Para usuários novos, o sistema parte de uma área de interesse escolhida. Nesse caso, os artigos daquela área são usados como base e o recomendador busca vizinhos na projeção.

Exemplos:

| Área escolhida | Recomendações principais |
|---|---|
| Processamento de Linguagem Natural | T03, T01, T13 |
| Grafos e Redes | T28, T04, T08 |
| Sistemas Distribuídos | T21, T24 |
| Sistemas de Recomendação | T16, T11, T04 |
| Visão Computacional | T18, T13, T01 |

Esses resultados mostram que o sistema consegue recomendar artigos de áreas próximas, não apenas da mesma área escolhida. Por exemplo, ao escolher PLN, aparecem artigos de Aprendizado de Máquina, indicando que os padrões de leitura aproximam essas duas áreas.

## Limitações observadas

O principal limite do sistema é que a recomendação depende das interações cadastradas. Artigos sem interação, como T19, ficam isolados e não podem ser recomendados pela estratégia atual.

Outra limitação é o problema de partida fria. Para usuários novos, o sistema precisa usar uma área de interesse como aproximação inicial, porque ainda não existe histórico individual de leitura.

Também é importante destacar que a similaridade atual é baseada em co-leitura. O texto dos resumos e títulos está presente no dataset, mas não é usado diretamente no cálculo da recomendação. Portanto, a interpretação dos resultados deve ser apresentada como recomendação baseada no comportamento dos usuários no grafo.

## Conclusão

Os resultados indicam que a modelagem por grafos conseguiu capturar relações coerentes entre artigos e áreas. A projeção artigo-artigo formou comunidades temáticas, os pares com maior Jaccard representam artigos consumidos pelo mesmo público, e o recomendador gerou resultados explicáveis por meio dos artigos de origem e dos pesos das conexões.

O uso de vizinhos diretos torna a recomendação simples de interpretar: cada artigo recomendado pode ser justificado pelas ligações com artigos já lidos ou escolhidos como base. Isso facilita a análise dos resultados e torna o sistema adequado para uma apresentação acadêmica sobre grafos aplicados à recomendação de artigos.

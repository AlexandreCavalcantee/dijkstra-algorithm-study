# Algoritmo de Dijkstra — Estudo e Análise Empírica

Trabalho da disciplina de **Análise e Projeto de Algoritmos** (Engenharia de Software).
Implementa o algoritmo de Dijkstra do zero — incluindo a fila de prioridade (min-heap binário indexado) e a estrutura de grafo — e compara empiricamente duas variantes:

- **Versão com heap** — complexidade `O((V + E) log V)`
- **Versão naive (varredura linear)** — complexidade `O(V²)`

O projeto produz os artefatos necessários para o artigo acadêmico (gráficos, CSVs, grade de passos) e um notebook Jupyter usado na apresentação ao vivo.

---

## Índice
1. [Estrutura do projeto](#estrutura-do-projeto)
2. [Requisitos](#requisitos)
3. [Instalação](#instalação)
4. [Como rodar](#como-rodar)
5. [Apresentação ao vivo](#apresentação-ao-vivo)
6. [Resultados](#resultados-do-benchmark)
7. [Resumo da implementação](#resumo-da-implementação)

---

## Estrutura do projeto

```
dijkstra-algorithm-study/
├── src/                              # implementação principal
│   ├── min_heap.py                   # min-heap binário indexado (do zero)
│   ├── graph.py                      # grafo via lista de adjacência
│   ├── dijkstra.py                   # versão com heap — O((V+E) log V)
│   ├── dijkstra_naive.py             # versão naive — O(V²)
│   ├── dijkstra_traced.py            # versão geradora (emite cada passo)
│   └── visualization.py              # renderização matplotlib
│
├── tests/                            # 34 testes pytest
│   ├── test_min_heap.py              # testes do heap (12)
│   ├── test_graph.py                 # testes do grafo (8)
│   └── test_dijkstra.py              # testes de Dijkstra (14)
│
├── benchmarks/                       # análise empírica e renderização
│   ├── graph_generator.py            # geradores de grafos aleatórios
│   ├── complexity_analysis.py        # mede tempo, salva CSV + plots
│   └── render_visualization.py       # gera GIF e grade de passos
│
├── notebooks/
│   ├── apresentacao.ipynb            # notebook usado na apresentação
│   └── build_notebook.py             # script que monta o notebook
│
├── results/                          # artefatos gerados (commit-ados)
│   ├── sparse.csv, dense.csv         # tempos por tamanho
│   ├── sparse_linear.png             # tempo vs V (esparso)
│   ├── sparse_loglog.png             # log-log com slope (esparso)
│   ├── dense_linear.png              # tempo vs V (denso)
│   ├── dense_loglog.png              # log-log com slope (denso)
│   ├── dijkstra_animation.gif        # animação passo-a-passo
│   └── dijkstra_steps.png            # grade com todos os passos
│
├── conftest.py                       # adiciona raiz ao sys.path para o pytest
└── README.md
```

---

## Requisitos
- Python 3.10 ou superior (testado em 3.14)
- `pip` e `venv`

Bibliotecas usadas (apenas para auxiliares, não para o algoritmo):
- `pytest` — testes
- `matplotlib`, `numpy` — gráficos do benchmark
- `pillow` — gravação do GIF
- `jupyter`, `nbformat`, `ipykernel` — notebook

> O **algoritmo e a fila de prioridade** são implementados do zero. Bibliotecas externas servem apenas para teste, gráfico e exibição.

---

## Instalação

```bash
git clone https://github.com/AlexandreCavalcantee/dijkstra-algorithm-study.git
cd dijkstra-algorithm-study

python3 -m venv .venv
source .venv/bin/activate

pip install pytest matplotlib numpy pillow jupyter ipykernel nbformat
```

> Toda a documentação a seguir assume a venv ativa. Se preferir não ativar, rode os comandos via `.venv/bin/python ...` e `.venv/bin/pytest ...`.

---

## Como rodar

### 1. Testes

Roda os 34 testes (heap, grafo, Dijkstra):

```bash
pytest -v
```

Saída esperada: `34 passed in 0.05s`.

### 2. Benchmark empírico

Compara a versão com heap contra a naive em grafos esparsos e densos. Salva CSV e gráficos em `results/`.

```bash
python benchmarks/complexity_analysis.py
```

Saída no terminal: tabela com tempo médio (ms) e speedup para cada tamanho, mais o expoente empírico estimado por regressão log-log.

Tempo de execução: ~1-2 minutos (depende do hardware).

### 3. Visualização (GIF + grade de passos)

Gera o GIF animado e a imagem com todos os passos lado-a-lado:

```bash
python benchmarks/render_visualization.py
```

Produz `results/dijkstra_animation.gif` e `results/dijkstra_steps.png`.

### 4. Reconstruir o notebook

Caso queira regenerar o `apresentacao.ipynb` a partir do script:

```bash
python notebooks/build_notebook.py
jupyter nbconvert --to notebook --execute notebooks/apresentacao.ipynb \
    --output apresentacao.ipynb --ExecutePreprocessor.timeout=120
```

---

## Apresentação ao vivo

Abrir o notebook:

```bash
jupyter notebook notebooks/apresentacao.ipynb
```

O notebook tem 23 células organizadas em 7 seções:

| Seção | Conteúdo |
|-------|----------|
| 1 | Construção do grafo de demonstração |
| 2 | Legenda de cores |
| 3 | Passo-a-passo (chame `show_next()` para avançar) |
| 4 | Animação completa (GIF) |
| 5 | Resultado final — distâncias e caminhos |
| 6 | Verificação cruzada (heap × naive) |
| 7 | Análise empírica com plots log-log |

**Dica para a apresentação:** rode todas as células antes (já está executado no commit), depois clique célula por célula no momento certo. Se quiser refazer um passo, reinicie do bloco `steps = dijkstra_trace(graph, 'A')`.

---

## Resultados do benchmark

### Grafo esparso (`E ≈ 3V`)

| V | Heap (ms) | Naive (ms) | Speedup |
|--:|----------:|-----------:|--------:|
| 100  | 0.30  | 0.45   | 1.5×  |
| 200  | 0.63  | 1.58   | 2.5×  |
| 400  | 1.59  | 6.00   | 3.8×  |
| 800  | 3.65  | 24.0   | 6.6×  |
| 1600 | 7.96  | 97.6   | 12.3× |
| 3200 | 18.1  | 400.4  | **22.2×** |

Expoente empírico (log-log fit): heap ≈ **1.19** (≈ V log V), naive ≈ **1.97** (≈ V²) — confirma a teoria.

### Grafo denso (`p = 0.5`)

| V | Heap (ms) | Naive (ms) | Speedup |
|--:|----------:|-----------:|--------:|
| 50  | 0.19  | 0.17   | **0.89× — naive vence** |
| 100 | 0.50  | 0.56   | 1.1× |
| 200 | 1.42  | 2.11   | 1.5× |
| 400 | 5.25  | 8.65   | 1.7× |
| 800 | 20.1  | 35.5   | 1.8× |

Em grafos densos `E ≈ V²`, a versão com heap vira `O(V² log V)` enquanto a naive permanece `O(V²)` — a vantagem assintótica desaparece.

**Insight para o artigo:** não existe algoritmo universalmente melhor. A densidade do grafo determina a escolha — heap para grafos esparsos (ex.: malhas viárias), naive ou matriz para grafos densos.

---

## Resumo da implementação

### Min-heap binário indexado (`src/min_heap.py`)
- Lista interna armazena pares `(prioridade, item)`.
- Dicionário `_position` mapeia `item → índice` no heap, permitindo `decrease_key` em **O(log n)**.
- Operações: `push`, `pop`, `peek`, `decrease_key`, `contains`, `is_empty`.
- A travessia para cima/para baixo (`_sift_up`, `_sift_down`) atualiza o `_position` a cada troca para manter o invariante.

### Grafo (`src/graph.py`)
- Lista de adjacência (`dict[vertex, list[(neighbor, weight)]]`).
- Suporta direcionado e não-direcionado (uma única flag).
- Rejeita pesos negativos (pré-condição do Dijkstra).

### Dijkstra com heap (`src/dijkstra.py`)
1. Inicializa `distances[v] = ∞`, `distances[source] = 0`.
2. Insere todos os vértices no heap com suas distâncias.
3. Enquanto o heap não está vazio, extrai o mínimo `u`.
4. Para cada vizinho `v` de `u`, tenta relaxar a aresta: se `dist[u] + w(u,v) < dist[v]`, atualiza e chama `decrease_key`.
5. Para no momento em que o mínimo é `∞` (vértices restantes inalcançáveis).

Complexidade: `V` extrações × `O(log V)` + `E` relaxamentos × `O(log V)` = **`O((V + E) log V)`**.

### Dijkstra naive (`src/dijkstra_naive.py`)
Mesma lógica, mas a cada iteração varre todos os vértices não-visitados para encontrar o mínimo (em vez de usar heap).
Complexidade: **`O(V²)`**.

### Versão traceada (`src/dijkstra_traced.py`)
Idêntica à versão com heap, mas usa `yield` para emitir um snapshot a cada evento (`init`, `extract`, `relax`, `done`). É a base da visualização passo-a-passo.

---

## Licença
Trabalho acadêmico — Engenharia de Software, Análise e Projeto de Algoritmos.

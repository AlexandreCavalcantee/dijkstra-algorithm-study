import sys
from pathlib import Path

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "apresentacao.ipynb"


def markdown(text):
    return nbf.v4.new_markdown_cell(text)


def code(text):
    return nbf.v4.new_code_cell(text)


def build():
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        markdown(
            "# Algoritmo de Dijkstra — Caminhos Mínimos\n"
            "**Análise e Projeto de Algoritmos**\n\n"
            "Demonstração passo-a-passo com implementação própria de:\n"
            "- Min-heap binário indexado (`src/min_heap.py`)\n"
            "- Estrutura de grafo via lista de adjacência (`src/graph.py`)\n"
            "- Dijkstra com heap O((V + E) log V) (`src/dijkstra.py`)\n"
        ),
        code(
            "import sys\n"
            "from pathlib import Path\n"
            "\n"
            "sys.path.insert(0, str(Path.cwd().parent))\n"
            "\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "from src.graph import Graph\n"
            "from src.dijkstra import dijkstra, shortest_path\n"
            "from src.dijkstra_traced import dijkstra_trace\n"
            "from src.visualization import render_step, render_legend, animate_dijkstra\n"
        ),
        markdown(
            "## 1. Construindo o grafo\n"
            "Grafo não-direcionado com 5 vértices e 6 arestas. "
            "Origem **A**, destino qualquer vértice alcançável.\n"
        ),
        code(
            "graph = Graph(directed=False)\n"
            "graph.add_edge('A', 'B', 4)\n"
            "graph.add_edge('A', 'C', 1)\n"
            "graph.add_edge('C', 'B', 2)\n"
            "graph.add_edge('B', 'D', 1)\n"
            "graph.add_edge('C', 'D', 5)\n"
            "graph.add_edge('D', 'E', 3)\n"
            "\n"
            "positions = {\n"
            "    'A': (0.0, 1.0),\n"
            "    'B': (-1.0, 0.2),\n"
            "    'C': (1.0, 0.2),\n"
            "    'D': (-0.6, -1.0),\n"
            "    'E': (0.8, -1.0),\n"
            "}\n"
            "\n"
            "print(f'V = {graph.vertex_count()}, E = {graph.edge_count()}')\n"
        ),
        markdown(
            "## 2. Legenda de cores\n"
            "Útil para acompanhar a animação.\n"
        ),
        code(
            "figure, axis = plt.subplots(figsize=(7, 3))\n"
            "render_legend(axis)\n"
            "plt.show()\n"
        ),
        markdown(
            "## 3. Passo-a-passo\n"
            "Cada chamada a `next(steps)` avança o algoritmo em um evento: "
            "inicialização, extract-min, ou relaxamento de uma aresta.\n"
        ),
        code(
            "steps = dijkstra_trace(graph, 'A')\n"
            "\n"
            "def show_next():\n"
            "    state = next(steps)\n"
            "    figure, axis = plt.subplots(figsize=(7, 6))\n"
            "    render_step(graph, positions, state, 'A', axis)\n"
            "    plt.show()\n"
            "    return state\n"
            "\n"
            "show_next();\n"
        ),
        markdown("Avance célula por célula durante a apresentação:\n"),
        code("show_next();\n"),
        code("show_next();\n"),
        code("show_next();\n"),
        code("show_next();\n"),
        code("show_next();\n"),
        markdown(
            "## 4. Animação completa\n"
            "Útil para revisar a execução no fim da apresentação.\n"
        ),
        code(
            "from IPython.display import Image\n"
            "\n"
            "Image(filename='../results/dijkstra_animation.gif')\n"
        ),
        markdown(
            "## 5. Resultado final\n"
            "Distâncias mínimas e caminhos reconstruídos a partir de A.\n"
        ),
        code(
            "distances, predecessors = dijkstra(graph, 'A')\n"
            "for vertex in sorted(distances):\n"
            "    path, cost = shortest_path(graph, 'A', vertex)\n"
            "    pretty_path = ' → '.join(path) if path else '(inalcançável)'\n"
            "    print(f'A → {vertex}:  distância = {cost}    caminho = {pretty_path}')\n"
        ),
        markdown(
            "## 6. Verificação cruzada\n"
            "Versão naive O(V²) deve produzir o mesmo resultado.\n"
        ),
        code(
            "from src.dijkstra_naive import dijkstra_naive\n"
            "\n"
            "naive_distances, _ = dijkstra_naive(graph, 'A')\n"
            "assert naive_distances == distances\n"
            "print('OK — heap e naive concordam.')\n"
        ),
        markdown(
            "## 7. Análise empírica\n"
            "Resultados do `benchmarks/complexity_analysis.py`:\n"
            "\n"
            "**Grafo esparso (E ≈ 3V):** speedup do heap cresce de 1.5× (V=100) "
            "para 22× (V=3200) — confirma O((V+E) log V) vs O(V²).\n"
            "\n"
            "**Grafo denso (p=0.5):** speedup pequeno (1-1.8×). Em V=50 a versão "
            "naive até vence — em grafos densos E ≈ V², o overhead do heap deixa "
            "de compensar.\n"
            "\n"
            "**Conclusão:** densidade do grafo determina a escolha. Heap para grafos "
            "esparsos (ex. malhas viárias), naive ou matriz para densos.\n"
        ),
        code(
            "from IPython.display import Image\n"
            "Image(filename='../results/sparse_loglog.png')\n"
        ),
        code("Image(filename='../results/dense_loglog.png')\n"),
    ]

    notebook.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }

    NOTEBOOK_PATH.parent.mkdir(exist_ok=True)
    nbf.write(notebook, NOTEBOOK_PATH)
    print(f"Notebook escrito em {NOTEBOOK_PATH}")


if __name__ == "__main__":
    build()

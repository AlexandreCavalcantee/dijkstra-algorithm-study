import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.graph import Graph
from src.visualization import animate_dijkstra, save_step_grid

RESULTS_DIR = PROJECT_ROOT / "results"


def build_demo_graph():
    graph = Graph(directed=False)
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "B", 2)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "D", 5)
    graph.add_edge("D", "E", 3)
    return graph


DEMO_POSITIONS = {
    "A": (0.0, 1.0),
    "B": (-1.0, 0.2),
    "C": (1.0, 0.2),
    "D": (-0.6, -1.0),
    "E": (0.8, -1.0),
}


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    graph = build_demo_graph()

    gif_path = RESULTS_DIR / "dijkstra_animation.gif"
    grid_path = RESULTS_DIR / "dijkstra_steps.png"

    frames = animate_dijkstra(graph, "A", DEMO_POSITIONS, gif_path, interval_ms=1100)
    print(f"GIF salvo em {gif_path}  ({frames} frames)")

    saved = save_step_grid(graph, "A", DEMO_POSITIONS, grid_path, columns=3)
    print(f"Grid salvo em {grid_path}  ({saved} passos)")


if __name__ == "__main__":
    main()

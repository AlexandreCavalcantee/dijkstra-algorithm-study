import math

import matplotlib.pyplot as plt

INFINITY = float("inf")

COLOR_SOURCE = "#27ae60"
COLOR_CURRENT = "#f39c12"
COLOR_VISITED = "#2980b9"
COLOR_UNVISITED = "#95a5a6"
COLOR_EDGE_DEFAULT = "#d5d8dc"
COLOR_EDGE_TREE = "#1f2d3d"
COLOR_EDGE_RELAXED = "#27ae60"
COLOR_EDGE_REJECTED = "#c0392b"


def circular_layout(vertices, radius=1.0):
    ordered = list(vertices)
    n = len(ordered)
    return {
        vertex: (
            radius * math.cos(2 * math.pi * i / n - math.pi / 2),
            radius * math.sin(2 * math.pi * i / n - math.pi / 2),
        )
        for i, vertex in enumerate(ordered)
    }


def _vertex_color(vertex, source, state):
    if state["event"] != "init" and vertex == state["current"]:
        return COLOR_CURRENT
    if vertex == source:
        return COLOR_SOURCE
    if vertex in state["visited"]:
        return COLOR_VISITED
    return COLOR_UNVISITED


def _format_distance(distance):
    if distance == INFINITY:
        return "∞"
    if isinstance(distance, float) and distance.is_integer():
        return str(int(distance))
    return str(distance)


def _title_for(state):
    event = state["event"]
    if event == "init":
        return "Inicialização — todas as distâncias são ∞ exceto a origem"
    if event == "extract":
        current = state["current"]
        distance = _format_distance(state["distances"][current])
        return f"Extract-min: vértice {current} (d = {distance})"
    if event == "relax":
        source, target, weight = state["edge"]
        verdict = "relaxa" if state["relaxed"] else "rejeita"
        return f"Relaxa aresta {source} → {target} (w = {weight}): {verdict}"
    if event == "done":
        return "Concluído — árvore de caminhos mínimos completa"
    return event


def _iter_unique_edges(graph):
    seen = set()
    for vertex in graph.vertices():
        for neighbor, weight in graph.neighbors(vertex):
            if graph.directed:
                key = (vertex, neighbor)
            else:
                key = (min(vertex, neighbor), max(vertex, neighbor))
            if key in seen:
                continue
            seen.add(key)
            yield vertex, neighbor, weight


def render_step(graph, positions, state, source, ax):
    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")

    predecessors = state["predecessors"]
    edge_event = state["edge"]
    relaxed = state["relaxed"]

    for u, v, weight in _iter_unique_edges(graph):
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        in_tree = predecessors.get(v) == u or predecessors.get(u) == v
        color = COLOR_EDGE_DEFAULT
        width = 1.3
        if in_tree:
            color = COLOR_EDGE_TREE
            width = 2.6

        if edge_event is not None:
            es, et, _ = edge_event
            if (es, et) == (u, v) or (es, et) == (v, u):
                color = COLOR_EDGE_RELAXED if relaxed else COLOR_EDGE_REJECTED
                width = 3.5

        ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, zorder=1)

        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(
            mx,
            my,
            str(weight),
            fontsize=10,
            ha="center",
            va="center",
            zorder=2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#bbbbbb"),
        )

    for vertex in graph.vertices():
        x, y = positions[vertex]
        color = _vertex_color(vertex, source, state)
        ax.scatter(
            x,
            y,
            s=1100,
            c=color,
            zorder=3,
            edgecolors="black",
            linewidths=1.5,
        )
        ax.text(
            x,
            y,
            str(vertex),
            fontsize=13,
            fontweight="bold",
            ha="center",
            va="center",
            color="white",
            zorder=4,
        )
        distance_label = _format_distance(state["distances"][vertex])
        ax.text(
            x,
            y - 0.18,
            f"d = {distance_label}",
            fontsize=10,
            ha="center",
            va="top",
            zorder=4,
        )

    ax.set_title(_title_for(state), fontsize=12)
    ax.margins(0.25)


def render_legend(ax):
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_SOURCE, markersize=12, label="Origem"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_CURRENT, markersize=12, label="Sendo processado"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_VISITED, markersize=12, label="Finalizado"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_UNVISITED, markersize=12, label="Não visitado"),
        plt.Line2D([0], [0], color=COLOR_EDGE_TREE, linewidth=2.6, label="Árvore de caminhos mínimos"),
        plt.Line2D([0], [0], color=COLOR_EDGE_RELAXED, linewidth=3.5, label="Aresta relaxada"),
        plt.Line2D([0], [0], color=COLOR_EDGE_REJECTED, linewidth=3.5, label="Aresta rejeitada"),
    ]
    ax.legend(handles=handles, loc="center", frameon=False, fontsize=10)
    ax.axis("off")


def animate_dijkstra(graph, source, positions, output_path, interval_ms=900):
    from matplotlib.animation import FuncAnimation, PillowWriter

    from src.dijkstra_traced import dijkstra_trace

    states = list(dijkstra_trace(graph, source))
    figure, ax = plt.subplots(figsize=(8, 7))

    def update(frame_index):
        render_step(graph, positions, states[frame_index], source, ax)
        return []

    animation = FuncAnimation(
        figure,
        update,
        frames=len(states),
        interval=interval_ms,
        repeat=False,
        blit=False,
    )
    writer = PillowWriter(fps=max(1, int(1000 / interval_ms)))
    animation.save(output_path, writer=writer)
    plt.close(figure)
    return len(states)


def save_step_grid(graph, source, positions, output_path, columns=3):
    from src.dijkstra_traced import dijkstra_trace

    states = list(dijkstra_trace(graph, source))
    rows = math.ceil(len(states) / columns)
    figure, axes = plt.subplots(rows, columns, figsize=(columns * 5, rows * 4.5))
    axes = axes.flatten() if rows * columns > 1 else [axes]

    for index, state in enumerate(states):
        render_step(graph, positions, state, source, axes[index])
    for index in range(len(states), len(axes)):
        axes[index].axis("off")

    figure.tight_layout()
    figure.savefig(output_path, dpi=110)
    plt.close(figure)
    return len(states)

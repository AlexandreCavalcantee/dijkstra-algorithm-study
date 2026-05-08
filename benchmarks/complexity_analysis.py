import csv
import math
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.graph_generator import random_dense_graph, random_sparse_graph
from src.dijkstra import dijkstra
from src.dijkstra_naive import dijkstra_naive

RESULTS_DIR = PROJECT_ROOT / "results"
TRIALS = 5
SPARSE_SIZES = [100, 200, 400, 800, 1600, 3200]
SPARSE_AVERAGE_DEGREE = 6
DENSE_SIZES = [50, 100, 200, 400, 800]
DENSE_PROBABILITY = 0.5


def measure(algorithm, graph, source):
    start = time.perf_counter()
    algorithm(graph, source)
    return time.perf_counter() - start


def run_scenario(name, graph_factory, sizes):
    print(f"\n=== {name} ===")
    rows = []
    for size in sizes:
        heap_times = []
        naive_times = []
        for trial in range(TRIALS):
            graph = graph_factory(size, seed=size * 1000 + trial)
            source = next(iter(graph.vertices()))
            heap_times.append(measure(dijkstra, graph, source))
            naive_times.append(measure(dijkstra_naive, graph, source))
        edge_count = graph.edge_count()
        heap_median = statistics.median(heap_times)
        naive_median = statistics.median(naive_times)
        rows.append(
            {
                "vertices": size,
                "edges": edge_count,
                "heap_median": heap_median,
                "naive_median": naive_median,
                "heap_mean": statistics.mean(heap_times),
                "naive_mean": statistics.mean(naive_times),
                "heap_stdev": statistics.stdev(heap_times) if TRIALS > 1 else 0.0,
                "naive_stdev": statistics.stdev(naive_times) if TRIALS > 1 else 0.0,
            }
        )
        print(
            f"V={size:>5}  E={edge_count:>7}  "
            f"heap={heap_median*1000:>9.3f} ms  "
            f"naive={naive_median*1000:>9.3f} ms  "
            f"speedup={naive_median/heap_median:>6.2f}x"
        )
    return rows


def save_csv(rows, path):
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fit_loglog_exponent(sizes, times):
    log_sizes = np.log(sizes)
    log_times = np.log(times)
    slope, intercept = np.polyfit(log_sizes, log_times, 1)
    return slope, intercept


def plot_linear(rows, scenario, output_path):
    sizes = np.array([row["vertices"] for row in rows])
    edges = np.array([row["edges"] for row in rows])
    heap = np.array([row["heap_median"] for row in rows])
    naive = np.array([row["naive_median"] for row in rows])

    theoretical_heap = (sizes + edges) * np.log2(sizes)
    theoretical_naive = sizes ** 2
    theoretical_heap = theoretical_heap * (heap[-1] / theoretical_heap[-1])
    theoretical_naive = theoretical_naive * (naive[-1] / theoretical_naive[-1])

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(sizes, heap * 1000, marker="o", label="Heap O((V+E) log V)")
    axis.plot(sizes, naive * 1000, marker="s", label="Naive O(V²)")
    axis.plot(sizes, theoretical_heap * 1000, "--", alpha=0.5, label="Curva teórica heap")
    axis.plot(sizes, theoretical_naive * 1000, "--", alpha=0.5, label="Curva teórica naive")
    axis.set_xlabel("Número de vértices (V)")
    axis.set_ylabel("Tempo (ms)")
    axis.set_title(f"Dijkstra — {scenario} (escala linear)")
    axis.legend()
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_path, dpi=120)
    plt.close(figure)


def plot_loglog(rows, scenario, output_path):
    sizes = np.array([row["vertices"] for row in rows], dtype=float)
    heap = np.array([row["heap_median"] for row in rows])
    naive = np.array([row["naive_median"] for row in rows])

    heap_slope, _ = fit_loglog_exponent(sizes, heap)
    naive_slope, _ = fit_loglog_exponent(sizes, naive)

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.loglog(sizes, heap, marker="o", label=f"Heap (slope={heap_slope:.2f})")
    axis.loglog(sizes, naive, marker="s", label=f"Naive (slope={naive_slope:.2f})")
    axis.set_xlabel("Número de vértices (V) — log")
    axis.set_ylabel("Tempo (s) — log")
    axis.set_title(f"Dijkstra — {scenario} (log-log)")
    axis.legend()
    axis.grid(True, which="both", alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_path, dpi=120)
    plt.close(figure)
    return heap_slope, naive_slope


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    sparse_rows = run_scenario(
        "Esparso (E ≈ 3V)",
        lambda size, seed: random_sparse_graph(size, SPARSE_AVERAGE_DEGREE, seed=seed),
        SPARSE_SIZES,
    )
    dense_rows = run_scenario(
        "Denso (p = 0.5)",
        lambda size, seed: random_dense_graph(size, DENSE_PROBABILITY, seed=seed),
        DENSE_SIZES,
    )

    save_csv(sparse_rows, RESULTS_DIR / "sparse.csv")
    save_csv(dense_rows, RESULTS_DIR / "dense.csv")

    plot_linear(sparse_rows, "grafo esparso", RESULTS_DIR / "sparse_linear.png")
    plot_linear(dense_rows, "grafo denso", RESULTS_DIR / "dense_linear.png")

    sparse_slopes = plot_loglog(sparse_rows, "grafo esparso", RESULTS_DIR / "sparse_loglog.png")
    dense_slopes = plot_loglog(dense_rows, "grafo denso", RESULTS_DIR / "dense_loglog.png")

    print("\n=== Expoentes empíricos (log-log fit) ===")
    print(f"Esparso  heap={sparse_slopes[0]:.2f}  naive={sparse_slopes[1]:.2f}")
    print(f"Denso    heap={dense_slopes[0]:.2f}  naive={dense_slopes[1]:.2f}")
    print(f"\nResultados em {RESULTS_DIR}")


if __name__ == "__main__":
    main()

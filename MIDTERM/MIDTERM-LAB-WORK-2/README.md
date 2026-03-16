# Cavite Transportation Network Analyzer

A Python program that models, visualizes, and analyzes a road network across eight municipalities in Cavite, Philippines. It builds an interactive graph map and computes the shortest path between any two locations using Dijkstra's algorithm.

---

## Project Overview

The program has two core functions:

- **Node Map Generation** — Displays the transportation network as an undirected graph, where each municipality is a node and each road connection is an edge. Every edge is labeled with its Distance (km), Travel Time (min), and Fuel consumption (L).
- **Shortest Path Computation** — Given a starting location, a destination, and a chosen optimization metric, the program calculates the most efficient route using Dijkstra's algorithm and visually highlights it on the graph with directional arrows.

---

## Approach

- **Graph Modeling with NetworkX** — The network is built as an `nx.Graph` (undirected). Each edge stores three attributes: `distance`, `time`, and `fuel`. Duplicate directional entries in the dataset (e.g., `BACOOR → SILANG` and `SILANG → BACOOR`) are detected and merged into a single undirected edge.
- **Visualization with Matplotlib** — The graph is rendered in an interactive Matplotlib window. Normal edges are drawn in a neutral gray/purple color. When a shortest path is found, its edges are redrawn in red with `FancyArrowPatch` directional arrowheads, simulating a directed route on an otherwise undirected graph.
- **Fixed Node Layout** — Node positions are defined manually in a plain Python dictionary (see [Node Positions](#node-positions) below). This dictionary is computed once at startup and reused on every redraw, so the layout never shifts between searches.
- **Number-Based Node Selection** — Instead of typing location names, users select nodes by entering a number (1–8). The program maps each number to the corresponding municipality name internally.
- **Metric Selection** — Users choose which attribute to optimize: Distance, Time, or Fuel. The selected attribute is passed directly to Dijkstra's algorithm as the edge weight.

---

## Algorithm Used

Shortest paths are computed using **Dijkstra's algorithm**, accessed via NetworkX's built-in `nx.dijkstra_path()` function. The algorithm finds the path with the lowest cumulative weight across the chosen metric. After the path is found, the program also accumulates the totals for all three metrics (distance, time, and fuel) regardless of which one was optimized, so a complete summary is always displayed.

---

## Challenges Faced

### Messy Automatic Layout

Initially, node positions were generated automatically using NetworkX's `spring_layout()` with a fixed random seed. While this kept the layout consistent between runs, the result was visually cluttered — nodes ended up packed together, edge labels overlapped, and the graph was difficult to read at a glance.

### Solution: Manual Position Dictionary

The automatic layout was replaced with a manually defined dictionary of `(x, y)` coordinates for each node. This gave full control over where each node appears on the canvas, making it possible to:

- Space nodes far enough apart so edge labels don't collide
- Roughly mirror the real-world geography of Cavite (north up, east right)
- Group related municipalities into readable clusters

The dictionary is defined in the `get_node_positions()` function and is called exactly once at startup. The same object is passed into `draw_graph()` on every redraw, so positions are permanently fixed for the lifetime of the program.

---

## Outcome / Results

- **Clean, Fixed Layout** — The graph displays in a stable, readable arrangement that never changes between searches. Each node is clearly separated, and edge labels are consistently legible.
- **Dynamic Path Highlighting** — After each search, the shortest path edges are redrawn in red with triangular directional arrowheads indicating travel direction. Path nodes are also highlighted in red. All other edges remain in their neutral color.
- **Detailed Console Summary** — Results are printed to the terminal in a formatted block that includes the full node sequence, total distance, total travel time, and total fuel consumption.
- **In-Window Annotation** — The same path summary (start node, destination, and optimization metric) is displayed as a text box directly inside the graph window, updating dynamically with every new search.
- **Input Validation** — All user input is validated gracefully. The program handles empty input, out-of-range numbers, invalid metric selections, and selecting the same node as both start and destination.

---

## Node Positions

To adjust the graph layout, edit the `get_node_positions()` function in `transportation_network.py`. Each entry maps a node name to an `(x, y)` coordinate:

```python
pos = {
    "NOVELETA": (3.0, 8.0),
    "IMUS":     (4.5, 8.0),
    "BACOOR":   (5.5, 6.5),
    "DASMA":    (5.5, 3.5),
    "SILANG":   (2.0, 3.5),
    "GENTRI":   (2.0, 6.5),
    "KAWIT":    (4.5, 0.5),
    "INDANG":   (3.0, 0.5),
}
```

Change any `(x, y)` value and re-run the program — no other changes are needed. A gap of roughly **1.5–2.0 units** between adjacent nodes keeps edge labels readable without overlapping.

---

## Requirements

```
pip install networkx matplotlib
```

## Usage

```
python MidtermLab2-GarciaLee.py
```

1. A graph window opens showing the full network.
2. Enter a starting location number (1–8).
3. Enter a destination location number (1–8).
4. Choose an optimization metric: Distance, Time, or Fuel.
5. The shortest path is highlighted on the graph and printed in the console.
6. Choose to run another search or exit.

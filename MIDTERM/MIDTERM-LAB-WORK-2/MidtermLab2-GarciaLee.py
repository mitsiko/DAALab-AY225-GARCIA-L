"""
Transportation Network Analyzer
=================================
Visualizes a transportation network and finds shortest paths
using Dijkstra's algorithm via NetworkX.

Locations: IMUS, BACOOR, DASMA, KAWIT, INDANG, SILANG, GENTRI, NOVELETA
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import sys

# ─────────────────────────────────────────────
# 1. GRAPH CONSTRUCTION
# ─────────────────────────────────────────────

def build_graph():
    """
    Build and return an undirected weighted graph from the dataset.
    Duplicate directional routes with identical attributes are merged
    into a single undirected edge.
    """

    # Raw dataset: (from, to, distance_km, time_min, fuel_liters)
    raw_edges = [
        ("IMUS",     "BACOOR",   10, 15, 1.2),
        ("BACOOR",   "DASMA",    12, 25, 1.5),
        ("DASMA",    "KAWIT",    12, 25, 1.5),
        ("KAWIT",    "INDANG",   12, 25, 1.2),
        ("INDANG",   "SILANG",   14, 25, 1.5),
        ("SILANG",   "GENTRI",   10, 25, 1.3),
        ("GENTRI",   "NOVELETA", 10, 25, 1.5),
        ("NOVELETA", "IMUS",     10, 15, 1.2),
        ("BACOOR",   "SILANG",   10, 25, 1.3),
        ("DASMA",    "SILANG",   12, 25, 1.5),
        ("SILANG",   "BACOOR",   10, 25, 1.3),   # duplicate of BACOOR→SILANG
        ("NOVELETA", "BACOOR",   10, 15, 1.2),   # duplicate of BACOOR→NOVELETA direction
        ("SILANG",   "KAWIT",    14, 25, 1.2),
        ("IMUS",     "NOVELETA", 10, 15, 1.2),   # duplicate of NOVELETA→IMUS
    ]

    G = nx.Graph()  # Undirected graph

    # Use a set to track already-added (frozenset) pairs
    seen_edges = {}

    for (u, v, dist, time, fuel) in raw_edges:
        key = frozenset([u, v])
        if key not in seen_edges:
            # New edge — add it
            G.add_edge(u, v, distance=dist, time=time, fuel=fuel)
            seen_edges[key] = (dist, time, fuel)
        else:
            # Edge already exists — only add if attributes differ
            existing = seen_edges[key]
            if existing != (dist, time, fuel):
                # Different attributes: add as a separate representation
                # For this dataset all duplicates have identical values,
                # so this branch will not trigger, but it is here for safety.
                pass  # keep the first occurrence

    return G


# ─────────────────────────────────────────────
# 2. FIXED NODE POSITIONS  ← edit these!
# ─────────────────────────────────────────────


def get_node_positions():
    """
    Return the manually defined position dictionary.

    Keys   : node names (must match the names used in build_graph())
    Values : (x, y) tuples — adjust freely to improve the visual layout

    This function is called exactly ONCE in main(), and the same
    dictionary is passed into draw_graph() every time the graph is
    redrawn, so node positions never shift between searches.
    """

    pos = {
        # ── Northern cluster (Imus corridor) ──────────────────────────
        # These three towns sit roughly along the northern edge of Cavite.
        # Noveleta is on the far left (west), Bacoor on the right (east).
        "NOVELETA": (3.0, 8.0),   # ← move left/right to spread the cluster
        "IMUS":     (4.5, 8.0),   # ← centre of the northern group
        "BACOOR":   (5.5, 6.5),   # ← eastern end of the northern cluster

        # ── Eastern side (Dasmariñas) ─────────────────────────────────
        # Dasma is south-east of Bacoor; give it enough x-distance from
        # Silang so their shared edge label is readable.
        "DASMA":    (5.5, 3.5),   # ← shift right to separate from Silang

        # ── Central hub (Silang) ──────────────────────────────────────
        # Silang connects to many nodes; keeping it near the centre of
        # the graph reduces edge crossings.
        "SILANG":   (2.0, 3.5),   # ← try (5,5) or (4,4) if labels clash

        # ── Western cluster ───────────────────────────────────────────
        # Gentri, Kawit and Indang run roughly north→south on the western
        # side.  Keeping them in a vertical column avoids overlap.
        "GENTRI":   (2.0, 6.5),   # ← adjust y to space them vertically
        "KAWIT":    (4.5, 0.5),   # ← same x as Gentri, lower y
        "INDANG":   (3.0, 0.5),   # ← furthest south on the western column
    }

    return pos


# ─────────────────────────────────────────────
# 3. GRAPH DRAWING
# ─────────────────────────────────────────────

def draw_graph(G, pos, path_edges=None, path_nodes=None,
               info_text="", ax=None):
    """
    Draw the transportation network.

    Parameters
    ----------
    G           : NetworkX graph
    pos         : fixed position dictionary
    path_edges  : list of (u, v) tuples for the highlighted shortest path
    path_nodes  : ordered list of nodes on the shortest path
    info_text   : annotation string displayed inside the figure
    ax          : Matplotlib Axes to draw on
    """

    if ax is None:
        ax = plt.gca()

    ax.clear()
    ax.set_facecolor("#d3ceca")          # dark navy background
    ax.figure.patch.set_facecolor("#d3ceca")

    path_edges = path_edges or []
    path_nodes = path_nodes or []

    # Separate normal edges from path edges for coloring
    path_edge_set = set(frozenset(e) for e in path_edges)
    normal_edges  = [e for e in G.edges() if frozenset(e) not in path_edge_set]

    # ── Draw normal (non-path) edges ──────────────────────────────────
    nx.draw_networkx_edges(
        G, pos,
        edgelist=normal_edges,
        edge_color="#2c333c",
        width=1,
        style="solid",
        ax=ax,
        arrows=False,
    )

    # ── Draw path edges (red, thicker) ───────────────────────────────
    if path_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color="#c75520",
            width=2,
            style="solid",
            ax=ax,
            arrows=False,
        )

        # Draw directional arrowheads on each path segment
        for (u, v) in path_edges:
            x1, y1 = pos[u]
            x2, y2 = pos[v]

            # Offset slightly so the arrowhead sits near the destination node
            dx = x2 - x1
            dy = y2 - y1

            arrow = FancyArrowPatch(
                posA=(x1 + dx * 0.25, y1 + dy * 0.25),
                posB=(x2 - dx * 0.15, y2 - dy * 0.15),
                arrowstyle="-|>",
                color="#c75520",
                lw=2,
                mutation_scale=18,
                zorder=5,
            )
            ax.add_patch(arrow)

    # ── Draw all nodes ────────────────────────────────────────────────
    normal_node_list = [n for n in G.nodes() if n not in path_nodes]
    path_node_list   = [n for n in path_nodes]

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=normal_node_list,
        node_color="#809b87",
        node_size=3500,
        edgecolors="#2c333c",
        linewidths=1,
        ax=ax,
    )

    if path_node_list:
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=path_node_list,
            node_color="#809b87",
            node_size=3500,
            edgecolors="#c75520",
            linewidths=2,
            ax=ax,
        )

    # ── Draw node labels ──────────────────────────────────────────────
    nx.draw_networkx_labels(
        G, pos,
        font_color="#2c333c",
        font_size=8,
        font_weight="bold",
        ax=ax,
    )

    # ── Edge labels: Distance, Time, Fuel ────────────────────────────
    edge_labels = {}
    for (u, v, data) in G.edges(data=True):
        label = (
            f"D:{data['distance']} km\n"
            f"T:{data['time']} min\n"
            f"F:{data['fuel']} L"
        )
        edge_labels[(u, v)] = label

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_color="#2c333c",
        font_size=6,
        bbox=dict(boxstyle="square,pad=0.5", fc="#d3ceca", ec="none", alpha=1),
        ax=ax,
    )

    # ── Info text box ─────────────────────────────────────────────────
    if info_text:
        ax.text(
            0.01, 1.03, info_text,
            transform=ax.transAxes,
            fontsize=7,
            verticalalignment="top",
            color="#d3ceca",
            bbox=dict(boxstyle="square,pad=1", fc="#c75520", ec="#c75520", alpha=1),
        )
    else:
        ax.text(
            0.01, 1.03,
            "Transportation Network\nCavite Province, Philippines",
            transform=ax.transAxes,
            fontsize=7,
            verticalalignment="top",
            color="#d3ceca",
            bbox=dict(boxstyle="square,pad=1", fc="#c75520", ec="#c75520", alpha=1),
        )

    ax.set_title(
        "CAVITE TRANSPORTATION NETWORK",
        color="#2c333c", fontsize=13, fontweight="bold", pad=12,
    )
    ax.axis("off")
    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)


# ─────────────────────────────────────────────
# 4. SHORTEST PATH
# ─────────────────────────────────────────────

def find_shortest_path(G, source, target, metric):
    """
    Find the shortest path using Dijkstra's algorithm.

    Parameters
    ----------
    G      : NetworkX graph
    source : starting node name
    target : destination node name
    metric : 'distance' | 'time' | 'fuel'

    Returns
    -------
    path        : ordered list of node names
    path_edges  : list of (u, v) edge tuples along the path
    totals      : dict with total distance, time, and fuel
    """

    try:
        path = nx.dijkstra_path(G, source, target, weight=metric)
    except nx.NetworkXNoPath:
        return None, None, None
    except nx.NodeNotFound as e:
        print(f"  [Error] Node not found: {e}")
        return None, None, None

    # Build the edge list in path direction
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    # Accumulate totals for all three metrics
    total_distance = 0.0
    total_time     = 0.0
    total_fuel     = 0.0

    for (u, v) in path_edges:
        data = G[u][v]
        total_distance += data["distance"]
        total_time     += data["time"]
        total_fuel     += data["fuel"]

    totals = {
        "distance": total_distance,
        "time":     total_time,
        "fuel":     total_fuel,
    }

    return path, path_edges, totals


# ─────────────────────────────────────────────
# 5. CONSOLE OUTPUT
# ─────────────────────────────────────────────

def print_results(path, totals, source, target, metric):
    """Print the shortest path results to the console."""

    metric_label = {"distance": "Distance", "time": "Time", "fuel": "Fuel"}[metric]

    print("\n" + "=" * 50)
    print(f"  Shortest Path from {source} to {target}")
    print(f"  Optimization Metric: {metric_label}")
    print("=" * 50)
    print("\n  Path:")
    print("  " + " → ".join(path))
    print(f"\n  Total Distance : {totals['distance']:.1f} km")
    print(f"  Total Time     : {totals['time']:.0f} minutes")
    print(f"  Total Fuel     : {totals['fuel']:.1f} liters")
    print("=" * 50 + "\n")


# ─────────────────────────────────────────────
# 6. INPUT HELPERS
# ─────────────────────────────────────────────

NODE_MAP = {
    1: "IMUS",
    2: "BACOOR",
    3: "DASMA",
    4: "KAWIT",
    5: "INDANG",
    6: "SILANG",
    7: "GENTRI",
    8: "NOVELETA",
}

METRIC_MAP = {
    1: "distance",
    2: "time",
    3: "fuel",
}


def display_node_menu():
    print("\n  Locations:")
    for num, name in NODE_MAP.items():
        print(f"    {num} - {name}")


def display_metric_menu():
    print("\n  Optimization Metric:")
    print("    1 - Distance")
    print("    2 - Time")
    print("    3 - Fuel")


def get_node_input(prompt):
    """Prompt the user for a valid node number and return the node name."""
    while True:
        raw = input(f"  {prompt}").strip()
        if not raw:
            print("  [!] Input cannot be empty. Please enter a number 1–8.")
            continue
        try:
            num = int(raw)
        except ValueError:
            print("  [!] Invalid input. Please enter a number between 1 and 8.")
            continue
        if num not in NODE_MAP:
            print("  [!] Number out of range. Please enter a number between 1 and 8.")
            continue
        return NODE_MAP[num]


def get_metric_input():
    """Prompt the user for a metric choice and return the metric key."""
    while True:
        raw = input("  Enter metric (1–3): ").strip()
        if not raw:
            print("  [!] Input cannot be empty. Please enter 1, 2, or 3.")
            continue
        try:
            num = int(raw)
        except ValueError:
            print("  [!] Invalid input. Please enter 1, 2, or 3.")
            continue
        if num not in METRIC_MAP:
            print("  [!] Number out of range. Please enter 1, 2, or 3.")
            continue
        return METRIC_MAP[num]


# ─────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────

def main():
    print("\n" + "━" * 50)
    print("   CAVITE TRANSPORTATION NETWORK ANALYZER")
    print("━" * 50)

    # Build graph and load the manually defined fixed positions.
    # get_node_positions() is called exactly once here; the same
    # dictionary (pos) is reused every time draw_graph() is called,
    # so nodes never move between searches.
    G   = build_graph()
    pos = get_node_positions()

    # Open the Matplotlib window (interactive mode)
    plt.ion()
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.canvas.manager.set_window_title("Transportation Network")

    # Initial draw — no path highlighted
    draw_graph(G, pos, ax=ax)
    plt.show(block=False)
    print("\n  [✓] Graph window opened.")

    # ── Main interaction loop ─────────────────────────────────────────
    while True:
        print("\n" + "─" * 50)
        display_node_menu()

        source = get_node_input("Enter starting location (1–8): ")
        target = get_node_input("Enter destination location (1–8): ")

        if source == target:
            print("  [!] Starting and destination locations must be different.")
            continue

        display_metric_menu()
        metric = get_metric_input()

        # Compute shortest path
        path, path_edges, totals = find_shortest_path(G, source, target, metric)

        if path is None:
            print(f"  [!] No path found between {source} and {target}.")
            continue

        # Print results to console
        print_results(path, totals, source, target, metric)

        # Build info text for graph annotation
        metric_label = {"distance": "Distance", "time": "Time", "fuel": "Fuel"}[metric]
        info_text = (
            f"Shortest Path: {source} → {target}\n"
            f"Optimization Metric: {metric_label}\n"
            f"\nPath: {' → '.join(path)}\n"
            f"\nTotal Distance : {totals['distance']:.1f} km\n"
            f"Total Time     : {totals['time']:.0f} minutes\n"
            f"Total Fuel     : {totals['fuel']:.1f} liters"
        )

        # Update graph visualization
        draw_graph(
            G, pos,
            path_edges=path_edges,
            path_nodes=path,
            info_text=info_text,
            ax=ax,
        )
        print("  [✓] Graph visualization updated — shortest path highlighted in red.")

        # ── Ask to continue ───────────────────────────────────────────
        print("\n  What would you like to do next?")
        print("    1 - Run another search")
        print("    2 - Exit")

        while True:
            choice = input("  Enter choice (1 or 2): ").strip()
            if choice == "1":
                break
            elif choice == "2":
                print("\n  Thank you for using the Transportation Network Analyzer!")
                print("  Exiting...\n")
                plt.ioff()
                plt.show()   # Keep window open until manually closed
                sys.exit(0)
            else:
                print("  [!] Please enter 1 or 2.")


if __name__ == "__main__":
    main()
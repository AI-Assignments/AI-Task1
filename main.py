import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import sys
from typing import List, Set

G = nx.Graph()

# Add nodes to graph
nodes = [
    "SportsComplex",
    "Siwaka",
    "Ph.1A",
    "Ph.1B",
    "Phase2",
    "J1",
    "Mada",
    "STC",
    "Phase3",
    "Parking Lot",
]
G.add_nodes_from(nodes)

# Position the nodes accordingly
G.nodes["SportsComplex"]["pos"] = (0, 0)
G.nodes["Siwaka"]["pos"] = (2, 0)
G.nodes["Ph.1A"]["pos"] = (4, 0)
G.nodes["Ph.1B"]["pos"] = (4, -2)
G.nodes["Phase2"]["pos"] = (6, -2)
G.nodes["J1"]["pos"] = (8, -2)
G.nodes["Mada"]["pos"] = (10, -2)
G.nodes["STC"]["pos"] = (4, -4)
G.nodes["Phase3"]["pos"] = (8, -4)
G.nodes["Parking Lot"]["pos"] = (8, -6)

node_pos = nx.get_node_attributes(G, "pos")

# Add edges to graph
straight_edges = [
    ("SportsComplex", "Siwaka", {"weight": 450, "name": "UnkRoad"}),
    ("Siwaka", "Ph.1A", {"weight": 10, "name": "SangaleRd"}),
    ("Ph.1A", "Ph.1B", {"weight": 100, "name": "ParkingWalkWay"}),
    ("Ph.1B", "Phase2", {"weight": 112, "name": "KeriRd"}),
    ("Ph.1B", "STC", {"weight": 50, "name": "KeriRd"}),
    ("Phase2", "J1", {"weight": 600, "name": "KeriRd"}),
    ("J1", "Mada", {"weight": 200, "name": "SangaleRd"}),
    ("STC", "Parking Lot", {"weight": 250, "name": "LibraryWalkWay"}),
    ("Phase3", "Parking Lot", {"weight": 450, "name": "HimaGardensRd"}),
]

G.add_edges_from(straight_edges)

curved_out_edges = [
    ("Ph.1A", "Mada", {"weight": 850, "name": "SangaleRd"}),
    ("Mada", "Parking Lot", {"weight": 700, "name": "langataRd"}),
    ("Phase2", "Phase3", {"weight": 500, "name": "KeriRd"}),
    ("Phase2", "STC", {"weight": 50, "name": "STCwalkway"}),
]

G.add_edges_from(curved_out_edges)

curved_in_edges = [
    ("Siwaka", "Ph.1B", {"weight": 230, "name": "SangaleLink"}),
]
G.add_edges_from(curved_in_edges)

ax = plt.gca()
for edge in curved_out_edges:
    ax.annotate(
        "",
        xy=node_pos[edge[0]],
        xycoords="data",
        xytext=node_pos[edge[1]],
        textcoords="data",
        arrowprops=dict(
            arrowstyle="-",
            color="0.5",
            shrinkA=5,
            shrinkB=5,
            patchA=None,
            patchB=None,
            connectionstyle="arc3,rad=0.3",
        ),
    )

for edge in curved_in_edges:
    ax.annotate(
        "",
        xy=node_pos[edge[0]],
        xycoords="data",
        xytext=node_pos[edge[1]],
        textcoords="data",
        arrowprops=dict(
            arrowstyle="-",
            color="0.5",
            shrinkA=5,
            shrinkB=5,
            patchA=None,
            patchB=None,
            connectionstyle="arc3,rad=-0.3",
        ),
    )

path_names = nx.get_edge_attributes(G, "name")


def bfs(
    G: nx.Graph, destination: str, start: str = "SportsComplex"
) -> (List[str], Set[str]):
    """
    Searches for a path from *destination* from *start* in the
    graph *G*. A path is a list of nodes from start you need to
    pass to reach destination. Returns the path and a set of
    nodes visited during the search
    """
    if start == destination:
        return []
    frontier = deque([start])
    explored = set()
    solution = []
    visited = set()
    while True:
        if not frontier:
            return []
        node = frontier.popleft()
        explored.add(node)
        solution.append(node)
        for adj in G.neighbors(node):
            visited.add(adj)
            if adj not in explored and adj not in frontier:
                if adj == destination:
                    return solution, visited
                frontier.appendleft(adj)


def ucs(
    G: nx.Graph, destination: str, start: str = "SportsComplex"
) -> (List[str], Set[str]):
    """
    Searches for a path from *destination* from *start* in the
    graph *G* using Uniform Cost Search. A path is a list of nodes from start
    you need to pass to reach destination. Returns the path and a set of
    nodes visited during the search
    """

    distances = {
        "SportsComplex": 730,
        "Siwaka": 405,
        "Ph.1A": 380,
        "Ph.1B": 280,
        "STC": 213,
        "Phase2": 210,
        "J1": 500,
        "Phase3": 160,
        "Mada": 630,
        "Parking Lot": 0,
    }
    if start == destination:
        return []
    frontier = deque([start])
    explored = set()
    solution = []
    visited = set()
    while True:
        if not frontier:
            return []
        node = frontier.popleft()
        explored.add(node)
        solution.append(node)
        if node == destination:
            visited.add(node)
            return solution, visited
        neighbors_dist = {}
        for n in G.neighbors(node):
            visited.add(node)
            neighbors_dist[n] = distances[n]
        shortest_neighbour = min(neighbors_dist, key=lambda n: distances[n])
        frontier.appendleft(shortest_neighbour)
        neighbors_dist.clear()


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "bfs":
        path, visited = bfs(G, "STC")
    elif sys.argv[1] == "ucs":
        path, visited = ucs(G, "Parking Lot")
    else:
        path, visited = bfs(G, "STC")
    color_map = []
    # color nodes that have been visited red
    for node in G:
        if node in visited:
            color_map.append("#bb2205")
        else:
            color_map.append("#0e918c")
    nx.draw_networkx(
        G,
        node_pos,
        node_size=2000,
        node_color=color_map,
        edgelist=straight_edges,
    )
    edge_labels = []
    nx.draw_networkx_edge_labels(G, node_pos, path_names)
    plt.axis("off")
    plt.show()
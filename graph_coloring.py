"""
Graph Coloring Algorithm using Welsh-Powell and Greedy approaches.
Used for scheduling, register allocation, map coloring, etc.
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def greedy_coloring(adjacency: Dict[int, List[int]], order: Optional[List[int]] = None) -> Dict[int, int]:
    """
    Greedy graph coloring algorithm.
    Returns a dict mapping node -> color (integer starting from 0).
    """
    if not adjacency:
        return {}

    nodes = list(adjacency.keys())
    if order is None:
        order = nodes

    coloring: Dict[int, int] = {}

    for node in order:
        # Get colors used by neighbors
        neighbor_colors = set()
        for neighbor in adjacency.get(node, []):
            if neighbor in coloring:
                neighbor_colors.add(coloring[neighbor])

        # Assign lowest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color

    return coloring


def welsh_powell_coloring(adjacency: Dict[int, List[int]]) -> Dict[int, int]:
    """
    Welsh-Powell algorithm: order nodes by degree (descending), then apply greedy.
    Generally produces fewer colors than random greedy.
    """
    if not adjacency:
        return {}

    # Sort nodes by degree descending
    order = sorted(adjacency.keys(), key=lambda n: len(adjacency.get(n, [])), reverse=True)
    return greedy_coloring(adjacency, order)


def chromatic_number(coloring: Dict[int, int]) -> int:
    """Return the number of colors used (chromatic number)."""
    if not coloring:
        return 0
    return max(coloring.values()) + 1


def verify_coloring(adjacency: Dict[int, List[int]], coloring: Dict[int, int]) -> bool:
    """Verify no two adjacent nodes share the same color."""
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            if node in coloring and neighbor in coloring:
                if coloring[node] == coloring[neighbor]:
                    return False
    return True


def build_conflict_graph(tasks: List[str], conflicts: List[Tuple[str, str]]) -> Dict[int, List[int]]:
    """
    Build adjacency list from a scheduling problem.
    tasks: list of task names
    conflicts: list of (task_a, task_b) pairs that cannot be scheduled at same time
    """
    task_index = {task: i for i, task in enumerate(tasks)}
    adjacency: Dict[int, List[int]] = {i: [] for i in range(len(tasks))}

    for a, b in conflicts:
        if a in task_index and b in task_index:
            i, j = task_index[a], task_index[b]
            if j not in adjacency[i]:
                adjacency[i].append(j)
            if i not in adjacency[j]:
                adjacency[j].append(i)

    return adjacency


# ─── Preset graph examples ────────────────────────────────────────────────────

PRESETS = {
    "petersen": {
        "name": "Petersen Graph",
        "description": "Classic graph, chromatic number = 3",
        "nodes": list(range(10)),
        "edges": [
            (0,1),(1,2),(2,3),(3,4),(4,0),   # outer pentagon
            (0,5),(1,6),(2,7),(3,8),(4,9),   # spokes
            (5,7),(7,9),(9,6),(6,8),(8,5)    # inner pentagram
        ]
    },
    "complete_k4": {
        "name": "Complete Graph K4",
        "description": "Every node connected to every other, chromatic = 4",
        "nodes": [0,1,2,3],
        "edges": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    },
    "bipartite": {
        "name": "Bipartite Graph",
        "description": "Two-colorable, chromatic number = 2",
        "nodes": list(range(6)),
        "edges": [(0,3),(0,4),(0,5),(1,3),(1,4),(2,5)]
    },
    "cycle_c5": {
        "name": "Cycle C5",
        "description": "Odd cycle, chromatic number = 3",
        "nodes": list(range(5)),
        "edges": [(0,1),(1,2),(2,3),(3,4),(4,0)]
    },
    "scheduling": {
        "name": "Course Scheduling",
        "description": "7 courses with shared students",
        "nodes": list(range(7)),
        "edges": [(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(3,6),(4,6),(5,6)]
    }
}


def edges_to_adjacency(nodes: List[int], edges: List[Tuple[int,int]]) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = {n: [] for n in nodes}
    for a, b in edges:
        if b not in adj[a]: adj[a].append(b)
        if a not in adj[b]: adj[b].append(a)
    return adj


if __name__ == "__main__":
    # Demo
    for key, preset in PRESETS.items():
        adj = edges_to_adjacency(preset["nodes"], preset["edges"])
        coloring = welsh_powell_coloring(adj)
        chi = chromatic_number(coloring)
        valid = verify_coloring(adj, coloring)
        print(f"{preset['name']}: {chi} colors, valid={valid}, coloring={coloring}")

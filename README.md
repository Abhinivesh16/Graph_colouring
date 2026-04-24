# 🎨 Graph Coloring Visualizer

An interactive web app that assigns minimum colors to graph nodes so no two adjacent nodes share a color — the classic **Graph Coloring Problem**, widely used in scheduling, register allocation, and map coloring.

---

## 🚀 Quick Start

```bash
cd graph-coloring

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 🧠 Algorithms

### Welsh–Powell (default)
1. Sort nodes by degree (most connections first)
2. Assign the lowest available color to each node in order
3. Tends to use fewer colors than random greedy

### Greedy
1. Process nodes in their natural order
2. Assign the lowest color not used by any neighbor

---

## 📐 Graph Presets

| Preset | Chromatic # | Notes |
|--------|-------------|-------|
| Petersen Graph | 3 | Classic benchmark graph |
| Complete K4 | 4 | Every node touches every other |
| Bipartite | 2 | Always 2-colorable |
| Cycle C5 | 3 | Odd cycles need 3 colors |
| Course Scheduling | 3 | Real-world scheduling example |

---

## 🖱️ Interactive Controls

| Mode | Action |
|------|--------|
| **Add Node** (＋) | Click the canvas to place a node |
| **Add Edge** (⟵) | Click node A, then node B to connect them |
| **Delete** (✕) | Click any node or edge to remove it |
| **Run Coloring** | Apply the selected algorithm |
| **Reset Colors** | Clear colors, keep the graph |
| **Clear Graph** | Remove everything |

---

## 📁 Project Structure

```
graph-coloring/
├── graph_coloring.py    # Core algorithms (Welsh-Powell, Greedy)
├── app.py               # Flask web server + REST API
├── templates/
│   └── index.html       # Interactive visualizer UI
├── requirements.txt
└── README.md
```

---

## 🔌 REST API

### POST `/api/color`
Color a graph.

**Request:**
```json
{
  "nodes": [0, 1, 2, 3, 4],
  "edges": [[0,1],[1,2],[2,3],[3,4],[4,0]],
  "algorithm": "welsh_powell"
}
```

**Response:**
```json
{
  "coloring": {"0": 0, "1": 1, "2": 0, "3": 1, "4": 2},
  "chromatic_number": 3,
  "valid": true,
  "algorithm": "welsh_powell"
}
```

### GET `/api/presets`
Returns all built-in graph presets.

---

## 💡 Use Cases

- **Exam/Course Scheduling** — courses sharing students get different time slots (colors)
- **Register Allocation** — variables in use at the same time get different CPU registers
- **Map Coloring** — adjacent regions get different colors
- **Wireless Frequency Assignment** — overlapping cells get different frequencies

---

## 🧪 Using the Python Module Directly

```python
from graph_coloring import welsh_powell_coloring, chromatic_number, verify_coloring

adj = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

coloring = welsh_powell_coloring(adj)
print(f"Colors used: {chromatic_number(coloring)}")  # → 2
print(f"Valid: {verify_coloring(adj, coloring)}")     # → True
print(coloring)  # → {0: 0, 3: 1, 1: 1, 2: 1}
```

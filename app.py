from flask import Flask, request, jsonify, render_template
from graph_coloring import (
    greedy_coloring, welsh_powell_coloring, chromatic_number,
    verify_coloring, edges_to_adjacency, PRESETS
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/color", methods=["POST"])
def color_graph():
    data = request.json
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    algorithm = data.get("algorithm", "welsh_powell")

    adj = edges_to_adjacency(nodes, [tuple(e) for e in edges])

    if algorithm == "greedy":
        coloring = greedy_coloring(adj)
    else:
        coloring = welsh_powell_coloring(adj)

    chi = chromatic_number(coloring)
    valid = verify_coloring(adj, coloring)

    return jsonify({
        "coloring": coloring,
        "chromatic_number": chi,
        "valid": valid,
        "algorithm": algorithm
    })


@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify({
        k: {
            "name": v["name"],
            "description": v["description"],
            "nodes": v["nodes"],
            "edges": v["edges"]
        }
        for k, v in PRESETS.items()
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

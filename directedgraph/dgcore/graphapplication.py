from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from directedgraph.dgcore import Graph


def create_graph(graph_name, graph_raw_data):
    new_graph = Graph(graph_name)
    for item in graph_raw_data:
        new_graph.create_element(item)
    return new_graph

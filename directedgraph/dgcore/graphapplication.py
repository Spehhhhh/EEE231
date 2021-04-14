import timeit
import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph


def create_graph(graph_name, graph_raw_data):
    new_graph = Graph(graph_name)
    for item in graph_raw_data:
        new_graph.create_element(item)
    return new_graph


def test_1():
    name = "graph1"
    data = [
        {"type": "Node", "name": "node1", "uid": "7778da0a0a0a"},
        {"type": "Node", "name": "node2", "uid": "32a24bfcfefe"},
        {"type": "Node", "uid": "32a24bfcfefe"},
    ]
    graph1 = create_graph(name, data)
    graph1.print_graph_details()


if __name__ == "__main__":
    print(
        timeit.timeit(
            "test_1()",
            setup="from __main__ import test_1",
            number=100,
        )
    )
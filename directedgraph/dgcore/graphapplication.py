import timeit
import sys
import os
from pathlib import Path
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph
from directedgraph.dgutils import FileManager


class DirectedGraphApplication:
    def __init__(self):
        pass

    def main(self):
        pass

    def quit(self):
        pass


def create_graph(graph_raw_data):
    new_graph = Graph(graph_raw_data[0][0].get("name"))
    for item in graph_raw_data[1]:
        new_graph.create_element(item)
    return new_graph


def load_graph(path):
    fm = FileManager()
    new_graph = create_graph(fm.read_graph(path))
    return new_graph


def test_1():
    graph_attribute = [{"name": "graph1"}]
    graph_elements = [
        {"type": "Node", "name": "node1", "uid": "7778da0a0a0a"},
        {"type": "Node", "name": "node2", "uid": "32a24bfcfefe"},
        {"type": "Node", "uid": "32a24bfcfefe"},
    ]
    graph_raw_data = (graph_attribute, graph_elements)
    graph1 = create_graph(graph_raw_data)
    graph1.print_graph_details()


def test_2():
    path = (
        Path(os.path.dirname(__file__))
        .parent.parent.joinpath("tests")
        .joinpath("test.xml")
    )
    graph = load_graph(str(path))
    graph.print_graph_details()


if __name__ == "__main__":
    # print(
    #     timeit.timeit(
    #         "test_1()",
    #         setup="from __main__ import test_1",
    #         number=10,
    #     )
    # )
    pass

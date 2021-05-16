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
        self.auto_save_interval = 300  # Seconds
        pass

    def main(self):
        pass

    def quit(self):
        pass


def create_graph(graph_raw_data):
    new_graph = Graph(graph_raw_data[0][0].get("name"))
    for item in graph_raw_data[1]:
        new_graph.create_component(item)
    return new_graph


def load_graph(path):
    fm = FileManager()
    new_graph = create_graph(fm.read_graph(path))
    return new_graph


def get_graph(graph):
    pass


def export_graph(path):
    pass


if __name__ == "__main__":
    import unittest
    from tests.test_dgcore_graphapplication import TestDirectedGraphApplication

    unittest.main()

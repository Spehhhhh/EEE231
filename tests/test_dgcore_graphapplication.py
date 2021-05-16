import sys
import os
import time
import timeit
import itertools
import unittest
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import create_graph, load_graph

logger.add(
    "logs/test_dgcore_graphapplication.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestDirectedGraphApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @logger.catch
    def test_(self):
        pass

    def test_create_graph(self):
        graph_attribute = [{"name": "graph1"}]
        graph_components = [
            {"type": "Node", "name": "node1", "uid": "7778da"},
            {"type": "Node", "name": "node2", "uid": "32a24b"},
            {"type": "Node", "uid": "32a24b"},
        ]
        graph_raw_data = (graph_attribute, graph_components)
        graph1 = create_graph(graph_raw_data)
        graph1.print_graph_details()

    def test_load_graph(self):
        path = Path(os.path.dirname(__file__)).joinpath("test.xml")
        graph = load_graph(str(path))
        graph.print_graph_details()


if __name__ == "__main__":
    unittest.main()

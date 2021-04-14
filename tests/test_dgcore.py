import sys
import time
import timeit
import itertools
import unittest
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import (
    GraphElement,
    Graph,
    Node,
    GroundNode,
    SourceNode,
    Arc,
    create_graph,
)

logger.add(
    "logs/test_dgcore.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class GraphUsage(unittest.TestCase):
    @logger.catch
    def test_id(self):
        graph1 = Graph("graph1")
        graph1.create_element({"type": "Node", "name": "Node without UID"})
        graph1.create_element({"type": "Node", "name": "Node 1", "uid": "7778da0a0a0a"})

        graph2 = Graph("graph2")

        self.assertEqual(graph2.elements, {})
        self.assertEqual(len(graph1.elements), 2)

    @logger.catch
    def test_insert_element(self):
        graph1 = Graph("graph1")

        node1 = Node(graph1, "b911b214f553", "node1")
        graph1.insert_element(node1)
        node2 = Node(graph1, "9a2812943a39", "node2")
        graph1.insert_element(node2)

        self.assertEqual(len(graph1.elements), 2)
        self.assertEqual(graph1.get_element("b911b214f553"), node1)
        self.assertEqual(graph1.get_element("b911b214f553").name, "node1")
        self.assertEqual(graph1.get_element("9a2812943a39").parent_graph, graph1)

    @logger.catch
    def test_create_element(self):
        graph1 = Graph("graph1")
        graph1.create_element({"type": "Node", "name": "node1", "uid": "b911b214f553"})

        self.assertEqual(graph1.get_element("b911b214f553").name, "node1")
        self.assertEqual(type(graph1.get_element("b911b214f553")), Node)

    @logger.catch
    def test_create_graph(self):
        name = "graph1"
        data = [
            {"type": "Node", "name": "node1", "uid": "7778da0a0a0a"},
            {"type": "Node", "name": "node2", "uid": "32a24bfcfefe"},
            {"type": "Node", "uid": "32a24bfcfefe"},
        ]
        graph1 = create_graph(name, data)

        self.assertEqual(graph1.name, "graph1")
        self.assertEqual(graph1.get_element("32a24bfcfefe").name, "node2")
        self.assertEqual(len(graph1.elements), 3)

    @logger.catch
    def test_generate_element_uid(self):
        graph1 = Graph("graph1")
        graph1.create_element({"type": "Node", "name": "Node without UID 1"})
        graph1.create_element({"type": "Node", "name": "Node without UID 2"})
        graph1.create_element(
            {"type": "Node", "name": "Node with UID", "uid": "7778da0a0a0a"}
        )
        graph1.create_element(
            {"type": "Node", "name": "Node with duplicate UID", "uid": "7778da0a0a0a"}
        )

        self.assertEqual(len(graph1.elements), 4)

    @logger.catch
    def test_error(self):
        graph1 = Graph("graph1")
        # graph1.create_element({"type": "Arc", "name": "Arc 1", "uid": "7778da0a0a0a"})
        # graph1.create_element({"name": "Fooo", "uid": "7778da0a0a0a"})

    @logger.catch
    def test_query_and_delete(self):
        # print("---Init---")
        graph1 = Graph("graph1")
        graph1.create_element({"type": "Node", "name": "Node without UID 1"})
        graph1.create_element({"type": "Node", "name": "Node without UID 2"})
        graph1.create_element({"type": "Node", "name": "Foo", "uid": "7778da0a0a0a"})
        graph1.create_element({"type": "Node", "uid": "32a24bfcfefe"})
        self.assertEqual(len(graph1.elements), 4)

        # print("---Try Get Node---")
        self.assertEqual(graph1.get_element("7778da0a0a0a").name, "Foo")
        self.assertEqual(graph1.get_element("32a24bfcfefe").name, "Untitled")

        # print("---Try Delete---")
        self.assertEqual(graph1.delete_element("32a24bfcfefe"), True)
        self.assertEqual(graph1.delete_element("32a24bfcfefe"), False)
        self.assertEqual(graph1.delete_element("31233"), False)
        self.assertEqual(len(graph1.elements), 3)

    def test_graph_efficiency(self):
        start_time = time.time()
        for _ in itertools.repeat(None, 100):
            self.test_query_and_delete()
        end_time = time.time()
        print("Elapsed time was %g seconds" % (end_time - start_time))


if __name__ == "__main__":
    unittest.main()

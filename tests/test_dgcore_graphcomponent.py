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
    GraphComponent,
    Graph,
    Node,
    SourceNode,
    GroundNode,
    Arc,
    create_graph,
)

logger.add(
    "logs/test_dgcore_graphcomponent.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestGraphComponent(unittest.TestCase):
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
    def test_get(self):
        component1 = GraphComponent()
        self.assertEqual(vars(component1), component1.get())
        self.assertEqual(component1.get("name"), "Untitled")

    @logger.catch
    def test_node_position(self):
        # node1 = Node(None, None, None, None, [1, 2])
        node1 = Node()
        node1.update_position([0, 9])
        self.assertEqual(node1.get("position"), [0, 9])

    @logger.catch
    def test_groundnode_sourcenode(self):
        groundnode1 = GroundNode()
        self.assertEqual(groundnode1.get("user_defined_attribute"), "0")
        sourcenode1 = SourceNode(None, None, "sourcenode1", None, [2, 3], "foo")
        self.assertEqual(sourcenode1.get("user_defined_attribute"), "foo")


# pass  node as uid
def test_arc_init_case_1():
    from directedgraph.dgcore.graph import Graph

    graph1 = Graph("graph1")
    graph1.create_component({"type": "Node", "name": "Node 1", "uid": "859e4b2ec309"})
    graph1.create_component({"type": "Node", "name": "Node 2", "uid": "7778da0a0a0a"})
    # graph1.print_graph_details()
    arc1 = Arc(
        graph1,
        "123",
        None,
        "arc1",
        "859e4b2ec309",
        "7778da0a0a0a",
    )
    print(arc1.get())
    # print(arc1.nodes)
    print(arc1.get_position())


# pass node as objects
def test_arc_init_case_2():
    node1 = Node(None, None, "node1", None, None)
    node2 = GroundNode(None, None, "node2", None, [10, 10])
    arc1 = Arc(
        None,
        "123",
        None,
        "arc1",
        node1,
        node2,
    )
    print(arc1.get())
    # print(arc1.nodes)
    print(arc1.get_position())


def test_arc_function():
    node1 = GroundNode(None, None, "node1", None, None)
    # set SourceNode user_define_attribute to 5(5v)
    node2 = SourceNode(None, None, "ndoe2", None, None, 10)
    arc1 = Arc(None, "sdasd", "arc1", None, node1, node2, "resistance", 5)
    arc1.get_function()
    print(arc1.get())
    arc1.update_function("resistance")
    print(arc1.get())

    from directedgraph.dgcore.graph import Graph

    graph1 = Graph("graph1")
    graph1.create_component({"type": "Node", "name": "Node 1", "uid": "859e4b2ec309"})
    graph1.create_component({"type": "Node", "name": "Node 2", "uid": "7778da0a0a0a"})
    # graph1.print_graph_details()
    arc2 = Arc(
        graph1, "123", None, "arc2", "859e4b2ec309", "7778da0a0a0a", "resistance", 5
    )
    arc2.get_function()
    print(arc2.get())
    arc2.update_function("resistance")
    print(arc2.get())


if __name__ == "__main__":
    unittest.main()
    # test_arc_init_case_1()
    # test_arc_init_case_2()
    # test_arc_function()

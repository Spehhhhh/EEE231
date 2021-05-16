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
)

logger.add(
    "logs/test_dgcore.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.xml = "TODO"
        pass

    def tearDown(self):
        pass

    @logger.catch
    def test_id(self):
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID"})
        graph1.create_component({"type": "Node", "name": "Node 1", "uid": "7778da"})

        graph2 = Graph("graph2")

        self.assertEqual(graph2.components, {})
        self.assertEqual(len(graph1.components), 2)

    @logger.catch
    def test_insert_component(self):
        graph1 = Graph("graph1")

        node1 = Node(graph1, "b911b2", "node1")
        graph1.insert_component(node1)
        node2 = Node(graph1, "9a2812", "node2")
        graph1.insert_component(node2)

        self.assertEqual(len(graph1.components), 2)
        self.assertEqual(graph1.get_component("b911b2"), node1)
        self.assertEqual(graph1.get_component("b911b2").name, "node1")
        self.assertEqual(graph1.get_component("9a2812").connected_graph, graph1)

    @logger.catch
    def test_create_component(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da",
                "name": "node1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )

        self.assertEqual(graph1.get_component("7778da").name, "node1")
        self.assertIsInstance(graph1.get_component("7778da"), Node)

        graph1.create_component(
            {
                "type": "Node",
                "uid": "0a0a0b",
                "name": "node2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2812",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "0a0a0b",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        self.assertEqual(
            graph1.get_component("9a2812").get_position(), ([50, 50], [400, 500])
        )

    @logger.catch
    def test_generate_component_uid(self):
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component(
            {"type": "Node", "name": "Node with UID", "uid": "7778da"}
        )
        graph1.create_component(
            {"type": "Node", "name": "Node with duplicate UID", "uid": "7778da"}
        )

        self.assertEqual(len(graph1.components), 4)

    @logger.catch
    def test_error(self):
        # graph1.create_component({"type": "Arc", "name": "Arc 1", "uid": "7778da"})
        # graph1.create_component({"name": "Fooo", "uid": "7778da"})
        pass

    @logger.catch
    def test_query_and_delete(self):
        # print("---Init---")
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component({"type": "Node", "name": "Foo", "uid": "7778da"})
        graph1.create_component({"type": "Node", "uid": "32a24b"})
        self.assertEqual(len(graph1.components), 4)

        # print("---Try Get Node---")
        self.assertEqual(graph1.get_component("7778da").name, "Foo")
        self.assertEqual(graph1.get_component("32a24b").name, "Untitled")

        # print("---Try Delete---")
        self.assertTrue(graph1.delete_component("32a24b"))
        self.assertFalse(graph1.delete_component("32a24b"))
        self.assertFalse(graph1.delete_component("31233"))
        self.assertEqual(len(graph1.components), 3)

    def test_verify_graph_integrity(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778da",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778da",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "SourceNode",
                "uid": "9a2812",
                "name": "SourceNode 1",
                "colour": "#0000",
                "position_x": "1000",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da",
                "name": "Node 2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2812",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "7778da",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "b7c567",
                "name": "Arc 2",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "9a2812",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "365bb9",
                "name": "Arc 3",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "9a2812",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        # graph1.print_graph_details()
        # print(graph1.get_component("9a2812943a39").get_position())
        self.assertEqual(
            graph1.verify_graph_integrity(),
            ["Only one Ground Node is allowed", "Source only allows single arcs"],
        )
        # print(graph1.verify_graph_integrity())
        # graph1.print_graph_details()
        # print(graph1.get_component("7778da0a0a0a").get())

    @logger.catch
    def test_query_and_delete_efficiency(self):
        start_time = time.time()
        for _ in itertools.repeat(None, 100):
            self.test_query_and_delete()
        end_time = time.time()
        print(
            "test_query_and_delete_efficiency() Elapsed time was %g seconds"
            % (end_time - start_time)
        )


if __name__ == "__main__":
    unittest.main()

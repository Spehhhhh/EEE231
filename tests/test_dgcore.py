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
        graph1.create_component(
            {"type": "Node", "name": "Node 1", "uid": "7778da0a0a0a"}
        )

        graph2 = Graph("graph2")

        self.assertEqual(graph2.components, {})
        self.assertEqual(len(graph1.components), 2)

    @logger.catch
    def test_insert_component(self):
        graph1 = Graph("graph1")

        node1 = Node(graph1, "b911b214f553", "node1")
        graph1.insert_component(node1)
        node2 = Node(graph1, "9a2812943a39", "node2")
        graph1.insert_component(node2)

        self.assertEqual(len(graph1.components), 2)
        self.assertEqual(graph1.get_component("b911b214f553"), node1)
        self.assertEqual(graph1.get_component("b911b214f553").name, "node1")
        self.assertEqual(graph1.get_component("9a2812943a39").connected_graph, graph1)

    @logger.catch
    def test_create_component(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da0a0a0a",
                "name": "node1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )

        self.assertEqual(graph1.get_component("7778da0a0a0a").name, "node1")
        self.assertIsInstance(graph1.get_component("7778da0a0a0a"), Node)

        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da0a0a0b",
                "name": "node2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2812943a39",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da0a0a0a",
                "node2_uid": "7778da0a0a0b",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        self.assertEqual(
            graph1.get_component("9a2812943a39").get_position(), ([50, 50], [400, 500])
        )

    @logger.catch
    def test_create_graph(self):
        graph1 = create_graph(
            (
                [{"name": "graph1"}],
                [
                    {
                        "type": "Node",
                        "uid": "7778da0a0a0a",
                        "name": "node1",
                        "colour": "#FFFFFF",
                        "position_x": "100",
                        "position_y": "105",
                    },
                    {
                        "type": "Node",
                        "uid": "32a24bfcfefe",
                        "name": "node2",
                        "colour": "#000000",
                        "position_x": "30",
                        "position_y": "30",
                    },
                    {
                        "type": "Node",
                        "uid": "9a2812943a39",
                        "name": "node3",
                    },
                    {
                        "type": "SourceNode",
                        "uid": "b203507d9ef3",
                        "name": "sourcenode1",
                        "colour": "#000000",
                        "position_x": "40",
                        "position_y": "40",
                        "user_defined_attribute": "0",
                    },
                    {
                        "type": "SourceNode",
                        "uid": "e26c0487a31f",
                        "name": "sourcenode2",
                        "colour": "#000000",
                        "position_x": "200",
                        "position_y": "200",
                        "user_defined_attribute": "Test",
                    },
                    {
                        "type": "SourceNode",
                        "uid": "3d8cc5a3ce64",
                        "name": "sourcenode3",
                        "colour": "#000000",
                        "position_x": "500",
                        "position_y": "500",
                        "user_defined_attribute": "Foo",
                    },
                    {
                        "type": "GroundNode",
                        "uid": "365bb94004f2",
                        "name": "groundnode",
                    },
                    {
                        "type": "Arc",
                        "uid": "b7c567add4ff",
                        "name": "arc1",
                        "node1": "365bb94004f2",
                        "node2": "3d8cc5a3ce64",
                    },
                ],
            )
        )
        self.assertEqual(graph1.name, "graph1")
        self.assertEqual(graph1.get_component("b7c567add4ff").name, "arc1")
        self.assertEqual(len(graph1.components), 8)

    @logger.catch
    def test_generate_component_uid(self):
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component(
            {"type": "Node", "name": "Node with UID", "uid": "7778da0a0a0a"}
        )
        graph1.create_component(
            {"type": "Node", "name": "Node with duplicate UID", "uid": "7778da0a0a0a"}
        )

        self.assertEqual(len(graph1.components), 4)

    @logger.catch
    def test_error(self):
        # graph1.create_component({"type": "Arc", "name": "Arc 1", "uid": "7778da0a0a0a"})
        # graph1.create_component({"name": "Fooo", "uid": "7778da0a0a0a"})
        pass

    @logger.catch
    def test_query_and_delete(self):
        # print("---Init---")
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component({"type": "Node", "name": "Foo", "uid": "7778da0a0a0a"})
        graph1.create_component({"type": "Node", "uid": "32a24bfcfefe"})
        self.assertEqual(len(graph1.components), 4)

        # print("---Try Get Node---")
        self.assertEqual(graph1.get_component("7778da0a0a0a").name, "Foo")
        self.assertEqual(graph1.get_component("32a24bfcfefe").name, "Untitled")

        # print("---Try Delete---")
        self.assertTrue(graph1.delete_component("32a24bfcfefe"))
        self.assertFalse(graph1.delete_component("32a24bfcfefe"))
        self.assertFalse(graph1.delete_component("31233"))
        self.assertEqual(len(graph1.components), 3)

    def test_verify_graph_integrity(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778da0a0a0a",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778da0a0a0a",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "SourceNode",
                "uid": "9a2812943a39",
                "name": "SourceNode 1",
                "colour": "#0000",
                "position_x": "1000",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da0a0a0a",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da0a0a0b",
                "name": "Node 2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2812943a39",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da0a0a0a",
                "node2_uid": "7778da0a0a0b",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "b7c567add4ff",
                "name": "Arc 2",
                "colour": "#0000",
                "node1_uid": "7778da0a0a0a",
                "node2_uid": "9a2812943a39",
                "user_define_attribute": None,
                "user_define_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "365bb94004f2",
                "name": "Arc 3",
                "colour": "#0000",
                "node1_uid": "7778da0a0a0a",
                "node2_uid": "9a2812943a39",
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

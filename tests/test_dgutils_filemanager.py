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

from directedgraph.dgutils import FileManager

logger.add(
    "logs/test_dgutils.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestFileManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.path = Path(os.path.dirname(__file__)).joinpath("test.xml")

    def tearDown(self):
        pass

    @logger.catch
    def test_read_graph(self):
        pass

    @logger.catch
    def test_read_graph_raw_data(self):
        fm = FileManager()
        data1 = fm.read_graph_raw_data(str(self.path))
        list1 = [{"name": "My Graph"}]
        list2 = [
            {
                "type": "Node",
                "uid": "1f9cb9",
                "name": "N1",
                "colour": "#FF0000",
                "position_x": "0",
                "position_y": "0",
            },
            {
                "type": "Node",
                "uid": "9cf405",
                "name": "N2",
                "colour": "#FF0000",
                "position_x": "10",
                "position_y": "10",
            },
            {
                "type": "Node",
                "uid": "a129a9",
                "name": "N3",
                "colour": "#FF0000",
                "position_x": "20",
                "position_y": "20",
            },
            {
                "type": "Node",
                "uid": "59d632",
                "name": "N4",
                "colour": "#FF0000",
                "position_x": "30",
                "position_y": "30",
            },
            {
                "type": "Node",
                "uid": "8ad505",
                "name": "N5",
                "colour": "#FF0000",
                "position_x": "40",
                "position_y": "40",
            },
            {
                "type": "Node",
                "uid": "1d2386",
                "name": "N6",
                "colour": "#FF0000",
                "position_x": "50",
                "position_y": "50",
            },
            {
                "type": "Node",
                "uid": "567071",
                "name": "N7",
                "colour": "#FF0000",
                "position_x": "60",
                "position_y": "60",
            },
            {
                "type": "SourceNode",
                "uid": "14123f",
                "name": "S1",
                "colour": "#00FF00",
                "position_x": "100",
                "position_y": "100",
                "user_defined_attribute": "5",
            },
            {
                "type": "GroundNode",
                "uid": "365bb9",
                "name": "G1",
                "colour": "#FFFF00",
                "position_x": "200",
                "position_y": "200",
            },
            {
                "type": "Arc",
                "uid": "8665f0",
                "name": "A1",
                "colour": "#FFFFFF",
                "node1_uid": "14123f",
                "node2_uid": "1f9cb9",
                "user_defined_attribute": "None",
                "user_defined_arc_type": "None",
            },
            {
                "type": "Arc",
                "uid": "174404",
                "name": "C1",
                "colour": "#FFFFFF",
                "node1_uid": "59d632",
                "node2_uid": "1d2386",
                "user_defined_attribute": "10",
                "user_defined_arc_type": "Capacitor",
            },
            {
                "type": "Arc",
                "uid": "1c7ad3",
                "name": "C2",
                "colour": "#FFFFFF",
                "node1_uid": "1d2386",
                "node2_uid": "567071",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Capacitor",
            },
            {
                "type": "Arc",
                "uid": "2201bd",
                "name": "R1",
                "colour": "#FFFFFF",
                "node1_uid": "1f9cb9",
                "node2_uid": "9cf405",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "bd6295",
                "name": "R2",
                "colour": "#FFFFFF",
                "node1_uid": "9cf405",
                "node2_uid": "a129a9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "a88df3",
                "name": "R3",
                "colour": "#FFFFFF",
                "node1_uid": "9cf405",
                "node2_uid": "a129a9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "b081b6",
                "name": "R4",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "2f7002",
                "name": "R5",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "0dcb2f",
                "name": "R6",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "33ae52",
                "name": "R7",
                "colour": "#FFFFFF",
                "node1_uid": "59d632",
                "node2_uid": "8ad505",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "6bf56b",
                "name": "R8",
                "colour": "#FFFFFF",
                "node1_uid": "8ad505",
                "node2_uid": "567071",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "ea40e5",
                "name": "R9",
                "colour": "#FFFFFF",
                "node1_uid": "567071",
                "node2_uid": "365bb9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
        ]
        self.assertEqual(data1[0], list1)
        self.assertEqual(data1[1], list2)

        graph1 = fm.create_graph((list1, list2))
        self.assertEqual(data1[0], graph1.get()[0])

    @logger.catch
    def test_create_graph(self):
        fm = FileManager()
        graph_attribute = [{"name": "graph1"}]
        graph_components = [
            {
                "type": "Node",
                "uid": "7778da",
                "name": "node1",
                "colour": "#FFFFFF",
                "position_x": "100",
                "position_y": "105",
            },
            {
                "type": "Node",
                "uid": "32a24b",
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
                "uid": "b20350",
                "name": "sourcenode1",
                "colour": "#000000",
                "position_x": "40",
                "position_y": "40",
                "user_defined_attribute": "0",
            },
            {
                "type": "SourceNode",
                "uid": "e26c04",
                "name": "sourcenode2",
                "colour": "#000000",
                "position_x": "200",
                "position_y": "200",
                "user_defined_attribute": "Test",
            },
            {
                "type": "SourceNode",
                "uid": "3d8cc5",
                "name": "sourcenode3",
                "colour": "#000000",
                "position_x": "500",
                "position_y": "500",
                "user_defined_attribute": "Foo",
            },
            {
                "type": "GroundNode",
                "uid": "365bb9",
                "name": "groundnode",
            },
            {
                "type": "Arc",
                "uid": "b7c567",
                "name": "arc1",
                "node1": "365bb9",
                "node2": "3d8cc5",
            },
        ]
        graph_raw_data = (graph_attribute, graph_components)
        graph1 = fm.create_graph(graph_raw_data)
        self.assertEqual(graph1.name, "graph1")
        self.assertEqual(graph1.get_component("b7c567").name, "arc1")
        self.assertEqual(len(graph1.components), 8)

    @logger.catch
    def test_read_and_create_graph(self):
        fm = FileManager()
        data1 = fm.read_graph_raw_data(str(self.path))
        graph1 = fm.create_graph(data1)

        graph1.verify_graph_integrity()
        # graph1.print_graph_details()

        self.assertEqual(len(graph1.get_component("1f9cb9").arcs), 2)  # N1 Arcs
        self.assertEqual(len(graph1.get_component("9cf405").arcs), 3)  # N2 Arcs
        self.assertEqual(len(graph1.get_component("59d632").arcs), 5)  # N4 Arcs
        self.assertEqual(len(graph1.get_component("567071").arcs), 3)  # N7 Arcs
        self.assertEqual(len(graph1.get_component("365bb9").arcs), 1)  # G1 Arcs
        # print("N1 Arcs:", len(graph1.get_component("1f9cb9").arcs))
        # print("N2 Arcs:", len(graph1.get_component("9cf405").arcs))
        # print("N4 Arcs:", len(graph1.get_component("59d632").arcs))
        # print("N7 Arcs:", len(graph1.get_component("567071").arcs))
        # print("G1 Arcs:", len(graph1.get_component("365bb9").arcs))


if __name__ == "__main__":
    unittest.main()

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


class FileManagerUsage(unittest.TestCase):
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
        filemanager1 = FileManager()
        data1 = filemanager1.read_graph(str(self.path))
        list1 = [{"name": "graph1"}]
        list2 = [
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
                "colour": "#000000",
                "node1": "365bb94004f2",
                "node2": "3d8cc5a3ce64",
            },
        ]
        self.assertEqual(data1[0], list1)
        self.assertEqual(data1[1], list2)


if __name__ == "__main__":
    unittest.main()

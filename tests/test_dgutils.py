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
        list1 = [{"graph1", "name"}]
        list2 = [
            {"type": "Node", "name": "node1", "uid": "7778da0a0a0a"},
            {"type": "Node", "name": "node2", "uid": "32a24bfcfefe"},
            {"type": "Node", "name": "node3", "uid": "32a24bfcfefe"},
            {"type": "Arc", "name": "arc1", "uid": "32a24bfcfefe"},
        ]
        self.assertEqual(data1[0], list1)
        self.assertEqual(data1[1], list2)


if __name__ == "__main__":
    unittest.main()

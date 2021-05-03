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
        self.xml = "TODO"
        pass

    def tearDown(self):
        pass

    @logger.catch
    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()

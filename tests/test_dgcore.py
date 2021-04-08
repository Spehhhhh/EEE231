import sys
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

import directedgraph

logger.add(
    "logs/test_dgcore.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


@logger.catch
def test_id():
    graph1 = directedgraph.dgcore.Graph("graph1")
    graph2 = directedgraph.dgcore.Graph("graph2")
    graph1.create_element({"type": "Node", "name": "No UID 1"})
    graph1.create_element({"type": "Node", "name": "Foo", "uid": "7778da0a0a0a"})
    graph1.print_graph_details()
    graph2.print_graph_details()


test_id()
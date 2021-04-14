import sys
import timeit
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph, Node, create_graph

logger.add(
    "logs/test_dgcore.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


@logger.catch
def test_id():
    graph1 = Graph("graph1")
    graph2 = Graph("graph2")
    graph1.create_element({"type": "Node", "name": "No UID 1"})
    graph1.create_element({"type": "Node", "name": "Foo", "uid": "7778da0a0a0a"})
    graph1.print_graph_details()
    graph2.print_graph_details()


@logger.catch
def test_insert_element():
    my_graph = Graph("MyGraph")
    node1 = Node(my_graph, "b911b214f553", "Node1")
    node2 = Node(my_graph, "9a2812943a39", "Node2")
    my_graph.insert_element(node1)
    my_graph.insert_element(node2)
    my_graph.print_graph_details()
    print(my_graph.get_element("9a2812943a39"))
    print(my_graph)
    print(my_graph.elements["9a2812943a39"].parent_graph)


@logger.catch
def test_create_element():
    my_graph = Graph("MyGraph")
    my_graph.create_element({"type": "Node", "name": "Node1", "uid": "7778da0a0a0a"})
    my_graph.print_graph_details()


@logger.catch
def test_query_and_delete():
    print("---Init---")
    my_graph = Graph("MyGraph")
    my_graph.create_element({"type": "Node", "name": "No UID 1"})
    my_graph.create_element({"type": "Node", "name": "No UID 2"})
    my_graph.create_element({"type": "Node", "name": "Fooo", "uid": "7778da0a0a0a"})
    my_graph.create_element({"type": "Node", "name": "Foooo", "uid": "32a24bfcfefe"})
    my_graph.print_graph_details()
    print("---Try Get Node---")
    print(my_graph.get_element("7778da0a0a0a"))
    print(my_graph.get_element("32a24bfcfefe"))
    print("---Try Delete---")
    print(my_graph.delete_element("32a24bfcfefe"))
    print(my_graph.delete_element("31233"))
    my_graph.print_graph_details()
    print(my_graph)
    print("---Try Node---")
    node1 = Node(my_graph, "b911b4f553")
    print(node1.get_parent_graph())


@logger.catch
def test_duplicate_key():
    my_graph = Graph("MyGraph")
    my_graph.create_element({"type": "Node", "name": "No UID 1"})
    my_graph.create_element({"type": "Node", "name": "No UID 2"})
    my_graph.create_element({"type": "Node", "name": "Foo", "uid": "7778da0a0a0a"})
    my_graph.create_element({"type": "Node", "name": "Fooo", "uid": "7778da0a0a0a"})
    my_graph.create_element({"type": "Arc", "name": "Fooo", "uid": "7778da0a0a0a"})
    my_graph.create_element({"name": "Fooo", "uid": "7778da0a0a0a"})
    my_graph.print_graph_details()
    # MyGraph.get_element("7778da0a0a0a")


@logger.catch
def test_create_graph():
    name = "my_graph"
    data = [
        {"type": "Node", "name": "Node1", "uid": "7778da0a0a0a"},
        {"type": "Node", "name": "Node2", "uid": "32a24bfcfefe"},
        {"type": "Node", "name": "Node2", "uid": "32a24bfcfefe"},
        {"type": "Node", "uid": "32a24bfcfefe"},
    ]
    my_graph = create_graph(name, data)
    my_graph.print_graph_details()


if __name__ == "__main__":
    print(
        timeit.timeit(
            "test_create_graph()",
            setup="from __main__ import test_create_graph",
            number=1,
        )
    )

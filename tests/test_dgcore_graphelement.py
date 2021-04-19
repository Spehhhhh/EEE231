import sys
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


def test_get():
    element1 = GraphElement()
    print(vars(element1))
    print(element1.get())
    print(element1.get("name"))


def test_node_position():
    # node1 = Node(None, None, None, None, [1, 2])
    node1 = Node()
    print(node1.get())
    node1.update_position([0, 9])
    print(node1.get("position"))
    print(node1.get_position())


def test_groundnode():
    groundnode1 = GroundNode()
    print(groundnode1.get())
    sourcenode1 = SourceNode(None, None, "sourcenode1", None, [2, 3], "abc")
    print(sourcenode1.get())


def test_arc_init_case_1():
    from directedgraph.dgcore.graph import Graph

    graph1 = Graph("graph1")
    graph1.create_element({"type": "Node", "name": "Node 1", "uid": "859e4b2ec309"})
    graph1.create_element({"type": "Node", "name": "Node 2", "uid": "7778da0a0a0a"})
    # graph1.print_graph_details()
    arc1 = Arc(
        graph1,
        "123",
        None,
        "arc1",
        "859e4b2ec309",
        "7778da0a0a0a",
    )
    print(arc1.nodes)
    print(arc1.get_position())


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
    print(arc1.nodes)
    print(arc1.get_position())


if __name__ == "__main__":
    pass

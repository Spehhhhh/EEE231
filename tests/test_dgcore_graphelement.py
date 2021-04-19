import sys
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore.graphelement import (
    GraphElement,
    Node,
    GroundNode,
    SourceNode,
    Arc,
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

def test_arc():
    node1=Node()
    node2=Node()
    arc1=Arc(None,None,'arc1',None,node1,node2)
    print(node1)
    print(arc1.get())
    print(arc1.get_position(node1,node2))

test_arc()

# test_get()
# test_get()
# test_groundnode()
# test_node_position()

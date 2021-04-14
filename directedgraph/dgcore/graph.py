import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import GraphElement, Node


class Graph:
    def __init__(self, name=None):
        self.name = name if name else "Untitled"
        self.elements = {}
        # #TODO 可以优化速度，除了 UID 之外，还有什么经常调用的可以放到外层。

    def rename_graph(self, name):
        self.name = name

    def verify_graph_integrity(self):
        return True

    def get_all(self):
        return True

    def print_graph_details(self):
        print("vars(self):", vars(self))
        # attrs = vars(self)
        # print(", ".join("%s: %s" % item for item in attrs.items()))
        for element in self.elements:  # #TODO 改成从 Value 遍历，不然性能损耗很大。
            print(
                "       UID:",
                self.elements[element].uid,
                "|",
                "Name:",
                self.elements[element].name,
            )

    def create_element(self, parameters):  # #TODO 按参数里的字典新建组件
        if parameters.get("type", None) == "Node":
            element = Node(
                self, parameters.get("uid", None), parameters.get("name", None)
            )
            self.insert_element(element)
            return element
        elif parameters.get("type", None) == "Arc":
            print("Error: Todo")
        elif parameters.get("type", None) == "GroundNode":
            print("Error: Todo")
        elif parameters.get("type", None) == "SourceNode":
            print("Error: Todo")
        else:
            print("Error: Element Type")

    def insert_element(self, element):
        self.elements[element.get_uid()] = element

    def update_element_name(self, uid, name):
        self.elements[uid].name = name

    def update_element_colour(self, uid, colour):
        self.elements[uid].colour = colour

    def get_name(self):
        return self.name

    def get_element(self, uid):
        # print(self.elements[uid].get_name())
        # print("parent_graph:", self.elements[uid].get_parent_graph())
        # print(vars(self.elements[uid])) # 可以返回对象也可以返回字典
        return self.elements[uid]

    def delete_element(self, uid):  # #TODO 需要写误删除逻辑
        if uid in self.elements:
            self.elements.pop(uid)
            return True
        else:
            return False


def init_graph(graph_name, graph_raw_data):
    new_graph = Graph(graph_name)
    for item in graph_raw_data:
        new_graph.create_element(item)
    return new_graph


if __name__ == "__main__":
    import timeit

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

    def test_create_element():
        my_graph = Graph("MyGraph")
        my_graph.create_element(
            {"type": "Node", "name": "Node1", "uid": "7778da0a0a0a"}
        )
        my_graph.print_graph_details()

    def test_query_and_delete():
        print("---Init---")
        my_graph = Graph("MyGraph")
        my_graph.create_element({"type": "Node", "name": "No UID 1"})
        my_graph.create_element({"type": "Node", "name": "No UID 2"})
        my_graph.create_element({"type": "Node", "name": "Fooo", "uid": "7778da0a0a0a"})
        my_graph.create_element(
            {"type": "Node", "name": "Foooo", "uid": "32a24bfcfefe"}
        )
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

    def test_init_graph():
        name = "my_graph"
        data = [
            {"type": "Node", "name": "Node1", "uid": "7778da0a0a0a"},
            {"type": "Node", "name": "Node2", "uid": "32a24bfcfefe"},
            {"type": "Node", "name": "Node2", "uid": "32a24bfcfefe"},
            {"type": "Node", "uid": "32a24bfcfefe"},
        ]
        my_graph = init_graph(name, data)
        my_graph.print_graph_details()

    print(
        timeit.timeit(
            "test_init_graph()",
            setup="from __main__ import test_init_graph",
            number=1,
        )
    )

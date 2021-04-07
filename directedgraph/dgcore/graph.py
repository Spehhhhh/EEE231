from graphelement import GraphElement, Node


class Graph:
    def __init__(self, name="Untitled"):
        self.name = name
        self.elements = {}

    def create_graph():
        return Graph()

    def rename_graph(self, name):
        self.name = name

    def verify_graph_integrity(self):
        return True

    def print_graph_details(self):
        for element in self.elements:
            print(
                "UID:",
                self.elements[element].uid,
                "|",
                "Name:",
                self.elements[element].name,
            )

    def create_element(self, parameters):  # 按参数里的字典新建组件
        element = GraphElement(
            self, parameters.get("uid", None), parameters.get("name", None)
        )
        self.insert_element(element)
        return element

    def insert_element(self, element):
        self.elements[element.get_uid()] = element

    def update_element_name(self, uid, name):
        self.elements[uid].name = name

    def update_element_name(self, uid, colour):
        self.elements[uid].colour = colour

    def get_name(self):
        return self.name

    def get_compoment(self, uid):
        # print(self.elements[uid].get_name())
        # print("parent_graph:", self.elements[uid].get_parent_graph())
        print(vars(self.elements[uid]))
        return self.elements[uid]

    def delete_element(self, uid):
        if uid in self.elements:
            self.elements.pop(uid)
            return True
        else:
            return False


def test1():  # Test Insert
    Node1 = Node("b911b214f553", "Node1")
    Node2 = Node("9a2812943a39", "Node2")
    Node3 = Node("5a1a33237add", "Node3")
    MyGraph = Graph("MyGraph")
    MyGraph.insert_element(Node1)
    MyGraph.insert_element(Node2)
    MyGraph.insert_element(Node3)

    MyGraph.print_graph_details()
    MyGraph.get_compoment("5a1a337add")


def test2():  # Test New
    MyGraph = Graph("MyGraph")
    MyGraph.create_element("Node1")
    MyGraph.create_element("Node2")
    MyGraph.create_element("Node3")
    MyGraph.print_graph_details()


def test3():  # Test Query / Delete
    MyGraph = Graph("MyGraph")
    MyGraph.create_element({"name": "No UID 1"})
    MyGraph.create_element({"name": "No UID 2"})
    MyGraph.create_element({"name": "Fooo", "uid": "7778da0a0a0a"})
    MyGraph.create_element({"name": "Foooo", "uid": "32a24bfcfefe"})
    MyGraph.print_graph_details()
    print("---Try Get Node---")
    MyGraph.get_compoment("7778da0a0a0a")
    MyGraph.get_compoment("32a24bfcfefe")
    print("---Try Delete---")
    print(MyGraph.delete_element("32a24bfcfefe"))
    print(MyGraph.delete_element("31233"))
    MyGraph.print_graph_details()
    print(MyGraph)
    print("---Try Node---")
    Node1 = Node(MyGraph, "b911b4f553")
    print(Node1.get_parent_graph())


def test4():  # Test Duplicate Key
    MyGraph = Graph("MyGraph")
    MyGraph.create_element({"name": "No UID 1"})
    MyGraph.create_element({"name": "No UID 2"})
    MyGraph.create_element({"name": "Foo", "uid": "7778da0a0a0a"})
    MyGraph.create_element({"name": "Fooo", "uid": "7778da0a0a0a"})
    MyGraph.print_graph_details()
    # MyGraph.get_compoment("7778da0a0a0a")


if __name__ == "__main__":
    test4()

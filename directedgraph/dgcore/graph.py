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
        return 0

    def print_graph_details(self):
        for element in self.elements:
            print(
                "UID:",
                self.elements[element].uid,
                "Name:",
                self.elements[element].name,
            )

    def create_element(self, parameters):
        element = GraphElement(
            parameters.get("uid", None), parameters.get("name", None)
        )
        self.insert_element(element)
        return element

    def insert_element(self, element):
        self.elements[element.get_uid()] = element

    def update_element_name(self, uid, name):
        self.elements[uid].name = name

    def update_element_name(self, uid, colour):
        self.elements[uid].colour = colour

    def get_compoment(self, uid):
        print(self.elements[uid].get_name())

    def delete_element(self, uid):
        self.elements.pop(uid)
        return True


def test1():
    Node1 = Node("b911b4f553", "Node1")
    Node2 = Node("9a28943a39", "Node2")
    Node3 = Node("5a1a337add", "Node3")
    MyGraph = Graph("MyGraph")
    MyGraph.insert_element(Node1)
    MyGraph.insert_element(Node2)
    MyGraph.insert_element(Node3)

    MyGraph.print_graph_details()
    MyGraph.get_compoment("5a1a337add")


def test2():
    MyGraph = Graph("MyGraph")
    MyGraph.create_element("Node1")
    MyGraph.create_element("Node2")
    MyGraph.create_element("Node3")
    MyGraph.print_graph_details()


def test3():
    MyGraph = Graph("MyGraph")
    MyGraph.create_element({"name": "No UID"})
    MyGraph.create_element({"name": "Fooo", "uid": "7778da0a0a"})
    MyGraph.create_element({"name": "Foooo", "uid": "32a24bfcfe"})
    MyGraph.print_graph_details()
    print("---Try Delete---")
    MyGraph.delete_element("32a24bfcfe")
    MyGraph.print_graph_details()
    print(MyGraph)


if __name__ == "__main__":
    test3()

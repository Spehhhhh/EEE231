import uuid
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class GraphElement:
    def __init__(self, parent_graph=None, uid=None, name=None, colour=None):
        self.parent_graph = parent_graph
        self.uid = None
        self.generate_uid(uid)
        self.name = name if name else "Untitled"
        self.colour = colour if colour else "#000000"

    def generate_uid(self, old_uid=None):
        if __name__ == "__main__":
            self.uid = uuid.uuid4().hex[:12]
        else:
            if old_uid == None:
                new_uid = uuid.uuid4().hex[:12]
                while new_uid in self.parent_graph.elements:
                    new_uid = uuid.uuid4().hex[:12]
                    self.uid = new_uid
                self.uid = new_uid
                return new_uid
            else:
                if old_uid not in self.parent_graph.elements:
                    self.uid = old_uid
                    return old_uid
                else:
                    print("Error: Duplicate uid occurs:", old_uid)
                    print("Try to reassign UID...")
                    new_uid = uuid.uuid4().hex[:12]
                    while new_uid in self.parent_graph.elements:
                        new_uid = uuid.uuid4().hex[:12]
                        self.uid = new_uid
                    self.uid = new_uid
                    return new_uid

    def get(self, a):
        return vars(self).get(a, None)

    def get_all(self):
        return vars(self)

    def get_parent_graph(self):
        return self.parent_graph

    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour


class Node(GraphElement):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
    ):
        super().__init__(parent_graph, uid, name, colour)
        self.position = position if position else [0, 0]

    def get_position(self):
        return self.position

    def update_node_position(self, position_x, position_y):
        self.position[0] = position_x
        self.position[1] = position_y


class GroundNode(Node):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
    ):
        super().__init__(parent_graph, uid, name, colour, position)
        self.user_defined_attribute = "0"


class SourceNode(Node):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
        user_defined_attribute=None,
    ):
        super().__init__(parent_graph, uid, name, colour, position)
        self.user_defined_attribute = (
            user_defined_attribute if user_defined_attribute else "0"
        )


class Arc(GraphElement):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
    ):
        super().__init__(parent_graph, uid, name, colour)


if __name__ == "__main__":
    element1 = GraphElement()
    print(vars(element1))
    print(element1.get("name"))
    # node1 = Node(None, None, None, None, [1, 2])
    node1 = Node()
    print(node1.get_all())
    node1.update_node_position(0, 9)
    print(node1.get("position"))
    print(node1.get_position())
    groundnode1 = GroundNode()
    print(groundnode1.get_all())
    sourcenode1 = SourceNode(None, None, "sourcenode1", None, [2, 3], "abc")
    print(sourcenode1.get_all())

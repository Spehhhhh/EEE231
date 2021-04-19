import uuid
import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)


class GraphElement:
    def __init__(self, parent_graph=None, uid=None, name=None, colour=None):
        self.parent_graph = parent_graph
        self.uid = None
        self.generate_uid(uid)
        self.name = name if name else "Untitled"
        self.colour = colour if colour else "#000000"

    def generate_uid(self, old_uid=None):
        if self.parent_graph == None:
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
                    print(
                        "Error: Duplicate uid occurs",
                        old_uid,
                        "Try to reassign UID...",
                    )
                    new_uid = uuid.uuid4().hex[:12]
                    while new_uid in self.parent_graph.elements:
                        new_uid = uuid.uuid4().hex[:12]
                        self.uid = new_uid
                    self.uid = new_uid
                    return new_uid

    # .get(): return all
    # .get("name") return name
    def get(self, element_attribute=None):
        if element_attribute == None:
            return vars(self)
        else:
            return vars(self).get(element_attribute, None)

    def get_parent_graph(self):
        return self.parent_graph

    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour

    # #TODO 需要设计 Trace Back 捕捉
    def update(self, element_attribute, element_attribute_new):
        self.element_attribute = element_attribute_new


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

    def update_position(self, position):
        self.position[0] = position[0]
        self.position[1] = position[1]


class GroundNode(Node):
    number_ground_node = 0

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
        GroundNode.number_ground_node += 1

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def check_number_ground_node(self):
        return GroundNode.number_ground_node


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

    def get_user_defined_attribute(self):
        return self.user_defined_attribute


class Arc(GraphElement):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
    ):
        super().__init__(parent_graph, uid, name, colour)

    def get_source_pos(self, node):
        return node.get_position()

    def get_destin_pos(self, node):
        return node.get_position()


if __name__ == "__main__":
    from tests.test_dgcore_graphelement import (
        test_get,
        test_groundnode,
        test_node_position,
    )

    test_get()
    test_groundnode()
    test_node_position()
    pass

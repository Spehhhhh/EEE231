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
        UID_LENGTH = 12
        if self.parent_graph == None:
            self.uid = uuid.uuid4().hex[:UID_LENGTH]
        else:
            if old_uid == None:
                new_uid = uuid.uuid4().hex[:UID_LENGTH]
                while new_uid in self.parent_graph.elements:
                    new_uid = uuid.uuid4().hex[:UID_LENGTH]
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
                    new_uid = uuid.uuid4().hex[:UID_LENGTH]
                    while new_uid in self.parent_graph.elements:
                        new_uid = uuid.uuid4().hex[:UID_LENGTH]
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
    # .update(name)
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

    def update(self, element_attribute, element_attribute_new):
        if element_attribute == "position":
            self.position[0] = element_attribute_new[0]
            self.position[1] = element_attribute_new[1]
        else:
            return super().update(element_attribute, element_attribute_new)

    def update_position(self, position):
        self.position[0] = position[0]
        self.position[1] = position[1]


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


class GroundNode(Node):
    groundnode_counter = 0

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
        GroundNode.groundnode_counter += 1

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def update_user_defined_attribute(self, user_defined_attribute_new):
        self.user_defined_attribute = user_defined_attribute_new

    def check_groundnode_counter(self):
        return GroundNode.groundnode_counter


class Arc(GraphElement):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        node1=None,
        node2=None,
    ):
        super().__init__(parent_graph, uid, name, colour)
        self.nodes = []
        self.update_position(node1, node2)

    # get_position() get positions of two objects connected by the arc
    def get_position(self):
        return (self.nodes[0].get_position(), self.nodes[1].get_position())

    # update_position() get positions of two objects connected by the arc
    # update_position() can accept both UIDs and objects as parameters
    def update_position(self, node1=None, node2=None):
        if node1 is not None:
            if isinstance(node1, str):
                if len(node2) == 12 and self.parent_graph != None:
                    self.nodes.append(self.parent_graph.get_element(node1))
            elif isinstance(node1, Node) or issubclass(node1, Node):
                self.nodes.append(node1)

        if node2 is not None:
            if isinstance(node2, str) and self.parent_graph != None:
                if len(node2) == 12 and self.parent_graph != None:
                    self.nodes.append(self.parent_graph.get_element(node2))
            elif isinstance(node2, Node) or issubclass(node2, Node):
                self.nodes.append(node2)


if __name__ == "__main__":
    from tests.test_dgcore_graphelement import *  # import Test Case

    test_arc_init_case_1()
    test_arc_init_case_2()
    pass

import uuid
import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)


class GraphComponent:
    def __init__(self, connected_graph=None, uid=None, name=None, colour=None):
        self.connected_graph = connected_graph if connected_graph else None
        self.connected_window = None
        self.connected_gui = None

        self.uid = None
        self.generate_uid(uid)
        self.name = name if name else "Untitled"
        self.colour = colour if colour else "#000000"

    # If the instance does not have a UID, a UID is generated.
    # If there is a duplicate UID in the Graph to which the instance belongs, reassign a UID.
    def generate_uid(self, uid_old=None):
        UID_LENGTH = 6
        if self.connected_graph == None:
            self.uid = uuid.uuid4().hex[:UID_LENGTH]
        else:
            if uid_old == None:
                uid_new = uuid.uuid4().hex[:UID_LENGTH]
                while uid_new in self.connected_graph.components:
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    self.uid = uid_new
                self.uid = uid_new
                return uid_new
            else:
                if uid_old not in self.connected_graph.components:
                    self.uid = uid_old
                    return uid_old
                else:
                    # print(
                    #     "Error: Duplicate uid occurs",
                    #     uid_old,
                    #     "Try to reassign UID...",
                    # )
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    while uid_new in self.connected_graph.components:
                        uid_new = uuid.uuid4().hex[:UID_LENGTH]
                        self.uid = uid_new
                    self.uid = uid_new
                    return uid_new

    # .get(): return all
    # .get("name") return name
    def get(self, element_attribute=None):
        if element_attribute == None:
            return vars(self)
        else:
            return vars(self).get(element_attribute, None)

    def get_connected_graph(self):
        return self.connected_graph

    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour

    # .update(name)
    # #TODO 需要设计 Trace Back 捕捉
    def update(self, element_attribute, element_attribute_new):
        self.element_attribute = element_attribute_new

    def update_connected_gui(self, connected_gui_new):
        self.connected_gui = connected_gui_new

    def delete(self):
        if self.connected_graph != None:
            return self.connected_graph.delete_component(self.uid)
        else:
            return False


class Node(GraphComponent):
    def __init__(
        self,
        connected_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
    ):
        self.colour = colour if colour else "#fd5455"
        super().__init__(connected_graph, uid, name, self.colour)

        self.position = position if position else [0, 0]

        # it won't get any value which can be obtained from the simulator
        # The user cannot change (Default is 0)
        self.value = 0

        # Objects of the arc connected to this node
        # #TODO 此处要注意的是 Node 当中这个 List 可能有多个，而 Source Node 中只能有一个
        self.arcs = []

    def get_position(self):
        return self.position

    def get_value(self):
        return self.value

    # .update(position, [10, 10])
    def update(self, element_attribute, element_attribute_new):
        if element_attribute == "position":
            self.position[0] = element_attribute_new[0]
            self.position[1] = element_attribute_new[1]
        else:
            return super().update(element_attribute, element_attribute_new)

    # .update_position([10, 10])
    def update_position(self, position):
        self.position[0] = position[0]
        self.position[1] = position[1]


class SourceNode(Node):
    def __init__(
        self,
        connected_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
        user_defined_attribute=None,  # Current
    ):
        self.colour = colour if colour else "#0f8080"
        super().__init__(connected_graph, uid, name, self.colour, position)

        self.user_defined_attribute = (
            user_defined_attribute if user_defined_attribute else "0"
        )

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def update_user_defined_attribute(self, user_defined_attribute_new):
        self.user_defined_attribute = user_defined_attribute_new


class GroundNode(Node):
    def __init__(
        self,
        connected_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
    ):
        self.colour = colour if colour else "#d4aa01"
        super().__init__(connected_graph, uid, name, self.colour, position)
        self.user_defined_attribute = "0"

        if connected_graph != None:
            self.connected_graph.groundnode_counter += 1

    def get_groundnode_counter(self):
        return self.connected_graph.groundnode_counter

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def update_user_defined_attribute(self):
        return False  # groundnote user_defined_attribute cannot be modified


if __name__ == "__main__":
    import unittest
    from tests.test_dgcore_graphcomponent import TestGraphComponent

    unittest.main()

import uuid
import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)


class GraphComponent:
    def __init__(self, parent_graph=None, uid=None, name=None, colour=None):
        self.parent_graph = parent_graph
        self.uid = None
        self.generate_uid(uid)
        self.name = name if name else "Untitled"
        self.colour = colour if colour else "#000000"

    # If the instance does not have a UID, a UID is generated.
    # If there is a duplicate UID in the Graph to which the instance belongs, reassign a UID.
    def generate_uid(self, uid_old=None):
        UID_LENGTH = 12
        if self.parent_graph == None:
            self.uid = uuid.uuid4().hex[:UID_LENGTH]
        else:
            if uid_old == None:
                uid_new = uuid.uuid4().hex[:UID_LENGTH]
                while uid_new in self.parent_graph.components:
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    self.uid = uid_new
                self.uid = uid_new
                return uid_new
            else:
                if uid_old not in self.parent_graph.components:
                    self.uid = uid_old
                    return uid_old
                else:
                    print(
                        "Error: Duplicate uid occurs",
                        uid_old,
                        "Try to reassign UID...",
                    )
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    while uid_new in self.parent_graph.components:
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

    def get_parent_graph(self):
        return self.parent_graph

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


class Node(GraphComponent):
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
        # it won't get any value which can be obtained from the simulator
        # The user cannot change (Default is 0)
        self.value = 0
        # Objects of the arc connected to this node
        # #TODO 此处要注意的是 Node 当中这个 List 可能有多个，而 Source Node 中只能有一个
        self.arcs = []

    def get_position(self):
        return self.position

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

    def get_value(self):
        return self.value


class SourceNode(Node):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        position=None,
        user_defined_attribute=None,
        current=None,
    ):
        super().__init__(parent_graph, uid, name, colour, position)
        self.user_defined_attribute = (
            user_defined_attribute if user_defined_attribute else "0"
        )
        if current == None:
            self.current = 0
        else:
            self.current = current

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def update_user_defined_attribute(self, user_defined_attribute_new):
        self.user_defined_attribute = user_defined_attribute_new


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

    def get_groundnode_counter(self):
        return GroundNode.groundnode_counter

    def get_user_defined_attribute(self):
        return self.user_defined_attribute

    def update_user_defined_attribute(self):
        return False  # groundnote user_defined_attribute cannot be modified


class Arc(GraphComponent):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        node1=None,
        node2=None,
        #     属性是啥：纯电阻？电容？
        user_define_attribute=None,
        #     阻抗值
        Impedance=None,
    ):
        super().__init__(parent_graph, uid, name, colour)
        self.nodes = []
        self.node1 = node1
        self.node2 = node2
        self.user_define_attribute = user_define_attribute
        self.update_position(node1, node2)
        self.function = {}
        self.Impedance = Impedance

    # get_position() get positions of two objects connected by the arc
    # #TODO 需要设计 Trace Back 捕捉
    def get_position(self):
        return (self.nodes[0].get_position(), self.nodes[1].get_position())

    def update_value(self, data):
        self.Impedance = data

    # update_position() get positions of two objects connected by the arc
    # update_position() can accept both UIDs and objects as parameters
    # #TODO 需要设计 Trace Back 捕捉
    def update_position(self, node1=None, node2=None):
        if node1 is not None:
            if isinstance(node1, str):
                if len(node2) == 12 and self.parent_graph != None:
                    self.nodes.append(self.parent_graph.get_component(node1))
            elif isinstance(node1, Node) or issubclass(node1, Node):
                self.nodes.append(node1)

        if node2 is not None:
            if isinstance(node2, str) and self.parent_graph != None:
                if len(node2) == 12 and self.parent_graph != None:
                    self.nodes.append(self.parent_graph.get_component(node2))
            elif isinstance(node2, Node) or issubclass(node2, Node):
                self.nodes.append(node2)

    def update_user_define_attribute(self, new_user_define_attribute):
        self.user_define_attribute = new_user_define_attribute

    # get editable function,eg: if Take a resistance.
    # The current through the resistance from node i to node j is given by (V_i - V)j) / R.
    # But if the arc represented a diode, the current would be I_0 [exp((V_i - V_j)/kT) - 1].
    def get_function(self):
        if self.user_define_attribute == None:
            return
        elif self.user_define_attribute.lower() == "resistance":
            if (
                isinstance(self.node1, Node)
                and isinstance(self.node2, SourceNode)
                or isinstance(self.node2, GroundNode)
            ):
                return (
                    abs(self.node1.value - float(self.node2.user_defined_attribute))
                    / self.Impedance
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, Node)
            ):
                return (
                    abs(
                        float(self.node1.user_defined_attribute)
                        - float(self.node2.value)
                    )
                    / self.Impedance
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, GroundNode)
                or isinstance(self.node2, SourceNode)
            ):
                return (
                    abs(
                        float(self.node1.user_defined_attribute)
                        - float(self.node2.user_defined_attribute)
                    )
                    / self.Impedance
                )
        elif self.user_define_attribute.lower() == "capacitor":
            if (
                isinstance(self.node1, Node)
                and isinstance(self.node2, SourceNode)
                or isinstance(self.node2, GroundNode)
            ):
                return (
                    abs(self.node1.value - float(self.node2.user_defined_attribute))
                    / self.Impedance
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, Node)
            ):
                return (
                    abs(
                        float(self.node1.user_defined_attribute)
                        - float(self.node2.value)
                    )
                    / self.Impedance
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, GroundNode)
                or isinstance(self.node2, SourceNode)
            ):
                return (
                    abs(
                        float(self.node1.user_defined_attribute)
                        - float(self.node2.user_defined_attribute)
                    )
                    / self.Impedance
                )
        elif self.user_define_attribute.lower() == "diode":
            pass

    # function['resistance']=(V_i - V)j) / R.
    def update_function(self):
        function_update = self.get_function()
        self.function[self.user_define_attribute] = function_update

    def update_node(self):
        if isinstance(self.node1, SourceNode) and isinstance(self.node2, Node):
            node2.value = float(
                self.node1.user_defined_attribute
            ) - node1.current * float(self.Impedance)
        elif isinstance(self.node1, Node) and isinstance(self.node2, Node):
            node2.value = (
                float(self.node1.value)
                - self.Impedance * self.function[self.user_define_attribute]
            )


if __name__ == "__main__":
    node1 = SourceNode(None, None, "Node1", None, [200, 300], 8, 2)
    node2 = Node(None, None, "Node2", None, [300, 300])
    arc1 = Arc(None, None, None, None, node1, node2, "resistance", 5)
    print(
        arc1.user_define_attribute
        + " connceted between {} and {}".format(arc1.node1.name, arc1.node2.name)
    )
    if arc1.user_define_attribute == "resistance":
        print(
            "r1:"
            + str(arc1.Impedance)
            + "\t\t"
            + str(arc1.node1.value)
            + "\t \t"
            + str(arc1.node2.value)
        )
    else:
        print(
            "c1:"
            + str(arc1.Impedance)
            + "\t\t"
            + str(arc1.node1.value)
            + "\t \t"
            + str(arc1.node2.value)
        )
    print(node2.get())
    arc1.update_function()
    arc1.update_node()
    print(node2.get())
    # import unittest
    # from tests.test_dgcore_graphcomponent import TestGraphComponent
    #
    # unittest.main()

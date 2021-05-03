import uuid
import sys
from pathlib import Path
from directedgraph.dgcore.excp import ArcfunctionError

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
    def generate_uid(self, old_uid=None):
        UID_LENGTH = 12
        if self.parent_graph == None:
            self.uid = uuid.uuid4().hex[:UID_LENGTH]
        else:
            if old_uid == None:
                new_uid = uuid.uuid4().hex[:UID_LENGTH]
                while new_uid in self.parent_graph.components:
                    new_uid = uuid.uuid4().hex[:UID_LENGTH]
                    self.uid = new_uid
                self.uid = new_uid
                return new_uid
            else:
                if old_uid not in self.parent_graph.components:
                    self.uid = old_uid
                    return old_uid
                else:
                    print(
                        "Error: Duplicate uid occurs",
                        old_uid,
                        "Try to reassign UID...",
                    )
                    new_uid = uuid.uuid4().hex[:UID_LENGTH]
                    while new_uid in self.parent_graph.components:
                        new_uid = uuid.uuid4().hex[:UID_LENGTH]
                        self.uid = new_uid
                    self.uid = new_uid
                    return new_uid

    # .get(): return all
    # .get("name") return name
    def get(self, component_attribute=None):
        if component_attribute == None:
            return vars(self)
        else:
            return vars(self).get(component_attribute, None)

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
    def update(self, component_attribute, component_attribute_new):
        self.component_attribute = component_attribute_new


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
        self.value = 0

    def get_position(self):
        return self.position

    # .update(position, [10, 10])
    def update(self, component_attribute, component_attribute_new):
        if component_attribute == "position":
            self.position[0] = component_attribute_new[0]
            self.position[1] = component_attribute_new[1]
        else:
            return super().update(component_attribute, component_attribute_new)

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


class Arc(GraphComponent):
    def __init__(
        self,
        parent_graph=None,
        uid=None,
        name=None,
        colour=None,
        node1=None,
        node2=None,
        user_define_attribute=None,
        value=None,
    ):
        super().__init__(parent_graph, uid, name, colour)
        self.nodes = []
        self.node1 = node1
        self.node2 = node2
        self.update_position(node1, node2)
        self.user_define_attribute = user_define_attribute
        self.function = {}
        self.value = value

    # get_position() get positions of two objects connected by the arc
    # #TODO 需要设计 Trace Back 捕捉
    def get_position(self):
        return (self.nodes[0].get_position(), self.nodes[1].get_position())

    def update_value(self, data):
        self.attribute_value = data

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
        if self.user_define_attribute.lower() == "resistance":
            if isinstance(self.node1, str) or isinstance(self.node2, str):
                raise ArcfunctionError("You must enter an Object!!")

            elif (
                isinstance(self.node1, Node)
                and isinstance(self.node2, SourceNode)
                or isinstance(self.node2, GroundNode)
            ):
                return (
                    abs(self.node1.value - int(self.node2.user_defined_attribute))
                    / self.value
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, Node)
            ):
                return (
                    abs(int(self.node1.user_defined_attribute) - int(self.node2.value))
                    / self.value
                )

            elif (
                isinstance(self.node1, SourceNode)
                or isinstance(self.node1, GroundNode)
                and isinstance(self.node2, GroundNode)
                or isinstance(self.node2, SourceNode)
            ):
                return (
                    abs(
                        int(self.node1.user_defined_attribute)
                        - int(self.node2.user_defined_attribute)
                    )
                    / self.value
                )

        elif self.user_define_attribute.lower() == "diode":
            pass

    # function['resistance']=(V_i - V)j) / R.
    def update_function(self, name):
        function_update = self.get_function()
        self.function[name] = function_update


if __name__ == "__main__":
    from tests.test_dgcore_graphcomponent import *  # import Test Case

    test_arc_init_case_1()
    test_arc_init_case_2()
    pass

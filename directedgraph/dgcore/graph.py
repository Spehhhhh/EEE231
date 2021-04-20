import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import GraphElement, Node, SourceNode, GroundNode, Arc
from directedgraph.dgcore import excp


class Graph:
    def __init__(self, name=None):
        self.name = name if name else "Untitled"
        self.elements = {}
        # #TODO 可以优化速度，除了 UID 之外，还有什么经常调用的可以放到外层。

    def print_graph_details(self):
        print("------------------")
        print("Graph vars(self):")
        print(vars(self))
        # attrs = vars(self)
        # print(", ".join("%s: %s" % item for item in attrs.items()))
        print("------------------")
        print("Graph Elements:")
        for element in self.elements:  # #TODO 改成从 Value 遍历，不然性能损耗很大。
            print(
                "UID:",
                self.elements[element].uid,
                "|",
                "Name:",
                self.elements[element].name,
            )

    def get(self):
        return True

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    def get_element(self, uid):
        # print(self.elements[uid].get_name())
        # print("parent_graph:", self.elements[uid].get_parent_graph())
        # print(vars(self.elements[uid])) # 可以返回对象也可以返回字典
        return self.elements[uid]

    def create_element(self, parameters):  # #TODO 按参数里的字典新建组件
        if parameters.get("type", None) == "Node":
            element = Node(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
            )
            self.insert_element(element)
            return element
        elif parameters.get("type", None) == "SourceNode":
            element = SourceNode(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
                parameters.get("user_defined_attribute", None),
            )
            self.insert_element(element)
            return element
        elif parameters.get("type", None) == "GroundNode":
            element = GroundNode(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
                parameters.get("position", None),
            )
            self.insert_element(element)
            return element
        elif parameters.get("type", None) == "Arc":
            element = Arc(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                parameters.get("node1", None),
                parameters.get("node2", None),
            )
            self.insert_element(element)
            return element
        else:
            print("Error: Element Type")

    def insert_element(self, element):
        self.elements[element.get_uid()] = element

    def update_element_name(self, uid, name):
        self.elements[uid].name = name

    def update_element_colour(self, uid, colour):
        self.elements[uid].colour = colour

    # update_arc_position(uid, uid, uid)
    # update_arc_position(uid, node1, node2)
    # update_arc_position(arc, node1, node2)
    def update_arc_position(self, arc1, node1, node2):
        if isinstance(arc1, Arc):
            arc1.update_position(node1, node2)
        elif isinstance(arc1, str):
            if len(node2) == 12 and self.parent_graph == self:
                self.get_element["arc1"].update_position(node1, node2)

    def delete_element(self, uid):  # #TODO 需要写误删除逻辑
        if uid in self.elements:
            self.elements.pop(uid)
            return True
        else:
            return False

    def verify_graph_integrity(self):
        groundnode_counter = 0
        for key in self.elements:
            if self.elements[key]["type"] == "GroundNode":
                groundnode_counter += 1
        if groundnode_counter != 1:
            return False
        else:
            return True


if __name__ == "__main__":
    pass

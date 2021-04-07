from collections import UserList
import uuid


class GraphElement:
    def __init__(self, parent_graph=None, uid=None, name=None, colour=None):
        self.parent_graph = parent_graph
        self.uid = None
        self.generate_uid(uid)
        self.name = "Untitled" if name == None else name
        self.colour = "#000000" if colour == None else colour

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

    def get_parent_graph(self):
        return self.parent_graph

    def get(self, a):
        return vars(self).get(a, None)

    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour

    def get_all(self):
        return vars(self)


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
        self.position = [0, 0] if position == None else position

    def get_position(self):
        return self.position

    def update_node_position(self, position_x, position_y):
        self.position[0] = position_x
        self.position[1] = position_y


if __name__ == "__main__":
    a = GraphElement()
    print(vars(a))
    print(a.get("name"))
    # b = Node(None, None, None, None, [1, 2])
    b = Node()
    print(b.get_all())
    print(b.get("position"))

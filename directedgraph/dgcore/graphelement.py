import uuid


class GraphElement:
    def __init__(self, uid=None, name="Untitled", colour="#000000"):
        if uid == None:
            self.uid = self.generate_uid()
        else:
            self.uid = uid
        self.name = name
        self.colour = colour

    def generate_uid(self):
        return uuid.uuid4().hex[:10]

    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour

    def get_info(self):
        return dir(self)


class Node(GraphElement):
    def __init__(
        self,
        uid=None,
        name="Untitled",
        colour="#000000",
        position=[0, 0],
    ):
        super().__init__(uid, name, colour)
        self.position = position

    def get_position(self):
        return self.position

    def update_node_position(self, position_x, position_y):
        self.position[0] = position_x
        self.position[1] = position_y


class GroundNode(Node):
    def __init__(
        self,
        uid=None,
        name="Untitled",
        colour="#000000",
        position=[0, 0],
    ):
        super().__init__(uid, name, colour, position)


if __name__ == "__main__":

    # a = GraphElement()
    # print(a.get_uid())
    # print(a.get_name())
    # print(a.get_colour())
    b = Node("b911b4f553", 13, 14, [1, 2])
    print(b.get_uid())
    print(b.get_name())
    print(b.get_position())
    # print(b.get_position())

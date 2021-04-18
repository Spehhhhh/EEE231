class GroundNodeNumberException(Exception):
    def __init__(self,number_ground_node=None):
        self.number_ground_node=number_ground_node

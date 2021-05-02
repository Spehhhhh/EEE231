class GroundNodeNumberException(Exception):
    def __init__(self, groundnode_counter=None):
        self.groundnode_counter = groundnode_counter

class ArcfunctionError(Exception):
    pass
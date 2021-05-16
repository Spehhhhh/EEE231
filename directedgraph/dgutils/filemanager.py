import sys
from pathlib import Path
from xml.dom import minidom

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph


class FileManager:
    def __init__(self):
        # self.link_filepath = None
        # self.link_graph = None
        pass

    def parse_attribute(self, component, temp, attributes):
        for attribute in attributes:
            try:
                temp[attribute] = (
                    component.getElementsByTagName(attribute)[0].childNodes[0].data
                )
            except IndexError:
                pass

    def read_graph(self, filepath):
        new_graph = self.create_graph(self.read_graph_raw_data(filepath))
        return new_graph

    def read_graph_raw_data(self, filepath):
        dom1 = minidom.parse(filepath)
        graph_attribute = []
        graph_components = []
        type_list = ["Node", "SourceNode", "GroundNode", "Arc"]

        # Get Graph Name
        graph_name = (
            dom1.getElementsByTagName("Graph")[0]
            .getElementsByTagName("name")[0]
            .childNodes[0]
            .data
        )
        graph_attribute.append({"name": graph_name})

        # Get Graph components
        for component_type in type_list:
            components = dom1.getElementsByTagName(component_type)
            for component in components:
                temp = {}
                temp["type"] = component_type
                temp["uid"] = component.getAttribute("uid")

                self.parse_attribute(component, temp, ["name", "colour"])
                if component_type == "Node":
                    self.parse_attribute(component, temp, ["position_x", "position_y"])
                elif component_type == "SourceNode":
                    self.parse_attribute(
                        component,
                        temp,
                        ["position_x", "position_y", "user_defined_attribute"],
                    )
                elif component_type == "GroundNode":
                    self.parse_attribute(component, temp, ["position_x", "position_y"])
                elif component_type == "Arc":
                    self.parse_attribute(
                        component,
                        temp,
                        [
                            "node1_uid",
                            "node2_uid",
                            "user_defined_attribute",
                            "user_define_arc_type",
                        ],
                    )
                graph_components.append(temp)

        # Return Data as Tuple
        graph = (graph_attribute, graph_components)
        return graph

    def create_graph(self, graph_raw_data):
        new_graph = Graph(graph_raw_data[0][0].get("name"))
        for item in graph_raw_data[1]:
            new_graph.create_component(item)
        return new_graph

    def export_graph(self, filepath, import_graph):
        import_graph.get()

    def export_graph_png(self, filepath, import_graph):
        pass

    def export_graph_pdf(self, filepath, import_graph):
        pass


if __name__ == "__main__":
    # import os

    # path = (
    #     Path(os.path.dirname(__file__))
    #     .parent.parent.joinpath("tests")
    #     .joinpath("test.xml")
    # )
    # dom1 = minidom.parse(str(path))

    import unittest
    from tests.test_dgutils import TestFileManager

    unittest.main()

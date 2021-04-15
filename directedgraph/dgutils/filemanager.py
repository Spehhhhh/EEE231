import sys
from pathlib import Path
from xml.dom import minidom

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph, graph


class FileManager:
    def __init__(self):
        # self.link_filepath = None
        # self.link_graph = None
        pass

    def read_file(self, filepath):
        pass

    def read_graph(self, filepath):
        dom1 = minidom.parse(filepath)
        graph_attribute = []
        graph_elements = []
        type_list = ["Node", "Arc"]

        graph_name = (
            dom1.getElementsByTagName("Graph")[0]
            .getElementsByTagName("name")[0]
            .childNodes[0]
            .data
        )
        graph_attribute.append({"name", graph_name})

        for element_type in type_list:
            elements = dom1.getElementsByTagName(element_type)
            for element in elements:
                temp = {}
                temp["type"] = element_type
                temp["name"] = (
                    element.getElementsByTagName("name")[0].childNodes[0].data
                )
                temp["uid"] = element.getAttribute("uid")
                if element_type == "Node":
                    pass
                elif element_type == "GroundNode":
                    pass
                elif element_type == "SourceNode":
                    pass
                elif element_type == "Arc":
                    pass
                graph_elements.append(temp)

        graph = (graph_attribute, graph_elements)
        return graph

    def save_graph(self, graph, filepath):
        pass

    def export_graph_png(self, graph):
        pass

    def export_graph_pdf(self, graph):
        pass


if __name__ == "__main__":
    pass

import sys
from pathlib import Path
from xml.dom import minidom
import csv
from uuid import uuid4

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph, Node, SourceNode, GroundNode, Arc


def main():
    # Build graph
    graph = Graph("DemoGraph")

    id_node0 = "0"
    node0 = graph.create_component({"type": "Node", "name": "Node 1", "uid": id_node0})
    graph.insert_component(node0)

    id_node1 = "1"
    node1 = graph.create_component({"type": "Node", "name": "Node 1", "uid": id_node1})
    graph.insert_component(node1)

    id_node2 = "2"
    node2 = graph.create_component({"type": "Node", "name": "Node 2", "uid": id_node2})
    graph.insert_component(node2)

    r1 = graph.create_component(
        {
            "type": "Arc",
            "name": "r1",
            "uid": str(uuid4()),
            "node1": id_node1,
            "node2": id_node2,
            "user_defined_attribute": "resistor",
            "Impedance": 1000,
        }
    )
    graph.insert_component(r1)

    r2 = graph.create_component(
        {
            "type": "Arc",
            "name": "r2",
            "uid": str(uuid4()),
            "node1": id_node2,
            "node2": id_node1,
            "user_defined_attribute": "resistor",
            "Impedance": 1000,
        }
    )
    graph.insert_component(r2)

    r3 = graph.create_component(
        {
            "type": "Arc",
            "name": "r3",
            "uid": str(uuid4()),
            "node1": id_node2,
            "node2": id_node1,
            "user_defined_attribute": "resistor",
            "Impedance": 1000,
        }
    )
    vdd = graph.create_component(
        {
            "type": "Arc",
            "name": "vdd",
            "uid": str(uuid4()),
            "node1": id_node1,
            "node2": id_node0,
            "value": 5,
        }
    )
    print(r3.get())

    # Output txt
    with open("../dgcore/DemoGraph.csv", "w", newline="", encoding="utf-8") as f:
        headers = ["#", "Arc", "node1", "node2", "value"]
        f_csv = csv.writer(f, delimiter=" ")
        f_csv.writerow(headers)
        for component in graph.components.values():
            if isinstance(component, Arc):
                f_csv.writerow(
                    [
                        component.get("user_defined_attribute"),
                        "connected between node {} and {}".format(
                            component.get("node1"), component.get("node2")
                        ),
                    ]
                )
                f_csv.writerow(
                    [
                        component.name,
                        graph.components[component.node1].uid,
                        graph.components[component.node2].uid,
                        component.Impedance,
                    ]
                )
        f_csv.writerow([".end"])


if __name__ == "__main__":
    main()

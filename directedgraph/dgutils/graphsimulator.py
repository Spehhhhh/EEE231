import sys
from pathlib import Path
from xml.dom import minidom
import csv
from uuid import uuid4

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import (
    Graph,
    Node,
    SourceNode,
    GroundNode,
    Arc,
    create_graph,
)


def main():
    # Build graph
    graph = Graph("DemoGraph")

    source_node = graph.create_component(
        {"type": "SourceNode", "name": "s1", "color": "#0123123"}
    )

    node4 = graph.create_component(
        {"type": "Node", "name": "n4", "position": [200, 300]}
    )
    graph.insert_component(node4)

    node1 = graph.create_component(
        {"type": "Node", "name": "n1", "position": [300, 400]}
    )
    graph.insert_component(node1)

    node2 = graph.create_component(
        {"type": "Node", "name": "n2", "position": [400, 500]}
    )
    graph.insert_component(node2)

    node3 = graph.create_component(
        {"type": "Node", "name": "n3", "position": [700, 500]}
    )
    graph.insert_component(node3)

    node5 = graph.create_component(
        {"type": "Node", "name": "n5", "position": [800, 500]}
    )

    node6 = graph.create_component(
        {"type": "Node", "name": "n6", "position": [900, 500]}
    )

    node7 = graph.create_component(
        {"type": "Node", "name": "n7", "position": [1000, 500]}
    )

    ground_node = graph.create_component(
        {"type": "GroundNode", "name": "g1", "position": [2000, 500]}
    )

    r1 = graph.create_component(
        {
            "type": "Arc",
            "name": "r1",
            "uid": str(uuid4()),
            "node1": node2,
            "node2": node3,
            "user_define_arc_type": "resistor",
            "user_define_attribute": 150,
        }
    )
    graph.insert_component(r1)

    r2 = graph.create_component(
        {
            "type": "Arc",
            "name": "r2",
            "uid": str(uuid4()),
            "node1": node2,
            "node2": node3,
            "user_define_attribute": 15,
            "user_define_arc_type": "resistor",
        }
    )
    r3 = graph.create_component(
        {
            "type": "Arc",
            "name": "r3",
            "uid": str(uuid4()),
            "node1": node3,
            "node2": node4,
            "user_define_attribute": "255k",
            "user_define_arc_type": "resistor",
        }
    )
    r4 = graph.create_component(
        {
            "type": "Arc",
            "name": "r4",
            "uid": str(uuid4()),
            "node1": node3,
            "node2": node4,
            "user_define_attribute": "200k",
            "user_define_arc_type": "resistor",
        }
    )
    r5 = graph.create_component(
        {
            "type": "Arc",
            "name": "r5",
            "uid": str(uuid4()),
            "node1": node3,
            "node2": node4,
            "user_define_attribute": "120k",
            "user_define_arc_type": "resistor",
        }
    )

    r6 = graph.create_component(
        {
            "type": "Arc",
            "name": "r6",
            "uid": str(uuid4()),
            "node1": node4,
            "node2": node5,
            "user_define_attribute": 40,
            "user_define_arc_type": "resistor",
        }
    )
    graph.insert_component(r2)

    c1 = graph.create_component(
        {
            "type": "Arc",
            "name": "c1",
            "uid": str(uuid4()),
            "node1": source_node,
            "node2": node1,
            "user_define_attribute": 20,
            "user_define_arc_type": "capacitor",
        }
    )
    graph.insert_component(c1)
    c2 = graph.create_component(
        {
            "type": "Arc",
            "name": "c2",
            "uid": str(uuid4()),
            "node1": node1,
            "node2": node2,
            "user_define_attribute": "20u",
            "user_define_arc_type": "capacitor",
        }
    )
    c3 = graph.create_component(
        {
            "type": "Arc",
            "name": "c3",
            "uid": str(uuid4()),
            "node1": node4,
            "node2": node6,
            "user_define_attribute": "100p",
            "user_define_arc_type": "capacitor",
        }
    )
    c4 = graph.create_component(
        {
            "type": "Arc",
            "name": "c4",
            "uid": str(uuid4()),
            "node1": node6,
            "node2": node7,
            "user_define_attribute": "220u",
            "user_define_arc_type": "capacitor",
        }
    )
    c5 = graph.create_component(
        {
            "type": "Arc",
            "name": "c5",
            "uid": str(uuid4()),
            "node1": node7,
            "node2": ground_node,
            "user_define_attribute": "120 nF",
            "user_define_arc_type": "capacitor",
        }
    )
    # Output txt
    with open("../dgcore/DemoGraph.csv", "w", newline="", encoding="utf-8") as f:
        headers = ["#", "Arc_type", "node1", "node2", "value"]
        f_csv = csv.writer(f, delimiter=" ")
        f_csv.writerow(headers)
        f_csv.writerow(["\n"])
        for component in graph.components.values():
            if isinstance(component, Arc):
                f_csv.writerow(
                    [
                        component.get("user_define_arc_type"),
                        "connected between {} and {}".format(
                            component.get("node1").name, component.get("node2").name
                        ),
                    ]
                )
                f_csv.writerow(
                    [
                        component.name,
                        graph.components[component.uid].node1.name,
                        graph.components[component.uid].node2.name,
                        component.user_define_attribute,
                    ]
                )
                f_csv.writerow(["\n"])
        f_csv.writerow([".end"])


if __name__ == "__main__":
    main()

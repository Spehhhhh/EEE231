import csv
import os
from pathlib import Path
import sys

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import Arc, GroundNode, Node, SourceNode
from directedgraph.dgutils import FileManager


class GraphSimulator:
    def __init__(self):
        pass

    def export(self, filepath, import_graph):
        arc_list = []
        node_uid_list = []
        sourcenode_list = []
        groundnode_list = []

        resistor_count = 1
        capacitor_count = 1
        inductor_count = 1

        uid_map = {}

        for component in import_graph.components.values():
            if type(component) == Arc:
                arc_list.append(component)
            if type(component) == SourceNode:
                sourcenode_list.append(component)
            if type(component) == GroundNode:
                groundnode_list.append(component)
            if type(component) == Node:
                node_uid_list.append(component)

        print(arc_list)
        print(node_uid_list)
        print(sourcenode_list)
        print(groundnode_list)
        ####################
        i = 0
        for n in groundnode_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1
        for n in sourcenode_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1
        for n in node_uid_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1

        print(uid_map)

        ####################

        # Output txt
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            graph_name = import_graph.name
            headers = ["Arc", "Node1", "Node2", "Value", "#", str(graph_name)]
            f_csv = csv.writer(f, delimiter=" ")
            f_csv.writerow(headers)

            f_csv.writerow(
                [
                    "VS",
                    uid_map[sourcenode_list[0].uid],
                    uid_map[groundnode_list[0].uid],
                    sourcenode_list[0].user_defined_attribute,
                    ";",
                    sourcenode_list[0].uid,
                    groundnode_list[0].uid,
                ]
            )

            for arc in arc_list:
                if arc.user_defined_arc_type == "Capacitor":
                    print(
                        "C"
                        + str(capacitor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"C{capacitor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    capacitor_count += 1
                elif arc.user_defined_arc_type == "Inductor":
                    print(
                        "L"
                        + str(inductor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"L{inductor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    inductor_count += 1
                elif arc.user_defined_arc_type == "Resistor":
                    print(
                        "R"
                        + str(resistor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"R{resistor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    resistor_count += 1
            f_csv.writerow([".TRAN", "0.1M", "30M", "UIC"])
            f_csv.writerow([".end"])

            # ???????????? UID
            # ??????????????? UID ?????????????????? R ??? C?????????????????????????????? UID ????????? 0 1 2 ??????
            # Eg. (a-f ???????????? Arc ?????????????????? uid) (???????????????????????????????????????????????????????????? Arc ???????????????????????????????????????.cir)
            #   R1 a b
            #   R2 b c
            #   R3 b c
            #   R4,R5,R6 c d
            #   R7 d e
            #   R8 e g
            #   R9 g h
            #   C1 d f
            #   C2 f g
            # ???????????????????????? ab bc bc cd cd cd de df fg eg gh
            # ??? Spice ?????????????????????????????????????????? groundnode ??? sourcenode
            # ?????????????????????????????????????????????????????? groundnode ??? sourcenode ????????? Vdd ??????????????????????????????
            # ?????????????????????R1 ??? node1 ??????????????? UID,R9 ??? node2 ??????????????? UID?????????????????? node ???????????????????????????
            # groundnode ??? sourcenode ?????????????????????????????? node1 ????????? sourcenode???node2 ????????? groundnode
            # ?????????????????????uid=> 01 12 12 23 23 23 34 35 56 46 67
            # ????????????????????? [0,1,1,2,1,2,2,3,2,3,2,3,3,4,3,5,5,6,4,7,6,7]
            # ?????????????????? Vdd 1 22 value???1 22 ??????????????????
            #             R1 1 2 value
            #             R2 3 4 value
            #             ??????
            #             R9 21 22 valu
            #
            # ?????????????????????????????????
            #   Vdd 0 7 x????????? value???
            #   C1 3 5 x
            #   C2 5 6 x
            #   R1 0 1 x
            #   R2 1 2 x
            #   R3 1 2 x
            #   R4 2 3 x
            #   R5 2 3 x
            #   R6 2 3 x
            #   R7 3 4 x
            #   R8 4 6 x
            #   R9 6 7 x


if __name__ == "__main__":
    path = Path(os.path.dirname(__file__)).parent.parent.joinpath("tests").joinpath("test_rlc.xml")

    path_out = Path(os.path.dirname(__file__)).parent.parent.joinpath("tests").joinpath("test_rlc.cir")

    fm = FileManager()
    import_graph = fm.open_graph(str(path))
    gs = GraphSimulator()
    gs.export(path_out, import_graph)

    # graph_attribute = [{"name": "import_graph"}]
    # graph_components = [
    #     {
    #         "type": "Node",
    #         "uid": "7778da",
    #         "name": "Node 2",
    #         "colour": "#fd5455",
    #         "position_x": "100",
    #         "position_y": "105",
    #     },
    #     {
    #         "type": "Node",
    #         "uid": "32a24b",
    #         "name": "Node 3",
    #         "colour": "#fd5455",
    #         "position_x": "30",
    #         "position_y": "30",
    #     },
    #     {
    #         "type": "SourceNode",
    #         "uid": "b20350",
    #         "name": "SourceNode 1",
    #         "colour": "#0f8080",
    #         "position_x": "40",
    #         "position_y": "40",
    #         "user_defined_attribute": "10",
    #     },
    #     {
    #         "type": "GroundNode",
    #         "uid": "365bb9",
    #         "name": "GroundNode 0",
    #         "colour": "#d4aa01",
    #         "position_x": "40",
    #         "position_y": "40",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "2f7002",
    #         "name": "Resistor 1",
    #         "colour": "#0000",
    #         "node1_uid": "b20350",
    #         "node2_uid": "7778da",
    #         "user_defined_attribute": "20",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "0dcb2f",
    #         "name": "Resistor 2",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "7778da",
    #         "user_defined_attribute": "20",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "33ae52",
    #         "name": "Resistor 3",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "4000",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "6bf56b",
    #         "name": "Capacitor 1",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "0.0000005",
    #         "user_defined_arc_type": "Capacitor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "2201bd",
    #         "name": "Inductor 1",
    #         "colour": "#0000",
    #         "node1_uid": "7778da",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "0.2",
    #         "user_defined_arc_type": "Inductor",
    #     },
    # ]
    # graph_raw_data = (graph_attribute, graph_components)
    # import_graph = fm.create_graph(graph_raw_data)

    # import_graph.print_graph_details()

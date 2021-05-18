import sys
import os
from pathlib import Path
import csv
from uuid import UUID, uuid1
from xml.dom.minidom import parseString

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Graph, Node, SourceNode, GroundNode, Arc
from directedgraph.dgutils import FileManager

if __name__ == "__main__":
    fm = FileManager()
    path = (
        Path(os.path.dirname(__file__))
        .parent.parent.joinpath("tests")
        .joinpath("test.xml")
    )
    graph1 = fm.read_graph(str(path))

    arc_list = []
    node_uid_list = []
    sourcenode_list = []
    groundnode_list = []
    resistor_count = 1
    capacitor_count = 1
    uid_map = {}

    for component in graph1.components.values():
        if type(component) == Arc:
            arc_list.append(component)
        if type(component) == SourceNode:
            sourcenode_list.append(component)
        if type(component) == GroundNode:
            groundnode_list.append(component)
        if type(component) == Node:
            node_uid_list.append(component)

    for sourcenode in sourcenode_list:
        pass

    for groundnode in groundnode_list:
        pass

    ####################
    i = 0
    for n in sourcenode_list:
        if n.uid not in uid_map:
            uid_map[n.uid] = i
            i += 1
    for n in node_uid_list:
        if n.uid not in uid_map:
            uid_map[n.uid] = i
            i += 1
    for n in groundnode_list:
        if n.uid not in uid_map:
            uid_map[n.uid] = i
            i += 1
    ####################

    # Output txt
    with open("test.cir", "w", newline="", encoding="utf-8") as f:
        headers = ["#", "Arc", "node1", "node2", "value"]
        f_csv = csv.writer(f, delimiter=" ")
        f_csv.writerow(headers)

        f_csv.writerow(
            [
                f"VDD",
                uid_map[sourcenode_list[0].uid],
                uid_map[groundnode_list[0].uid],
                sourcenode_list[0].user_defined_attribute,
            ]
        )

        for arc in arc_list:
            if arc.user_defined_arc_type == "Resistor":
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
                    ]
                )
                resistor_count = resistor_count + 1
                pass
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
                        f"C{resistor_count}",
                        uid_map[arc.nodes[0].uid],
                        uid_map[arc.nodes[1].uid],
                        arc.user_defined_attribute,
                    ]
                )
                capacitor_count = capacitor_count + 1
                pass
            if arc.user_defined_arc_type == "None":
                pass

        f_csv.writerow([".end"])

    # 批量替换 UID
    # 先把所有的UID按照顺序（先R 再C）输出一下，再把每个UID替换成0 1 2 ……
    # Eg. (a-f 代指每个Arc的两个不同的uid) (这只是一个例子，最后程序应该能根据输入的Arc来输出相对应的电路规格文本.cir)
    #   R1 a b
    #   R2 b c
    #   R3 b c
    #   R4,R5,R6 c d
    #   R7 d e
    #   R8 e g
    #   R9 g h
    #   C1 d f
    #   C2 f g
    # 如果全部列出来即 ab bc bc cd cd cd de df fg eg gh
    # 在Spice输出规范里面不直接考虑单独的groundnode和sourcenode
    # 那么在这个输出规范里面我们应该认为在groundnode和sourcenode有一个Vdd等效为一个电源的输入
    # 在这个例子里，R1的node1没有重合的UID,R9的node2没有重合的UID，所以这两个node可以被认为和单独的
    # groundnode和sourcenode相连结，并通过算法将node1等效于sourcenode，node2等效于groundnode
    # 然后依次替换,uid=> 01 12 12 23 23 23 34 35 56 46 67
    # 这个可能储存在[0,1,1,2,1,2,2,3,2,3,2,3,3,4,3,5,5,6,4,7,6,7]
    # 最后读取输出 Vdd 1 22 value （1 22 指的是位置）
    #             R1 1 2 value
    #             R2 3 4 value
    #             ……
    #             R9 21 22 valu
    #
    # 最后输出到文本里应该是
    #   Vdd 0 7 x（代指value）
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

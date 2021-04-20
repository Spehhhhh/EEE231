from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from directedgraph.dgcore.excp import GroundNodeNumberException
from directedgraph.dgcore.graphelement import (
    GraphElement,
    Node,
    SourceNode,
    GroundNode,
    Arc,
)
from directedgraph.dgcore.graph import Graph
from directedgraph.dgcore.graphapplication import DirectedGraphApplication, create_graph

# import directedgraph.dgcore.graphelement
# import directedgraph.dgcore.graph
# import directedgraph.dgcore.graphapplication

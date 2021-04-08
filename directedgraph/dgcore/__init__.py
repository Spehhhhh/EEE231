from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from directedgraph.dgcore.graphelement import (
    GraphElement,
    Node,
    GroundNode,
    SourceNode,
    Arc,
)
from directedgraph.dgcore.graph import Graph, init_graph

# import directedgraph.dgcore.graphelement
# import directedgraph.dgcore.graph
# import directedgraph.dgcore.graphapplication
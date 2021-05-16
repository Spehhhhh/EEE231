from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from directedgraph.dgcore.excp import GroundNodeNumberError, ArcError
from directedgraph.dgcore.graphcomponent import (
    GraphComponent,
    Node,
    SourceNode,
    GroundNode,
)
from directedgraph.dgcore.graphcomponent_arc import Arc
from directedgraph.dgcore.graph import Graph
from directedgraph.dgcore.graphapplication import DirectedGraphApplication

# import directedgraph.dgcore.graphcomponent
# import directedgraph.dgcore.graph
# import directedgraph.dgcore.graphapplication

from typing import Annotated

from fastapi import Depends
from rdflib import Graph

from app.core.database import graph_singleton

GraphDep = Annotated[Graph, Depends(graph_singleton.get_graph)]

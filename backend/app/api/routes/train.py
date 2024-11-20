from enum import Enum
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Path, Response, status
from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery

from app.api.deps import GraphDep
from app.core.database import PHT, TrainNS, StationNS
from app.models import TrainMetadataBase as TrainMetadataCreate, TrainMetadataUpdate

router = APIRouter()


# Select all triples of subject (?sub) where subject is of type (?uri)
query_subject_properties = prepareQuery(
    """
    SELECT ?sub ?pred ?obj
    WHERE {
        ?sub a ?uri .
        ?sub ?pred ?obj .
    }
    """
)


class ResponseType(str, Enum):
    default = "default"
    jsonld = "json-ld"
    turtle = "turtle"


@router.get("/query-triples")
async def query_triples(graph: GraphDep):
    query = """
        SELECT ?train ?property ?value
        WHERE {
            ?train a pht:Train ;
                ?property ?value .
        }
    """

    query_graph = Graph()
    query_result = graph.query(query, initNs={"pht": PHT})
    for row in query_result:
        query_graph.add(row)

    context = {"pht": PHT, "train": TrainNS}
    jsonld_payload = query_graph.serialize(format="json-ld", indent=4, context=context)

    # Delete temporary graph
    del query_graph

    return Response(jsonld_payload, media_type="application/json+ld")


@router.get("/total-triples")
async def total_triples(graph: GraphDep) -> dict:
    return {"total_triples": len(graph)}


@router.get("/")
async def get_all_trains(graph: GraphDep):
    query_graph = Graph()
    query_result = graph.query(
        query_subject_properties, initBindings={"uri": PHT.Train}
    )
    for row in query_result:
        query_graph.add(row)

    context = {"pht": PHT, "train": TrainNS}
    jsonld_payload = query_graph.serialize(format="json-ld", indent=4, context=context)

    # Delete temporary graph
    del query_graph
    return Response(jsonld_payload, media_type="application/json+ld")


# GET Train metadata by ID
@router.get("/{train_id}", status_code=status.HTTP_200_OK)
async def get_train_metadata(
    graph: GraphDep,
    train_id: Annotated[str, Path(min_length=5)],
    response_type: ResponseType = ResponseType.default,
):
    rdf_triple = (TrainNS[train_id], None, None)

    # Check if Train URI exists
    if rdf_triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train ({train_id}) metadata not found",
        )

    # Return default response
    if response_type is ResponseType.default:
        train_metadata = {"id": train_id}
        for pred, obj in graph.predicate_objects(TrainNS[train_id]):
            train_metadata.update({str(pred): str(obj)})

        return train_metadata

    # Return json-ld response
    subject_graph = Graph()
    for sub, pred, obj in graph.triples(rdf_triple):
        subject_graph.add((sub, pred, obj))

    context = {"pht": PHT, "train": TrainNS}
    jsonld_payload = subject_graph.serialize(
        format="json-ld", indent=4, context=context
    )
    # Delete temporary graph
    del subject_graph

    return Response(jsonld_payload, media_type="application/json+ld")


# Create new Train
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_train_metadata(graph: GraphDep, metadata: TrainMetadataCreate):
    rdf_triple = (TrainNS[metadata.identifier], None, None)
    if rdf_triple in graph:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Metadata already exists for Train ({metadata.identifier})",
        )

    train_id = f"{metadata.identifier}-{uuid4()}"
    jsonld_payload = {
        "@context": {"pht": str(PHT), "train": str(TrainNS)},
        "@id": f"{TrainNS}{metadata.identifier}",
        "@type": "pht:Train",
        "pht:identifier": train_id,
        "pht:title": metadata.title,
        "pht:creator": metadata.creator,
        "pht:description": metadata.description,
        "pht:version": metadata.version,
        "pht:createdAt": metadata.createdAt,
        "pht:updatedAt": metadata.updatedAt,
    }

    graph.parse(
        data=jsonld_payload,
        format="json-ld",
    )
    return jsonld_payload


@router.put("/{train_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_train_metadata(
    graph: GraphDep,
    metadata: TrainMetadataUpdate,
    train_id: Annotated[str, Path(min_length=5)],
):
    rdf_triple = (TrainNS[train_id], None, None)

    # Check if Train URI triples exists
    if rdf_triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train ({train_id}) metadata not found",
        )

    for pred, _ in graph.predicate_objects(TrainNS[train_id]):
        predicate_name = pred.n3(graph.namespace_manager).split(":")[-1]
        new_value = metadata.model_dump().get(predicate_name)

        # If property does not exists in request body, skip the iteration.
        # There can be many properties such as rdf:type etc.
        if not new_value:
            continue

        # Update triples one by one
        graph.set((TrainNS[train_id], pred, Literal(new_value)))


# @router.get("/query-triples")
# async def query_triples(graph: GraphDep):
#     # query = """
#     #     SELECT ?train ?creator
#     #     WHERE {
#     #         ?train a pht:Train ;
#     #            pht:creator ?creator .
#     #     }
#     # """

#     query = """
#     SELECT ?train ?p ?o
#     WHERE {
#         ?train a pht:Train ;
#             ?p ?o .
#     }
#     """

#     # response = []
#     # result = graph.query(query, initNs={"pht": PHT})
#     # for row in result:
#     #     response.append(f"Train: {row.train}, Creator: {row.creator}")

#     return Response(
#         graph.query(query, initNs={"pht": PHT}).serialize(format="json"),
#         media_type="application/json",
#     )

#     #     return Response(
#     #         graph.query(query).serialize(format="json"), media_type="application/json"
#     #     )

#     # return response


@router.get("/clear")
async def remove_all_triples(graph: GraphDep):
    graph.remove((None, None, None))

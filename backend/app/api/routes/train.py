from enum import Enum
import json
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Path, Response, status
from rdflib import Graph, Literal, RDF

from app.api.deps import GraphDep
from app.core.database import PHT, TrainNS, StationNS
from app.models import TrainMetadataBase as TrainMetadataCreate, TrainMetadataUpdate
from app.utils import query_subject_properties

router = APIRouter()


class ResponseType(str, Enum):
    default = "default"
    jsonld = "json-ld"
    turtle = "turtle"


@router.get(
    path="/count",
    summary="Count all triples of type [rdf:type pht:Train]",
    status_code=status.HTTP_200_OK,
)
async def get_triple_count(graph: GraphDep) -> dict:
    triple_count = len(set(graph.subjects(RDF.type, PHT.Train)))
    return {"total_triples": triple_count}


@router.get("/clear")
async def remove_all_triples(graph: GraphDep):
    graph.remove((None, None, None))


@router.get("/")
async def get_all_trains(
    graph: GraphDep,
    response_type: ResponseType = ResponseType.jsonld,
    offset: int = 0,
    limit: int = 10,
):
    query_graph = Graph()
    query_result = graph.query(
        query_subject_properties(),
        initBindings={"uri": PHT.Train},
    )
    for row in query_result:
        query_graph.add(row)

    # Return turtle response
    if response_type is ResponseType.turtle:
        query_graph.bind("pht", PHT)
        query_graph.bind("train", TrainNS)
        ttl_payload = query_graph.serialize()

        del query_graph
        return Response(ttl_payload, media_type="text/turtle")

    # Return json-ld response
    context = {"pht": PHT, "train": TrainNS}
    jsonld_payload: dict = json.loads(
        query_graph.serialize(format="json-ld", indent=4, context=context)
    )
    jsonld_payload["@graph"] = jsonld_payload["@graph"][offset : offset + limit]

    # Delete temporary graph
    del query_graph
    return jsonld_payload


# Get Train metadata by ID
@router.get("/{train_id}")
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

    # Return default response with train metadata as a dictionary
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

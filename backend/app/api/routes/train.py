from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Path, status
from rdflib import Literal

from app import crud
from app.api.deps import GraphDep
from app.core.database import PHT, TrainNS
from app.models import TrainMetadataBase as TrainMetadataCreate, TrainMetadataUpdate
from app.utils import get_triple_count, ResponseType

router = APIRouter()


@router.get(
    path="/count",
    summary="Count all triples of type [rdf:type pht:Train]",
    status_code=status.HTTP_200_OK,
)
async def get_train_triple_count(graph: GraphDep) -> dict:
    return await get_triple_count(graph, PHT.Train)


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
    return crud.get_resources(
        graph=graph,
        response_type=response_type,
        subject=PHT.Train,
        namespace=TrainNS,
        prefix="train",
        offset=offset,
        limit=limit,
    )


# Get Train metadata by ID
@router.get("/{train_id}")
async def get_train_metadata(
    graph: GraphDep,
    train_id: Annotated[str, Path(min_length=5)],
    response_type: ResponseType = ResponseType.default,
):
    return crud.get_resource_metadata(
        graph=graph,
        response_type=response_type,
        subject_id=train_id,
        namespace=TrainNS,
        prefix="train",
    )


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
    payload = {
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
        data=payload,
        format="json-ld",
    )
    return payload


@router.put("/{train_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_train_metadata(
    graph: GraphDep,
    metadata: TrainMetadataUpdate,
    train_id: Annotated[str, Path(min_length=5)],
):
    triple = (TrainNS[train_id], None, None)

    # Check if Train URI triples exists
    if triple not in graph:
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

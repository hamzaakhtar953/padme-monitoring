from typing import Annotated

from fastapi import APIRouter, Path, status

from app import crud
from app.api.deps import GraphDep
from app.api.routes.train import ResponseType
from app.core.database import PHT, StationNS
from app.utils import get_triple_count

router = APIRouter()


@router.get(
    path="/count",
    summary="Count all triples of type [rdf:type pht:Station]",
    status_code=status.HTTP_200_OK,
)
async def get_station_triple_count(graph: GraphDep) -> dict:
    return await get_triple_count(graph, PHT.Station)


@router.get("/")
async def get_all_stations(
    graph: GraphDep,
    response_type: ResponseType = ResponseType.jsonld,
    offset: int = 0,
    limit: int = 10,
):
    return crud.get_resources(
        graph=graph,
        response_type=response_type,
        subject=PHT.Station,
        namespace=StationNS,
        prefix="station",
        offset=offset,
        limit=limit,
    )


@router.get("/{station_id}")
async def get_station_metadata(
    graph: GraphDep,
    station_id: Annotated[str, Path(min_length=3)],
    response_type: ResponseType = ResponseType.default,
):
    return crud.get_resource_metadata(
        graph=graph,
        response_type=response_type,
        subject_id=station_id,
        namespace=StationNS,
        prefix="station",
    )

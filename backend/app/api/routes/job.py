from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Path, Body, status
from rdflib.collection import Collection
from rdflib.namespace import RDF

from app import crud
from app.api.deps import GraphDep
from app.core.database import PHT, TrainNS, StationNS, JobNS, MemoryNS, CpuNS, NetworkNS
from app.models import JobMetadataBase, JobMetricMetadataCreate, JobMetricMetadataDelete
from app.utils import (
    convert_list_to_jsonld,
    JobState,
    JobStateURI,
    MetricType,
    MetricTypeURI,
    MetricNamespace,
    ResponseType,
)

router = APIRouter()


@router.get("/")
async def get_jobs(
    graph: GraphDep,
    response_type: ResponseType = ResponseType.jsonld,
    offset: int = 0,
    limit: int = 10,
):

    return crud.get_resources(
        graph=graph,
        response_type=response_type,
        subject=PHT.TrainExecution,
        namespace=JobNS,
        prefix="job",
        offset=offset,
        limit=limit,
        extra_context={"station": StationNS, "train": TrainNS},
    )


@router.get("/state")
async def get_jobs_count_by_state(graph: GraphDep, state: JobState):
    total_subjects = len(set(graph.subjects(PHT.state, JobStateURI[state].value)))
    return {"total": total_subjects}


@router.get("/{job_id}")
async def get_job_metadata(
    graph: GraphDep,
    job_id: Annotated[str, Path(min_length=5)],
    response_type: ResponseType = ResponseType.default,
):

    return crud.get_resource_metadata(
        graph=graph,
        response_type=response_type,
        subject_id=job_id,
        namespace=JobNS,
        prefix="job",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job_metadata(graph: GraphDep, metadata: JobMetadataBase):
    triple = (JobNS[metadata.identifier], None, None)

    if triple in graph:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Metadata already exists for Job ({metadata.identifier})",
        )

    """
    TODO: Check if current station is in planned route. Throw an error if not.
    """

    # Adding a no consumption memory event to initialize the collection in job
    memory_event_id = str(uuid4())
    payload = {
        "@context": {"pht": str(PHT), "memory": str(MemoryNS)},
        "@graph": [
            {
                "@id": MemoryNS[memory_event_id],
                "@type": PHT.MemoryUsageReportEvent,
                "pht:eventTimestamp": metadata.createdAt,
                "pht:hasJobId": metadata.identifier,
                "pht:value": "0",
                "pht:stationId": {"@id": StationNS[metadata.currentStation]},
            },
            {
                "@id": JobNS[metadata.identifier],
                "@type": PHT.TrainExecution,
                "pht:identifier": metadata.identifier,
                "pht:creator": metadata.creator,
                "pht:description": metadata.description,
                "pht:currentStation": {"@id": StationNS[metadata.currentStation]},
                "pht:trainId": {"@id": TrainNS[metadata.train_id]},
                "pht:state": {"@id": PHT.trainStateIdle},
                "pht:plannedRoute": {
                    "@list": convert_list_to_jsonld(
                        items=metadata.plannedRoute, namespace=StationNS
                    )
                },
                "pht:event": {
                    "@list": convert_list_to_jsonld(
                        items=[memory_event_id], namespace=MemoryNS
                    )
                },
                "pht:createdAt": metadata.createdAt,
                "pht:updatedAt": metadata.updatedAt,
            },
        ],
    }

    graph.parse(data=payload, format="json-ld")
    return payload


@router.get("/{job_id}/status")
async def get_job_status(graph: GraphDep, job_id: Annotated[str, Path(min_length=5)]):
    triple = (JobNS[job_id], None, None)

    # Check if Job URI exists
    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    job_status = graph.value(JobNS[job_id], PHT.state)
    return {"status": JobStateURI._value2member_map_[job_status].name}


@router.put("/{job_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_status(
    graph: GraphDep,
    job_id: Annotated[str, Path(min_length=5)],
    state: JobState,
):
    triple = (JobNS[job_id], None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    graph.set((JobNS[job_id], PHT.state, JobStateURI[state].value))


@router.put("/{job_id}/station", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_current_station(
    graph: GraphDep,
    job_id: Annotated[str, Path(min_length=5)],
    station_name: Annotated[str, Body(embed=True)],
):
    triple = (JobNS[job_id], None, None)

    # TODO: Also check if the station exists in the planned route
    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    graph.set((JobNS[job_id], PHT.currentStation, StationNS[station_name]))


@router.get("/{job_id}/metrics")
async def get_job_metrics(
    graph: GraphDep, metric: MetricType, job_id: Annotated[str, Path(min_length=5)]
):
    triple = (JobNS[job_id], None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    collection = graph.value(JobNS[job_id], PHT.event)
    event_uris = Collection(graph, collection)
    ns_manager = graph.namespace_manager

    metrics = {"source": metric, "metrics": []}
    for uri in event_uris:
        # * Filter only the required event type: memory | cpu | network
        if (uri, RDF.type, MetricTypeURI[metric].value) not in graph:
            continue

        metrics["metrics"].append(
            {
                "id": uri.n3(ns_manager),
                "station_id": graph.value(uri, PHT.stationId).n3(ns_manager),
                "timestamp": graph.value(uri, PHT.eventTimestamp),
                "value": graph.value(uri, PHT.value),
            }
        )

    return metrics


@router.post("/{job_id}/metrics", status_code=status.HTTP_201_CREATED)
async def create_job_metrics(
    graph: GraphDep,
    job_id: Annotated[str, Path(min_length=5)],
    metadata: JobMetricMetadataCreate,
):
    triple = (JobNS[job_id], None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    metric_id = str(uuid4())
    metric_namespace = MetricNamespace[metadata.metric_type].value
    metric_uri = metric_namespace[metric_id]

    payload = {
        "@context": {
            "pht": str(PHT),
            "memory": str(MemoryNS),
            "cpu": str(CpuNS),
            "network": str(NetworkNS),
        },
        "@graph": [
            {
                "@id": metric_uri,
                "@type": MetricTypeURI[metadata.metric_type].value,
                "pht:eventTimestamp": metadata.timestamp,
                "pht:hasJobId": metadata.job_id,
                "pht:value": metadata.value,
                "pht:stationId": {"@id": StationNS[metadata.station_id]},
            },
        ],
    }

    # Add event metadata to database
    graph.parse(data=payload, format="json-ld")

    # Add event to the PHT job event list
    collection = graph.value(JobNS[job_id], PHT.event)
    event_uris = Collection(graph, collection)
    event_uris.append(metric_uri)

    return payload


@router.delete("/{job_id}/metrics", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_metric(
    graph: GraphDep,
    job_id: Annotated[str, Path(min_length=5)],
    metadata: JobMetricMetadataDelete,
):
    triple = (JobNS[job_id], None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    metric_namespace = MetricNamespace[metadata.metric_type].value
    metric_uri = metric_namespace[str(metadata.metric_id)]

    collection = graph.value(JobNS[job_id], PHT.event)
    event_uris = Collection(graph, collection)

    if metric_uri not in event_uris:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Metric ({metric_uri.n3(graph.namespace_manager)}) metadata not found",
        )

    # Remove the metric from the job event list
    event_uris.__delitem__(event_uris.index(metric_uri))

    # Remove the metric data from database
    graph.remove((metric_uri, None, None))

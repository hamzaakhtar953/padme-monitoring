from datetime import datetime
from typing import Annotated
import uuid

from fastapi import APIRouter, HTTPException, Body, status
from rdflib import Graph, Literal, RDF, XSD
from rdflib.collection import Collection

from app import crud
from app.api.deps import GraphDep
from app.core.database import PHT, TrainNS, StationNS, JobNS, MemoryNS, CpuNS, NetworkNS
from app.core.logger import logger
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
    response_type: ResponseType = ResponseType.default,
    offset: int = 0,
    limit: int = 10,
):
    if response_type is not ResponseType.default:
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

    jobs = []
    for subject in graph.subjects(RDF.type, PHT.TrainExecution):
        station_uri = graph.value(subject, PHT.currentStation)
        station_name = graph.value(station_uri, PHT.title)

        job_state_uri = graph.value(subject, PHT.state)
        job_state = JobStateURI._value2member_map_[job_state_uri].name

        jobs.append(
            {
                "identifier": str(graph.value(subject, PHT.identifier)),
                "state": job_state,
                "creator": str(graph.value(subject, PHT.creator)),
                "currentStation": {"uri": station_uri, "name": station_name},
                "trainId": str(graph.value(subject, PHT.trainId)),
                "description": str(graph.value(subject, PHT.description)),
                "createdAt": str(graph.value(subject, PHT.createdAt)),
                "updatedAt": str(graph.value(subject, PHT.updatedAt)),
            }
        )

    # Sort by updatedAt in DESC order
    jobs.sort(key=lambda job: job["updatedAt"], reverse=True)

    return jobs[offset : offset + limit]


# TODO: Add filters i.e. last 7, 30, 90 days
@router.get("/count")
async def get_job_count_by_state(graph: GraphDep, state: JobState):
    total_subjects = len(set(graph.subjects(PHT.state, JobStateURI[state].value)))
    return {"count": total_subjects}


# TODO: Add filters i.e. last 7, 30, 90 days
@router.get("/summary")
async def get_job_summary_by_state(graph: GraphDep):
    query = """
    SELECT ?state (COUNT(?job) AS ?job_count)
    WHERE {
        ?job a pht:TrainExecution .
        ?job pht:state ?state .
    }
    GROUP BY ?state
    ORDER BY DESC(?job_count)
    """

    result = graph.query(query, initNs={"pht": PHT})

    grouped_jobs = []
    for row in result:
        job_state = JobStateURI._value2member_map_[row.state].name
        grouped_jobs.append(
            {
                "state": job_state,
                "count": int(row.job_count),
            }
        )

    return grouped_jobs


@router.get("/{job_id}")
async def get_job_metadata(
    graph: GraphDep,
    job_id: uuid.UUID,
    response_type: ResponseType = ResponseType.default,
):
    subject = JobNS[str(job_id)]

    # Check if Job URI exists
    if (subject, None, None) not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    if response_type is not ResponseType.default:
        return crud.get_resource_metadata(
            graph=graph,
            response_type=response_type,
            subject_id=str(job_id),
            namespace=JobNS,
            prefix="job",
        )

    # Get current station
    station_uri = graph.value(subject, PHT.currentStation)
    station_name = graph.value(station_uri, PHT.title)

    # Get job state
    job_state_uri = graph.value(subject, PHT.state)
    job_state = JobStateURI._value2member_map_[job_state_uri].name

    return {
        "metadataUri": subject,
        "identifier": str(graph.value(subject, PHT.identifier)),
        "state": job_state,
        "creator": str(graph.value(subject, PHT.creator)),
        "currentStation": {"uri": station_uri, "name": station_name},
        "trainId": str(graph.value(subject, PHT.trainId)),
        "description": str(graph.value(subject, PHT.description)),
        "createdAt": str(graph.value(subject, PHT.createdAt)),
        "updatedAt": str(graph.value(subject, PHT.updatedAt)),
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job_metadata(graph: GraphDep, metadata: JobMetadataBase):
    job_id = str(metadata.identifier)
    triple = (JobNS[job_id], None, None)

    if triple in graph:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Metadata already exists for job ({job_id})",
        )

    """
    TODO: Check if current station is in planned route. Throw an error if not.
    """

    # Adding a zero memory consumption event to initialize the event collection in job
    memory_event_id = str(uuid.uuid4())
    payload = {
        "@context": {"pht": str(PHT), "memory": str(MemoryNS)},
        "@graph": [
            {
                "@id": MemoryNS[memory_event_id],
                "@type": PHT.MemoryUsageReportEvent,
                "pht:eventTimestamp": metadata.createdAt,
                "pht:hasJobId": job_id,
                "pht:hasStationId": metadata.currentStation,
                "pht:value": "0",
            },
            {
                "@id": JobNS[job_id],
                "@type": PHT.TrainExecution,
                "pht:identifier": job_id,
                "pht:creator": metadata.creator,
                "pht:description": metadata.description,
                "pht:currentStation": {"@id": StationNS[metadata.currentStation]},
                "pht:trainId": {"@id": TrainNS[metadata.trainId]},
                "pht:state": {"@id": JobStateURI.waiting.value},
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
async def get_job_status(graph: GraphDep, job_id: uuid.UUID):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    # Check if Job URI exists
    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    job_status = graph.value(subject, PHT.state)
    return {"status": JobStateURI._value2member_map_[job_status].name}


@router.put("/{job_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_status(
    graph: GraphDep,
    job_id: uuid.UUID,
    state: JobState,
):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    # Update state
    graph.set((subject, PHT.state, JobStateURI[state].value))

    # Update timestamp
    graph.set(
        (
            subject,
            PHT.updatedAt,
            Literal(datetime.now(), datatype=XSD.dateTime),
        )
    )


@router.put("/{job_id}/station", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_current_station(
    graph: GraphDep,
    job_id: uuid.UUID,
    station_id: Annotated[uuid.UUID, Body(embed=True)],
):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    # TODO: Also check if the station exists in the planned route
    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    # Update current station
    graph.set((subject, PHT.currentStation, StationNS[str(station_id)]))

    # Update timestamp
    graph.set(
        (
            subject,
            PHT.updatedAt,
            Literal(datetime.now(), datatype=XSD.dateTime),
        )
    )


@router.get("/{job_id}/metrics")
async def get_job_metrics(graph: GraphDep, metric: MetricType, job_id: uuid.UUID):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    collection = graph.value(subject, PHT.event)
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
                "jobId": graph.value(uri, PHT.hasJobId),
                "stationId": graph.value(uri, PHT.hasStationId),
                "timestamp": graph.value(uri, PHT.eventTimestamp),
                "value": graph.value(uri, PHT.value),
            }
        )

    metrics["metrics"].sort(key=lambda job: job["timestamp"], reverse=True)
    return metrics


@router.post("/{job_id}/metrics", status_code=status.HTTP_204_NO_CONTENT)
async def create_job_metrics(
    graph: GraphDep,
    job_id: uuid.UUID,
    metadata: JobMetricMetadataCreate,
):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    metric_id = str(uuid.uuid4())
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
                "pht:hasJobId": job_id,
                "pht:hasStationId": metadata.station_id,
                "pht:value": metadata.value,
            },
        ],
    }

    # Add event metadata to database
    graph.parse(data=payload, format="json-ld")

    # Add event to the PHT job event list
    collection = graph.value(subject, PHT.event)
    event_uris = Collection(graph, collection)
    event_uris.append(metric_uri)


# TODO: Implement subscriber pattern to delete all job metrics when job is finished.
# TODO: Maybe use Rabbitmq for message passing.
@router.delete("/{job_id}/metrics", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_metric(
    graph: GraphDep,
    job_id: uuid.UUID,
    metadata: JobMetricMetadataDelete,
):
    subject = JobNS[str(job_id)]
    triple = (subject, None, None)

    if triple not in graph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ({job_id}) metadata not found",
        )

    metric_namespace = MetricNamespace[metadata.metric_type].value
    metric_uri = metric_namespace[str(metadata.metric_id)]

    collection = graph.value(subject, PHT.event)
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

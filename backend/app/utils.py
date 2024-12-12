from enum import Enum

from rdflib.namespace import RDF, Namespace
from rdflib.plugins.sparql import prepareQuery

from app.api.deps import GraphDep
from app.core.database import PHT, MemoryNS, CpuNS, NetworkNS


class ResponseType(str, Enum):
    default = "default"
    jsonld = "json-ld"
    turtle = "turtle"


class JobState(str, Enum):
    idle = "idle"
    transmission = "transmission"
    waiting = "waiting"
    running = "running"
    failed = "failed"
    finished = "finished"


# class JobStateURI(Enum):
class JobStateURI(Enum):
    idle = PHT.trainStateIdle
    transmission = PHT.trainStateTransmission
    waiting = PHT.trainStateWaiting
    running = PHT.trainStateRunning
    failed = PHT.trainStateFailed
    finished = PHT.trainStateFinished


class MetricType(str, Enum):
    memory = "memory"
    cpu = "cpu"
    network = "network"


class MetricNamespace(Enum):
    memory = MemoryNS
    cpu = CpuNS
    network = NetworkNS


class MetricTypeURI(Enum):
    memory = PHT.MemoryUsageReportEvent
    cpu = PHT.CPUUsageReportEvent
    network = PHT.NetworkUsageReportEvent


# Select all triples of subject (?sub) where subject is of type (?uri)
def query_subject_properties():
    return prepareQuery(
        """
        SELECT ?sub ?pred ?obj
        WHERE {
            ?sub a ?uri .
            ?sub ?pred ?obj .
        }
        """
    )


async def get_triple_count(graph: GraphDep, rdf_type) -> dict:
    triple_count = len(set(graph.subjects(RDF.type, rdf_type)))
    return {"total_triples": triple_count}


def convert_list_to_jsonld(items: list, namespace: Namespace):
    return list(map(lambda item: {"@id": namespace[item]}, items))

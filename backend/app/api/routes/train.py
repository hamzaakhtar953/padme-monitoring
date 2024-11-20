from fastapi import APIRouter, Response
from rdflib import FOAF

from app.api.deps import GraphDep
from app.core.database import NPHT, NTrain, NStation
from app.models import TrainMetadataModel

router = APIRouter()


# data_graph = {
#     "@context": {"@vocab": "http://schema.org/"},
#     "@id": "http://example.org/#Bob",
#     "@type": "Person",
#     "givenName": "Muhammad Hamza",
#     "familyName": "Akhtar",
#     "birthDate": "1995-15-12",
#     "deathDate": "1999-15-12",
#     "address": {
#         "@id": "http://example.org/ns#BobsAddress",
#         "streetAddress": "1600 Amphitheatre Pkway",
#         "postalCode": 9404,
#     },
# }


# {
#     "identifier": "metrics-csv",
#     "title": "Metrics CSV",
#     "creator": "Hamza Akhtar",
#     "description": "A Big Description of the Train",
#     "version": "1.0",
#     "created_at": "2024-11-19T23:39:29.355726",
# }


@router.post("/")
async def add_train_metadata(graph: GraphDep, metadata: TrainMetadataModel):
    payload = {
        "@context": {"pht": str(NPHT), "train": str(NTrain)},
        "@id": f"{NTrain}{metadata.identifier}",
        "@type": "pht:Train",
        "pht:identifier": metadata.identifier,
        "pht:title": metadata.title,
        "pht:creator": metadata.creator,
        "pht:description": metadata.description,
        "pht:version": metadata.version,
        "pht:createdAt": metadata.created_at,
    }

    graph.parse(data=payload, format="json-ld")
    return payload


@router.get("/total-triples")
async def total_triples(graph: GraphDep) -> dict:
    return {"total_triples": len(graph)}


@router.get("/query-triples")
async def query_triples(graph: GraphDep):
    query = """
        SELECT ?train ?creator
        WHERE {
            ?train a pht:Train ;
               pht:creator ?creator .
        }
    """

    response = []
    result = graph.query(query, initNs={"pht": NPHT})
    for row in result:
        response.append(f"Train: {row.train}, Creator: {row.creator}")

    # return Response(
    #     graph.query(query, initNs={"pht": NPHT}).serialize(format="json"),
    #     media_type="application/json",
    # )

    return response


@router.get("/clear")
async def remove_all_triples(graph: GraphDep):
    graph.remove((None, None, None))


# @app.get("/metadata/train/add")
# async def add_train_metadata(graph: GraphDep):
#     pass


# @app.get("/test/create-triples")
# async def create_triples(graph: GraphDep):
#     EX = Namespace("http://example.org/#")
#     graph.bind("ex", EX)

#     graph.add((EX.Hamza, RDF.type, FOAF.Person))
#     graph.add(
#         (EX.Hamza, FOAF.name, Literal("Muhammad Hamza Akhtar", datatype=XSD.string))
#     )
#     graph.add((EX.Hamza, FOAF.age, Literal(28)))
#     graph.add((EX.Hamza, FOAF.knows, EX.Ayesha))

#     graph.add((EX.Ayesha, RDF.type, FOAF.Person))
#     graph.add((EX.Ayesha, FOAF.name, Literal("Ayesha Ali")))


# @app.get("/test/total-triples")
# async def total_triples(graph: GraphDep) -> dict:
#     return {"total_triples": len(graph)}


# @app.get("/test/query-triples")
# async def query_triples(graph: GraphDep):
#     query = """
#         SELECT ?person ?name ?age
#         WHERE {
#             ?person a foaf:Person ;
#                     foaf:name ?name .
#         }
#     """

#     return Response(
#         graph.query(query).serialize(format="json"), media_type="application/json"
#     )


@router.get("/")
# async def get_triples(graph: GraphDep, format: Literal["ttl", "json-ld"] = "ttl"):
async def get_triples(graph: GraphDep):
    context = {"foaf": str(FOAF)}
    # return Response(
    #     graph.serialize(
    #         format="json-ld", context=context, media_type="application/json+ld"
    #     )
    # )
    return Response(graph.serialize(), media_type="text/turtle")

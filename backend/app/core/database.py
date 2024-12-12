from rdflib import Graph, Namespace
from rdflib_sqlalchemy.store import SQLAlchemy
from sqlalchemy.engine.url import URL

from app.core.logger import logger

SCHEMA_URL = "https://schema.padme-analytics.de/1_0.ttl"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="hamzaakhtar",
    host="localhost",
    port=5432,
    database="TestDB",
)

# TODO: Add 's' at the end of Train and Station Namespace
PHT = Namespace("http://schema.padme-analytics.de/#")
TrainNS = Namespace("http://monitoring.padme-analytics.de/train/")
StationNS = Namespace("http://monitoring.padme-analytics.de/stations/")
JobNS = Namespace("http://monitoring.padme-analytics.de/jobs/")
MemoryNS = Namespace("http://monitoring.padme-analytics.de/memory/")
CpuNS = Namespace("http://monitoring.padme-analytics.de/cpu/")
NetworkNS = Namespace("http://monitoring.padme-analytics.de/network/")


class RDFGraphSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RDFGraphSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.info("Initializing the Graph Database")
        self.store = SQLAlchemy(configuration=DATABASE_URL)
        self.rdf_graph = Graph(self.store, identifier="rdf_store")
        self.rdf_graph.open(configuration=DATABASE_URL, create=True)

    def get_graph(self) -> Graph:
        return self.rdf_graph

    def close_graph(self) -> None:
        logger.debug("Closing the RDF graph database...")
        self.rdf_graph.close()


graph_singleton = RDFGraphSingleton()

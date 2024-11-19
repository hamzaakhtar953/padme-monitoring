from enum import Enum

from rdflib import Graph, Namespace
from rdflib_sqlalchemy import registerplugins
from rdflib_sqlalchemy.store import SQLAlchemy
from sqlalchemy.engine.url import URL

from core.log_config import logger

# Register SQLAlchemy Plugins
registerplugins()

SCHEMA_URL = "https://schema.padme-analytics.de/1_0.ttl"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="hamzaakhtar",
    host="localhost",
    port=5432,
    database="TestDB",
)

NPHT = Namespace("http://schema.padme-analytics.de/#")
NTrain = Namespace("http://monitoring.padme-analytics.de/train/")
NStation = Namespace("http://monitoring.padme-analytics.de/station/")


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

        # Only add schema for the first time
        # We don't need to load this schema in our graph.
        
        # if len(self.rdf_graph) == 0:
        #     logger.info(f"Loading ontology in RDF graph from: {SCHEMA_URL}")
        #     self.rdf_graph.parse(SCHEMA_URL)

    def get_graph(self) -> Graph:
        return self.rdf_graph

    def close_graph(self):
        logger.debug("Closing the RDF graph database...")
        self.rdf_graph.close()


rdf_graph = RDFGraphSingleton()

from rdflib.plugins.sparql import prepareQuery


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

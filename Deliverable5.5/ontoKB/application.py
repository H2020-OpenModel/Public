import os
from tripper import Triplestore
from ontoflow.engine import OntoFlowDMEngine
from ontoflow.mco_strategies.minimumCostStrategy import MinimumCostStrategy


ONTOLOGY_FOLDER = __file__
ONTOLOGY_FILENAME = "openmodel-inferred.ttl"
INDIVIDUALS_FILENAME = "individuals.ttl"
COST_FILENAME = "cost_definitions.yaml"


if __name__ == "__main__":
    
    mco_strategy = MinimumCostStrategy()

    ## Init triplestore
    Triplestore.remove_database(backend="stardog", database="d55_usecase", triplestore_url="http://localhost:5820")
    Triplestore.create_database(backend="stardog", database="d55_usecase", triplestore_url="http://localhost:5820")
    ts = Triplestore(backend="stardog", triplestore_url="http://localhost:5820", database="d55_usecase")

    # Add ontology and individuals
    ts.parse(os.path.join(ONTOLOGY_FOLDER, "..", ONTOLOGY_FILENAME), format="turtle")
    ts.parse(os.path.join(ONTOLOGY_FOLDER, "..", INDIVIDUALS_FILENAME), format="turtle")


    engine = OntoFlowDMEngine(triplestore = ts, cost_file = os.path.join(ONTOLOGY_FOLDER, "..", COST_FILENAME), mco_interface = mco_strategy)

    target_IRI = "http://emmo.info/emmo#FluidDensity"
    sources_IRIs = {}
    route = engine.getmappingroute(target_IRI, sources_IRIs)

    print(route[target_IRI].show())

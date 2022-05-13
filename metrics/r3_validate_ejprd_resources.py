from fair_test import FairTest, FairTestEvaluation
from pyshex import ShExEvaluator
from rdflib import URIRef
from rdflib.namespace import DC, DCTERMS, RDF, RDFS


class MetricTest(FairTest):
    metric_path = 'RD-R1-3'
    applies_to_principle = 'R1.3'
    title = 'FAIR Metrics Domain Specific - RD-R1.3 Metadata conforms to EJP RD model'
    description = """A domain-specific test for metadata of resources in the Rare Disease domain. It tests if the metadata is structured conforming to the EJP RD DCAT-based metadata model. No failures in the ShEx validation of the metadata content of the resource against the EJP RD ShEx shapes, will be sufficient to pass the test."""
    topics = ['rare-disease']
    
    author = '0000-0003-0169-8159'
    metric_readme_url="https://w3id.org/rd-fairmetrics/RD-R1-3"
    contact_url="https://github.com/LUMC-BioSemantics/RD-FAIRmetrics"
    contact_name="Núria Queralt Rosinach"
    # contact_name="Núria Queralt Rosinach"
    contact_email="n.queralt_rosinach@lumc.nl"
    organization="EJP-RD & ELIXIR Metrics for Rare Disease"

    metric_version = 'Hvst-1.4.0:RD-R1-3-Tst-0.0.3'
    test_test={
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl': 1,
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/catalog.ttl': 0,
    }

    patientregistry_shex = """PREFIX : <http://purl.org/ejp-rd/metadata-model/v1/shex/>
PREFIX dcat:  <http://www.w3.org/ns/dcat#>
PREFIX dct:   <http://purl.org/dc/terms/>
PREFIX ejp:   <http://purl.org/ejp-rd/vocabulary/>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sio:  <http://semanticscience.org/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

:ejprdResourceShape IRI {
    a [ejp:PatientRegistry ejp:Biobank ejp:Guideline dcat:Dataset];
    a [dcat:Resource]*;
    dct:title xsd:string;
    dct:description xsd:string*;
    dcat:theme IRI+;
    foaf:page IRI*
}"""


    def evaluate(self, eval: FairTestEvaluation):
        shex_failed = False

        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        evaluator = ShExEvaluator(g.serialize(format='turtle'), self.patientregistry_shex,
            start="http://purl.org/ejp-rd/metadata-model/v1/shex/ejprdResourceShape",
            # start="http://purl.org/ejp-rd/metadata-model/v1/shex/patientRegistryShape",
        )
        
        # Validate all entities with the following types:
        validate_types = [ 
            URIRef('http://purl.org/ejp-rd/vocabulary/PatientRegistry'), 
            URIRef('http://purl.org/ejp-rd/vocabulary/Biobank'), 
            URIRef('http://purl.org/ejp-rd/vocabulary/Guideline'), 
            URIRef('http://www.w3.org/ns/dcat#Dataset')
        ]
        patient_registry_found = False
        for validate_type in validate_types: 
            
            for s, p, o in g.triples((None, RDF.type, validate_type)):
                patient_registry_found = True
                # print('ShEx evaluate focus entity ' + str(s))
                # For specific RDF format: evaluator.evaluate(rdf_format="json-ld")
                for shex_eval in evaluator.evaluate(focus=str(s)):
                    # comment = comment + f"{result.focus}: "
                    if shex_eval.result:
                        if not shex_failed:
                            eval.success(f'ShEx validation passing for type <{validate_type}> with focus <{shex_eval.focus}>')
                        else:
                            eval.info(f'ShEx validation passing for type <{validate_type}> with focus <{shex_eval.focus}>')
                    else:
                        eval.failure(f'ShEx validation failing for type <{validate_type}> with focus <{shex_eval.focus}> due to {shex_eval.reason}')
                        shex_failed = True

        if patient_registry_found == False:
            eval.failure(f'No subject with the type <http://purl.org/ejp-rd/vocabulary/PatientRegistry> found in the RDF metadata available at <{eval.subject}>')

        return eval.response()

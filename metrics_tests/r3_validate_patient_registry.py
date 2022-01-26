from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from api.metrics_test import MetricResult, MetricInput, yaml_params
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, DC, DCTERMS, RDFS
from pyshex import ShExEvaluator
import requests

metric_id = 'RD-R1-3'
metric_name = "FAIR Metrics Domain Specific - RD-R1.3 Metadata conforms to EJP RD model"
metric_description = """A domain-specific test for metadata of resources in the Rare Disease domain. It tests if the metadata is structured conforming to the EJP RD DCAT-based metadata model. No failures in the ShEx validation of the metadata content of the resource against the EJP RD ShEx shapes, will be sufficient to pass the test."""
metric_version = 'Hvst-1.4.0:RD-R1-3-Tst-0.0.3'

class TestInput(MetricInput):
    subject = 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl'


api = APIRouter()

@api.get(f"/{metric_id}", name=metric_name,
    description=metric_description, response_model=str, response_class=PlainTextResponse(media_type='text/x-yaml'),
)
def metric_yaml() -> str:
    return PlainTextResponse(content=test_yaml, media_type='text/x-yaml')


@api.post(f"/{metric_id}", name=metric_name,
    description=metric_description, response_model=dict,
)            
def metric_test(input: TestInput = Body(...)) -> dict:
    result = MetricResult(subject=input.subject, metric_test=metric_id)
    shex_failed = False

    # Download and parse RDF available at the subject URL
    r = requests.get(input.subject)
    rdf_str = r.text
    # rdf_str = rdf_test
    g = Graph()
    g.parse(data=rdf_str)
    # print(f"Parsed {len(g)} triples")

    evaluator = ShExEvaluator(rdf_str, patientregistry_shex,
        start="http://purl.org/ejp-rd/metadata-model/v1/shex/patientRegistryShape",
    )
    # Check all entities with type ejp:PatientRegistry
    # registry_subjects = g.triples((None, RDF.type, URIRef('http://purl.org/ejp-rd/vocabulary/PatientRegistry')))
    # if len(list(registry_subjects)) < 1:
    #   result.comment = f'FAILURE: No subject with the type <http://purl.org/ejp-rd/vocabulary/PatientRegistry> found in the RDF metadata available at {input.subject}'

    # print(len(list(registry_subjects)))
    # print('registry_subjects')
    # print(registry_subjects)
    # for s, p, o in registry_subjects:
    for s, p, o in g.triples((None, RDF.type, URIRef('http://purl.org/ejp-rd/vocabulary/PatientRegistry'))):
        print('ssss')
        print(s)
        # print('ShEx evaluate focus entity ' + str(s))
        # For specific RDF format: evaluator.evaluate(rdf_format="json-ld")
        for shex_eval in evaluator.evaluate(focus=str(s)):
            # comment = comment + f"{result.focus}: "
            print(shex_eval)
            if shex_eval.result:
                result.comment = result.comment + f'SUCCESS: ShEx validation passing for <{shex_eval.focus}>\n\n'
                if not shex_failed:
                    result.score = 1
            else:
                result.comment = result.comment + f'FAILURE: ShEx validation  failing for <{shex_eval.focus}> due to' + shex_eval.reason + '\n\n'
                shex_failed = True
                result.score = 0

    if not result.comment:
      result.comment = f'FAILURE: No subject with the type <http://purl.org/ejp-rd/vocabulary/PatientRegistry> found in the RDF metadata available at <{input.subject}>'

    return JSONResponse(result.toJsonld())

# x-tests_metric: 'https://w3id.org/rd-fairmetrics/{metric_id}'
test_yaml = f"""swagger: '2.0'
info:
 version: {metric_version}
 title: "{metric_name}"
 x-tests_metric: 'https://rare-disease.api.fair-enough.semanticscience.org/tests/{metric_id}'
 description: >-
  {metric_description}
 x-applies_to_principle: "R1.3"
 contact:
  x-organization: "EJP-RD & ELIXIR Metrics for Rare Disease"
  url: "https://github.com/LUMC-BioSemantics/RD-FAIRmetrics"
  name: 'Núria Queralt Rosinach'
  x-role: "responsible developer"
  email: n.queralt_rosinach@lumc.nl
  x-id: '0000-0003-0169-8159'
host: w3id.org/rd-fairness-tests
basePath: /rest/tests/
schemes:
  - https
paths:
 {metric_id}:
{yaml_params}"""


patientregistry_shex = """PREFIX : <http://purl.org/ejp-rd/metadata-model/v1/shex/>
PREFIX dcat:  <http://www.w3.org/ns/dcat#>
PREFIX dct:   <http://purl.org/dc/terms/>
PREFIX ejp:   <http://purl.org/ejp-rd/vocabulary/>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sio:  <http://semanticscience.org/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
:patientRegistryShape IRI {
  a [ejp:PatientRegistry];
  dct:title xsd:string;
  dct:description xsd:string*;
  ejp:populationCoverage @:populationCoverageShape*;
  dcat:theme IRI+;
  dct:publisher @:organisationShape;
  foaf:page IRI*
}
:locationShape IRI {
  a [dct:Location];
  dct:title xsd:string;
  dct:description xsd:string*;
}
:organisationShape IRI {
  a [foaf:Organisation];
  dct:title xsd:string;
  dct:description xsd:string*;
  dct:spatial @:locationShape*;
  foaf:page IRI*
}
:populationCoverageShape IRI {
  a [sio:SIO_001166];
  rdfs:label ["National" "International" "Regional"]
}"""


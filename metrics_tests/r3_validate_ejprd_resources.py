from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from api.metrics_test import FairEvaluationInput, FairEvaluation, yaml_params
from rdflib import URIRef
from rdflib.namespace import RDF, DC, DCTERMS, RDFS
from pyshex import ShExEvaluator

metric_id = 'RD-R1-3'
metric_name = "FAIR Metrics Domain Specific - RD-R1.3 Metadata conforms to EJP RD model"
metric_description = """A domain-specific test for metadata of resources in the Rare Disease domain. It tests if the metadata is structured conforming to the EJP RD DCAT-based metadata model. No failures in the ShEx validation of the metadata content of the resource against the EJP RD ShEx shapes, will be sufficient to pass the test."""
metric_version = 'Hvst-1.4.0:RD-R1-3-Tst-0.0.3'

class TestInput(FairEvaluationInput):
    subject = 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl'


api = APIRouter()

@api.get(f"/{metric_id}", name=metric_name,
    description=metric_description, response_model=str, response_class=PlainTextResponse(media_type='text/x-yaml'),
)
def metric_yaml() -> str:
    return PlainTextResponse(content=metric_info, media_type='text/x-yaml')


@api.post(f"/{metric_id}", name=metric_name,
    description=metric_description, response_model=dict,
)
def metric_test(input: TestInput = Body(...)) -> dict:
    eval = FairEvaluation(subject=input.subject, metric_id=metric_id, metric_version=metric_version)
    shex_failed = False

    g = eval.getRDF(input.subject)
    if len(g) == 0:
        eval.failure('No RDF found at the subject URL provided.')
        return JSONResponse(eval.toJsonld())

    evaluator = ShExEvaluator(g.serialize(format='turtle'), patientregistry_shex,
        start="http://purl.org/ejp-rd/metadata-model/v1/shex/patientRegistryShape",
    )
    # Validate all entities with type ejp:PatientRegistry
    patient_registry_found = False
    for s, p, o in g.triples((None, RDF.type, URIRef('http://purl.org/ejp-rd/vocabulary/PatientRegistry'))):
        patient_registry_found = True
        # print('ShEx evaluate focus entity ' + str(s))
        # For specific RDF format: evaluator.evaluate(rdf_format="json-ld")
        for shex_eval in evaluator.evaluate(focus=str(s)):
            # comment = comment + f"{result.focus}: "
            print(shex_eval)
            if shex_eval.result:
                if not shex_failed:
                    eval.success(f'ShEx validation passing for <{shex_eval.focus}>')
                else:
                    eval.info(f'ShEx validation passing for <{shex_eval.focus}>')
            else:
                eval.failure(f'ShEx validation failing for <{shex_eval.focus}> due to {shex_eval.reason}')
                shex_failed = True

    if patient_registry_found == False:
      eval.failure(f'No subject with the type <http://purl.org/ejp-rd/vocabulary/PatientRegistry> found in the RDF metadata available at <{input.subject}>')

    return JSONResponse(eval.toJsonld())

# x-tests_metric: 'https://w3id.org/rd-fairmetrics/{metric_id}'
# host: w3id.org/rd-fairness-tests
metric_info = f"""swagger: '2.0'
info:
 version: {metric_version}
 title: "{metric_name}"
 x-tests_metric: 'https://w3id.org/rd-fairmetrics/{metric_id}'
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
basePath: /tests/
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

:ejprdResourceShape IRI {
  a [ejp:PatientRegistry ejp:Biobank ejp:Guideline dcat:Dataset];
  a [dcat:Resource]*;
  dct:title xsd:string;
  dct:description xsd:string*;
  dcat:theme IRI+;
  foaf:page IRI*
}"""

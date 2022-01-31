from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from api.metrics_test import FairEvaluationInput, FairEvaluation, yaml_params
from rdflib import URIRef
from rdflib.namespace import RDF, DC, DCTERMS, RDFS
import requests


metric_id = 'RD-F4'
metric_name = "FAIR Metrics Domain Specific - Use of Rare Disease (RD) specific Search Engines to find the (meta)data of the indexed resource"
metric_description = """We extract the title property of the resource from the metadata document and check if the RD specific search engine returns the metadata document of the resource that we are testing."""
metric_version = 'Hvst-1.4.0:RD-F4-Tst-0.0.3'

class TestInput(FairEvaluationInput):
    subject = 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972'


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
    eval = FairEvaluation(
        subject=input.subject, 
        metric_id=metric_id, 
        metric_version=metric_version
    )
    fdp_search_url = "https://home.fairdatapoint.org/search"

    g = eval.getRDF(input.subject)
    if len(g) == 0:
        eval.failure('No RDF found at the subject URL provided.')
        return JSONResponse(eval.toJsonld())

    # Get the subject resource title from the RDF metadata
    subject_title = None
    title_preds = [ RDFS.label, DC.title, DCTERMS.title, URIRef('http://schema.org/name')]
    for title_pred in title_preds: 
        for s, p, o in g.triples((eval.subject, title_pred, None)):
            subject_title = str(o)
        if subject_title:
            break
    
    # Search if the subject can be found by searching its title in the FAIR Data Point search
    if subject_title:
        payload = {'q': subject_title}
        headers = {
            'Content-Type': "application/json"
        }
        response = requests.post(fdp_search_url, json=payload, headers=headers)
        for res in response.json():
            if res['uri'] == str(eval.subject):
                eval.success('The subject has been found when searching for its title in the FAIR Data Points')
                return JSONResponse(eval.toJsonld())
        eval.failure(f'The subject <{input.subject}> has not been found when searching in the FAIR Data Points for: {subject_title}')
    else:
        eval.failure(f'The subject title could not be found in the resource RDF available at {input.subject}')

    return JSONResponse(eval.toJsonld())


metric_info = f"""swagger: '2.0'
info:
 version: {metric_version}
 title: "{metric_name}"
 x-tests_metric: 'https://w3id.org/rd-fairmetrics/{metric_id}'
 description: >-
   {metric_description}
 x-applies_to_principle: "F4"
 contact:
  x-organization: "EJP-RD & ELIXIR Metrics for Rare Disease"
  url: "https://github.com/LUMC-BioSemantics/RD-FAIRmetrics"
  name: 'Rajaram Kaliyaperumal'
  x-role: "responsible developer"
  email: r.kaliyaperumal@lumc.nl
  x-id: '0000-0002-1215-167X'
host: w3id.org/rd-fairness-tests
basePath: /tests/
schemes:
  - https
paths:
 {metric_id}:
{yaml_params}
"""
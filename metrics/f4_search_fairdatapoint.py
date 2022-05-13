from urllib.parse import urlparse

import requests
from fair_test import FairTest, FairTestEvaluation
from rdflib import URIRef
from rdflib.namespace import DC, DCTERMS, OWL, RDFS, SKOS, VOID, XSD


class MetricTest(FairTest):
    metric_path = 'RD-F4'
    applies_to_principle = 'F4'
    title = 'FAIR Metrics Domain Specific - Use of Rare Disease (RD) specific Search Engines to find the (meta)data of the indexed resource'
    description = """We extract the title property of the resource from the metadata document and check if the RD specific search engine returns the metadata document of the resource that we are testing."""
    topics = ['rare-disease']

    author = '0000-0002-1215-167X'
    metric_readme_url="https://w3id.org/rd-fairmetrics/RD-F4"
    contact_url="https://github.com/LUMC-BioSemantics/RD-FAIRmetrics"
    contact_name="Rajaram Kaliyaperumal"
    contact_email="r.kaliyaperumal@lumc.nl"
    organization="EJP-RD & ELIXIR Metrics for Rare Disease"

    metric_version = 'Hvst-1.4.0:RD-F4-Tst-0.0.3'
    test_test={
        'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972': 1,
        'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl': 0,
    }


    def evaluate(self, eval: FairTestEvaluation):
        fdp_search_url = "https://home.fairdatapoint.org/search"

        g = eval.retrieve_metadata(eval.subject)
        if not isinstance(g, (list, dict)) and len(g) > 0:
            eval.info(f'Successfully found and parsed RDF metadata. It contains {str(len(g))} triples')
        else:
            eval.failure(f"No RDF metadata found at the subject URL {eval.subject}")
            return eval.response()

        # Get the subject resource title from the RDF metadata
        subject_title = None
        title_preds = [ RDFS.label, DC.title, DCTERMS.title, URIRef('http://schema.org/name')]
        for title_pred in title_preds: 
            for s, p, o in g.triples((URIRef(eval.subject), title_pred, None)):
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
                    return eval.response()
            eval.failure(f'The subject <{eval.subject}> has not been found when searching in the FAIR Data Points for: {subject_title}')
        else:
            eval.failure(f'The subject title could not be found in the resource RDF available at {eval.subject}')

        return eval.response()

import pytest
import yaml
import json

eval_list = [
    # f4_search_fairdatapoint.py
    {
        'metric_id': 'RD-F4',
        'subject': 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972',
        'score': 1,
    },
    {
        'metric_id': 'RD-F4',
        'subject': 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl',
        'score': 0,
    },
    # r3_validate_patient_registry.py
    {
        'metric_id': 'RD-R1-3',
        'subject': 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema/master/data/example-rdf/turtle/patientRegistry.ttl',
        'score': 1,
    },
    {
        'metric_id': 'RD-R1-3',
        'subject': 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972',
        'score': 0,
    },
]



metrics_id_to_test = set()
def test_get_yaml(test_api):
    for eval in eval_list:
        metrics_id_to_test.add(eval['metric_id'])
    for metric_id in list(metrics_id_to_test):
        r = test_api.get(f"/tests/{metric_id}")
        assert r.status_code == 200
        api_yaml = yaml.load(r.text, Loader=yaml.FullLoader)
        assert api_yaml['info']['title']
        assert api_yaml['info']['x-applies_to_principle']
        assert api_yaml['info']['x-tests_metric']


def test_post_eval(test_api):
    for eval in eval_list:
        r = test_api.post(f"/tests/{eval['metric_id']}",
            data=json.dumps({ 'subject': eval['subject'] }),
            headers={"Accept": "application/json"}
        )
        print(f"Test posting subject <{eval['subject']}> to {eval['metric_id']} (expect {eval['score']})")
        assert r.status_code == 200
        res = r.json()
        # Check score:
        assert res[0]['http://semanticscience.org/resource/SIO_000300'][0]['@value'] == eval['score']

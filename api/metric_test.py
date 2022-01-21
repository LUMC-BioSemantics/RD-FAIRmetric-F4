from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
import urllib.parse
import json
from rdflib import Graph, URIRef
# Plugin and serializer required to parse jsonld with rdflib

# from app.config import settings
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class MetricInput(BaseModel):
    subject: str


class MetricResult(BaseModel):
    subject: Optional[URIRef]
    comment: str = ''
    score: int = 0
    bonus: int = 0
    softwareVersion: str = '0.1'
    date: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    id: Optional[str]
    metric_test: Optional[str]


    def __init__(self, subject: str, metric_test: str) -> None:
        super().__init__()
        self.subject = URIRef(subject)
        self.metric_test = metric_test
        self.id = f"/metrics/{self.metric_test}#{urllib.parse.quote(str(self.subject))}/result-{self.date}"


    def toJsonld(self):
        return [
            {
                "@id": self.id,
                "@type": [
                    "http://fairmetrics.org/resources/metric_evaluation_result"
                ],
                "http://purl.obolibrary.org/obo/date": [
                    {
                        "@value": self.date,
                        "@type": "http://www.w3.org/2001/XMLSchema#date"
                    }
                ],
                "http://schema.org/softwareVersion": [
                {
                    "@value": self.softwareVersion,
                    "@type": "http://www.w3.org/2001/XMLSchema#float"
                }
                ],
                "http://schema.org/comment": [
                    {
                    "@value": self.comment,
                    "@language": "en"
                    }
                ],
                "http://semanticscience.org/resource/SIO_000332": [
                    {
                    "@value": str(self.subject),
                    "@language": "en"
                    }
                ],
                "http://semanticscience.org/resource/SIO_000300": [
                    {
                    "@value": float(self.score),
                    "@type": "http://www.w3.org/2001/XMLSchema#float"
                    }
                ]
            }
        ]


    class Config:
        arbitrary_types_allowed = True

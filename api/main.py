from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseSettings

from metrics_tests import router


api_router = APIRouter()

# Import tests from the metrics_tests folder:
api_router.include_router(router, prefix='/tests', tags=["FAIR Metrics Tests"])


app = FastAPI(
    title='FAIR Metrics tests API for Rare Disease',
    description="""FAIR Metrics tests API for resources related to research on Rare Disease.

[![Test Metrics](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml/badge.svg)](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml)

[Source code](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4)    
""",
    license_info = {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT"
    },
    contact = {
        "name": "Vincent Emonet",
        "email": "vincent.emonet@gmail.com",
        "url": "https://github.com/vemonet",
    },
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def redirect_root_to_docs():
    """Redirect the route / to /docs"""
    return RedirectResponse(url='/docs')


from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field

from api import f4_search_fairdatapoint, r3_validate_patient_registry


api_router = APIRouter()
api_router.include_router(f4_search_fairdatapoint.api, tags=["RD-FAIRmetric-F4"])
api_router.include_router(r3_validate_patient_registry.api, tags=["RD-FAIRmetric-R1-3"])

app = FastAPI(
    title='FAIR Metrics for Rare Disease',
    description="""FAIR Metrics tests for Rare Disease data.

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

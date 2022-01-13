from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field

from api import fairmetrics_f4


api_router = APIRouter()
api_router.include_router(fairmetrics_f4.router, tags=["RD-FAIRmetric-F4"])


app = FastAPI(
    title='FAIR Metrics',
    description="""Perform evaluations of FAIR Metrics.

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

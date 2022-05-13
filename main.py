from fair_test import FairTestAPI

app = FairTestAPI(
    title='FAIR Metrics tests API for Rare Disease',
    metrics_folder_path='metrics',
    description="""FAIR Metrics tests API for resources related to research on Rare Disease.

[![Test Metrics](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml/badge.svg)](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml)

[Source code](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4)
""",
    license_info = {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT"
    },
    # contact = {
    #     "name": "Vincent Emonet",
    #     "email": "vincent.emonet@gmail.com",
    #     "url": "https://github.com/vemonet",
    # },
)

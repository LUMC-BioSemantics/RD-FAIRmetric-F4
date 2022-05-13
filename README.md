# 🧫 FAIR metrics for Rare Disease research

[![Test Metrics](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml/badge.svg)](https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4/actions/workflows/test.yml)

An API to deploy FAIR metrics tests for the research on Rare Disease community.

FAIR metrics tests are API operations which test if a subject URL is complying with certain requirements defined by a community, they usually check if the resource available at the subject URL complies with the FAIR principles (Findable, Accessible, Interoperable, Reusable).

This API is deployed publicly at **https://rare-disease.api.fair-enough.semanticscience.org**

🗃️ It can be used with the following FAIR evaluation services::

* https://fair-enough.semanticscience.org
* https://fairsharing.github.io/FAIR-Evaluator-FrontEnd

This FAIR Metrics tests API has been built with the [**FAIR test**](https://maastrichtu-ids.github.io/fair-test/) python library.


## 🧑‍💻 Deploy the API

Clone the repository:

```bash
git clone https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4
cd RD-FAIRmetric-F4
```

### 🐳 Development with docker (recommended)

From the root of this repository, run the command below, and access the OpenAPI Swagger UI on http://localhost:8000

```bash
docker-compose up
```

The API will automatically reload on changes to the code.

### 🐍 Development without docker

Note: it has been tested only with Python 3.8

Install dependencies from the source code:

```bash
pip install -e .
```

Start the API locally on http://localhost:8000

```bash
uvicorn main:app --reload
```

### 🚀 In production with docker

We use the `docker-compose.prod.yml` file to define the production deployment configuration.

To start the stack with production config:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

> We use a reverse [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) for docker to route the services.

## ✅ Test the Metrics API

The tests are run automatically by a GitHub Action workflow at every push to the `main` branch.

Add tests using the `test_test` parameter in each metric test in the `metrics` folder.

Run the tests locally with docker-compose:

```bash
docker-compose -f docker-compose.test.yml up --force-recreate
```

You can enable more detailed logs by changing the `command:` in the `docker-compose.test.yml` file to use `pytest -s`

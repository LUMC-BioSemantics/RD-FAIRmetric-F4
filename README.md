# RD-FAIRmetric-F4
RD-FAIRmetric-F4


## Deploy the API

Clone the repository:

```bash
git clone https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4
cd RD-FAIRmetric-F4
```

Install dependencies after cloning the repo:

```bash
pip install -e .
```

Start the API locally after installing the dependencies:

```bash
uvicorn api.main:app --reload
```

Or start it with docker:

```bash
docker-compose up
```

Access it on http://localhost:8000/docs


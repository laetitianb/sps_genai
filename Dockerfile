# Dockerfile
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /code

# deps first for caching
COPY pyproject.toml /code/
RUN uv sync

# install spaCy model WITHOUT pip by using uv's pip shim + model wheel
RUN uv pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl"

# app code
COPY ./app /code/app

EXPOSE 80
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]

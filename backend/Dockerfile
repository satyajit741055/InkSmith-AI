FROM python:3.12-slim

# System deps: build-essential/libpq-dev for psycopg/asyncpg C extensions,
# curl for the healthcheck.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

# Install deps first so this layer is cached unless pyproject/lock change
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Now copy the rest of the backend source
COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
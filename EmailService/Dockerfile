FROM python:3.13-slim AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.13-slim

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

WORKDIR /app

EXPOSE 8000
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8000"]
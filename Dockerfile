# Use Python 3.11 slim as base image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create directory for the app user
RUN mkdir -p /home/app/web && \
    groupadd -r app && \
    useradd -r -g app app && \
    chown -R app:app /home/app

# Set work directory
WORKDIR /home/app/web

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy project
COPY --chown=app:app . .

# Change to non-root user
USER app

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "edu_platform.wsgi:application"]
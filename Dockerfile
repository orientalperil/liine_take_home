# Use official Python runtime as base image
FROM python:3.9-bookworm

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

# Copy project files
COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]

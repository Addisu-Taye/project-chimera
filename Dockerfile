# Project Chimera: Autonomous Influencer Factory
# SRS Trace: §2.3 Operational Environment
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
# Use uv for faster installs (recommended in challenge)
RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache-dir --all-extras

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' chimera
USER chimera

# Default command
CMD ["make", "test"]
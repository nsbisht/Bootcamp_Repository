# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install uv for faster dependency installation (optional but recommended)
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system --no-cache-dir -e .

# Copy application files
COPY . .

# Expose port 2024
EXPOSE 2024

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANGGRAPH_PORT=2024

# Run langgraph dev
CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "2024"]

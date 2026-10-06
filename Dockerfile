# ==========================================
# STAGE 1: BUILDER (The Factory)
# ==========================================
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files & buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv (The ultra-fast rust package manager)
RUN pip install uv==0.1.10

# Create a virtual environment using uv
RUN uv venv /app/.venv

# Copy requirements first to leverage Docker layer caching!
COPY requirements.txt .

# Install dependencies into the virtual environment
# We use 'uv pip install' and point it to the python inside our venv
RUN /app/.venv/bin/uv pip install -r requirements.txt

# ==========================================
# STAGE 2: RUNTIME (The Production Payload)
# ==========================================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add /app/.venv/bin to PATH so we don't have to type the full path to python
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create a non-root user for security (Industry Standard)
RUN useradd -m appuser

# Copy ONLY the virtual environment from the builder stage
# This discards all the pip/uv installation overhead
COPY --from=builder /app/.venv /app/.venv

# Copy the source code
COPY src/ /app/src/

COPY data/ /app/data/

# Ensure the artifacts directory exists and is owned by our non-root user
RUN mkdir -p /app/artifacts && chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# The default command to run when the container starts
CMD ["python", "src/train.py"]
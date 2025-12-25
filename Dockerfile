# Bio-Watcher Backend with Pathway
FROM pathwaycom/pathway:latest

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-pathway.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-pathway.txt

# Copy application code
COPY backend/ ./backend/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY .env .env

# Set Python path
ENV PYTHONPATH=/app

# Expose port for API
EXPOSE 8765

# Run the application
CMD ["python", "backend/main_docker.py"]

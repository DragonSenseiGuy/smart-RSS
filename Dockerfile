# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY app.py ./
COPY templates ./templates
COPY static ./static

# Create data directory for feed storage
RUN mkdir -p data

# Install dependencies using uv
RUN uv sync --frozen

# Expose port 5000 (Flask default)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run Flask application
CMD ["uv", "run", "flask", "run", "--host", "0.0.0.0"]

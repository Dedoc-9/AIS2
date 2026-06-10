FROM python:3.11-slim

WORKDIR /app

# Copy entire repo
COPY . /app

# Install minimal dependencies
RUN pip install --no-cache-dir streamlit

# Create traces directory
RUN mkdir -p /app/traces

# Default command: generate trace and launch dashboard
CMD ["sh", "-c", "cd /app && python examples/minimal_system.py && streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0"]

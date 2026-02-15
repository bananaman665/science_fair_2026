FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy models and code
COPY *.h5 ./
COPY *.json ./
COPY apple_api_regression.py .

# Cloud Run uses PORT env variable
ENV PORT=8080
EXPOSE 8080

# Run with uvicorn
CMD uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}

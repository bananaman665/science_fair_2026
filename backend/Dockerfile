FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and models
COPY apple_api_regression.py .
COPY *.h5 .
COPY model_metadata_regression_*.json .

# Cloud Run uses PORT env variable (default 8080)
ENV PORT=8080
EXPOSE 8080

# Start server
CMD ["sh", "-c", "uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}"]

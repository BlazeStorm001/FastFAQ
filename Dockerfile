# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Default command (will be overridden by docker-compose.override.yml in development)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

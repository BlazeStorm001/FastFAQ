# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI application into the container
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI app using Gunicorn with Uvicorn workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
